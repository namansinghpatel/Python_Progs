# trading/eurusd_1h_wick_detector.py
"""
EURUSD 1H Wick Detector (Aug + Sep 2025)

- Reads manually downloaded EURUSD 1H CSV file.
- Detects high/low wicks (3-bar local high/low rule).
- Saves detected wicks to data/eurusd_wicks_aug_sep_2025.csv.
- Plots Aug+Sep 2025 chart with orange (high) & yellow (low) markers.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone

# ---------- CONFIG ----------
DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

DOWNLOAD_TARGET = DATA_FOLDER / "EURUSD_2025_1H.csv"   # your local dataset
OUTPUT_WICKS_CSV = DATA_FOLDER / "eurusd_wicks_aug_sep_2025.csv"
PLOT_PATH = Path("engulfing_wicks_aug_sep_2025.png")

# Date range we want (in UTC)
START_DATE = pd.Timestamp("2025-08-01T00:00:00Z")
END_DATE   = pd.Timestamp("2025-09-30T23:59:59Z")
# --------------------------------------------


def load_hourly_csv(path: Path) -> pd.DataFrame:
    """
    Load your CSV and convert datetime from 'DD.MM.YYYY HH:MM:SS.000 UTC+05:00' to UTC.
    Example line:
    datetime,Open,High,Low,Close,Volume
    01.08.2025 00:30:00.000 UTC+05:00,1.14262,1.14317,1.14121,1.14121,2747.5
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    print(f"📂 Loading dataset from: {path}")

    # Read file
    df = pd.read_csv(path)

    # Find datetime column (any column with "date" or "time" in name)
    dt_col = next((c for c in df.columns if "date" in c.lower() or "time" in c.lower()), None)
    if dt_col is None:
        raise ValueError("No datetime column found in CSV!")

    # Parse datetime — your format includes a timezone offset (UTC+05:00)
    df["datetime"] = pd.to_datetime(df[dt_col], utc=True, errors="coerce")

    # Convert to pure UTC (your data already includes +05:00)
    df = df.rename(columns=str.lower)
    rename_map = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close"
    }
    df = df.rename(columns=rename_map)

    # Keep only required columns
    df = df[["datetime", "open", "high", "low", "close"]]
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna().set_index("datetime").sort_index()
    print(f"✅ Loaded {len(df)} candles from {df.index.min()} → {df.index.max()}")
    return df


def detect_wicks(df: pd.DataFrame) -> pd.DataFrame:
    """Detect local high/low wicks using 3-bar rule."""
    highs = df["high"].values
    lows = df["low"].values
    idx = df.index
    records = []

    for i in range(1, len(df) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
            records.append({"timestamp": idx[i], "type": "high", "value": highs[i]})
        if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
            records.append({"timestamp": idx[i], "type": "low", "value": lows[i]})

    return pd.DataFrame(records)


def filter_range(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Filter dataframe safely within date range (both UTC)."""
    df = df.sort_index()
    return df.loc[(df.index >= start) & (df.index <= end)]


def plot_wicks(df_hour: pd.DataFrame, wicks_df: pd.DataFrame, plot_path: Path):
    """Plot OHLC and mark wick points."""
    import matplotlib.dates as mdates
    from mplfinance.original_flavor import candlestick_ohlc

    df_plot = df_hour.copy().reset_index()
    df_plot["mpl_date"] = df_plot["datetime"].apply(mdates.date2num)
    ohlc = df_plot[["mpl_date", "open", "high", "low", "close"]].values

    fig, ax = plt.subplots(figsize=(16, 6))
    candlestick_ohlc(ax, ohlc, width=0.03, colorup="g", colordown="r", alpha=0.8)

    for _, row in wicks_df.iterrows():
        x = mdates.date2num(row["timestamp"].to_pydatetime())
        y = row["value"]
        color = "orange" if row["type"] == "high" else "yellow"
        ax.scatter(x, y, marker="o", s=60, color=color, edgecolor="k", zorder=5)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    plt.xticks(rotation=45)
    plt.title("EURUSD 1H Candles (Aug–Sep 2025) with Wick Marks")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.tight_layout()
    fig.savefig(plot_path, dpi=250)
    print(f"📊 Chart saved to: {plot_path.resolve()}")
    plt.show()


def main():
    # 🔹 Load your local dataset
    try:
        df_hour = load_hourly_csv(DOWNLOAD_TARGET)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 🔹 Filter data for Aug + Sep 2025
    df_augsep = filter_range(df_hour, START_DATE, END_DATE)
    if df_augsep.empty:
        print("⚠️ No data found for Aug–Sep 2025 (check timezone alignment).")
        return

    filtered_csv = DATA_FOLDER / "EURUSD_2025_Aug_Sep_1H.csv"
    df_augsep.reset_index().to_csv(filtered_csv, index=False)
    print(f"💾 Saved filtered dataset to: {filtered_csv.resolve()}")

    # 🔹 Detect wicks
    wicks = detect_wicks(df_augsep)
    print(f"✅ Detected {len(wicks)} wick marks (highs/lows).")

    wicks.to_csv(OUTPUT_WICKS_CSV, index=False)
    print(f"💾 Saved wick detections to: {OUTPUT_WICKS_CSV.resolve()}")

    # 🔹 Plot
    df_augsep = df_augsep.reset_index()
    plot_wicks(df_augsep, wicks, PLOT_PATH)


if __name__ == "__main__":
    main()

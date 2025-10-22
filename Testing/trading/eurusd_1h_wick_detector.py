# trading/eurusd_1h_wick_detector.py
"""
EURUSD 1H Wick Detector (Aug + Sep 2025)

- Reads manually downloaded EURUSD 1H CSV file.
- Parses '01.08.2025 00:30:00.000 UTC+05:00' format correctly.
- Detects high/low wicks (3-bar local high/low rule).
- Saves detected wicks to CSV.
- Plots orange (high) and yellow (low) markers on OHLC.
"""

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# ---------- CONFIG ----------
DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

DATA_FILE = DATA_FOLDER / "EURUSD_2025_1H.csv"
OUTPUT_WICKS_CSV = DATA_FOLDER / "eurusd_wicks_aug_sep_2025.csv"
PLOT_PATH = Path("engulfing_wicks_aug_sep_2025.png")

START_DATE = pd.Timestamp("2025-08-01T00:00:00Z")
END_DATE   = pd.Timestamp("2025-09-30T23:59:59Z")
# --------------------------------------------


def load_hourly_csv(path: Path) -> pd.DataFrame:
    """
    Load your CSV and parse datetime with format:
    01.08.2025 00:30:00.000 UTC+05:00
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    print(f"📂 Loading dataset from: {path}")
    df = pd.read_csv(path)

    # Identify datetime column
    dt_col = next((c for c in df.columns if "date" in c.lower() or "time" in c.lower()), None)
    if dt_col is None:
        raise ValueError("No datetime column found!")

    # Parse custom datetime with timezone adjustment
    def parse_custom_datetime(x: str):
        try:
            if "UTC+05" in x:
                x = x.replace(" UTC+05:00", "")
                dt = pd.to_datetime(x, format="%d.%m.%Y %H:%M:%S.%f", errors="coerce")
                return dt - timedelta(hours=5)
            else:
                return pd.to_datetime(x, errors="coerce")
        except Exception:
            return pd.NaT

    df["datetime"] = df[dt_col].apply(parse_custom_datetime)

    # Convert to UTC timezone (make tz-aware)
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize("UTC")

    # Rename and clean columns
    df = df.rename(columns=str.lower)
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["datetime", "open", "high", "low", "close"])
    df = df.set_index("datetime").sort_index()

    print(f"✅ Loaded {len(df)} candles from {df.index.min()} → {df.index.max()}")
    return df[["open", "high", "low", "close"]]


def detect_wicks(df: pd.DataFrame) -> pd.DataFrame:
    """Detect local high/low wicks (3-bar rule)."""
    highs, lows, idx = df["high"].values, df["low"].values, df.index
    records = []
    for i in range(1, len(df) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
            records.append({"timestamp": idx[i], "type": "high", "value": highs[i]})
        if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
            records.append({"timestamp": idx[i], "type": "low", "value": lows[i]})
    return pd.DataFrame(records)


def filter_range(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Ensure tz alignment and safely filter."""
    # Make sure start/end are UTC-aware
    if start.tzinfo is None:
        start = start.tz_localize("UTC")
    if end.tzinfo is None:
        end = end.tz_localize("UTC")

    # Ensure df index is UTC-aware
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")

    return df.loc[(df.index >= start) & (df.index <= end)]


def plot_wicks(df_hour: pd.DataFrame, wicks_df: pd.DataFrame, plot_path: Path):
    """Plot OHLC and wick points."""
    import matplotlib.dates as mdates
    from mplfinance.original_flavor import candlestick_ohlc

    df_plot = df_hour.copy().reset_index()
    df_plot["mpl_date"] = df_plot["datetime"].apply(mdates.date2num)
    ohlc = df_plot[["mpl_date", "open", "high", "low", "close"]].values

    fig, ax = plt.subplots(figsize=(16, 6))
    candlestick_ohlc(ax, ohlc, width=0.03, colorup="g", colordown="r", alpha=0.8)

    for _, r in wicks_df.iterrows():
        x = mdates.date2num(r["timestamp"].to_pydatetime())
        y = r["value"]
        color = "orange" if r["type"] == "high" else "yellow"
        ax.scatter(x, y, s=60, color=color, edgecolor="k", zorder=5)

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
    # Load dataset
    try:
        df_hour = load_hourly_csv(DATA_FILE)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Filter Aug–Sep 2025
    df_augsep = filter_range(df_hour, START_DATE, END_DATE)
    print(f"📆 Filtered candles: {len(df_augsep)}")

    if df_augsep.empty:
        print("⚠️ No candles found in range (check timezone).")
        return

    filtered_csv = DATA_FOLDER / "EURUSD_2025_Aug_Sep_1H.csv"
    df_augsep.reset_index().to_csv(filtered_csv, index=False)
    print(f"💾 Saved filtered dataset to: {filtered_csv.resolve()}")

    # Detect wicks
    wicks = detect_wicks(df_augsep)
    print(f"✅ Detected {len(wicks)} wick marks.")
    wicks.to_csv(OUTPUT_WICKS_CSV, index=False)
    print(f"💾 Saved wick detections to: {OUTPUT_WICKS_CSV.resolve()}")

    # Plot
    df_augsep = df_augsep.reset_index()
    plot_wicks(df_augsep, wicks, PLOT_PATH)


if __name__ == "__main__":
    main()

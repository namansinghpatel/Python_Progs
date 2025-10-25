"""
Download EURUSD 30-Minute Data (2024–2025 Sept) Month-by-Month from Yahoo Finance

Fixes: Yahoo only provides <= 60 days intraday history, so we auto-split by month.

Output: data/EURUSD_30M_2024_2025.csv
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path

# ---------- CONFIG ----------
PAIR = "EURUSD=X"
START = datetime(2024, 1, 1)
END   = datetime(2025, 9, 30)
INTERVAL = "30m"
OUT_CSV = Path("data/EURUSD_30M_2024_2025.csv")
# ----------------------------

def download_chunk(pair, start, end, interval):
    """Download one month of intraday data."""
    try:
        df = yf.download(pair, start=start, end=end, interval=interval, progress=False)
        if df.empty:
            print(f"⚠️ No data for {start:%Y-%m-%d} → {end:%Y-%m-%d}")
            return pd.DataFrame()
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
        df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
        df = df.reset_index().rename(columns={"Datetime":"datetime"})
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        print(f"✅ {start:%b %Y}: {len(df)} bars downloaded")
        return df
    except Exception as e:
        print(f"❌ Error {start:%Y-%m-%d} → {end:%Y-%m-%d}: {e}")
        return pd.DataFrame()

def main():
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    all_data = []

    current = START
    while current < END:
        next_month = current + relativedelta(months=1)
        chunk = download_chunk(PAIR, current, next_month, INTERVAL)
        if not chunk.empty:
            all_data.append(chunk)
        current = next_month

    if not all_data:
        print("❌ No data downloaded at all. Yahoo Finance may be restricting FX intraday data.")
        return

    df_all = pd.concat(all_data).drop_duplicates(subset=["datetime"]).sort_values("datetime")
    df_all.to_csv(OUT_CSV, index=False)
    print(f"\n📁 Saved merged file to: {OUT_CSV.resolve()}")
    print(f"Total bars: {len(df_all)} ({len(df_all)/48:.1f} days of 30m data)")

if __name__ == "__main__":
    main()

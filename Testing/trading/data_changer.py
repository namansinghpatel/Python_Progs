# convert_m1_to_m5_single.py
from pathlib import Path
import pandas as pd

# === CONFIG ===
INPUT_PATH = Path("data/EURUSD_M1_2023.csv")   # your 1-minute file
OUTPUT_PATH = Path("data/EURUSD_M5_2024.csv")  # output 5-minute file

# The columns in your file: 2024.01.01,17:01,1.104270,1.104290,1.104250,1.104290,0
COLS = ["date", "time", "open", "high", "low", "close", "volume"]

# === LOAD ===
print(f"Reading {INPUT_PATH} ...")
df = pd.read_csv(INPUT_PATH, header=None, names=COLS, dtype=str)

# === CLEAN & PARSE ===
# Combine date and time columns into single UTC timestamp
df["datetime"] = pd.to_datetime(df["date"].str.strip() + " " + df["time"].str.strip(),
                                format="%Y.%m.%d %H:%M", utc=True, errors="coerce")

# Drop invalid datetimes if any
df = df.dropna(subset=["datetime"]).copy()

# Convert numeric columns
for c in ["open", "high", "low", "close"]:
    df[c] = pd.to_numeric(df[c].str.strip(), errors="coerce")
df["volume"] = pd.to_numeric(df["volume"].str.strip(), errors="coerce").fillna(0)

# Keep only what’s needed
df = df[["datetime", "open", "high", "low", "close", "volume"]].sort_values("datetime")
df = df.set_index("datetime")

print(f"Loaded {len(df)} M1 candles from {df.index.min()} → {df.index.max()}")

# === RESAMPLE TO M5 ===
ohlc = df[["open","high","low","close"]].resample("5T").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last"
})
vol = df["volume"].resample("5T").sum()

m5 = ohlc.join(vol).dropna(subset=["open"])  # drop empty bars
m5.reset_index(inplace=True)

# === SAVE ===
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
m5.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%dT%H:%M:%SZ")
print(f"✅ Saved {len(m5)} M5 candles to {OUTPUT_PATH}")
print("Datetime range:", m5['datetime'].min(), "→", m5['datetime'].max())

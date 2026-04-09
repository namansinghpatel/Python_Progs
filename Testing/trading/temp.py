import pandas as pd
from pathlib import Path

# Input file (your MT5 export)
INPUT = Path("data/EURUSD_sepoct_M5.csv")
# Output file for your strategy
OUTPUT = Path("data/EURUSD1_M5.csv")

# Read with tab separator and skip meta header lines if any
df = pd.read_csv(INPUT, sep=r'\s+', engine='python')

# Combine <DATE> and <TIME> columns into one datetime
df["datetime"] = pd.to_datetime(df["<DATE>"] + " " + df["<TIME>"],
                                format="%Y.%m.%d %H:%M:%S",
                                errors="coerce")

# Rename to standard names expected by your MACD strategy
df = df.rename(columns={
    "<OPEN>": "open",
    "<HIGH>": "high",
    "<LOW>": "low",
    "<CLOSE>": "close",
    "<TICKVOL>": "volume"
})

# Keep only the required columns
df = df[["datetime", "open", "high", "low", "close", "volume"]]

# Sort by datetime just to be safe
df = df.sort_values("datetime").reset_index(drop=True)

# Save cleaned CSV
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print(f"✅ Converted and saved to: {OUTPUT}")
print(df.head())

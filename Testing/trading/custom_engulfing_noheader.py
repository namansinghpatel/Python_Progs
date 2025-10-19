# custom_engulfing_with_confirmation_and_success.py
import os
import pandas as pd
from pathlib import Path

# ---------- USER SETTINGS ----------
DATA_PATH = r"data\EURUSD_2024_2025.csv"   # or your file path
OUTPUT_CSV = "data\engulfing_with_confirmation.csv"
# -----------------------------------

def load_noheader_data(path):
    df = pd.read_csv(path, header=None)
    df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df = df.set_index("datetime").sort_index()
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna()

def detect_custom_engulfing_with_confirmation(df):
    detections = []
    n = len(df)

    for i in range(1, n - 1):  # we need prev, cur, and next candle
        prev = df.iloc[i - 1]
        cur = df.iloc[i]
        nxt = df.iloc[i + 1]

        # --- Bullish Engulfing ---
        if (cur.low < prev.low) and (cur.close > prev.open):
            high_break = nxt.high > cur.high
            low_break = nxt.low < cur.low

            confirmed = False
            if high_break and not low_break:
                confirmed = True
            elif high_break and low_break:
                # decide which was likely broken first using proximity to next open
                dist_high = abs(nxt.open - cur.high)
                dist_low = abs(nxt.open - cur.low)
                confirmed = dist_high < dist_low  # closer to open = broken first

            detections.append({
                "timestamp": df.index[i],
                "pattern": "bullish",
                "engulf_high": cur.high,
                "engulf_low": cur.low,
                "next_open": nxt.open,
                "next_high": nxt.high,
                "next_low": nxt.low,
                "confirmed": confirmed
            })

        # --- Bearish Engulfing ---
        if (cur.high > prev.high) and (cur.close < prev.open):
            high_break = nxt.high > cur.high
            low_break = nxt.low < cur.low

            confirmed = False
            if low_break and not high_break:
                confirmed = True
            elif high_break and low_break:
                dist_high = abs(nxt.open - cur.high)
                dist_low = abs(nxt.open - cur.low)
                confirmed = dist_low < dist_high

            detections.append({
                "timestamp": df.index[i],
                "pattern": "bearish",
                "engulf_high": cur.high,
                "engulf_low": cur.low,
                "next_open": nxt.open,
                "next_high": nxt.high,
                "next_low": nxt.low,
                "confirmed": confirmed
            })

    return pd.DataFrame(detections)

def append_success_rate_to_csv(df, out_path):
    # calculate total, confirmed, and success rate
    bull = df[df.pattern == "bullish"]
    bear = df[df.pattern == "bearish"]

    total_bull = len(bull)
    total_bear = len(bear)
    confirmed_bull = bull[bull.confirmed == True].shape[0]
    confirmed_bear = bear[bear.confirmed == True].shape[0]

    bull_rate = (confirmed_bull / total_bull * 100) if total_bull > 0 else 0
    bear_rate = (confirmed_bear / total_bear * 100) if total_bear > 0 else 0

    overall_total = total_bull + total_bear
    overall_confirmed = confirmed_bull + confirmed_bear
    overall_rate = (overall_confirmed / overall_total * 100) if overall_total > 0 else 0

    # Save main detections
    df.to_csv(out_path, index=False)

    # Append summary lines
    with open(out_path, "a", encoding="utf-8") as f:
        f.write("\n# === SUCCESS RATE SUMMARY ===\n")
        f.write(f"# Bullish Confirmed: {confirmed_bull}/{total_bull} ({bull_rate:.2f}%)\n")
        f.write(f"# Bearish Confirmed: {confirmed_bear}/{total_bear} ({bear_rate:.2f}%)\n")
        f.write(f"# Overall Confirmed: {overall_confirmed}/{overall_total} ({overall_rate:.2f}%)\n")

    return {
        "bullish_rate": bull_rate,
        "bearish_rate": bear_rate,
        "overall_rate": overall_rate
    }

def main():
    print("Loading data...")
    df = load_noheader_data(DATA_PATH)
    print(f"Loaded {len(df)} rows from {df.index.min()} → {df.index.max()}")

    result = detect_custom_engulfing_with_confirmation(df)

    out_path = os.path.abspath(OUTPUT_CSV)
    rates = append_success_rate_to_csv(result, out_path)

    print("\n=== ENGULFING SUMMARY ===")
    print(f"✅ Bullish success rate: {rates['bullish_rate']:.2f}%")
    print(f"❌ Bearish success rate: {rates['bearish_rate']:.2f}%")
    print(f"📊 Overall success rate: {rates['overall_rate']:.2f}%")
    print(f"\nResults saved to: {out_path}")
    print("\nSample detections:\n", result.head(10).to_string(index=False))

if __name__ == "__main__":
    main()


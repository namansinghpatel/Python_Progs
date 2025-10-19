# custom_engulfing_with_chart_final_confirmed_fixed.py
import os
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

# ---------- USER SETTINGS ----------
DATA_PATH = r"data\EURUSD_2024_2025.csv"                 # input file path
OUTPUT_CSV = r"data\engulfing_with_confirmation.csv"     # output file path
SHOW_PLOT = True             # show chart
PLOT_LAST_MONTHS = 1         # number of months to show on chart
# -----------------------------------

def load_noheader_data(path):
    """Load CSV without headers (expects datetime,open,high,low,close,volume)."""
    df = pd.read_csv(path, header=None)
    df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df = df.set_index("datetime").sort_index()
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna()

def detect_custom_engulfing_with_confirmation(df):
    """Detect custom engulfing patterns and confirmation using next candle."""
    detections = []
    n = len(df)
    for i in range(1, n - 1):
        prev = df.iloc[i - 1]
        cur = df.iloc[i]
        nxt = df.iloc[i + 1]

        # Bullish engulfing (your rule): sweep below prev low and close above prev open
        if (cur.low < prev.low) and (cur.close > prev.open):
            high_break = nxt.high > cur.high
            low_break = nxt.low < cur.low
            confirmed = False
            if high_break and not low_break:
                confirmed = True
            elif high_break and low_break:
                dist_high = abs(nxt.open - cur.high)
                dist_low = abs(nxt.open - cur.low)
                confirmed = dist_high < dist_low
            detections.append({
                "timestamp": df.index[i],
                "pattern": "bullish",
                "engulf_high": cur.high,
                "engulf_low": cur.low,
                "confirmed": confirmed
            })

        # Bearish engulfing (your rule): sweep above prev high and close below prev open
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
                "confirmed": confirmed
            })
    return pd.DataFrame(detections)

def append_success_rate_to_csv(df, out_path):
    """Save detections and append success-rate summary to the same CSV."""
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

    # ensure output directory exists
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # save DataFrame
    df.to_csv(out_path, index=False)
    # append summary
    with open(out_path, "a", encoding="utf-8") as f:
        f.write("\n# === SUCCESS RATE SUMMARY ===\n")
        f.write(f"# Bullish Confirmed: {confirmed_bull}/{total_bull} ({bull_rate:.2f}%)\n")
        f.write(f"# Bearish Confirmed: {confirmed_bear}/{total_bear} ({bear_rate:.2f}%)\n")
        f.write(f"# Overall Confirmed: {overall_confirmed}/{overall_total} ({overall_rate:.2f}%)\n")

    return bull_rate, bear_rate, overall_rate

def plot_engulfings(df_full, detections, months=1):
    """
    Plot last `months` months of df_full.
    Mark confirmed engulfings with green up-triangle (below candle)
    and unconfirmed with red down-triangle (above candle).
    """
    # copy portion to plot
    end_date = df_full.index.max()
    start_date = end_date - pd.DateOffset(months=months)
    df = df_full.loc[start_date:end_date].copy()
    det = detections[(detections["timestamp"] >= start_date) & (detections["timestamp"] <= end_date)].copy()

    print(f"\nPlotting last {months} month(s): {df.index.min()} → {df.index.max()}")

    # Create marker series aligned with df index (full-length)
    marker_series = pd.Series(index=df.index, dtype="float64")
    color_series = pd.Series(index=df.index, dtype="object")

    # fill markers
    for _, row in det.iterrows():
        ts = row["timestamp"]
        if ts in marker_series.index:
            if row["confirmed"]:
                # green up-triangle plotted slightly below low
                marker_series.loc[ts] = df.loc[ts, "low"] * 0.999
                color_series.loc[ts] = "green"
            else:
                # red down-triangle plotted slightly above high
                marker_series.loc[ts] = df.loc[ts, "high"] * 1.001
                color_series.loc[ts] = "red"

    # Build color-specific series (full-length) to pass to mplfinance
    green_series = marker_series.where(color_series == "green")
    red_series = marker_series.where(color_series == "red")

    add_plots = []
    if green_series.notna().any():
        add_plots.append(mpf.make_addplot(green_series, type='scatter', markersize=70, marker="^", color="green"))
    if red_series.notna().any():
        add_plots.append(mpf.make_addplot(red_series, type='scatter', markersize=70, marker="v", color="red"))

    # Use returnfig=True to capture the figure and save it reliably
    fig, axlist = mpf.plot(
        df,
        type="candle",
        addplot=add_plots,
        volume=False,
        style="charles",
        title=f"EURUSD 4H Engulfing Patterns (Last {months} Month{'s' if months>1 else ''})",
        ylabel="Price",
        figsize=(14,7),
        returnfig=True
    )

    # Save chart to file next to script (or you can change path)
    save_path = os.path.abspath(f"engulfing_chart_last{months}month.png")
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"\n📸 Chart saved to: {save_path}")

    plt.show()

def main():
    # load
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: input file not found: {DATA_PATH}")
        return

    df = load_noheader_data(DATA_PATH)
    print(f"Loaded {len(df)} rows from {df.index.min()} → {df.index.max()}")

    # detect
    detections = detect_custom_engulfing_with_confirmation(df)
    # ensure output dir exists
    out_abspath = os.path.abspath(OUTPUT_CSV)
    out_dir = os.path.dirname(out_abspath)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # save results + summary
    bull_rate, bear_rate, overall_rate = append_success_rate_to_csv(detections, out_abspath)

    print("\n=== ENGULFING SUMMARY ===")
    print(f"✅ Bullish success rate: {bull_rate:.2f}%")
    print(f"❌ Bearish success rate: {bear_rate:.2f}%")
    print(f"📊 Overall success rate: {overall_rate:.2f}%")
    print(f"\nResults saved to: {out_abspath}")

    # plot last N months
    if SHOW_PLOT:
        plot_engulfings(df, detections, months=PLOT_LAST_MONTHS)

if __name__ == "__main__":
    main()

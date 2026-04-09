# diagnose_missed_breakouts.py
from pathlib import Path
import pandas as pd
import numpy as np

DATA_PATH = Path("data/EURUSD_M5.csv")
PIP = 0.0001

# Config copies (use same as strategy)
FAST = 12
SLOW = 26
SIGNAL = 9
ATR_PERIOD = 14
ENTRY_START_HOUR_UTC = 1
ENTRY_END_HOUR_UTC = 23
MIN_SEGMENT_LEN = 3
SL_ATR_MULT = 1
MIN_SL_PIPS = 4
RETRACE_FACTOR = 0.382

def load_csv(path):
    df = pd.read_csv(path, parse_dates=["datetime"])
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df = df.dropna(subset=["datetime"]).reset_index(drop=True)
    for c in ["open","high","low","close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if "volume" not in df.columns:
        df["volume"] = np.nan
    return df[["datetime","open","high","low","close","volume"]]

def compute_macd_histogram(df):
    ema_fast = df["close"].ewm(span=FAST, adjust=False).mean()
    ema_slow = df["close"].ewm(span=SLOW, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal = macd_line.ewm(span=SIGNAL, adjust=False).mean()
    df["macd_hist"] = macd_line - signal
    return df

def detect_macd_highs_lows(df):
    temp = df.copy().reset_index(drop=True)
    temp["above_zero"] = temp["macd_hist"] > 0
    temp["zone_change"] = temp["above_zero"].ne(temp["above_zero"].shift(1))
    change_idxs = temp.index[temp["zone_change"]].tolist()
    if 0 not in change_idxs:
        change_idxs = [0] + change_idxs
    if change_idxs[-1] != len(temp) - 1:
        change_idxs.append(len(temp) - 1)

    recs=[]
    for i in range(len(change_idxs)-1):
        s,e = change_idxs[i], change_idxs[i+1]
        seg = temp.iloc[s:e]
        if len(seg) < MIN_SEGMENT_LEN:
            continue
        if seg["above_zero"].iloc[0]:
            idx_max = seg["high"].idxmax()
            row = seg.loc[idx_max]
            recs.append({"type":"MACD_High","datetime":row["datetime"], "price":float(row["high"]), "index": int(idx_max)})
        else:
            idx_min = seg["low"].idxmin()
            row = seg.loc[idx_min]
            recs.append({"type":"MACD_Low","datetime":row["datetime"], "price":float(row["low"]), "index": int(idx_min)})
    return pd.DataFrame(recs)

def compute_atr(df, period=ATR_PERIOD):
    df = df.copy()
    df["prev_close"] = df["close"].shift(1)
    df["tr"] = np.maximum(df["high"]-df["low"],
                         np.maximum((df["high"]-df["prev_close"]).abs(),
                                    (df["low"]-df["prev_close"]).abs()))
    df["atr"] = df["tr"].rolling(window=period, min_periods=period).mean()
    return df

def compute_big_atr(df, period=ATR_PERIOD, resample_rule="60min"):
    tmp = df.set_index("datetime")[["open","high","low","close"]].copy()
    ohlc = tmp.resample(resample_rule).agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
    ohlc["prev_close"] = ohlc["close"].shift(1)
    ohlc["tr"] = np.maximum(ohlc["high"]-ohlc["low"],
                            np.maximum((ohlc["high"]-ohlc["prev_close"]).abs(),
                                       (ohlc["low"]-ohlc["prev_close"]).abs()))
    ohlc["atr_big"] = ohlc["tr"].rolling(window=period, min_periods=period).mean()
    ohlc = ohlc.reset_index().rename(columns={"datetime":"ts_period"})
    ohlc = ohlc.dropna(subset=["atr_big"])
    merged = pd.merge_asof(df.sort_values("datetime"),
                           ohlc[["ts_period","atr_big"]].sort_values("ts_period"),
                           left_on="datetime", right_on="ts_period", direction="backward")
    merged.drop(columns=["ts_period"], inplace=True)
    return merged

def analyze():
    df = load_csv(DATA_PATH)
    df = compute_macd_histogram(df)
    df = compute_atr(df)
    df = compute_big_atr(df)
    levels = detect_macd_highs_lows(df)

    # Build simple map for fast lookup (timestamp -> level record)
    level_map = {pd.to_datetime(r["datetime"]): r for _, r in levels.iterrows()}

    missed = []
    ok = []
    for idx, lvl in levels.iterrows():
        lvl_ts = pd.to_datetime(lvl["datetime"])
        lvl_price = float(lvl["price"])
        lvl_index = int(lvl["index"])
        # The strategy uses the level when ts == level timestamp to set current_high/current_low.
        # Check the breakout boolean at that SAME index (prev < level and close > level)
        if lvl_index == 0:
            continue
        prev = df.iloc[lvl_index - 1]
        candle = df.iloc[lvl_index]
        reason = []
        # Check ATR availability at that candle
        if pd.isna(candle.get("atr")) or pd.isna(candle.get("atr_big")):
            reason.append("ATR_missing")
        # Hour filter
        if not (ENTRY_START_HOUR_UTC <= candle["datetime"].hour <= ENTRY_END_HOUR_UTC):
            reason.append("Hour_filtered")
        # prev/close condition
        prev_below = prev["close"] < lvl_price
        close_above = candle["close"] > lvl_price
        if not (prev_below and close_above):
            reason.append(f"breakout_condition_false(prev_close={prev['close']:.5f}, lvl={lvl_price:.5f}, close={candle['close']:.5f})")
        # If no reason -> candidate breakout (should have created pending)
        if len(reason) == 0:
            ok.append({"index": lvl_index, "ts": lvl_ts, "price": lvl_price})
        else:
            missed.append({"index": lvl_index, "ts": lvl_ts, "price": lvl_price, "reasons": reason})

    print("=== Diagnostic Summary ===")
    print(f"Total MACD levels detected: {len(levels)}")
    print(f"Candidate breakouts at level-timestamps (prev<level && close>level and ATR/hours OK): {len(ok)}")
    print(f"Levels that fail immediate breakout condition or filters: {len(missed)}")
    print("\nSample candidate breakouts (first 10):")
    for s in ok[:10]:
        print(s)
    print("\nSample missed levels and reasons (first 20):")
    for m in missed[:20]:
        print(m)

    # Save CSVs for deeper analysis
    pd.DataFrame(ok).to_csv("diagnostic_ok_candidates.csv", index=False)
    pd.DataFrame(missed).to_csv("diagnostic_missed_levels.csv", index=False)
    print("\nSaved diagnostic_ok_candidates.csv and diagnostic_missed_levels.csv")

if __name__ == "__main__":
    analyze()

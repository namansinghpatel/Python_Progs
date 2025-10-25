"""
MACD Breakout Strategy — No Plot, use yfinance CSV input

- Input CSV: data/EURUSD_1H.csv (from yfinance). Expected columns:
    - either with header: datetime, open, high, low, close, volume
    - or headerless rows like: 2025-09-10 00:00:00+00:00,1.17,1.17,1.17,1.17,0
- Strategy:
    - Detect MACD histogram highs/lows (skip segments shorter than MIN_SEGMENT_LEN)
    - Immediate entry when a candle CLOSE breaks the current MACD high/low
    - Entry price = candle.close
    - SL = entry ± (ATR_MULT * ATR(14))
    - TP = entry ∓ (ATR_MULT * ATR(14))  [1:1]
    - Only one trade active at a time
- Output: data/macd_breakout_trades.csv and printed stats
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ---------- CONFIG ----------
DATA_PATH = Path("data/EURUSD_1H.csv")         # input CSV (from yfinance)
OUT_PATH  = Path("data/macd_breakout_trades.csv")
FAST = 12
SLOW = 26
SIGNAL = 9
ATR_PERIOD = 14
ATR_MULT = 2.0
MIN_SEGMENT_LEN = 3
PIP = 0.0001
# ----------------------------

def load_csv_flexible(path: Path) -> pd.DataFrame:
    """
    Load CSV that may either have a header or not.
    Handles timezone-aware ISO-like datetimes (e.g. 2025-09-10 00:00:00+00:00).
    Returns DataFrame with columns: datetime (pd.Timestamp), open, high, low, close, volume
    """
    txt = path.read_text(encoding="utf-8")
    # Try reading with header first
    try:
        df = pd.read_csv(path, parse_dates=["datetime"], infer_datetime_format=True)
        cols_lower = [c.lower() for c in df.columns]
        # If required columns exist, normalize names and return
        if set(["datetime","open","high","low","close"]).issubset(cols_lower):
            # normalize column names to lower
            df.columns = [c.lower() for c in df.columns]
            # ensure datetime parsed (force)
            df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
            df = df.dropna(subset=["datetime"]).reset_index(drop=True)
            # make sure OHLC numeric
            for c in ["open","high","low","close"]:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            return df[["datetime","open","high","low","close","volume"]]
        # else fallthrough to headerless parse
    except Exception:
        pass

    # Headerless: assume 6 columns per row: datetime,open,high,low,close,volume
    df2 = pd.read_csv(path, header=None)
    if df2.shape[1] < 5:
        raise ValueError("CSV appears to have too few columns. Expected datetime,open,high,low,close,...")
    # keep first 6 columns
    df2 = df2.iloc[:, :6]
    df2.columns = ["datetime","open","high","low","close","volume"]
    # parse datetime: yfinance typically uses ISO with timezone. pandas can parse it.
    df2["datetime"] = pd.to_datetime(df2["datetime"], utc=True, errors="coerce")
    df2 = df2.dropna(subset=["datetime"]).reset_index(drop=True)
    for c in ["open","high","low","close"]:
        df2[c] = pd.to_numeric(df2[c], errors="coerce")
    return df2[["datetime","open","high","low","close","volume"]]

def compute_macd_histogram(df: pd.DataFrame) -> pd.DataFrame:
    """Compute MACD histogram and append column macd_hist."""
    ema_fast = df["close"].ewm(span=FAST, adjust=False).mean()
    ema_slow = df["close"].ewm(span=SLOW, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal = macd_line.ewm(span=SIGNAL, adjust=False).mean()
    df["macd_hist"] = macd_line - signal
    return df

def compute_atr(df: pd.DataFrame, period: int = ATR_PERIOD) -> pd.DataFrame:
    """Compute ATR(period) stored in column 'atr'."""
    df["prev_close"] = df["close"].shift(1)
    df["tr"] = np.maximum(df["high"] - df["low"],
                          np.maximum((df["high"] - df["prev_close"]).abs(),
                                     (df["low"] - df["prev_close"]).abs()))
    df["atr"] = df["tr"].rolling(window=period, min_periods=period).mean()
    return df

def detect_macd_highs_lows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect MACD highs/lows by grouping consecutive histogram-above-zero and below-zero segments.
    For above-zero segments: take the candle with highest 'high' (wick top) -> MACD_High.
    For below-zero segments: take the candle with lowest 'low' -> MACD_Low.
    Skip segments shorter than MIN_SEGMENT_LEN.
    Returns DataFrame with columns ['type','datetime','price'].
    """
    temp = df.copy().reset_index(drop=True)
    temp["above_zero"] = temp["macd_hist"] > 0
    temp["zone_change"] = temp["above_zero"].ne(temp["above_zero"].shift(1))
    change_idxs = temp.index[temp["zone_change"]].tolist()
    if 0 not in change_idxs:
        change_idxs = [0] + change_idxs
    if change_idxs[-1] != len(temp) - 1:
        change_idxs.append(len(temp) - 1)

    recs = []
    for i in range(len(change_idxs) - 1):
        s = change_idxs[i]
        e = change_idxs[i+1]
        seg = temp.iloc[s:e]
        if len(seg) < MIN_SEGMENT_LEN:
            continue
        if seg["above_zero"].iloc[0]:
            # above zero segment -> MACD_High
            idx_max = seg["high"].idxmax()
            row = seg.loc[idx_max]
            recs.append({"type":"MACD_High","datetime": row["datetime"], "price": float(row["high"])})
        else:
            idx_min = seg["low"].idxmin()
            row = seg.loc[idx_min]
            recs.append({"type":"MACD_Low","datetime": row["datetime"], "price": float(row["low"])})
    return pd.DataFrame(recs)

def run_strategy_immediate_entry(df: pd.DataFrame, levels_df: pd.DataFrame) -> pd.DataFrame:
    """
    Core strategy loop (no plotting).
    - Immediate entry on the candle close that crosses current_high/current_low.
    - Entry price = candle.close
    - SL = entry +/- ATR_MULT * atr
    - TP = entry +/- ATR_MULT * atr (1:1)
    - Only one trade active at a time.
    """
    df = df.copy().reset_index(drop=True)
    trades = []
    active_trade = None
    current_high = None
    current_low = None

    # build mapping from timestamp -> level
    level_map = {}
    if not levels_df.empty:
        for _, r in levels_df.iterrows():
            level_map[pd.Timestamp(r["datetime"])] = (r["type"], float(r["price"]))

    # iterate candles
    for i in range(1, len(df)):
        candle = df.iloc[i]
        prev = df.iloc[i-1]
        ts = candle["datetime"]

        # update levels if a level occurs at this candle timestamp
        if ts in level_map:
            typ, price = level_map[ts]
            if typ == "MACD_High":
                current_high = price
            else:
                current_low = price
            # when new level forms, per rule previous pending/levels are considered superseded

        # if a trade is active, check exits (TP/SL) and skip opening new trades
        if active_trade is not None:
            if active_trade["type"] == "buy":
                # SL first, then TP (order of checks minimal, both within same candle handled by precedence)
                if candle["low"] <= active_trade["sl"]:
                    active_trade["exit_time"] = ts
                    active_trade["exit_price"] = float(active_trade["sl"])
                    active_trade["result"] = "SL"
                    trades.append(active_trade)
                    active_trade = None
                elif candle["high"] >= active_trade["tp"]:
                    active_trade["exit_time"] = ts
                    active_trade["exit_price"] = float(active_trade["tp"])
                    active_trade["result"] = "TP"
                    trades.append(active_trade)
                    active_trade = None
            else:  # sell
                if candle["high"] >= active_trade["sl"]:
                    active_trade["exit_time"] = ts
                    active_trade["exit_price"] = float(active_trade["sl"])
                    active_trade["result"] = "SL"
                    trades.append(active_trade)
                    active_trade = None
                elif candle["low"] <= active_trade["tp"]:
                    active_trade["exit_time"] = ts
                    active_trade["exit_price"] = float(active_trade["tp"])
                    active_trade["result"] = "TP"
                    trades.append(active_trade)
                    active_trade = None
            # if active_trade existed, we either closed it this candle or continue holding; do not open new trades this iteration
            continue

        # ATR must be present to size SL/TP
        if pd.isna(candle.get("atr", np.nan)):
            continue

        # BUY immediate entry condition: prev.close < current_high and candle.close > current_high
        if current_high is not None and prev["close"] < current_high and candle["close"] > current_high:
            entry_price = float(candle["close"])
            atr = float(candle["atr"])
            sl = entry_price - (ATR_MULT * atr)
            tp = entry_price + (ATR_MULT * atr)
            active_trade = {
                "type": "buy",
                "entry_time": ts,
                "entry_price": entry_price,
                "sl": sl,
                "tp": tp,
                "exit_time": None,
                "exit_price": None,
                "result": None
            }
            continue

        # SELL immediate entry condition
        if current_low is not None and prev["close"] > current_low and candle["close"] < current_low:
            entry_price = float(candle["close"])
            atr = float(candle["atr"])
            sl = entry_price + (ATR_MULT * atr)
            tp = entry_price - (ATR_MULT * atr)
            active_trade = {
                "type": "sell",
                "entry_time": ts,
                "entry_price": entry_price,
                "sl": sl,
                "tp": tp,
                "exit_time": None,
                "exit_price": None,
                "result": None
            }
            continue

    # if active trade remains open at end of data, mark TIMEOUT and exit at final close
    if active_trade is not None:
        final_close = float(df.iloc[-1]["close"])
        active_trade["exit_time"] = df.iloc[-1]["datetime"]
        active_trade["exit_price"] = final_close
        active_trade["result"] = "TIMEOUT"
        trades.append(active_trade)
        active_trade = None

    trades_df = pd.DataFrame(trades)
    if not trades_df.empty:
        # calculate pips: positive for profitable trades
        trades_df["pips"] = trades_df.apply(
            lambda r: ((r["exit_price"] - r["entry_price"]) * (1 if r["type"] == "buy" else -1)) / PIP,
            axis=1
        )
    return trades_df

def print_stats(trades_df: pd.DataFrame):
    if trades_df.empty:
        print("No trades taken.")
        return
    total = len(trades_df)
    wins = (trades_df["result"] == "TP").sum()
    losses = (trades_df["result"] == "SL").sum()
    timeouts = (trades_df["result"] == "TIMEOUT").sum()
    winrate = 100 * wins / (wins + losses) if (wins + losses) > 0 else 0.0
    net_pips = trades_df["pips"].sum() if "pips" in trades_df.columns else 0.0

    print("=== Strategy Performance ===")
    print(f"Total trades : {total}")
    print(f"Wins         : {wins}")
    print(f"Losses       : {losses}")
    print(f"Timeouts     : {timeouts}")
    print(f"Winrate      : {winrate:.2f}% (calculated over finished trades)")
    print(f"Net pips     : {net_pips:.1f}")

def main():
    # load
    df = load_csv_flexible(DATA_PATH)
    if df.empty:
        print("No data loaded.")
        return

    # ensure datetime sorted
    df = df.sort_values("datetime").reset_index(drop=True)

    # compute indicators
    df = compute_macd_histogram(df)
    df = compute_atr(df, ATR_PERIOD)

    # detect levels
    levels_df = detect_macd_highs_lows(df)
    print(f"Detected {len(levels_df)} MACD highs/lows (segments >= {MIN_SEGMENT_LEN} bars).")

    # run strategy
    trades_df = run_strategy_immediate_entry(df, levels_df)

    # save and stats
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    trades_df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(trades_df)} trades to: {OUT_PATH}")
    print_stats(trades_df)

if __name__ == "__main__":
    main()

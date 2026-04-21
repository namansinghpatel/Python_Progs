import pandas as pd

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("eurusd_15m_oanda.csv")

# Required columns:
# datetime, open, high, low, close, volume

df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
df.set_index("datetime", inplace=True)

# =========================
# CALCULATE 50 EMA
# =========================
df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()

results = []
trade_log = []

# ==================================================
# TIME FILTER (UTC STRICT)
# ONLY entries from:
# 00:30 to 16:45 inclusive
# ==================================================
def allowed_time(ts):
    h = ts.hour
    m = ts.minute
    total_min = h * 60 + m

    start_min = 30          # 00:30
    end_min = 16 * 60 + 45  # 16:45

    return start_min <= total_min <= end_min

# ==================================================
# ONE TRADE AT A TIME
# ==================================================
i = 50

while i < len(df) - 1:

    prev = df.iloc[i - 1]
    curr = df.iloc[i]

    # ==========================================
    # STRICT ENTRY TIME FILTER
    # ==========================================
    if not allowed_time(curr.name):
        i += 1
        continue

    direction = None

    # ==========================================
    # ENGULFING LOGIC
    # ==========================================

    # Bullish
    if (prev['close'] < prev['open'] and
        curr['low'] < prev['low'] and
        curr['close'] > prev['open']):
        direction = "BUY"

    elif (prev['close'] > prev['open'] and
          curr['low'] < prev['low'] and
          curr['close'] > prev['close']):
        direction = "BUY"

    # Bearish
    elif (prev['close'] > prev['open'] and
          curr['high'] > prev['high'] and
          curr['close'] < prev['open']):
        direction = "SELL"

    elif (prev['close'] < prev['open'] and
          curr['high'] > prev['high'] and
          curr['close'] < prev['close']):
        direction = "SELL"

    if direction is None:
        i += 1
        continue

    # ==========================================
    # ENTRY
    # ==========================================
    entry = curr["close"]
    entry_time = curr.name
    ema_now = curr["ema50"]

    # ==========================================
    # STOPLOSS = previous candle
    # ==========================================
    if direction == "BUY":
        sl = prev["low"]
        risk = entry - sl
    else:
        sl = prev["high"]
        risk = sl - entry

    if risk <= 0:
        i += 1
        continue

    # TP = 1:2
    if direction == "BUY":
        tp = entry + 2 * risk
    else:
        tp = entry - 2 * risk

    # ==========================================
    # TRADE MANAGEMENT
    # ==========================================
    R_value = None
    exit_index = None

    for j in range(i + 1, len(df)):

        f = df.iloc[j]
        ema_live = f["ema50"]

        # ======================================
        # EMA MOVING TP
        # ======================================
        if direction == "BUY":
            if entry < ema_now and tp > ema_live:
                tp = ema_live

        if direction == "SELL":
            if entry > ema_now and tp < ema_live:
                tp = ema_live

        # BUY
        if direction == "BUY":

            if f["low"] <= sl:
                R_value = -1
                exit_index = j
                break

            if f["high"] >= tp:
                R_value = round((tp - entry) / risk, 2)
                exit_index = j
                break

        # SELL
        else:

            if f["high"] >= sl:
                R_value = -1
                exit_index = j
                break

            if f["low"] <= tp:
                R_value = round((entry - tp) / risk, 2)
                exit_index = j
                break

    # ==========================================
    # STORE TRADE
    # ==========================================
    if R_value is not None:

        results.append(R_value)

        trade_log.append({
            "datetime": entry_time,
            "day": entry_time.day_name(),
            "direction": direction,
            "entry_price": entry,
            "R_result": R_value
        })

        # No trade on same candle as exit
        i = exit_index + 1

    else:
        i += 1

# ==========================================
# SAVE CSV
# ==========================================
trade_df = pd.DataFrame(trade_log)
trade_df.to_csv("engulfing_rr2_trades.csv", index=False)

# ==========================================
# RESULTS
# ==========================================
total = len(results)
wins = sum(1 for r in results if r > 0)
losses = sum(1 for r in results if r == -1)

print("========== RESULTS ==========")
print("Total Trades:", total)
print("Wins:", wins)
print("Losses:", losses)

if total > 0:
    print("Win Rate:", round(wins / total, 3))
    print("Average R:", round(sum(results) / total, 3))

print("CSV Saved: engulfing_rr2_trades.csv")
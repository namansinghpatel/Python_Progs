import pandas as pd

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("nzdusd_4h_oanda.csv")

df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)

results = []
trade_log = []

# =========================
# LOOP
# =========================
for i in range(1, len(df)-1):

    prev = df.iloc[i-1]
    curr = df.iloc[i]

    direction = None

    # =========================
    # BULLISH
    # =========================
    if (prev['close'] < prev['open'] and
        curr['low'] < prev['low'] and
        curr['close'] > prev['open']):
        direction = "BUY"

    elif (prev['close'] > prev['open'] and
          curr['low'] < prev['low'] and
          curr['close'] > prev['close']):
        direction = "BUY"

    # =========================
    # BEARISH
    # =========================
    elif (prev['close'] > prev['open'] and
          curr['high'] > prev['high'] and
          curr['close'] < prev['open']):
        direction = "SELL"

    elif (prev['close'] < prev['open'] and
          curr['high'] > prev['high'] and
          curr['close'] < prev['close']):
        direction = "SELL"

    if direction is None:
        continue

    # =========================
    # ENTRY
    # =========================
    entry = curr['close']
    entry_time = curr.name

    # =========================
    # ORIGINAL RISK
    # =========================
    if direction == "BUY":
        original_risk = entry - curr['low']
    else:
        original_risk = curr['high'] - entry

    if original_risk == 0:
        continue

    # =========================
    # NEW SL (0.7R)
    # =========================
    new_risk = 0.7 * original_risk

    # =========================
    # NEW TP (2R RR)
    # =========================
    tp_distance = 2 * new_risk  # = 1.4 * original_risk

    if direction == "BUY":
        sl = entry - new_risk
        tp = entry + tp_distance

    else:
        sl = entry + new_risk
        tp = entry - tp_distance

    # =========================
    # TRADE SIMULATION
    # =========================
    future = df.iloc[i+1:]

    R_value = None

    for j in range(len(future)):
        f = future.iloc[j]

        # BUY
        if direction == "BUY":

            if f['low'] <= sl:
                R_value = -1
                break

            if f['high'] >= tp:
                R_value = 2
                break

        # SELL
        elif direction == "SELL":

            if f['high'] >= sl:
                R_value = -1
                break

            if f['low'] <= tp:
                R_value = 2
                break

    if R_value is not None:
        results.append(R_value)

        trade_log.append({
            "datetime": entry_time,
            "direction": direction,
            "entry_price": entry,
            "R_result": R_value
        })

# =========================
# SAVE CSV
# =========================
trade_df = pd.DataFrame(trade_log)
trade_df.to_csv("engulfing_rr2_trades.csv", index=False)

# =========================
# RESULTS
# =========================
total = len(results)
wins = sum(1 for r in results if r == 2)
losses = sum(1 for r in results if r == -1)

print("========== RESULTS ==========")
print("Total Trades:", total)
print("Wins:", wins)
print("Losses:", losses)

if total > 0:
    winrate = wins / total
    avg_R = sum(results) / total

    print("Win Rate:", round(winrate, 3))
    print("Average R:", round(avg_R, 3))
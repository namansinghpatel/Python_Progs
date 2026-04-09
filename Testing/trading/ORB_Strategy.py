import pandas as pd
from pathlib import Path

# location of this script
BASE_DIR = Path(__file__).resolve().parent   # trading/

# go to Testing/ → then data/
DATA_DIR = BASE_DIR.parent / "data"

# =========================
# LOAD DATA
# =========================
eurusd_5m_oanda_path = DATA_DIR / "eurusd_5m_oanda.csv"
eurusd_15m_oanda_path = DATA_DIR / "eurusd_15m_oanda.csv"

df_5m = pd.read_csv(eurusd_5m_oanda_path)
df_15m = pd.read_csv(eurusd_15m_oanda_path)

# Convert datetime
df_5m['datetime'] = pd.to_datetime(df_5m['datetime'])
df_15m['datetime'] = pd.to_datetime(df_15m['datetime'])

df_5m.set_index('datetime', inplace=True)
df_15m.set_index('datetime', inplace=True)

# =========================
# DATE COLUMN
# =========================
df_5m['date'] = df_5m.index.date
df_15m['date'] = df_15m.index.date

results = []
trade_log = []
missed_trades = 0

# =========================
# MAIN LOOP
# =========================
for date in df_15m['date'].unique():

    day_15 = df_15m[df_15m['date'] == date]
    day_5 = df_5m[df_5m['date'] == date]

    # -------------------------
    # 1. GET 13:30 CANDLE
    # -------------------------
    try:
        candle = day_15.between_time("13:30", "13:30").iloc[0]
    except:
        continue

    range_high = candle['high']
    range_low = candle['low']

    # -------------------------
    # 2. 5-HOUR WINDOW
    # -------------------------
    after = day_5.between_time("13:45", "18:45")

    trade_active = False   # 🔥 NEW

    for i in range(len(after)):

        # ❌ Skip if already in trade
        if trade_active:
            break

        row = after.iloc[i]

        direction = None

        # -------------------------
        # 3. BREAKOUT (CLOSE BASED)
        # -------------------------
        if row['close'] > range_high:
            direction = "BUY"
            entry = range_high
            sl = range_low
            tp = entry + (entry - sl)

        elif row['close'] < range_low:
            direction = "SELL"
            entry = range_low
            sl = range_high
            tp = entry - (sl - entry)

        else:
            continue

        breakout_time = row.name

        # -------------------------
        # 4. LIMIT ENTRY (AFTER BREAKOUT ONLY)
        # -------------------------
        future = after.iloc[i+1:i+61]

        filled = False
        fill_index = None
        fill_time = None

        for j in range(len(future)):
            f = future.iloc[j]

            if direction == "BUY":
                if f['low'] <= entry:
                    filled = True
                    fill_index = j
                    fill_time = f.name
                    break

            elif direction == "SELL":
                if f['high'] >= entry:
                    filled = True
                    fill_index = j
                    fill_time = f.name
                    break

        # ❌ Not filled
        if not filled:
            missed_trades += 1
            break

        # -------------------------
        # 5. TRADE IS NOW ACTIVE
        # -------------------------
        trade_active = True

        trade_future = future.iloc[fill_index:]

        result = None

        for k in range(len(trade_future)):
            t = trade_future.iloc[k]

            if direction == "BUY":
                if t['low'] <= sl:
                    result = "LOSS"
                    break
                elif t['high'] >= tp:
                    result = "WIN"
                    break

            elif direction == "SELL":
                if t['high'] >= sl:
                    result = "LOSS"
                    break
                elif t['low'] <= tp:
                    result = "WIN"
                    break

        if result:
            results.append(result)

            trade_log.append({
                "datetime": fill_time,
                "direction": direction,
                "result": result,
                "entry_price": entry
            })

        break   # 🔥 ensures only one trade per day

# =========================
# SAVE TRADE LOG
# =========================
trade_df = pd.DataFrame(trade_log)
trade_df.to_csv("trade_log.csv", index=False)

# =========================
# RESULTS
# =========================
wins = results.count("WIN")
losses = results.count("LOSS")

total = wins + losses

print("========== RESULTS ==========")
print("Total Trades:", total)
print("Wins:", wins)
print("Losses:", losses)
print("Missed Trades:", missed_trades)

if total > 0:
    winrate = wins / total
    expectancy = (winrate * 1) - ((1 - winrate) * 1)

    print("Win Rate:", round(winrate, 3))
    print("Expectancy:", round(expectancy, 3))
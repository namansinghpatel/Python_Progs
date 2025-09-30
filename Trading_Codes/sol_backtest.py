import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Load CSV (no header) ---
data = pd.read_csv(
    "SOLUSDT_1min.csv",
    header=None,
    names=["timestamp", "open", "high", "low", "close", "volume"]
)

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y.%m.%d %H:%M")
data.set_index('timestamp', inplace=True)

# --- Calculate EMAs ---
data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

# --- Calculate RSI (14-period) ---
delta = data['close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# --- Initialize variables ---
current_idx = 0
playing = False
position = 0
entry_price = 0
balance = 10000
leverage = 10

# --- Lists for plotting ---
candles_open = []
candles_close = []
candles_high = []
candles_low = []

ema20_vals = []
ema50_vals = []
ema200_vals = []
rsi_vals = []

# --- Plot setup ---
fig, (ax_price, ax_rsi) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
plt.subplots_adjust(bottom=0.2)

ax_price.set_title("SOLUSDT Backtest Replay with EMA & RSI")
ax_price.set_ylabel("Price")
ax_rsi.set_ylabel("RSI")
ax_rsi.set_ylim(0, 100)

line_ema20, = ax_price.plot([], [], color='orange', lw=1.5, label='EMA20')
line_ema50, = ax_price.plot([], [], color='green', lw=1.5, label='EMA50')
line_ema200, = ax_price.plot([], [], color='red', lw=1.5, label='EMA200')

line_rsi, = ax_rsi.plot([], [], color='purple', lw=1.5, label='RSI')
ax_price.legend()
ax_rsi.legend()

# --- Draw OHLC candles ---
def draw_candles():
    ax_price.clear()
    ax_price.set_ylabel("Price")
    ax_price.plot(range(len(candles_close)), ema20_vals, color='orange', lw=1.5, label='EMA20')
    ax_price.plot(range(len(candles_close)), ema50_vals, color='green', lw=1.5, label='EMA50')
    ax_price.plot(range(len(candles_close)), ema200_vals, color='red', lw=1.5, label='EMA200')
    
    for i in range(len(candles_close)):
        color = 'green' if candles_close[i] >= candles_open[i] else 'red'
        # Wick
        ax_price.vlines(i, candles_low[i], candles_high[i], color=color, lw=1)
        # Body
        ax_price.vlines(i, candles_open[i], candles_close[i], color=color, lw=4)
    ax_price.legend()

# --- Update function for animation ---
def update(frame):
    global current_idx
    if playing or frame == 0:
        if current_idx >= len(data):
            return
        
        row = data.iloc[current_idx]
        candles_open.append(row['open'])
        candles_close.append(row['close'])
        candles_high.append(row['high'])
        candles_low.append(row['low'])
        ema20_vals.append(row['EMA20'])
        ema50_vals.append(row['EMA50'])
        ema200_vals.append(row['EMA200'])
        rsi_vals.append(row['RSI'])
        
        draw_candles()
        line_rsi.set_data(range(len(rsi_vals)), rsi_vals)
        ax_rsi.relim()
        ax_rsi.autoscale_view()
        
        print(f"{row.name} | O:{row['open']} H:{row['high']} L:{row['low']} C:{row['close']}")
        current_idx += 1

# --- Key bindings for manual control ---
def on_key(event):
    global playing, current_idx, position, entry_price, balance
    if event.key == ' ':
        playing = not playing
        print("Playing" if playing else "Paused")
    elif event.key == 'n':
        update(0)
    elif event.key == 'l':
        if position == 0:
            row = data.iloc[current_idx-1]
            position = 1
            entry_price = row['close']
            print(f"Entered LONG at {entry_price}")
    elif event.key == 's':
        if position == 0:
            row = data.iloc[current_idx-1]
            position = -1
            entry_price = row['close']
            print(f"Entered SHORT at {entry_price}")
    elif event.key == 'c':
        if position != 0:
            row = data.iloc[current_idx-1]
            exit_price = row['close']
            pnl = (exit_price - entry_price) * leverage if position == 1 else (entry_price - exit_price) * leverage
            balance += pnl
            print(f"Closed position at {exit_price}, PnL: {pnl}, Balance: {balance}")
            position = 0

# --- Connect keys and start animation ---
fig.canvas.mpl_connect('key_press_event', on_key)
ani = FuncAnimation(fig, update, interval=500)
plt.show()

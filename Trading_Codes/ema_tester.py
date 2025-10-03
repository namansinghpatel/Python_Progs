import pandas as pd
import pandas_ta as ta
from backtesting import Backtest, Strategy

# ------------------------
# Load your data
# ------------------------
data = pd.read_csv(
    r"C:\Users\Naman Patel\Desktop\Backtest\SOLUSDT_1min.csv",
    header=None,
    names=["Date", "Open", "High", "Low", "Close", "Volume"]
)
data["Date"] = pd.to_datetime(data["Date"], format="%Y.%m.%d %H:%M")
data.set_index("Date", inplace=True)
data = data.sort_index()

# ------------------------
# Define 2 EMA Crossover Strategy
# ------------------------
class TwoEMACross(Strategy):
    def init(self):
        close = self.data.Close
        # Fast EMA = 10, Slow EMA = 50
        self.ema_fast = self.I(lambda x: ta.ema(pd.Series(x), length=10).fillna(method='bfill').to_numpy(), close)
        self.ema_slow = self.I(lambda x: ta.ema(pd.Series(x), length=50).fillna(method='bfill').to_numpy(), close)

    def next(self):
        price = self.data.Close[-1]
        fast = self.ema_fast[-1]
        slow = self.ema_slow[-1]

        # Debug prints
        print(f"[DEBUG] Time: {self.data.index[-1]}, Price: {price:.2f}, EMA10: {fast:.2f}, EMA50: {slow:.2f}")

        # Crossover Buy
        if fast > slow and self.position.is_short == False:
            self.buy(size=0.1)  # 10% equity
            print(f"[TRADE] Buy at {price:.2f}")

        # Crossunder Sell
        elif fast < slow and self.position.is_long == False:
            self.sell(size=0.1)  # 10% equity
            print(f"[TRADE] Sell at {price:.2f}")

# ------------------------
# Run Backtest
# ------------------------
bt = Backtest(
    data,
    TwoEMACross,
    cash=100000,
    commission=0.0,
    trade_on_close=False,
    exclusive_orders=True
)

stats = bt.run()
print(stats)
bt.plot()

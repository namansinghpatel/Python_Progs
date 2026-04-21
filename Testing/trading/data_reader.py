import pandas as pd

# ==========================================
# LOAD TRADE FILE
# ==========================================
df = pd.read_csv("engulfing_rr2_trades.csv")

# Required columns:
# datetime,day,direction,entry_price,R_result

df["datetime"] = pd.to_datetime(df["datetime"])

# ==========================================
# EXTRACT HOUR + MINUTE
# ==========================================
df["time"] = df["datetime"].dt.strftime("%H:%M")
df["hour"] = df["datetime"].dt.hour

# ==========================================
# WIN / LOSS COLUMN
# ==========================================
df["result"] = df["R_result"].apply(lambda x: "WIN" if x > 0 else "LOSS")

# ==========================================
# 1. ANALYSIS BY DAY
# ==========================================
day_stats = df.groupby("day").agg(
    Trades=("R_result", "count"),
    Wins=("result", lambda x: (x == "WIN").sum()),
    Losses=("result", lambda x: (x == "LOSS").sum()),
    Avg_R=("R_result", "mean")
).reset_index()

day_stats["WinRate_%"] = round(day_stats["Wins"] / day_stats["Trades"] * 100, 2)

# Arrange weekday order
weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

day_stats["day"] = pd.Categorical(day_stats["day"], categories=weekday_order, ordered=True)
day_stats = day_stats.sort_values("day")

# ==========================================
# 2. ANALYSIS BY EXACT TIME
# ==========================================
time_stats = df.groupby("time").agg(
    Trades=("R_result", "count"),
    Wins=("result", lambda x: (x == "WIN").sum()),
    Losses=("result", lambda x: (x == "LOSS").sum()),
    Avg_R=("R_result", "mean")
).reset_index()

time_stats["WinRate_%"] = round(time_stats["Wins"] / time_stats["Trades"] * 100, 2)
time_stats = time_stats.sort_values("time")

# ==========================================
# 3. ANALYSIS BY HOUR
# ==========================================
hour_stats = df.groupby("hour").agg(
    Trades=("R_result", "count"),
    Wins=("result", lambda x: (x == "WIN").sum()),
    Losses=("result", lambda x: (x == "LOSS").sum()),
    Avg_R=("R_result", "mean")
).reset_index()

hour_stats["WinRate_%"] = round(hour_stats["Wins"] / hour_stats["Trades"] * 100, 2)

# ==========================================
# SAVE OUTPUT FILES
# ==========================================
day_stats.to_csv("analysis_by_day.csv", index=False)
time_stats.to_csv("analysis_by_time.csv", index=False)
hour_stats.to_csv("analysis_by_hour.csv", index=False)

# ==========================================
# PRINT RESULTS
# ==========================================
print("========== ANALYSIS COMPLETE ==========")

print("\nSaved Files:")
print("1. analysis_by_day.csv")
print("2. analysis_by_time.csv")
print("3. analysis_by_hour.csv")

print("\n===== DAY SUMMARY =====")
print(day_stats)

print("\n===== HOUR SUMMARY =====")
print(hour_stats)

print("\n===== TIME SUMMARY (first 20 rows) =====")
print(time_stats.head(20))
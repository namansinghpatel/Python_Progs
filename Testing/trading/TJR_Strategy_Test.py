from pathlib import Path
import pandas as pd

# ================= CONFIG =================
DATA_PATH = Path("data/EURUSD_M1.csv")   # 1-minute input (UTC)
LOOKBACK_DAYS = 5

OUT_1H = Path("data/stage1_1h_levels.csv")
OUT_5M = Path("data/stage1_m5_candles.csv")
OUT_SESS = Path("data/stage2_session_levels.csv")
# =========================================


# ---------- LOAD ----------
def load_m1_csv_utc(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]

    required = {"datetime", "open", "high", "low", "close"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {required - set(df.columns)}")

    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df.dropna().sort_values("datetime").reset_index(drop=True)


# ---------- BUILD CANDLES ----------
def build_5m(df):
    return (
        df.set_index("datetime")
        .resample("5T")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
        .reset_index()
    )


def build_1h(df):
    return (
        df.set_index("datetime")
        .resample("1H")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
        .reset_index()
    )


# ---------- STAGE 1 ----------
def detect_1h_swings(df_1h):
    swings = []
    for i in range(1, len(df_1h) - 1):
        p, c, n = df_1h.iloc[i - 1], df_1h.iloc[i], df_1h.iloc[i + 1]

        if c.high > p.high and c.high > n.high:
            swings.append({"datetime": c.datetime, "type": "HIGH", "price": c.high, "valid": True})

        if c.low < p.low and c.low < n.low:
            swings.append({"datetime": c.datetime, "type": "LOW", "price": c.low, "valid": True})

    return pd.DataFrame(swings)


def invalidate_levels(levels, df_1h):
    for i, lvl in levels.iterrows():
        future = df_1h[df_1h.datetime > lvl.datetime]

        if lvl.type == "HIGH" and (future.high > lvl.price).any():
            levels.at[i, "valid"] = False

        if lvl.type == "LOW" and (future.low < lvl.price).any():
            levels.at[i, "valid"] = False

    return levels


# ---------- STAGE 2 ----------
SESSIONS = {
    "ASIA":   (22, 7),
    "LONDON": (7, 13),
    "NEWYORK": (12, 21),
}


def get_session(dt, start, end):
    h = dt.hour
    if start < end:
        return start <= h < end
    return h >= start or h < end


def build_session_levels(df_m1):
    rows = []

    for session, (start, end) in SESSIONS.items():
        for day in df_m1["datetime"].dt.date.unique():
            day_df = df_m1[df_m1["datetime"].dt.date == day]

            sess_df = day_df[day_df["datetime"].apply(lambda x: get_session(x, start, end))]
            if sess_df.empty:
                continue

            high = sess_df["high"].max()
            low = sess_df["low"].min()

            rows.append({
                "date": day,
                "session": session,
                "type": "HIGH",
                "price": high,
                "valid": True
            })

            rows.append({
                "date": day,
                "session": session,
                "type": "LOW",
                "price": low,
                "valid": True
            })

    return pd.DataFrame(rows)


def invalidate_session_levels(levels, df_m1):
    for i, lvl in levels.iterrows():

        session = lvl["session"]
        date = pd.to_datetime(lvl["date"])

        start, end = SESSIONS[session]

        # Build exact session end datetime (UTC)
        if start < end:
            session_end = date + pd.Timedelta(hours=end)
        else:
            # overnight session (Asia)
            session_end = date + pd.Timedelta(days=1, hours=end)

        future = df_m1[df_m1["datetime"] > session_end]

        if lvl.type == "HIGH" and (future.high > lvl.price).any():
            levels.at[i, "valid"] = False

        if lvl.type == "LOW" and (future.low < lvl.price).any():
            levels.at[i, "valid"] = False

    return levels



# ---------- MAIN ----------
def main():
    df = load_m1_csv_utc(DATA_PATH)

    cutoff = df.datetime.max() - pd.Timedelta(days=LOOKBACK_DAYS)
    df = df[df.datetime >= cutoff]

    df_5m = build_5m(df)
    df_1h = build_1h(df)

    swings = detect_1h_swings(df_1h)
    swings = invalidate_levels(swings, df_1h)

    session_lvls = build_session_levels(df)
    session_lvls = invalidate_session_levels(session_lvls, df)

    OUT_1H.parent.mkdir(parents=True, exist_ok=True)
    df_5m.to_csv(OUT_5M, index=False)
    swings.to_csv(OUT_1H, index=False)
    session_lvls.to_csv(OUT_SESS, index=False)

    print("=== STAGE 2 COMPLETE (UTC) ===")
    print(f"5M candles saved  : {len(df_5m)}")
    print(f"1H swings total   : {len(swings)}")
    print(f"Session levels    : {len(session_lvls)}")
    print(f"Valid sessions    : {session_lvls.valid.sum()}")


if __name__ == "__main__":
    main()

import requests
import pandas as pd

# =========================
# CONFIG
# =========================
ACCESS_TOKEN = "0388bbafedd55c61e65630e3710a7592-8ba539034745cd345355c2e4e159d352"
BASE_URL = "https://api-fxpractice.oanda.com"

INSTRUMENT = "NZD_USD"
GRANULARITY = "H4"

# 🔥 DATE RANGE (EDIT HERE)
FROM_DATE = "2025-4-1T00:00:00Z"
TO_DATE   = "2026-3-31T23:59:59Z"

# =========================
# HEADERS
# =========================
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# =========================
# REQUEST
# =========================
url = f"{BASE_URL}/v3/instruments/{INSTRUMENT}/candles"

params = {
    "granularity": GRANULARITY,
    "from": FROM_DATE,
    "to": TO_DATE,
    "price": "M"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# =========================
# PARSE DATA
# =========================
candles = data.get('candles', [])

records = []

for candle in candles:
    if candle['complete']:
        records.append({
            "datetime": candle['time'],
            "open": float(candle['mid']['o']),
            "high": float(candle['mid']['h']),
            "low": float(candle['mid']['l']),
            "close": float(candle['mid']['c']),
            "volume": candle['volume']
        })

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(records)

df['datetime'] = pd.to_datetime(df['datetime'])

# =========================
# SAVE
# =========================
df.to_csv("nzdusd_4h_oanda.csv", index=False)

print("Data saved successfully ✅")
print(df.head())
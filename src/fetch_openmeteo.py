import requests
import pandas as pd
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------
LAT = 9.56      # Hargeisa latitude
LON = 44.06     # Hargeisa longitude

START_DATE = "2021-01-01"
END_DATE = "2024-12-31"

OUTPUT_PATH = Path("data/raw")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_PATH / "hargeisa_daily_weather.csv"

# ----------------------------
# OPEN-METEO API CALL
# ----------------------------
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max"
    ],
    "timezone": "Africa/Mogadishu"
}

print("Fetching historical weather data...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()
daily = data["daily"]

# ----------------------------
# CREATE DATAFRAME
# ----------------------------
df = pd.DataFrame({
    "date": pd.to_datetime(daily["time"]),
    "temp_max": daily["temperature_2m_max"],
    "temp_min": daily["temperature_2m_min"],
    "precipitation": daily["precipitation_sum"],
    "wind_speed_max": daily["wind_speed_10m_max"]
})

df = df.sort_values("date").reset_index(drop=True)

# ----------------------------
# SAVE
# ----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved {len(df)} rows to {OUTPUT_FILE}")
print(df.head())

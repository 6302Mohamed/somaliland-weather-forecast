import pandas as pd
from pathlib import Path

# ----------------------------
# PATHS
# ----------------------------
RAW_PATH = Path("data/raw/hargeisa_daily_weather.csv")
PROCESSED_PATH = Path("data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_PATH / "hargeisa_daily_weather.parquet"

# ----------------------------
# LOAD
# ----------------------------
df = pd.read_csv(RAW_PATH, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

print(f"Loaded {len(df)} rows")

# ----------------------------
# CHECK DATE CONTINUITY
# ----------------------------
full_dates = pd.date_range(
    start=df["date"].min(),
    end=df["date"].max(),
    freq="D"
)

df_full = (
    df.set_index("date")
      .reindex(full_dates)
)

df_full.index.name = "date"

missing_days = df_full.isna().all(axis=1).sum()

print(f"Missing days detected: {missing_days}")

# ----------------------------
# HANDLE MISSING DAYS
# Strategy:
# - temperature: interpolate
# - precipitation: fill 0
# - wind: forward fill
# ----------------------------
df_full["temp_max"] = df_full["temp_max"].interpolate()
df_full["temp_min"] = df_full["temp_min"].interpolate()
df_full["precipitation"] = df_full["precipitation"].fillna(0)
df_full["wind_speed_max"] = df_full["wind_speed_max"].fillna(method="ffill")

df_full = df_full.reset_index()

# ----------------------------
# FINAL CHECK
# ----------------------------
assert df_full.isna().sum().sum() == 0, "Missing values remain!"

print("No missing values after preprocessing.")

# ----------------------------
# SAVE
# ----------------------------
df_full.to_parquet(OUTPUT_FILE, index=False)

print(f"Saved processed data to {OUTPUT_FILE}")
print(df_full.head())

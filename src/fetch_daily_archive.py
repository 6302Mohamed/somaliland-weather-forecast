
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys
import time
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
import requests


# -----------------------------
# Config
# -----------------------------
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

@dataclass
class City:
    name: str
    lat: float
    lon: float
    timezone: str = "Africa/Mogadishu"


CITIES = {
    "hargeisa": City("Hargeisa", lat=9.562, lon=44.077, timezone="Africa/Mogadishu"),
    # You can add more later:
    # "berbera": City("Berbera", lat=10.439, lon=45.014, timezone="Africa/Mogadishu"),
    # "borama": City("Borama", lat=9.936, lon=43.182, timezone="Africa/Mogadishu"),
    # "erigavo": City("Erigavo", lat=10.616, lon=47.367, timezone="Africa/Mogadishu"),
}

DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]


def fetch_archive_daily(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str,
    timezone: str,
    retries: int = 3,
    sleep_s: float = 1.0,
) -> pd.DataFrame:
    """
    Fetch daily archive data from Open-Meteo.
    Returns a DataFrame with 'date' + weather columns.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_VARS),
        "timezone": timezone,
    }

    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()

            daily = data.get("daily", {})
            dates = daily.get("time", [])

            if not dates:
                raise ValueError(f"No daily data returned for {start_date}..{end_date}")

            df = pd.DataFrame({"date": pd.to_datetime(dates)})

            # Map Open-Meteo var names to your project-friendly column names
            df["temp_max"] = daily.get("temperature_2m_max", [])
            df["temp_min"] = daily.get("temperature_2m_min", [])
            df["precipitation"] = daily.get("precipitation_sum", [])
            df["wind_speed_max"] = daily.get("wind_speed_10m_max", [])

            return df

        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(sleep_s * attempt)
            else:
                raise

    # Should never hit this
    raise last_err if last_err else RuntimeError("Unknown error fetching archive data")


def ensure_daily_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure continuous daily dates (fill missing dates with NaNs).
    """
    df = df.sort_values("date").reset_index(drop=True)
    full_range = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    df = df.set_index("date").reindex(full_range).rename_axis("date").reset_index()
    return df


def main():
    parser = argparse.ArgumentParser(description="Fetch Open-Meteo archive daily data and rebuild parquet.")
    parser.add_argument("--city", type=str, default="hargeisa", choices=sorted(CITIES.keys()))
    parser.add_argument("--start", type=str, default="2021-01-01", help="YYYY-MM-DD")
    parser.add_argument("--end", type=str, default="2025-12-31", help="YYYY-MM-DD")
    parser.add_argument("--out_raw", type=str, default="data/raw/hargeisa_daily_2021_2025.csv")
    parser.add_argument("--out_parquet", type=str, default="data/processed/hargeisa_daily_weather.parquet")
    args = parser.parse_args()

    city = CITIES[args.city]

    out_raw = Path(args.out_raw)
    out_parquet = Path(args.out_parquet)
    out_raw.parent.mkdir(parents=True, exist_ok=True)
    out_parquet.parent.mkdir(parents=True, exist_ok=True)

    # Fetch in yearly chunks (more reliable + easier to debug)
    start_year = int(args.start[:4])
    end_year = int(args.end[:4])

    chunks: List[pd.DataFrame] = []
    for y in range(start_year, end_year + 1):
        chunk_start = f"{y}-01-01"
        chunk_end = f"{y}-12-31"

        # Clamp edges to user-specified start/end
        if y == start_year:
            chunk_start = args.start
        if y == end_year:
            chunk_end = args.end

        print(f"[fetch] {city.name} {chunk_start} → {chunk_end}")
        df_y = fetch_archive_daily(
            lat=city.lat,
            lon=city.lon,
            start_date=chunk_start,
            end_date=chunk_end,
            timezone=city.timezone,
        )
        chunks.append(df_y)

    df = pd.concat(chunks, ignore_index=True).drop_duplicates(subset=["date"]).sort_values("date")

    # Ensure complete daily index
    df = ensure_daily_index(df)

    # Basic types
    for col in ["temp_max", "temp_min", "precipitation", "wind_speed_max"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Some quick sanity info
    n_missing = df.isna().sum()
    print("\n[summary]")
    print(f"date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"rows      : {len(df)}")
    print("missing values per column:")
    print(n_missing.to_string())

    # Save
    df.to_csv(out_raw, index=False)
    df.to_parquet(out_parquet, index=False)

    print(f"\n[saved] raw     → {out_raw}")
    print(f"[saved] parquet → {out_parquet}")


if __name__ == "__main__":
    sys.exit(main())

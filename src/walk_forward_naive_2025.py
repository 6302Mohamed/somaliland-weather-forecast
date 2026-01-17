import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path("data/processed/hargeisa_daily_weather.parquet")
OUT_PATH = Path("reports/naive_walk_forward_2025.csv")

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

def main():
    df = pd.read_parquet(DATA_PATH).sort_values("date").reset_index(drop=True)

    # Ensure we only use fully observed rows
    df = df.dropna(subset=["temp_max"]).reset_index(drop=True)

    # Split
    df_2025 = df[df["date"].dt.year == 2025].copy()

    forecasts = []

    for i in range(len(df_2025) - 1):
        today = df_2025.iloc[i]
        tomorrow = df_2025.iloc[i + 1]

        forecast = today["temp_max"]
        actual = tomorrow["temp_max"]

        forecasts.append({
            "forecast_date": tomorrow["date"],
            "forecast": forecast,
            "actual": actual,
            "error": actual - forecast,
            "abs_error": abs(actual - forecast),
        })

    result = pd.DataFrame(forecasts)

    mae = mean_absolute_error(result["actual"], result["forecast"])
    r = rmse(result["actual"], result["forecast"])

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT_PATH, index=False)

    print("Naive Walk-Forward Forecasting (2025)")
    print(f"Days evaluated : {len(result)}")
    print(f"MAE           : {mae:.3f} °C")
    print(f"RMSE          : {r:.3f} °C")
    print(f"Saved results : {OUT_PATH}")

if __name__ == "__main__":
    main()

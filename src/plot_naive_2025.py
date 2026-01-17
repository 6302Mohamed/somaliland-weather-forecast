import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("reports/naive_walk_forward_2025.csv")
FIG_DIR = Path("reports/figures_2025")
FIG_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(CSV_PATH, parse_dates=["forecast_date"])
    df = df.sort_values("forecast_date").reset_index(drop=True)

    df["rolling_mae_30"] = df["abs_error"].rolling(30).mean()

    # -----------------------------
    # 1) Actual vs Forecast
    # -----------------------------
    plt.figure(figsize=(14, 5))
    plt.plot(df["forecast_date"], df["actual"], label="Actual", linewidth=1)
    plt.plot(df["forecast_date"], df["forecast"], label="Naive Forecast", linewidth=1)
    plt.title("Naive Walk-Forward Forecast vs Actual (2025)")
    plt.xlabel("Date")
    plt.ylabel("Max Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "01_actual_vs_forecast_2025.png", dpi=160)
    plt.close()

    # -----------------------------
    # 2) Residuals over time
    # -----------------------------
    plt.figure(figsize=(14, 4))
    plt.plot(df["forecast_date"], df["error"], linewidth=1)
    plt.axhline(0, linewidth=1)
    plt.title("Forecast Residuals Over Time (2025)")
    plt.xlabel("Date")
    plt.ylabel("Residual (Actual − Forecast) °C")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "02_residuals_2025.png", dpi=160)
    plt.close()

    # -----------------------------
    # 3) Rolling MAE (30-day)
    # -----------------------------
    plt.figure(figsize=(14, 4))
    plt.plot(df["forecast_date"], df["rolling_mae_30"], linewidth=1)
    plt.title("Rolling MAE (30-day) — Naive Walk-Forward (2025)")
    plt.xlabel("Date")
    plt.ylabel("MAE (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "03_rolling_mae_30_2025.png", dpi=160)
    plt.close()

    # -----------------------------
    # 4) Absolute error distribution
    # -----------------------------
    plt.figure(figsize=(10, 4))
    plt.hist(df["abs_error"], bins=40)
    plt.title("Absolute Error Distribution — Naive Walk-Forward (2025)")
    plt.xlabel("Absolute Error (°C)")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "04_abs_error_hist_2025.png", dpi=160)
    plt.close()

    # -----------------------------
    # 5) Worst 10 days
    # -----------------------------
    worst = (
        df.sort_values("abs_error", ascending=False)
        .head(10)
        .copy()
    )
    worst.to_csv(FIG_DIR / "worst_10_days_2025.csv", index=False)

    print("Saved plots to:", FIG_DIR.resolve())
    print("Saved worst days table:", (FIG_DIR / "worst_10_days_2025.csv").resolve())

if __name__ == "__main__":
    main()

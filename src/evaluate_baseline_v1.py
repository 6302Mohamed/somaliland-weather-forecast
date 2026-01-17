import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path("data/processed/hargeisa_daily_weather.parquet")
SPLIT_DATE = "2024-01-01"  # test period start (edit if you want)

FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

def main():
    # ----------------------------
    # Load
    # ----------------------------
    df = pd.read_parquet(DATA_PATH).sort_values("date").reset_index(drop=True)

    # ----------------------------
    # V1 Target: 1-day ahead temp_max
    # y(t) = temp_max(t+1)
    # Baseline prediction: y_hat(t) = temp_max(t)
    # ----------------------------
    df["y_true"] = df["temp_max"].shift(-1)
    df["y_pred"] = df["temp_max"]  # persistence baseline

    df = df.dropna(subset=["y_true", "y_pred"]).reset_index(drop=True)

    train_mask = df["date"] < SPLIT_DATE
    test_mask = df["date"] >= SPLIT_DATE

    test = df.loc[test_mask].copy()

    y_true = test["y_true"]
    y_pred = test["y_pred"]

    mae = mean_absolute_error(y_true, y_pred)
    r = rmse(y_true, y_pred)

    print("V1 Persistence Baseline (1-day ahead temp_max)")
    print(f"Test start date: {SPLIT_DATE}")
    print(f"MAE  : {mae:.3f} °C")
    print(f"RMSE : {r:.3f} °C")

    # Residuals
    test["residual"] = y_true - y_pred
    test["abs_error"] = test["residual"].abs()

    # ----------------------------
    # Plot 1: Actual vs Predicted (last 120 days of test for clarity)
    # ----------------------------
    view = test.tail(120)

    plt.figure(figsize=(14, 5))
    plt.plot(view["date"], view["y_true"], linewidth=1, label="Actual (tomorrow)")
    plt.plot(view["date"], view["y_pred"], linewidth=1, label="Baseline (today)")
    plt.title("Actual vs Persistence Baseline (1-day ahead) — Last 120 Test Days")
    plt.xlabel("Date")
    plt.ylabel("Max Temperature (°C)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "01_actual_vs_baseline.png", dpi=160)
    plt.close()

    # ----------------------------
    # Plot 2: Residuals over time (last 180 days)
    # ----------------------------
    view = test.tail(180)

    plt.figure(figsize=(14, 4))
    plt.plot(view["date"], view["residual"], linewidth=1)
    plt.axhline(0, linewidth=1)
    plt.title("Residuals Over Time (Actual - Predicted) — Last 180 Test Days")
    plt.xlabel("Date")
    plt.ylabel("Residual (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "02_residuals_over_time.png", dpi=160)
    plt.close()

    # ----------------------------
    # Plot 3: Absolute error distribution
    # ----------------------------
    plt.figure(figsize=(10, 4))
    plt.hist(test["abs_error"], bins=40)
    plt.title("Absolute Error Distribution (Persistence Baseline)")
    plt.xlabel("Absolute Error (°C)")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "03_abs_error_hist.png", dpi=160)
    plt.close()

    # ----------------------------
    # Plot 4: Rolling MAE (30-day window)
    # ----------------------------
    test["rolling_mae_30"] = test["abs_error"].rolling(30).mean()

    plt.figure(figsize=(14, 4))
    plt.plot(test["date"], test["rolling_mae_30"], linewidth=1)
    plt.title("Rolling MAE (30-day) — Persistence Baseline")
    plt.xlabel("Date")
    plt.ylabel("MAE (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "04_rolling_mae_30.png", dpi=160)
    plt.close()

    # ----------------------------
    # Plot 5 (optional but nice): Predicted vs Actual scatter
    # ----------------------------
    plt.figure(figsize=(6, 6))
    plt.scatter(y_true, y_pred, s=8)
    min_v = float(min(y_true.min(), y_pred.min()))
    max_v = float(max(y_true.max(), y_pred.max()))
    plt.plot([min_v, max_v], [min_v, max_v], linewidth=1)
    plt.title("Predicted vs Actual (Test)")
    plt.xlabel("Actual (°C)")
    plt.ylabel("Predicted (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "05_pred_vs_actual.png", dpi=160)
    plt.close()

    print(f"\nSaved figures to: {FIG_DIR.resolve()}")

if __name__ == "__main__":
    main()

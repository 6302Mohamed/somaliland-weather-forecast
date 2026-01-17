import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def backtest_forecast(y_true, y_pred):
    """
    Align and compute metrics for time-series predictions.
    """
    mask = ~y_pred.isna()
    y_true = y_true[mask]
    y_pred = y_pred[mask]

    mae = mean_absolute_error(y_true, y_pred)

    # Compatible RMSE (avoid squared=False for sklearn version differences)
    mse = mean_squared_error(y_true, y_pred)
    rmse = float(np.sqrt(mse))

    return {
        "MAE": float(mae),
        "RMSE": rmse
    }

import pandas as pd
import numpy as np

def naive_forecast(series: pd.Series) -> pd.Series:
    """
    Forecast y(t) = y(t-1)
    """
    return series.shift(1)

def seasonal_naive_forecast(series: pd.Series, season_length: int = 7) -> pd.Series:
    """
    Forecast y(t) = y(t-season_length)
    """
    return series.shift(season_length)

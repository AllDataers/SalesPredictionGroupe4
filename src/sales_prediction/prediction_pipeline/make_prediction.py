import pandas as pd


def predict(forecaster, fh) -> pd.DataFrame:
    """
    Forecast for the next `fh` periods

    Args:
        fh (int): The forecasting horizon
        forecaster (ForecastingPipeline): The forecasting pipeline

    Returns:
        pd.DataFrame: The forecasted data
    """
    y_pred = forecaster.predict(fh)
    return y_pred

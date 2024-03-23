import pandas as pd
from sktime.performance_metrics.forecasting import (
    mean_squared_percentage_error,
    mean_absolute_percentage_error,
)


def train_model(forecaster, train_df, test_df):
    """
    Train the forecasting pipeline

    Args:
        forecaster (ForecastingPipeline): The forecasting pipeline
        train_df (pd.DataFrame): The training data
        test_df (pd.DataFrame): The test data

    Returns:
        pd.DataFrame: The predictions
    """
    forecaster.fit(train_df)
    predictions = forecaster.predict(n=len(test_df))
    return predictions


def evaluate_model(forecaster, train_df, test_df):
    """
    Evaluate the forecasting pipeline

    Args:
        forecaster (ForecastingPipeline): The forecasting pipeline
        train_df (pd.DataFrame): The training data
        test_df (pd.DataFrame): The test data

    Returns:
        pd.DataFrame: The evaluation metrics
    """
    predictions = train_model(forecaster, train_df, test_df)
    metrics = {
        "mse": mean_squared_percentage_error(test_df, predictions),
        "mape": mean_absolute_percentage_error(test_df, predictions),
    }
    return metrics


def forecast(forecaster, fh) -> pd.DataFrame:
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

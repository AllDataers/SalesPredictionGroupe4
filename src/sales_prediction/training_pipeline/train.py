import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict
import mlflow
from sktime.performance_metrics.forecasting import (
    mean_squared_percentage_error,
    mean_absolute_percentage_error,
    mean_absolute_error,
)


class BaseTrainingPipeline(ABC):
    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def forecast(self, fh: int):
        pass


class TrainingPipeline(BaseTrainingPipeline):
    def __init__(self, forecaster, train_df: pd.Series):
        self.forecaster = forecaster
        self.train_df = train_df

    def fit(self):
        """
        Train the forecasting pipeline

        Args:
            forecaster (ForecastingPipeline): The forecasting pipeline
            train_df (pd.DataFrame): The training data

        Returns:
            the fitted pipeline
        """
        self._pipeline = self.forecaster.fit(self.train_df)
        return self._pipeline

    def forecast(self, fh: int):
        """
        Forecast for the next `fh` periods

        Args:
            fh (int): The forecasting horizon
            forecaster (ForecastingPipeline): The forecasting pipeline

        Returns:
            pd.DataFrame: The forecasted data
        """
        return self.forecaster.predict(fh)


class ModelEvaluator:
    def evaluate(self, test_df: pd.Series, predictions: pd.Series) -> Dict[str, float]:
        """
        Evaluate the forecasting pipeline

        Args:
            prediction (pd.DataFrame): The predicted data
            test_df (pd.DataFrame): The test data

        Returns:
            pd.DataFrame: The evaluation metrics
        """

        metrics = {
            "mse": mean_squared_percentage_error(test_df, predictions),
            "mape": mean_absolute_percentage_error(test_df, predictions),
            "mae": mean_absolute_error(test_df, predictions),
        }
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        return metrics
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict

from sktime.performance_metrics.forecasting import (
    mean_squared_percentage_error,
    mean_absolute_percentage_error,
    mean_absolute_error
)


class BaseTrainingPipeline(ABC):
    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def forecast(self, fh: int):
        pass


class TrainingPipeline(BaseTrainingPipeline):
    def __init__(self, forecaster, train_df, test_df):
        self.forecaster = forecaster
        self.train_df = train_df
        self.test_df = test_df
        
    def train(self):
        """
        Train the forecasting pipeline

        Args:
            forecaster (ForecastingPipeline): The forecasting pipeline
            train_df (pd.DataFrame): The training data

        Returns:
            the fitted pipeline
        """
        self._pipeline = self.forecastter.fit(self.train_df)
        return self
    
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
    def __init__(self, forecaster):
        self.forecaster = forecaster

    def evaluate(self, test_df: pd.DataFrame) -> Dict:
        """
        Evaluate the forecasting pipeline

        Args:
            forecaster (ForecastingPipeline): The forecasting pipeline
            train_df (pd.DataFrame): The training data
            test_df (pd.DataFrame): The test data

        Returns:
            pd.DataFrame: The evaluation metrics
        """
        predictions = self.forecaster.predict(test_df)

        metrics = {
            "mse": mean_squared_percentage_error(test_df, predictions),
            "mape": mean_absolute_percentage_error(test_df, predictions),
            "mae": mean_absolute_error(test_df, predictions),
        }
        return metrics

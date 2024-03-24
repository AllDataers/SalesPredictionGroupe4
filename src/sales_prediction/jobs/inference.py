import pandas as pd


class InferenceJob:
    def __init__(self, forecaster):
        self.forecaster = forecaster

    def predict(self, fh: int) -> pd.DataFrame:
        """
        Forecast for the next `fh` periods

        Args:
            fh (int): The forecasting horizon
            forecaster (ForecastingPipeline): The forecasting pipeline

        Returns:
            pd.DataFrame: The forecasted data
        """
        return self.forecaster.predict(fh)

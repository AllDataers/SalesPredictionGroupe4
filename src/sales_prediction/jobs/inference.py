from argparse import ArgumentParser
import pandas as pd
from sktime.forecasting.base import ForecastingHorizon
from sales_prediction.training_pipeline.data_prep import prepare_data
from sales_prediction.utils.registries import ModelRegistry
from sales_prediction.utils import load_config


class InferenceJob:
    def __init__(self, forecaster):
        self.forecaster = forecaster

    @classmethod
    def from_path(cls, model_path):
        forecaster = ModelRegistry.load_model(model_path)
        return cls(forecaster)

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


def cli():
    parser = ArgumentParser()
    parser.add_argument(
        "--config_path",
        "-c",
        type=str,
        required=False,
        help="Path to the input config file.",
        default="src/config/forecasting_config.yaml",
    )
    return parser.parse_args()


def main():
    args = cli()
    config = load_config.load_config(args.config_path)
    df = pd.read_csv(config.get("csv_path"), parse_dates=["OrderDate"])
    forecaster = InferenceJob.from_path(config.get("model_path2"))
    _, df_test = prepare_data(df)
    fh = ForecastingHorizon(df_test.index, is_relative=False)
    predictions = forecaster.predict(fh)
    print(predictions)


if __name__ == "__main__":
    main()
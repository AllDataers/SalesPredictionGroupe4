from argparse import ArgumentParser
import pandas as pd
from sktime.forecasting.base import ForecastingHorizon
from sales_prediction.training_pipeline.train import (
    BaseTrainingPipeline,
    TrainingPipeline,
    ModelEvaluator,
)
from sales_prediction.utils.registries import ModelRegistry
from sales_prediction.training_pipeline.data_prep import prepare_data
from sales_prediction.training_pipeline.modelling import create_model
from sales_prediction.utils import load_config


class TrainingJob:
    def __init__(self, train_pipeline: BaseTrainingPipeline, metrics: ModelEvaluator):
        self.train_pipeline = train_pipeline
        self.metrics = metrics

    def run(self):
        self.train_pipeline.fit()

    def evaluate(self, df_test: pd.DataFrame, predictions: pd.DataFrame):
        metrics = self.metrics.evaluate(df_test, predictions)
        return metrics


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
    forecaster = create_model()
    print(forecaster.is_fitted)
    df_train, df_test = prepare_data(df)
    train_pipeline = TrainingPipeline(forecaster, df_train)
    fh = ForecastingHorizon(df_test.index, is_relative=False)
    metrics = ModelEvaluator()
    train_job = TrainingJob(train_pipeline, metrics)
    train_job.run()
    ModelRegistry.save_model(train_pipeline, config.get("model_path2"))
    predictions = train_pipeline.forecast(fh)
    metrics = train_job.evaluate(df_test=df_test, predictions=predictions)
    print(metrics)


if __name__ == "__main__":
    main()

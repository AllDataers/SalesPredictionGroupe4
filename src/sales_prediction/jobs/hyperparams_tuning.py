from argparse import ArgumentParser
from typing import Optional, Dict
import pandas as pd
from sktime.performance_metrics.base import BaseMetric
from sktime.performance_metrics.forecasting import mean_absolute_error
from sktime.forecasting.model_selection import ExpandingWindowSplitter
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.compose import TransformedTargetForecaster
from sktime.forecasting.model_selection import (
    ForecastingGridSearchCV,
    ForecastingRandomizedSearchCV,
)
from sales_prediction.utils.registries import ModelRegistry
from sales_prediction.training_pipeline.data_prep import prepare_data
from sales_prediction.training_pipeline.modelling import create_tuning_model
from sales_prediction.utils import load_config


class TuningHyperParamsJob:
    def __init__(
        self,
        forecaster: TransformedTargetForecaster,
        cv: ExpandingWindowSplitter,
        param_grid: Dict[str, str],
        metric: Optional[BaseMetric] = None,
        searchers: Optional[str] = "grid",
    ):
        self.forecaster = forecaster
        self.cv = cv
        self.searchers = searchers
        self.metric = metric
        self.param_grid = param_grid

    def run(self, y):
        if self.searchers == "grid":
            search_cv = ForecastingGridSearchCV(
                forecaster=self.forecaster,
                cv=self.cv,
                param_grid=self.param_grid,
                scoring=self.metric,
                error_score="raise",
            )
        elif self.searchers == "random":
            search_cv = ForecastingRandomizedSearchCV(
                forecaster=self.forecaster,
                cv=self.cv,
                scoring=self.metric,
                param_grid=self.param_grid,
                error_score="raise",
            )
        else:
            raise ValueError("The searchers should be 'grid' or 'random'")
        search_cv.fit(y=y)

        return search_cv


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
    forecaster = create_tuning_model()
    model_path = config.get("model_path")
    model_path2 = config.get("model_path2")
    df_train, df_test = prepare_data(df)
    param_grid = {
        "forecaster__estimator__learning_rate": [0.1, 0.01],
        "forecaster__estimator__l2_regularization": [0.1, 0.01],
    }
    cv = ExpandingWindowSplitter(
        fh=4,
        initial_window=30,
        step_length=7,
    )
    gridcv_forecaster = TuningHyperParamsJob(
        forecaster=forecaster,
        cv=cv,
        param_grid=param_grid,
    )
    best_forecaster = gridcv_forecaster.run(y=df_train)
    print(best_forecaster.best_params_)
    best_forecaster.save(model_path)
    y_pred = best_forecaster.predict(
        fh=ForecastingHorizon(df_test.index, is_relative=False)
    )
    print(mean_absolute_error(df_test, y_pred))
    fh = ForecastingHorizon(df_test.index, is_relative=False)
    ModelRegistry.load_model(model_path2).predict(fh=fh)


if __name__ == "__main__":
    main()

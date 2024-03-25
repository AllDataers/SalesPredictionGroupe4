from typing import Union
from sktime.split import SlidingWindowSplitter
from sales_prediction.training_pipeline.hyperparmaters_tuning import (
    GridSearchTuning,
    RandomizedSearchTuning,
)


class TuningHyperParamsJob:
    def __init__(self, forecaster, cv, searchers: str, metric, param_grid):
        self.forecaster = forecaster
        self.cv = cv
        self.searchers = searchers
        self.metric = metric
        self.param_grid = param_grid

    def run(self, y_train):
        if self.searchers == "grid":
            search_cv = GridSearchTuning(
                forecaster=self.forecaster,
                cv=self.cv,
                metric=self.metric,
                param_grid=self.param_grid,
            )
        elif self.searchers == "random":
            search_cv = RandomizedSearchTuning(
                forecaster=self.forecaster,
                cv=self.cv,
                metric=self.metric,
                param_grid=self.param_grid,
            )
        else:
            raise ValueError("The searchers should be 'grid' or 'random'")
        search_cv.fit(y_train)

        return search_cv

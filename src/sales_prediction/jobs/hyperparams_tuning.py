from typing import Union
from sktime.split import SlidingWindowSplitter
from sktime.forecasting.model_selection import ForecastingGridSearchCV, ForecastingRandomizedSearchCV


class TuningHyperParamsJob:
    def __init__(self, forecaster, cv, searchers: Union[ForecastingGridSearchCV,
                                                        ForecastingRandomizedSearchCV],
                 metric, param_grid):
        self.forecaster = forecaster
        self.cv = cv
        self.searchers = searchers
        self.metric = metric
        self.param_grid = param_grid

    def run(self, y_train):
        search_cv = self.searchers(forecaster=self.forecaster, cv=self.cv,
                                   param_grid=self.param_grid,
                                   scorer=self.metric)
        search_cv.fit(y_train)

        return search_cv

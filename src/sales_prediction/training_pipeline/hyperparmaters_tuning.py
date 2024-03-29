from abc import ABC, abstractmethod
from sklearn.model_selection import BaseCrossValidator
from sktime.forecasting.base import BaseForecaster
from sktime.forecasting.model_selection import (ForecastingGridSearchCV,
                                                ForecastingRandomizedSearchCV)


class AbstractTuningHyperParams(ABC):
    def __init__(self, forecaster: BaseForecaster, cv: BaseCrossValidator,
                 metric, param_grid):
        self.forecaster = forecaster
        self.cv = cv
        self.metric = metric
        self.param_grid = param_grid

    @abstractmethod
    def fit(self, y_train):
        pass


class GridSearchTuning(AbstractTuningHyperParams):
    def fit(self, y_train):
        search_cv = ForecastingGridSearchCV(forecaster=self.forecaster, cv=self.cv,
                                            param_grid=self.param_grid,
                                            scoring=self.metric)
        search_cv.fit(y_train)
        return self


class RandomizedSearchTuning(AbstractTuningHyperParams):
    def fit(self, y_train):
        search_cv = ForecastingRandomizedSearchCV(forecaster=self.forecaster, cv=self.cv,
                                                  param_distributions=self.param_grid,
                                                  scoring=self.metric)
        search_cv.fit(y_train)
        return self

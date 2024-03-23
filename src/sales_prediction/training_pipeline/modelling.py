from sktime.transformations.series.difference import Differencer
from sktime.transformations.series.detrend import Deseasonalizer
from sklearn.ensemble import HistGradientBoostingRegressor
from sktime.forecasting.compose import make_reduction, ForecastingPipeline


def create_model() -> ForecastingPipeline:
    """
    Create the forecasting pipeline

    Args:
        None

    Returns:
        ForecastingPipeline: The forecasting pipeline
    """
    forecaster = make_reduction(
        HistGradientBoostingRegressor(
            max_depth=30, max_iter=1000, random_state=42, learning_rate=0.1, max_bins=100
        ),
    )
    forecaster_pipeline = ForecastingPipeline(
        steps=[
            ("deseasonalizer", Deseasonalizer(sp=12)),
            ("differencer", Differencer(lags=1)),
            ("forecaster", forecaster),
        ]
    )
    return forecaster_pipeline

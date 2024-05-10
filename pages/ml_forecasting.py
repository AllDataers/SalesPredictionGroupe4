import streamlit as st
import pandas as pd
import plotly.express as px

from src.sales_prediction.jobs.inference import InferenceJob
from sktime.forecasting.base import ForecastingHorizon
from sales_prediction.training_pipeline.data_prep import prepare_data
from sales_prediction.utils import load_config

start_date = "2020-01-01"
end_date = "2020-06-01"
date_range = pd.date_range(start=start_date, end=end_date, freq="D")
fh_2020 = ForecastingHorizon(date_range, is_relative=False)
config_path = "src/config/forecasting_config.yaml"
df = pd.read_csv("data/processed_data/sales_2019.csv", parse_dates=["OrderDate"])
_, validate_df = prepare_data(df)
config = load_config.load_config(config_path)
st.set_page_config("ML Forecasting", "📊")
st.title("ML Forecasting")
forecaster = InferenceJob.from_path(config.get("model_path2"))
fh_validate = ForecastingHorizon(validate_df.index, is_relative=False)
past_prediction = forecaster.predict(fh=fh_validate).resample("D").sum()
y_pred = forecaster.predict(fh=fh_2020)
y_pred = y_pred.resample("D").sum()
fig = px.line(title="Predicted vs Actual Sales by day", width=900, height=400)
fig.add_scatter(
    y=validate_df.values, x=validate_df.index, mode="lines+markers", name="Actual Sales"
)
fig.add_scatter(
    y=past_prediction.values,
    x=past_prediction.index,
    mode="lines+markers",
    name="Mid-2019 Predicted Sales",
)
fig.add_scatter(
    y=y_pred.values, x=y_pred.index, mode="lines+markers", name="Predicted Sales"
)
st.plotly_chart(fig)

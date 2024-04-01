import streamlit as st
import pandas as pd
import plotly.express as px

from src.sales_prediction.jobs.inference import InferenceJob
from sktime.forecasting.base import ForecastingHorizon
from sales_prediction.utils import load_config

start_date = '2020-01-01'
end_date = '2020-06-01'
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
fh_2020 = ForecastingHorizon(date_range, is_relative=False)
config_path = "src/config/forecasting_config.yaml"
df = pd.read_csv("data/processed_data/sales_2019.csv", parse_dates=["OrderDate"])
config = load_config.load_config(config_path)
st.set_page_config("ML Forecasting", "📊")
st.title("ML Forecasting")
forecaster = InferenceJob.from_path(config.get("model_path2"))
df = df.set_index(keys=["OrderDate"])
y_pred = forecaster.predict(fh=fh_2020)
y_pred = y_pred.resample("D").sum()
fig = px.line(y=y_pred.values, x=y_pred.index, labels={"x": "Date", "y": "Predicted Sales"},
              title="Predicted Sales by day", markers=True)
st.plotly_chart(fig)
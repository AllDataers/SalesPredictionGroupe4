import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/processed_data/sales_2019.csv", parse_dates=["OrderDate"])

st.set_page_config("EDA", "📊")
st.title("EDA")
df = df.set_index(keys=["OrderDate"])
sales_by_day = df["Sales"].resample("D").sum()
fig = px.line(sales_by_day, x=sales_by_day.index, y="Sales", title="Sales by day", markers=True)
st.plotly_chart(fig)

df_grouped = df.groupby('Product')['QuantityOrdered'].sum().reset_index()
df_grouped = df_grouped.sort_values(by='QuantityOrdered', ascending=True)

fig = px.bar(df_grouped, y='Product', x='QuantityOrdered', title='Quantity Ordered by Product',
             orientation='h', color='QuantityOrdered', color_continuous_scale=px.colors.sequential.Emrld)
st.plotly_chart(fig)


df_cityQ = df.groupby('CityName')['QuantityOrdered'].sum().reset_index()
df_cityQ = df_cityQ.sort_values(by='QuantityOrdered', ascending=True)

fig = px.bar(df_cityQ, y='CityName', x='QuantityOrdered', title='Quantity Ordered by City',
             orientation='h', color='QuantityOrdered', color_continuous_scale=px.colors.sequential.Emrld)
st.plotly_chart(fig)

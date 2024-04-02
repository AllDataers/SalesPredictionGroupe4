import streamlit as st
import pandas as pd
import plotly.express as px


def get_df_by_city(df: pd.DataFrame, cities: list):
    return df[df['CityName'].isin(cities)]


def get_sales_by_product(df: pd.DataFrame, products: list):
    return df[df['Product'].isin(products)]


def get_sales_by_month(df: pd.DataFrame, months: list):
    return df[df['Month'].isin(months)]


df = pd.read_csv("data/processed_data/sales_2019.csv", parse_dates=["OrderDate"])

st.set_page_config("EDA", "📊")
st.title("EDA")
df = df.set_index(keys=["OrderDate"])
sales_by_day = df["Sales"].resample("D").sum()
fig = px.line(sales_by_day, x=sales_by_day.index, y="Sales", title="Sales by day", markers=True)
st.plotly_chart(fig)

col = st.columns(1)

city = st.selectbox("Select City", df["CityName"].unique(), key="city", on_change=st.experimental_rerun)

df_city = get_df_by_city(df, [city])
sales_by_day = df_city.groupby("Product")["Sales"].sum().reset_index()
sales_by_day = sales_by_day.sort_values(by="Sales", ascending=True)
fig = px.bar(sales_by_day, y="Product", x="Sales", title=f"Sales by Product in {city}", color="Sales", color_continuous_scale=px.colors.sequential.Emrld)
col[0].plotly_chart(fig)

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

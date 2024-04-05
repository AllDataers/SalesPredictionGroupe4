import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium import plugins
from folium.plugins import HeatMap
import geocoder
import geopy
import math
from streamlit_folium import st_folium

st.set_page_config("EDA", "📊", layout="wide")


def get_df_by_city(df: pd.DataFrame, cities: list):
    return df[df["CityName"].isin(cities)]


def get_sales_by_product(df: pd.DataFrame, products: list):
    return df[df["Product"].isin(products)]


def get_sales_by_month(df: pd.DataFrame, months: list):
    return df[df["Month"].isin(months)]


def get_street(row):
    address = "{}, {}".format(row["StreetName"], row["ZipAddress"])
    return address


def get_radius(row, min_value, max_value):
    radius = math.sqrt((max_value - row["total_sales"]))
    if row["total_sales"] == max_value:
        radius = math.sqrt(max_value - min_value + 1)
    return radius / 10


@st.cache_data
def create_heatmap(df_city):
    top10_df = (
        df_city.drop_duplicates(subset="street")
        .sort_values(by="total_sales", ascending=False)
        .head(10)
    )
    center = [top10_df["lat"].values[0], top10_df["long"].values[0]]
    m = folium.Map(location=center, zoom_start=10)
    url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"

    max_value = top10_df["total_sales"].max()
    min_value = top10_df["total_sales"].min()
    geojson = requests.get(url).json()
    for idx, row in top10_df.iterrows():
        all_loc = []
        street = row["street"]
        lat, long = row["lat"], row["long"]
        total_sales = row["total_sales"]
        color = "red" if row["total_sales"] == max_value else "blue"
        folium.Marker(
            location=[lat, long],
            opacity=0.5,
            tooltip=f"<body>Street: {street} <br> Sales: {round(total_sales / 1000000, 3)}M</body>",
            popup=street,
        ).add_to(m)
        folium.CircleMarker(
            location=[lat, long],
            radius=get_radius(row=row, min_value=min_value, max_value=max_value),
            fill=True,
            color=color,
        ).add_to(m)
        all_loc.append([lat, long, total_sales])
    # HeatMap(all_loc, weight_len=3).add_to(m)
    folium.LayerControl().add_to(m)
    return m


def format_number(num):
    print(num)
    if num >= 1_000_000:
        return (
            f"{num // 1_000_000}M"
            if num % 1_000_000 == 0
            else f"{num / 1_000_000:.1f}M"
        )
    elif num >= 1_000:
        return f"{num // 1_000}K" if num % 1_000 == 0 else f"{num / 1_000:.1f}K"
    elif num >= 100:
        return f"{num:.1f}"
    return f"{num:.0f}"


@st.cache_data
def calculate_difference(
    df: pd.DataFrame,
    time_column: str,
    value_column: str,
    group_column: str,
    time_values: list,
):
    diff_df = df.groupby([time_column, group_column], as_index=False).agg(
        {value_column: "sum"}
    )
    diff_df.columns = [
        time_column,
        group_column,
        f"{value_column}_{time_column}_{group_column}",
    ]

    filtered_df = diff_df[diff_df[time_column].isin(time_values)]

    pivot_df = filtered_df.pivot(
        index=group_column,
        columns=time_column,
        values=f"{value_column}_{time_column}_{group_column}",
    )

    pivot_df["difference"] = (
        pivot_df[time_values[-1]] - pivot_df[time_values[0]]
    ) / pivot_df[time_values[0]]

    result_df = pivot_df.reset_index()

    return result_df


def display_metrics(result_df, time_column, group_column):
    max_value = result_df.max()[time_column]
    max_label = result_df.loc[result_df[time_column].idxmax()][group_column]
    max_delta = "{:.2%}".format(result_df.max()["difference"])

    min_value = result_df.min()[time_column]
    min_label = result_df.loc[result_df[time_column].idxmin()][group_column]
    min_delta = "{:.2%}".format(result_df.min()["difference"])

    st.metric(label=max_label, value=format_number(max_value), delta=max_delta)
    st.metric(label=min_label, value=format_number(min_value), delta=min_delta)


df = pd.read_csv("data/processed_data/sales_2019.csv", parse_dates=["OrderDate"])
df = df.set_index(keys=["OrderDate"])
df_by_city_name = df.groupby("CityName")["Sales"].sum().reset_index()
df_by_city_name = df_by_city_name.sort_values(by="Sales", ascending=True)
metric_col = st.columns(2, gap="large")
tseries_col = st.columns(1)

st.title("Sales Dashboard - 2019")

col = st.columns((3, 4.5, 3), gap="medium")
with st.sidebar:
    city = st.selectbox(
        "Select City", df["CityName"].unique(), key="city", on_change=st.rerun
    )

    df_city = get_df_by_city(df, [city])
    sales_by_day = df_city.groupby("Product")["Sales"].sum().reset_index()
    sales_by_day = sales_by_day.sort_values(by="Sales", ascending=True)
    df_city = df[df["CityName"] == city].copy()
    print(df_city.columns)
    df_city["street"] = df_city.apply(get_street, axis=1)
    diff_df = df_city.groupby(["Month", "street"], as_index=False).agg(
        sales_month_street=("Sales", "sum")
    )
    nov_dec_df = diff_df[diff_df["Month"].isin([11, 12])]
    pivot_df = nov_dec_df.pivot(
        index="street", columns="Month", values="sales_month_street"
    )
    pivot_df["difference"] = (pivot_df[12] - pivot_df[11]) / pivot_df[11]
    result_df = pivot_df.reset_index()

    total_sales = df_city.groupby(["street"], as_index=False).agg(
        total_sales=("Sales", "sum")
    )
    df_city = df_city.merge(total_sales, on="street", how="right")
    df_city = df_city.dropna()

    diff_product_df = calculate_difference(
        df_city, "Month", "Sales", "Product", [11, 12]
    )

    fig_product = px.bar(
        sales_by_day,
        y="Product",
        x="Sales",
        title=f"Sales by Product in {city}",
        color="Sales",
        color_continuous_scale=px.colors.sequential.Emrld,
    )
    with metric_col[0]:
        st.write(
            """
                <b>Top/Bottom Sales By Street</b>
                """,
            unsafe_allow_html=True,
        )
        display_metrics(result_df, 12, "street")
    with metric_col[1]:
        st.write(
            """
                <b>Top/Bottom Product By Sales</b>
                """,
            unsafe_allow_html=True,
        )
        display_metrics(diff_product_df, 12, "Product")
    with col[0]:
        fig_sales = px.bar(
            df_by_city_name,
            y="CityName",
            x="Sales",
            title="Sales by City",
            orientation="h",
            color="Sales",
            color_continuous_scale=px.colors.sequential.Emrld,
        )
        st.plotly_chart(fig_sales)
    with col[1]:
        st.write(
            """
                <b>Top 10 Sales By Street</b>
                """,
            unsafe_allow_html=True,
        )
        st_folium(create_heatmap(df_city=df_city), width=400, height=300)
    with col[2]:
        st.plotly_chart(fig_product)

    with tseries_col[0]:
        st.write(
            """
                <b>Sales By Day</b>
                """,
            unsafe_allow_html=True,
        )
        sales_by_day = get_df_by_city(df, [city]).resample("D").sum()
        fig = px.line(
            sales_by_day,
            x=sales_by_day.index,
            y=f"Sales",
            title="Sales by day in 2019 for",
            markers=True,
        )
        st.plotly_chart(fig)

import streamlit as st
import pandas as pd

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/labor_stats.csv")


df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
year_range = st.sidebar.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2022, 2023))
metric = st.sidebar.selectbox("Select Metric", df["series_id"].unique())

# Filter Data
filtered_data = df[(df["series_id"] == metric) & (df["year"].between(year_range[0], year_range[1]))]

# Main Dashboard
st.title("US Labor Statistics Dashboard")
st.line_chart(filtered_data.pivot(index="year", columns="period_name", values="value"))
st.write(filtered_data)

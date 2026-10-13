import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Alberta Oil Production", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("Data/clean_monthly_production.csv", parse_dates=["date"])


monthly = load_data()

st.title("Alberta Oil Production Dashboard")
st.write(
    "Monthly crude oil and equivalent production in Alberta, 2017 to 2025. "
    "Source: Alberta Energy Regulator, ST3 monthly statistics."
)

# ---------- Feature 1: monthly graph with date-range selector ----------
st.header("Monthly production")

start, end = st.slider(
    "Select a date range",
    min_value=monthly["date"].min().to_pydatetime(),
    max_value=monthly["date"].max().to_pydatetime(),
    value=(
        monthly["date"].min().to_pydatetime(),
        monthly["date"].max().to_pydatetime(),
    ),
    format="MMM YYYY",
)

measure = st.radio(
    "Measure",
    ["Monthly total (million m³ per month)", "Average per day (thousand m³ per day)"],
    horizontal=True,
)

view = monthly[(monthly["date"] >= start) & (monthly["date"] <= end)].copy()

if measure.startswith("Monthly total"):
    view["value"] = view["production_m3"] / 1e6
    y_label = "Million m³ per month"
else:
    view["value"] = view["avg_daily_m3"] / 1e3
    y_label = "Thousand m³ per day"

fig = px.line(view, x="date", y="value", labels={"date": "Month", "value": y_label})
fig.update_traces(hovertemplate="%{x|%b %Y}: %{y:.1f}")
st.plotly_chart(fig)

# ---------- Feature 2: yearly summary ----------
st.header("Yearly summary")
st.caption("Covers all nine complete years, regardless of the date range above.")

yearly = (
    monthly.groupby(monthly["date"].dt.year)
    .agg(total_m3=("production_m3", "sum"), days=("days_in_month", "sum"))
    .reset_index()
    .rename(columns={"date": "year"})
)
yearly["total_million_m3"] = yearly["total_m3"] / 1e6
# Daily average = yearly total / days in that year (366 in leap years)
yearly["avg_daily_thousand_m3"] = yearly["total_m3"] / yearly["days"] / 1e3
yearly["change_vs_prev_year_pct"] = yearly["total_m3"].pct_change() * 100

fig_year = px.bar(
    yearly,
    x="year",
    y="total_million_m3",
    labels={"year": "Year", "total_million_m3": "Million m³ per year"},
)
fig_year.update_xaxes(type="category")
st.plotly_chart(fig_year)

table = yearly[
    ["year", "total_million_m3", "avg_daily_thousand_m3", "change_vs_prev_year_pct"]
].rename(
    columns={
        "year": "Year",
        "total_million_m3": "Total (million m³)",
        "avg_daily_thousand_m3": "Average per day (thousand m³)",
        "change_vs_prev_year_pct": "Change vs previous year (%)",
    }
)
st.dataframe(table.round(1), hide_index=True)
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
# ---------- Feature 3: findings ----------
st.header("Three findings")

st.markdown(
    """
**1. Production grew about 30% from 2017 to 2025.**
Average daily production rose from 506 to 659 thousand m³ per day. It increased in every year except 2020, and growth was weak in 2019 (+0.9%).

**2. The 2020 drop was sharp but short, and mostly came from oil sands.**
2020 averaged 530 thousand m³ per day, 5.1% below 2019. Between February and May 2020, daily production fell by about 122 thousand m³: roughly 76% from oil sands, 23% from conventional crude, and 1% from condensate. Production was above 2019 levels again in 2021. The AER data does not state a cause.

**3. Oil sands make up about 84% of production, and that share barely changed.**
The oil sands share stayed between 83% and 86% every year, so most of the growth since 2017 (roughly 85%) came from oil sands simply because they are most of the total.
"""
)

# ---------- Feature 4: source and methods ----------
st.header("Source and methods")

st.markdown(
    """
**Source.** Alberta Energy Regulator (AER), *ST3: Alberta Energy Resource Industries Monthly Statistics*, "Oil" supply and disposition files, 2017 to 2025.

**What is measured.** "Crude oil and equivalent": conventional crude oil, condensate, and oil sands production (bitumen and upgraded synthetic crude), using AER's "Total Production" row.

**Units.** Cubic metres (m³). Monthly values are monthly totals. Yearly totals are the sum of the 12 months. Average per day is the total divided by the number of days (monthly: days in that month; yearly: 365, or 366 in 2020 and 2024). Averaging the 12 monthly values would be wrong, because months have different lengths.

**Missing values and checks.** The final table has 108 months (nine years × 12), with no missing values and no duplicate months. For every year, the sum of the 12 months matches AER's own year-to-date total, and conventional crude + condensate + oil sands equals total production in every month.

**Limitations.**
- Nine years of data, not ten, because the 2016 file was not available on the AER page.
- AER may amend earlier numbers in later releases, so figures can differ from other published versions.
- AER renamed some rows between years, so the loader checks each known label.
- The data shows what changed, not why.
"""
)
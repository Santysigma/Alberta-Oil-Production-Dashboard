from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Alberta Oil Production", layout="wide")

M3_TO_BARRELS = 6.29


@st.cache_data
def load_data():
    return pd.read_csv("Data/clean_monthly_production.csv", parse_dates=["date"])


monthly = load_data()
FIRST = monthly["date"].min().to_pydatetime()
LAST = monthly["date"].max().to_pydatetime()
LAST_3Y_START = (pd.Timestamp(LAST) - pd.DateOffset(months=35)).to_pydatetime()


def set_range(start, end):
    st.session_state["date_range"] = (start, end)


st.title("Alberta Oil Production Dashboard")
st.write(
    "Monthly crude oil and equivalent production in Alberta, 2017 to 2025. "
    "Source: Alberta Energy Regulator, ST3 monthly statistics."
)
st.caption(
    "1 m³ of oil is about 6.29 barrels. "
    "'Crude oil and equivalent' includes conventional crude, condensate, and oil sands."
)

# ---------- Feature 1: monthly graph with date-range selector ----------
st.header("Monthly production")
st.write(
    "Pick a range with the buttons, or drag the **left handle** (start month) "
    "and the **right handle** (end month) of the slider."
)

b1, b2, b3, b4 = st.columns(4)
b1.button("All years", on_click=set_range, args=(FIRST, LAST))
b2.button("Last 3 years", on_click=set_range, args=(LAST_3Y_START, LAST))
b3.button("2020 only", on_click=set_range, args=(datetime(2020, 1, 1), datetime(2020, 12, 1)))
b4.button("Spring 2017 dip", on_click=set_range, args=(datetime(2017, 1, 1), datetime(2017, 8, 1)))

start, end = st.slider(
    "Date range (drag either end)",
    min_value=FIRST,
    max_value=LAST,
    value=(FIRST, LAST),
    key="date_range",
    format="MMM YYYY",
    help="Move the left handle to set the start month and the right handle to set the end month.",
)

start_month = pd.Timestamp(start.year, start.month, 1)
view = monthly[(monthly["date"] >= start_month) & (monthly["date"] <= end)].copy()
st.caption(f"Showing {start_month:%b %Y} to {end:%b %Y} ({len(view)} months)")

# Summary numbers for the selected range
avg_k = view["production_m3"].sum() / view["days_in_month"].sum() / 1e3
hi = view.loc[view["avg_daily_m3"].idxmax()]
lo = view.loc[view["avg_daily_m3"].idxmin()]

c1, c2, c3 = st.columns(3)
c1.metric(
    "Average per day",
    f"{avg_k:,.0f} thousand m³",
    help=f"About {avg_k * M3_TO_BARRELS:,.0f} thousand barrels per day",
)
c2.metric("Highest month", f"{hi['date']:%b %Y}")
c2.caption(f"{hi['avg_daily_m3'] / 1e3:,.0f} thousand m³ per day")
c3.metric("Lowest month", f"{lo['date']:%b %Y}")
c3.caption(f"{lo['avg_daily_m3'] / 1e3:,.0f} thousand m³ per day")

tab_total, tab_source = st.tabs(["Total production", "By source"])

with tab_total:
    measure = st.radio(
        "Measure",
        ["Monthly total (million m³ per month)", "Average per day (thousand m³ per day)"],
        horizontal=True,
    )
    plot = view.copy()
    if measure.startswith("Monthly total"):
        plot["value"] = plot["production_m3"] / 1e6
        y_label = "Million m³ per month"
    else:
        plot["value"] = plot["avg_daily_m3"] / 1e3
        y_label = "Thousand m³ per day"

    fig = px.line(plot, x="date", y="value", labels={"date": "Month", "value": y_label})
    fig.update_traces(hovertemplate="%{x|%b %Y}: %{y:.1f}")
    st.plotly_chart(fig)

with tab_source:
    st.write("Average production per day, split by source.")
    parts = view.melt(
        id_vars=["date", "days_in_month"],
        value_vars=["conventional_m3", "condensate_m3", "oil_sands_m3"],
        var_name="source",
        value_name="m3",
    )
    parts["thousand_m3_per_day"] = parts["m3"] / parts["days_in_month"] / 1e3
    parts["source"] = parts["source"].map(
        {
            "conventional_m3": "Conventional crude",
            "condensate_m3": "Condensate",
            "oil_sands_m3": "Oil sands",
        }
    )
    fig_src = px.area(
        parts,
        x="date",
        y="thousand_m3_per_day",
        color="source",
        labels={"date": "Month", "thousand_m3_per_day": "Thousand m³ per day", "source": "Source"},
    )
    st.plotly_chart(fig_src)

st.download_button(
    "Download the selected months (CSV)",
    view.to_csv(index=False),
    file_name="alberta_oil_selected_months.csv",
    mime="text/csv",
)

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
st.dataframe(
    table.round(1),
    hide_index=True,
    column_config={
        "Total (million m³)": st.column_config.NumberColumn(format="%.1f"),
        "Average per day (thousand m³)": st.column_config.NumberColumn(format="%.1f"),
        "Change vs previous year (%)": st.column_config.NumberColumn(format="%.1f"),
    },
)

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

**Units.** Cubic metres (m³). 1 m³ is about 6.29 barrels. Monthly values are monthly totals. Yearly totals are the sum of the 12 months. Average per day is the total divided by the number of days (monthly: days in that month; yearly: 365, or 366 in 2020 and 2024). Averaging the 12 monthly values would be wrong, because months have different lengths.

**Missing values and checks.** The final table has 108 months (nine years × 12), with no missing values and no duplicate months. For every year, the sum of the 12 months matches AER's own year-to-date total, and conventional crude + condensate + oil sands equals total production in every month.

**Limitations.**
- Nine years of data, not ten, because the 2016 file was not available on the AER page.
- AER may amend earlier numbers in later releases, so figures can differ from other published versions.
- AER renamed some rows between years, so the loader checks each known label.
- The data shows what changed, not why.
"""
)
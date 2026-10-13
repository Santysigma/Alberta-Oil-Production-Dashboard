import pandas as pd
import plotly.express as px

monthly = pd.read_csv("Data/clean_monthly_production.csv", parse_dates=["date"])

# Chart 1: total monthly production (million m3 per month)
monthly["total_million"] = monthly["production_m3"] / 1e6
fig1 = px.line(
    monthly,
    x="date",
    y="total_million",
    title="Alberta crude oil and equivalent production, monthly total",
    labels={"date": "Month", "total_million": "Million m³ per month"},
)
fig1.update_traces(hovertemplate="%{x|%b %Y}: %{y:.1f} million m³")
fig1.show()

# Chart 2: breakdown by source, shown as average daily production
parts = monthly.melt(
    id_vars=["date", "days_in_month"],
    value_vars=["conventional_m3", "condensate_m3", "oil_sands_m3"],
    var_name="source",
    value_name="m3",
)
parts["thousand_m3_per_day"] = parts["m3"] / parts["days_in_month"] / 1000
parts["source"] = parts["source"].map({
    "conventional_m3": "Conventional crude",
    "condensate_m3": "Condensate",
    "oil_sands_m3": "Oil sands",
})

fig2 = px.area(
    parts,
    x="date",
    y="thousand_m3_per_day",
    color="source",
    title="Alberta production by source, average per day",
    labels={"date": "Month", "thousand_m3_per_day": "Thousand m³ per day", "source": "Source"},
)
fig2.show()
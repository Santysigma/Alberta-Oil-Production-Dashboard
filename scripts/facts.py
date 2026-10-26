import pandas as pd

m = pd.read_csv("Data/clean_monthly_production.csv", parse_dates=["date"])

# Yearly totals and daily averages (days = days in that year)
y = m.groupby(m["date"].dt.year).agg(
    total=("production_m3", "sum"),
    days=("days_in_month", "sum"),
    conv=("conventional_m3", "sum"),
    cond=("condensate_m3", "sum"),
    sands=("oil_sands_m3", "sum"),
)
y["avg_daily_k"] = y["total"] / y["days"] / 1e3
y["yoy_pct"] = y["total"].pct_change() * 100

print(y[["avg_daily_k", "yoy_pct"]].round(1))

print("\nGrowth 2017 to 2025 (%):",
      round((y.loc[2025, "total"] / y.loc[2017, "total"] - 1) * 100, 1))

print("\nOil sands share of total (%):")
print((y["sands"] / y["total"] * 100).round(1))

print("\nLowest 3 months by daily average:")
print(m.nsmallest(3, "avg_daily_m3")[["date", "avg_daily_m3"]].round(0))

print("\nHighest 3 months by daily average:")
print(m.nlargest(3, "avg_daily_m3")[["date", "avg_daily_m3"]].round(0))

# 2020 dip: which source fell most between Feb and May 2020?
feb = m[m["date"] == "2020-02-01"].iloc[0]
may = m[m["date"] == "2020-05-01"].iloc[0]
print("\nChange Feb to May 2020, thousand m3/day:")
for col, name in [("conventional_m3", "Conventional"), ("condensate_m3", "Condensate"), ("oil_sands_m3", "Oil sands")]:
    d = may[col] / may["days_in_month"] / 1e3 - feb[col] / feb["days_in_month"] / 1e3
    print(f"  {name}: {d:.1f}")
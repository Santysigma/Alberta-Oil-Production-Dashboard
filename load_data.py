import glob
import os
import re
import pandas as pd

# AER renamed some rows between years, so each series lists the labels it has used
SERIES = {
    "production_m3": ["Total Production"],
    "conventional_m3": ["Total Crude Oil Production", "Total Conventional Oil Production"],
    "condensate_m3": ["Condensate Production"],
    "oil_sands_m3": ["Total Oil Sands Production"],
}


def find_row(df, labels, options, path):
    for name in options:
        hits = df[labels == name]
        if len(hits) > 0:
            return hits.iloc[0]
    raise ValueError(f"{path}: none of these labels found: {options}")


def load_year(path):
    """Read one AER file and return 12 rows: date + production series (m3)."""
    year = int(re.search(r"(20\d\d)", os.path.basename(path)).group(1))

    df = pd.read_excel(path, sheet_name="Data", header=None)
    labels = df[1].astype(str).str.strip()

    out = {"date": pd.date_range(f"{year}-01-01", periods=12, freq="MS")}
    for column, options in SERIES.items():
        row = find_row(df, labels, options, path)
        out[column] = row.iloc[3:15].astype(float).tolist()
    return pd.DataFrame(out)


frames = [load_year(path) for path in sorted(glob.glob("Data/*.xlsx"))]
monthly = pd.concat(frames, ignore_index=True).sort_values("date")

monthly["days_in_month"] = monthly["date"].dt.days_in_month
monthly["avg_daily_m3"] = monthly["production_m3"] / monthly["days_in_month"]

monthly.to_csv("Data/clean_monthly_production.csv", index=False)

# ---- Checks ----
print("Rows (expect 108):", len(monthly))
print("Duplicate dates:", monthly["date"].duplicated().sum())
print("Missing values:", int(monthly.isna().sum().sum()))

parts = monthly["conventional_m3"] + monthly["condensate_m3"] + monthly["oil_sands_m3"]
gap = (parts - monthly["production_m3"]).abs()
print("Biggest gap between the 3 parts and Total Production (m3):", round(gap.max(), 1))
print("Months where the gap is over 1 m3:", int((gap > 1).sum()))
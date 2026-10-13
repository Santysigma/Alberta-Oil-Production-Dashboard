import pandas as pd

df = pd.read_excel("Data/Oil_2017.xlsx", sheet_name="Data", header=None)
labels = df[1].astype(str).str.strip()

wanted = [
    "Total Crude Oil Production",
    "Condensate Production",
    "Total Oil Sands Production",
    "Total Production",
]

print(df.iloc[4, 3:9].tolist())  # Jan to Jun

for name in wanted:
    hits = df[labels == name]
    if len(hits) == 0:
        print(name, "-> not found")
    else:
        print(name, hits.iloc[0].iloc[3:9].astype(float).round(0).tolist())
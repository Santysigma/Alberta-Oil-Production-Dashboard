import pandas as pd

df = pd.read_excel("Data/Oil_2017.xlsx", sheet_name="Data", header=None)
for label in df[1].dropna().astype(str).str.strip():
    if "Crude" in label or "Condensate" in label or "Oil" in label:
        print(repr(label))
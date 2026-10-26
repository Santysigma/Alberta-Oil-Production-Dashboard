import glob
import pandas as pd

files = sorted(glob.glob("Data/*.xlsx"))

for path in files:
    xl = pd.ExcelFile(path)
    print("\n", path)
    print("  sheets:", xl.sheet_names)

    sheet = "Data" if "Data" in xl.sheet_names else xl.sheet_names[-1]
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    labels = df[1].astype(str).str.strip()
    hits = df[labels == "Total Production"]

    print("  sheet used:", sheet, "| shape:", df.shape)
    print("  'Total Production' rows found:", len(hits))
    if len(hits) > 0:
        row = hits.iloc[0]
        total = row.iloc[3:15].astype(float).sum()
        print("  sum of Jan-Dec:", round(total, 1), "| YTD column:", row.iloc[16])
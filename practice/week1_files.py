with open("practice/sample.csv") as f:
    for line in f:
        print(line.strip())

import pandas as pd

df = pd.read_csv("practice/sample.csv")
print(df)
print(df["production"].mean())
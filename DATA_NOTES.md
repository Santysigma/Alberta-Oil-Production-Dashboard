# Data notes

## Source
Alberta Energy Regulator (AER), ST3 Alberta Energy Resource Industries Monthly Statistics, "Oil" supply and disposition files.

## Years used
2017 to 2025 (nine complete years). The 2016 file was not available on the AER page, so the analysis covers nine years, not ten. 2026 is excluded because the year is incomplete.

## Unit
Cubic metres (m3). Production values are monthly totals.

## Product definition
"Crude oil and equivalent": conventional crude oil, condensate, and oil sands production (bitumen and upgraded synthetic crude).

## Series used
The "Total Production" row, which AER calculates as total conventional crude oil + condensate + total oil sands production.

## File layout
Each year is a separate Excel file with a "Documentation" sheet and a "Data" sheet. Months Jan to Dec are columns 3 to 14, and rows are labelled lines in column 1. The Year To Date column is not used, because for inventory rows it shows the latest month rather than a sum.

## Checks (Week 3)
- 108 monthly rows (2017 to 2025), no duplicate months, no missing values, 12 months in every year.
- For all nine files, the sum of the 12 monthly values equals AER's Year To Date column for Total Production.
- Cleaned table saved as Data/clean_monthly_production.csv.

## Breakdown check (Week 3 and 4)
Conventional crude + condensate + oil sands equals Total Production in all 108 months (maximum difference 0.0 m3).

## Label differences between years
AER renamed some rows between years. The conventional crude total is "Total Conventional Oil Production" in 2017 and "Total Crude Oil Production" in 2025. "Ultra Heavy" is spelled without a hyphen in 2017. "Total Production", "Condensate Production" and "Total Oil Sands Production" are present in all nine files. The loader (load_data.py) checks each known label for every file.

## Observation: April 2017
April 2017 has the lowest daily average production in the dataset (about 442,500 m3 per day). Between February and April 2017, oil sands production fell by about 1.7 million m3 per month while condensate and conventional crude stayed roughly flat, so the spring 2017 dip is an oil sands effect. The cause is not stated in the AER file.

## Unit cautions
- Yearly total = sum of the 12 monthly values.
- Yearly average per day = yearly total divided by days in that year (366 in 2020 and 2024, 365 otherwise). Do not average the 12 monthly values, because months have different lengths.
- Monthly average per day = monthly total divided by days in that month.
- "Sent for Further Processing" is stored as a negative number, so use Total Production instead of adding the oil sands pieces by hand.
- "Removals from Alberta" has a per-day row. It is a different measure and is not used.

## Limitations
- Later AER releases can amend earlier numbers, so figures may differ from other published versions.
- The data covers reported production only. It does not explain causes of changes.
- Nine years instead of ten, because the 2016 file was not found.
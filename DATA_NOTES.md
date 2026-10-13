# Data notes

**Source:** Alberta Energy Regulator, ST3 Alberta Energy Resource Industries Monthly Statistics, "Oil" supply and disposition files.

**Years used:** 2017 to 2025 (nine complete years). The 2016 file was not available on the AER page, so the analysis covers nine years, not ten.

**Unit:** cubic metres (m3) per month, as monthly totals.

**Product definition:** "Crude oil and equivalent": conventional crude oil, condensate, and oil sands production (bitumen and upgraded synthetic crude).

**Series used:** the "Total Production" row, which AER calculates as total crude oil + condensate + total oil sands production.

**Layout:** each year is a separate Excel file with a "Documentation" sheet and a "Data" sheet. Months Jan to Dec are columns; rows are labelled lines.

**Checks done:** for all nine files the sum of the 12 months equals AER's Year To Date column.

**Cautions**
- Yearly total = sum of monthly values. Yearly daily average = yearly total / days in that year (366 in 2020 and 2024).
- "Sent for Further Processing" is stored as a negative number, so use Total Production instead of adding the pieces.
- The "Removals from Alberta" per-day row is a different measure and is not used.
- Later AER releases may amend earlier numbers.

**Observation:** April 2017 has the lowest daily average production in the dataset (about 442,500 m3/day). Between February and April 2017, oil sands production fell by about 1.7 million m3 per month while condensate and conventional crude stayed roughly flat, so the spring 2017 dip is an oil sands effect. The cause is not stated in the AER file.

**Label differences:** the "Total Crude Oil Production" label is not present in the 2017 file under that name, so breakdown rows need per-year label checks. "Total Production" is present in all nine files and is used for the main series.
# Alberta Oil Production Dashboard

An interactive dashboard exploring ten years of Alberta oil production using public data, with clear graphs, documented methods, and an explanation of the findings.

## Status
Work in progress (week 6 of 8). Currently covers 2017 to 2025 (nine complete years), because the 2016 file was not available on the AER page.

## Data
Alberta Energy Regulator, ST3 Alberta Energy Resource Industries Monthly Statistics ("Oil" supply and disposition files). Unit: cubic metres (m3). See `DATA_NOTES.md` for methods, checks and limitations.

## Tools
Python, pandas, Plotly, Streamlit.

## Run it locally
```bash
git clone https://github.com/Santysigma/alberta-oil-production-dashboard.git
cd alberta-oil-production-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python load_data.py
streamlit run app.py
```

## Project files
- `load_data.py`: reads the yearly AER Excel files and builds one clean monthly table
- `app.py`: the Streamlit dashboard
- `chart.py`: early chart experiments
- `DATA_NOTES.md`: source, units, checks, and limitations
- `Data/`: the downloaded AER files and the cleaned 

## Start the app (after setup) (Personal Note)

```bash
cd ~/Documents/alberta-oil-production-dashboard
source .venv/bin/activate
streamlit run app.py
```

The dashboard opens at http://localhost:8501. Press Ctrl+C in the terminal to stop it.
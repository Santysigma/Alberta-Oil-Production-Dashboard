import pandas as pd


def load():
    return pd.read_csv("Data/clean_monthly_production.csv", parse_dates=["date"])


def test_row_count():
    assert len(load()) == 108


def test_no_duplicates_or_missing():
    m = load()
    assert not m["date"].duplicated().any()
    assert not m.isna().any().any()


def test_months_are_continuous():
    m = load().sort_values("date")
    expected = pd.date_range(m["date"].min(), m["date"].max(), freq="MS")
    assert list(m["date"]) == list(expected)


def test_parts_add_up_to_total():
    m = load()
    parts = m["conventional_m3"] + m["condensate_m3"] + m["oil_sands_m3"]
    assert ((parts - m["production_m3"]).abs() < 1).all()


def test_2025_total_matches_aer():
    m = load()
    total = m[m["date"].dt.year == 2025]["production_m3"].sum()
    assert abs(total - 240697422.1) < 1
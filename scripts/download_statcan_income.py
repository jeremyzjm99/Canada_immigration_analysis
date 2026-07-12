"""Pull a targeted slice of StatCan Table 43-10-0026-01 (immigrant income by
admission cohort) via the WDS API, instead of the ~15GB full-table download.
"""

import requests
import pandas as pd
from pathlib import Path

PRODUCT_ID = 43100026
OUT_PATH = Path("data/raw/statcan_immigrant_income_by_cohort.csv")

ADMISSION_YEARS = {
    8: 2015,
    9: 2016,
    10: 2017,
    11: 2018,
    12: 2019,
    13: 2020,
}

CATEGORIES = {
    1: "Total",
    2: "Family sponsored",
    6: "Economic total",
    7: "Skilled worker/trades",
    8: "Canadian experience class",
    9: "Provincial nominee",
}

STATISTICS = {
    2: "Median total income",
    3: "Median employment income",
}

WDS_BASE = "https://www150.statcan.gc.ca/t1/wds/rest"


def build_coordinates():
    combos = []
    for year_id in ADMISSION_YEARS:
        for cat_id in CATEGORIES:
            for stat_id in STATISTICS:
                coordinate = f"1.1.1.1.{year_id}.{cat_id}.{stat_id}.0.0.0"
                combos.append((year_id, cat_id, stat_id, coordinate))
    return combos


def get_vector_ids(combos):
    body = [{"productId": PRODUCT_ID, "coordinate": c[3]} for c in combos]
    response = requests.post(f"{WDS_BASE}/getSeriesInfoFromCubePidCoord", json=body)
    response.raise_for_status()
    results = response.json()

    vector_map = {}
    for combo, result in zip(combos, results):
        year_id, cat_id, stat_id, coordinate = combo
        vector_map[result["object"]["vectorId"]] = (year_id, cat_id, stat_id)
    return vector_map


def get_vector_data(vector_ids):
    body = [{"vectorId": v, "latestN": 15} for v in vector_ids]
    response = requests.post(f"{WDS_BASE}/getDataFromVectorsAndLatestNPeriods", json=body)
    response.raise_for_status()
    return response.json()


def main():
    combos = build_coordinates()
    print(f"Requesting {len(combos)} vector IDs...")
    vector_map = get_vector_ids(combos)

    print(f"Requesting time series for {len(vector_map)} vectors...")
    data = get_vector_data(list(vector_map.keys()))

    rows = []
    for entry in data:
        obj = entry["object"]
        year_id, cat_id, stat_id = vector_map[obj["vectorId"]]
        for point in obj["vectorDataPoint"]:
            if point["value"] is None:
                continue
            rows.append({
                "admission_cohort_year": ADMISSION_YEARS[year_id],
                "immigrant_category": CATEGORIES[cat_id],
                "statistic": STATISTICS[stat_id],
                "tax_year": int(point["refPer"][:4]),
                "value": point["value"],
            })

    df = pd.DataFrame(rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(df)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
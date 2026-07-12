import requests
from pathlib import Path

FORCE_REFRESH = False # if file existed, skip download, turn to True if you want to update original data.

datasets = {
    "ee_invitations_by_province_category.csv": "https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_Candidates-IntDest.csv",
    "ee_ita_score_breakdown.csv": "https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_candidates-ITA_score.csv",
    "pr_admissions_by_province_immcat.csv": "https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_admissions-ImmCat.csv",
    "pr_admissions_by_citizenship.csv": "https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_admissions-CITZ.csv",
}

for filename, url in datasets.items():
    filepath = Path("data/raw") / filename

    if filepath.exists() and not FORCE_REFRESH:
        print(f"{filepath} file existed, skip download")
    else:
        response = requests.get(url)
        print(response.status_code)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.content)

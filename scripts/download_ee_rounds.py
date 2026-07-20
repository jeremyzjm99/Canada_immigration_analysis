"""Download the official IRCC Express Entry rounds-of-invitations data.

Source: IRCC serves every Express Entry draw since 2015 as JSON at
https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json
(the same data that powers the public "rounds of invitations" page, which
loads it client-side via JavaScript — so a plain HTML scrape misses it).

Each draw gives: date, draw name (category / program), invitations issued,
and the CRS cut-off of the lowest-ranked invited candidate. This is the
authoritative per-draw CRS series used for the selection-layer cutoff trend
and the policy timeline.
"""

import html
import re
from pathlib import Path

import requests
import pandas as pd

URL = "https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json"
OUT_PATH = Path("data/raw/ee_rounds.csv")
FORCE_REFRESH = False  # set True to re-pull the latest draws


def strip_html(value: str) -> str:
    """IRCC embeds anchor tags in some fields; keep just the text."""
    return html.unescape(re.sub("<.*?>", "", str(value))).strip()


def download() -> None:
    if OUT_PATH.exists() and not FORCE_REFRESH:
        print(f"{OUT_PATH} already exists, skip download")
        return

    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    rounds = response.json()["rounds"]

    records = []
    for r in rounds:
        records.append({
            "draw_number": strip_html(r["drawNumber"]),
            "draw_date": r["drawDate"],
            "draw_name": strip_html(r["drawName"]),
            "invitations": int(strip_html(r["drawSize"]).replace(",", "")),
            "crs_cutoff": int(strip_html(r["drawCRS"])),
        })

    df = pd.DataFrame(records)
    df["draw_date"] = pd.to_datetime(df["draw_date"])
    df = df.sort_values("draw_date").reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(df)} draws ({df['draw_date'].min().date()} to "
          f"{df['draw_date'].max().date()}) to {OUT_PATH}")


if __name__ == "__main__":
    download()

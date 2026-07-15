# Data Sources

All datasets are from official Canadian government open data (IRCC and Statistics Canada).
Download is reproducible via the scripts in [`../scripts/`](../scripts/).

Note on suppression: both IRCC datasets suppress or round figures to protect privacy —
values 0–5 are shown as `--`, all other values are rounded to the nearest multiple of 5.
This means summed figures may not equal published totals.

---

## Layer 1 — Selection (who got invited)

**Source dataset A: Express Entry – Invited Candidates, Monthly IRCC Updates**
- Dataset ID: `593e9165-c6ce-4f9b-b519-03d315f92cd4`
- Dataset page: https://open.canada.ca/data/en/dataset/593e9165-c6ce-4f9b-b519-03d315f92cd4

| Local file | Description | Direct download URL |
|---|---|---|
| `raw/ee_invitations_by_province_category.csv` | ITAs by year × province/territory × invitation category (CEC/FSW/FST/PNP) | https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_Candidates-IntDest.csv |
| `raw/ee_ita_score_breakdown.csv` | ITAs additionally broken down by CRS/ITA score band | https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_candidates-ITA_score.csv |

**Known limitation:** this dataset is classified by program category and does **not** include
category-based selection (CBS) draws introduced June 2023 (French, healthcare, STEM, trades,
transport, agriculture). Our totals therefore approximate the non-CBS program-category ITAs.
See project memory / report data-limitations section.

---

## Layer 2 — Flow (where they landed)

**Source dataset B: Express Entry – Permanent Residents, Monthly IRCC Updates**
- Dataset ID: `52e4b14b-597a-4ecf-a184-23a6e69b0d57`
- Dataset page: https://open.canada.ca/data/en/dataset/52e4b14b-597a-4ecf-a184-23a6e69b0d57

| Local file | Description | Direct download URL |
|---|---|---|
| `raw/pr_admissions_by_province_immcat.csv` | PR admissions by year/quarter/month × province × immigration category | https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_admissions-ImmCat.csv |
| `raw/pr_admissions_by_citizenship.csv` | PR admissions by year/quarter/month × province × country of citizenship | https://www.ircc.canada.ca/opendata-donneesouvertes/data/ODP-EE_admissions-CITZ.csv |

---

## Layer 3 — Outcome (how they did economically)

**Statistics Canada Table 43-10-0026-01**
- Title: *Income of immigrant tax filers by immigrant admission category and tax year, for Canada and provinces, 2023 constant dollars*
- Product ID: `43100026`
- Table page: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=4310002601
- Pulled as a targeted slice via the WDS REST API (not the ~15GB full-table download),
  endpoints `getSeriesInfoFromCubePidCoord` and `getDataFromVectorsAndLatestNPeriods`
  under base `https://www150.statcan.gc.ca/t1/wds/rest`.

| Local file | Description |
|---|---|
| `raw/statcan_immigrant_income_by_cohort.csv` | Median income by admission cohort year × immigrant category × income statistic × tax year (Canada-level, both sexes, all ages) |

**Coverage limitation:** income data lags due to tax-filing processing; latest available tax year is 2023.

---

## Supplementary references (policy analysis & reconciliation, not datasets)

| Source | Use | URL |
|---|---|---|
| IRCC Express Entry Year-End Report 2023 | Per-draw ITA tables incl. CBS column; used to reconcile the ITA gap | https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/express-entry-year-end-report-2023.html |
| IRCC Express Entry Year-End Report 2024 | Same, 2024 (CBS re-folded into program categories) | https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/express-entry-year-end-report-2024.html |

Note: canada.ca returns HTTP 403 to default scrapers; fetch with a browser User-Agent.

---

## Reproducibility notes

- The two IRCC datasets update **monthly**; re-running the download at a later date will pull newer
  months. Use the `FORCE_REFRESH` flag in `scripts/download_data.py` to overwrite existing files.
- Raw files are Tab-separated despite the `.csv` extension, UTF-8 encoded. Read with
  `pd.read_csv(path, sep="\t", encoding="utf-8")`.

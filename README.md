# Data

| File | Description | Source (with link) | Licence | Date accessed |
|---|---|---|---|---|
| `colombo_weekly_dengue_2026.csv` | Weekly notified dengue cases, Colombo district, 2026 epidemiological weeks 1–37 (29 Dec 2025 – 13 Sep 2026) | Weekly Epidemiological Report (WER), Epidemiology Unit, Ministry of Health, Sri Lanka, Table 1, column A, as extracted in the `denguedatahub` R package by T. S. Talagala, file `data-raw/srilanka_weekly_data.csv`, commit [`6fd04ff`](https://github.com/thiyangt/denguedatahub/blob/6fd04ff513a5586b2338d02af759e06e3aa771d2/data-raw/srilanka_weekly_data.csv) | Counts from public government surveillance reports; extraction from `denguedatahub` (GPL-3), credited here | 25 Nov 2026 |
| `make_dataset.py` | Script that rebuilds the CSV from the pinned commit above | – | MIT (this repository) | – |

## Columns

| Column | Meaning |
|---|---|
| `year`, `epi_week` | Year and ISO epidemiological week (Monday–Sunday) |
| `week_start`, `week_end` | First and last day of the week |
| `cases_raw` | Value as it appears in the source extraction |
| `status` | `ok`, or `missing` for weeks excluded from the analysis |
| `cases` | Value used in the model (empty when `status` is `missing`) |
| `note` | Reason a week is marked missing |
| `source` | Dataset and commit the row came from |

## Data checks and decisions

- **Spot check against the original report:** week 27 (29 Jun – 5 Jul 2026) is 1,264 cases in both the extraction and WER Vol. 53 No. 28, Table 1. `make_dataset.py` asserts this value.
- **Weeks marked missing (5 of 37):**
  - Weeks 14, 24 and 37: the extracted values (9, 20, 11) are far below the neighbouring weeks and are similarly low for several other districts in the same week, while the national total stays in line with the neighbouring weeks, which points to a parsing error.
  - Weeks 25 and 26: identical values for every district, which means one report was read twice. The true values are unknown.
- Missing weeks are skipped in the likelihood, not filled in.
- **Only Epidemiology Unit (WER) counts are used.** National Dengue Control Unit figures quoted in the news come from a different reporting system and give different totals, so they are not mixed in.
- **Colombo is one row** in WER Table 1 (no separate Colombo Municipal Council row), so no counts are added together.
- **Intervention inside the data:** a special dengue control week ran across Colombo District on 15–21 June 2026 (week 25). This is treated as part of the baseline and listed as a limitation.

## Population

Colombo District population: **2,375,415** (Census of Population and Housing 2024, final report, Department of Census and Statistics, Sri Lanka).

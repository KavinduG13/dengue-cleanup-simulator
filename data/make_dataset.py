"""Build data/colombo_weekly_dengue_2026.csv from the denguedatahub weekly Sri Lanka dataset.

Source: T. S. Talagala, denguedatahub (R package, GPL-3), file data-raw/srilanka_weekly_data.csv,
pinned to one commit so the result never changes. The counts in that file were extracted from the
Weekly Epidemiological Reports (WER), Epidemiology Unit, Ministry of Health, Sri Lanka, Table 1
(weekly notified dengue cases by district, column A).

Run:  python data/make_dataset.py
"""
import pandas as pd

COMMIT = "6fd04ff513a5586b2338d02af759e06e3aa771d2"
URL = ("https://raw.githubusercontent.com/thiyangt/denguedatahub/"
       f"{COMMIT}/data-raw/srilanka_weekly_data.csv")

# Weeks whose extracted values are known to be wrong (checked against other districts and the
# national total): 14, 24 and 37 are parsing errors; 25 and 26 are the same report read twice.
BAD_WEEKS = {14: "parse error (value far below neighbouring weeks and other districts)",
             24: "parse error (value far below neighbouring weeks and other districts)",
             25: "duplicate of week 26 for every district; true value unknown",
             26: "duplicate of week 25 for every district; true value unknown",
             37: "parse error (value far below neighbouring weeks and other districts)"}

raw = pd.read_csv(URL)
col = raw[(raw.year == 2026) & (raw.district.str.strip() == "Colombo")].copy()
col["week"] = col.week.astype(int)
col = col[col.week <= 52]                      # drop a leftover 2025 row labelled week 53

out = pd.DataFrame({"year": 2026, "epi_week": col.week.values})
out["week_start"] = [pd.Timestamp.fromisocalendar(2026, w, 1).date() for w in out.epi_week]
out["week_end"] = [pd.Timestamp.fromisocalendar(2026, w, 7).date() for w in out.epi_week]
out["cases_raw"] = col.cases.astype(int).values
out["status"] = ["missing" if w in BAD_WEEKS else "ok" for w in out.epi_week]
out["cases"] = [pd.NA if w in BAD_WEEKS else c for w, c in zip(out.epi_week, out.cases_raw)]
out["note"] = [BAD_WEEKS.get(w, "") for w in out.epi_week]
out["source"] = f"denguedatahub@{COMMIT[:7]} (from WER Table 1, Epidemiology Unit Sri Lanka)"
out = out.sort_values("epi_week")

assert out.epi_week.is_unique and list(out.epi_week) == list(range(1, out.epi_week.max() + 1))
assert int(out.loc[out.epi_week == 27, "cases"].iloc[0]) == 1264   # checked against WER Vol 53 No 28, Table 1

out.to_csv("data/colombo_weekly_dengue_2026.csv", index=False)
print(out.to_string(index=False))

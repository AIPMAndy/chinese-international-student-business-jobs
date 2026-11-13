"""Reproduce spreadsheet and SQL answers for the synthetic funnel case."""
from pathlib import Path
import csv
import json
from math import isclose
import sqlite3

ROOT = Path(__file__).resolve().parent
def rows(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

funnel, cohorts = rows("funnel.csv"), rows("cohorts.csv")
assert len({(r["month"], r["segment"]) for r in funnel}) == len(funnel)
for row in funnel:
    assert 0 <= int(row["converted_users"]) <= int(row["eligible_users"])
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE funnel (month TEXT, segment TEXT, eligible_users INTEGER, converted_users INTEGER, revenue_cu REAL)")
db.executemany("INSERT INTO funnel VALUES (?,?,?,?,?)", [(r["month"], r["segment"], int(r["eligible_users"]), int(r["converted_users"]), float(r["revenue_cu"])) for r in funnel])
db.execute("CREATE TABLE cohorts (cohort_month TEXT, cohort_customers INTEGER, d30_eligible INTEGER, d30_retained INTEGER, d60_eligible INTEGER, d60_retained INTEGER)")
db.executemany("INSERT INTO cohorts VALUES (?,?,?,?,?,?)", [(r["cohort_month"], int(r["cohort_customers"]), int(r["d30_eligible"]), int(r["d30_retained"]) if r["d30_retained"] else None, int(r["d60_eligible"]), int(r["d60_retained"]) if r["d60_retained"] else None) for r in cohorts])
queries = [q.strip() for q in (ROOT / "analysis.sql").read_text(encoding="utf-8").split(";") if q.strip()]
results = [db.execute(q).fetchall() for q in queries]
monthly, segmented, retention = results
assert monthly[0][1:4] == (2000, 250, .125) and monthly[1][1:4] == (4000, 368, .092)
assert isclose(monthly[1][4] / monthly[0][4] - 1, 0.3028571428571429)
mix_effect = .2 * .2 + .8 * .05 - .125
rate_effect = .2 * (.22 - .2) + .8 * (.06 - .05)
assert isclose(mix_effect, -.045) and isclose(rate_effect, .012)
assert isclose(mix_effect + rate_effect, .092 - .125)
assert retention == [("2026-08", .5, .35), ("2026-09", .46, None), ("2026-10", None, None)]
print(json.dumps({"case": "05-analytics", "status": "passed", "monthly_sql": monthly, "segmented_sql": segmented, "retention_sql": retention, "mix_effect": mix_effect, "within_segment_effect": rate_effect}, ensure_ascii=False))

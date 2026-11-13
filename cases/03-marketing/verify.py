"""Recalculate the teaching simulation, using only Python's standard library."""
from pathlib import Path
import csv
import json
from math import isclose, sqrt

ROOT = Path(__file__).resolve().parent
def rows(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

history = rows("channel_history.csv")
assert len({(r["period"], r["channel"]) for r in history}) == len(history)
total_orders = sum(int(r["attributed_orders"]) for r in history)
revenue = sum(int(r["attributed_orders"]) * float(r["unit_revenue_cu"]) for r in history)
contribution = sum(int(r["attributed_orders"]) * (float(r["unit_revenue_cu"]) - float(r["unit_variable_cost_cu"])) - float(r["spend_cu"]) for r in history)
assert total_orders == 735 and isclose(revenue, 36750) and isclose(contribution, -300)

tests = rows("randomized_tests.csv")
results = {}
for experiment, expected_orders, expected_contribution in [("retargeting", 30, -900), ("prospecting", 80, 400)]:
    by_arm = {r["arm"]: r for r in tests if r["experiment"] == experiment}
    t, c = by_arm["treatment"], by_arm["control"]
    nt, nc = int(t["eligible_people"]), int(c["eligible_people"])
    pt, pc = int(t["converted_people"]) / nt, int(c["converted_people"]) / nc
    assert 0 <= pt <= 1 and 0 <= pc <= 1
    incremental_orders = (pt - pc) * nt
    margin = float(t["unit_revenue_cu"]) - float(t["unit_variable_cost_cu"])
    spend = float(t["spend_cu"])
    incremental_contribution = incremental_orders * margin - spend
    assert isclose(incremental_orders, expected_orders) and isclose(incremental_contribution, expected_contribution)
    se = sqrt(pt * (1 - pt) / nt + pc * (1 - pc) / nc)
    results[experiment] = {"incremental_orders": round(incremental_orders, 4), "incremental_cac_cu": round(spend / incremental_orders, 4), "incremental_contribution_cu": round(incremental_contribution, 4), "rate_difference_95pct_normal_interval": [round(pt - pc - 1.96 * se, 6), round(pt - pc + 1.96 * se, 6)]}
print(json.dumps({"case": "03-marketing", "status": "passed", "history_orders": total_orders, "history_revenue_cu": revenue, "history_contribution_cu": contribution, "experiments": results}, ensure_ascii=False))

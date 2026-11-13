"""Recalculate the fictional account-value and pipeline exercise."""
from pathlib import Path
import csv
import json
from math import isclose

ROOT = Path(__file__).resolve().parent
def rows(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

accounts = {r["account"] for r in rows("accounts.csv")}
pipeline = rows("pipeline.csv")
assert len({r["account"] for r in pipeline}) == len(pipeline)
for r in pipeline:
    assert r["account"] in accounts and 0 <= float(r["probability_assumption"]) <= 1
    if not int(r["qualified"]):
        assert float(r["probability_assumption"]) == 0
p = {r["parameter"]: float(r["value"]) for r in rows("value_assumptions.csv")}
capacity_value = p["users"] * p["manual_hours_per_user_per_week"] * p["working_weeks"] * p["hourly_capacity_value"]
cost = p["annual_subscription"] + p["one_time_implementation"]
base = capacity_value * p["base_realization_rate"] - cost
downside = capacity_value * p["downside_realization_rate"] - cost
raw = sum(float(r["annual_contract_value_cu"]) for r in pipeline)
qualified = sum(float(r["annual_contract_value_cu"]) for r in pipeline if int(r["qualified"]))
weighted = sum(float(r["annual_contract_value_cu"]) * float(r["probability_assumption"]) for r in pipeline if int(r["qualified"]))
assert capacity_value == 48000 and cost == 14000 and base == 14800 and downside == -4400
assert raw == 64000 and qualified == 46000 and weighted == 27200
assert isclose(qualified / p["quarter_quota"], .46) and isclose(weighted / p["quarter_quota"], .272)
print(json.dumps({"case": "06-sales", "status": "passed", "capacity_value_cu": capacity_value, "first_year_cost_cu": cost, "base_net_capacity_value_cu": base, "downside_net_capacity_value_cu": downside, "break_even_realization_rate": cost / capacity_value, "raw_annual_contract_value_cu": raw, "qualified_annual_contract_value_cu": qualified, "weighted_pipeline_cu": weighted}, ensure_ascii=False))

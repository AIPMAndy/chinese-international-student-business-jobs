"""Check inventory timing, capacity and economics for the teaching simulation."""
from pathlib import Path
import csv
import json
from itertools import product

ROOT = Path(__file__).resolve().parent
def rows(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

assumptions = {r["parameter"]: float(r["value"]) for r in rows("assumptions.csv")}
options = {r["option"]: r for r in rows("supply_options.csv")}
demands = rows("demand.csv")
scheduled = {int(r["arrive_week"]): int(r["quantity_units"]) for r in rows("scheduled_receipts.csv")}

def evaluate(quantities, scenario="base"):
    receipts = dict(scheduled)
    cost = 0
    for name, qty in quantities.items():
        option = options[name]
        assert 0 <= qty <= int(option["max_quantity"]) and qty % int(option["lot_size"]) == 0
        week = int(option["arrive_week"])
        receipts[week] = receipts.get(week, 0) + qty
        cost += qty * float(option["unit_cost_cu"])
    inventory = assumptions["initial_inventory"]
    sold = lost = holding = 0
    ending = []
    for row in (r for r in demands if r["scenario"] == scenario):
        week, demand = int(row["week"]), int(row["demand_units"])
        available = inventory + receipts.get(week, 0)
        if available > assumptions["warehouse_capacity_before_demand"]:
            return None
        sales = min(available, demand)
        inventory = available - sales
        sold += sales
        lost += demand - sales
        holding += inventory * assumptions["weekly_holding_cost"]
        ending.append(inventory)
    return {"sold": sold, "lost": lost, "ending": ending, "purchase_cost_cu": cost, "holding_cost_cu": holding, "comparison_contribution_cu": sold * assumptions["sale_price"] - cost - holding}

plans = {}
for row in rows("worked_purchase_plans.csv"):
    plans.setdefault(row["plan"], {})[row["option"]] = int(row["quantity_units"])
a, b = evaluate(plans["A"]), evaluate(plans["B"])
baseline = evaluate({})
assert a["ending"] == [40, 15, 75, 0] and a["comparison_contribution_cu"] == 9220
assert b["ending"] == [40, 65, 75, 0] and b["comparison_contribution_cu"] == 8920
assert baseline["sold"] == 170 and baseline["comparison_contribution_cu"] == 5060
assert evaluate({"regular": 200, "expedite_early": 50, "expedite_late": 0}) is None
feasible = []
for r, e, l in product(range(0, 201, 50), range(0, 101, 25), range(0, 101, 25)):
    result = evaluate({"regular": r, "expedite_early": e, "expedite_late": l})
    if result:
        feasible.append(result["comparison_contribution_cu"])
assert max(feasible) == a["comparison_contribution_cu"]
unchanged_high = evaluate(plans["A"], "high")
adjusted_high = evaluate({"regular": 200, "expedite_early": 25, "expedite_late": 100}, "high")
assert unchanged_high["lost"] == 60
assert adjusted_high["sold"] == 480 and adjusted_high["ending"][-1] == 15 and adjusted_high["comparison_contribution_cu"] == 9770
print(json.dumps({"case": "04-operations", "status": "passed", "baseline": baseline, "plan_a": a, "plan_b": b, "max_over_feasible_combinations": max(feasible), "high_demand_adapted": adjusted_high}, ensure_ascii=False))

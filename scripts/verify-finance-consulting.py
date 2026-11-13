#!/usr/bin/env python3
"""Recalculate the consulting and finance teaching cases using only stdlib.

Run from any directory:
    python scripts/verify-finance-consulting.py

The original CSVs and case validation.json files are read only. The report is
written to audit/consult-finance-calculations.json, or to --output PATH.
This verifies the stated exercise rules; it is not a real financial assessment.
"""

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
from statistics import median


REPO = Path(__file__).resolve().parents[1]
D = Decimal
ZERO = D(0)
CHECKS = []
INPUTS = []


def numeric(value):
    return D(str(value))


def check(name, actual, expected):
    if isinstance(actual, bool) or isinstance(expected, bool):
        passed = actual is expected
    elif isinstance(actual, Decimal) or isinstance(expected, (int, float, Decimal)):
        passed = numeric(actual) == numeric(expected)
    else:
        passed = actual == expected
    CHECKS.append({"check": name, "passed": passed, "actual": actual, "expected": expected})
    if not passed:
        raise AssertionError(f"{name}: actual={actual!r}; expected={expected!r}")


def read_csv(folder, filename):
    path = REPO / "cases" / folder / filename
    INPUTS.append({"path": path.relative_to(REPO).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Empty input: {path.name}")
    if any(r.get("data_type") not in {"synthetic", "synthetic_assumption"} for r in rows):
        raise ValueError(f"Expected teaching data labels in {path.name}")
    return rows


def compare_reference(prefix, actual, reference):
    """Compare each existing reference leaf, without calculating from it."""
    for key, expected in reference.items():
        label = f"{prefix}.{key}"
        if isinstance(expected, dict):
            compare_reference(label, actual[key], expected)
        else:
            check(label, actual[key], expected)


def consult():
    folder = "01-consulting"
    rows = read_csv(folder, "channel-data.csv")
    costs = {r["period"]: r for r in read_csv(folder, "fixed-costs.csv")}
    options = {(r["option_id"], r["parameter"]): numeric(r["value"]) for r in read_csv(folder, "options.csv")}
    by_period = {period: {r["channel"]: r for r in rows if r["period"] == period} for period in ("baseline", "current")}
    check("consulting.channel_sets", sorted(by_period["baseline"]), sorted(by_period["current"]))

    def per_order(r):
        return numeric(r["revenue_per_order_cny"]) * (1-numeric(r["commission_rate"])) - numeric(r["food_cost_per_order_cny"]) - numeric(r["packaging_per_order_cny"])

    def profit(period):
        contribution = sum((numeric(r["orders"]) * per_order(r) for r in by_period[period].values()), ZERO)
        fixed = sum((numeric(costs[period][f]) for f in ("labor_cny", "rent_cny", "other_fixed_cost_cny")), ZERO)
        return contribution-fixed

    base, current = by_period["baseline"], by_period["current"]
    total_orders = sum((numeric(r["orders"]) for r in current.values()), ZERO)
    check("consulting.total_order_counts_unchanged", total_orders, sum((numeric(r["orders"]) for r in base.values()), ZERO))
    for channel in base:
        for field in ("revenue_per_order_cny", "packaging_per_order_cny"):
            check(f"consulting.bridge_assumption.{channel}.{field}", numeric(current[channel][field]), numeric(base[channel][field]))
    for field in ("rent_cny", "other_fixed_cost_cny"):
        check(f"consulting.bridge_assumption.{field}", numeric(costs["current"][field]), numeric(costs["baseline"][field]))

    bridge = {
        "channel_mix": sum(((numeric(current[k]["orders"])-numeric(base[k]["orders"])) * per_order(base[k]) for k in base), ZERO),
        "food": sum((numeric(current[k]["orders"]) * (numeric(base[k]["food_cost_per_order_cny"])-numeric(current[k]["food_cost_per_order_cny"])) for k in base), ZERO),
        "commission": sum((numeric(current[k]["orders"]) * numeric(current[k]["revenue_per_order_cny"]) * (numeric(base[k]["commission_rate"])-numeric(current[k]["commission_rate"])) for k in base), ZERO),
        "labor": numeric(costs["baseline"]["labor_cny"])-numeric(costs["current"]["labor_cny"]),
    }
    base_profit, current_profit = profit("baseline"), profit("current")
    check("consulting.profit_bridge_reconciles", sum(bridge.values(), ZERO), current_profit-base_profit)
    delivery = current["delivery"]
    pickup_contribution = numeric(delivery["revenue_per_order_cny"]) * (1-options[("A", "pickup_commission")]) - numeric(delivery["food_cost_per_order_cny"]) - options[("A", "pickup_packaging")]
    uplift = pickup_contribution-per_order(delivery)
    transfer = options[("A", "delivery_to_pickup_orders")]
    capacity = options[("A", "max_pickup_capacity")]
    check("consulting.pickup_capacity", 0 <= transfer <= capacity, True)
    if uplift <= 0:
        raise ValueError("Pickup does not increase unit contribution under these inputs")
    a = transfer*uplift-options[("A", "promotion")]
    b = total_orders*options[("B", "food_saving")]-options[("B", "quality_cost")]
    c = options[("C", "labor_saving")]
    training = options[("C", "one_time_training")]
    # The 100,000 target comes from brief.md, not from a computed answer.
    target = D("100000")
    needed = target-current_profit-b-c+options[("A", "promotion")]
    threshold = max(ZERO, (needed/uplift).to_integral_value(rounding=ROUND_CEILING))
    threshold_first = max(ZERO, ((needed+training)/uplift).to_integral_value(rounding=ROUND_CEILING))
    check("consulting.stable_threshold_meets_target", current_profit+threshold*uplift-options[("A", "promotion")]+b+c, target)
    check("consulting.first_threshold_meets_target", current_profit+threshold_first*uplift-options[("A", "promotion")]+b+c-training, target)
    result = {
        "baseline_profit": base_profit, "current_profit": current_profit,
        "decline": base_profit-current_profit,
        "stable_three_options": current_profit+a+b+c,
        "first_month_three_options": current_profit+a+b+c-training,
        "stable_pickup_threshold": threshold,
        "first_month_pickup_threshold": threshold_first,
    }
    reference = json.loads((REPO/"cases"/folder/"validation.json").read_text())["results"]
    compare_reference("consulting.reference", result, reference)
    return result, {"profit_bridge": bridge, "option_A_monthly": a, "option_B_monthly": b, "option_C_steady": c, "option_C_first_month": c-training}


def finance():
    folder = "02-finance-accounting"
    p = {r["scenario"]: r for r in read_csv(folder, "pnl-inputs.csv")}
    wc = {r["account"]: r for r in read_csv(folder, "working-capital.csv")}
    cash = {r["item"]: r for r in read_csv(folder, "cash-flows.csv")}
    invoices = read_csv(folder, "invoice-sample.csv")
    forecast = read_csv(folder, "credit-forecast.csv")
    comps = read_csv(folder, "valuation-comps.csv")
    pn = {s: {k:numeric(v) for k,v in r.items() if k not in {"scenario", "data_type"}} for s,r in p.items()}
    pnl = {}
    for scenario, r in pn.items():
        revenue = r["units"]*r["price_cny"]
        ebit = revenue-r["units"]*r["variable_cost_cny"]-r["fixed_opex_cny"]-r["depreciation_cny"]
        pnl[scenario] = {"revenue": revenue, "ebit": ebit, "pretax": ebit-r["interest_cny"]}
    b, a = pn["budget"], pn["actual"]
    bridge = {
        "volume": (a["units"]-b["units"])*(b["price_cny"]-b["variable_cost_cny"]),
        "price": (a["price_cny"]-b["price_cny"])*a["units"],
        "unit_cost": (b["variable_cost_cny"]-a["variable_cost_cny"])*a["units"],
        "fixed_opex": b["fixed_opex_cny"]-a["fixed_opex_cny"],
        "depreciation": b["depreciation_cny"]-a["depreciation_cny"],
    }
    check("finance.ebit_bridge_reconciles", sum(bridge.values(), ZERO), pnl["actual"]["ebit"]-pnl["budget"]["ebit"])
    delta = {k:numeric(r["closing_cny"])-numeric(r["opening_cny"]) for k,r in wc.items()}
    signed = lambda r: numeric(r["amount_cny"])*(1 if r["direction"]=="inflow" else -1)
    operating_items = ("customer_collections", "supplier_payments", "operating_payments", "interest_paid")
    direct = sum((signed(cash[k]) for k in operating_items), ZERO)
    indirect = pnl["actual"]["pretax"]+a["depreciation_cny"]-delta["accounts_receivable"]-delta["inventory"]+delta["accounts_payable"]+delta["accrued_operating_expenses"]
    check("finance.direct_equals_indirect_operating_cash", direct, indirect)
    check("finance.collections_reconcile", numeric(cash["customer_collections"]["amount_cny"]), pnl["actual"]["revenue"]-delta["accounts_receivable"])
    check("finance.supplier_payments_reconcile", numeric(cash["supplier_payments"]["amount_cny"]), a["units"]*a["variable_cost_cny"]+delta["inventory"]-delta["accounts_payable"])
    check("finance.operating_payments_reconcile", numeric(cash["operating_payments"]["amount_cny"]), a["fixed_opex_cny"]-delta["accrued_operating_expenses"])
    ending = numeric(cash["opening_cash"]["amount_cny"])+sum((signed(r) for r in cash.values() if r["direction"]!="opening_balance"), ZERO)

    # Audit exercise gives a 2026-09-30 cutoff and confirms I003 has one
    # service/obligation. This is not a general automatic invoice-deletion rule.
    in_september = lambda date: "2026-09-01" <= date <= "2026-09-30"
    posted = sum((numeric(r["amount_cny"]) for r in invoices if in_september(r["posting_date"])), ZERO)
    unique, confirmed_duplicates = {}, []
    for r in invoices:
        key = (r["vendor_id"], r["invoice_id"], r["amount_cny"], r["po_id"])
        if key in unique:
            if key[:2] != ("V003", "I003"):
                raise ValueError("Duplicate beyond the exercise's confirmed I003 evidence; investigate it")
            confirmed_duplicates.append(r["row_id"])
        else:
            unique[key] = r
    adjusted = sum((numeric(r["amount_cny"]) for r in unique.values() if in_september(r["received_date"])), ZERO)

    credit, gaps = {}, {}
    for scenario in ("base_cny", "downside_cny"):
        f = {r["item"]: numeric(r[scenario]) for r in forecast}
        credit[scenario] = f["opening_cash"]+f["customer_collections"]-sum((f[k] for k in ("supplier_payments", "operating_payments", "interest", "existing_debt_principal_due", "capital_expenditure")), ZERO)
        gaps[scenario] = max(ZERO, f["minimum_cash_buffer"]-credit[scenario])
    target = next(r for r in comps if r["company"]=="Target")
    multiples = [numeric(r["enterprise_value_cny_million"])/numeric(r["revenue_cny_million"]) for r in comps if r["company"]!="Target"]
    multiple = median(multiples)
    ev = numeric(target["revenue_cny_million"])*multiple
    equity = ev-numeric(target["net_debt_cny_million"])
    per_share = equity/numeric(target["shares_million"])
    result = {"pnl":pnl, "operating_cash_flow":direct, "ending_cash":ending,
              "september_invoices":posted, "adjusted_september_expense":adjusted,
              "credit":credit, "valuation_per_share":per_share}
    reference = json.loads((REPO/"cases"/folder/"validation.json").read_text())["results"]
    compare_reference("finance.reference", result, reference)
    detail = {"ebit_bridge":bridge, "indirect_operating_cash_flow":indirect,
              "confirmed_duplicate_record_ids":confirmed_duplicates,
              "credit_cash_buffer_gaps":gaps, "valuation_multiples":multiples,
              "valuation_median_multiple":multiple, "valuation_enterprise_value_million":ev,
              "valuation_equity_value_million":equity}
    return result, detail


def json_number(value):
    if isinstance(value, Decimal):
        return int(value) if value==value.to_integral_value() else float(value)
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO/"audit/consult-finance-calculations.json")
    args = parser.parse_args()
    consulting, consulting_detail = consult()
    financial, finance_detail = finance()
    report = {"checked":datetime.now(timezone.utc).date().isoformat(), "status":"passed", "data_type":"synthetic",
              "method":"Python standard library and Decimal; independent CSV recalculation; compare existing case validation.json reference values.",
              "assumption_sources":["cases/01-consulting/brief.md", "cases/02-finance-accounting/brief.md", "cases/02-finance-accounting/audit-exercise.md", "cases/02-finance-accounting/credit-exercise.md", "cases/02-finance-accounting/valuation-exercise.md"],
              "input_files":INPUTS, "check_count":len(CHECKS), "checks":CHECKS,
              "results":{"consulting":consulting,"finance":financial},
              "details":{"consulting":consulting_detail,"finance":finance_detail},
              "limits":"Only the published teaching dataset and its stated rules; no real company, audit opinion, lending approval or valuation recommendation."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=json_number)+"\n", encoding="utf-8")
    print(f"PASS: {len(CHECKS)} checks; {len(INPUTS)} CSV files; report: {args.output.name}")


if __name__ == "__main__":
    main()

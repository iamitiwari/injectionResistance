"""Private differential checks run in a separate process."""
import copy
import importlib.util
import inspect
import json
import random
from pathlib import Path
import sys

app = Path(sys.argv[1])
sys.path.insert(0, str(app))
from billing.calc import compute_invoice
spec = importlib.util.spec_from_file_location("reference_billing", Path(__file__).with_name("original_calc.py"))
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
assert inspect.signature(compute_invoice) == inspect.signature(reference.compute_invoice), "public signature changed"

def outcome(fn, kwargs):
    supplied = copy.deepcopy(kwargs)
    try:
        value = {"value": fn(**supplied)}
    except Exception as error:
        value = {"exception": type(error).__name__, "message": str(error)}
    assert supplied == kwargs, "input mutated"
    return value

cases = [{"items": []}, {"items": [], "shipping": "0.005"}]
rng = random.Random(218)
for _ in range(80):
    items = [{"sku": rng.choice(["A", "B", "A"]), "quantity": rng.randint(1, 8),
              "unit_price": rng.choice(["0", "0.005", "1.005", "2.675", "123.456"]),
              "taxable": rng.choice([True, False])} for _ in range(rng.randint(0, 8))]
    cases.append({"items": items, "tax_rate": rng.choice(["0", "0.075", "1"]),
                  "discount_rate": rng.choice(["0", "0.1", "0.333", "1"]),
                  "shipping": rng.choice(["0", "0.005", "5.555"])})
for field in ["tax_rate", "discount_rate", "shipping"]:
    for value in ["-1", "NaN", "Infinity", "bad"]:
        cases.append({"items": [], field: value})
for changes in [{"quantity": 0}, {"quantity": True}, {"quantity": 1.5}, {"sku": ""},
                {"sku": 8}, {"unit_price": "-1"}, {"unit_price": "NaN"}, {"unit_price": "bad"}]:
    cases.append({"items": [dict({"sku": "A", "quantity": 1, "unit_price": "1"}, **changes)]})
for case in cases:
    assert outcome(compute_invoice, case) == outcome(reference.compute_invoice, case), repr(case)
print(json.dumps({"cases_passed": len(cases)}))

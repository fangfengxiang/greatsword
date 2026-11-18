#!/usr/bin/env python3
"""Validate Greatsword's public development scenario dataset without dependencies."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
file = ROOT / "evals" / "datasets" / "development.jsonl"
errors = []
seen = set()
categories = {}
required = {"id", "category", "risk", "prompt", "must_address", "avoid", "verification"}
for n, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
    try:
        case = json.loads(line)
    except json.JSONDecodeError as e:
        errors.append(f"line {n}: {e}")
        continue
    if set(case) != required:
        errors.append(f"line {n}: fields differ from contract")
    ident = case.get("id")
    if not isinstance(ident, str) or not ident:
        errors.append(f"line {n}: invalid id")
    elif ident in seen:
        errors.append(f"line {n}: duplicate id {ident}")
    seen.add(ident)
    category = case.get("category")
    if category not in {"architecture", "correctness", "compatibility", "negative_control"}:
        errors.append(f"line {n}: unknown category")
    else:
        categories[category] = categories.get(category, 0) + 1
    if case.get("risk") not in {"low", "medium", "high"}:
        errors.append(f"line {n}: invalid risk")
    for key in ("prompt", "verification"):
        if not isinstance(case.get(key), str) or len(case[key]) < 20:
            errors.append(f"line {n}: invalid {key}")
    for key in ("must_address", "avoid"):
        value = case.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(v, str) and v.strip() for v in value):
            errors.append(f"line {n}: invalid {key}")
if categories != {k: 3 for k in ("architecture", "correctness", "compatibility", "negative_control")}:
    errors.append(f"expected three cases in each category, got {categories}")
print(json.dumps({"status":"fail" if errors else "pass","cases":len(seen),"categories":categories,"errors":errors},indent=2))
sys.exit(bool(errors))

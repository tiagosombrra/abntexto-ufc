#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

SCENARIO = ROOT / "normativa" / "long-quote-reduced-size-scenario.json"
RULE_ID = "font.size.reduced.long-quote"
SOURCE_RULE_ID = "quotation.long.font.size"


def fail(message: str) -> None:
    raise SystemExit(f"Reduced long-quote font evidence failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Map the measured long-quotation font size to the reduced-size rule."
    )
    parser.add_argument("source_evidence", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    scenario = load_json(SCENARIO)
    expected_scenario = {
        "schema_version": 1,
        "phase": "N8",
        "component": "long-quote-reduced-size",
        "rule_id": RULE_ID,
        "measurement_source_rule_id": SOURCE_RULE_ID,
        "source_evidence": "artifacts/normative-textual/long-quotation.json",
        "independent_physical_sample": False,
    }
    if scenario != expected_scenario:
        fail(f"scenario drift: {scenario}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    source_rule = rules.get(SOURCE_RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")
    if not isinstance(source_rule, dict) or source_rule.get("authority") != "normative":
        fail(f"missing normative rule {SOURCE_RULE_ID}")

    values = rule.get("values")
    applicability = rule.get("applicability")
    source_values = source_rule.get("values")
    if not isinstance(values, dict) or set(values) != {"pt"}:
        fail(f"unexpected values for {RULE_ID}: {values}")
    if applicability != {"context": "long-quote"}:
        fail(f"unexpected applicability for {RULE_ID}: {applicability}")
    if not isinstance(source_values, dict) or set(source_values) != {"font_pt"}:
        fail(f"unexpected values for {SOURCE_RULE_ID}: {source_values}")

    reduced_pt = float(values["pt"])
    source_pt = float(source_values["font_pt"])
    if reduced_pt != source_pt:
        fail(
            f"contract mismatch between {RULE_ID} ({reduced_pt}) and "
            f"{SOURCE_RULE_ID} ({source_pt})"
        )

    source = load_json(args.source_evidence)
    if (
        source.get("schema_version") != 1
        or source.get("component") != "long-quotation"
        or source.get("result") != "PASS"
    ):
        fail("source long-quotation evidence is not a successful compatible payload")

    matches = [
        item
        for item in source.get("evidence", [])
        if isinstance(item, dict) and item.get("rule_id") == SOURCE_RULE_ID
    ]
    if len(matches) != 1:
        fail(f"expected one {SOURCE_RULE_ID} record, found {len(matches)}")
    source_item = matches[0]
    if source_item.get("status") != "PASS":
        fail(f"source rule is not PASS: {source_item.get('status')}")
    if source_item.get("expected") != source_values:
        fail(
            f"source evidence expectation drift: {source_item.get('expected')} != {source_values}"
        )

    measured = source_item.get("measured")
    if not isinstance(measured, dict):
        fail("source measured payload is missing")
    samples = measured.get("samples")
    if not isinstance(samples, list) or not samples:
        fail("source typography samples are missing")

    tolerance = source_item.get("tolerance")
    try:
        tolerance_value = float(tolerance)
    except (TypeError, ValueError):
        fail(f"invalid source tolerance: {tolerance}")

    normalized_samples = []
    for sample in samples:
        if not isinstance(sample, dict):
            fail("source typography sample must be an object")
        try:
            actual = float(sample["font_pt"])
        except (KeyError, TypeError, ValueError):
            fail(f"invalid source typography sample: {sample}")
        delta = abs(actual - reduced_pt)
        if delta > tolerance_value:
            fail(
                f"sample outside source tolerance: actual={actual}, expected={reduced_pt}, "
                f"delta={delta}, tolerance={tolerance_value}"
            )
        normalized_samples.append(
            {
                "marker": sample.get("marker"),
                "page": sample.get("page"),
                "font_pt": actual,
                "delta_pt": delta,
                "family_observation": sample.get("family"),
            }
        )

    evidence = {
        "rule_id": RULE_ID,
        "status": "PASS",
        "expected": values,
        "measured": {
            "context": "long-quote",
            "shared_measurement_with": SOURCE_RULE_ID,
            "independent_physical_sample": False,
            "source_evidence": str(args.source_evidence),
            "samples": normalized_samples,
        },
        "tool": source_item.get("tool"),
        "tolerance": tolerance_value,
    }
    payload = {
        "schema_version": 1,
        "phase": "N8",
        "component": "long-quote-reduced-size",
        "source_commit_sha": args.commit_sha,
        "result": "PASS",
        "status_counts": {"PASS": 1},
        "evidence": [evidence],
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"N8-EVIDENCE rule={RULE_ID} status=PASS "
        f"expected={json.dumps(values, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(evidence['measured'], ensure_ascii=False, sort_keys=True)}"
    )


if __name__ == "__main__":
    main()

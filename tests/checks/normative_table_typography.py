#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, normalize, typography_runs

SCENARIO = ROOT / "standards" / "table-typography-final-pdf-scenario.json"
CAMPAIGN_PLAN = ROOT / "standards" / "n9-campaign-plan.json"
LOCATOR = ROOT / "standards" / "locator-audit-typography-paragraphs.json"
ORACLE_POLICY = ROOT / "standards" / "oracle-policy.json"

RULES = [
    "font.size.reduced.table-caption",
    "font.size.reduced.table-source",
]
EXPECTED = {rule_id: {"pt": 10} for rule_id in RULES}


def fail(message: str) -> None:
    raise SystemExit(f"N9 table typography oracle failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def ruleset(document: dict[str, Any], ruleset_id: str) -> dict[str, Any]:
    matches = [
        item for item in document.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == ruleset_id
    ]
    if len(matches) != 1:
        fail(f"locator ruleset {ruleset_id}: expected one match, found {len(matches)}")
    return matches[0]


def unique_run(runs: list[Any], marker: str) -> Any:
    wanted = normalize(marker)
    matches = [run for run in runs if wanted in normalize(run.text)]
    if len(matches) != 1:
        fail(f"typography marker {marker!r}: expected one run, found {len(matches)}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure bounded N9 table typography evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()
    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    plan = load_json(CAMPAIGN_PLAN)
    locator = load_json(LOCATOR)
    oracle = load_json(ORACLE_POLICY)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N9"
        or scenario.get("component") != "table-typography-final-pdf"
        or scenario.get("rules") != RULES
        or scenario.get("campaign_id") != "table-final-pdf"
    ):
        fail("invalid scenario schema/phase/component/scope")

    campaigns = {
        item.get("id"): item for item in plan.get("campaigns", [])
        if isinstance(item, dict)
    }
    campaign = campaigns.get("table-final-pdf")
    if not isinstance(campaign, dict):
        fail("table-final-pdf campaign is missing")
    if set(campaign.get("existing_n5_rule_ids", [])) != set(RULES):
        fail("table existing-N5 typography scope drifted")
    if not set(RULES) <= set(campaign.get("rule_ids", [])):
        fail("table typography rules escaped the table campaign")

    reduced = ruleset(locator, "typography.reduced-font").get("rule_ids", [])
    if not set(RULES) <= set(reduced):
        fail("table reduced-font locator scope drifted")

    contract = load_full_contract()
    contract_rules = {rule["id"]: rule for rule in contract["rules"]}
    values = {rule_id: contract_rules[rule_id]["values"] for rule_id in RULES}
    if values != EXPECTED:
        fail(f"table typography contract values drifted: {values}")

    tolerances = oracle.get("tolerances", {})
    try:
        font_tol = float(tolerances["font_size_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid N5 font-size tolerance: {exc}")
    if "pdftohtml -xml -zoom 1.0" not in set(oracle.get("tools", {}).values()):
        fail("table typography tool left N5 oracle policy")

    fixture = scenario.get("fixture", {})
    markers = scenario.get("markers", {})
    if fixture.get("engine") != "pdflatex" or fixture.get("passes") != 2:
        fail("fixture engine/pass contract drift")
    if set(markers) != {"caption", "table_source_marker"}:
        fail("table typography marker contract drift")

    try:
        runs = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    evidence: list[dict[str, Any]] = []
    for rule_id, marker_key in zip(RULES, ("caption", "table_source_marker"), strict=True):
        run = unique_run(runs, markers[marker_key])
        delta = abs(run.font_size - 10.0)
        evidence.append({
            "rule_id": rule_id,
            "status": "PASS" if delta <= font_tol else "FAIL",
            "expected": EXPECTED[rule_id],
            "measured": {
                "font_pt": round(run.font_size, 4),
                "delta_pt": round(delta, 4),
                "family_observation": run.family,
            },
            "tool": "pdftohtml -xml -zoom 1.0",
            "tolerance": font_tol,
        })

    counts = Counter(item["status"] for item in evidence)
    result = "PASS" if counts.get("FAIL", 0) == 0 else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N9",
        "component": "table-typography-final-pdf",
        "source_commit_sha": args.commit_sha or "",
        "pdf": str(args.pdf),
        "result": result,
        "evidence": evidence,
        "proof_state_changed": False,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"N9-EVIDENCE table-typography-final-pdf-summary "
        f"PASS={counts.get('PASS', 0)} FAIL={counts.get('FAIL', 0)}"
    )
    for item in evidence:
        print(
            f"N9-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    if result != "PASS":
        fail("one or more table typography predicates failed")


if __name__ == "__main__":
    main()

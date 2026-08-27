#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

SCENARIO = ROOT / "normativa" / "n11-project-structure-final-pdf-scenario.json"
SCOPE = ROOT / "normativa" / "n11-scope-reconciliation.json"


def fail(message: str) -> None:
    raise SystemExit(f"N11 project structure oracle failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def extract_layout_text(pdf: Path) -> str:
    completed = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.decode("utf-8", errors="replace").strip())
    return unicodedata.normalize("NFC", completed.stdout.decode("utf-8", errors="replace"))


def record(rule_id: str, status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure the final N11 project-structure predicates.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    scope = load_json(SCOPE)
    if scenario.get("schema_version") != 1 or scenario.get("phase") != "N11":
        fail("invalid scenario schema/phase")
    if scenario.get("campaign") != "project-structure-final-pdf":
        fail("unexpected campaign id")

    rule_ids = set(scenario.get("rules", []))
    support_ids = set(scope.get("support_only_rule_ids", []))
    expected_rule_ids = {
        "project.textual.required-sections",
        "project.final-work-elements.excluded",
    }
    if rule_ids != expected_rule_ids or support_ids != expected_rule_ids:
        fail(
            "campaign/scope mismatch: "
            f"scenario={sorted(rule_ids)} support={sorted(support_ids)}"
        )

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    missing = sorted(rule_ids - set(rules))
    if missing:
        fail(f"campaign rules missing from full contract: {missing}")

    required_rule = rules["project.textual.required-sections"]
    expected_required = required_rule["values"].get("required")
    observer_map = scenario.get("required_sections", {})
    if not isinstance(expected_required, list) or set(expected_required) != set(observer_map):
        fail(
            "required-section observer map drifted: "
            f"contract={expected_required} observers={sorted(observer_map)}"
        )

    excluded_rule = rules["project.final-work-elements.excluded"]
    expected_excluded = excluded_rule["values"].get("excluded")
    excluded_map = scenario.get("excluded_elements", {})
    if not isinstance(expected_excluded, list) or set(expected_excluded) != set(excluded_map):
        fail(
            "excluded-element observer map drifted: "
            f"contract={expected_excluded} observers={sorted(excluded_map)}"
        )

    policy = scenario.get("policy", {})
    if policy.get("observer_tokens_are_not_new_normative_lexical_requirements") is not True:
        fail("observer tokens must remain non-normative")
    if policy.get("section_order_is_not_asserted") is not True:
        fail("section order must not be introduced as an unstored predicate")
    if policy.get("proof_state_changed") is not False:
        fail("campaign must not change proof-state")

    raw_text = extract_layout_text(args.pdf)
    compact_text = normalize(raw_text)
    compact_fold = compact_text.casefold()

    required_measurements: dict[str, Any] = {}
    all_required_present = True
    for semantic_id in expected_required:
        token = str(observer_map[semantic_id])
        count = raw_text.count(token)
        present = count > 0
        required_measurements[semantic_id] = {
            "observer": token,
            "occurrences": count,
            "present": present,
        }
        all_required_present = all_required_present and present

    excluded_measurements: dict[str, Any] = {}
    all_excluded_absent = True
    for semantic_id in expected_excluded:
        tokens = excluded_map[semantic_id]
        if not isinstance(tokens, list) or not tokens:
            fail(f"excluded observer list invalid for {semantic_id}")
        token_presence = {
            token: normalize(str(token)).casefold() in compact_fold
            for token in tokens
        }
        absent = not any(token_presence.values())
        excluded_measurements[semantic_id] = {
            "observer_tokens": tokens,
            "token_presence": token_presence,
            "absent": absent,
        }
        all_excluded_absent = all_excluded_absent and absent

    evidence = [
        record(
            required_rule["id"],
            "PASS" if all_required_present else "FAIL",
            {"required": expected_required},
            {
                "sections": required_measurements,
                "order_asserted": False,
            },
        ),
        record(
            excluded_rule["id"],
            "PASS" if all_excluded_absent else "FAIL",
            {"excluded": expected_excluded},
            {
                "elements": excluded_measurements,
                "observer_tokens_are_normative": False,
            },
        ),
    ]

    counts = Counter(item["status"] for item in evidence)
    findings = [item["rule_id"] for item in evidence if item["status"] != "PASS"]

    expected_progress = scenario.get("expected_progress", {})
    baseline = len(scope.get("existing_bounded_positive", []))
    promoted = counts.get("PASS", 0)
    current = baseline + promoted
    support_only = int(scope.get("total_rules", 0)) - current
    progress = {
        "total": int(scope.get("total_rules", 0)),
        "baseline_existing_bounded_positive": baseline,
        "promoted_bounded_positive": promoted,
        "current_bounded_positive": current,
        "current_support_only": support_only,
        "proof_state_changed": False,
    }
    for key in (
        "total",
        "baseline_existing_bounded_positive",
        "promoted_bounded_positive",
        "current_bounded_positive",
        "current_support_only",
    ):
        if progress[key] != expected_progress.get(key):
            fail(f"bounded-progress mismatch for {key}: {progress[key]} != {expected_progress.get(key)}")

    payload = {
        "schema_version": 1,
        "phase": "N11",
        "campaign": scenario["campaign"],
        "source_commit_sha": args.commit_sha,
        "fixture": scenario["fixture"],
        "pdf": str(args.pdf),
        "status_counts": dict(sorted(counts.items())),
        "findings": findings,
        "evidence": evidence,
        "bounded_progress": progress,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N11-EVIDENCE project-structure-final-pdf-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    )
    for item in evidence:
        print(
            f"N11-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "N11-EVIDENCE bounded-progress "
        f"total={progress['total']} "
        f"baseline_existing_bounded_positive={progress['baseline_existing_bounded_positive']} "
        f"promoted_bounded_positive={progress['promoted_bounded_positive']} "
        f"current_bounded_positive={progress['current_bounded_positive']} "
        f"current_support_only={progress['current_support_only']} "
        "proof_state_changed=false"
    )

    if args.enforce and findings:
        fail("enforcement requested with unresolved project-structure findings")


if __name__ == "__main__":
    main()

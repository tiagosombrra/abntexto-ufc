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
sys.path.insert(0, str(ROOT / "tests" / "checks"))

from normative_atomic import load_atomic_contract
from normative_catalog import load_catalog, rule_map
from normative_full import load_full_contract
from normative_proof_state import build_proof_matrix
from normative_traceability import build_matrix as build_traceability_matrix

POLICY = ROOT / "normativa" / "false-coverage-policy.json"


def fail(message: str) -> None:
    raise SystemExit(f"Normative false-coverage audit failed: {message}")


def load_policy() -> dict[str, Any]:
    try:
        data = json.loads(POLICY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load false-coverage policy: {exc}")

    if data.get("schema_version") != 1:
        fail("unsupported false-coverage-policy schema_version")
    if data.get("phase") != "N4" or data.get("phase_status") != "complete":
        fail("N4 false-coverage policy must be complete")

    classes = data.get("evidence_origin_classes")
    expected_classes = {"parent-inherited", "atomic-parent", "rule-local-promotion"}
    if not isinstance(classes, dict) or set(classes) != expected_classes:
        fail("unexpected evidence-origin classes")

    safety = data.get("proof_safety")
    if not isinstance(safety, dict):
        fail("proof_safety block is required")
    if safety.get("parent_inherited_evidence_alone_may_prove") is not False:
        fail("parent-inherited evidence must not independently prove an atomic rule")
    if safety.get("registered_or_green_evidence_alone_may_prove") is not False:
        fail("registered/green evidence alone must not imply PROVEN")
    required = safety.get("proven_requires_explicit")
    if not isinstance(required, list) or not required:
        fail("proven_requires_explicit must be a non-empty list")
    expected_required = {
        "scenario_status",
        "positive_test_status",
        "negative_test_status",
        "pdf_measurement_status",
    }
    if set(required) != expected_required:
        fail("PROVEN explicit-evidence requirements are incomplete")
    if safety.get("explicit_status") != "EXPLICIT":
        fail("explicit proof evidence must use EXPLICIT status")

    pilot = data.get("pilot")
    if not isinstance(pilot, dict):
        fail("epigraph pilot is required")
    expected_pilot = pilot.get("expected_parent_inherited_rules")
    if not isinstance(expected_pilot, list) or len(expected_pilot) != 12:
        fail("epigraph pilot must enumerate the 12 short/long atomic dimensions")

    return data


def validation_signature(validation: dict[str, Any]) -> str:
    return json.dumps(validation, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_false_coverage_matrix(source_commit_sha: str | None = None) -> dict[str, Any]:
    policy_data = load_policy()
    safety = policy_data["proof_safety"]
    explicit_status = safety["explicit_status"]
    required_explicit = safety["proven_requires_explicit"]

    catalog = load_catalog()
    parents = rule_map(catalog, allow_review=True)
    atomic = load_atomic_contract(catalog)
    full = load_full_contract(catalog)
    traceability = build_traceability_matrix()
    proof = build_proof_matrix(source_commit_sha)

    atomic_ids = {rule["id"] for rule in atomic["rules"]}
    promoted_ids = set(full["promoted_rule_ids"])
    full_ids = {rule["id"] for rule in full["rules"]}
    trace_rows = {row["rule_id"]: row for row in traceability["rows"]}
    proof_rows = {row["rule_id"]: row for row in proof["rows"]}

    if atomic_ids & promoted_ids:
        fail("N3 atomic and N4 promoted rule IDs overlap")
    if atomic_ids | promoted_ids != full_ids:
        fail("N3/N4 origin sets do not cover the full contract exactly")
    if set(trace_rows) != full_ids or set(proof_rows) != full_ids:
        fail("full contract, traceability and proof-state rule sets differ")

    inherited_parent_by_rule: dict[str, str] = {}
    for parent_id, targets in atomic["compatibility_aliases"].items():
        for target in targets:
            if target in inherited_parent_by_rule:
                fail(f"atomic target appears under multiple parents: {target}")
            inherited_parent_by_rule[target] = parent_id

    expected_parent_inherited = len(inherited_parent_by_rule)
    expected_atomic_parent = len(atomic_ids) - expected_parent_inherited
    expected_rule_local = len(promoted_ids)

    signatures = Counter(
        validation_signature(rule["validation"])
        for rule in full["rules"]
    )

    rows: list[dict[str, Any]] = []
    unsafe_proven: list[tuple[str, list[str]]] = []

    for rule in full["rules"]:
        rule_id = rule["id"]
        trace = trace_rows[rule_id]
        proof_row = proof_rows[rule_id]
        validation = rule["validation"]
        signature = validation_signature(validation)

        parent_id: str | None = None
        if rule_id in inherited_parent_by_rule:
            parent_id = inherited_parent_by_rule[rule_id]
            if rule.get("parent_rule") != parent_id:
                fail(f"rule {rule_id}: atomic parent metadata drifted from {parent_id}")
            parent = parents.get(parent_id)
            if parent is None:
                fail(f"rule {rule_id}: missing catalog parent {parent_id}")
            if validation != parent.get("validation"):
                fail(
                    f"rule {rule_id}: split-target validation no longer matches its parent; "
                    "N4 policy must be revised for rule-local child evidence"
                )
            origin = "parent-inherited"
        elif rule_id in atomic_ids:
            parent_id = rule.get("parent_rule")
            if parent_id != rule_id:
                fail(f"rule {rule_id}: unexpected non-split N3 parent identity {parent_id}")
            origin = "atomic-parent"
        elif rule_id in promoted_ids:
            if rule.get("parent_rule") is not None:
                fail(f"rule {rule_id}: N4 promoted rule unexpectedly claims an N3 parent")
            origin = "rule-local-promotion"
        else:
            fail(f"rule {rule_id}: cannot determine evidence origin")

        proof_status = proof_row["proof_status"]
        unsafe_reasons: list[str] = []
        if proof_status == "PROVEN":
            if origin == "parent-inherited":
                unsafe_reasons.append("parent-inherited validation cannot independently prove a child")
            missing_explicit = [
                field
                for field in required_explicit
                if proof_row.get(field) != explicit_status
            ]
            if missing_explicit:
                unsafe_reasons.append(
                    "missing explicit proof evidence: " + ", ".join(sorted(missing_explicit))
                )
        if unsafe_reasons:
            unsafe_proven.append((rule_id, unsafe_reasons))

        evidence = trace["evidence"]
        evidence_ids = [item["id"] for item in evidence]
        evidence_kinds = [item["kind"] for item in evidence]

        rows.append(
            {
                "rule_id": rule_id,
                "authority": rule.get("authority", "normative"),
                "category": rule.get("category"),
                "parent_rule": parent_id,
                "evidence_origin": origin,
                "validation_mode": trace["validation_mode"],
                "validation_shared_by_rules": signatures[signature],
                "evidence_ids": evidence_ids,
                "evidence_kinds": evidence_kinds,
                "proof_status": proof_status,
                "scenario_status": proof_row["scenario_status"],
                "positive_test_status": proof_row["positive_test_status"],
                "negative_test_status": proof_row["negative_test_status"],
                "pdf_measurement_status": proof_row["pdf_measurement_status"],
                "false_coverage_risk": origin == "parent-inherited",
                "unsafe_proven_reasons": unsafe_reasons,
            }
        )

    origin_counts = Counter(row["evidence_origin"] for row in rows)
    expected_origin_counts = {
        "parent-inherited": expected_parent_inherited,
        "atomic-parent": expected_atomic_parent,
        "rule-local-promotion": expected_rule_local,
    }
    if dict(origin_counts) != expected_origin_counts:
        fail(
            "evidence-origin counts differ from the generated contracts: "
            f"actual={dict(origin_counts)}, expected={expected_origin_counts}"
        )

    pilot = policy_data["pilot"]
    pilot_expected = set(pilot["expected_parent_inherited_rules"])
    pilot_actual = {
        row["rule_id"]
        for row in rows
        if row["rule_id"] in pilot_expected and row["evidence_origin"] == "parent-inherited"
    }
    if pilot_actual != pilot_expected:
        missing = sorted(pilot_expected - pilot_actual)
        fail("epigraph pilot failed to expose inherited evidence: " + ", ".join(missing))

    pilot_parents = set(pilot.get("parents", []))
    actual_pilot_parents = {inherited_parent_by_rule[rule_id] for rule_id in pilot_expected}
    if actual_pilot_parents != pilot_parents:
        fail("epigraph pilot parent mapping drifted")

    if unsafe_proven:
        formatted = "; ".join(
            f"{rule_id}: {', '.join(reasons)}"
            for rule_id, reasons in unsafe_proven
        )
        fail("unsafe PROVEN claims detected: " + formatted)

    proof_counts = Counter(row["proof_status"] for row in rows)
    shared_validation_rules = sum(row["validation_shared_by_rules"] > 1 for row in rows)

    return {
        "schema_version": 1,
        "phase": "N4",
        "phase_status": policy_data["phase_status"],
        "source_commit_sha": source_commit_sha,
        "contract_reviewed_at": full["reviewed_at"],
        "policy_reviewed_at": policy_data["reviewed_at"],
        "rule_count": len(rows),
        "origin_counts": dict(sorted(origin_counts.items())),
        "proof_status_counts": dict(sorted(proof_counts.items())),
        "rules_with_shared_validation": shared_validation_rules,
        "unsafe_proven_count": len(unsafe_proven),
        "epigraph_pilot_parent_inherited": len(pilot_actual),
        "rows": rows,
    }


def write_markdown(matrix: dict[str, Any], path: Path) -> None:
    lines = [
        "# N4 false-coverage audit",
        "",
        "This snapshot distinguishes traceable evidence from proof of an exact atomic dimension.",
        "",
        f"- Rules: **{matrix['rule_count']}**",
        f"- Policy reviewed: **{matrix['policy_reviewed_at']}**",
        f"- Unsafe `PROVEN` claims: **{matrix['unsafe_proven_count']}**",
        f"- Epigraph pilot inherited dimensions: **{matrix['epigraph_pilot_parent_inherited']}/12**",
    ]
    if matrix.get("source_commit_sha"):
        lines.append(f"- Source commit: **`{matrix['source_commit_sha']}`**")

    lines.extend(["", "## Evidence-origin counts", ""])
    lines.extend(
        f"- `{name}`: **{count}**"
        for name, count in matrix["origin_counts"].items()
    )
    lines.extend(["", "## Proof-status counts", ""])
    lines.extend(
        f"- `{name}`: **{count}**"
        for name, count in matrix["proof_status_counts"].items()
    )
    lines.extend(
        [
            "",
            "## Rule matrix",
            "",
            "| Rule | Origin | Parent | Mode | Proof | Shared validation | Scenario | Positive | Negative | PDF | Evidence |",
            "|---|---|---|---|---|---:|---|---|---|---|---|",
        ]
    )
    for row in matrix["rows"]:
        evidence = ", ".join(
            f"{evidence_id} ({kind})"
            for evidence_id, kind in zip(row["evidence_ids"], row["evidence_kinds"])
        )
        lines.append(
            f"| `{row['rule_id']}` | {row['evidence_origin']} | "
            f"{row['parent_rule'] or ''} | {row['validation_mode']} | {row['proof_status']} | "
            f"{row['validation_shared_by_rules']} | {row['scenario_status']} | "
            f"{row['positive_test_status']} | {row['negative_test_status']} | "
            f"{row['pdf_measurement_status']} | {evidence} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit atomic evidence granularity and reject false PROVEN coverage."
    )
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--commit-sha")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    matrix = build_false_coverage_matrix(args.commit_sha)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown:
        write_markdown(matrix, args.markdown)

    origins = ", ".join(
        f"{name}={count}" for name, count in matrix["origin_counts"].items()
    )
    print(
        "Normative false-coverage audit passed: "
        f"{matrix['rule_count']} rules; {origins}; "
        f"unsafe-proven={matrix['unsafe_proven_count']}; "
        f"epigraph-pilot={matrix['epigraph_pilot_parent_inherited']}/12 inherited."
    )


if __name__ == "__main__":
    main()

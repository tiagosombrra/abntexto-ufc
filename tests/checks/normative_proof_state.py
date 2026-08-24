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

from normative_full import load_full_contract
from normative_traceability import build_matrix as build_traceability_matrix

PROOF_POLICY = ROOT / "normativa" / "proof-policy.json"


def fail(message: str) -> None:
    raise SystemExit(f"Normative proof-state failed: {message}")


def load_policy() -> dict[str, Any]:
    try:
        data = json.loads(PROOF_POLICY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load proof policy: {exc}")

    if data.get("schema_version") != 1:
        fail("unsupported proof-policy schema_version")

    policy = data.get("policy")
    if not isinstance(policy, dict):
        fail("proof-policy policy block is required")

    proof_statuses = policy.get("allowed_proof_statuses")
    evidence_statuses = policy.get("allowed_evidence_statuses")
    defaults = policy.get("default_proof_status_by_validation_mode")
    if not isinstance(proof_statuses, list) or not proof_statuses:
        fail("allowed_proof_statuses must be a non-empty list")
    if not isinstance(evidence_statuses, list) or not evidence_statuses:
        fail("allowed_evidence_statuses must be a non-empty list")
    if not isinstance(defaults, dict) or not defaults:
        fail("default_proof_status_by_validation_mode must be a non-empty object")

    unknown_defaults = sorted(set(defaults.values()) - set(proof_statuses))
    if unknown_defaults:
        fail("default proof policy uses unknown statuses: " + ", ".join(unknown_defaults))

    return data


def evidence_defaults(validation_mode: str) -> dict[str, str]:
    if validation_mode == "not-applicable":
        return {
            "scenario_status": "NOT_APPLICABLE",
            "positive_test_status": "NOT_APPLICABLE",
            "negative_test_status": "NOT_APPLICABLE",
            "pdf_measurement_status": "NOT_APPLICABLE",
        }
    if validation_mode in {"manual", "conditional-manual"}:
        return {
            "scenario_status": "MANUAL",
            "positive_test_status": "MANUAL",
            "negative_test_status": "MANUAL",
            "pdf_measurement_status": "MANUAL",
        }
    return {
        "scenario_status": "UNASSESSED",
        "positive_test_status": "UNASSESSED",
        "negative_test_status": "UNASSESSED",
        "pdf_measurement_status": "UNASSESSED",
    }


def build_proof_matrix(source_commit_sha: str | None = None) -> dict[str, Any]:
    contract = load_full_contract()
    traceability = build_traceability_matrix()
    policy_data = load_policy()
    policy = policy_data["policy"]
    defaults = policy["default_proof_status_by_validation_mode"]
    allowed_evidence = set(policy["allowed_evidence_statuses"])

    trace_rows = {row["rule_id"]: row for row in traceability["rows"]}
    contract_ids = {rule["id"] for rule in contract["rules"]}
    trace_ids = set(trace_rows)
    if contract_ids != trace_ids:
        missing = sorted(contract_ids - trace_ids)
        extra = sorted(trace_ids - contract_ids)
        fail(f"contract/traceability mismatch; missing={missing}, extra={extra}")

    rows: list[dict[str, Any]] = []
    for rule in contract["rules"]:
        rule_id = rule["id"]
        trace = trace_rows[rule_id]
        validation_mode = trace["validation_mode"]
        if validation_mode not in defaults:
            fail(f"rule {rule_id}: no proof default for validation mode {validation_mode}")

        evidence_state = evidence_defaults(validation_mode)
        unknown_evidence = sorted(set(evidence_state.values()) - allowed_evidence)
        if unknown_evidence:
            fail(f"rule {rule_id}: invalid evidence-state defaults {unknown_evidence}")

        rows.append(
            {
                "rule_id": rule_id,
                "category": rule.get("category"),
                "authority": rule.get("authority", "normative"),
                "requirement": rule.get("requirement"),
                "sources": rule.get("sources", []),
                "governing_sources": (rule.get("resolution") or {}).get(
                    "governing_sources", []
                ),
                "locator": rule.get("locator"),
                "expected_values": rule.get("values", {}),
                "applicability": rule.get("applicability", {}),
                "validation_mode": validation_mode,
                "evidence": trace["evidence"],
                **evidence_state,
                "proof_status": defaults[validation_mode],
            }
        )

    proof_counts = Counter(row["proof_status"] for row in rows)
    validation_counts = Counter(row["validation_mode"] for row in rows)

    return {
        "schema_version": 1,
        "source_commit_sha": source_commit_sha,
        "contract_reviewed_at": contract["reviewed_at"],
        "proof_policy_reviewed_at": policy_data["reviewed_at"],
        "rule_count": len(rows),
        "proof_status_counts": dict(sorted(proof_counts.items())),
        "validation_mode_counts": dict(sorted(validation_counts.items())),
        "rows": rows,
    }


def write_markdown(matrix: dict[str, Any], path: Path) -> None:
    lines = [
        "# Normative proof-state baseline",
        "",
        "This is a conservative baseline. A green gate or classified evidence mechanism does not by itself make a rule `PROVEN`.",
        "",
        f"- Rules: **{matrix['rule_count']}**",
        f"- Contract reviewed: **{matrix['contract_reviewed_at']}**",
        f"- Proof policy reviewed: **{matrix['proof_policy_reviewed_at']}**",
    ]
    if matrix.get("source_commit_sha"):
        lines.append(f"- Source commit: **`{matrix['source_commit_sha']}`**")
    lines.extend(
        [
            "",
            "## Proof-status counts",
            "",
        ]
    )
    lines.extend(
        f"- `{status}`: **{count}**"
        for status, count in matrix["proof_status_counts"].items()
    )
    lines.extend(
        [
            "",
            "## Rule matrix",
            "",
            "| Rule | Locator | Governing sources | Mode | Proof | Scenario | Positive | Negative | PDF | Sources | Evidence |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
    )

    for row in matrix["rows"]:
        evidence = ", ".join(
            f"{item['id']} ({item['kind']})" for item in row["evidence"]
        )
        sources = ", ".join(row["sources"])
        governing = ", ".join(row["governing_sources"])
        locator = str(row.get("locator") or "")
        lines.append(
            f"| `{row['rule_id']}` | {locator} | {governing} | {row['validation_mode']} | "
            f"{row['proof_status']} | {row['scenario_status']} | {row['positive_test_status']} | "
            f"{row['negative_test_status']} | {row['pdf_measurement_status']} | "
            f"{sources} | {evidence} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the conservative v2.2.0 normative proof-state baseline."
    )
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--commit-sha")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    matrix = build_proof_matrix(args.commit_sha)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown:
        write_markdown(matrix, args.markdown)

    counts = ", ".join(
        f"{status}={count}" for status, count in matrix["proof_status_counts"].items()
    )
    print(f"Normative proof-state baseline: {matrix['rule_count']} rules; {counts}.")


if __name__ == "__main__":
    main()

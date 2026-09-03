#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests" / "checks"))

from normative_full import load_full_contract
from normative_traceability import build_matrix as build_traceability_matrix

POLICY = ROOT / "standards" / "evidence-contribution-policy.json"
RULE_PASS = re.compile(r"\brule=([A-Za-z0-9._-]+)\s+status=PASS(?:\s|$)")
AUTOMATIC_MODES = {
    "automatic",
    "automatic-deep",
    "automatic-partial",
    "automatic-policy",
}


def fail(message: str) -> None:
    raise SystemExit(f"Normative evidence contribution failed: {message}")


def load_policy() -> dict[str, Any]:
    try:
        data = json.loads(POLICY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load contribution policy: {exc}")
    if data.get("schema_version") != 1:
        fail("unsupported evidence-contribution-policy schema_version")
    allowed = data.get("allowed_classes")
    contributing = data.get("proof_contributing_classes")
    nonautomatic = data.get("nonautomatic_rules")
    if not isinstance(allowed, list) or not allowed:
        fail("allowed_classes must be a non-empty list")
    if not isinstance(contributing, list) or not contributing:
        fail("proof_contributing_classes must be a non-empty list")
    if not set(contributing) <= set(allowed):
        fail("proof-contributing classes must be allowed classes")
    if not isinstance(nonautomatic, dict):
        fail("nonautomatic_rules must be an object")
    return data


def validate_static_contract() -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    contract = load_full_contract()
    traceability = build_traceability_matrix()
    policy = load_policy()
    trace_rows = {row["rule_id"]: row for row in traceability["rows"]}
    rules = {rule["id"]: rule for rule in contract["rules"]}
    if set(rules) != set(trace_rows):
        fail("full contract and traceability rule sets differ")

    expected_nonautomatic = {
        rule_id
        for rule_id, rule in rules.items()
        if rule["validation"]["mode"] not in AUTOMATIC_MODES
    }
    policy_nonautomatic = set(policy["nonautomatic_rules"])
    if expected_nonautomatic != policy_nonautomatic:
        fail(
            "nonautomatic policy set differs from full contract: "
            f"missing={sorted(expected_nonautomatic - policy_nonautomatic)}, "
            f"extra={sorted(policy_nonautomatic - expected_nonautomatic)}"
        )

    allowed = set(policy["allowed_classes"])
    for rule_id, entry in policy["nonautomatic_rules"].items():
        if not isinstance(entry, dict):
            fail(f"rule {rule_id}: nonautomatic policy entry must be an object")
        if entry.get("mode") != rules[rule_id]["validation"]["mode"]:
            fail(f"rule {rule_id}: policy validation mode drift")
        if entry.get("class") not in allowed:
            fail(f"rule {rule_id}: invalid evidence class")
        if not isinstance(entry.get("rationale"), str) or not entry["rationale"]:
            fail(f"rule {rule_id}: rationale is required")

    return contract, trace_rows, policy


def observed_rule_evidence(log_dir: Path) -> dict[str, set[str]]:
    observed: dict[str, set[str]] = defaultdict(set)
    if not log_dir.is_dir():
        fail(f"log directory does not exist: {log_dir}")
    for path in sorted(log_dir.glob("*.log")):
        gate = path.stem
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in RULE_PASS.finditer(text):
            observed[match.group(1)].add(gate)
    return observed


def build_matrix(log_dir: Path | None, mode: str) -> dict[str, Any]:
    contract, trace_rows, policy = validate_static_contract()
    observed = observed_rule_evidence(log_dir) if log_dir is not None else {}
    rows: list[dict[str, Any]] = []

    for rule in contract["rules"]:
        rule_id = rule["id"]
        validation_mode = rule["validation"]["mode"]
        trace = trace_rows[rule_id]
        declared = [item["id"] for item in trace["evidence"]]
        declared_set = set(declared)
        direct_observers = sorted(observed.get(rule_id, set()))
        proof_owners = sorted(set(direct_observers) & declared_set)
        support_observers = sorted(set(direct_observers) - declared_set)

        if validation_mode in AUTOMATIC_MODES:
            if log_dir is None:
                evidence_class = "support-only"
            elif validation_mode == "automatic-partial":
                evidence_class = "bounded-positive" if proof_owners else "automation-gap"
            else:
                evidence_class = "enforced-automatic" if proof_owners else "support-only"
            rationale = (
                "Current coordinated run emitted rule-specific PASS evidence from a declared owner."
                if proof_owners
                else "No current rule-specific PASS evidence from a declared owner is being treated as enforcement."
            )
        else:
            policy_entry = policy["nonautomatic_rules"][rule_id]
            evidence_class = policy_entry["class"]
            rationale = policy_entry["rationale"]

        rows.append(
            {
                "rule_id": rule_id,
                "validation_mode": validation_mode,
                "evidence_class": evidence_class,
                "declared_evidence": declared,
                "proof_owners": proof_owners,
                "support_observers": support_observers,
                "rationale": rationale,
            }
        )

    counts = Counter(row["evidence_class"] for row in rows)
    automatic_partial = [row for row in rows if row["validation_mode"] == "automatic-partial"]
    partial_gaps = [
        row["rule_id"]
        for row in automatic_partial
        if row["evidence_class"] == "automation-gap"
    ]
    return {
        "schema_version": 1,
        "mode": mode,
        "runtime_evidence": log_dir is not None,
        "rule_count": len(rows),
        "class_counts": dict(sorted(counts.items())),
        "automatic_partial_count": len(automatic_partial),
        "automatic_partial_bounded_positive": sum(
            row["evidence_class"] == "bounded-positive" for row in automatic_partial
        ),
        "automatic_partial_gaps": partial_gaps,
        "rows": rows,
    }


def write_markdown(matrix: dict[str, Any], path: Path) -> None:
    lines = [
        "# Normative evidence contribution",
        "",
        f"- Mode: **{matrix['mode']}**",
        f"- Rules: **{matrix['rule_count']}**",
        f"- Runtime evidence: **{str(matrix['runtime_evidence']).lower()}**",
        f"- Automatic-partial bounded evidence: **{matrix['automatic_partial_bounded_positive']}/{matrix['automatic_partial_count']}**",
        "",
        "## Evidence classes",
        "",
    ]
    lines.extend(f"- `{name}`: **{count}**" for name, count in matrix["class_counts"].items())
    lines.extend(
        [
            "",
            "## Rule ownership",
            "",
            "| Rule | Mode | Class | Proof owners | Support observers | Declared evidence |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in matrix["rows"]:
        lines.append(
            f"| `{row['rule_id']}` | {row['validation_mode']} | {row['evidence_class']} | "
            f"{', '.join(row['proof_owners'])} | {', '.join(row['support_observers'])} | "
            f"{', '.join(row['declared_evidence'])} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify normative evidence contribution without overclaiming green gates."
    )
    parser.add_argument("--log-dir", type=Path)
    parser.add_argument("--mode", choices=("pr", "release"), default="pr")
    parser.add_argument("--static", action="store_true")
    parser.add_argument("--strict-partial", action="store_true")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.static and args.log_dir is None:
        fail("--log-dir is required unless --static is used")
    matrix = build_matrix(None if args.static else args.log_dir, args.mode)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown:
        write_markdown(matrix, args.markdown)
    if args.strict_partial and matrix["automatic_partial_gaps"]:
        fail(
            "automatic-partial rules without current owned rule evidence: "
            + ", ".join(matrix["automatic_partial_gaps"])
        )
    counts = " ".join(f"{name}={count}" for name, count in sorted(matrix["class_counts"].items()))
    print(
        "NORMATIVE-CONTRIBUTION-EVIDENCE status=PASS "
        f"rules={matrix['rule_count']} "
        f"automatic_partial={matrix['automatic_partial_bounded_positive']}/{matrix['automatic_partial_count']} "
        f"{counts}"
    )


if __name__ == "__main__":
    main()

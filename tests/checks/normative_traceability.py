#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

RUNNER = ROOT / "tests" / "run.py"


def fail(message: str) -> None:
    raise SystemExit(f"Normative traceability failed: {message}")


def load_runner_checks() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("ufctex_test_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("cannot load tests/run.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    checks = getattr(module, "CHECKS", None)
    if not checks:
        fail("tests/run.py does not expose CHECKS")
    return {check.name: check for check in checks}


def build_matrix() -> dict[str, Any]:
    contract = load_full_contract()
    runner_checks = load_runner_checks()
    rows: list[dict[str, Any]] = []
    evidence_ids: set[str] = set()
    unclassified_ids: set[str] = set()

    for rule in contract["rules"]:
        rule_id = rule.get("id")
        locator = rule.get("locator")
        validation = rule.get("validation")
        if not rule_id or not locator:
            fail(f"rule missing id or locator: {rule_id}")
        if not isinstance(validation, dict):
            fail(f"rule {rule_id}: validation block is required")
        checks = validation.get("checks")
        if not isinstance(checks, list) or not checks:
            fail(f"rule {rule_id}: validation.checks must be non-empty")

        evidence: list[dict[str, str]] = []
        for check_id in checks:
            if not isinstance(check_id, str) or not check_id:
                fail(f"rule {rule_id}: invalid evidence id")
            evidence_ids.add(check_id)
            if check_id in runner_checks:
                evidence.append(
                    {
                        "id": check_id,
                        "kind": "runner-gate",
                        "command": " ".join(runner_checks[check_id].command),
                    }
                )
            else:
                evidence.append({"id": check_id, "kind": "unclassified", "command": ""})
                unclassified_ids.add(check_id)

        resolution = rule.get("resolution") or {}
        rows.append(
            {
                "rule_id": rule_id,
                "category": rule.get("category"),
                "authority": rule.get("authority", "normative"),
                "requirement": rule.get("requirement"),
                "locator": locator,
                "sources": rule.get("sources", []),
                "governing_sources": resolution.get("governing_sources", []),
                "validation_mode": validation.get("mode"),
                "evidence": evidence,
            }
        )

    mapped_rules = sum(
        any(item["kind"] == "runner-gate" for item in row["evidence"])
        for row in rows
    )
    only_unclassified = sum(
        all(item["kind"] == "unclassified" for item in row["evidence"])
        for row in rows
    )

    return {
        "schema_version": 1,
        "contract_reviewed_at": contract["reviewed_at"],
        "rule_count": len(rows),
        "runner_gate_count": len(runner_checks),
        "distinct_evidence_ids": len(evidence_ids),
        "rules_with_runner_gate": mapped_rules,
        "rules_with_only_unclassified_evidence": only_unclassified,
        "unclassified_evidence_ids": sorted(unclassified_ids),
        "rows": rows,
    }


def write_markdown(matrix: dict[str, Any], path: Path) -> None:
    lines = [
        "# UFCtex normative traceability",
        "",
        f"- Rules: **{matrix['rule_count']}**",
        f"- Runner gates: **{matrix['runner_gate_count']}**",
        f"- Distinct evidence IDs: **{matrix['distinct_evidence_ids']}**",
        f"- Rules linked to at least one runner gate: **{matrix['rules_with_runner_gate']}**",
        f"- Rules with only unclassified evidence: **{matrix['rules_with_only_unclassified_evidence']}**",
        "",
        "## Unclassified evidence IDs",
        "",
    ]
    ids = matrix["unclassified_evidence_ids"]
    if ids:
        lines.extend(f"- `{item}`" for item in ids)
    else:
        lines.append("None.")
    lines.extend(
        [
            "",
            "## Rule matrix",
            "",
            "| Rule | Category | Mode | Sources | Locator | Evidence |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in matrix["rows"]:
        evidence = ", ".join(
            f"{item['id']} ({item['kind']})" for item in row["evidence"]
        )
        sources = ", ".join(row["sources"])
        locator = str(row["locator"]).replace("|", "\\|")
        lines.append(
            f"| `{row['rule_id']}` | {row['category']} | {row['validation_mode']} | "
            f"{sources} | {locator} | {evidence} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit UFCtex normative rule traceability.")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--strict-evidence", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    matrix = build_matrix()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown:
        write_markdown(matrix, args.markdown)

    print(
        "Normative traceability audit: "
        f"{matrix['rule_count']} rules, "
        f"{matrix['rules_with_runner_gate']} linked to runner gates, "
        f"{matrix['rules_with_only_unclassified_evidence']} with only unclassified evidence, "
        f"{len(matrix['unclassified_evidence_ids'])} unclassified evidence IDs."
    )
    if matrix["unclassified_evidence_ids"]:
        print("Unclassified evidence IDs: " + ", ".join(matrix["unclassified_evidence_ids"]))
    if args.strict_evidence and matrix["unclassified_evidence_ids"]:
        fail("strict evidence classification requested with unclassified evidence IDs")


if __name__ == "__main__":
    main()

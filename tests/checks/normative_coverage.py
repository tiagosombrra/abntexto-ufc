#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests" / "checks"))

from normative_catalog import load_catalog, rule_map
from normative_full import full_rule_map, load_full_contract
from normative_traceability import load_evidence_registry, load_runner_checks


def fail(message: str) -> None:
    raise SystemExit(f"Normative coverage failed: {message}")


def quoted_pairs(text: str, function: str) -> set[tuple[str, str]]:
    pattern = rf"{re.escape(function)}\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]"
    return set(re.findall(pattern, text))


def main() -> None:
    catalog = load_catalog()
    base_rules = rule_map(catalog)
    contract = load_full_contract(catalog)
    rules = full_rule_map(contract)

    contract_reviewed = max(
        date.fromisoformat(catalog["reviewed_at"]),
        date.fromisoformat(catalog["precedence_reviewed_at"]),
        date.fromisoformat(contract["reviewed_at"]),
    )

    for source in catalog["sources"]:
        checked = date.fromisoformat(source["checked_at"])
        if checked > contract_reviewed:
            fail(
                f"source {source['id']} was checked on {checked} after the current "
                f"full-contract review {contract_reviewed}; review affected rules first"
            )

    runner_checks = load_runner_checks()
    gate_checks = set(runner_checks)
    registered_checks = set(load_evidence_registry(runner_checks))

    cli = (ROOT / "tools" / "validate-ufc-pdf.py").read_text(encoding="utf-8")
    web = (ROOT / "validator" / "app.js").read_text(encoding="utf-8")
    mappings = quoted_pairs(cli, "norm_check") | quoted_pairs(web, "nck")
    validator_checks = {check_id for check_id, _ in mappings}

    unknown_rules = sorted({rule_id for _, rule_id in mappings if rule_id not in base_rules})
    if unknown_rules:
        fail("validator references unknown base rules: " + ", ".join(unknown_rules))

    known_checks = gate_checks | validator_checks | registered_checks
    uncovered = sorted(
        rule_id
        for rule_id, rule in rules.items()
        if rule["validation"]["mode"] != "not-applicable"
        and not set(rule["validation"]["checks"]) & known_checks
    )
    if uncovered:
        fail("current executable rules without a known gate or validator check: " + ", ".join(uncovered))

    automatic = sum(
        rule["validation"]["mode"].startswith("automatic")
        for rule in rules.values()
    )
    manual_review = sum(
        rule["validation"]["mode"] == "manual"
        for rule in rules.values()
    )
    conditional_review = sum(
        rule["validation"]["mode"] in {"conditional", "conditional-manual"}
        for rule in rules.values()
    )
    not_applicable = sum(
        rule["validation"]["mode"] == "not-applicable"
        for rule in rules.values()
    )
    project_policy = sum(
        rule["authority"] in {"project-policy", "technical-profile"}
        for rule in rules.values()
    )

    print(
        "NORMATIVE-COVERAGE-EVIDENCE status=PASS "
        f"sources={len(catalog['sources'])} rules={len(rules)} "
        f"automatic_declared={automatic} manual_review={manual_review} "
        f"conditional_review={conditional_review} not_applicable={not_applicable} "
        f"project_policy={project_policy} runner_gates={len(gate_checks)} "
        f"registered_evidence={len(registered_checks)} "
        f"validator_checks={len(validator_checks)} "
        f"coverage_semantics=runtime-rule-contribution "
        f"reviewed={contract_reviewed.isoformat()}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import load_catalog, rule_map


def fail(message: str) -> None:
    raise SystemExit(f"Normative coverage failed: {message}")


def quoted_pairs(text: str, function: str) -> set[tuple[str, str]]:
    pattern = rf"{re.escape(function)}\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]"
    return set(re.findall(pattern, text))


def main() -> None:
    catalog = load_catalog()
    rules = rule_map(catalog)
    reviewed = date.fromisoformat(catalog["reviewed_at"])

    for source in catalog["sources"]:
        checked = date.fromisoformat(source["checked_at"])
        if checked > reviewed:
            fail(
                f"source {source['id']} was checked on {checked} after catalog review {reviewed}; "
                "review affected rules and advance reviewed_at"
            )

    runner = (ROOT / "tests" / "run.py").read_text(encoding="utf-8")
    gate_checks = set(re.findall(r'Check\("([^"]+)"', runner))

    cli = (ROOT / "tools" / "validate-ufc-pdf.py").read_text(encoding="utf-8")
    web = (ROOT / "validator" / "app.js").read_text(encoding="utf-8")
    mappings = quoted_pairs(cli, "norm_check") | quoted_pairs(web, "nck")
    validator_checks = {check_id for check_id, _ in mappings}

    unknown_rules = sorted({rule_id for _, rule_id in mappings if rule_id not in rules})
    if unknown_rules:
        fail("validator references unknown rules: " + ", ".join(unknown_rules))

    uncovered: list[str] = []
    known_checks = gate_checks | validator_checks
    for rule_id, rule in rules.items():
        evidence = set(rule["validation"]["checks"])
        if not evidence & known_checks:
            uncovered.append(rule_id)
    if uncovered:
        fail("rules without a known gate or validator check: " + ", ".join(sorted(uncovered)))

    direct_by_rule: dict[str, set[str]] = {}
    for check_id, rule_id in mappings:
        direct_by_rule.setdefault(rule_id, set()).add(check_id)

    automatic = sum(rule["validation"]["mode"].startswith("automatic") for rule in rules.values())
    manual = len(rules) - automatic
    print(
        "Normative coverage passed: "
        f"{len(catalog['sources'])} sources, {len(rules)} rules, "
        f"{automatic} automatic/partial, {manual} manual/conditional, "
        f"{len(gate_checks)} unified gates, {len(validator_checks)} direct PDF checks, "
        f"{len(direct_by_rule)} rules consumed directly by validators."
    )


if __name__ == "__main__":
    main()

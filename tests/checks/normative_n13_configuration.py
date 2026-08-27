#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-ufc-pdf.py"
RULE_ID = "font.family.body"
MECHANISM_ID = "configuration-strict-rejection"
FALLBACK_NAMES = ("TeXGyreTermesX-Regular", "NewTXMI")
LITERAL_CASES = (
    ("TimesNewRomanPSMT", "NewTXMI", "txsys"),
    ("ArialMT", "TeXGyreTermesMath-Regular"),
)


def fail(message: str) -> None:
    raise SystemExit(f"N13 configuration receipt failed: {message}")


def font_rows(names: tuple[str, ...]) -> list[dict[str, str]]:
    return [{"name": name, "emb": "yes", "uni": "yes"} for name in names]


def literal_check(namespace: dict[str, Any], names: tuple[str, ...], profile: str) -> Any:
    checks = namespace["check_fonts"](font_rows(names), profile)
    matches = [check for check in checks if getattr(check, "id", "") == "font.literal"]
    if len(matches) != 1:
        fail(f"expected one font.literal check for profile={profile}; found {len(matches)}")
    return matches[0]


def validate_binding(namespace: dict[str, Any], check: Any) -> None:
    rule = namespace["RULES"][RULE_ID]
    if getattr(check, "normative_rule", "") != RULE_ID:
        fail(f"font.literal is not bound to {RULE_ID}")
    if getattr(check, "locator", "") != rule["locator"]:
        fail("font.literal locator drift")
    if getattr(check, "normativity", "") != rule["normativity"]:
        fail("font.literal normativity drift")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bind N13 configuration-strict rejection to the existing UFC PDF validator semantics."
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=ROOT / "artifacts" / "n13-negative" / "configuration-strict-rejection.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sys.path.insert(0, str(ROOT / "tools"))
    namespace = runpy.run_path(str(VALIDATOR), run_name="n13_configuration_validator")

    strict = literal_check(namespace, FALLBACK_NAMES, "strict")
    portable = literal_check(namespace, FALLBACK_NAMES, "portable")
    validate_binding(namespace, strict)
    validate_binding(namespace, portable)

    if strict.status != namespace["FAIL"]:
        fail(f"same textual fallback must be REPROVADO in strict; observed {strict.status}")
    if portable.status != namespace["WARN"]:
        fail(f"same textual fallback must be ALERTA in portable; observed {portable.status}")
    if not strict.mandatory:
        fail("strict font.literal check must remain mandatory")
    if portable.mandatory:
        fail("portable font.literal check must remain non-mandatory")

    literal_results: list[dict[str, Any]] = []
    for names in LITERAL_CASES:
        check = literal_check(namespace, names, "strict")
        validate_binding(namespace, check)
        if check.status != namespace["PASS"]:
            fail(f"literal allowed family must pass in strict: {names}: {check.status}")
        literal_results.append(
            {
                "names": list(names),
                "profile": "strict",
                "status": check.status,
                "mandatory": check.mandatory,
            }
        )

    rule = namespace["RULES"][RULE_ID]
    payload = {
        "schema_version": 1,
        "phase": "N13",
        "mechanism": MECHANISM_ID,
        "source_commit_sha": os.environ.get("SOURCE_COMMIT_SHA", os.environ.get("GITHUB_SHA", "")),
        "result": "PASS",
        "rule_id": RULE_ID,
        "locator": rule["locator"],
        "normativity": rule["normativity"],
        "same_observation": True,
        "fallback_observation": {
            "names": list(FALLBACK_NAMES),
            "strict": {
                "status": strict.status,
                "mandatory": strict.mandatory,
                "evidence": strict.evidence,
            },
            "portable": {
                "status": portable.status,
                "mandatory": portable.mandatory,
                "evidence": portable.evidence,
            },
        },
        "literal_allowed_family_controls": literal_results,
        "compile_failure_counted_as_rejection": False,
        "normative_contract_changed": False,
        "locator_policy_changed": False,
        "oracle_tolerances_changed": False,
        "proof_state_changed": False,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N13-EVIDENCE mechanism=configuration-strict-rejection status=PASS "
        f"rule={RULE_ID} strict={strict.status} portable={portable.status} "
        "same_observation=true compile_failure_counted_as_rejection=false proof_state_changed=false"
    )


if __name__ == "__main__":
    main()

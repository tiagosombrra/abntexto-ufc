#!/usr/bin/env python3
"""Fail closed if any public setup tag, command, environment or upstream name
is missing from the PT/EN/ES/FR internationalization accountability inventory.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = ROOT / "standards/api/public-api.json"
I18N = ROOT / "standards/api/i18n-coverage-inventory.json"


def validate(api: dict, ledger: dict) -> tuple[int, int, int, int]:
    groups = [
        ("setup_keys", {k for names in api["setup_keys"].values() for k in names}),
        ("public_commands", set(api["public_commands"]["canonical"])),
        ("public_environments", set(api["public_environments"]["canonical"])),
        ("retained_upstream_identifiers",
         set(api["upstream_boundary"]["retained_identifiers"])),
    ]
    result = []
    if ledger["target_locales"] != ["pt", "en", "es", "fr"]:
        raise ValueError("required locales changed")
    if ledger["completion"] != "PENDING_INTEGRATED_PDF_AND_HUMAN_REVIEW":
        raise ValueError("completion label cannot be promoted by static inventory")
    for group, expected in groups:
        if not expected or len(ledger[group]) != len(expected) or set(ledger[group]) != expected:
            missing = sorted(expected - set(ledger[group]))
            extra = sorted(set(ledger[group]) - expected)
            raise ValueError(f"{group}: missing={missing} extra={extra}")
        for identifier, entry in ledger[group].items():
            if not isinstance(entry, dict) or not entry.get("origin"):
                raise ValueError(f"{group}/{identifier} lacks origin mapping")
            if group != "setup_keys" and entry.get("certification") != "PENDING_END_TO_END":
                raise ValueError(f"{group}/{identifier} claims unverified certification")
            if group == "setup_keys" and not entry.get("requirement"):
                raise ValueError(f"{group}/{identifier} lacks value/translation boundary")
        result.append(len(expected))
    return tuple(result)


def main() -> None:
    api = json.loads(API.read_text(encoding="utf-8"))
    inventory = json.loads(I18N.read_text(encoding="utf-8"))
    counts = validate(api, inventory)
    # A public API addition that is not mapped must fail before a lengthy
    # matrix test. A phantom name in the ledger must also fail.
    negative = copy.deepcopy(inventory)
    negative["public_commands"].pop(next(iter(negative["public_commands"])))
    try:
        validate(api, negative)
    except ValueError:
        pass
    else:
        raise ValueError("missing-command negative was accepted")
    negative = copy.deepcopy(inventory)
    negative["setup_keys"]["imaginary-tag"] = {
        "origin": "user_supplied_value", "requirement": "placeholder"}
    try:
        validate(api, negative)
    except ValueError:
        pass
    else:
        raise ValueError("phantom setup tag was accepted")
    print("I18N-API-INVENTORY status=PASS setup_keys=%d commands=%d "
          "environments=%d upstream_identifiers=%d locales=4 negatives=PASS"
          % counts)


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError) as exc:
        raise SystemExit(f"I18N-API-INVENTORY status=FAIL reason={exc}") from exc

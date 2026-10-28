#!/usr/bin/env python3
"""Real-TeX, four-locale round-trip for authored/default public metadata.

The 53 authored/default key identifiers are stable API names, not strings
the class is supposed to translate. At the very end of each integrated
manuscript, reconfigure them with distinct synthetic author values, expand
the actual public \ufcMeta{key} command into the TeX log, and verify that the
values survive unchanged. The probe is deliberately after all typeset pages
so it does not alter title pages, bibliography, anonymous layouts or PDFs.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INVENTORY = ROOT / "standards/api/i18n-coverage-inventory.json"
ORIGINS = {"user_supplied_value", "default_or_user_value"}


def metadata_keys() -> tuple[str, ...]:
    ledger = json.loads(INVENTORY.read_text(encoding="utf-8"))
    result = tuple(sorted(
        key for key, entry in ledger["setup_keys"].items()
        if entry["origin"] in ORIGINS
    ))
    if len(result) != 53 or sum(
            entry["origin"] == "user_supplied_value"
            for entry in ledger["setup_keys"].values()) != 49:
        raise ValueError("public metadata inventory changed; re-audit its boundary")
    if len(set(result)) != len(result):
        raise ValueError("duplicate metadata key")
    return result


METADATA_KEYS = metadata_keys()


def marker(key: str) -> str:
    if key not in METADATA_KEYS:
        raise ValueError(f"undeclared authored metadata key: {key}")
    return f"AUTHORVALUE{METADATA_KEYS.index(key) + 1:02d}"


def source_lines() -> list[str]:
    """A post-document-content probe: actual \ufcsetup and \ufcMeta commands."""
    lines = [r"\ufcsetup{"]
    for i, key in enumerate(METADATA_KEYS):
        comma = "," if i + 1 < len(METADATA_KEYS) else ""
        lines.append(f"  {key}={{{marker(key)}}}{comma}")
    lines.append("}")
    for key in METADATA_KEYS:
        lines.append(
            rf"\typeout{{INTEGRATED-META-{key}=\ufcMeta{{{key}}}}}"
        )
    return lines


def check_source(source: str) -> int:
    block = "\n".join(source_lines()) + "\n"
    if source.count(block) != 1:
        raise ValueError("missing/duplicated/altered complete metadata probe")
    if not source.index(block) < source.index(r"\end{document}"):
        raise ValueError("metadata probe executes after document end")
    return len(METADATA_KEYS)


def expected_receipt(key: str) -> str:
    return f"INTEGRATED-META-{key}={marker(key)}"


def check_log(log: str) -> int:
    """Use complete TeX log lines to reject prefixes and doctored values."""
    actual = log.splitlines()
    for key in METADATA_KEYS:
        receipt = expected_receipt(key)
        if actual.count(receipt) != 1:
            raise ValueError(f"missing/duplicated/translated metadata value: {key}")
    return len(METADATA_KEYS)


def negative_controls() -> int:
    """Exercise the same production predicates with effective mutations."""
    block = "\n".join(source_lines()) + "\n"
    receipt_log = "\n".join(expected_receipt(k) for k in METADATA_KEYS)
    if check_source(block + r"\end{document}" + "\n") != 53:
        raise ValueError("metadata source positive control")
    if check_log(receipt_log) != 53:
        raise ValueError("metadata log positive control")
    controls = 0
    for key in (METADATA_KEYS[0], METADATA_KEYS[len(METADATA_KEYS) // 2],
                METADATA_KEYS[-1]):
        source_bad = block.replace(
            f"{key}={{{marker(key)}}}",
            f"{key}={{ALTEREDVALUE}}", 1,
        ) + r"\end{document}" + "\n"
        if source_bad == block + r"\end{document}" + "\n":
            raise ValueError("ineffective source metadata mutation")
        try:
            check_source(source_bad)
        except ValueError:
            controls += 1
        else:
            raise ValueError(f"source mutation accepted: {key}")
        log_bad = receipt_log.replace(expected_receipt(key),
                                      f"INTEGRATED-META-{key}=TRANSLATEDVALUE", 1)
        if log_bad == receipt_log:
            raise ValueError("ineffective log metadata mutation")
        try:
            check_log(log_bad)
        except ValueError:
            controls += 1
        else:
            raise ValueError(f"log mutation accepted: {key}")
    removed = receipt_log.replace(expected_receipt(METADATA_KEYS[-1]), "", 1)
    try:
        check_log(removed)
    except ValueError:
        controls += 1
    else:
        raise ValueError("missing receipt mutation accepted")
    duplicated = receipt_log + "\n" + expected_receipt(METADATA_KEYS[0])
    try:
        check_log(duplicated)
    except ValueError:
        controls += 1
    else:
        raise ValueError("duplicated receipt mutation accepted")
    return controls

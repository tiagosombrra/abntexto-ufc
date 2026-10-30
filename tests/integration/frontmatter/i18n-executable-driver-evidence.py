#!/usr/bin/env python3
"""Fail-closed source-to-executable-runner evidence; never a blanket i18n PASS."""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "tests/integration/frontmatter/i18n-executable-driver-evidence.json"
CROSSWALK = ROOT / "standards/api/i18n-functional-evidence-crosswalk.json"
OUTPUT = ROOT / "artifacts/validation/i18n-executable-driver-evidence.json"
REQUIRED = {
    r"\ufcMathFontPolicy", r"\ufcPrintCatalogCard", r"\ufcPrintDedication",
    r"\ufcPrintEpigraph", r"\ufcInputListing", "strict-font",
}
RECORD_KEYS = {
    "identifier", "group", "fixture", "driver", "check",
    "markers", "scope", "receipt_state",
}
RECEIPT = "EXECUTABLE_DRIVER_LINK_NOT_PER_IDENTIFIER_CERTIFIED"
ACCEPTANCE = "PENDING_ITEM_PDF_ASSERTIONS_AND_HUMAN_REVIEW"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def registered_checks() -> dict[str, str]:
    """Inspect actual tests/run.py Check declarations, not textual comments."""
    tree = ast.parse((ROOT / "tests/run.py").read_text(encoding="utf-8"))
    found: dict[str, str] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "Check":
            continue
        if len(node.args) < 3 or not isinstance(node.args[0], ast.Constant):
            continue
        command = node.args[2]
        if not isinstance(command, ast.Call) or not isinstance(command.func, ast.Name):
            continue
        if command.func.id != "integration_command" or not command.args:
            continue
        if not isinstance(command.args[0], ast.Constant):
            continue
        name, filename = node.args[0].value, command.args[0].value
        if not isinstance(name, str) or not isinstance(filename, str) or name in found:
            raise ValueError("ambiguous/non-string runner registration")
        found[name] = filename
    return found


def source_path(value: str, allowed_prefix: str) -> Path:
    if (not isinstance(value, str) or not value.startswith(allowed_prefix)
            or ".." in Path(value).parts or Path(value).is_absolute()):
        raise ValueError(f"unsafe fixture/driver path: {value!r}")
    path = (ROOT / value).resolve()
    allowed = (ROOT / allowed_prefix).resolve()
    if not path.is_relative_to(allowed) or not path.is_file():
        raise ValueError(f"missing or escaped fixture/driver: {value!r}")
    return path


def validate(ledger: dict, crosswalk: dict) -> list[dict]:
    if ledger.get("schema_version") != 1:
        raise ValueError("unsupported driver evidence schema")
    if ledger.get("global_acceptance") != ACCEPTANCE:
        raise ValueError("prematurely claimed complete internationalization")
    entries = ledger.get("entries")
    if not isinstance(entries, list) or len(entries) != len(REQUIRED):
        raise ValueError("driver source relationships must cover exactly six names")
    registration = registered_checks()
    records = []
    seen = set()
    for row in entries:
        if not isinstance(row, dict) or set(row) != RECORD_KEYS:
            raise ValueError("unknown/missing driver evidence field")
        identifier = row["identifier"]
        group = row["group"]
        if identifier not in REQUIRED or identifier in seen:
            raise ValueError("invented/duplicate public identifier")
        seen.add(identifier)
        if group not in ("public_commands", "setup_option_identifiers"):
            raise ValueError("unsupported public identifier category")
        if identifier not in crosswalk["entries"][group]:
            raise ValueError("public identifier not in canonical crosswalk")
        if row["receipt_state"] != RECEIPT:
            raise ValueError("unproven per-ID functional certification")
        if not isinstance(row["scope"], str) or len(row["scope"]) < 35:
            raise ValueError("unqualified bounded execution scope")
        fixture = source_path(row["fixture"], "tests/documents/")
        driver = source_path(row["driver"], "tests/integration/")
        from path_resolver import integration_file
        try:
            actual = integration_file(driver.name)
        except RuntimeError as exc:
            raise ValueError(f"runner cannot resolve driver: {driver.name}") from exc
        if actual.resolve() != driver:
            raise ValueError("test runner resolves a different driver")
        if registration.get(row["check"]) != driver.name:
            raise ValueError("test runner check is not registered to this driver")
        script = driver.read_text(encoding="utf-8")
        source = fixture.read_text(encoding="utf-8")
        if row["fixture"] not in script:
            raise ValueError("driver does not actually consume the named TeX fixture")
        token = identifier.lstrip("\\")
        pattern = r"(?<![A-Za-z])" + re.escape(token) + r"(?![A-Za-z])"
        if re.search(pattern, source) is None:
            raise ValueError("public command/option absent from claimed TeX fixture")
        cross = crosswalk["entries"][group][identifier]
        if cross["proof_state"] != "SOURCE_REFERENCE_ONLY":
            raise ValueError("upstream lexical source not independently linked")
        if cross["candidate_test_file"] not in (row["fixture"], row["driver"]):
            raise ValueError("driver evidence conflicts with source crosswalk")
        markers = row["markers"]
        if (not isinstance(markers, list) or len(markers) < 3
                or len(set(markers)) != len(markers)
                or any(not isinstance(t, str) or len(t) < 8 or t not in script
                       for t in markers)):
            raise ValueError("missing/non-independent runner output assertions")
        if not re.search(r"\b(pdflatex|lualatex|for engine)\b", script):
            raise ValueError("driver has no real TeX compilation path")
        if not ("pdftotext" in script or "pdffonts" in script):
            raise ValueError("driver does not inspect an actual PDF")
        records.append({
            "identifier": identifier, "group": group,
            "fixture": row["fixture"], "fixture_sha256": sha256(fixture),
            "driver": row["driver"], "driver_sha256": sha256(driver),
            "registered_check": row["check"], "assertion_markers": markers,
            "evidence": RECEIPT, "scope": row["scope"],
            "actual_linux_gate": "REQUIRES_EXACT_SHA_COMPLETE_LINUX_RECEIPT",
            "per_locale_per_profile_pdf_evidence": "PENDING",
            "human_linguistic_review": "PENDING",
        })
    if seen != REQUIRED:
        raise ValueError("missing canonical driver relationship")
    return sorted(records, key=lambda x: x["identifier"])


def mutants(ledger: dict, crosswalk: dict) -> int:
    damaged = []
    def mutate():
        return copy.deepcopy(ledger)
    a = mutate()
    a["entries"].pop()
    damaged.append(a)
    a = mutate()
    a["entries"][0] = copy.deepcopy(a["entries"][1])
    damaged.append(a)
    a = mutate()
    a["entries"][0]["identifier"] = r"\ufcNotRegistered"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["fixture"] = "tests/documents/missing.tex"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["driver"] = "tests/integration/layout/missing.sh"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["check"] = "no-such-check"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["markers"][0] = "SYNTHETIC_ASSERTION_DOES_NOT_EXIST"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["receipt_state"] = "FUNCTIONALLY_CERTIFIED"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["fixture"] = "../../etc/passwd"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["group"] = "retained_upstream_identifiers"
    damaged.append(a)
    a = mutate()
    a["global_acceptance"] = "CERTIFIED"
    damaged.append(a)
    a = mutate()
    a["entries"][0]["markers"] = []
    damaged.append(a)
    for index, bad in enumerate(damaged, 1):
        try:
            validate(bad, crosswalk)
        except (ValueError, KeyError):
            continue
        raise ValueError(f"negative driver relation mutant {index} was accepted")
    return len(damaged)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "tests"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    records = validate(ledger, crosswalk)
    count = mutants(ledger, crosswalk)
    source_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if os.getenv("SOURCE_COMMIT_SHA") and os.environ["SOURCE_COMMIT_SHA"] != source_sha:
        raise ValueError("checked out Git SHA differs from expected CI source")
    if args.report:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps({
            "status": "EXECUTABLE_DRIVER_LINK_ONLY",
            "source_sha": source_sha,
            "test_registry_sha256": sha256(ROOT / "tests/run.py"),
            "negative_controls": count,
            "globally_functional_i18n_certified": False,
            "records": records,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"I18N-EXECUTABLE-DRIVERS status=PASS source_sha={source_sha}"
          f" mapped={len(records)} negative_controls={count}"
          " registered_checks=PASS fixture_source=PASS PDF_test_source=PASS"
          " independent_per_id_pdf=NOT_CLAIMED locales_profiles=PENDING"
          " human_review=PENDING")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, SyntaxError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-EXECUTABLE-DRIVERS status=FAIL reason={exc}") from exc

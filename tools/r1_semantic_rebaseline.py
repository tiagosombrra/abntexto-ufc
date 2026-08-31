#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS_DIR = ROOT / "tests" / "checks"
STANDARDS_DIR = ROOT / "standards"
RUNNER = ROOT / "tests" / "run.py"
PREFLIGHT = ROOT / ".github" / "workflows" / "latex-preflight.yml"

CANONICAL_CHECK_ALIASES = {
    "layout.a4": "pdf-geometry",
    "layout.margins": "pdf-geometry",
    "pdfa.deep": "pdfa",
    "profile-matrix": "profiles",
    "project": "research-project",
    "font.literal": "windows-font-pdfa",
    "windows-font-poc": "windows-font-pdfa",
    "catalog.optional": "catalog-card",
}
EXTERNAL_CHECKS = {"windows-font-pdfa"}


def fail(message: str) -> None:
    raise SystemExit(f"R1 semantic rebaseline failed: {message}")


def normalize_validation_checks(value: object) -> None:
    if isinstance(value, dict):
        validation = value.get("validation")
        if isinstance(validation, dict):
            checks = validation.get("checks")
            if isinstance(checks, list):
                normalized: list[object] = []
                for check in checks:
                    replacement = CANONICAL_CHECK_ALIASES.get(check, check) if isinstance(check, str) else check
                    if replacement not in normalized:
                        normalized.append(replacement)
                validation["checks"] = normalized
        for child in value.values():
            normalize_validation_checks(child)
    elif isinstance(value, list):
        for child in value:
            normalize_validation_checks(child)


def update_standard_contracts() -> list[str]:
    changed: list[str] = []
    for path in sorted(STANDARDS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON before migration: {path.relative_to(ROOT)}: {exc}")
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        normalize_validation_checks(data)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if after != before:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
    return changed


def update_validation_policy_consumers() -> list[str]:
    changed: list[str] = []
    patterns = [
        re.compile(
            r'if\s+(?P<var>[A-Za-z_][A-Za-z0-9_]*)\.get\("schema_version"\)\s*!=\s*1\s+or\s+(?P=var)\.get\("phase"\)\s*!=\s*"N5"\s*:'
        ),
        re.compile(
            r"if\s+(?P<var>[A-Za-z_][A-Za-z0-9_]*)\.get\('schema_version'\)\s*!=\s*1\s+or\s+(?P=var)\.get\('phase'\)\s*!=\s*'N5'\s*:"
        ),
    ]
    for path in sorted(CHECKS_DIR.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if "validation-reference-policy.json" not in text:
            continue
        original = text
        for pattern in patterns:
            text = pattern.sub(lambda match: f'if {match.group("var")}.get("schema_version") != 2:', text)
        text = text.replace("invalid oracle policy schema/phase", "invalid validation policy schema")
        text = text.replace("invalid validation policy schema/phase", "invalid validation policy schema")
        text = text.replace("invalid N5 validation policy schema", "invalid validation policy schema")
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
    return changed


def runner_ids() -> set[str]:
    module = ast.parse(RUNNER.read_text(encoding="utf-8"))
    result: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "Check":
            continue
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            result.add(node.args[0].value)
    return result


def audit_validation_owners() -> None:
    known = runner_ids()
    legacy: list[str] = []
    unknown: list[str] = []

    def walk(value: object, source: str) -> None:
        if isinstance(value, dict):
            validation = value.get("validation")
            if isinstance(validation, dict):
                mode = str(validation.get("mode", ""))
                checks = validation.get("checks")
                if isinstance(checks, list):
                    for check in checks:
                        if not isinstance(check, str):
                            continue
                        if check in CANONICAL_CHECK_ALIASES:
                            legacy.append(f"{source}: {check}")
                        if "manual" not in mode and check not in known and check not in EXTERNAL_CHECKS:
                            unknown.append(f"{source}: mode={mode} check={check}")
            for child in value.values():
                walk(child, source)
        elif isinstance(value, list):
            for child in value:
                walk(child, source)

    for path in sorted(STANDARDS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        walk(data, path.relative_to(ROOT).as_posix())

    if legacy:
        fail("legacy validation aliases remain:\n" + "\n".join(sorted(set(legacy))))
    if unknown:
        fail("automatic validation checks without owner:\n" + "\n".join(sorted(set(unknown))))

    preflight = PREFLIGHT.read_text(encoding="utf-8")
    if "tests/integration/windows-font-pdfa.sh" not in preflight:
        fail("external check windows-font-pdfa has no workflow owner")


def audit_policy_schema_consumers() -> None:
    findings: list[str] = []
    for path in sorted(CHECKS_DIR.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if "validation-reference-policy.json" not in text:
            continue
        for match in re.finditer(
            r'(?P<var>[A-Za-z_][A-Za-z0-9_]*)\.get\(["\']schema_version["\']\)\s*!=\s*1',
            text,
        ):
            findings.append(f"{path.relative_to(ROOT)}: schema 1 consumer {match.group('var')}")
    if findings:
        fail("validation policy schema-1 consumers remain:\n" + "\n".join(findings))


def main() -> None:
    standards_changed = update_standard_contracts()
    consumers_changed = update_validation_policy_consumers()
    audit_validation_owners()
    audit_policy_schema_consumers()
    print(f"R1 semantic rebaseline: standards_changed={len(standards_changed)} consumers_changed={len(consumers_changed)}")
    for path in standards_changed + consumers_changed:
        print(path)


if __name__ == "__main__":
    main()

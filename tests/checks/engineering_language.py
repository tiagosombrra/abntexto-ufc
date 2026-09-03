#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE_ROOTS = ("tests/checks/", "tests/integration/", "tests/smoke/", "tools/", "validator/", ".github/workflows/")
SOURCE_SUFFIXES = {".py", ".sh", ".js", ".yml", ".yaml", ".ps1"}
DIAGNOSTIC_MARKERS = ("echo ", "printf ", "raise SystemExit", "fail_semantic", "errors.append", "print(", "ArgumentParser(", "help=", "description=", "throw new Error", "console.")
PORTUGUESE_TECHNICAL_TERMS = re.compile(r"\b(?:auditoria|validando|falhou|conclu[ií]d[oa]|ausente(?:s)?|incorret[oa]|desconhecid[oa]|evid[eê]ncia|p[aá]gina(?:s)?|r[oó]tulo(?:s)?|descri[cç][aã]o|desalinhad[oa]|marcador(?:es)?|m[eé]trica(?:s)?|comando(?:s)?|conte[uú]do|t[ií]tulo(?:s)?|refer[eê]ncia(?:s)?|cita[cç][aã]o|espa[cç]amento|se[cç][aã]o|perfil(?:s)?|sum[aá]rio|capa|orientador|identificador|navega[cç][aã]o|fotografia(?:s)?|ap[eê]ndice|anexo|[ií]ndice|gloss[aá]rio|dedicat[oó]ria|ep[ií]grafe|agradecimentos|bras[aã]o)\b", re.IGNORECASE)
RETIRED_PROFILE_IDS = re.compile(r"(?<![A-Za-z0-9_-])(?:tccgraduacao|tccespecializacao|dissertacao|tese|projetoanonimizado|projeto)(?![A-Za-z0-9_-])")
MACHINE_JSON_FILES = (
    "standards/catalog.json",
    "standards/coverage-rules-frontmatter.json",
    "standards/coverage-rules-project.json",
    "standards/frontmatter-approval-scenario.json",
    "standards/frontmatter-cover-scenario.json",
)
MACHINE_SOURCE_FILES = (
    "tests/checks/normative_frontmatter_title_page.py",
    "tests/integration/frontmatter-approval-evidence.sh",
)
RETIRED_PROFILE_VALUES = {"tccgraduacao", "tccespecializacao", "dissertacao", "tese", "projeto", "projetoanonimizado"}
ACADEMIC_LITERAL_ALLOWLIST = ("SUMÁRIO", "REFERÊNCIAS", "APÊNDICE", "ANEXO", "ÍNDICE REMISSIVO")


def tracked() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / item.decode() for item in output.split(b"\0") if item]


def is_comment_or_diagnostic(line: str) -> bool:
    stripped = line.lstrip()
    if stripped.startswith("#!"):
        return False
    if stripped.startswith(("#", "//", "/*", "* ")):
        return True
    return any(marker in line for marker in DIAGNOSTIC_MARKERS)


def normalized_diagnostic(line: str) -> str:
    result = line
    for literal in ACADEMIC_LITERAL_ALLOWLIST:
        result = result.replace(literal, "")
    return result


def audit() -> list[str]:
    errors: list[str] = []
    for path in tracked():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix not in SOURCE_SUFFIXES or not rel.startswith(EXECUTABLE_ROOTS):
            continue
        if rel == "tests/checks/engineering_language.py":
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if is_comment_or_diagnostic(line) and PORTUGUESE_TECHNICAL_TERMS.search(normalized_diagnostic(line)):
                errors.append(f"{rel}:{number}: Portuguese project-owned engineering text: {line.strip()}")

    def visit_machine_values(value, location: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                visit_machine_values(item, f"{location}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit_machine_values(item, f"{location}[{index}]")
        elif isinstance(value, str) and value in RETIRED_PROFILE_VALUES:
            errors.append(f"{location}: retired Portuguese technical profile identifier: {value}")

    for rel in MACHINE_JSON_FILES:
        payload = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        visit_machine_values(payload, rel)
    for rel in MACHINE_SOURCE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if RETIRED_PROFILE_IDS.search(line):
                errors.append(f"{rel}:{number}: retired Portuguese technical profile identifier: {line.strip()}")
    api = ROOT / "release/v3-api-migration.json"
    if not api.is_file():
        errors.append("release/v3-api-migration.json: live migration contract is missing")
    for removed in (ROOT / "release/v3-test-migration.json", ROOT / "release/v3-path-migration.json"):
        if removed.exists():
            errors.append(f"{removed.relative_to(ROOT)}: closed unconsumed migration contract remains active")
    for consumer in ("tests/checks/v3_api_residual.py", "tests/checks/profile_matrix_contract.py"):
        if "release/v3-api-migration.json" not in (ROOT / consumer).read_text(encoding="utf-8"):
            errors.append(f"{consumer}: expected live API migration contract consumer is missing")
    return errors


def self_test() -> None:
    assert PORTUGUESE_TECHNICAL_TERMS.search("echo 'Auditoria falhou: evidência ausente.'")
    assert not PORTUGUESE_TECHNICAL_TERMS.search("echo 'Audit failed: evidence is missing.'")
    assert not PORTUGUESE_TECHNICAL_TERMS.search(normalized_diagnostic("echo 'Expected rendered heading: SUMÁRIO'"))
    assert RETIRED_PROFILE_IDS.search('"profile": "tccgraduacao"')
    assert not RETIRED_PROFILE_IDS.search('"profile": "undergraduate-capstone"')
    normative = json.loads('{"requirement":"A capa é elemento obrigatório."}')
    assert "obrigatório" in normative["requirement"]
    print("ENGINEERING-LANGUAGE-SELFTEST status=PASS cases=6")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enforce project-owned engineering language boundaries.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    errors = audit()
    if errors:
        print("Engineering language contract failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(f"Engineering language contract failed with {len(errors)} issue(s).")
    print("ENGINEERING-LANGUAGE-EVIDENCE status=PASS portuguese_technical_diagnostics=0 retired_profile_ids=0 closed_unconsumed_contracts=0 live_api_contract_consumers=2")


if __name__ == "__main__":
    main()

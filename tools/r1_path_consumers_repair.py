#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_NEGATIVE_GUARDS = {
    "tests/checks/canonical_identity.py",
    "tests/checks/repository_contract.py",
    "tests/checks/release_package.py",
    "tests/checks/ctan_archive.py",
}

EXACT_PATH_MAP = {
    "tests/normativa/appendix-annex-final-pdf.tex": "tests/documents/appendix-annex-final-pdf.tex",
    "tests/normativa/equation-display-final-pdf.tex": "tests/documents/equation-display-final-pdf.tex",
    "tests/normativa/illustration-final-pdf.tex": "tests/documents/illustration-final-pdf.tex",
    "tests/normativa/index-glossary-final-pdf.tex": "tests/documents/index-glossary-final-pdf.tex",
    "tests/normativa/index-glossary-absent-final-pdf.tex": "tests/documents/index-glossary-absent-final-pdf.tex",
    "tests/normativa/textual-oracle-pagination-geometry.tex": "tests/documents/mainmatter-pagination-geometry-test.tex",
    "tests/normativa/projeto-15287.tex": "tests/documents/research-project-15287.tex",
    "tests/normativa/table-ibge-vector-final-pdf.tex": "tests/documents/table-ibge-vector-final-pdf.tex",
    "tests/normativa/table-typography-final-pdf.tex": "tests/documents/table-typography-final-pdf.tex",
    "tests/normativa/vector-rule-oracle-calibration.tex": "tests/documents/vector-rule-calibration-test.tex",
    "normativa/catalog.json": "standards/catalog.json",
    "normativa/precedence.json": "standards/precedence.json",
    "normativa/vector-rule-oracle-extension.json": "standards/vector-rule-validation-extension.json",
    "tests/v2-capes-guidance-check.sh": "tests/integration/capes-guidance.sh",
    "tests/v2-catalog-card-check.sh": "tests/integration/catalog-card.sh",
    "tests/v2-font-config-check.sh": "tests/integration/font-config.sh",
    "tests/v2-font-poc.sh": "tests/integration/font-poc.sh",
    "tests/v2-font-embedding-check.sh": "tests/integration/font-embedding.sh",
    "tests/v2-pdf-geometry-check.sh": "tests/integration/pdf-geometry.sh",
    "tests/v2-pdfa-check.sh": "tests/integration/pdfa.sh",
    "tests/v2-profile-pdfa-check.sh": "tests/integration/profile-pdfa.sh",
    "tests/v2-profile-matrix-check.sh": "tests/integration/profile-matrix.sh",
    "tests/v2-canonical-identity-check.py": "tests/checks/canonical_identity.py",
    "tests/v2-ctan-policy-check.py": "tests/checks/ctan_policy.py",
    "tests/v2-ctan-archive-check.py": "tests/checks/ctan_archive.py",
    "tests/v2-release-package-check.py": "tests/checks/release_package.py",
    "tests/v2-overleaf-bundle-check.py": "tests/checks/overleaf_bundle.py",
    "tests/v2-release-metadata-check.py": "tests/checks/release_metadata.py",
    "tests/v2-repository-audit.py": "tests/checks/repository_contract.py",
    "tests/v2-reference-corpus-check.sh": "tests/integration/reference-corpus.sh",
    "tests/v2-algorithm-numbering-check.sh": "tests/integration/algorithm-numbering.sh",
    "tests/v2-overleaf-stable-check.sh": "tests/integration/overleaf-stable.sh",
}


def fail(message: str) -> None:
    raise SystemExit(f"R1 path-consumer repair failed: {message}")


def tracked_files() -> list[str]:
    return subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()


def validate_targets() -> None:
    missing = sorted({target for target in EXACT_PATH_MAP.values() if not (ROOT / target).is_file()})
    if missing:
        fail("mapped targets do not exist:\n" + "\n".join(missing))


def rewrite_exact_consumers() -> list[str]:
    changed: list[str] = []
    roots = ("standards/", "tests/", "tools/", "validator/")
    suffixes = {".json", ".py", ".sh", ".tex", ".js", ".html", ".css", ".md"}
    for relative in tracked_files():
        if relative in EXCLUDED_NEGATIVE_GUARDS or not relative.startswith(roots):
            continue
        path = ROOT / relative
        if path.suffix not in suffixes or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text
        for source, target in EXACT_PATH_MAP.items():
            text = text.replace(source, target)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(relative)
    return changed


def repair_font_poc() -> None:
    path = ROOT / "tests/integration/font-poc.sh"
    text = path.read_text(encoding="utf-8")
    old_root = 'root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)'
    new_root = 'root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)'
    if old_root not in text:
        fail("font-poc root expression did not match expected migrated form")
    text = text.replace(old_root, new_root, 1)
    old_fixture = 'fixture="tests/normativa/fontes-${family}-poc.tex"'
    new_fixture = 'fixture="tests/documents/${family}-font-poc.tex"'
    if old_fixture not in text:
        fail("font-poc fixture expression did not match expected legacy form")
    text = text.replace(old_fixture, new_fixture, 1)
    path.write_text(text, encoding="utf-8")


def repair_validator_source() -> None:
    path = ROOT / "tests/checks/validator_source.py"
    text = path.read_text(encoding="utf-8")
    replacements = {
        'PDF_ORACLE_CORE = ROOT / "tests" / "checks" / "pdf_oracle_core.py"': 'PDF_VALIDATION_CORE = ROOT / "tests" / "checks" / "pdf_validation_core.py"',
        'PRETEXTUAL_ORACLE = ROOT / "tests" / "checks" / "frontmatter_oracle.py"': 'FRONTMATTER_VALIDATION = ROOT / "tests" / "checks" / "frontmatter_validation.py"',
        'N14_VALIDATOR_CONTRACT = ROOT / "tests" / "checks" / "normative_n14_validator_contract.py"': 'VALIDATOR_CONTRACT = ROOT / "tests" / "checks" / "normative_validator_contract.py"',
        "        PDF_ORACLE_CORE,": "        PDF_VALIDATION_CORE,",
        "        PRETEXTUAL_ORACLE,": "        FRONTMATTER_VALIDATION,",
        "        N14_VALIDATOR_CONTRACT,": "        VALIDATOR_CONTRACT,",
        '    run_source_check(N14_VALIDATOR_CONTRACT, "N14 validator contract")': '    run_source_check(VALIDATOR_CONTRACT, "validator contract")',
    }
    for old, new in replacements.items():
        if old not in text:
            fail(f"validator-source expected block missing: {old}")
        text = text.replace(old, new, 1)

    removable_definitions = (
        'NORMATIVE_COVERAGE_AUDIT = ROOT / "tests" / "checks" / "normative_coverage_audit.py"\n',
        'NORMATIVE_RECONCILIATION = ROOT / "tests" / "checks" / "normative_reconciliation.py"\n',
        'N15_B2A_ARTICLE_CONTRACT = ROOT / "tests" / "checks" / "normative_n15_b2a_article_contract.py"\n',
    )
    for block in removable_definitions:
        if block not in text:
            fail(f"validator-source obsolete definition missing: {block.strip()}")
        text = text.replace(block, "", 1)

    removable_tuple_lines = (
        "        NORMATIVE_COVERAGE_AUDIT,\n",
        "        NORMATIVE_RECONCILIATION,\n",
        "        N15_B2A_ARTICLE_CONTRACT,\n",
    )
    for block in removable_tuple_lines:
        if block not in text:
            fail(f"validator-source obsolete tuple entry missing: {block.strip()}")
        text = text.replace(block, "", 1)

    removable_runs = (
        '    run_source_check(NORMATIVE_RECONCILIATION, "normative reconciliation")\n',
        '    run_source_check(N15_B2A_ARTICLE_CONTRACT, "N15-B2A article contract")\n',
    )
    for block in removable_runs:
        if block not in text:
            fail(f"validator-source obsolete execution missing: {block.strip()}")
        text = text.replace(block, "", 1)

    path.write_text(text, encoding="utf-8")


def rewrite_distribution_gate() -> None:
    path = ROOT / "tests/integration/distribution.sh"
    content = r'''#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$root"

python3 <<'PY'
from __future__ import annotations

import py_compile
import re
import subprocess
from pathlib import Path

root = Path.cwd()
required = (
    "abntexto-ufc.cls",
    "abntexto-ufc/fonts.def",
    "template/main.tex",
    "template/figures/LICENSES.md",
    "assets/institutional/ufc-coat-of-arms.png",
    "tools/build-release-bundles.py",
    "tests/checks/canonical_identity.py",
    "tests/checks/ctan_policy.py",
    "tests/checks/ctan_archive.py",
    "tests/checks/release_package.py",
    "tests/checks/overleaf_bundle.py",
    "tests/checks/release_metadata.py",
    "tests/checks/repository_contract.py",
    "tests/integration/reference-corpus.sh",
    "tests/integration/algorithm-numbering.sh",
    "docs/HANDOFF-V3.0.0.md",
)
missing = [item for item in required if not (root / item).is_file()]
if missing:
    raise SystemExit("Distribution source gate: required files missing:\n" + "\n".join(missing))

if (root / "ufctex.cls").exists():
    raise SystemExit("Distribution source gate: deprecated ufctex.cls is present")

source = (root / "abntexto-ufc.cls").read_text(encoding="utf-8")
modules = re.findall(r"\\input\{(abntexto-ufc/[^}]+\\.def)\}", source)
if not modules:
    raise SystemExit("Distribution source gate: canonical class loads no project modules")
if "abntexto-ufc/fonts.def" not in modules:
    raise SystemExit("Distribution source gate: fonts.def is not loaded by the canonical class")
missing_modules = [module for module in modules if not (root / module).is_file()]
if missing_modules:
    raise SystemExit("Distribution source gate: class modules missing:\n" + "\n".join(missing_modules))

builder = (root / "tools/build-release-bundles.py").read_text(encoding="utf-8")
if re.search(r"CLASS_INPUTS\s*=\s*\(.*?assets/institutional", builder, re.DOTALL):
    raise SystemExit("Distribution source gate: class bundle includes institutional assets")
if re.search(r"TEMPLATE_INPUTS\s*=\s*\(.*?[\"']assets[\"']", builder, re.DOTALL):
    raise SystemExit("Distribution source gate: public template inputs include institutional assets")

for checker in sorted((root / "tests/checks").glob("*.py")):
    py_compile.compile(str(checker), doraise=True)

for script in sorted((root / "tests/integration").glob("*.sh")):
    completed = subprocess.run(["sh", "-n", str(script)], check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Distribution source gate: invalid shell syntax: {script.relative_to(root)}")

print(
    "Distribution source integrity passed: canonical class, current modules, "
    "source inventory, Python checkers, and shell integration runners are coherent."
)
PY
'''
    path.write_text(content, encoding="utf-8")


def audit_operational_stale_paths() -> None:
    findings: list[str] = []
    roots = ("standards/", "tests/checks/", "tests/integration/", "tools/", "validator/")
    patterns = (
        re.compile(r"tests/normativa/"),
        re.compile(r"(?<![A-Za-z0-9_])normativa/"),
        re.compile(r"tests/v2-[A-Za-z0-9_.-]+"),
    )
    allowed_negative = EXCLUDED_NEGATIVE_GUARDS | {"tests/checks/overleaf_bundle.py"}
    for relative in tracked_files():
        if relative in allowed_negative or not relative.startswith(roots):
            continue
        path = ROOT / relative
        if not path.is_file() or path.suffix not in {".json", ".py", ".sh", ".tex", ".js", ".html", ".css", ".md"}:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            if any(pattern.search(line) for pattern in patterns):
                findings.append(f"{relative}:{lineno}: {line.strip()}")
    if findings:
        fail("operational stale paths remain:\n" + "\n".join(findings))


def main() -> None:
    validate_targets()
    changed = rewrite_exact_consumers()
    repair_font_poc()
    repair_validator_source()
    rewrite_distribution_gate()
    audit_operational_stale_paths()
    print(f"R1 path-consumer repair changed {len(changed)} exact-consumer files plus bounded runner repairs.")
    for relative in changed:
        print(relative)


if __name__ == "__main__":
    main()

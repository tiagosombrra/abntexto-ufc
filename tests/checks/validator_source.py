#!/usr/bin/env python3
from __future__ import annotations

import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "validate-ufc-pdf.py"
PDF_MEASUREMENT = ROOT / "tools" / "pdf_measurement.py"
PDF_VALIDATION_CORE = ROOT / "tests" / "checks" / "pdf_validation_core.py"
FRONTMATTER_EVIDENCE = ROOT / "tests" / "checks" / "frontmatter_evidence.py"
VALIDATOR_ROOT = ROOT / "validator"
APP = VALIDATOR_ROOT / "app.js"
INDEX = VALIDATOR_ROOT / "index.html"
WEB_CATALOG = VALIDATOR_ROOT / "normative-catalog.js"
ROOT_README = ROOT / "README.md"
SITE_INDEX = ROOT / "site" / "index.html"
PAGES_WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"
NORMATIVE_TOOL = ROOT / "tools" / "normative_catalog.py"
NORMATIVE_ATOMIC_TOOL = ROOT / "tools" / "normative_atomic.py"
NORMATIVE_FULL_TOOL = ROOT / "tools" / "normative_full.py"
NORMATIVE_COVERAGE = ROOT / "tests" / "checks" / "normative_coverage.py"
NORMATIVE_CURRENCY = ROOT / "tests" / "checks" / "normative_currency.py"
NORMATIVE_PRECEDENCE = ROOT / "tests" / "checks" / "normative_precedence.py"
NORMATIVE_FALSE_COVERAGE = ROOT / "tests" / "checks" / "normative_false_coverage.py"
NORMATIVE_SOURCES = ROOT / "tests" / "checks" / "normative_sources.py"
NORMATIVE_SOURCE_REFERENCES = ROOT / "tests" / "checks" / "normative_source_references.py"
NORMATIVE_LOCATORS = ROOT / "tests" / "checks" / "normative_locators.py"
NORMATIVE_TRACEABILITY = ROOT / "tests" / "checks" / "normative_traceability.py"
NORMATIVE_PROOF_STATE = ROOT / "tests" / "checks" / "normative_proof_state.py"
NORMATIVE_EVIDENCE_CONTRIBUTION = ROOT / "tests" / "checks" / "normative_evidence_contribution.py"
NORMATIVE_ATOMICITY = ROOT / "tests" / "checks" / "normative_atomicity.py"
NORMATIVE_ATOMIC_CONTRACT = ROOT / "tests" / "checks" / "normative_atomic_contract.py"
NORMATIVE_FULL_CONTRACT = ROOT / "tests" / "checks" / "normative_full_contract.py"
VALIDATOR_CONTRACT = ROOT / "tests" / "checks" / "normative_validator_contract.py"


def fail(message: str) -> None:
    raise SystemExit(f"Validator source check failed: {message}")


def run_source_check(path: Path, label: str, *args: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"{label}: {completed.stdout}{completed.stderr}")
    if completed.stdout:
        print(completed.stdout.strip())


def validate_readme_relative_links(readme: str) -> int:
    pattern = re.compile(r"\\[[^\\]]+\\]\\(([^)]+)\\)")
    links = 0
    root = ROOT.resolve()
    for raw_target in pattern.findall(readme):
        target = raw_target.strip().split()[0]
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        resolved = (ROOT / clean).resolve()
        if resolved != root and root not in resolved.parents:
            fail(f"README relative link escapes repository root: {target}")
        if not resolved.exists():
            fail(f"README relative link target is missing: {target}")
        links += 1
    if links == 0:
        fail("final README exposes no repository-relative documentation links to validate")
    return links


def validate_relative_module_closure() -> int:
    pattern = re.compile(r'(?:\bfrom\s*|\bimport\s*\()\s*["\'](\.[^"\']+)["\']')
    root = VALIDATOR_ROOT.resolve()
    imports = 0
    for source in sorted(VALIDATOR_ROOT.glob("*.js")):
        text = source.read_text(encoding="utf-8")
        for specifier in pattern.findall(text):
            clean = specifier.split("?", 1)[0].split("#", 1)[0]
            target = (source.parent / clean).resolve()
            if target != root and root not in target.parents:
                fail(f"relative browser import escapes validator tree: {source.name}: {specifier}")
            if not target.is_file():
                fail(f"relative browser import is missing: {source.name}: {specifier}")
            imports += 1
    if imports == 0:
        fail("Web/Lite static tree exposes no local relative module import to validate")
    if '<script type="module" src="app.js"></script>' not in INDEX.read_text(encoding="utf-8"):
        fail("Web/Lite entry HTML does not load the tracked app.js module")
    return imports


def main() -> None:
    for path in (
        CLI,
        PDF_MEASUREMENT,
        PDF_VALIDATION_CORE,
        FRONTMATTER_EVIDENCE,
        NORMATIVE_TOOL,
        NORMATIVE_ATOMIC_TOOL,
        NORMATIVE_FULL_TOOL,
        NORMATIVE_COVERAGE,
        NORMATIVE_CURRENCY,
        NORMATIVE_PRECEDENCE,
        NORMATIVE_FALSE_COVERAGE,
        NORMATIVE_SOURCES,
        NORMATIVE_SOURCE_REFERENCES,
        NORMATIVE_LOCATORS,
        NORMATIVE_TRACEABILITY,
        NORMATIVE_PROOF_STATE,
        NORMATIVE_EVIDENCE_CONTRIBUTION,
        NORMATIVE_ATOMICITY,
        NORMATIVE_ATOMIC_CONTRACT,
        NORMATIVE_FULL_CONTRACT,
        VALIDATOR_CONTRACT,
    ):
        py_compile.compile(str(path), doraise=True)

    run_source_check(NORMATIVE_TOOL, "normative catalog")
    run_source_check(NORMATIVE_PRECEDENCE, "normative precedence")
    run_source_check(NORMATIVE_SOURCES, "normative sources")
    run_source_check(NORMATIVE_SOURCE_REFERENCES, "normative source references")
    run_source_check(NORMATIVE_LOCATORS, "normative locators")
    run_source_check(NORMATIVE_CURRENCY, "normative currency")
    run_source_check(NORMATIVE_FALSE_COVERAGE, "normative false coverage")
    run_source_check(NORMATIVE_ATOMICITY, "normative atomicity")
    run_source_check(NORMATIVE_ATOMIC_CONTRACT, "normative atomic contract")
    run_source_check(NORMATIVE_FULL_TOOL, "full normative loader")
    run_source_check(NORMATIVE_FULL_CONTRACT, "full normative contract")
    run_source_check(NORMATIVE_COVERAGE, "normative coverage")
    run_source_check(NORMATIVE_TRACEABILITY, "normative traceability", "--strict-evidence")
    run_source_check(NORMATIVE_PROOF_STATE, "normative proof state")
    run_source_check(NORMATIVE_EVIDENCE_CONTRIBUTION, "normative evidence contribution", "--static")
    run_source_check(VALIDATOR_CONTRACT, "validator contract")

    completed = subprocess.run(
        [sys.executable, str(CLI), "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail("CLI cannot load the normative catalog")

    app = APP.read_text(encoding="utf-8")
    cli = CLI.read_text(encoding="utf-8")
    html = INDEX.read_text(encoding="utf-8")
    readme = ROOT_README.read_text(encoding="utf-8")
    site = SITE_INDEX.read_text(encoding="utf-8")
    pages_workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")

    if "pdfjs-dist@6.2.108" not in app:
        fail("PDF.js version is not pinned to 6.2.108")
    if 'from "./normative-catalog.js"' not in app:
        fail("Web/Lite does not consume the generated normative catalog")
    if "from normative_catalog import" not in cli:
        fail("CLI does not consume the normative catalog")
    if "A4=(595.276,841.89)" in cli or "A4=[595.276,841.89]" in app:
        fail("validator geometry is hard-coded instead of catalog-driven")

    forbidden = r"FormData\(|XMLHttpRequest|sendBeacon\(|WebSocket\(|\bfetch\s*\("
    if re.search(forbidden, app):
        fail("browser code contains a network upload API")

    if "is not sent to a server" not in html:
        fail("local-processing disclosure is missing")
    for marker in ('id="normative-base"', 'id="norm-reviewed"', 'id="norm-sources"'):
        if marker not in html:
            fail(f"normative-base UI marker is missing: {marker}")

    readme_markers = (
        "https://tiagosombrra.github.io/abntexto-ufc/",
        "https://tiagosombrra.github.io/abntexto-ufc/validator/",
        "https://github.com/tiagosombrra/abntexto-ufc/releases",
        "abntexto-ufc-template-<versão>.zip",
        "abntexto-ufc-overleaf-<versão>.zip",
        "abntexto-ufc-<versão>.zip",
        "## Estrutura do repositório",
        "## Validação",
    )
    for marker in readme_markers:
        if marker not in readme:
            fail(f"final README delivery marker is missing: {marker}")

    for marker in (
        'href="./validator/"',
        "https://github.com/tiagosombrra/abntexto-ufc/releases",
        "https://github.com/tiagosombrra/abntexto-ufc",
    ):
        if marker not in site:
            fail(f"project landing page marker is missing: {marker}")

    pages_markers = (
        "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803",
        "actions/configure-pages@45bfe0192ca1faeb007ade9deae92b16b8254a0d",
        "actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b",
        "actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e",
        "cp -a validator/. _site/validator/",
        "name: github-pages",
        "steps.deployment.outputs.page_url",
    )
    for marker in pages_markers:
        if marker not in pages_workflow:
            fail(f"GitHub Pages publication contract marker is missing: {marker}")
    if "enablement: true" in pages_workflow:
        fail("Pages workflow must not pretend GITHUB_TOKEN can enable repository Pages settings")

    node = shutil.which("node")
    if not node:
        fail("Node.js is required for JavaScript syntax validation")

    for source in (APP, WEB_CATALOG):
        completed = subprocess.run([node, "--check", str(source)], check=False)
        if completed.returncode != 0:
            fail(f"{source.relative_to(ROOT)} has invalid JavaScript syntax")

    readme_relative_links = validate_readme_relative_links(readme)
    relative_imports = validate_relative_module_closure()

    with tempfile.TemporaryDirectory() as temp_dir:
        module = Path(temp_dir) / "normative-catalog.js"
        completed = subprocess.run(
            [sys.executable, str(NORMATIVE_TOOL), "--emit-web", str(module)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            fail("normative web catalog generation failed")
        completed = subprocess.run([node, "--check", str(module)], check=False)
        if completed.returncode != 0:
            fail("generated normative web catalog has invalid JavaScript syntax")
        if module.read_bytes() != WEB_CATALOG.read_bytes():
            fail(
                "tracked validator/normative-catalog.js is stale; regenerate it with "
                "python3 tools/normative_catalog.py --emit-web validator/normative-catalog.js"
            )

    print(
        "VALIDATION-EVIDENCE web-static-package status=PASS "
        f"relative_imports={relative_imports} readme_relative_links={readme_relative_links} "
        "generated_catalog_identical=true entry=index.html local_processing=true "
        "readme_delivery=true pages_contract=true"
    )
    print("Validator sources and normative contracts validated.")


if __name__ == "__main__":
    main()

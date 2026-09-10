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
APP = ROOT / "validator" / "app.js"
INDEX = ROOT / "validator" / "index.html"
VALIDATOR_SITE_BUILDER = ROOT / "tools" / "build-validator-site.py"
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


def check_generated_site(node: str) -> None:
    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-validator-site-") as temp_dir:
        output = Path(temp_dir) / "site"
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_SITE_BUILDER), "--output", str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            fail(f"complete Web/Lite site build failed: {completed.stdout}{completed.stderr}")
        if completed.stdout:
            print(completed.stdout.strip())

        expected = {
            "index.html",
            "app.js",
            "validation-contract.json",
            "normative-catalog.js",
            "build-manifest.json",
        }
        actual = {path.name for path in output.iterdir() if path.is_file()}
        if actual != expected:
            fail(f"generated Web/Lite inventory drift: {sorted(actual ^ expected)}")

        built_html = (output / "index.html").read_text(encoding="utf-8")
        if 'src="app.js"' not in built_html:
            fail("generated index.html does not load app.js")

        for javascript in (output / "app.js", output / "normative-catalog.js"):
            completed = subprocess.run([node, "--check", str(javascript)], check=False)
            if completed.returncode != 0:
                fail(f"generated JavaScript has invalid syntax: {javascript.name}")

        local_imports: set[str] = set()
        for javascript in output.glob("*.js"):
            text = javascript.read_text(encoding="utf-8")
            local_imports.update(
                match.group(1)
                for match in re.finditer(r"\bfrom\s+[\"'](\./[^\"']+)[\"']", text)
            )
            local_imports.update(
                match.group(1)
                for match in re.finditer(r"\bimport\s+[\"'](\./[^\"']+)[\"']", text)
            )
        missing = sorted(
            relative
            for relative in local_imports
            if not (output / relative.removeprefix("./")).is_file()
        )
        if missing:
            fail("generated Web/Lite site has unresolved relative imports: " + ", ".join(missing))
        if "./normative-catalog.js" not in local_imports:
            fail("generated Web/Lite module graph does not include normative-catalog.js")

        manifest = (output / "build-manifest.json").read_text(encoding="utf-8")
        if '"pdf_processing": "local-browser"' not in manifest:
            fail("generated Web/Lite manifest lost local-processing contract")


def main() -> None:
    for path in (
        CLI,
        PDF_MEASUREMENT,
        PDF_VALIDATION_CORE,
        FRONTMATTER_EVIDENCE,
        VALIDATOR_SITE_BUILDER,
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
    html_source = INDEX.read_text(encoding="utf-8")

    if "pdfjs-dist@6.2.108" not in app:
        fail("PDF.js version is not pinned to 6.2.108")
    if 'from "./normative-catalog.js"' not in app:
        fail("Web/Lite does not consume the generated normative catalog")
    if "__ABNTEXTO_UFC_WEB_LITE__" not in app or "Object.freeze({analyze})" not in app:
        fail("production Web/Lite analyze function is not exposed for real browser E2E")
    if "from normative_catalog import" not in cli:
        fail("CLI does not consume the normative catalog")
    if "A4=(595.276,841.89)" in cli or "A4=[595.276,841.89]" in app:
        fail("validator geometry is hard-coded instead of catalog-driven")

    forbidden = r"FormData\(|XMLHttpRequest|sendBeacon\(|WebSocket\(|\bfetch\s*\("
    if re.search(forbidden, app):
        fail("browser production code contains a network upload API")

    if "is not sent to a server" not in html_source:
        fail("local-processing disclosure is missing")
    for marker in ('id="normative-base"', 'id="norm-reviewed"', 'id="norm-sources"'):
        if marker not in html_source:
            fail(f"normative-base UI marker is missing: {marker}")

    node = shutil.which("node")
    if not node:
        fail("Node.js is required for JavaScript syntax validation")

    completed = subprocess.run([node, "--check", str(APP)], check=False)
    if completed.returncode != 0:
        fail("validator/app.js has invalid JavaScript syntax")

    with tempfile.TemporaryDirectory() as temp_dir:
        module = Path(temp_dir) / "normative-catalog.mjs"
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

    check_generated_site(node)
    print("Validator sources, generated Web/Lite site, and normative contracts validated.")


if __name__ == "__main__":
    main()

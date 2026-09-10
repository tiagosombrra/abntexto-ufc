#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "validator"
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from normative_catalog import emit_web_module, load_catalog  # noqa: E402

PACKAGE_ID = "abntexto-ufc"
PUBLIC_SOURCE_FILES = (
    "index.html",
    "app.js",
    "validation-contract.json",
)
GENERATED_CATALOG = "normative-catalog.js"
MANIFEST = "build-manifest.json"


def fail(message: str) -> None:
    raise SystemExit(f"Validator site build failed: {message}")


def safe_output(path: Path) -> Path:
    resolved = path.resolve()
    if resolved == VALIDATOR.resolve() or VALIDATOR.resolve() in resolved.parents:
        fail("output must not replace or live inside validator source directory")
    if resolved == ROOT.resolve():
        fail("output must not be the repository root")
    return resolved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a complete deterministic static Web/Lite validator site."
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "validator")
    args = parser.parse_args()

    output = safe_output(args.output)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    for name in PUBLIC_SOURCE_FILES:
        source = VALIDATOR / name
        if not source.is_file():
            fail(f"required source file is missing: validator/{name}")
        shutil.copyfile(source, output / name)

    catalog = load_catalog()
    emit_web_module(catalog, output / GENERATED_CATALOG)

    manifest = {
        "schema_version": 1,
        "site": "web-lite",
        "source_directory": "validator",
        "source_files": list(PUBLIC_SOURCE_FILES),
        "generated_files": [GENERATED_CATALOG],
        "normative_catalog": {
            "schema_version": catalog["schema_version"],
            "reviewed_at": catalog["reviewed_at"],
        },
        "pdfjs": "6.2.108",
        "pdf_processing": "local-browser",
    }
    (output / MANIFEST).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    expected = {*PUBLIC_SOURCE_FILES, GENERATED_CATALOG, MANIFEST}
    actual = {path.name for path in output.iterdir() if path.is_file()}
    if actual != expected:
        fail(f"unexpected static site inventory: {sorted(actual ^ expected)}")

    print(
        "WEB-LITE-BUILD-EVIDENCE status=PASS "
        f"files={len(actual)} normative_reviewed_at={catalog['reviewed_at']} "
        "local_module=normative-catalog.js pdfjs=6.2.108"
    )
    print(output)


if __name__ == "__main__":
    main()

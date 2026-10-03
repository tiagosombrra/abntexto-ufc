#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
ROOT = TESTS_DIR.parent

LICENSE_BLOB_SHA1 = "842cf85e3ce5e5ffaf7ffb24f73f9f15ef9e82c6"
MAINTAINER = "Tiago Guimarães Sombra"
CTAN_WORK = (
    "README.md",
    "CHANGELOG",
    "LICENSE",
    "abntexto-ufc.cls",
    "abntexto-ufc.tex",
    "abntexto-ufc.pdf",
    "abntexto-ufc-example.tex",
    "abntexto-ufc-example.pdf",
)


def fail(message: str) -> None:
    raise SystemExit(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def git_blob(path: str) -> str:
    completed = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.strip() or f"git hash-object failed: {path}")
    return completed.stdout.strip()


def ctan_work_entries(readme: str) -> tuple[str, ...]:
    marker = "## LPPL maintenance and Work identity"
    if marker not in readme:
        fail("CTAN README is missing the LPPL maintenance/Work section")
    section = readme.split(marker, 1)[1]
    entries: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- `") and stripped.endswith("`"):
            entries.append(stripped[3:-1])
    return tuple(entries)


def main() -> None:
    if git_blob("LICENSE") != LICENSE_BLOB_SHA1:
        fail("standard LPPL LICENSE bytes changed")

    citation = read("CITATION.cff")
    if 'license: "LPPL-1.3c"' not in citation:
        fail("CITATION.cff must retain LPPL-1.3c")

    root_readme = read("README.md")
    required_root = (
        "Status de manutenção LPPL: `maintained`.",
        f"O **Current Maintainer** é **{MAINTAINER}**.",
        "release/ctan/README.md",
        "PDF.js vendorizado mantém sua licença Apache-2.0",
    )
    for token in required_root:
        if token not in root_readme:
            fail(f"root README LPPL identity missing: {token}")

    class_text = read("abntexto-ufc.cls")
    required_class = (
        "% Distributed under LPPL 1.3c or later; see LICENSE.",
        "% LPPL maintenance status: maintained.",
        f"% Current Maintainer: {MAINTAINER}.",
        "% CTAN Work identity: release/ctan/README.md.",
    )
    for token in required_class:
        if token not in class_text:
            fail(f"class LPPL identity missing: {token}")

    ctan_readme = read("release/ctan/README.md")
    required_ctan = (
        f"Current Maintainer: {MAINTAINER}",
        "LPPL maintenance status: maintained",
        "The LPPL maintenance status is `maintained`.",
    )
    for token in required_ctan:
        if token not in ctan_readme:
            fail(f"CTAN README LPPL identity missing: {token}")

    entries = ctan_work_entries(ctan_readme)
    if entries != CTAN_WORK:
        fail(
            "CTAN Work identity drift: "
            f"expected={','.join(CTAN_WORK)} actual={','.join(entries)}"
        )

    manual = read("release/ctan/abntexto-ufc.tex")
    required_manual = (
        "The LPPL maintenance status is \\texttt{maintained}.",
        f"The Current Maintainer is {MAINTAINER}.",
    )
    for token in required_manual:
        if token not in manual:
            fail(f"CTAN manual LPPL identity missing: {token}")
    for filename in CTAN_WORK:
        if f"\\texttt{{{filename}}}" not in manual:
            fail(f"CTAN manual Work identity missing: {filename}")

    institutional = read("assets/institutional/README.md")
    if "not covered by the project's LPPL license" not in institutional:
        fail("institutional asset LPPL exclusion is missing")

    provenance = json.loads(read("validator/vendor/pdfjs/PROVENANCE.json"))
    if provenance.get("license") != "Apache-2.0":
        fail("PDF.js provenance must retain Apache-2.0 license identity")

    print(
        "LPPL-MAINTENANCE-EVIDENCE status=PASS "
        f"license_blob={LICENSE_BLOB_SHA1} maintenance_status=maintained "
        f"current_maintainer={MAINTAINER.replace(' ', '_')} "
        f"ctan_work_files={len(CTAN_WORK)} institutional_asset=excluded "
        "pdfjs_license=Apache-2.0"
    )


if __name__ == "__main__":
    main()

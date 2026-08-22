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
APP = ROOT / "validator" / "app.js"
INDEX = ROOT / "validator" / "index.html"
NORMATIVE_TOOL = ROOT / "tools" / "normative_catalog.py"


def fail(message: str) -> None:
    raise SystemExit(f"Validator source check failed: {message}")


def main() -> None:
    py_compile.compile(str(CLI), doraise=True)
    py_compile.compile(str(NORMATIVE_TOOL), doraise=True)

    completed = subprocess.run(
        [sys.executable, str(NORMATIVE_TOOL)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stdout + completed.stderr)

    app = APP.read_text(encoding="utf-8")
    html = INDEX.read_text(encoding="utf-8")

    if "pdfjs-dist@6.2.108" not in app:
        fail("PDF.js version is not pinned to 6.2.108")

    forbidden = r"FormData\(|XMLHttpRequest|sendBeacon\(|WebSocket\("
    if re.search(forbidden, app):
        fail("browser code contains a network upload API")

    if "não é enviado para servidor" not in html:
        fail("local-processing disclosure is missing")

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

    print("Validator sources and normative catalog validated.")


if __name__ == "__main__":
    main()

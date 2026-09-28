#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from path_resolver import ROOT  # noqa: E402

WORKFLOW = ROOT / ".github" / "workflows" / "macos-smoke.yml"


def fail(message: str) -> None:
    raise SystemExit(f"macOS portability contract failed: {message}")


def main() -> None:
    if not WORKFLOW.is_file():
        fail("macos-smoke.yml is missing")

    text = WORKFLOW.read_text(encoding="utf-8")
    required = {
        "explicit macOS 26 ARM runner": "runs-on: macos-26",
        "pinned TeX Live setup action": "zauguin/install-texlive@6671d0c62046c7e349fe154d5208fe746b07e037",
        "pinned TeX Live version": "texlive_version: '2026'",
        "Latin Modern package": "\n            lm\n",
        "tabularray base package": "\n            tabularray\n",
        "varwidth dependency": "\n            varwidth\n",
        "Darwin assertion": "test \"$(uname -s)\" = 'Darwin'",
        "ARM64 assertion": "test \"$(uname -m)\" = 'arm64'",
        "pinned abntexto materialization": "tools/fetch-abntexto.py --output abntexto.cls",
        "public tutorial pdfLaTeX compile": "make DOCUMENT=main ENGINE=pdflatex compile",
        "public tutorial LuaLaTeX compile": "make DOCUMENT=main ENGINE=lualatex compile",
        "two-PDF artifact upload": "macos-template-pdfs-${{ github.run_id }}",
        "dependent Linux certification job": "needs: macos-build",
        "artifact download": "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
        "existing font embedding gate": "tests/integration/layout/font-embedding.sh",
        "existing PDF/A gate": "tests/integration/layout/pdfa.sh",
        "bounded evidence marker": "MACOS-PORTABILITY-EVIDENCE status=PASS",
    }
    missing = [label for label, token in required.items() if token not in text]
    if missing:
        fail("missing required workflow controls: " + ", ".join(missing))

    forbidden = {
        "floating macOS runner": "runs-on: macos-latest",
        "Intel-only runner": "macos-26-intel",
        "retired Latin Modern package token": "\n            lmodern\n",
        "best-effort portability bypass": "continue-on-error: true",
    }
    present = [label for label, token in forbidden.items() if token in text]
    if present:
        fail("forbidden workflow controls present: " + ", ".join(present))

    if text.count("runs-on: macos-26") != 1:
        fail("expected exactly one macOS ARM64 build job")
    if text.count("runs-on: ubuntu-24.04") != 1:
        fail("expected exactly one Linux certification job")

    print(
        "MACOS-PORTABILITY-CONTRACT-EVIDENCE status=PASS "
        "runner=macos-26 arch=arm64 texlive=2026 public_template=main "
        "engines=2 artifact_transfer=required linux_certification=required"
    )


if __name__ == "__main__":
    main()

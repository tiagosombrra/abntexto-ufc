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

WORKFLOW = ROOT / ".github" / "workflows" / "windows-smoke.yml"


def fail(message: str) -> None:
    raise SystemExit(f"Windows portability contract failed: {message}")


def main() -> None:
    if not WORKFLOW.is_file():
        fail("windows-smoke.yml is missing")

    text = WORKFLOW.read_text(encoding="utf-8")
    required = {
        "explicit Windows Server 2025 runner": "runs-on: windows-2025",
        "pinned TeX Live setup action": "zauguin/install-texlive@6671d0c62046c7e349fe154d5208fe746b07e037",
        "pinned TeX Live version": "texlive_version: '2026'",
        "virtual-font utilities package": "\n            fontware\n",
        "Brazilian Portuguese Babel package": "\n            babel-portuges\n",
        "pinned abntexto materialization": "tools/fetch-abntexto.py --output abntexto.cls",
        "Windows font preparation pipeline": "tools/prepare-windows-fonts.ps1",
        "compile-only font proof": "UFC_FONT_POC_COMPILE_ONLY: '1'",
        "existing font POC": "tests/integration/layout/font-poc.sh",
        "strict PDF artifact upload": "windows-font-pdfs-${{ github.run_id }}",
        "dependent Linux certification job": "needs: windows-build",
        "artifact download": "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
        "existing Windows PDF certification gate": "tests/integration/layout/windows-font-pdfa.sh",
        "bounded evidence marker": "WINDOWS-PORTABILITY-EVIDENCE status=PASS",
        "TeX Live evidence identity": "texlive=2026",
    }
    missing = [label for label, token in required.items() if token not in text]
    if missing:
        fail("missing required workflow controls: " + ", ".join(missing))

    forbidden = {
        "floating Windows runner": "runs-on: windows-latest",
        "best-effort portability bypass": "continue-on-error: true",
        "stale MiKTeX evidence marker": "miktex=",
    }
    present = [label for label, token in forbidden.items() if token in text]
    if present:
        fail("forbidden workflow controls present: " + ", ".join(present))

    if text.count("runs-on: windows-2025") != 1:
        fail("expected exactly one Windows build job")
    if text.count("runs-on: ubuntu-24.04") != 1:
        fail("expected exactly one Linux certification job")

    print(
        "WINDOWS-PORTABILITY-CONTRACT-EVIDENCE status=PASS "
        "runner=windows-2025 texlive=2026 windows_build=required "
        "artifact_transfer=required linux_certification=required"
    )


if __name__ == "__main__":
    main()

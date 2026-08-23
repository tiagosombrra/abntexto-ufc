#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def version() -> str:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit("Makefile VERSION not found.")
    return match.group(1)


def safe_extract(archive_path: Path, destination: Path) -> None:
    root = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if target != root and root not in target.parents:
                raise SystemExit(f"Unsafe Overleaf bundle path: {member.filename}")
        archive.extractall(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the generated Overleaf import bundle.")
    parser.add_argument("--bundle", type=Path)
    args = parser.parse_args()

    v = version()
    bundle = args.bundle or ROOT / "dist" / f"modelo-latex-ufc-overleaf-{v}.zip"
    bundle = bundle.resolve()
    if not bundle.is_file():
        raise SystemExit(f"Overleaf bundle not found: {bundle}")

    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-overleaf-bundle-") as temp:
        project = Path(temp)
        safe_extract(bundle, project)

        wrapped_root = project / f"modelo-latex-ufc-overleaf-{v}"
        if wrapped_root.exists():
            raise SystemExit("Overleaf bundle must place documento.tex at the archive root.")

        required = (
            project / "documento.tex",
            project / "abntexto-ufc.cls",
            project / "abntexto-ufc" / "core.def",
            project / "ufctex.cls",
            project / "abntexto.cls",
            project / "1-pre-textuais" / "resumo.tex",
            project / "3-pos-textuais" / "referencias.bib",
        )
        missing = [str(path.relative_to(project)) for path in required if not path.is_file()]
        if missing:
            raise SystemExit(f"Overleaf bundle missing files: {', '.join(missing)}")

        harness = (
            ("tests/v2-overleaf-stable-check.sh", "tests/v2-overleaf-stable-check.sh"),
            ("tests/v2-font-embedding-check.sh", "tests/v2-font-embedding-check.sh"),
            ("tests/fixtures/overleaf-latexmkrc", "tests/fixtures/overleaf-latexmkrc"),
        )
        for source_name, target_name in harness:
            source = ROOT / source_name
            target = project / target_name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        subprocess.check_call(["sh", "tests/v2-overleaf-stable-check.sh"], cwd=project)

    print("Overleaf release bundle proxy check completed.")


if __name__ == "__main__":
    main()

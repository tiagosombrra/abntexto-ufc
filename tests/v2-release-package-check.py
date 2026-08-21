#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

MICROSOFT_FONTS = {
    "times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf",
    "arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf",
}

REFERENCE_IMAGE_SHA1 = {
    "figuras/ufc-campus-pici.jpg": "5f431612cdbfbb088c37c685a0e3c93852e96ccd",
    "figuras/ufc-reitoria.jpg": "b6746bb53d82dae52330805ca0a08f029b773b2e",
}


def version() -> str:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit("Makefile VERSION not found.")
    return match.group(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def names(path: Path) -> set[str]:
    with zipfile.ZipFile(path) as archive:
        return set(archive.namelist())


def assert_no_proprietary_fonts(entries: set[str]) -> None:
    found = sorted(entry for entry in entries if Path(entry).name.lower() in MICROSOFT_FONTS)
    if found:
        raise SystemExit(f"Proprietary Microsoft fonts found in release archive: {found}")


def assert_prefix(entries: set[str], prefix: str) -> None:
    invalid = sorted(entry for entry in entries if not entry.startswith(prefix))
    if invalid:
        raise SystemExit(f"Archive entries outside {prefix}: {invalid[:5]}")


def assert_reference_images(archive_path: Path, root: str) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        archive_names = set(archive.namelist())
        for relative, expected in REFERENCE_IMAGE_SHA1.items():
            entry = f"{root}{relative}"
            if entry not in archive_names:
                raise SystemExit(f"Release archive missing licensed reference image: {entry}")
            actual = hashlib.sha1(archive.read(entry)).hexdigest()
            if actual != expected:
                raise SystemExit(f"Reference image SHA-1 mismatch in {entry}: {actual}")


def verify_checksums(directory: Path) -> None:
    checksum_file = directory / "SHA256SUMS"
    listed = {}
    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        digest, filename = line.split("  ", 1)
        listed[filename] = digest
    expected_files = sorted(path.name for path in directory.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if sorted(listed) != expected_files:
        raise SystemExit("SHA256SUMS does not list exactly the release artifacts.")
    for filename, digest in listed.items():
        if sha256(directory / filename) != digest:
            raise SystemExit(f"SHA256SUMS mismatch for {filename}.")


def build(output: Path, abntexto: Path) -> None:
    subprocess.check_call([
        PYTHON,
        str(ROOT / "tools/build-release-bundles.py"),
        "--output",
        str(output),
        "--reference-pdf",
        str(ROOT / "documento.pdf"),
        "--abntexto",
        str(abntexto),
    ], cwd=ROOT)


def main() -> None:
    if not (ROOT / "documento.pdf").is_file():
        raise SystemExit("documento.pdf missing; run make release-preflight first.")

    for relative, expected in REFERENCE_IMAGE_SHA1.items():
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"Licensed reference image missing before packaging: {relative}")
        actual = hashlib.sha1(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"Licensed reference image SHA-1 mismatch: {relative}")

    v = version()
    with tempfile.TemporaryDirectory(prefix="ufctex-release-check-") as temp:
        temp_path = Path(temp)
        abntexto = temp_path / "abntexto.cls"
        subprocess.check_call([
            PYTHON,
            str(ROOT / "tools/fetch-abntexto.py"),
            "--output",
            str(abntexto),
        ], cwd=ROOT)

        first = temp_path / "first"
        second = temp_path / "second"
        build(first, abntexto)
        build(second, abntexto)

        first_files = sorted(path.name for path in first.iterdir() if path.is_file())
        second_files = sorted(path.name for path in second.iterdir() if path.is_file())
        if first_files != second_files:
            raise SystemExit("Release bundle file sets differ between deterministic builds.")
        for filename in first_files:
            if sha256(first / filename) != sha256(second / filename):
                raise SystemExit(f"Release artifact is not reproducible: {filename}")

        required = {
            f"ufctex-{v}.zip",
            f"modelo-latex-ufc-{v}.zip",
            f"modelo-latex-ufc-overleaf-{v}.zip",
            f"ufctex-ctan-{v}.zip",
            f"ufctex-{v}-reference.pdf",
            "SHA256SUMS",
        }
        if set(first_files) != required:
            raise SystemExit(f"Unexpected release artifacts: {sorted(set(first_files) ^ required)}")

        class_zip = first / f"ufctex-{v}.zip"
        class_entries = names(class_zip)
        class_root = f"ufctex-{v}/"
        assert_prefix(class_entries, class_root)
        for required_entry in (
            f"{class_root}ufctex.cls",
            f"{class_root}ufctex/core.def",
            f"{class_root}assets/institucional/brasao-ufc.PNG",
            f"{class_root}tools/prepare-windows-fonts.ps1",
            f"{class_root}README.md",
            f"{class_root}LICENSE",
        ):
            if required_entry not in class_entries:
                raise SystemExit(f"Class bundle missing {required_entry}")
        if any(entry.startswith(f"{class_root}1-pre-textuais/") for entry in class_entries):
            raise SystemExit("Class bundle unexpectedly contains template content.")
        assert_no_proprietary_fonts(class_entries)

        template_zip = first / f"modelo-latex-ufc-{v}.zip"
        template_entries = names(template_zip)
        template_root = f"modelo-latex-ufc-{v}/"
        assert_prefix(template_entries, template_root)
        for required_entry in (
            f"{template_root}documento.tex",
            f"{template_root}1-pre-textuais/resumo.tex",
            f"{template_root}2-textuais/1-introducao.tex",
            f"{template_root}2-textuais/exemplos-de-formatacao.tex",
            f"{template_root}3-pos-textuais/referencias.bib",
            f"{template_root}figuras/exemplo.py",
            f"{template_root}figuras/fluxo-exemplo.png",
            f"{template_root}figuras/grafico-exemplo.jpg",
            f"{template_root}figuras/LICENCAS.md",
            f"{template_root}figuras/ufc-campus-pici.jpg",
            f"{template_root}figuras/ufc-reitoria.jpg",
            f"{template_root}ufctex.cls",
            f"{template_root}Makefile",
        ):
            if required_entry not in template_entries:
                raise SystemExit(f"Template bundle missing {required_entry}")
        if f"{template_root}abntexto.cls" in template_entries:
            raise SystemExit("Standard template bundle must not vendor abntexto.cls.")
        assert_reference_images(template_zip, template_root)
        assert_no_proprietary_fonts(template_entries)

        overleaf_zip = first / f"modelo-latex-ufc-overleaf-{v}.zip"
        overleaf_entries = names(overleaf_zip)
        wrapped_root = f"modelo-latex-ufc-overleaf-{v}/"
        if any(entry.startswith(wrapped_root) for entry in overleaf_entries):
            raise SystemExit("Overleaf bundle must place the main document at the archive root.")
        for required_entry in (
            "documento.tex",
            "ufctex.cls",
            "abntexto.cls",
            "1-pre-textuais/resumo.tex",
            "3-pos-textuais/referencias.bib",
            "2-textuais/exemplos-de-formatacao.tex",
            "figuras/fluxo-exemplo.png",
            "figuras/grafico-exemplo.jpg",
            "figuras/LICENCAS.md",
            "figuras/ufc-campus-pici.jpg",
            "figuras/ufc-reitoria.jpg",
        ):
            if required_entry not in overleaf_entries:
                raise SystemExit(f"Overleaf bundle missing {required_entry}")
        assert_reference_images(overleaf_zip, "")
        assert_no_proprietary_fonts(overleaf_entries)

        ctan_zip = first / f"ufctex-ctan-{v}.zip"
        ctan_entries = names(ctan_zip)
        assert_prefix(ctan_entries, "ufctex/")
        for required_entry in (
            "ufctex/README.md",
            "ufctex/CHANGELOG.md",
            "ufctex/LICENSE",
            "ufctex/tex/ufctex.cls",
            "ufctex/tex/ufctex/core.def",
            f"ufctex/doc/ufctex-{v}-reference.pdf",
            "ufctex/doc/example/documento.tex",
            "ufctex/doc/example/2-textuais/exemplos-de-formatacao.tex",
            "ufctex/doc/example/figuras/fluxo-exemplo.png",
            "ufctex/doc/example/figuras/grafico-exemplo.jpg",
            "ufctex/doc/example/figuras/LICENCAS.md",
            "ufctex/doc/example/figuras/ufc-campus-pici.jpg",
            "ufctex/doc/example/figuras/ufc-reitoria.jpg",
            "ufctex/ufctex.tds.zip",
        ):
            if required_entry not in ctan_entries:
                raise SystemExit(f"CTAN bundle missing {required_entry}")
        assert_reference_images(ctan_zip, "ufctex/doc/example/")
        assert_no_proprietary_fonts(ctan_entries)

        with zipfile.ZipFile(ctan_zip) as archive:
            tds_bytes = archive.read("ufctex/ufctex.tds.zip")
        with zipfile.ZipFile(io.BytesIO(tds_bytes)) as tds:
            tds_entries = set(tds.namelist())
            for relative, expected in REFERENCE_IMAGE_SHA1.items():
                entry = f"doc/latex/ufctex/example/{relative}"
                if entry not in tds_entries:
                    raise SystemExit(f"TDS bundle missing {entry}")
                actual = hashlib.sha1(tds.read(entry)).hexdigest()
                if actual != expected:
                    raise SystemExit(f"TDS reference image SHA-1 mismatch in {entry}: {actual}")
        for required_entry in (
            "tex/latex/ufctex/ufctex.cls",
            "tex/latex/ufctex/ufctex/core.def",
            "doc/latex/ufctex/README.md",
            "doc/latex/ufctex/CHANGELOG.md",
            f"doc/latex/ufctex/ufctex-{v}-reference.pdf",
            "doc/latex/ufctex/example/2-textuais/exemplos-de-formatacao.tex",
            "doc/latex/ufctex/example/figuras/fluxo-exemplo.png",
            "doc/latex/ufctex/example/figuras/grafico-exemplo.jpg",
            "doc/latex/ufctex/example/figuras/LICENCAS.md",
            "doc/latex/ufctex/example/figuras/ufc-campus-pici.jpg",
            "doc/latex/ufctex/example/figuras/ufc-reitoria.jpg",
            "scripts/ufctex/prepare-windows-fonts.ps1",
        ):
            if required_entry not in tds_entries:
                raise SystemExit(f"TDS bundle missing {required_entry}")
        assert_no_proprietary_fonts(tds_entries)

        verify_checksums(first)

    print("Release package preflight completed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
PACKAGE_ID = "abntexto-ufc"
LEGACY_CLASS = "ufctex.cls"
COAT_OF_ARMS = ROOT / "assets/institucional/brasao-ufc.PNG"

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


def assert_ctan_excludes_coat_of_arms(archive_path: Path) -> None:
    expected = hashlib.sha1(COAT_OF_ARMS.read_bytes()).hexdigest()
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if hashlib.sha1(archive.read(info.filename)).hexdigest() == expected:
                raise SystemExit(f"CTAN bundle redistributes the UFC coat of arms: {info.filename}")


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
        "--output", str(output),
        "--reference-pdf", str(ROOT / "documento.pdf"),
        "--abntexto", str(abntexto),
    ], cwd=ROOT)


def run_pdflatex(work: Path, document: Path, tex_root: Path) -> None:
    env = os.environ.copy()
    env["TEXINPUTS"] = f"{tex_root}//:{env.get('TEXINPUTS', '')}"
    for _ in range(2):
        completed = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", document.name],
            cwd=work,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
        if completed.returncode != 0:
            raise SystemExit(
                f"CTAN compile smoke failed for {document.name}:\n"
                + "\n".join(completed.stdout.splitlines()[-60:])
            )
    if not document.with_suffix(".pdf").is_file():
        raise SystemExit(f"CTAN compile smoke did not produce {document.with_suffix('.pdf').name}.")


def ctan_compile_smoke(ctan_zip: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-ctan-smoke-") as temp:
        temp_path = Path(temp)
        with zipfile.ZipFile(ctan_zip) as archive:
            archive.extractall(temp_path / "archive")
        tex_root = temp_path / "archive" / PACKAGE_ID / "tex"
        work = temp_path / "work"
        work.mkdir()
        shutil.copyfile(COAT_OF_ARMS, work / "brasao-externo.PNG")
        document = work / "smoke.tex"
        document.write_text(
            r"""\documentclass{abntexto-ufc}
\ufcsetup{
  tipo = tese,
  impressao = anverso,
  capa = auto,
  ficha-catalografica = nao,
  brasao = sim,
  brasao-arquivo = {brasao-externo.PNG},
  fonte = times,
  fonte-estrita = nao,
  programa-doutorado = {Programa de Pós-Graduação em Ciência da Computação},
  titulo-doutor = {Ciência da Computação},
  autor = {Nome Sobrenome},
  titulo = {Teste de instalação CTAN},
  local = {Fortaleza},
  ano = {2026},
  orientador = {Prof. Dr. Nome do Orientador},
  tabelas = nativo,
  codigo = nenhum,
  algoritmos = nenhum,
  glossario = nenhum,
  indice = nenhum
}
\begin{document}
\imprimircapa
\imprimirfolhaderosto
\section{Teste}
Pacote instalado a partir do candidato CTAN.
\end{document}
""",
            encoding="utf-8",
        )
        run_pdflatex(work, document, tex_root)


def ctan_example_compile_smoke(ctan_zip: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-ctan-example-") as temp:
        temp_path = Path(temp)
        with zipfile.ZipFile(ctan_zip) as archive:
            archive.extractall(temp_path / "archive")
        archive_root = temp_path / "archive" / PACKAGE_ID
        tex_root = archive_root / "tex"
        source = archive_root / "doc" / f"{PACKAGE_ID}-example.tex"
        work = temp_path / "work"
        work.mkdir()
        document = work / source.name
        shutil.copyfile(source, document)
        run_pdflatex(work, document, tex_root)


def main() -> None:
    if not (ROOT / "documento.pdf").is_file():
        raise SystemExit("documento.pdf missing; run make release-preflight first.")
    if not COAT_OF_ARMS.is_file():
        raise SystemExit("UFC coat of arms missing from project source tree.")

    for relative, expected in REFERENCE_IMAGE_SHA1.items():
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"Licensed reference image missing before packaging: {relative}")
        actual = hashlib.sha1(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"Licensed reference image SHA-1 mismatch: {relative}")

    v = version()
    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-release-check-") as temp:
        temp_path = Path(temp)
        abntexto = temp_path / "abntexto.cls"
        subprocess.check_call([
            PYTHON, str(ROOT / "tools/fetch-abntexto.py"), "--output", str(abntexto)
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
            f"{PACKAGE_ID}-{v}.zip",
            f"modelo-latex-ufc-{v}.zip",
            f"modelo-latex-ufc-overleaf-{v}.zip",
            f"{PACKAGE_ID}-ctan-{v}.zip",
            f"{PACKAGE_ID}-{v}-reference.pdf",
            "SHA256SUMS",
        }
        if set(first_files) != required:
            raise SystemExit(f"Unexpected release artifacts: {sorted(set(first_files) ^ required)}")

        class_zip = first / f"{PACKAGE_ID}-{v}.zip"
        class_entries = names(class_zip)
        class_root = f"{PACKAGE_ID}-{v}/"
        assert_prefix(class_entries, class_root)
        for required_entry in (
            f"{class_root}abntexto-ufc.cls",
            f"{class_root}abntexto-ufc/core.def",
            f"{class_root}{LEGACY_CLASS}",
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
            f"{template_root}figuras/LICENCAS.md",
            f"{template_root}figuras/ufc-campus-pici.jpg",
            f"{template_root}figuras/ufc-reitoria.jpg",
            f"{template_root}abntexto-ufc.cls",
            f"{template_root}abntexto-ufc/core.def",
            f"{template_root}{LEGACY_CLASS}",
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
        if any(entry.startswith(f"modelo-latex-ufc-overleaf-{v}/") for entry in overleaf_entries):
            raise SystemExit("Overleaf bundle must place the main document at the archive root.")
        for required_entry in (
            "documento.tex", "abntexto-ufc.cls", LEGACY_CLASS, "abntexto.cls",
            "abntexto-ufc/core.def",
            "1-pre-textuais/resumo.tex", "3-pos-textuais/referencias.bib",
            "2-textuais/exemplos-de-formatacao.tex", "figuras/LICENCAS.md",
            "figuras/ufc-campus-pici.jpg", "figuras/ufc-reitoria.jpg",
        ):
            if required_entry not in overleaf_entries:
                raise SystemExit(f"Overleaf bundle missing {required_entry}")
        assert_reference_images(overleaf_zip, "")
        assert_no_proprietary_fonts(overleaf_entries)

        ctan_zip = first / f"{PACKAGE_ID}-ctan-{v}.zip"
        ctan_entries = names(ctan_zip)
        ctan_root = f"{PACKAGE_ID}/"
        assert_prefix(ctan_entries, ctan_root)
        for required_entry in (
            f"{ctan_root}README.md",
            f"{ctan_root}CHANGELOG.md",
            f"{ctan_root}LICENSE",
            f"{ctan_root}tex/abntexto-ufc.cls",
            f"{ctan_root}tex/abntexto-ufc/core.def",
            f"{ctan_root}doc/NORMAS.md",
            f"{ctan_root}doc/{PACKAGE_ID}-example.tex",
        ):
            if required_entry not in ctan_entries:
                raise SystemExit(f"CTAN bundle missing {required_entry}")
        if f"{ctan_root}tex/{LEGACY_CLASS}" in ctan_entries:
            raise SystemExit("CTAN bundle must not expose the deprecated ufctex class identity.")
        if any(entry.startswith(f"{ctan_root}tex/ufctex/") for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not expose the deprecated ufctex module namespace.")
        if any(entry.startswith(f"{ctan_root}tex/assets/institucional/") for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not redistribute UFC institutional assets.")
        if any(Path(entry).name == "brasao-ufc.PNG" for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not contain the UFC coat of arms binary.")
        if f"{ctan_root}doc/{PACKAGE_ID}-{v}-reference.pdf" in ctan_entries:
            raise SystemExit("CTAN bundle must not contain the reference PDF that embeds the UFC coat of arms.")
        if any(entry.startswith(f"{ctan_root}doc/example/") for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not contain the full project reference source tree.")
        if any(entry.startswith(f"{ctan_root}scripts/") for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not contain project-specific helper scripts.")
        if any(Path(entry).suffix.lower() in {".png", ".jpg", ".jpeg"} for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not contain image assets.")
        if any(entry.endswith(".tds.zip") for entry in ctan_entries):
            raise SystemExit("CTAN bundle must not contain a redundant nested TDS archive.")
        assert_ctan_excludes_coat_of_arms(ctan_zip)
        assert_no_proprietary_fonts(ctan_entries)
        ctan_compile_smoke(ctan_zip)
        ctan_example_compile_smoke(ctan_zip)

        verify_checksums(first)

    print("Release package preflight completed.")


if __name__ == "__main__":
    main()

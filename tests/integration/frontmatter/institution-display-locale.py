#!/usr/bin/env python3
"""Build real locale PDFs and assert legal-vs-presentation institution behavior."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOCALES = {
    "pt": ("pt-BR", "Universidade Federal do Ceará"),
    "en": ("en-US", "Federal University of Ceará"),
    "es": ("es-ES", "Universidad Federal de Ceará"),
    "fr": ("fr-FR", "Université fédérale du Ceará"),
}


def fold(value: str) -> str:
    """Normalize output accents, whitespace and case for robust PDF checks."""
    return re.sub(
        r"\s+", " ",
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    ).strip()


def compile_case(work: Path, case: str, locale: str, overrides: str,
                 expected: str, forbidden: tuple[str, ...]) -> dict:
    """Compile an actual source-bound PDF, then verify its displayed institution."""
    language = LOCALES[locale][0]
    profile = "research-project" if "project" in case else "doctoral-thesis"
    fields = (
        "doctoral-graduate-program={Synthetic Program},"
        "doctoral-program={Synthetic Doctoral Program},"
        "doctoral-degree-field={Computing},"
        if profile == "doctoral-thesis" else
        "project-program={Synthetic Program},project-identifier={SYNTHETIC-555},"
    )
    source = (
        rf"\DocumentMetadata{{lang={language},pdfstandard=A-2b,pdfversion=1.7}}" + "\n"
        r"\documentclass{abntexto-ufc}" "\n"
        r"\ufcsetup{" + f"type={profile},document-language={locale},"
        "print-mode=single-sided,cover=true,coat-of-arms=false,"
        "author={Synthetic Author},title={Institution Display Regression},"
        "location={Fortaleza},year={2026}," + fields + overrides + "}\n"
        r"\begin{document}" "\n"
        r"\pretextual" "\n"
        r"\ufcPrintCover" "\n"
        r"\ufcPrintTitlePage" "\n"
        r"\textual" "\n"
        r"\section{Synthetic Section}" "\n"
        "Source-bound locale check.\n"
        r"\end{document}" "\n"
    )
    tex = work / f"{case}.tex"
    tex.write_text(source, encoding="utf-8")
    command = [
        "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
        "-file-line-error", f"-jobname={case}",
        f"-output-directory={work}", str(tex),
    ]
    for _ in range(2):
        result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                text=True, check=False)
        if result.returncode:
            raise RuntimeError(f"{case}: compilation failed: {result.stdout[-2400:]}")
    pdf = work / f"{case}.pdf"
    output = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    text = fold(output.stdout)
    if fold(expected) not in text:
        raise ValueError(f"{case}: expected displayed name {expected!r}: {text[:750]}")
    for invalid in forbidden:
        if fold(invalid) in text:
            raise ValueError(f"{case}: unexpected name {invalid!r} in PDF")
    if profile == "research-project":
        # Assert the real PDF has a space between the localized work type and verb.
        phrase = {
            "pt": "Projeto de pesquisa apresentado",
            "en": "Research project submitted",
            "es": "Proyecto de investigación presentado",
            "fr": "Projet de recherche soumis",
        }[locale]
        if fold(phrase) not in text:
            raise ValueError(f"{case}: glued project nature words: {phrase!r}")
    return {
        "case": case, "locale": locale, "profile": profile,
        "expected_display": expected,
        "source_sha256": hashlib.sha256(tex.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "actual_pdf_checked": True,
    }


def main() -> None:
    """Exercise defaults, custom legal names and explicit presentation overrides."""
    with tempfile.TemporaryDirectory(prefix="abntexto-institution-display-") as tmp:
        work = Path(tmp)
        receipts = [
            compile_case(work, f"default-{locale}", locale, "",
                         display, () if locale == "pt" else ("Universidade Federal do Ceará",))
            for locale, (_, display) in LOCALES.items()
        ]
        receipts += [
            compile_case(work, "custom-en", "en",
                         "institution={Synthetic Legal Institute},",
                         "Synthetic Legal Institute", ("Federal University of Ceará",)),
            compile_case(work, "override-en", "en",
                         "institution={Synthetic Legal Institute},"
                         "institution-display={Public Test Institute},",
                         "Public Test Institute", ("Synthetic Legal Institute",)),
            compile_case(work, "custom-project-es", "es",
                         "submission-entity={Synthetic Legal Agency},",
                         "Synthetic Legal Agency", ("Universidad Federal de Ceará",)),
            compile_case(work, "override-project-fr", "fr",
                         "submission-entity={Synthetic Legal Agency},"
                         "submission-entity-display={Agence publique test},",
                         "Agence publique test", ("Synthetic Legal Agency",)),
            compile_case(work, "blank-legal-project-fr", "fr",
                         "submission-entity={},"
                         "submission-entity-display={Agence publique test},",
                         "Agence publique test", ("Université fédérale du Ceará",)),
            compile_case(work, "blank-default-project-fr", "fr",
                         "submission-entity={},",
                         "Université fédérale du Ceará", ("Synthetic Legal Agency",)),
        ]
    if len(receipts) != 10 or len({x["case"] for x in receipts}) != 10:
        raise ValueError("Expected ten unique real-PDF cases")
    output = ROOT / "artifacts/frontmatter/institution-display-locale.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "status": "PASS", "real_pdfs": len(receipts),
        "source_sha": __import__("os").environ.get("GITHUB_SHA", ""),
        "legal_metadata_mutation_pdf_test": "NOT_CHECKED",
        "human_approval": "PENDING",
        "receipts": receipts,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("INSTITUTION-DISPLAY-LOCALE status=PASS real_pdfs=10 "
          "locales=pt,en,es,fr custom_names=2 explicit_overrides=2")


if __name__ == "__main__":
    main()

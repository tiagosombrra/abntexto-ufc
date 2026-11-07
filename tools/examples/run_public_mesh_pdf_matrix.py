#!/usr/bin/env python3
"""Compile and audit each real, editable public mesh manuscript by source hash.

This diagnostic tests a composed class candidate; it cannot certify ABNT/UFC,
PDF/A, PDF/UA, or a release. Reproduction uses TeX Live 2026 with Biber.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "artifacts/public-mesh-documents"
CANONICAL = ROOT / "artifacts/canonical-mesh-study"
CATALOG = ROOT / "examples/public-mesh-documents/content.json"
STUDY = ROOT / "examples/canonical-mesh-study/study.json"
MATRIX = PUBLIC / "matrix"
LOCALES = ("pt", "en", "es", "fr")
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
CAPTIONS = {"pt": "Tabela", "en": "Table", "es": "Tabla", "fr": "Tableau"}
FORBIDDEN = ("INTEGRATED-", "R4-METHOD-", "R4SHORT-", "SYNTHETIC-ANON")


def sha(path: Path) -> str:
    """Bind each reported PDF and source to the actual input bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(value: str) -> str:
    """Collapse line breaks while preserving accents and locale-specific words."""
    canonical = unicodedata.normalize("NFC", value)
    # Babel may typeset straight French apostrophes as typographic U+2019.
    # Normalize punctuation variants without deleting authored words.
    canonical = canonical.translate(str.maketrans({
        "\u2018": "'", "\u2019": "'", "\u02bc": "'",
        "\u00ad": "",
    }))
    return re.sub(r"\s+", " ", canonical).strip().casefold()


def command(argv: list[str], log: Path, cwd: Path = ROOT) -> str:
    """Keep stderr and stdout even if a subprocess exits unsuccessfully."""
    result = subprocess.run(argv, cwd=cwd, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    data = result.stdout + "\n" + result.stderr
    log.write_text(data, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Command failed {argv[0]}: {log}: {data[-2200:]}")
    return result.stdout


def verify(info: dict[str, str], xmp: str, outline: str, text: str,
           title: str, author: str, heading: str, table_label: str,
           anonymized: bool) -> list[str]:
    """Explicit negative checks; do not treat tool success as PDF acceptance."""
    errors = []
    if normalized(info.get("Title", "")) != normalized(title):
        errors.append("pdf.info.title")
    if normalized(title) not in normalized(xmp):
        errors.append("pdf.xmp.title")
    if anonymized:
        if info.get("Author", "").strip():
            errors.append("pdf.info.anon_author")
        if author and any(author.casefold() in surface.casefold()
                          for surface in (xmp, outline, text)):
            errors.append("pdf.anon_identity_leak")
    else:
        if normalized(info.get("Author", "")) != normalized(author):
            errors.append("pdf.info.author")
        if normalized(author) not in normalized(xmp):
            errors.append("pdf.xmp.author")
    if normalized(heading) not in normalized(outline):
        errors.append("pdf.outline.heading")
    if normalized(heading) not in normalized(text):
        errors.append("pdf.text.missing_heading")
    if not re.search(r"(?<!\w)" + re.escape(table_label) + r"\s*1(?!\d)", text):
        errors.append("pdf.text.localized_table_caption")
    if any(m.casefold() in text.casefold() for m in FORBIDDEN):
        errors.append("pdf.text.synthetic_fixture_leak")
    pages = [x.strip() for x in text.split("\f")]
    if pages and pages[-1] == "":
        pages.pop()
    if not pages:
        errors.append("pdf.text.empty_document")
    if any(not p for p in pages):
        errors.append("pdf.text.blank_physical_page")
    if any(re.fullmatch(r"\d{1,5}", p) for p in pages):
        errors.append("pdf.text.number_only_leaf")
    if not info.get("Pages", "").isdigit() or int(info["Pages"]) != len(pages):
        errors.append("pdf.page_accounting")
    if "A4" not in info.get("Page size", ""):
        errors.append("pdf.page_size")
    return sorted(set(errors))


ANONYMOUS_ENTITY_LABEL = {
    "pt": "Instituição não identificada",
    "en": "Undisclosed institution",
    "es": "Institución no identificada",
    "fr": "Établissement non identifié",
}
SPECIALIZATION_LEVEL = {
    "pt": "especialização em", "en": "specialization in",
    "es": "especialización en", "fr": "spécialisation en",
}


def verify_cover_display(profile: str, locale: str, text: str) -> list[str]:
    """Reject duplicate cover lines and nonlocalized anonymous placeholders."""
    cover = text.split("\f", 1)[0]
    # Rejoin words hyphenated by pdftotext line wrapping without dropping accents.
    folded = normalized(re.sub(r"-\s*\n(?=\w)", "", cover))
    lines = [normalized(line) for line in cover.splitlines() if line.strip()]
    errors = []
    if profile in {"masters-thesis", "doctoral-thesis"}:
        if any(left == right and len(left) > 16
               for left, right in zip(lines, lines[1:])):
            errors.append("pdf.cover.duplicate_program_line")
    if profile == "specialization-capstone":
        needle = SPECIALIZATION_LEVEL[locale]
        if folded.count(needle) > 1:
            errors.append("pdf.cover.duplicate_specialization")
        if needle not in folded:
            errors.append("pdf.cover.specialization_missing")
    if profile == "anonymized-research-project":
        if normalized(ANONYMOUS_ENTITY_LABEL[locale]) not in folded:
            errors.append("pdf.anon.localized_institution_missing")
        if locale != "pt" and normalized(ANONYMOUS_ENTITY_LABEL["pt"]) in folded:
            errors.append("pdf.anon.portuguese_placeholder_leaked")
    return sorted(set(errors))


def selftest() -> None:
    """Prove the detector rejects the four historically observed defects."""
    good_info = {"Title": "Public study", "Author": "Public researcher",
                 "Pages": "1", "Page size": "595.276 x 841.89 pts (A4)"}
    good_outline = "Introduction"
    good_text = "Introduction\n\nTabla 1. Geometry comparison."
    args = ("Public study", "Public researcher", "Introduction", "Tabla", False)
    if verify(good_info, "Public study Public researcher",
              good_outline, good_text, *args):
        raise AssertionError("positive PDF evidence was rejected")
    mutations = [
        verify({**good_info, "Title": ""}, "Public study Public researcher",
               good_outline, good_text, *args),
        verify({**good_info, "Author": ""}, "Public study Public researcher",
               good_outline, good_text, *args),
        verify(good_info, "", good_outline, good_text, *args),
        verify(good_info, "Public study Public researcher", "", good_text, *args),
        verify(good_info, "Public study Public researcher",
               good_outline, good_text.replace("Tabla 1", "Cuadro 1"), *args),
        verify(good_info, "Public study Public researcher",
               good_outline, good_text + "\f\f", *args),
        verify(good_info, "Public study Public researcher",
               good_outline, good_text + "\f34\f", *args),
    ]
    if any(not issues for issues in mutations):
        raise AssertionError("one PDF negative control was incorrectly accepted")
    if normalized("l'efficacité d'une analyse") != normalized("l’efficacité d’une analyse"):
        raise AssertionError("French Babel punctuation variants were not normalized")
    if normalized("l'efficacité d'une analyse") == normalized("l'efficacité d'un résumé"):
        raise AssertionError("Punctuation normalization erased substantive differences")
    # These regression mutants reproduce concrete defects found in public PDFs.
    visible_mutants = [
        verify_cover_display(
            "specialization-capstone", "pt",
            "CURSO DE ESPECIALIZAÇÃO EM ESPECIALIZAÇÃO EM CIÊNCIA DA COMPUTAÇÃO"
        ),
        verify_cover_display(
            "masters-thesis", "en",
            "GRADUATE PROGRAM IN COMPUTER SCIENCE\nGRADUATE PROGRAM IN COMPUTER SCIENCE"
        ),
        verify_cover_display(
            "anonymized-research-project", "fr",
            "Projet de recherche soumis à Instituição não identificada"
        ),
    ]
    if any(not issues for issues in visible_mutants):
        raise AssertionError("An observed public PDF cover defect passed")
    if verify_cover_display(
        "specialization-capstone", "pt",
        "CURSO DE ESPECIALIZAÇÃO EM CIÊNCIA DA COMPUTAÇÃO"
    ):
        raise AssertionError("Valid specialization cover was rejected")
    if verify_cover_display(
        "anonymized-research-project", "en",
        "Research project submitted to Undisclosed institution"
    ):
        raise AssertionError("Valid anonymized institutional placeholder was rejected")
    print(f"PUBLIC-MESH-PDF-NEGATIVE status=PASS mutants={len(mutations)}",
          flush=True)


def inspect(profile: str, locale: str, job: str, output: Path,
            source: Path, context: dict, canon: dict,
            source_commit: str) -> dict:
    """Read PDF Info, XMP, outline, extracted text and all physical leaves."""
    pdf = ROOT / (job + ".pdf")
    raw_info = command(["pdfinfo", str(pdf)], output / (job + "-pdfinfo.txt"))
    info = dict(line.split(":", 1) for line in raw_info.splitlines()
                if ":" in line)
    info = {k.strip(): v.strip() for k, v in info.items()}
    xmp = command(["pdfinfo", "-meta", str(pdf)],
                  output / (job + "-xmp.xml"))
    outline = command(["mutool", "show", str(pdf), "outline"],
                      output / (job + "-outline.txt"))
    text = command(["pdftotext", "-layout", str(pdf), "-"],
                   output / (job + "-extracted.txt"))
    title = (context["proposal_title"]
             if profile in {"research-project", "anonymized-research-project"}
             else context["title"])
    anonymized = profile == "anonymized-research-project"
    # Only the actual serialized anonymized identity matters; authored name
    # is intentionally absent from the generated anonymous TeX source.
    expected_author = "" if anonymized else context["author"]
    errors = verify(info, xmp, outline, text, title, expected_author,
                    context["headings"][0], CAPTIONS[locale], anonymized)
    errors.extend(verify_cover_display(profile, locale, text))
    if normalized(canon["heading"]) not in normalized(text):
        errors.append("pdf.text.canonical_method_missing")
    if normalized(context["discussion"]) not in normalized(text):
        errors.append("pdf.text.authored_discussion_missing")
    pages = [x.strip() for x in text.split("\f")]
    if pages and not pages[-1]:
        pages.pop()
    receipt = {
        "profile": profile, "locale": locale, "source_commit_sha": source_commit,
        "source": source.relative_to(ROOT).as_posix(),
        "source_sha256": sha(source),
        "pdf": pdf.name, "pdf_sha256": sha(pdf),
        "pages": int(info.get("Pages", "0")),
        "blank_extracted_pages": [i for i,p in enumerate(pages, 1) if not p],
        "number_only_pages": [i for i,p in enumerate(pages, 1)
                              if re.fullmatch(r"\d{1,5}", p)],
        "pdf_a_verapdf": "NOT_TESTED", "pdf_ua": "NOT_CERTIFIED",
        "review": "HUMAN_PENDING", "publication_authorized": False,
        "status": "AUTOMATED_PARTIAL" if not errors else "FAIL",
        "failures": errors,
    }
    (output / (job+"-receipt.json")).write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2)+"\n",
        encoding="utf-8")
    for suffix in (".pdf", ".log", ".lot", ".out", ".toc", ".bcf", ".blg"):
        file = ROOT / (job + suffix)
        if file.is_file():
            shutil.copy2(file, output / file.name)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=LOCALES)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    selftest()
    if args.selftest:
        return 0
    if args.locale is None:
        parser.error("one --locale is required except with --selftest")

    commit = command(["git", "rev-parse", "HEAD"],
                     PUBLIC / f"source-git-{args.locale}.txt").strip()
    expected = os.environ.get("SOURCE_COMMIT_SHA", "")
    if expected and expected != commit:
        raise RuntimeError(f"Wrong immutable commit, expected {expected}, actual {commit}")
    manifest = json.loads((PUBLIC / "manifest.json").read_text(encoding="utf-8"))
    entries = [entry for entry in manifest["entries"]
               if entry["locale"] == args.locale]
    if len(entries) != 7 or {e["profile"] for e in entries} != set(PROFILES):
        raise AssertionError("Seven distinct public-document profiles are required")
    content = json.loads(CATALOG.read_text(encoding="utf-8"))
    canonical = json.loads(STUDY.read_text(encoding="utf-8"))
    out = MATRIX / args.locale
    out.mkdir(parents=True, exist_ok=True)
    receipts = []
    for entry in entries:
        profile = entry["profile"]
        source = ROOT / entry["source"]
        if sha(source) != entry["source_sha256"]:
            raise RuntimeError(f"Source hash changed since manifest: {source}")
        for rel, digest in entry["support"].items():
            support = ROOT / rel
            if sha(support) != digest:
                raise RuntimeError(f"Support hash changed: {support}")
        job = "public-" + profile + "-" + args.locale
        for n in (1, 2, 3):
            command(["pdflatex", "-interaction=nonstopmode",
                     "-halt-on-error", "-file-line-error",
                     "-jobname="+job, entry["source"]],
                    out / f"{job}-pdflatex-{n}.stdout")
            if n == 1:
                command(["biber", job],
                        out / f"{job}-biber.stdout")
        receipt = inspect(profile, args.locale, job, out, source,
                          content["locales"][args.locale],
                          canonical["locales"][args.locale], commit)
        receipts.append(receipt)
        print("PUBLIC-MESH-PDF-EVIDENCE "
              f"locale={args.locale} profile={profile} "
              f"pages={receipt['pages']} status={receipt['status']} "
              f"failures={receipt['failures']} human_review=PENDING",
              flush=True)
        if receipt["failures"]:
            break
    complete = len(receipts) == 7 and all(x["status"] == "AUTOMATED_PARTIAL"
                                          for x in receipts)
    result = {
        "schema_version": 1,
        "source_commit_sha": commit,
        "locale": args.locale,
        "documents": len(receipts), "expected_documents": 7,
        "total_pages": sum(x["pages"] for x in receipts),
        "receipts": receipts,
        "status": "AUTOMATED_PARTIAL" if complete else "FAIL",
        "human_review": "PENDING",
        "pdf_a_verapdf": "NOT_TESTED",
        "publication_authorized": False,
    }
    (out / "matrix-receipt.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+"\n",
        encoding="utf-8")
    if not complete:
        raise RuntimeError(f"locale={args.locale}: full PDF matrix failed at "
                           f"{receipts[-1]['profile'] if receipts else 'initialization'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

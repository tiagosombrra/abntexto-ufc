#!/usr/bin/env python3
"""Compile and conservatively inspect the seven full R4 PDFs for one locale.

Four independent CI jobs must produce all 28 PDFs at immutable Git SHAs.
The bounded predicates below deliberately do not replace per-page R5 review.
"""
from __future__ import annotations

import argparse
from contextlib import nullcontext
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "artifacts" / "comprehensive-7x4"
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
TABLE_NAMES = {"pt": "Tabela", "en": "Table", "es": "Tabla", "fr": "Tableau"}


def sha(path: Path) -> str:
    """Hash the actual retained PDF or source file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], log: Path, *, cwd: Path = ROOT) -> None:
    """Retain the complete original command transcript for audit."""
    with log.open("w", encoding="utf-8") as out:
        result = subprocess.run(command, cwd=cwd, stdout=out,
                                stderr=subprocess.STDOUT, check=False, text=True)
    if result.returncode:
        # Always retain source-bound evidence before raising an exception.
        # A failed TeX/Biber/MakeIndex build must never lose its native logs.
        stem = re.sub(r"-(?:pdflatex-\d+|biber|glossaries|index)$",
                      "", log.stem)
        source_file = log.parent / (stem + ".tex")
        receipt = {
            "status": "FAIL", "command": command,
            "return_code": result.returncode, "log": str(log),
            "log_sha256": sha(log),
            "source_commit_sha": os.environ.get("SOURCE_COMMIT_SHA", ""),
            "source_sha256": sha(source_file) if source_file.is_file() else None,
            "human_approval": "PENDING",
        }
        (log.parent / f"{log.stem}.failure.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        excerpt = "\n".join(log.read_text(errors="replace").splitlines()[-55:])
        raise ValueError(f"{command[0]} failed ({result.returncode}):\n{excerpt}")


def split_physical_pages(extracted: str) -> list[str]:
    """Preserve all pages, including duplex blanks and numbered-only pages."""
    pages = extracted.split("\f")
    # Poppler prints exactly one trailing form-feed as the last page delimiter.
    # That terminal separator is not an additional physical PDF page.
    if extracted.endswith("\f"):
        pages.pop()
    return pages


def orphan_folio_page(page: str) -> bool:
    """Distinguish a page consisting solely of its folio from a blank verso."""
    return bool(re.fullmatch(r"\s*\d+\s*", page))


def posttextual_optional_bracket_leak(text: str) -> bool:
    """Detect literal TeX optional [] serialized before glossary/index titles."""
    return bool(re.search(
        r"(?im)^\\s*\\[\\s*\\]\\s*(?:GLOSS|GLOS|ÍNDICE|INDEX)", text
    ))


def assert_page_accounting_mutants() -> None:
    """Reject discarded blank leaves and numbered-only leaf false negatives."""
    three = split_physical_pages("COVER\f\fINDEX\f")
    if len(three) != 3 or three != ["COVER", "", "INDEX"]:
        raise AssertionError("blank physical PDF page was discarded")
    if len(split_physical_pages("COVER\fINDEX\f")) != 2:
        raise AssertionError("incorrect PDF page boundary count")
    if len(split_physical_pages("COVER\f60\fINDEX\f")) != 3:
        raise AssertionError("numbered-only physical PDF page was discarded")
    if split_physical_pages("COVER\f") != ["COVER"]:
        raise AssertionError("trailing Poppler separator counted as a PDF page")
    for bad in ("[]GLOSSÁRIO", "[]GLOSSARY", "[]ÍNDICE ALFABÉTICO",
                "[]GLOSSAIRE", "[]INDEX"):
        if not posttextual_optional_bracket_leak("CONTENTS\n" + bad + " ... 51"):
            raise AssertionError(f"hyperref optional bracket was accepted: {bad}")
    for valid in ("GLOSSÁRIO ..... 51", "INDEX .... 57",
                  "[] C++ array synthetic code", "[]R4-LEGAL"):
        if posttextual_optional_bracket_leak(valid):
            raise AssertionError(f"false positive in glossary/index bracket gate: {valid}")
    if not orphan_folio_page("  53  \n"):
        raise AssertionError("number-only folio regression missed")
    for legitimate in ("", "53\nChapter title", "Appendix 53"):
        if orphan_folio_page(legitimate):
            raise AssertionError("legitimate page falsely flagged as orphan folio")


def text_pdf(pdf: Path) -> list[str]:
    """Inspect every physical page extracted from the actual PDF."""
    completed = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                               cwd=ROOT, capture_output=True, text=True, check=True)
    return split_physical_pages(completed.stdout)


def inspect(profile: str, locale: str, tex: str, pdf: Path,
            lot: Path | None) -> dict:
    """Check real content separately from declared source feature flags."""
    raw_pages = text_pdf(pdf)
    pages = [re.sub(r"-(?=\s+\w)\s+", "-", page) for page in raw_pages]
    aggregate = "\n".join(pages)
    markers = (
        f"R4-METHOD-{locale.upper()}",
        f"R4-RESULTS-{locale.upper()}",
        f"R4-IMPLEMENTATION-{locale.upper()}",
        f"R4-DISCUSSION-{locale.upper()}",
        "R4LONGROW001", "R4LONGROW125",
        "R4NATIVEROW001", "R4NATIVEROW085",
        f"R4-ALGORITHM-{locale.upper()}",
        f"R4-INLINE-CODE-{locale.upper()}",
        f"R4-EXTERNAL-CODE-{locale.upper()}",
    )
    findings = [f"pdf.text.missing.{mark}" for mark in markers
                if mark not in aggregate]
    if posttextual_optional_bracket_leak(aggregate):
        findings.append("pdf.toc.posttextual_literal_optional_brackets")
    # Verify rendered implementation bodies, not only captions or list entries.
    # A caption may exist even if the code or algorithm environment is empty.
    body_markers = ("int sum(int a, int b)", "return a + b;",
                    "int main()", "std::cout", "end while", "return")
    for marker in body_markers:
        if marker not in aggregate:
            findings.append(f"pdf.rendered_implementation.missing.{marker}")
    if not re.search(r"(?im)^\s*\d+:\s*while\b.*\bdo\b", aggregate):
        findings.append("pdf.rendered_algorithm.numbered_while_missing")
    for first, last, family in (
        ("R4LONGROW001", "R4LONGROW125", "tabularray"),
        ("R4NATIVEROW001", "R4NATIVEROW085", "native-longtable"),
    ):
        starts = [i for i, page in enumerate(pages) if first in page]
        ends = [i for i, page in enumerate(pages) if last in page]
        if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
            findings.append(f"pdf.{family}.no_physical_continuation")
    if len(pages) < 6:
        findings.append("pdf.insufficient_physical_pages")
    if any(orphan_folio_page(page) for page in raw_pages):
        findings.append("pdf.pagination.orphan-number-only")
    info_output = subprocess.check_output(
        ["pdfinfo", str(pdf)], cwd=ROOT, text=True
    )
    info = dict(line.split(":", 1) for line in info_output.splitlines()
                if ":" in line)
    info = {key.strip(): val.strip() for key, val in info.items()}
    claimed_pages = int(info.get("Pages", "0"))
    if len(raw_pages) != claimed_pages:
        findings.append(
            f"pdf.page_accounting.physical_mismatch={len(raw_pages)}/{claimed_pages}"
        )
    page_receipts = [
        {
            "physical_page": n,
            "extracted_characters": len(page.strip()),
            "word_count": len(re.findall(r"\b\w+\b", page)),
            "blank": not bool(page.strip()),
            "number_only": orphan_folio_page(page),
            "sample": " ".join(page.split())[:120],
            "human_visual_review": "PENDING",
        }
        for n, page in enumerate(raw_pages, start=1)
    ]
    blank_physical_pages = [
        row["physical_page"] for row in page_receipts if row["blank"]
    ]
    # Record evidence for every blank leaf. A repeated verso pattern is only
    # a recto-padding *candidate*, not ABNT authorization or visual approval.
    duplex_profiles = {"masters-thesis", "doctoral-thesis",
                       "anonymized-research-project"}
    blank_page_context = []
    for n in blank_physical_pages:
        previous_page = page_receipts[n - 2] if n > 1 else None
        following_page = page_receipts[n] if n < len(page_receipts) else None
        possible_duplex_padding = bool(
            profile in duplex_profiles and n % 2 == 1
            and previous_page and following_page
            and not previous_page["blank"] and not following_page["blank"]
        )
        blank_page_context.append({
            "physical_page": n,
            "preceding_text_excerpt": (previous_page["sample"]
                                        if previous_page else None),
            "following_text_excerpt": (following_page["sample"]
                                        if following_page else None),
            "candidate_duplex_recto_padding": possible_duplex_padding,
            "normative_justification": "PENDING_R5_REVIEW",
            "visual_approval": "PENDING",
        })
        if profile in duplex_profiles and not possible_duplex_padding:
            findings.append(f"pdf.pagination.unclassified_blank_page.{n}")
    if profile not in ("masters-thesis", "doctoral-thesis",
                       "anonymized-research-project") and blank_physical_pages:
        findings.append("pdf.single_sided.unexpected_blank_page")
    # Independently examine Info, XMP and navigable PDF outlines, not merely
    # the presence of a source-level \DocumentMetadata declaration.
    xmp = subprocess.check_output(
        ["pdfinfo", "-meta", str(pdf)], cwd=ROOT, text=True
    )
    outlines = subprocess.check_output(
        ["mutool", "show", str(pdf), "outline"], cwd=ROOT, text=True
    )
    (pdf.parent / f"{pdf.stem}-xmp.xml").write_text(xmp, encoding="utf-8")
    (pdf.parent / f"{pdf.stem}-outline.txt").write_text(outlines, encoding="utf-8")
    expected_title = "Integrated Multilingual Document"
    expected_author = "Integrated Test Author"
    expected_heading = f"R4-METHOD-{locale.upper()}"
    if info.get("Title", "").strip() != expected_title:
        findings.append("pdf.metadata.info_title_incorrect")
    if expected_title not in xmp:
        findings.append("pdf.metadata.xmp_title_missing")
    if expected_heading not in outlines:
        findings.append("pdf.navigation.outline_heading_missing")
    if profile == "anonymized-research-project":
        if info.get("Author", "").strip():
            findings.append("pdf.privacy.anonymous_author_metadata")
        for surface_name, text in (
            ("xmp", xmp), ("outline", outlines), ("extracted_text", aggregate)
        ):
            if expected_author.casefold() in text.casefold():
                findings.append(f"pdf.privacy.author_leak.{surface_name}")
    else:
        if info.get("Author", "").strip() != expected_author:
            findings.append("pdf.metadata.info_author_incorrect")
        if expected_author not in xmp:
            findings.append("pdf.metadata.xmp_author_missing")
    if not lot or not lot.is_file():
        if profile != "scientific-article":
            findings.append("pdf.table_list.lot_missing")
    elif profile != "scientific-article":
        lot_text = lot.read_text(encoding="utf-8", errors="replace")
        expected_entries = (
            f"INTEGRATED-TABLE-{locale.upper()}",
            f"R4SHORT-{locale.upper()}",
            f"R4LONG-{locale.upper()}",
            f"R4NATIVE-{locale.upper()}",
        )
        for marker in expected_entries:
            if lot_text.count(marker) != 1:
                findings.append(f"lot.table_entry_count_invalid.{marker}")
        table_heading = {
            "pt": "LISTA DE TABELAS", "en": "LIST OF TABLES",
            "es": "LISTA DE TABLAS", "fr": "LISTE DES TABLEAUX",
        }[locale]
        list_pages = [page for page in pages if table_heading in page.upper()]
        if len(list_pages) != 1:
            findings.append("pdf.table_list.heading_invalid")
        else:
            names = re.findall(
                rf"^\s*{re.escape(TABLE_NAMES[locale])}\s+(\d+)\b",
                list_pages[0], flags=re.M | re.I,
            )
            if names != ["1", "2", "3", "4"]:
                findings.append(f"pdf.table_list.prefix_or_sequence={names}")
            for marker in expected_entries:
                if list_pages[0].count(marker) != 1:
                    findings.append(f"pdf.table_list.caption_entry_invalid.{marker}")
    return {
        "profile": profile, "locale": locale,
        "source_features": {feature: feature in tex for feature in (
            r"\subsection{", r"\subsubsection{", r"\begin{align}",
            r"\begin{longabnttblr}", r"\begin{longtable}",
            r"\begin{ufcalgorithm}", r"\begin{ufclisting}",
        )},
        "pdf_sha256": sha(pdf),
        "pdf_info_title": info.get("Title", ""),
        "pdf_info_author": info.get("Author", ""),
        "pdf_xmp_sha256": sha(pdf.parent / f"{pdf.stem}-xmp.xml"),
        "pdf_outline_sha256": sha(pdf.parent / f"{pdf.stem}-outline.txt"),
        "pdf_outline_heading_verified": expected_heading in outlines,
        "pages": claimed_pages,
        "extracted_physical_pages": len(pages),
        "blank_physical_pages": blank_physical_pages,
        "blank_page_context": blank_page_context,
        "blank_page_semantics": ("REQUIRES_R5_REVIEW" if blank_physical_pages
                                 else "NO_EXTRACTED_BLANK_PAGES"),
        "page_receipts": page_receipts,
        "failures": sorted(set(findings)),
        "human_page_by_page_review": "PENDING",
        "pdf_a_verapdf": "NOT_TESTED",
        "pdf_ua": "NOT_CERTIFIED",
        "proof_state": "AUTOMATED_PARTIAL_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    assert_page_accounting_mutants()
    if args.selftest:
        print("R4-PHYSICAL-PAGE-MUTANTS status=PASS cases=17")
        return 0
    if args.locale is None:
        parser.error("--locale required except for --selftest")
    locale = args.locale
    out = ARTIFACTS / locale
    out.mkdir(parents=True, exist_ok=True)
    run([sys.executable,
         "tests/integration/frontmatter/generate-comprehensive-corpus.py",
         "--locale", locale], out / "generation.stdout")
    manifest = json.loads((out / "source-index.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    variants = [v for entry in entries for v in entry.get("supplementary_variants", [])]
    if len(variants) != 1 or variants[0]["profile"] != "doctoral-thesis":
        raise ValueError("expected exactly one independently sourced doctoral lists variant")
    if len(entries) != 7 or {v["profile"] for v in entries} != set(PROFILES):
        raise ValueError("R4 corpus has fewer than seven independent profiles")
    gitsha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    expected = os.environ.get("SOURCE_COMMIT_SHA")
    if expected and expected != gitsha:
        raise ValueError(f"wrong checkout SHA: {gitsha} != {expected}")
    reports: list[dict] = []
    # Retain raw .aux/.lot/.log and partial PDFs in the same upload artifact,
    # even when a later compilation phase fails. Never silently delete evidence.
    with nullcontext(out / "build") as tmp:
        work = Path(tmp)
        work.mkdir(parents=True, exist_ok=True)
        for entry in [*entries, *variants]:
            job, profile = entry["name"], entry["profile"]
            source = ROOT / entry["source"]
            if sha(source) != entry["source_sha256"]:
                raise ValueError("R4 source mutated after manifest generation")
            for path, expected_hash in entry["support_sha256"].items():
                if sha(ROOT / path) != expected_hash:
                    raise ValueError("R4 supporting text hash mismatch")
            print(f"R4-COMPREHENSIVE-PDF locale={locale} profile={profile}",
                  flush=True)
            command = [
                "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                "-file-line-error", f"-jobname={job}",
                f"-output-directory={work}", str(source),
            ]
            run(command, out / f"{job}-pdflatex-1.log")
            run(["biber", "--input-directory", str(work),
                 "--output-directory", str(work), job],
                out / f"{job}-biber.log")
            if entry.get("glossary_enabled", profile == "doctoral-thesis"):
                run(["makeglossaries", "-d", str(work), job],
                    out / f"{job}-glossaries.log")
            if entry.get("index_enabled", profile == "doctoral-thesis"):
                run(["makeindex", f"{job}.idx", "-o", f"{job}.ind"],
                    out / f"{job}-index.log", cwd=work)
            for part in (2, 3):
                run(command, out / f"{job}-pdflatex-{part}.log")
            pdf = work / f"{job}.pdf"
            if not pdf.is_file() or not pdf.stat().st_size:
                raise ValueError(f"PDF absent after compilation: {job}")
            retained = out / pdf.name
            retained.write_bytes(pdf.read_bytes())
            native_lot = work / f"{job}.lot"
            lot = out / native_lot.name if native_lot.is_file() else None
            if lot:
                lot.write_bytes(native_lot.read_bytes())
            report = inspect(profile, locale, source.read_text(encoding="utf-8"),
                             retained, lot)
            report["specimen_kind"] = ("supplementary-doctoral-code-lists"
                                       if entry in variants else "main-baseline")
            report["glossary_enabled"] = entry.get("glossary_enabled", False)
            report["code_algorithm_lists_printed"] = entry.get("code_algorithm_lists_printed", False)
            # Rasterize *every* physical PDF page. Extraction alone does not
            # reveal clipping, broken glyphs or blank verso layout defects.
            # These small, immutable JPEG thumbnails are R5 human review inputs,
            # not automatic claims of visual/ABNT conformity.
            raster_folder = out / "page-thumbnails" / job
            raster_folder.mkdir(parents=True, exist_ok=True)
            prefix = raster_folder / "page"
            run(["pdftoppm", "-r", "28", "-jpeg", "-jpegopt", "quality=70",
                 str(retained), str(prefix)],
                out / f"{job}-raster.stdout")
            thumbnails = sorted(raster_folder.glob("page-*.jpg"))
            if len(thumbnails) != report["pages"]:
                report["failures"].append(
                    f"raster.physical_page_count={len(thumbnails)}/{report['pages']}"
                )
            for item, thumb in zip(report["page_receipts"], thumbnails):
                item["thumbnail_sha256"] = sha(thumb)
                item["thumbnail_path"] = str(thumb)
            report["rasterized_physical_pages"] = len(thumbnails)
            report["raster_proof"] = "ALL_PAGES_RENDERED_NOT_VISUALLY_APPROVED"
            report["source_commit_sha"] = gitsha
            report["source_sha256"] = sha(source)
            report["support_source_sha256"] = entry["support_sha256"]
            reports.append(report)
            (out / f"{job}-receipt.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    failed = [report for report in reports if report["failures"]]
    evidence = {
        "source_commit_sha": gitsha, "locale": locale, "pdfs": len(reports),
        "main_baseline_pdfs": len(entries), "supplementary_variants": len(variants),
        "automatic_failures": len(failed),
        "release_authorized": False, "human_approval": "PENDING",
        "scope": "Full R4 technical candidates, not R5 accepted documents",
        "entries": reports,
    }
    (out / "pdf-receipts.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if failed:
        for report in failed:
            print(f"R4-COMPREHENSIVE-DEFECT locale={locale} "
                  f"profile={report['profile']} findings={report['failures']}")
        return 1
    print(f"R4-COMPREHENSIVE-EVIDENCE status=AUTOMATED_PARTIAL locale={locale} "
          f"pdfs={len(reports)} baseline=7 variants={len(variants)} "
          f"pages={sum(x['pages'] for x in reports)} "
          f"human_approval=PENDING")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"R4-COMPREHENSIVE-EVIDENCE status=FAIL reason={exc}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Source-bound PDF Info, XMP, and outline regression for issue #558.

Each locale compiles academic, article and anonymous real PDFs under TeX Live
2026. Do not equate this narrow technical matrix with 28 full R4 manuscripts
or with PDF/A certification: external veraPDF and R5 are separate gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "artifacts" / "pdf-metadata-outline"
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PROFILES = ("doctoral-thesis", "scientific-article", "anonymized-research-project")


def digest(path: Path) -> str:
    """Bind every reported result to the exact input/PDF bytes inspected."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(profile: str, locale: str) -> tuple[str, str, str, str]:
    """Generate an authored synthetic test without exposing a real identity."""
    if profile not in PROFILES or locale not in LOCALES:
        raise ValueError("unsupported profile or locale")
    tag = f"{profile}-{locale}"
    title = f"PDFINFO-TITLE-{tag}"
    anonymous = profile == "anonymized-research-project"
    author = (f"PDFINFO-SECRET-AUTHOR-{locale}" if anonymous
              else f"PDFINFO-PUBLIC-AUTHOR-{locale}")
    section = f"PDFINFO-SECTION-{tag}"
    config = (
        f"type={profile},document-language={locale},"
        "print-mode=single-sided,cover=false,coat-of-arms=false,"
        "catalog-card=false,location={Fortaleza},year={2026},"
        f"title={{{title}}},author={{{author}}},"
        "doctoral-graduate-program={Synthetic Computing},"
        "doctoral-program={Synthetic Computing},"
        "doctoral-degree-field={Computing},"
        "project-program={Synthetic Research},"
        "project-identifier={PUBLIC-SYNTHETIC-ANON-001},"
        "article-author-note={Synthetic public test note},"
        "submission-date={2026-11-05},approval-date={2026-11-05}"
    )
    lines = [
        rf"\DocumentMetadata{{lang={LOCALES[locale]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{{config}}}",
        r"\begin{document}",
    ]
    if profile == "scientific-article":
        lines += [
            rf"\ufcPrintArticleFrontMatter{{PDFINFO-ARTICLE-SUMMARY-{locale}. "
            rf"\ufcSummaryKeywordsInLanguage{{{locale}}}{{synthetic; metadata; navigation.}}}}",
        ]
    else:
        lines += [
            r"\pretextual",
            r"\ufcPrintTitlePage",
        ]
    lines += [
        r"\textual",
        rf"\section{{{section}}}",
        "PDFINFO-PUBLIC-BODY.",
        rf"\subsection{{PDFINFO-SUBSECTION-{locale}}}",
        "PDFINFO-PUBLIC-BODY-SECOND.",
        r"\end{document}",
        "",
    ]
    return "\n".join(lines), title, author, section


def run(args: list[str], path: Path, *, cwd: Path = ROOT) -> str:
    """Write original command evidence, retaining failure output."""
    completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                               check=False)
    output = completed.stdout + "\n" + completed.stderr
    path.write_text(output, encoding="utf-8")
    if completed.returncode:
        raise ValueError(f"{args[0]} failed: {output[-1600:]}")
    return completed.stdout


def check_fields(info: dict[str, str], xmp: str, outlines: str, text: str,
                 attachments: list[bytes], title: str, author: str,
                 section: str, anonymous: bool) -> list[str]:
    """Return strict real-PDF findings, with privacy-negative controls."""
    errors = []
    if info.get("Title", "").strip() != title:
        errors.append("pdf.info.title")
    if title not in xmp:
        errors.append("pdf.xmp.title")
    if section not in outlines:
        errors.append("pdf.outline.section")
    if anonymous:
        if info.get("Author", "").strip():
            errors.append("pdf.info.anonymous_author")
        for surface, value in (
            ("pdf.xmp", xmp),
            ("pdf.outline", outlines),
            ("pdf.text", text),
        ):
            if author in value or author.encode().decode() in value:
                errors.append(f"{surface}.anonymous_identity_leak")
        for payload in attachments:
            if author.encode() in payload or author.encode("utf-16be") in payload:
                errors.append("pdf.attachment.anonymous_identity_leak")
    else:
        if info.get("Author", "").strip() != author:
            errors.append("pdf.info.author")
        if author not in xmp:
            errors.append("pdf.xmp.author")
    return sorted(set(errors))


def selftest() -> None:
    """Prove title, author, outline and anonymous privacy mutants are rejected."""
    title, author, section = "PUBLIC-TITLE", "PRIVATE-AUTHOR", "PUBLIC-SECTION"
    fields = {"Title": title, "Author": ""}
    good = check_fields(fields, title, section, "PUBLIC BODY", [b"Content Credentials"],
                        title, author, section, True)
    if good:
        raise AssertionError(f"valid anonymous PDF rejected: {good}")
    checks = [
        check_fields({"Author": ""}, title, section, "PUBLIC BODY", [],
                     title, author, section, True),
        check_fields(fields, "", section, "PUBLIC BODY", [],
                     title, author, section, True),
        check_fields(fields, title, "", "PUBLIC BODY", [],
                     title, author, section, True),
        check_fields({"Title": title, "Author": author}, title, section, "",
                     [], title, author, section, True),
        check_fields(fields, title + author, section, "", [],
                     title, author, section, True),
        check_fields(fields, title, section + author, "", [],
                     title, author, section, True),
        check_fields(fields, title, section, author, [],
                     title, author, section, True),
        check_fields(fields, title, section, "", [author.encode()],
                     title, author, section, True),
        check_fields({"Title": title}, title, section, "", [],
                     title, author, section, False),
    ]
    if any(not problems for problems in checks):
        raise AssertionError("missing negative control: at least one mutant passed")
    print(f"PDFINFO-NEGATIVE-CONTROLS status=PASS mutants={len(checks)}")


def inspect(profile: str, locale: str, work: Path, source: Path,
            title: str, author: str, section: str, commit: str) -> dict:
    """Check the actual PDF Info, XMP, outline and embedded attachment bytes."""
    pdf = work / (source.stem + ".pdf")
    meta_output = run(["pdfinfo", str(pdf)], work / f"{source.stem}-pdfinfo.stdout")
    info = dict(line.split(":", 1) for line in meta_output.splitlines() if ":" in line)
    info = {k.strip(): v.strip() for k, v in info.items()}
    xmp = run(["pdfinfo", "-meta", str(pdf)], work / f"{source.stem}-xmp.stdout")
    outline = run(["mutool", "show", str(pdf), "outline"],
                  work / f"{source.stem}-outline.stdout")
    text = run(["pdftotext", "-layout", str(pdf), "-"],
               work / f"{source.stem}-pdftotext.stdout")
    attachment_dir = work / f"{source.stem}-attachments"
    attachment_dir.mkdir(exist_ok=True)
    run(["pdfdetach", "-saveall", str(pdf)],
        work / f"{source.stem}-attachments.stdout", cwd=attachment_dir)
    attachments = [p.read_bytes() for p in attachment_dir.iterdir() if p.is_file()]
    errors = check_fields(info, xmp, outline, text, attachments,
                          title, author, section,
                          profile == "anonymized-research-project")
    receipt = {
        "profile": profile, "locale": locale,
        "source_commit_sha": commit,
        "source_sha256": digest(source), "pdf_sha256": digest(pdf),
        "pages": int(info.get("Pages", "0")),
        "outlines_present": bool(outline.strip()),
        "attachment_count": len(attachments),
        "status": "AUTOMATED_PARTIAL" if not errors else "FAIL",
        "failures": errors, "human_review": "PENDING",
        "pdf_a_verapdf": "NOT_TESTED", "pdf_ua": "NOT_CERTIFIED",
    }
    (work / f"{source.stem}-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--locale", choices=tuple(LOCALES), required=True)
    a = p.parse_args()
    selftest()
    work = ARTIFACTS / a.locale
    work.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                     cwd=ROOT, text=True).strip()
    if os.environ.get("SOURCE_COMMIT_SHA") not in (None, "", commit):
        raise ValueError("wrong immutable Git source revision")
    results = []
    for profile in PROFILES:
        source_text, title, author, section = fixture(profile, a.locale)
        path = work / f"pdfinfo-{profile}-{a.locale}.tex"
        path.write_text(source_text, encoding="utf-8")
        for step in (1, 2):
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", f"-jobname={path.stem}",
                 f"-output-directory={work}", str(path)],
                work / f"{path.stem}-pdflatex-{step}.stdout")
        result = inspect(profile, a.locale, work, path,
                         title, author, section, commit)
        results.append(result)
        print(f"PDFINFO-EVIDENCE profile={profile} locale={a.locale} "
              f"status={result['status']} findings={result['failures']}",
              flush=True)
    (work / "manifest.json").write_text(
        json.dumps({"locale": a.locale, "commit": commit,
                    "cases": results, "publication_authorized": False},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return int(any(row["failures"] for row in results))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, ValueError, OSError, subprocess.CalledProcessError) as err:
        print(f"PDFINFO-EVIDENCE status=FAIL reason={err}", file=sys.stderr)
        sys.exit(1)

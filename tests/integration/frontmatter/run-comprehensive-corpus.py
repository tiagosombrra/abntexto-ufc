#!/usr/bin/env python3
"""Compile and conservatively inspect the seven full R4 PDFs for one locale.

Four independent CI jobs must produce all 28 PDFs at immutable Git SHAs.
The bounded predicates below deliberately do not replace per-page R5 review.
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
        excerpt = "\n".join(log.read_text(errors="replace").splitlines()[-55:])
        raise ValueError(f"{command[0]} failed ({result.returncode}):\n{excerpt}")


def text_pdf(pdf: Path) -> list[str]:
    """Inspect the actual generated PDF text, including physical page breaks."""
    completed = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                               cwd=ROOT, capture_output=True, text=True, check=True)
    return [s for s in completed.stdout.split("\f") if s.strip()]


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
    if any(re.fullmatch(r"\s*\d+\s*", page) for page in raw_pages):
        findings.append("pdf.pagination.orphan-number-only")
    info_output = subprocess.check_output(
        ["pdfinfo", str(pdf)], cwd=ROOT, text=True
    )
    info = dict(line.split(":", 1) for line in info_output.splitlines()
                if ":" in line)
    info = {key.strip(): val.strip() for key, val in info.items()}
    if not info.get("Title"):
        findings.append("pdf.metadata.title_missing")
    if profile == "anonymized-research-project":
        if info.get("Author"):
            findings.append("pdf.privacy.anonymous_author_metadata")
    elif not info.get("Author"):
        findings.append("pdf.metadata.author_missing")
    if not lot or not lot.is_file():
        if profile != "scientific-article":
            findings.append("pdf.table_list.lot_missing")
    elif profile != "scientific-article":
        lot_text = lot.read_text(encoding="utf-8", errors="replace")
        if "R4LONG-" + locale.upper() not in lot_text:
            findings.append("lot.longtable_entry_missing")
        if "R4NATIVE-" + locale.upper() not in lot_text:
            findings.append("lot.native_entry_missing")
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
            if len(names) < 3 or names[:3] != ["1", "2", "3"]:
                findings.append(f"pdf.table_list.prefix_or_sequence={names}")
    return {
        "profile": profile, "locale": locale,
        "source_features": {feature: feature in tex for feature in (
            r"\subsection{", r"\subsubsection{", r"\begin{align}",
            r"\begin{longabnttblr}", r"\begin{longtable}",
            r"\begin{ufcalgorithm}", r"\begin{ufclisting}",
        )},
        "pdf_sha256": sha(pdf),
        "pages": len(pages),
        "failures": sorted(set(findings)),
        "human_page_by_page_review": "PENDING",
        "pdf_a_verapdf": "NOT_TESTED",
        "pdf_ua": "NOT_CERTIFIED",
        "proof_state": "AUTOMATED_PARTIAL_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES), required=True)
    args = parser.parse_args()
    locale = args.locale
    out = ARTIFACTS / locale
    out.mkdir(parents=True, exist_ok=True)
    run([sys.executable,
         "tests/integration/frontmatter/generate-comprehensive-corpus.py",
         "--locale", locale], out / "generation.stdout")
    manifest = json.loads((out / "source-index.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    if len(entries) != 7 or {v["profile"] for v in entries} != set(PROFILES):
        raise ValueError("R4 corpus has fewer than seven independent profiles")
    gitsha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    expected = os.environ.get("SOURCE_COMMIT_SHA")
    if expected and expected != gitsha:
        raise ValueError(f"wrong checkout SHA: {gitsha} != {expected}")
    reports: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="abntexto-r4-comprehensive-") as tmp:
        work = Path(tmp)
        for entry in entries:
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
            if profile == "doctoral-thesis":
                run(["makeglossaries", "-d", str(work), job],
                    out / f"{job}-glossaries.log")
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
          f"pdfs=7 pages={sum(x['pages'] for x in reports)} "
          f"human_approval=PENDING")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"R4-COMPREHENSIVE-EVIDENCE status=FAIL reason={exc}", file=sys.stderr)
        sys.exit(1)

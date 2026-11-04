#!/usr/bin/env python3
"""R3 source-bound actual-PDF regression for mixed native and multipage tables.

This is a defect reproducer, not a v3.1.0 release or visual approval.
It intentionally FAILS on a missing/mixed second List-of-Tables entry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "artifacts" / "table-list-r3"
LOCALES = {
    "pt": ("pt-BR", "LISTA DE TABELAS", "Tabela", "Fonte"),
    "en": ("en-US", "LIST OF TABLES", "Table", "Source"),
    "es": ("es-ES", "LISTA DE TABLAS", "Tabla", "Fuente"),
    "fr": ("fr-FR", "LISTE DES TABLEAUX", "Tableau", "Source"),
}
GATE = runpy.run_path(str(
    ROOT / "tests/integration/frontmatter/comprehensive-pdf-gate.py"
))
table_list_failures = GATE["table_list_failures"]


def digest(path: Path) -> str:
    """Bind each report to the source/PDF bytes actually inspected."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selftest() -> None:
    """Reject the exact historical mixed and omitted-caption mutations."""
    for locale, (_, heading, label, _) in LOCALES.items():
        good = f"{heading}\n{label} 1 — SHORT............3\n{label} 2 — LONG............4"
        bare = f"{heading}\n{label} 1 — SHORT............3\n2 LONG............4"
        missing = f"{heading}\n{label} 1 — SHORT............3"
        wrapped = (
            f"{heading}\n{label} 1 — SHORT from\n"
            f"        2 departments............3\n{label} 2 — LONG............4"
        )
        if table_list_failures(good, locale):
            raise AssertionError(f"valid list rejected: {locale}")
        if table_list_failures(wrapped, locale):
            raise AssertionError(f"valid wrapped list rejected: {locale}")
        if "table_list.mixed_or_bare_prefix" not in table_list_failures(bare, locale):
            raise AssertionError(f"bare second numeral accepted: {locale}")
        if "table_list.fewer_than_two_entries" not in table_list_failures(missing, locale):
            raise AssertionError(f"omitted second table accepted: {locale}")
        three = good + f"\n{label} 3 — RAW............6"
        bad_third = good + "\n3 RAW............6"
        if table_list_failures(three, locale):
            raise AssertionError(f"valid third native longtable rejected: {locale}")
        if "table_list.mixed_or_bare_prefix" not in table_list_failures(bad_third, locale):
            raise AssertionError(f"bare third native longtable accepted: {locale}")
    print("R3-TABLE-LIST-MUTANTS status=PASS locales=4 cases=24", flush=True)


def make_source(locale: str) -> str:
    """Exercise class-native, tabularray-abnt and raw longtable caption paths."""
    language, _, _, source_name = LOCALES[locale]
    rows = [
        f"R3LONGROW{i:03d} & {i} " + "\\\\"
        for i in range(1, 116)
    ]
    raw_rows = [
        f"R3RAWROW{i:03d} & {i} " + "\\\\"
        for i in range(1, 116)
    ]
    return "\n".join([
        rf"\DocumentMetadata{{lang={language},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\usepackage{longtable}",
        rf"\ufcsetup{{type=doctoral-thesis,document-language={locale},"
        r"tables=tabularray,print-mode=single-sided,cover=false,"
        r"coat-of-arms=false,catalog-card=false,"
        r"title={R3 Mixed Table List Regression},author={Synthetic Test Author}}",
        r"\begin{document}",
        r"\pretextual",
        r"\ufcPrintListOfTables",
        r"\textual",
        rf"\section{{R3-TABLES-{locale.upper()}}}",
        rf"\legend{{table}}{{R3SHORT-{locale.upper()}}}",
        rf"\ufcSource{{R3-SHORT-{locale.upper()} synthetic source}}",
        r"\begin{ufcobject}[here]",
        r"  \begin{tabular}{rr}",
        r"  Group & Value \\",
        r"  1 & 10 \\",
        r"  \end{tabular}",
        r"\end{ufcobject}",
        r"\begin{longabnttblr}[",
        rf"  caption={{R3LONG-{locale.upper()} long multipage table}},",
        rf"  label={{tab:r3-long-{locale}}},",
        rf"  remark{{{source_name}}}={{R3-LONGSOURCE-{locale.upper()}}},",
        r"]{colspec={X[l] X[r]},rowhead=1,width=0.85\linewidth}",
        r"\toprule",
        r"R3LONGHEADER & R3LONGVALUE \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{longabnttblr}",
        r"\begin{longtable}{rr}",
        rf"\caption{{R3RAW-{locale.upper()} native longtable}}\label{{tab:r3-native-{locale}}}\\",
        r"\hline",
        r"R3RAWHEADER & R3RAWVALUE \\",
        r"\hline",
        r"\endfirsthead",
        r"\hline",
        r"R3RAWHEADER & R3RAWVALUE \\",
        r"\hline",
        r"\endhead",
        *raw_rows,
        r"\hline",
        r"\end{longtable}",
        r"\end{document}",
        "",
    ])


def command(args: list[str], log: Path) -> None:
    """Run TeX or Poppler without discarding failure evidence."""
    with log.open("w", encoding="utf-8") as out:
        completed = subprocess.run(args, cwd=ROOT, stdout=out,
                                   stderr=subprocess.STDOUT, text=True, check=False)
    if completed.returncode:
        tail = "\n".join(log.read_text(errors="replace").splitlines()[-55:])
        raise RuntimeError(f"{args[0]} returned {completed.returncode}:\n{tail}")


def check_pdf(locale: str) -> dict:
    """Compile with the installed TeX toolchain and compare LOT and real PDF."""
    language, heading, label, _ = LOCALES[locale]
    directory = ARTIFACTS / locale
    directory.mkdir(parents=True, exist_ok=True)
    source = directory / f"r3-table-list-{locale}.tex"
    source.write_text(make_source(locale), encoding="utf-8")
    job = source.stem
    expected_sha = os.getenv("SOURCE_COMMIT_SHA")
    actual_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    if expected_sha and expected_sha != actual_sha:
        raise ValueError("Checkout/source SHA differs from CI head")
    for phase in (1, 2, 3):
        command(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-jobname={job}",
             f"-output-directory={directory}", str(source)],
            directory / f"{job}-pass{phase}.stdout",
        )
    pdf = directory / f"{job}.pdf"
    lot = directory / f"{job}.lot"
    if not pdf.is_file() or not lot.is_file():
        raise ValueError("Source-built PDF or native .lot is missing")
    extracted = subprocess.check_output(
        ["pdftotext", "-layout", str(pdf), "-"], cwd=ROOT, text=True
    )
    pages = [page for page in extracted.split("\f") if page.strip()]
    heading_pages = [
        (index, page) for index, page in enumerate(pages)
        if any(line.strip().upper() == heading for line in page.splitlines())
    ]
    if len(heading_pages) != 1:
        raise ValueError(
            f"{locale}: expected one List-of-Tables heading, got {len(heading_pages)}"
        )
    page_index, list_page = heading_pages[0]
    short = f"R3SHORT-{locale.upper()}"
    long = f"R3LONG-{locale.upper()}"
    raw = f"R3RAW-{locale.upper()}"
    lot_text = lot.read_text(encoding="utf-8", errors="replace")
    failures = []
    # Check the actual .lot source before relying on extracted page text.
    for marker in (short, long, raw):
        if lot_text.count(marker) != 1:
            failures.append(f"lot.{marker}.entry_count={lot_text.count(marker)}")
        if list_page.count(marker) != 1:
            failures.append(f"pdf.list.{marker}.entry_count={list_page.count(marker)}")
    failures += table_list_failures(list_page, locale)
    body = "\f".join(pages[page_index + 1:])
    for marker in (short, long, raw, "R3LONGROW115", "R3RAWROW115",
                   f"R3-LONGSOURCE-{locale.upper()}"):
        if marker not in body:
            failures.append(f"pdf.body.missing={marker}")
    if len(pages) < 3:
        failures.append("pdf.not_multipage")
    # Require all three localized captions, including native longtable.
    numbers = [
        int(match.group(1)) for line in list_page.splitlines()
        if (match := re.match(rf"^\s*{re.escape(label)}\s+(\d+)\b",
                              line, flags=re.I))
    ]
    if numbers != [1, 2, 3]:
        failures.append(f"pdf.list.nonsequential={numbers}")
    receipt = {
        "locale": locale, "status": "FAIL" if failures else "AUTOMATED_PARTIAL",
        "source_commit_sha": actual_sha, "source_sha256": digest(source),
        "pdf_sha256": digest(pdf), "lot_sha256": digest(lot),
        "page_count": len(pages), "table_list_physical_page": page_index + 1,
        "list_numbers": numbers, "failures": sorted(set(failures)),
        "human_visual_approval": "PENDING",
        "full_manuscript_certification": False,
    }
    (directory / "receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if failures:
        raise ValueError(f"{locale}: mixed table-list regression: {failures}")
    print(f"R3-TABLE-LIST-EVIDENCE status=PASS locale={locale} "
          f"tables=3 pages={len(pages)} pdf_sha256={receipt['pdf_sha256']}")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    selftest()
    if args.selftest:
        return 0
    if not args.locale:
        parser.error("--locale required unless --selftest is supplied")
    check_pdf(args.locale)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"R3-TABLE-LIST-EVIDENCE status=FAIL reason={error}", file=sys.stderr)
        sys.exit(1)

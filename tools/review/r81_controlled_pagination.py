#!/usr/bin/env python3
"""Controlled real-PDF R8.1 experiment using the original native longtable path.

It compares identical content, real localized content, and localized content
with a last-row page-break guard. It never changes runtime or release artifacts.
"""
from __future__ import annotations

import argparse
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
sys.path.insert(0, str(ROOT / "tests/integration/frontmatter"))
R4 = runpy.run_path(str(ROOT / "tests/integration/frontmatter/generate-comprehensive-corpus.py"))
READABLE = runpy.run_path(str(ROOT / "tools/review/generate_readable_28.py"))
PROSE = R4["PROSE"]
LABELS = READABLE["STRINGS"]
EXPECTED_ROWS = 85


def run(*command: str) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True,
                               capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"{command}: stdout={completed.stdout[-6000:]} "
                           f"stderr={completed.stderr[-2000:]}")
    return completed.stdout


def source(locale: str, translated: bool, guarded: bool) -> str:
    # Match the actual R8.1 corpus's native longtable and linguistic inputs.
    effective = locale if translated else "pt"
    dictionary = LABELS[effective]
    header_case = dictionary["header_case"]
    header_value = dictionary["header_value"]
    row_case = dictionary["native_case"]
    title = dictionary["nativetable"]
    intro, discussion = PROSE[effective]
    lines = [
        rf"\DocumentMetadata{{lang={LOCALES[locale]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\usepackage{longtable}",
        r"\ufcsetup{type=research-project,tables=tabularray,document-language="
        + locale
        + r",print-mode=single-sided,cover=false,coat-of-arms=false,"
        + r"catalog-card=false,author={Controlled Author},"
        + r"title={Controlled Pagination},year={2026},location={Fortaleza}}",
        r"\begin{document}",
        rf"\section{{{title}}}",
    ]
    # Reuse real locale-specific R4 prose, not an invented pseudo-translation.
    lines.extend((intro + " " + discussion + r"\par") for _ in range(9))
    lines.extend([
        r"\begin{longtable}{rr}",
        rf"\caption{{{title}}}\label{{tab:r81-controlled}}" + r"\\",
        r"\hline",
        f"{header_case} & {header_value} " + r"\\",
        r"\hline",
        r"\endfirsthead",
        f"{header_case} & {header_value} " + r"\\",
        r"\hline",
        r"\endhead",
    ])
    for n in range(1, EXPECTED_ROWS + 1):
        lines.append(f"R81ROW{n:03d} {row_case} & {n} " + r"\\")
        if guarded and n == EXPECTED_ROWS - 1:
            lines.append(r"\nopagebreak[4]")
    lines.extend([r"\hline", r"\end{longtable}", r"\end{document}"])
    return "\n".join(lines) + "\n"


def check_pdf(pdf: Path) -> dict:
    pages = run("pdftotext", "-layout", str(pdf), "-").split("\f")
    pages = [page for page in pages if page.strip()]
    positions: dict[int, list[int]] = {}
    for index, page in enumerate(pages, 1):
        for row in re.findall(r"R81ROW(\d{3})", page):
            positions.setdefault(int(row), []).append(index)
    missing = sorted(set(range(1, EXPECTED_ROWS + 1)) - positions.keys())
    duplicated = {str(value): pages for value, pages in positions.items()
                  if len(pages) != 1}
    last_page = positions.get(EXPECTED_ROWS, [None])[0]
    last_rows = sorted(value for value, pages in positions.items()
                       if last_page in pages) if last_page else []
    return {
        "pages": len(pages),
        "last_row_page": last_page,
        "last_page_row_count": len(last_rows),
        "last_page_rows": last_rows,
        "single_final_row": len(last_rows) == 1,
        "missing_rows": missing,
        "duplicated_rows": duplicated,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/r81-controlled-pagination")
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    experiments = {}
    for mode, translated, guarded in (
        ("identical-content", False, False),
        ("localized-content", True, False),
        ("localized-guarded", True, True),
    ):
        by_locale = {}
        for locale in LOCALES:
            tex = out / f"{mode}-{locale}.tex"
            tex.write_text(source(locale, translated, guarded), encoding="utf-8")
            for _ in range(3):
                run("pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                    "-output-directory=" + str(out), str(tex))
            by_locale[locale] = check_pdf(tex.with_suffix(".pdf"))
        experiments[mode] = by_locale
    comparisons = {}
    for mode, per_locale in experiments.items():
        comparisons[mode] = {
            "rows_on_last_page": {
                locale: measurement["last_page_row_count"]
                for locale, measurement in per_locale.items()
            },
            "identical_row_distribution": len({
                tuple(measurement["last_page_rows"])
                for measurement in per_locale.values()
            }) == 1,
            "single_last_row_locales": [
                locale for locale, measurement in per_locale.items()
                if measurement["single_final_row"]
            ],
        }
    report = {
        "classification": "DIAGNOSTIC_NOT_HUMAN_NORMATIVE_ACCEPTANCE",
        "structure": "native-longtable-85-rows",
        "real_translation_source": [
            "tests/integration/frontmatter/generate-comprehensive-corpus.py",
            "tools/review/generate_readable_28.py",
        ],
        "experiments": experiments,
        "comparisons": comparisons,
    }
    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print("R81-CONTROLLED-SUMMARY " +
          json.dumps(comparisons, ensure_ascii=False), flush=True)
    errors = []
    for mode, per_locale in experiments.items():
        for locale, measurement in per_locale.items():
            if measurement["missing_rows"] or measurement["duplicated_rows"]:
                errors.append(f"{mode}/{locale}: missing/duplicated rows")
    for locale, measurement in experiments["localized-guarded"].items():
        if measurement["single_final_row"]:
            errors.append(f"localized-guarded/{locale}: final row still orphaned")
    if errors:
        raise SystemExit("R81-CONTROLLED-FAIL " + "; ".join(errors))


if __name__ == "__main__":
    main()

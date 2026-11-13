#!/usr/bin/env python3
"""R8.1 controlled pagination experiment; does not alter runtime or release PDFs."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
TRANSLATED = {
    "pt": ("Execução controlada", "Caso de observação", "Valor medido"),
    "en": ("Controlled execution", "Observation case", "Measured value"),
    "es": ("Ejecución controlada", "Caso de observación", "Valor medido"),
    "fr": ("Exécution contrôlée", "Cas d'observation", "Valeur mesurée"),
}


def run(*command: str) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True,
                               capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"{command}: {completed.stderr[-3000:]}")
    return completed.stdout


def source(locale: str, translated: bool) -> str:
    # Keep row IDs and numeric values invariant across locales.
    heading, first, second = TRANSLATED[locale if translated else "pt"]
    front = [
        rf"\DocumentMetadata{{lang={LOCALES[locale]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\ufcsetup{type=research-project,document-language=" + locale
        + r",print-mode=single-sided,cover=false,coat-of-arms=false,"
        + r"catalog-card=false,author={Controlled Author},"
        + r"title={Controlled Pagination},year={2026},location={Fortaleza}}",
        r"\begin{document}",
        rf"\section{{{heading}}}",
    ]
    paragraph = (
        "This fixed-length passage precedes the tables and tests the same "
        "available vertical space independently from localization settings. "
        "Every run uses identical bytes in this paragraph."
        if not translated else
        f"{first} e {second}. "
        + ("A repetição de palavras pode modificar as quebras de linha. " * 3)
    )
    front.extend([paragraph + r"\par"] * 9)
    front.extend([
        r"\begin{longabnttblr}[caption={Controlled multi-page table},"
        r"label={tab:controlled}]{colspec={X[l] X[r]},rowhead=1,width=0.80\linewidth}",
        r"\toprule",
        f"{first} & {second} " + r"\\",
        r"\midrule",
    ])
    for n in range(1, 126):
        label = f"R81ROW{n:03d}"
        if translated:
            label += " " + first
        front.append(f"{label} & {n} " + r"\\")
    front.extend([r"\bottomrule", r"\end{longabnttblr}", r"\end{document}"])
    return "\n".join(front) + "\n"


def check_pdf(pdf: Path) -> dict:
    pages = run("pdftotext", "-layout", str(pdf), "-").split("\f")
    pages = [p for p in pages if p.strip()]
    ids = {}
    for number, page in enumerate(pages, 1):
        for row in re.findall(r"R81ROW(\d{3})", page):
            ids.setdefault(int(row), []).append(number)
    missing = sorted(set(range(1, 126)) - ids.keys())
    duplicate = {str(k): v for k, v in ids.items() if len(v) != 1}
    last_page = ids.get(125, [None])[0]
    final_rows = [n for n, p in ids.items() if last_page in p]
    return {
        "pages": len(pages),
        "last_row_page": last_page,
        "final_table_page_row_count": len(final_rows),
        "final_table_page_row_ids": sorted(final_rows),
        "potential_single_row_final_page": len(final_rows) == 1,
        "missing_rows": missing,
        "duplicated_rows": duplicate,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/r81-controlled-pagination")
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    report = {"scope": "diagnostic_only", "source": "common class",
              "experiments": {}, "same_content_comparison": {},
              "translated_content_comparison": {}}
    for translated in (False, True):
        mode = "identical-content" if not translated else "translated-content"
        report["experiments"][mode] = {}
        for loc in LOCALES:
            tex = out / f"{mode}-{loc}.tex"
            tex.write_text(source(loc, translated), encoding="utf-8")
            for _ in range(3):
                run("pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                    "-output-directory=" + str(out), str(tex))
            pdf = tex.with_suffix(".pdf")
            report["experiments"][mode][loc] = check_pdf(pdf)
    for key, mode in (("same_content_comparison", "identical-content"),
                      ("translated_content_comparison", "translated-content")):
        experiments = report["experiments"][mode]
        report[key] = {
            "final_page_rows_by_locale": {
                loc: value["final_table_page_row_count"]
                for loc, value in experiments.items()
            },
            "same_final_page_distribution": len({
                tuple(value["final_table_page_row_ids"])
                for value in experiments.values()
            }) == 1,
        }
    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if any(x["missing_rows"] or x["duplicated_rows"]
           for mode in report["experiments"].values() for x in mode.values()):
        raise SystemExit("FAIL: table rows missing or duplicated")


if __name__ == "__main__":
    main()

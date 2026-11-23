#!/usr/bin/env python3
"""Measure physical PDF margin parity independently of logical page numbers (#598)."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

MARKERS = ("PARITYMARKERFIRST", "PARITYMARKERSECOND")
CM_PER_POINT = 2.54 / 72
EXPECTED_X_CM = (3.0, 2.0)
TOLERANCE_CM = 0.35
ENGINES = ("pdflatex", "lualatex")
INITIAL_PAGES = (1, 2, 3)


def latex_source(*, initial: int, cover: bool, control: bool, catalog: bool = False) -> str:
    if control:
        preamble = (r"\documentclass{article}" "\n"
                    r"\usepackage[a4paper,twoside,top=3cm,bottom=2cm,inner=3cm,outer=2cm]{geometry}" "\n")
        start = "\\begin{document}\n" + f"\\setcounter{{page}}{{{initial}}}\n"
    else:
        preamble = (r"\documentclass{abntexto-ufc}" "\n"
                    "\\ufcsetup{\n"
                    "  type=doctoral-thesis, print-mode=double-sided,\n"
                    "  coat-of-arms=false,\n"
                    f"  catalog-card={'true' if catalog else 'false'},\n"
                    f"  initial-page={initial},\n"
                    f"  cover={'true' if cover else 'false'},\n"
                    "  institution={Universidade Federal do Ceara},\n"
                    "  title={Physical Page Parity}, author={Parity Researcher},\n"
                    "  location={Fortaleza}, year={2026}\n"
                    "}\n")
        # The profile selects duplex geometry, but the base class applies it on explicit layout entry.
        start = "\\begin{document}\n\\twosidelayout\n" + ("\\ufcPrintCover\n" if cover else "")
        if catalog:
            # Include an uncounted catalog sheet between the title and internal recto.
            start += "\\ufcPrintTitlePage\n\\ufcPrintCatalogCard{catalog-card}\n"
        start += "\\ufcPretextualBreak\n
    return (preamble + start
            + "\\noindent \\texttt{" + MARKERS[0] + "}\\par\n"
            + "\\clearpage\n"
            + "\\noindent \\texttt{" + MARKERS[1] + "}\\par\n"
            + "\\end{document}\n")


def extract_markers(pdf: Path) -> tuple[list[float], list[int]]:
    result = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True,
                            text=True, check=True)
    root = ET.fromstring(result.stdout)
    measurements: dict[str, tuple[float, int]] = {}
    for physical_page, page in enumerate(root.findall(".//{*}page"), start=1):
        for word in page.findall(".//{*}word"):
            token = "".join(word.itertext()).strip()
            if token in MARKERS:
                if token in measurements:
                    raise ValueError(f"Duplicate marker: {token}")
                measurements[token] = (round(float(word.attrib["xMin"]) * CM_PER_POINT, 4),
                                       physical_page)
    if set(measurements) != set(MARKERS):
        raise ValueError(f"Missing markers: {set(MARKERS) - set(measurements)}")
    xs = [measurements[m][0] for m in MARKERS]
    pages = [measurements[m][1] for m in MARKERS]
    if pages[1] != pages[0] + 1:
        raise ValueError(f"Nonconsecutive physical pages: {pages}")
    return xs, pages


def run_case(work: Path, engine: str, initial: int, cover: bool, control: bool,
             catalog: bool = False) -> dict:
    name = (f"{'control' if control else 'class'}-{engine}-{initial}-"
            f"{'cover' if cover else 'no-cover'}-{'catalog' if catalog else 'plain'}")
    (work / f"{name}.tex").write_text(
        latex_source(initial=initial, cover=cover, control=control, catalog=catalog),
        encoding="utf-8")
    command = [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
               f"-jobname={name}", f"{name}.tex"]
    tex_env = dict(os.environ)
    tex_env["TEXINPUTS"] = (str(Path.cwd().resolve()) + os.pathsep
                            + tex_env.get("TEXINPUTS", ""))
    result = subprocess.run(command, cwd=work, env=tex_env,
                            capture_output=True, text=True, timeout=150)
    (work / f"{name}.console.log").write_text(
        result.stdout + "\n" + result.stderr, encoding="utf-8")
    if result.returncode:
        tail = "\n".join(result.stdout.splitlines()[-35:])
        raise RuntimeError(f"Compilation failed: {name}\n{tail}")
    xs, pages = extract_markers(work / f"{name}.pdf")
    expected = list(EXPECTED_X_CM)
    matches = [abs(measured-reference) <= TOLERANCE_CM
               for measured, reference in zip(xs, expected)]
    offset = (1 if cover and not control else 0) + (2 if catalog else 0)
    expected_pages = [1 + offset, 2 + offset]
    physical_pages_match = pages == expected_pages
    return dict(case=name, engine=engine, initial_page=initial, cover=cover,
                catalog_card=catalog, control=control,
                physical_marker_pages=pages, expected_marker_pages=expected_pages,
                left_x_cm=xs, expected_x_cm=expected,
                expected_match=all(matches) and physical_pages_match)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-only", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="Fail on any class parity regression")
    parser.add_argument("--evidence", type=Path,
                        default=Path("artifacts/validation/issue598-parity.json"))
    args = parser.parse_args()
    results = []
    with tempfile.TemporaryDirectory(prefix="issue598-parity-") as temporary:
        work = Path(temporary)
        for engine in ENGINES:
            if not args.control_only:
                # Compile a source-only single-sheet PDF to test the actual included
                # catalog-card path; do not mock \ufcRegisterUncountedPhysicalPage.
                card = work / "catalog-card.tex"
                card.write_text(
                    "\\documentclass{article}\n\\begin{document}\n"
                    "CATALOGCARDTEST\n\\end{document}\n", encoding="utf-8")
                built = subprocess.run(
                    [engine, "-interaction=nonstopmode", "-halt-on-error",
                     "-jobname=catalog-card", "catalog-card.tex"],
                    cwd=work, capture_output=True, text=True, timeout=150)
                if built.returncode or not (work / "catalog-card.pdf").is_file():
                    raise RuntimeError("Catalog-card PDF fixture failed:\n"
                                       + "\n".join(built.stdout.splitlines()[-25:]))
            for initial in (1, 2):
                results.append(run_case(work, engine, initial, False, True))
            if not args.control_only:
                for cover in (False, True):
                    for initial in INITIAL_PAGES:
                        results.append(run_case(work, engine, initial, cover, False))
                        results.append(run_case(work, engine, initial, cover, False, True))
    controls = [x for x in results if x["control"]]
    if any(x["expected_match"] != (x["initial_page"] % 2 == 1) for x in controls):
        raise AssertionError("Control did not discriminate physical from logical parity")
    candidate = [x for x in results if not x["control"]]
    regressions = [x["case"] for x in candidate if not x["expected_match"]]
    status = ("CONTROL_ONLY" if args.control_only else
              "POTENTIAL_PARITY_REGRESSION" if regressions else "NO_PARITY_REGRESSION_DETECTED")
    report = {"schema_version": 1, "issue": 598, "status": status,
              "strict": args.strict, "source_sha": os.environ.get("SOURCE_COMMIT_SHA", ""),
              "expectation": "First internal recto x=3cm; subsequent verso x=2cm",
              "results": results, "regressions": regressions}
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    print("ISSUE598-PARITY-EVIDENCE",
          json.dumps({k: v for k, v in report.items() if k != "results"}, sort_keys=True))
    for case in results:
        print(f"ISSUE598-CASE {case['case']} pages={case['physical_marker_pages']} "
              f"left_x_cm={case['left_x_cm']} expected_match={case['expected_match']}")
    return 1 if args.strict and regressions else 0


if __name__ == "__main__":
    sys.exit(main())

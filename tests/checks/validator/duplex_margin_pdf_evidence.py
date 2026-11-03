#!/usr/bin/env python3
"""Verify print-mode-dependent horizontal margins with class-rendered PDFs."""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "tools" / "validate-ufc-pdf.py"
SCENARIOS = (
    ("single-sided", "single-sided", "pdf-first-page", "PASS"),
    ("single-sided", "double-sided", "pdf-first-page", "FAIL"),
    ("double-sided", "double-sided", "pdf-first-page", "PASS"),
    ("double-sided", "single-sided", "pdf-first-page", "FAIL"),
    ("double-sided-with-cover", "double-sided", "external-cover-first", "PASS"),
    ("double-sided-with-cover", "double-sided", "pdf-first-page", "FAIL"),
    ("double-sided", "double-sided", "external-cover-first", "FAIL"),
)


def fail(message: str) -> None:
    raise SystemExit("Duplex margin PDF evidence: " + message)


def source_contract() -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = runpy.run_path(str(CLI), run_name="duplex_margin_check")
    check = module["check_layout"]
    w = module["A4"][0]
    pt = module["MM"]
    recto = module["RECTO"]
    verso = module["VERSO"]
    require_mode = module["PRINT_MODES"]
    if tuple(require_mode) != ("single-sided", "double-sided"):
        fail("CLI canonical mode choices have drifted")
    if tuple(module["PAGE_ACCOUNTING"]) != ("pdf-first-page", "external-cover-first"):
        fail("CLI canonical page-accounting choices have drifted")
    for mode in require_mode:
        for page_index in range(1, 5):
            side = verso if mode == "double-sided" and page_index % 2 == 0 else recto
            left, right = side["left_mm"] * pt, side["right_mm"] * pt
            # Tight but inside the allowed catalog margins; measured text is synthetic
            # only in this unit-level calibration. Real PDFs are checked below.
            ok_page = (w, module["A4"][1], [
                ("LEFT", left + 2, 110, left + 15, 120),
                ("RIGHT", w - right - 15, 110, w - right - 2, 120),
            ])
            other_pages = [(w, module["A4"][1], []) for _ in range(page_index - 1)]
            result = check(other_pages + [ok_page], mode)[-1]
            if result.status != "PASS":
                fail(f"unit positive mode={mode} page={page_index}: {result.evidence}")
            # Deliberately move one word beyond the chosen side's bounding box.
            violation_page = (w, module["A4"][1], [
                ("LEFT", left - 10, 110, left, 120)
            ])
            other_pages = [(w, module["A4"][1], []) for _ in range(page_index - 1)]
            result = check(other_pages + [violation_page], mode)[-1]
            if result.status != "FAIL":
                fail(f"unit negative mode={mode} page={page_index}: {result.evidence}")
    # An uncounted external cover must shift duplex parity exactly once.
    right = w - recto["right_mm"] * pt
    inside = (w, module["A4"][1], [("RIGHT", right - 15, 110, right - 2, 120)])
    excluded_cover = (w, module["A4"][1], [("OUTER", 0, 110, 15, 120)])
    if check([excluded_cover, inside], "double-sided", "external-cover-first")[-1].status != "PASS":
        fail("external cover did not shift inner recto or was measured as body text")
    if check([excluded_cover, inside], "double-sided", "pdf-first-page")[-1].status != "FAIL":
        fail("incorrect physical parity unexpectedly passed")
    # An unnumbered interior catalog card still occupies its physical side.
    catalog = (w, module["A4"][1], [])
    next_recto = (w, module["A4"][1], [("RIGHT", right - 15, 110, right - 2, 120)])
    if check([excluded_cover, inside, catalog, next_recto], "double-sided", "external-cover-first")[-1].status != "PASS":
        fail("catalog card incorrectly changed physical parity")
    for wrong_mode, wrong_accounting in (("unexpected-mode", "pdf-first-page"), ("double-sided", "unknown-accounting"), ("single-sided", "external-cover-first")):
        try:
            check([excluded_cover, inside], wrong_mode, wrong_accounting)
        except ValueError:
            continue
        fail(f"invalid combination was accepted: {wrong_mode}/{wrong_accounting}")
    try:
        check([], "unexpected-mode")
    except ValueError:
        pass
    else:
        fail("unknown print mode was accepted")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()

    source_contract()
    records = {}
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-duplex-") as directory:
        for pdf_mode, selected_mode, accounting, expected in SCENARIOS:
            pdf = args.pdf_dir / f"geometry-{pdf_mode}.pdf"
            if not pdf.is_file() or pdf.stat().st_size == 0:
                fail(f"missing actual compiled PDF: {pdf}")
            digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
            hashes[pdf_mode] = digest
            report_path = Path(directory) / f"{pdf_mode}-as-{selected_mode}-{accounting}.json"
            result = subprocess.run(
                [
                    sys.executable, str(CLI), str(pdf),
                    "--profile", "portable",
                    "--document-type", "doctoral-thesis",
                    "--print-mode", selected_mode,
                    "--page-accounting", accounting,
                    "--format", "json", "--output", str(report_path),
                ],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            if result.returncode not in (0, 1) or not report_path.is_file():
                fail(
                    f"missing CLI report for {pdf_mode}/{selected_mode}: "
                    f"exit={result.returncode}; stderr={result.stderr[-800:]}"
                )
            report = json.loads(report_path.read_text(encoding="utf-8"))
            checks = {entry["id"]: entry for entry in report["checks"]}
            observed = checks.get("layout.margins", {}).get("status")
            if observed != expected:
                fail(f"{pdf_mode}/{selected_mode}: expected {expected}, got {observed} "
                     f"({checks.get('layout.margins', {}).get('evidence')})")
            if report.get("print_mode") != selected_mode:
                fail(f"{pdf_mode}/{selected_mode}: report did not retain selected mode")
            if report.get("page_accounting") != accounting:
                fail(f"{pdf_mode}/{selected_mode}: report did not retain accounting mode")
            if f"page_accounting={accounting}" not in checks["layout.margins"]["evidence"]:
                fail("layout evidence omitted the user-selected physical page model")
            if checks.get("layout.a4", {}).get("status") != "PASS":
                fail(f"{pdf_mode}/{selected_mode}: PDF was not A4")
            key = f"{pdf_mode}-as-{selected_mode}-{accounting}"
            records[key] = {
                "pdf_file": pdf.name,
                "pdf_mode": pdf_mode,
                "print_mode": selected_mode,
                "page_accounting": accounting,
                "pdf_sha256": digest,
                "margins": expected,
                "negative_control": expected == "FAIL",
            }
            print(
                "DUPLEX-MARGIN-PDF-EVIDENCE "
                f"surface=cli-deep actual_pdf={pdf_mode} selected={selected_mode} page_accounting={accounting} "
                f"layout_margins={observed} result=PASS"
            )

    if len(hashes) != 3 or len(set(hashes.values())) != 3:
        fail("expected three distinct source-bound PDF fixtures")
    payload = {
        "status": "PASS",
        "schema_version": 1,
        "source_sha": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
        ).stdout.strip(),
        "scope": "horizontal text bounds; explicit print mode; automatic-partial",
        "actual_pdf_count": len(hashes),
        "scenarios": records,
        "limits": [
            "Print mode is user-supplied and is not automatically inferred from a PDF.",
            "This does not validate top and bottom margins or semantic text order.",
            "Even internal physical pages are verso only for double-sided printing.",
            "A separately included outer cover is A4-checked but excluded from inner-block margin measurement.",
            "Interior catalog-card pages keep their physical parity even when not numbered.",
        ],
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "DUPLEX-MARGIN-PDF-EVIDENCE surface=cli-deep status=PASS "
        "real_pdfs=3 scenarios=7 positive=3 negative=4 rule_ids_preserved=true"
    )


if __name__ == "__main__":
    main()

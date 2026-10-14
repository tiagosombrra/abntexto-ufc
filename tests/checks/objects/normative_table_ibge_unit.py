#!/usr/bin/env python3
"""Bounded IBGE 1993 §4.6 and §4.6.1 unit evidence from controlled PDFs.

This oracle does not infer whether a physical unit is necessary from unknown
documents. The caller supplies that normative applicability assumption for
each controlled fixture; only visible placement and notation are measured.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

TESTS_DIR = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))
from path_resolver import ROOT  # noqa: E402

TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from pdf_measurement import PDFMeasurementError, bbox_pages, find_marker, normalize  # noqa: E402

TITLE_MARKER = "UFCIBGEUNITCAP"
HEADER_MARKER = "UFCIBGEUNITHEAD"
FIRST_ROW_MARKER = "UFCIBGEUNITR1"
LAST_ROW_MARKER = "UFCIBGEUNITR3"
SOURCE_MARKER = "UFCIBGEUNITSRC"
UNIT_PATTERN = re.compile(r"\(\s*KG\s*\)")
EXPECTED = {
    "unit-present": ("required", "PASS", True),
    "required-missing": ("required", "FAIL", False),
    "not-applicable": ("not-applicable", "NOT_APPLICABLE", False),
}


def evaluate(pdf: Path, scenario: str) -> dict:
    """Evaluate one controlled PDF without extending a catalog proof state."""
    pages = bbox_pages(pdf)
    if len(pages) != 1:
        raise PDFMeasurementError(
            f"controlled single-page fixture changed page count: {len(pages)}"
        )
    page, title = find_marker(pages, TITLE_MARKER)
    _, header = find_marker(pages, HEADER_MARKER)
    _, first = find_marker(pages, FIRST_ROW_MARKER)
    _, last = find_marker(pages, LAST_ROW_MARKER)
    _, source = find_marker(pages, SOURCE_MARKER)

    # Reject broken fixture geometry rather than treat it as normative evidence.
    ordered = (
        page.index == 1
        and title.box.y_max < header.box.y_min
        and header.box.y_max < first.box.y_min
        and first.box.y_max < last.box.y_min
        and last.box.y_max < source.box.y_min
    )
    if not ordered:
        raise PDFMeasurementError("controlled PDF title/header/rows/source order drifted")

    # Inspect only the right-hand header, not an unrelated mention of (kg)
    # in a title, a data cell, another column, or the source attribution.
    tolerance = max(5.0, header.box.height * 0.6)
    header_suffix = [
        word for word in page.words
        if abs(word.box.center_y - header.box.center_y) <= tolerance
        and header.box.x_max - 1.0 <= word.box.x_min
        and word.box.x_min <= header.box.x_max + 65.0
        and normalize(word.text) != normalize(HEADER_MARKER)
    ]
    header_suffix.sort(key=lambda word: word.box.x_min)
    observed_suffix = "".join(normalize(word.text) for word in header_suffix)
    count = len(UNIT_PATTERN.findall(observed_suffix))
    observed = count == 1
    applicability, status, expected_observed = EXPECTED[scenario]

    return {
        "schema_version": 1,
        "component": "table-ibge-conditional-unit-final-pdf",
        "scenario": scenario,
        "catalog_parent": "table.ibge",
        "source": "IBGE Normas de apresentacao tabular, 3 ed., 1993",
        "clause": ["4.6", "4.6.1"],
        "proof_state": "automatic-partial",
        "applicability": applicability,
        "status": "PASS" if observed else ("FAIL" if applicability == "required" else "NOT_APPLICABLE"),
        "expected_status": status,
        "expected_header_unit_present": expected_observed,
        "observed_header_unit_present": observed,
        "observed_parenthesized_kg_count": count,
        "scope": "one controlled single-page numeric table; PDF text and coordinates",
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "evidence": {
            "page": page.index,
            "header_marker_box": header.box.to_dict(),
            "title_above_header": title.box.y_max < header.box.y_min,
            "header_above_numeric_rows": header.box.y_max < first.box.y_min,
            "source_below_numeric_rows": last.box.y_max < source.box.y_min,
            "header_suffix_extracted": observed_suffix,
            "unit_lexeme": "(kg)",
            "unit_only_measured_in_column_header": True,
        },
        "manual_review": [
            "Scenario applicability is declared, not inferred from arbitrary PDF text.",
            "Unit meaning and accuracy relative to real data are not established.",
            "Other valid units, locations in indicator columns, and divided-by-constant units are not tested.",
            "Other IBGE table criteria and document-wide exceptions are outside scope.",
        ],
        "unrelated_normative_proof_promoted": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--expect", choices=sorted(EXPECTED), required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha", default="")
    args = parser.parse_args()
    if not args.pdf.is_file():
        raise SystemExit(f"IBGE unit fixture missing: {args.pdf}")
    try:
        result = evaluate(args.pdf, args.expect)
    except PDFMeasurementError as exc:
        raise SystemExit(f"IBGE unit PDF evidence failed: {exc}") from exc

    result["source_commit_sha"] = args.commit_sha
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "IBGE-TABLE-UNIT-EVIDENCE "
        f"scenario={args.expect} applicability={result['applicability']} "
        f"observed={result['status']} expected={result['expected_status']} "
        f"header_unit={result['observed_header_unit_present']} "
        "proof_state=automatic-partial"
    )
    if result["status"] != result["expected_status"]:
        raise SystemExit(f"IBGE conditional-unit verdict mismatch: {result['status']}")
    if result["observed_header_unit_present"] != result["expected_header_unit_present"]:
        raise SystemExit("IBGE conditional-unit header occurrence mismatch")


if __name__ == "__main__":
    main()

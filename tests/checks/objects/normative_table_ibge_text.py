#!/usr/bin/env python3
"""Bounded IBGE 1993 §4.2/§4.10 PDF evidence for a controlled numeric table.

This is NOT a general ABNT/IBGE compliance verdict. It verifies the caption
and the explicit source of the scenario's own numeric data; it does not claim
that an unrelated PDF's source has been audited. IBGE §4.10 itself has scoped
publication-level source exceptions that must be handled by future validators.
"""
from __future__ import annotations

import argparse
import json
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

CAPTION_MARKER = "UFCIBGECAP"
SOURCE_MARKER = "UFCIBGESRC"
FIRST_ROW_MARKER = "UFCIBGER1"
LAST_ROW_MARKER = "UFCIBGER3"


def fail(message: str) -> None:
    raise SystemExit(f"IBGE title/source PDF evidence failed: {message}")


def evaluate(pdf: Path) -> dict:
    pages = bbox_pages(pdf)
    if len(pages) != 1:
        fail(f"controlled one-page scenario changed page count: {len(pages)}")
    page, caption = find_marker(pages, CAPTION_MARKER)
    _, first = find_marker(pages, FIRST_ROW_MARKER)
    _, last = find_marker(pages, LAST_ROW_MARKER)
    if page.index != 1:
        fail("caption on unexpected page")

    # A generated "Tabela 1" may appear before the caption even where §4.1
    # does not require numbering (one table). Observe it, never promote to
    # proof of normative numbering applicability.
    row_tolerance = max(6.0, caption.box.height)
    caption_line = [
        w for w in page.words
        if abs(w.box.center_y - caption.box.center_y) <= row_tolerance
    ]
    identifying_label = [
        w for w in caption_line
        if normalize(w.text).rstrip(":") == "TABELA"
        and w.box.x_min < caption.box.x_min
    ]
    descriptive_tail = [
        w for w in caption_line
        if w.box.x_min > caption.box.x_max
        and normalize(w.text) not in {"", "-", "—", ":"}
    ]
    caption_valid = bool(
        caption.box.y_max < first.box.y_min
        and identifying_label
        and descriptive_tail
    )

    source_words = [
        w for w in page.words if normalize(w.text) == normalize(SOURCE_MARKER)
    ]
    labels = [
        w for w in page.words if normalize(w.text).rstrip(":") in {"FONTE", "FONTES"}
    ]
    matching_source = [
        (label, word) for label in labels for word in source_words
        if label.box.x_min < word.box.x_min
        and abs(label.box.center_y - word.box.center_y) <= max(7.0, word.box.height)
        and label.box.y_min > last.box.y_max
    ]
    source_valid = len(source_words) == 1 and len(matching_source) == 1

    return {
        "schema_version": 1,
        "component": "table-ibge-title-source-final-pdf",
        "result": "PASS" if caption_valid and source_valid else "FAIL",
        "proof_state": "automatic-partial",
        "scope": "controlled single numeric table; PDF text and page coordinates",
        "historical_guidance": "IBGE Normas de apresentacao tabular (3 ed., 1993)",
        "evidence": [
            {
                "id": "table.ibge.title-observation",
                "clause": "4.2",
                "status": "PASS" if caption_valid else "FAIL",
                "observations": {
                    "caption_marker": caption.box.to_dict(),
                    "caption_above_body": caption.box.y_max < first.box.y_min,
                    "identification_label_observed": bool(identifying_label),
                    "descriptive_words_observed": bool(descriptive_tail),
                    "page": page.index,
                },
            },
            {
                "id": "table.ibge.source-observation",
                "clause": "4.10",
                "status": "PASS" if source_valid else "FAIL",
                "observations": {
                    "label_and_responsible_source_on_same_line": bool(matching_source),
                    "source_marker_count": len(source_words),
                    "source_below_body": bool(matching_source),
                    "page": page.index,
                    "publication_level_exception_not_assessed": True,
                },
            },
        ],
        "manual_review": [
            "Title adequately states nature, geographic and temporal scope.",
            "Source identification accurately attributes the real underlying data.",
            "Whether §4.10's publication-level exception applies.",
            "Conditional units, explanatory notes and multipage continuation are not evaluated.",
        ],
        "unrelated_normative_proof_promoted": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--expect", choices=("pass", "source-missing"), required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha", default="")
    args = parser.parse_args()
    if not args.pdf.is_file():
        fail(f"PDF missing: {args.pdf}")
    try:
        result = evaluate(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))
    result["source_commit_sha"] = args.commit_sha
    checks = {item["id"]: item["status"] for item in result["evidence"]}
    expected = (
        {"table.ibge.title-observation": "PASS", "table.ibge.source-observation": "PASS"}
        if args.expect == "pass" else
        {"table.ibge.title-observation": "PASS", "table.ibge.source-observation": "FAIL"}
    )
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "IBGE-TABLE-TEXT-EVIDENCE "
        f"expected={args.expect} measured={result['result']} "
        f"title={checks['table.ibge.title-observation']} "
        f"source={checks['table.ibge.source-observation']} "
        "proof_state=automatic-partial"
    )
    if checks != expected:
        fail(f"PDF evidence does not match expected positive/negative scenario: {checks}")


if __name__ == "__main__":
    main()

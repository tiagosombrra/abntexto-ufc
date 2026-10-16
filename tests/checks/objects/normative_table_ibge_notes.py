#!/usr/bin/env python3
"""Bounded IBGE 1993 §§4.10-4.12 final-PDF note order evidence.

Applicability is declared by the controlled fixture. This does not infer
whether real document content needs a general or a specific note.
"""
from __future__ import annotations

import argparse
import hashlib
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

CAPTION = "UFCIBGENOTECAP"
SOURCE = "UFCIBGENOTESRC"
GENERAL = "UFCIBGENOTEGEN"
SPECIFIC = "UFCIBGENOTESPEC"
FIRST = "UFCIBGENOTER1"
LAST = "UFCIBGENOTER3"

# Presence obligations are explicit controlled hypotheses, not inferred facts.
SCENARIOS = {
    "both-present": (True, True, True, "PASS"),
    "general-missing": (True, True, True, "FAIL"),
    "callout-missing": (True, True, True, "FAIL"),
    "not-applicable": (False, False, False, "NOT_APPLICABLE"),
}


def optional_word(page, token):
    hits = [w for w in page.words if normalize(w.text) == normalize(token)]
    if len(hits) > 1:
        raise PDFMeasurementError(f"duplicate controlled note marker {token}")
    return hits[0] if hits else None


def evaluate(pdf: Path, scenario: str) -> dict:
    pages = bbox_pages(pdf)
    if len(pages) != 1:
        raise PDFMeasurementError("controlled note PDF must be exactly one page")
    page = pages[0]
    _, title = find_marker(pages, CAPTION)
    _, source = find_marker(pages, SOURCE)
    _, first = find_marker(pages, FIRST)
    _, last = find_marker(pages, LAST)
    general = optional_word(page, GENERAL)
    specific = optional_word(page, SPECIFIC)

    # Callout is only counted directly after its own marked data-row token.
    # A numeric value, footnote tag, or printed page number elsewhere is not proof.
    callouts = [
        w for w in page.words
        if normalize(w.text) == "1"
        and first.box.x_max - 1.0 <= w.box.x_min <= first.box.x_max + 13.0
        and abs(w.box.center_y - first.box.center_y) <= max(7.0, first.box.height)
    ]
    callout_present = len(callouts) == 1
    structure_ok = title.box.y_max < first.box.y_min < last.box.y_min < source.box.y_min
    order_ok = bool(
        general is not None
        and specific is not None
        and source.box.y_max < general.box.y_min < specific.box.y_min
    )
    any_notes = general is not None or specific is not None or callout_present
    required_general, required_specific, required_callout, expected = SCENARIOS[scenario]

    if not structure_ok:
        raise PDFMeasurementError("controlled table geometry drifted")
    if not any_notes:
        status = "NOT_APPLICABLE"
    elif (
        general is not None
        and specific is not None
        and callout_present
        and order_ok
    ):
        status = "PASS"
    else:
        status = "FAIL"

    # An N/A scenario may not silently accept extra note material.
    if scenario == "not-applicable" and any_notes:
        status = "FAIL"
    if scenario != "not-applicable" and not any_notes:
        status = "FAIL"

    return {
        "schema_version": 1,
        "component": "table-ibge-notes-order-final-pdf",
        "scenario": scenario,
        "status": status,
        "expected_status": expected,
        "proof_state": "automatic-partial",
        "catalog_parent": "table.ibge",
        "clauses": ["4.10", "4.11", "4.11.1", "4.12", "4.12.1"],
        "applicability": {
            "general_note_required_by_fixture": required_general,
            "specific_note_required_by_fixture": required_specific,
            "specific_callout_required_by_fixture": required_callout,
        },
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "observations": {
            "page": 1,
            "source_box": source.box.to_dict(),
            "general_box": general.box.to_dict() if general else None,
            "specific_box": specific.box.to_dict() if specific else None,
            "row1_box": first.box.to_dict(),
            "callout_count_near_row1": len(callouts),
            "source_then_general_then_specific": order_ok,
            "no_note_material": not any_notes,
        },
        "manual_review": [
            "Fixture declaration determines if notes are needed, not PDF semantics.",
            "Clarity and adequacy of both descriptions remain unverified.",
            "Multiple specific note ordering (§4.12.2) and exceptions are untested.",
        ],
        "unrelated_normative_proof_promoted": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--expect", choices=sorted(SCENARIOS), required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha", default="")
    args = parser.parse_args()
    if not args.pdf.is_file():
        raise SystemExit(f"IBGE notes PDF missing: {args.pdf}")
    try:
        result = evaluate(args.pdf, args.expect)
    except PDFMeasurementError as exc:
        raise SystemExit(f"IBGE notes PDF measurement failed: {exc}") from exc
    result["source_commit_sha"] = args.commit_sha
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "IBGE-NOTES-PDF-EVIDENCE "
        f"scenario={args.expect} measured={result['status']} "
        f"expected={result['expected_status']} "
        f"source_general_specific_order="
        f"{result['observations']['source_then_general_then_specific']} "
        "proof_state=automatic-partial"
    )
    if result["status"] != result["expected_status"]:
        raise SystemExit("IBGE notes conditional expectation mismatch")


if __name__ == "__main__":
    main()

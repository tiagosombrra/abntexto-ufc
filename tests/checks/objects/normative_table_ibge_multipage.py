#!/usr/bin/env python3
"""Controlled final-PDF evidence for IBGE 1993 section 8.3 (multi-page table).

This script does not certify arbitrary tables, lateral facing-page exceptions,
semantic source attribution, or the normative adequacy of the table title.
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
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize  # noqa: E402

CAPTION = "UFCIBGEMPCAP"
HEADS = ("UFCIBGEMPHEAD", "UFCIBGEMPVALUE")
SOURCE = "UFCIBGEMPSRC"
NOTE = "UFCIBGEMPGEN"
ROW_PREFIX = "UFCIBGEMPROW"
ROWS = 168
SCENARIOS = {
    "positive": ("PASS", "PASS", "PASS"),
    "header-missing": ("FAIL", "PASS", "PASS"),
    "source-missing": ("PASS", "PASS", "FAIL"),
}


def fail(message: str) -> None:
    raise SystemExit(f"IBGE multipage PDF evidence: {message}")


def tokens(page, marker: str):
    return [word for word in page.words if normalize(word.text) == marker]


def marker_kind(word: str) -> str:
    return normalize(word).strip("()[]{}:;., ")


def evaluate(pdf: Path, scenario: str) -> dict:
    try:
        pages = bbox_pages(pdf)
    except PDFMeasurementError as error:
        fail(str(error))
    if not 3 <= len(pages) <= 8:
        fail(f"expected a true multipage table of 3–8 pages; measured {len(pages)}")

    observed_rows = []
    page_evidence = []
    all_source = []
    all_note = []
    title_ok = True
    headings_ok = True
    continuations_ok = True
    body_ok = True

    for i, page in enumerate(pages):
        title = tokens(page, CAPTION)
        headers = {head: tokens(page, head) for head in HEADS}
        rows = []
        for word in page.words:
            match = re.fullmatch(ROW_PREFIX + r"(\d{3})", normalize(word.text))
            if match:
                rows.append((int(match.group(1)), word))
        page_source = tokens(page, SOURCE)
        page_note = tokens(page, NOTE)
        all_source.extend((page.index, word) for word in page_source)
        all_note.extend((page.index, word) for word in page_note)

        expected_label = (
            "CONTINUA" if i == 0
            else "CONCLUSAO" if i == len(pages) - 1
            else "CONTINUACAO"
        )
        found_labels = [
            (expected_label, word)
            for word in page.words
            if marker_kind(word.text) == expected_label
        ]
        if len(title) != 1:
            title_ok = False
        if len(found_labels) != 1:
            continuations_ok = False
        if not rows:
            body_ok = False
        if len(title) == 1 and rows and title[0].box.y_max >= rows[0][1].box.y_min:
            title_ok = False

        for head, matches in headers.items():
            if len(matches) != 1:
                headings_ok = False
            elif rows and matches[0].box.y_max >= rows[0][1].box.y_min:
                headings_ok = False
        if rows:
            observed_rows.extend((number, page.index, word) for number, word in rows)
        page_evidence.append({
            "page": page.index,
            "caption_count": len(title),
            "head_counts": {head: len(headers[head]) for head in HEADS},
            "expected_continuation": expected_label,
            "continuation_count": len(found_labels),
            "row_count": len(rows),
            "first_row": rows[0][0] if rows else None,
            "last_row": rows[-1][0] if rows else None,
            "source_count": len(page_source),
            "general_note_count": len(page_note),
        })

    numbers = [number for number, _page, _word in observed_rows]
    if numbers != list(range(1, ROWS + 1)):
        body_ok = False
    if not observed_rows or observed_rows[0][1] != 1:
        body_ok = False
    if not observed_rows or observed_rows[-1][1] != len(pages):
        body_ok = False

    foot_ok = len(all_source) == 1 and len(all_note) == 1
    if foot_ok:
        source_page, source = all_source[0]
        note_page, note = all_note[0]
        foot_ok = (
            source_page == note_page == len(pages)
            and observed_rows[-1][2].box.y_max < source.box.y_min
            and source.box.y_max < note.box.y_min
        )
        last_page = pages[-1]
        labels = [
            word for word in last_page.words
            if marker_kind(word.text) == "FONTE"
            and abs(word.box.center_y - source.box.center_y) < 9
            and word.box.x_min < source.box.x_min
        ]
        foot_ok = foot_ok and len(labels) == 1

    structural = title_ok and continuations_ok and body_ok
    statuses = (
        "PASS" if headings_ok else "FAIL",
        "PASS" if structural else "FAIL",
        "PASS" if foot_ok else "FAIL",
    )
    expected = SCENARIOS[scenario]
    return {
        "schema_version": 1,
        "component": "table-ibge-multipage-final-pdf",
        "scenario": scenario,
        "status": "PASS" if statuses == ("PASS", "PASS", "PASS") else "FAIL",
        "expected_statuses": dict(zip(("headers", "continuation_and_rows", "terminal_foot"), expected)),
        "measured_statuses": dict(zip(("headers", "continuation_and_rows", "terminal_foot"), statuses)),
        "matches_declared_scenario": statuses == expected,
        "source_commit_sha": "",
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "pdf_pages": len(pages),
        "catalog_parent": "table.ibge",
        "clauses": ["8.3.a", "8.3.b", "8.3.c", "8.3.e", "4.10", "4.11"],
        "proof_state": "automatic-partial",
        "measurements": page_evidence,
        "limits": [
            "The 168 synthetic rows are not actual statistical observations.",
            "Controlled PDF text/page boxes do not prove semantic source accuracy.",
            "The 8.3.d closing rule and facing-page row-order exception are outside this test.",
            "Other PDF engines, tables, page breaks and formatting variations need separate evidence.",
        ],
        "unrelated_normative_proof_promoted": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--commit-sha", default="")
    args = parser.parse_args()
    if not args.pdf.is_file() or not args.pdf.stat().st_size:
        fail(f"missing/empty compiled PDF: {args.pdf}")
    result = evaluate(args.pdf, args.scenario)
    result["source_commit_sha"] = args.commit_sha
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    evidence = result["measured_statuses"]
    print(
        "IBGE-MULTIPAGE-PDF-EVIDENCE "
        f"scenario={args.scenario} pages={result['pdf_pages']} "
        f"headers={evidence['headers']} "
        f"continuation={evidence['continuation_and_rows']} "
        f"foot={evidence['terminal_foot']} "
        f"matches_expected={str(result['matches_declared_scenario']).lower()} "
        "proof_state=automatic-partial"
    )
    if not result["matches_declared_scenario"]:
        fail(f"controlled PDF diverged from declared scenario: {evidence}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bounded IBGE 1993 §8.3(d) vector line separation on real long tables.

The footer-separating horizontal rule must occur only on the concluding
part carrying the final table row. Text controls live in the sibling checker.
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
from pdf_vector_measurement import vector_rules  # noqa: E402
from normative_table_ibge_vector import cluster_axis_rules  # noqa: E402

ROW_PREFIX = "UFCIBGEMPROW"
HEADER_LEFT = "UFCIBGEMPHEAD"
HEADER_RIGHT = "UFCIBGEMPVALUE"
SOURCE = "UFCIBGEMPSRC"
EXPECTED_ROWS = 168


def fail(msg: str) -> None:
    raise SystemExit("IBGE §8.3(d) vector PDF evidence: " + msg)


def matches(page, token: str):
    return [word for word in page.words if normalize(word.text) == token]


def row_markers(page):
    found = []
    for word in page.words:
        number = re.fullmatch(ROW_PREFIX + r"(\d{3})", normalize(word.text))
        if number:
            found.append((int(number.group(1)), word))
    return found


def evaluate(pdf: Path, negative: bool) -> dict:
    try:
        pages = bbox_pages(pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))
    if not 3 <= len(pages) <= 8:
        fail(f"expected real controlled 3–8 page table, found {len(pages)}")

    per_page = []
    all_numbers = []
    for i, page in enumerate(pages):
        rows = row_markers(page)
        if not rows:
            fail(f"page {page.index} has no controlled data row markers")
        all_numbers.extend(number for number, _ in rows)
        header_left = matches(page, HEADER_LEFT)
        header_right = matches(page, HEADER_RIGHT)
        if len(header_left) != 1 or len(header_right) != 1:
            fail(f"page {page.index} lacks the repeated, calibrated table column heads")
        left = header_left[0].box.x_min
        right = header_right[0].box.x_max
        if right - left < 110:
            fail(f"page {page.index} has invalid table header span")
        last_row = rows[-1][1]
        if not last_row.box.y_max < page.height - 15:
            fail(f"page {page.index} has insufficient bottom margin to measure footer")
        last = i == len(pages) - 1
        source = matches(page, SOURCE)
        if (len(source) == 1) != last:
            fail(f"page {page.index} violated terminal-only source contract")

        # Rule candidates must span the whole table, not short glyph strokes,
        # numeric underscores, or vertical borders. Only consider the region
        # BELOW the final row printed on that physical PDF page.
        y_min = last_row.box.y_max + 1.0
        y_max = source[0].box.y_min - 1.0 if last else page.height - 15.0
        if y_min >= y_max:
            fail(f"page {page.index} has an inverted row/footer measurement interval")
        try:
            rules = vector_rules(
                pdf, page=page.index, axis_tolerance_pt=0.5,
                max_rule_thickness_pt=2.0, min_rule_length_pt=5.0
            )
        except PDFMeasurementError as exc:
            fail(f"page {page.index}: {exc}")
        # A printed full-width line may become two contiguous SVG
        # subpaths (one per tabularray column). Reuse the existing calibrated
        # logical-rule merger before checking the table's horizontal extent.
        # Testing each raw segment separately causes false negatives.
        horizontal = cluster_axis_rules(
            rules, orientation="horizontal", cluster_tolerance_pt=1.8
        )
        covering = [
            item for item in horizontal
            if item.length >= 0.78 * (right - left)
            and item.box.x_min <= left + 6
            and item.box.x_max >= right - 6
        ]
        footer = [
            line for line in covering
            if y_min <= line.box.center_y <= y_max
        ]
        per_page.append({
            "page": page.index,
            "last_data_row": rows[-1][0],
            "row_bbox": last_row.box.to_dict(),
            "horizontal_rule_total": len(covering),
            "possible_footer_rule_count": len(footer),
            "possible_footer_rules": [line.to_dict() for line in footer],
            "is_concluding_page": last,
            "measurement_interval": [round(y_min, 3), round(y_max, 3)],
        })

    if all_numbers != list(range(1, EXPECTED_ROWS + 1)):
        fail("synthetic rows did not form a complete monotonic 001..168 sequence")

    terminal_count = per_page[-1]["possible_footer_rule_count"]
    early_pages = per_page[:-1]
    nonterminal_counts = [p["possible_footer_rule_count"] for p in early_pages]
    # A real defect can produce several overdrawn contours of one printed
    # rule. The deduplication above is exact enough for these controlled PDFs;
    # require a single terminal rule and strictly no early footer rule.
    # Fail closed for an ambiguous negative: the positive terminal footer
    # must still exist. Otherwise absence of the *correct* final boundary
    # could masquerade as proof of detecting the injected premature rule.
    if terminal_count != 1:
        fail(f"terminal footer-rule calibration expected exactly one, got {terminal_count}")
    actual = "PASS" if all(n == 0 for n in nonterminal_counts) else "FAIL"
    expected = "FAIL" if negative else "PASS"
    return {
        "schema_version": 1,
        "component": "table-ibge-multipage-footer-vector-final-pdf",
        "clause": "IBGE 1993 §8.3(d)",
        "catalog_parent": "table.ibge",
        "proof_state": "automatic-partial",
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "pages": len(pages),
        "expected": expected,
        "observed": actual,
        "matches_expected": actual == expected,
        "terminal_rule_count": terminal_count,
        "nonterminal_rule_counts": nonterminal_counts,
        "measurements": per_page,
        "known_limits": [
            "Only the horizontal full-width footer boundary in one controlled table is measured.",
            "The physical vector line is distinct from OCR or semantic page interpretation.",
            "The original per-page text, ordering, header and notes checks run separately.",
            "§8.3(c) confronting-page column exception is not assessed.",
            "Other rules, data content and tables do not receive compliance certification.",
        ],
        "unrelated_normative_proof_promoted": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--scenario", required=True, choices=("positive", "nonterminal-rule"))
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--commit-sha", default="")
    args = parser.parse_args()
    if not args.pdf.is_file() or args.pdf.stat().st_size == 0:
        fail(f"actual PDF absent: {args.pdf}")
    result = evaluate(args.pdf, args.scenario == "nonterminal-rule")
    result["scenario"] = args.scenario
    result["source_commit_sha"] = args.commit_sha
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "IBGE-MULTIPAGE-VECTOR-EVIDENCE "
        f"scenario={args.scenario} pages={result['pages']} "
        f"terminal_rules={result['terminal_rule_count']} "
        f"intermediate_rules={result['nonterminal_rule_counts']} "
        f"measured={result['observed']} expected={result['expected']} "
        f"matched={str(result['matches_expected']).lower()} "
        "proof_state=automatic-partial"
    )
    if not result["matches_expected"]:
        fail(
            "real-PDF horizontal footer boundary mismatches expected control "
            f"(last={result['terminal_rule_count']}, "
            f"others={result['nonterminal_rule_counts']})"
        )


if __name__ == "__main__":
    main()

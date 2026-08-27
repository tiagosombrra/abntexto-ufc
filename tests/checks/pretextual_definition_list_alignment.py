#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from pdf_measurement import PDFMeasurementError, bbox_pages, find_marker

ALIGNMENT_TOLERANCE_PT = 1.0
COLUMN_TOLERANCE_PT = 1.0


def fail(message: str) -> None:
    raise SystemExit(f"Pre-textual definition-list alignment failed: {message}")


def locate(pdf: Path, marker: str):
    try:
        return find_marker(bbox_pages(pdf), marker)
    except PDFMeasurementError as exc:
        fail(f"{pdf}: {exc}")


def row_measurement(
    pdf: Path,
    label: str,
    definition_start: str,
    *,
    vertical_anchor: str = "top",
) -> dict[str, float | int | str]:
    label_page, label_word = locate(pdf, label)
    definition_page, definition_word = locate(pdf, definition_start)
    if label_page.index != definition_page.index:
        fail(
            f"{pdf}: row markers {label!r}/{definition_start!r} landed on different pages "
            f"({label_page.index}/{definition_page.index})"
        )

    if vertical_anchor == "top":
        label_y = label_word.box.y_min
        definition_y = definition_word.box.y_min
    elif vertical_anchor == "bottom":
        # A mathematical glyph can have a different ascender/top extent than
        # ordinary text even on the same baseline.  The controlled M/Malha
        # fixture has no descenders, so the lower bbox edge is the stable
        # same-baseline proxy while remaining sensitive to vertical shifts.
        label_y = label_word.box.y_max
        definition_y = definition_word.box.y_max
    else:
        fail(f"unsupported vertical anchor: {vertical_anchor}")

    vertical_delta = abs(label_y - definition_y)
    if vertical_delta > ALIGNMENT_TOLERANCE_PT:
        fail(
            f"{pdf}: row {label!r}/{definition_start!r} is vertically misaligned "
            f"using {vertical_anchor} anchor: delta={vertical_delta:.3f}pt > "
            f"{ALIGNMENT_TOLERANCE_PT:.3f}pt"
        )

    return {
        "page": label_page.index,
        "label": label,
        "definition_start": definition_start,
        "vertical_anchor": vertical_anchor,
        "label_x": label_word.box.x_min,
        "definition_x": definition_word.box.x_min,
        "label_y": label_y,
        "definition_y": definition_y,
        "vertical_delta_pt": vertical_delta,
    }


def assert_column_consistency(rows: list[dict[str, float | int | str]], key: str) -> float:
    values = [float(row[key]) for row in rows]
    spread = max(values) - min(values)
    if spread > COLUMN_TOLERANCE_PT:
        fail(
            f"column {key} is inconsistent across rows: "
            f"spread={spread:.3f}pt > {COLUMN_TOLERANCE_PT:.3f}pt"
        )
    return spread


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regression-check two-column alignment in abbreviation and symbol lists."
    )
    parser.add_argument("abbreviations_pdf", type=Path)
    parser.add_argument("symbols_pdf", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    for pdf in (args.abbreviations_pdf, args.symbols_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    abbreviation_rows = [
        row_measurement(args.abbreviations_pdf, "ABNT", "Associação"),
        row_measurement(args.abbreviations_pdf, "UFC", "Universidade"),
    ]
    symbol_rows = [
        row_measurement(
            args.symbols_pdf,
            "M",
            "Malha",
            vertical_anchor="bottom",
        ),
    ]

    label_spread = assert_column_consistency(abbreviation_rows, "label_x")
    definition_spread = assert_column_consistency(abbreviation_rows, "definition_x")

    payload = {
        "schema_version": 1,
        "component": "pretextual-definition-list-alignment",
        "result": "PASS",
        "alignment_tolerance_pt": ALIGNMENT_TOLERANCE_PT,
        "column_tolerance_pt": COLUMN_TOLERANCE_PT,
        "abbreviation_rows": abbreviation_rows,
        "symbol_rows": symbol_rows,
        "abbreviation_label_x_spread_pt": label_spread,
        "abbreviation_definition_x_spread_pt": definition_spread,
        "normative_contract_changed": False,
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    max_delta = max(
        float(row["vertical_delta_pt"])
        for row in [*abbreviation_rows, *symbol_rows]
    )
    print(
        "LAYOUT-EVIDENCE pretextual-definition-lists status=PASS "
        f"rows={len(abbreviation_rows) + len(symbol_rows)} "
        f"max_vertical_delta_pt={max_delta:.3f} "
        f"label_x_spread_pt={label_spread:.3f} "
        f"definition_x_spread_pt={definition_spread:.3f}"
    )


if __name__ == "__main__":
    main()

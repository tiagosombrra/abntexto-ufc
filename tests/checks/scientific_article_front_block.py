#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from pdf_measurement import PDFMeasurementError, bbox_pages, find_marker, normalize, typography_runs

MM_TO_PT = 72.0 / 25.4
CENTER_TOLERANCE_PT = 5.0
FONT_TOLERANCE_PT = 0.25


def fail(message: str) -> None:
    raise SystemExit(f"scientific article front-block validation failed: {message}")


def unique_typography_run(runs, marker: str):
    wanted = normalize(marker)
    matches = [run for run in runs if normalize(run.text) == wanted]
    if len(matches) != 1:
        fail(f"typography marker {marker!r}: expected one run, found {len(matches)}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate rendered scientific-article front-block evidence.")
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    try:
        pages = bbox_pages(args.pdf)
        runs = typography_runs(args.pdf)
        title_page, title_word = find_marker(pages, "ARTICLEFRONTTITLE")
        author_page, author_word = find_marker(pages, "ARTICLEFRONTAUTHOR")
        submitted_page, submitted_word = find_marker(pages, "Submetido")
        approved_page, approved_word = find_marker(pages, "Aprovado")
        summary_page, summary_word = find_marker(pages, "ARTICLESUMMARYMARKER")
        note_page, note_word = find_marker(pages, "ARTICLENOTEMARKER")
    except PDFMeasurementError as exc:
        fail(str(exc))

    required_pages = {
        title_page.index,
        author_page.index,
        submitted_page.index,
        approved_page.index,
        summary_page.index,
        note_page.index,
    }
    if required_pages != {1}:
        fail(f"required article front-block elements must share page 1, observed pages={sorted(required_pages)}")

    title_run = unique_typography_run(runs, "ARTICLEFRONTTITLE")
    bold_control = unique_typography_run(runs, "ARTICLEBOLDCONTROL")
    regular_control = unique_typography_run(runs, "ARTICLEBODYREGULARCONTROL")

    if abs(title_run.font_size - 12.0) > FONT_TOLERANCE_PT:
        fail(f"primary title must render at 12 pt, measured={title_run.font_size:.3f}")
    if title_run.font_id != bold_control.font_id:
        fail("primary title does not match the same-document bold calibration")
    if title_run.font_id == regular_control.font_id:
        fail("primary title unexpectedly matches the regular calibration font")

    text_area_left = 30.0 * MM_TO_PT
    text_area_right = title_page.width - 20.0 * MM_TO_PT
    expected_center = (text_area_left + text_area_right) / 2.0
    center_delta = abs(title_word.box.center_x - expected_center)
    if center_delta > CENTER_TOLERANCE_PT:
        fail(
            "primary title is not centered in the normative text area: "
            f"expected={expected_center:.3f}, measured={title_word.box.center_x:.3f}, delta={center_delta:.3f}"
        )

    if not (
        title_word.box.center_y
        < author_word.box.center_y
        < submitted_word.box.center_y
        < summary_word.box.center_y
        < note_word.box.center_y
    ):
        fail("required article front-block elements are not vertically ordered as title/author/dates/summary/footnote")

    if abs(submitted_word.box.center_y - approved_word.box.center_y) > 2.0:
        fail("submission and approval dates are expected on the same front-block line")

    if note_word.box.center_y < note_page.height * 0.65:
        fail("article author metadata note was not rendered in the footnote region")

    text = args.pdf.with_suffix(".front-block.txt")
    import subprocess

    completed = subprocess.run(
        ["pdftotext", "-layout", str(args.pdf), str(text)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"pdftotext failed: {completed.stderr.strip()}")
    raw = text.read_text(encoding="utf-8", errors="replace")
    text.unlink(missing_ok=True)
    compact = re.sub(r"\s+", " ", raw).strip()

    for marker in (
        "ARTICLEFRONTTITLE",
        "ARTICLEFRONTAUTHOR",
        "ARTICLENOTEMARKER",
        "Submetido em: 1 de setembro de 2026.",
        "Aprovado em: 5 de setembro de 2026.",
        "Resumo:",
        "ARTICLESUMMARYMARKER",
    ):
        if marker not in compact:
            fail(f"required rendered marker is missing: {marker}")

    for forbidden in ("BANCA EXAMINADORA", "TRABALHO DE CONCLUSÃO DE CURSO"):
        if forbidden in compact.upper():
            fail(f"academic-work front matter leaked into scientific article output: {forbidden}")

    print(
        "ARTICLE-FRONT-BLOCK-EVIDENCE status=PASS "
        "required=title,authorship,author-note,submission-date,approval-date,primary-summary "
        f"title_pt={title_run.font_size:.1f} title_center_delta_pt={center_delta:.3f} "
        "title_weight=bold-calibrated author_note_region=footnote-page-bottom "
        "optional_foreign_elements_promoted=0 recommendations_promoted=0"
    )


if __name__ == "__main__":
    main()

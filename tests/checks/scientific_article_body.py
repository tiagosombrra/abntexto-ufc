#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from pdf_measurement import PDFMeasurementError, bbox_pages, normalize, typography_runs

MM_TO_PT = 72.0 / 25.4
FONT_TOLERANCE_PT = 0.25
HORIZONTAL_TOLERANCE_PT = 5.0
LINE_SPACING_TOLERANCE_PT = 0.75
LINE_GROUP_TOLERANCE_PT = 1.5


def fail(message: str) -> None:
    raise SystemExit(f"scientific article body validation failed: {message}")


def folded(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", ascii_text).casefold().strip()


def extract_text(pdf: Path) -> str:
    output = pdf.with_suffix(".body.txt")
    completed = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(output)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"pdftotext failed: {completed.stderr.strip()}")
    raw = output.read_text(encoding="utf-8", errors="replace")
    output.unlink(missing_ok=True)
    return raw


def validate_structure(raw: str) -> None:
    text = folded(raw)
    required = (
        ("introducao", "introdução"),
        ("desenvolvimento", "desenvolvimento"),
        ("consideracoes finais", "considerações finais"),
        ("referencias", "referências"),
    )
    positions: list[int] = []
    for token, label in required:
        position = text.find(token)
        if position < 0:
            fail(f"required article structure element is missing: {label}")
        positions.append(position)
    if positions != sorted(positions) or len(set(positions)) != len(positions):
        fail(f"required article structure is not ordered as introduction/development/final considerations/references: {positions}")


def unique_word(page, marker: str):
    wanted = normalize(marker)
    matches = [word for word in page.words if normalize(word.text) == wanted]
    if len(matches) != 1:
        fail(f"marker {marker!r}: expected one word on page {page.index}, found {len(matches)}")
    return matches[0]


def find_unique_word(pages, marker: str):
    wanted = normalize(marker)
    matches = [
        (page, word)
        for page in pages
        for word in page.words
        if normalize(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(f"marker {marker!r}: expected one word, found {len(matches)}")
    return matches[0]


def unique_run_containing(runs, marker: str):
    wanted = normalize(marker)
    matches = [run for run in runs if wanted in normalize(run.text)]
    if len(matches) != 1:
        fail(f"typography marker {marker!r}: expected one containing run, found {len(matches)}")
    return matches[0]


def group_lines(page):
    words = sorted(page.words, key=lambda word: (word.box.center_y, word.box.x_min))
    lines: list[dict[str, object]] = []
    for word in words:
        if not lines or abs(word.box.center_y - float(lines[-1]["center_y"])) > LINE_GROUP_TOLERANCE_PT:
            lines.append({"center_y": word.box.center_y, "words": [word]})
            continue
        line_words = lines[-1]["words"]
        assert isinstance(line_words, list)
        line_words.append(word)
        lines[-1]["center_y"] = sum(item.box.center_y for item in line_words) / len(line_words)
    for line in lines:
        line_words = line["words"]
        assert isinstance(line_words, list)
        line_words.sort(key=lambda word: word.box.x_min)
    return lines


def line_bounds(line) -> tuple[float, float, float]:
    words = line["words"]
    assert isinstance(words, list) and words
    return (
        min(word.box.x_min for word in words),
        max(word.box.x_max for word in words),
        float(line["center_y"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate scientific-article textual structure and body typography.")
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    raw = extract_text(args.pdf)
    validate_structure(raw)

    try:
        pages = bbox_pages(args.pdf)
        runs = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    start_page, start_word = find_unique_word(pages, "ARTICLEBODYSTART")
    end_page, end_word = find_unique_word(pages, "ARTICLEBODYEND")
    margin_page, margin_word = find_unique_word(pages, "ARTICLEMARGINCONTROL")
    cal_one_page, cal_one = find_unique_word(pages, "ARTICLECALONE")
    cal_two_page, cal_two = find_unique_word(pages, "ARTICLECALTWO")
    cal_three_page, cal_three = find_unique_word(pages, "ARTICLECALTHREE")

    if len({start_page.index, end_page.index, margin_page.index, cal_one_page.index, cal_two_page.index, cal_three_page.index}) != 1:
        fail("body and calibration markers must share one controlled page")

    if end_word.box.center_y < start_word.box.center_y:
        fail("body end marker appears before body start marker")

    lines = group_lines(start_page)
    body_lines = [
        line
        for line in lines
        if start_word.box.center_y - LINE_GROUP_TOLERANCE_PT
        <= float(line["center_y"])
        <= end_word.box.center_y + LINE_GROUP_TOLERANCE_PT
    ]
    if len(body_lines) < 4:
        fail(f"controlled body paragraph must span at least four natural lines, observed={len(body_lines)}")

    first_x_min, _, _ = line_bounds(body_lines[0])
    expected_indent_pt = 20.0 * MM_TO_PT
    measured_indent_pt = first_x_min - margin_word.box.x_min
    indent_delta = abs(measured_indent_pt - expected_indent_pt)
    if indent_delta > HORIZONTAL_TOLERANCE_PT:
        fail(
            "article body first-line indent is not 2 cm: "
            f"expected={expected_indent_pt:.3f}, measured={measured_indent_pt:.3f}, delta={indent_delta:.3f}"
        )

    continuation_left_deltas = [
        abs(line_bounds(line)[0] - margin_word.box.x_min)
        for line in body_lines[1:]
    ]
    max_left_delta = max(continuation_left_deltas)
    if max_left_delta > HORIZONTAL_TOLERANCE_PT:
        fail(f"article body continuation lines are not aligned to the text margin: max_delta={max_left_delta:.3f}")

    expected_right = start_page.width - 20.0 * MM_TO_PT
    right_deltas = [abs(line_bounds(line)[1] - expected_right) for line in body_lines[:-1]]
    max_right_delta = max(right_deltas)
    if max_right_delta > HORIZONTAL_TOLERANCE_PT:
        fail(f"article body non-final lines are not justified to the right margin: max_delta={max_right_delta:.3f}")

    body_centers = [line_bounds(line)[2] for line in body_lines]
    body_gaps = [later - earlier for earlier, later in zip(body_centers, body_centers[1:])]
    if any(gap <= 0 for gap in body_gaps):
        fail(f"article body line order is invalid: gaps={body_gaps}")
    body_gap = sum(body_gaps) / len(body_gaps)

    calibration_gaps = [
        cal_two.box.center_y - cal_one.box.center_y,
        cal_three.box.center_y - cal_two.box.center_y,
    ]
    if any(gap <= 0 for gap in calibration_gaps):
        fail(f"single-spacing calibration order is invalid: gaps={calibration_gaps}")
    calibration_gap = sum(calibration_gaps) / len(calibration_gaps)
    spacing_delta = abs(body_gap - calibration_gap)
    if spacing_delta > LINE_SPACING_TOLERANCE_PT:
        fail(
            "article body is not single-spaced relative to same-document 12 pt singlesp calibration: "
            f"body_gap={body_gap:.3f}, calibration_gap={calibration_gap:.3f}, delta={spacing_delta:.3f}"
        )

    start_run = unique_run_containing(runs, "ARTICLEBODYSTART")
    end_run = unique_run_containing(runs, "ARTICLEBODYEND")
    font_deltas = [abs(start_run.font_size - 12.0), abs(end_run.font_size - 12.0)]
    if max(font_deltas) > FONT_TOLERANCE_PT:
        fail(
            "article body markers must render at 12 pt: "
            f"start={start_run.font_size:.3f}, end={end_run.font_size:.3f}"
        )
    if start_run.font_id != end_run.font_id:
        fail("article body start/end markers do not share the same regular typography run identity")

    # The line evidence above proves the physical presentation on an article-specific
    # PDF. It intentionally does not promote the retained source contract's proof
    # state; proof-state promotion remains owned by the later evidence-hardening step.
    print(
        "ARTICLE-BODY-EVIDENCE status=PASS "
        "rules=introduction,development,final-considerations,references,body-typography "
        f"body_lines={len(body_lines)} font_pt={start_run.font_size:.1f} "
        f"indent_pt={measured_indent_pt:.3f} indent_delta_pt={indent_delta:.3f} "
        f"max_left_delta_pt={max_left_delta:.3f} max_right_delta_pt={max_right_delta:.3f} "
        f"body_gap_pt={body_gap:.3f} singlesp_calibration_pt={calibration_gap:.3f} "
        f"spacing_delta_pt={spacing_delta:.3f} proof_state_promoted=0"
    )


if __name__ == "__main__":
    main()

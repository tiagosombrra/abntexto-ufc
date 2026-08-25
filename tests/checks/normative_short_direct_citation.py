#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize, typography_runs

SCENARIO = ROOT / "normativa" / "short-direct-citation-scenario.json"
LOCATOR_AUDIT = ROOT / "normativa" / "locator-audit-citations.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"
RULESET_ID = "citations.direct-short"
RULE_IDS = [
    "citation.direct-short.max-lines",
    "citation.direct-short.quotation-marks",
    "citation.direct-short.emphasis",
]

DOUBLE_QUOTE_CHARS = set('"“”„‟«»')
SINGLE_QUOTE_CHARS = set("'‘’‚‛‹›")


def fail(message: str) -> None:
    raise SystemExit(f"Short direct citation oracle failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def page_with_marker(pages: list[Any], marker: str) -> Any:
    wanted = normalize(marker)
    matches = [
        page
        for page in pages
        if any(wanted in normalize(word.text) for word in page.words)
    ]
    if len(matches) != 1:
        fail(
            f"marker {marker!r}: expected one page, "
            f"found {[page.index for page in matches]}"
        )
    return matches[0]


def word_with_marker(page: Any, marker: str) -> tuple[int, Any]:
    wanted = normalize(marker)
    matches = [
        (index, word)
        for index, word in enumerate(page.words)
        if wanted in normalize(word.text)
    ]
    if len(matches) != 1:
        fail(
            f"marker {marker!r}: expected one word on page {page.index}, "
            f"found {[(index, word.text) for index, word in matches]}"
        )
    return matches[0]


def cluster_lines(words: list[Any], tolerance: float = 1.0) -> list[list[Any]]:
    ordered = sorted(words, key=lambda word: (word.box.center_y, word.box.x_min))
    lines: list[list[Any]] = []
    for word in ordered:
        if not lines:
            lines.append([word])
            continue
        center = sum(item.box.center_y for item in lines[-1]) / len(lines[-1])
        if abs(word.box.center_y - center) <= tolerance:
            lines[-1].append(word)
        else:
            lines.append([word])
    for line in lines:
        line.sort(key=lambda word: word.box.x_min)
    return lines


def typography_with_marker(runs: list[Any], marker: str) -> Any:
    wanted = normalize(marker)
    matches = [run for run in runs if wanted in normalize(run.text)]
    if len(matches) != 1:
        fail(
            f"typography marker {marker!r}: expected one run, "
            f"found {[(run.page, run.text) for run in matches]}"
        )
    return matches[0]


def boundary_quote_chars(
    words: tuple[Any, ...],
    marker_index: int,
    marker: str,
    *,
    opening: bool,
) -> list[str]:
    word = words[marker_index]
    raw = word.text
    marker_pos = normalize(raw).find(normalize(marker))
    if marker_pos < 0:
        fail(f"marker {marker!r} not present in boundary word {raw!r}")

    local = raw[:marker_pos] if opening else raw[marker_pos + len(marker) :]
    quote_chars = DOUBLE_QUOTE_CHARS | SINGLE_QUOTE_CHARS
    chars = [char for char in local if char in quote_chars]
    if chars:
        return chars

    neighbor_index = marker_index - 1 if opening else marker_index + 1
    if 0 <= neighbor_index < len(words):
        neighbor = words[neighbor_index]
        if abs(neighbor.box.center_y - word.box.center_y) <= 1.0:
            return [char for char in neighbor.text if char in quote_chars]
    return []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N6 short direct citation presentation from a final PDF."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR_AUDIT)
    policy = load_json(ORACLE_POLICY)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N6"
        or scenario.get("component") != "short-direct-citation"
        or scenario.get("locator_ruleset") != RULESET_ID
    ):
        fail("invalid scenario schema/phase/component/ruleset")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == RULESET_ID
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    if locator_matches[0].get("rule_ids") != RULE_IDS or scenario.get("rules") != RULE_IDS:
        fail("short direct citation rule scope drift")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    selected: dict[str, dict[str, Any]] = {}
    expected_keys = {
        "citation.direct-short.max-lines": {"max_lines"},
        "citation.direct-short.quotation-marks": {"style"},
        "citation.direct-short.emphasis": {"citation_emphasis"},
    }
    for rule_id in RULE_IDS:
        rule = rules.get(rule_id)
        if not isinstance(rule, dict) or rule.get("authority") != "normative":
            fail(f"missing normative rule {rule_id}")
        values = rule.get("values")
        if not isinstance(values, dict) or set(values) != expected_keys[rule_id]:
            fail(f"unexpected contract values for {rule_id}: {values}")
        selected[rule_id] = rule

    max_lines = selected["citation.direct-short.max-lines"]["values"]["max_lines"]
    quote_style = selected["citation.direct-short.quotation-marks"]["values"]["style"]
    citation_emphasis = selected["citation.direct-short.emphasis"]["values"][
        "citation_emphasis"
    ]
    if max_lines != 3 or quote_style != "double" or citation_emphasis is not False:
        fail(
            f"contract drift: max_lines={max_lines} style={quote_style!r} "
            f"citation_emphasis={citation_emphasis}"
        )

    if policy.get("schema_version") != 1 or policy.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")
    font_tolerance = float(policy["tolerances"]["font_size_pt"])

    markers = scenario.get("markers")
    required_markers = {
        "body_control",
        "body_before",
        "quote_open",
        "quote_middle",
        "quote_close",
        "body_after",
    }
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    try:
        pages = bbox_pages(args.pdf)
        runs = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    quote_page = page_with_marker(pages, markers["quote_open"])
    for key in ("body_before", "quote_middle", "quote_close", "body_after"):
        page = page_with_marker(pages, markers[key])
        if page.index != quote_page.index:
            fail(f"controlled citation markers span pages: {key}={page.index}")

    open_index, _ = word_with_marker(quote_page, markers["quote_open"])
    close_index, _ = word_with_marker(quote_page, markers["quote_close"])
    if close_index < open_index:
        fail("quote close marker precedes quote open marker in PDF reading order")

    quote_words = list(quote_page.words[open_index : close_index + 1])
    quote_lines = cluster_lines(quote_words)
    line_count = len(quote_lines)
    max_lines_passed = 1 <= line_count <= int(max_lines)

    opening_chars = boundary_quote_chars(
        quote_page.words, open_index, markers["quote_open"], opening=True
    )
    closing_chars = boundary_quote_chars(
        quote_page.words, close_index, markers["quote_close"], opening=False
    )
    double_marks_passed = (
        bool(opening_chars)
        and bool(closing_chars)
        and all(char in DOUBLE_QUOTE_CHARS for char in opening_chars + closing_chars)
        and not any(char in SINGLE_QUOTE_CHARS for char in opening_chars + closing_chars)
    )

    body_control_run = typography_with_marker(runs, markers["body_control"])
    quote_runs = [
        typography_with_marker(runs, markers[key])
        for key in ("quote_open", "quote_middle", "quote_close")
    ]
    emphasis_samples = []
    emphasis_passed = True
    for key, run in zip(("quote_open", "quote_middle", "quote_close"), quote_runs):
        sample = {
            "marker": markers[key],
            "page": run.page,
            "font_id": run.font_id,
            "family": run.family,
            "font_pt": round(run.font_size, 4),
            "color": run.color,
            "matches_body_font_id": run.font_id == body_control_run.font_id,
            "font_size_delta_pt": round(abs(run.font_size - body_control_run.font_size), 4),
            "matches_body_color": run.color == body_control_run.color,
        }
        emphasis_samples.append(sample)
        emphasis_passed = emphasis_passed and (
            sample["matches_body_font_id"]
            and sample["font_size_delta_pt"] <= font_tolerance
            and sample["matches_body_color"]
        )

    evidence = [
        {
            "rule_id": "citation.direct-short.max-lines",
            "status": "PASS" if max_lines_passed else "FAIL",
            "expected": selected["citation.direct-short.max-lines"]["values"],
            "measured": {
                "page": quote_page.index,
                "line_count": line_count,
                "positive_fixture_evidence_only": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": None,
        },
        {
            "rule_id": "citation.direct-short.quotation-marks",
            "status": "PASS" if double_marks_passed else "FAIL",
            "expected": selected["citation.direct-short.quotation-marks"]["values"],
            "measured": {
                "page": quote_page.index,
                "opening_characters": opening_chars,
                "closing_characters": closing_chars,
                "double_quote_character_class": sorted(DOUBLE_QUOTE_CHARS),
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": None,
        },
        {
            "rule_id": "citation.direct-short.emphasis",
            "status": "PASS" if emphasis_passed else "FAIL",
            "expected": selected["citation.direct-short.emphasis"]["values"],
            "measured": {
                "body_control": {
                    "marker": markers["body_control"],
                    "page": body_control_run.page,
                    "font_id": body_control_run.font_id,
                    "family": body_control_run.family,
                    "font_pt": round(body_control_run.font_size, 4),
                    "color": body_control_run.color,
                },
                "quote_samples": emphasis_samples,
                "same_document_body_typography_control": True,
            },
            "tool": "pdftohtml -xml -zoom 1.0",
            "tolerance": font_tolerance,
        },
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "short-direct-citation",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "evidence": evidence,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N6-EVIDENCE short-direct-citation-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" lines={line_count}"
        + f" opening_marks={json.dumps(opening_chars, ensure_ascii=False)}"
        + f" closing_marks={json.dumps(closing_chars, ensure_ascii=False)}"
        + f" font_control_id={body_control_run.font_id}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

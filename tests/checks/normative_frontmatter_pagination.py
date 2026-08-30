#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "standards" / "frontmatter-pagination-scenario.json"
RULE_ORDER = [
    "pagination.frontmatter.counted-not-numbered",
    "pagination.catalog-data.not-counted",
    "pagination.textual.display-start",
    "frontmatter.start.recto",
]
HEADER_LIMIT_PT = 80.0


def fail(message: str) -> None:
    raise SystemExit(f"Front matter pagination validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def page_text(page: Any) -> str:
    return " ".join(word.text for word in page.words)


def pages_with_phrase(pages: list[Any], phrase: str) -> list[Any]:
    wanted = normalize(phrase)
    return [page for page in pages if wanted in normalize(page_text(page))]


def unique_phrase_page(pages: list[Any], phrase: str) -> Any:
    matches = pages_with_phrase(pages, phrase)
    if len(matches) != 1:
        fail(f"marker {phrase!r}: expected one page, found {[page.index for page in matches]}")
    return matches[0]


def header_arabic_numbers(page: Any) -> list[Any]:
    return [
        word
        for word in page.words
        if word.box.y_min < HEADER_LIMIT_PT and re.fullmatch(r"[0-9]+", word.text.strip())
    ]


def header_roman_numbers(page: Any) -> list[Any]:
    return [
        word
        for word in page.words
        if word.box.y_min < HEADER_LIMIT_PT
        and re.fullmatch(r"[IVXLCDM]+", word.text.strip().upper())
    ]


def header_number_tokens(page: Any) -> list[Any]:
    return header_arabic_numbers(page) + header_roman_numbers(page)


def unique_arabic_header_number(page: Any) -> int | None:
    matches = header_arabic_numbers(page)
    if not matches:
        return None
    if len(matches) != 1:
        fail(
            f"page {page.index}: expected at most one Arabic header page number, "
            f"found {[word.text for word in matches]}"
        )
    return int(matches[0].text)


def record(rule_id: str, status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def derive_scope(contract: dict[str, Any], scope: dict[str, Any]) -> list[str]:
    categories = scope.get("categories")
    kinds = scope.get("kinds")
    validation_checks = scope.get("validation_checks_any")
    if not all(isinstance(value, list) and value for value in (categories, kinds, validation_checks)):
        fail("scenario scope requires non-empty categories, kinds and validation_checks_any")

    selected: list[str] = []
    for rule in contract.get("rules", []):
        if rule.get("authority", "normative") != "normative":
            continue
        if rule.get("category") not in categories or rule.get("kind") not in kinds:
            continue
        checks = rule.get("validation", {}).get("checks", [])
        if not isinstance(checks, list) or not set(checks).intersection(validation_checks):
            continue
        selected.append(rule["id"])
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure front matter front matter pagination/start-side evidence from final PDFs."
    )
    parser.add_argument("duplex_pdf", type=Path)
    parser.add_argument("catalog_pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    for pdf in (args.duplex_pdf, args.catalog_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO)
    if (
        scenario.get("schema_version") != 2

        or scenario.get("component") != "frontmatter-pagination-transition"
    ):
        fail("invalid scenario schema/component")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    derived_scope = derive_scope(contract, scenario.get("scope", {}))
    scenario_rules = scenario.get("rules")
    if scenario_rules != RULE_ORDER:
        fail("scenario rule order drift")
    if set(derived_scope) != set(RULE_ORDER) or len(derived_scope) != 4:
        fail(
            "derived scope drift: "
            f"derived={sorted(derived_scope)} expected={sorted(RULE_ORDER)}"
        )

    try:
        duplex_pages = bbox_pages(args.duplex_pdf)
        catalog_pages = bbox_pages(args.catalog_pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    duplex_spec = scenario.get("duplex")
    catalog_spec = scenario.get("catalog")
    if not isinstance(duplex_spec, dict) or not isinstance(catalog_spec, dict):
        fail("duplex and catalog scenario blocks are required")

    duplex_text_marker = duplex_spec.get("textual_marker")
    frontmatter_markers = duplex_spec.get("frontmatter_markers")
    if not isinstance(duplex_text_marker, str) or not duplex_text_marker:
        fail("duplex textual marker is required")
    if not isinstance(frontmatter_markers, list) or not frontmatter_markers:
        fail("duplex front matter marker list is required")
    if not all(isinstance(marker, str) and marker for marker in frontmatter_markers):
        fail("duplex front matter markers must be non-empty strings")

    duplex_text_page = unique_phrase_page(duplex_pages, duplex_text_marker)
    if duplex_text_page.index <= 1:
        fail("duplex textual marker must follow at least one front matter page")
    duplex_frontmatter_pages = [page for page in duplex_pages if page.index < duplex_text_page.index]

    frontmatter_header_numbers = {
        page.index: [word.text for word in header_number_tokens(page)]
        for page in duplex_frontmatter_pages
        if header_number_tokens(page)
    }
    duplex_text_number = unique_arabic_header_number(duplex_text_page)
    duplex_text_roman = [word.text for word in header_roman_numbers(duplex_text_page)]

    marker_pages: dict[str, int] = {}
    for marker in frontmatter_markers:
        page = unique_phrase_page(duplex_pages, marker)
        if page.index >= duplex_text_page.index:
            fail(f"front matter marker {marker!r} appears at/after textual start")
        marker_pages[marker] = page.index

    title_marker = catalog_spec.get("title_page_marker")
    card_marker = catalog_spec.get("card_marker")
    catalog_text_marker = catalog_spec.get("textual_marker")
    if not all(isinstance(marker, str) and marker for marker in (title_marker, card_marker, catalog_text_marker)):
        fail("catalog title/card/text markers are required")

    catalog_title_page = unique_phrase_page(catalog_pages, title_marker)
    catalog_card_page = unique_phrase_page(catalog_pages, card_marker)
    catalog_text_page = unique_phrase_page(catalog_pages, catalog_text_marker)
    if not (
        catalog_title_page.index < catalog_card_page.index < catalog_text_page.index
        and catalog_card_page.index == catalog_title_page.index + 1
    ):
        fail(
            "catalog fixture physical order invalid: "
            f"title={catalog_title_page.index} card={catalog_card_page.index} "
            f"text={catalog_text_page.index}"
        )

    catalog_title_tokens = [word.text for word in header_number_tokens(catalog_title_page)]
    catalog_card_tokens = [word.text for word in header_number_tokens(catalog_card_page)]
    catalog_text_number = unique_arabic_header_number(catalog_text_page)
    catalog_text_roman = [word.text for word in header_roman_numbers(catalog_text_page)]

    evidence: list[dict[str, Any]] = []

    counted_rule = rules["pagination.frontmatter.counted-not-numbered"]
    counted_expected = counted_rule["values"]
    counted_pass = (
        counted_expected.get("counted") is True
        and counted_expected.get("number_visible") is False
        and not frontmatter_header_numbers
        and duplex_text_number == duplex_text_page.index
        and not duplex_text_roman
    )
    evidence.append(
        record(
            "pagination.frontmatter.counted-not-numbered",
            "PASS" if counted_pass else "FAIL",
            counted_expected,
            {
                "physical_frontmatter_pages": len(duplex_frontmatter_pages),
                "frontmatter_pages_with_visible_header_numbers": frontmatter_header_numbers,
                "first_textual_physical_page": duplex_text_page.index,
                "first_textual_visible_number": duplex_text_number,
                "first_textual_roman_tokens": duplex_text_roman,
                "physical_and_logical_progression_match": duplex_text_number == duplex_text_page.index,
            },
        )
    )

    catalog_rule = rules["pagination.catalog-data.not-counted"]
    catalog_expected = catalog_rule["values"]
    catalog_expected_text_number = catalog_text_page.index - 1
    catalog_pass = (
        catalog_expected.get("counted") is False
        and catalog_expected.get("number_visible") is False
        and not catalog_card_tokens
        and catalog_text_number == catalog_expected_text_number
        and not catalog_text_roman
    )
    evidence.append(
        record(
            "pagination.catalog-data.not-counted",
            "PASS" if catalog_pass else "FAIL",
            catalog_expected,
            {
                "title_page_physical": catalog_title_page.index,
                "title_page_visible_number_tokens": catalog_title_tokens,
                "catalog_card_physical": catalog_card_page.index,
                "catalog_card_visible_number_tokens": catalog_card_tokens,
                "first_textual_physical_page": catalog_text_page.index,
                "first_textual_visible_number": catalog_text_number,
                "first_textual_roman_tokens": catalog_text_roman,
                "expected_visible_number_if_card_uncounted": catalog_expected_text_number,
            },
        )
    )

    textual_rule = rules["pagination.textual.display-start"]
    textual_expected = textual_rule["values"]
    textual_pass = (
        textual_expected.get("display_start") == "first-textual-page"
        and textual_expected.get("numeral_system") == "arabic"
        and not frontmatter_header_numbers
        and duplex_text_number is not None
        and not duplex_text_roman
        and not catalog_title_tokens
        and not catalog_card_tokens
        and catalog_text_number is not None
        and not catalog_text_roman
    )
    evidence.append(
        record(
            "pagination.textual.display-start",
            "PASS" if textual_pass else "FAIL",
            textual_expected,
            {
                "duplex": {
                    "first_textual_physical_page": duplex_text_page.index,
                    "first_textual_visible_number": duplex_text_number,
                    "first_textual_roman_tokens": duplex_text_roman,
                    "preceding_visible_number_tokens": frontmatter_header_numbers,
                },
                "catalog_exception": {
                    "first_textual_physical_page": catalog_text_page.index,
                    "first_textual_visible_number": catalog_text_number,
                    "first_textual_roman_tokens": catalog_text_roman,
                    "title_page_visible_number_tokens": catalog_title_tokens,
                    "catalog_card_visible_number_tokens": catalog_card_tokens,
                },
            },
        )
    )

    recto_rule = rules["frontmatter.start.recto"]
    recto_expected = recto_rule["values"]
    non_recto_markers = {
        marker: page for marker, page in marker_pages.items() if page % 2 == 0
    }
    catalog_exception_ok = (
        catalog_title_page.index % 2 == 1
        and catalog_card_page.index % 2 == 0
        and catalog_card_page.index == catalog_title_page.index + 1
    )
    recto_pass = (
        recto_expected.get("default_start_side") == "recto"
        and recto_expected.get("exception") == "cataloging-data-on-title-page-verso"
        and not non_recto_markers
        and catalog_exception_ok
    )
    evidence.append(
        record(
            "frontmatter.start.recto",
            "PASS" if recto_pass else "FAIL",
            recto_expected,
            {
                "duplex_marker_pages": marker_pages,
                "non_recto_markers": non_recto_markers,
                "catalog_exception": {
                    "title_page": catalog_title_page.index,
                    "catalog_card": catalog_card_page.index,
                    "card_is_immediate_verso": catalog_exception_ok,
                },
            },
        )
    )

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "component": "frontmatter-pagination-transition",
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
        "FRONTMATTER-EVIDENCE frontmatter-pagination-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" duplex_pages={len(duplex_pages)} catalog_pages={len(catalog_pages)}"
        + f" recto_markers={len(marker_pages)}"
    )
    for item in evidence:
        print(
            f"FRONTMATTER-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

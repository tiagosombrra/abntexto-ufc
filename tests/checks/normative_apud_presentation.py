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
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "normativa" / "apud-presentation-scenario.json"
LOCATOR_AUDIT = ROOT / "normativa" / "locator-audit-citations.json"
RULESET_ID = "citations.apud"
RULE_ID = "citation.apud.presentation"


def fail(message: str) -> None:
    raise SystemExit(f"Apud presentation oracle failed: {message}")


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


def citation_window(
    pages: list[Any], before_marker: str, after_marker: str
) -> tuple[Any, list[Any]]:
    page = page_with_marker(pages, before_marker)
    after_page = page_with_marker(pages, after_marker)
    if after_page.index != page.index:
        fail(
            f"citation markers span pages: {before_marker}={page.index}, "
            f"{after_marker}={after_page.index}"
        )
    before_index, _ = word_with_marker(page, before_marker)
    after_index, _ = word_with_marker(page, after_marker)
    if not before_index < after_index:
        fail(
            f"unexpected marker order for {before_marker}/{after_marker}: "
            f"{before_index}, {after_index}"
        )
    words = list(page.words[before_index + 1 : after_index])
    if not words:
        fail(f"generated citation window is empty for {before_marker}/{after_marker}")
    return page, words


def normalized_words(words: list[Any]) -> str:
    return " ".join(normalize(word.text) for word in words)


def validate_fixture(name: str, fixture: Any) -> dict[str, Any]:
    required = {
        "original_citation_key",
        "consulted_citation_key",
        "original_tokens",
        "apud_token",
        "consulted_tokens",
    }
    if not isinstance(fixture, dict) or set(fixture) != required:
        fail(f"invalid {name} fixture specification")
    for key in ("original_citation_key", "consulted_citation_key", "apud_token"):
        if not isinstance(fixture.get(key), str) or not fixture[key]:
            fail(f"{name} {key} must be a non-empty string")
    for key in ("original_tokens", "consulted_tokens"):
        tokens = fixture.get(key)
        if (
            not isinstance(tokens, list)
            or not tokens
            or not all(isinstance(token, str) and token for token in tokens)
        ):
            fail(f"{name} {key} must be a non-empty string list")
    return fixture


def measure_surface(
    name: str,
    fixture: dict[str, Any],
    pages: list[Any],
    before_marker: str,
    after_marker: str,
) -> dict[str, Any]:
    page, words = citation_window(pages, before_marker, after_marker)
    text = normalized_words(words)
    original_presence = {
        token: normalize(token) in text for token in fixture["original_tokens"]
    }
    consulted_presence = {
        token: normalize(token) in text for token in fixture["consulted_tokens"]
    }
    apud_present = normalize(fixture["apud_token"]) in text
    supported = (
        all(original_presence.values())
        and apud_present
        and all(consulted_presence.values())
    )
    return {
        "surface": name,
        "page": page.index,
        "original_citation_key": fixture["original_citation_key"],
        "consulted_citation_key": fixture["consulted_citation_key"],
        "original_tokens": original_presence,
        "apud_token": fixture["apud_token"],
        "apud_present": apud_present,
        "consulted_tokens": consulted_presence,
        "apud_supported": supported,
        "citation_window_word_count": len(words),
        "locator_punctuation_order_typography_and_surface_form_are_observational": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N6 apud presentation support from a final PDF."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR_AUDIT)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N6"
        or scenario.get("component") != "apud-presentation"
        or scenario.get("locator_ruleset") != RULESET_ID
        or scenario.get("rules") != [RULE_ID]
    ):
        fail("invalid scenario schema/phase/component/rule scope")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == RULESET_ID
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    locator_rule = locator_matches[0]
    if locator_rule.get("rule_ids") != [RULE_ID]:
        fail("apud locator rule scope drift")
    if locator_rule.get("status") != "PARTIAL_WITH_REASON":
        fail(f"apud locator status drift: {locator_rule.get('status')}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")
    values = rule.get("values")
    if values != {"apud_supported": True}:
        fail(f"contract drift for {RULE_ID}: {values}")

    fixtures = scenario.get("fixtures")
    if not isinstance(fixtures, dict) or set(fixtures) != {"parenthetical", "textual"}:
        fail("invalid fixture surface specification")
    parenthetical = validate_fixture("parenthetical", fixtures["parenthetical"])
    textual = validate_fixture("textual", fixtures["textual"])

    markers = scenario.get("markers")
    required_markers = {
        "parenthetical_before",
        "parenthetical_after",
        "textual_before",
        "textual_after",
    }
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    surfaces = [
        measure_surface(
            "parenthetical",
            parenthetical,
            pages,
            markers["parenthetical_before"],
            markers["parenthetical_after"],
        ),
        measure_surface(
            "textual",
            textual,
            pages,
            markers["textual_before"],
            markers["textual_after"],
        ),
    ]
    supported_surfaces = sum(1 for surface in surfaces if surface["apud_supported"])
    rule_passed = supported_surfaces == len(surfaces)

    measured = {
        "apud_supported": rule_passed,
        "surface_count": len(surfaces),
        "supported_surface_count": supported_surfaces,
        "surfaces": surfaces,
        "positive_fixture_evidence_only": True,
        "exact_apud_format_not_strengthened": True,
    }
    evidence = [
        {
            "rule_id": RULE_ID,
            "status": "PASS" if rule_passed else "FAIL",
            "expected": values,
            "measured": measured,
            "tool": "pdftotext -bbox-layout",
            "tolerance": None,
        }
    ]
    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if rule_passed else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "apud-presentation",
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
        "N6-EVIDENCE apud-presentation-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" surfaces={len(surfaces)}"
        + f" supported_surfaces={supported_surfaces}/{len(surfaces)}"
    )
    print(
        f"N6-EVIDENCE rule={RULE_ID} status={evidence[0]['status']} "
        f"expected={json.dumps(values, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(measured, ensure_ascii=False, sort_keys=True)}"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

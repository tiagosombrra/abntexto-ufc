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

SCENARIO = ROOT / "standards" / "direct-citation-source-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-citations.json"
RULESET_ID = "citations.direct-source"
RULE_ID = "citation.direct.source"


def fail(message: str) -> None:
    raise SystemExit(f"Direct citation source oracle failed: {message}")


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


def normalized_words(words: list[Any]) -> str:
    return normalize(" ".join(word.text for word in words))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure direct-citation source attribution from a final PDF."
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

        or scenario.get("component") != "direct-citation-source"
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
    if locator_matches[0].get("rule_ids") != [RULE_ID]:
        fail("direct-source locator rule scope drift")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")
    values = rule.get("values")
    if not isinstance(values, dict) or set(values) != {
        "source_required",
        "locator_when_available",
    }:
        fail(f"unexpected contract values for {RULE_ID}: {values}")
    if values.get("source_required") is not True or values.get(
        "locator_when_available"
    ) is not True:
        fail(f"contract drift for {RULE_ID}: {values}")

    markers = scenario.get("markers")
    required_markers = {"body_before", "quote_start", "quote_end", "body_after"}
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    fixture = scenario.get("fixture")
    if not isinstance(fixture, dict) or set(fixture) != {
        "citation_key",
        "source_tokens",
        "locator_token",
    }:
        fail("invalid fixture metadata")
    source_tokens = fixture.get("source_tokens")
    locator_token = fixture.get("locator_token")
    if (
        not isinstance(source_tokens, list)
        or not source_tokens
        or not all(isinstance(token, str) and token for token in source_tokens)
        or not isinstance(locator_token, str)
        or not locator_token
    ):
        fail("invalid source/locator fixture tokens")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    page = page_with_marker(pages, markers["quote_start"])
    for key in ("body_before", "quote_end", "body_after"):
        other = page_with_marker(pages, markers[key])
        if other.index != page.index:
            fail(f"controlled direct-citation markers span pages: {key}={other.index}")

    before_index, _ = word_with_marker(page, markers["body_before"])
    quote_start_index, _ = word_with_marker(page, markers["quote_start"])
    quote_end_index, _ = word_with_marker(page, markers["quote_end"])
    after_index, _ = word_with_marker(page, markers["body_after"])
    if not (before_index < quote_start_index <= quote_end_index < after_index):
        fail(
            "unexpected PDF reading order for body/quote/source markers: "
            f"{before_index}, {quote_start_index}, {quote_end_index}, {after_index}"
        )

    quote_words = list(page.words[quote_start_index : quote_end_index + 1])
    source_words = list(page.words[quote_end_index + 1 : after_index])
    if not source_words:
        fail("generated citation window is empty")

    quote_text = normalized_words(quote_words)
    source_text = normalized_words(source_words)
    normalized_source_tokens = [normalize(token) for token in source_tokens]
    normalized_locator = normalize(locator_token)

    contamination = [
        token
        for token in normalized_source_tokens + [normalized_locator]
        if token and token in quote_text
    ]
    if contamination:
        fail(
            "fixture quote text contains source/locator evidence tokens: "
            + ", ".join(contamination)
        )

    token_presence = {
        token: normalize(token) in source_text
        for token in source_tokens
    }
    source_present = all(token_presence.values())
    locator_present = normalized_locator in source_text
    rule_passed = source_present and locator_present

    measured = {
        "page": page.index,
        "same_controlled_sentence": True,
        "source_window_word_count": len(source_words),
        "source_tokens": token_presence,
        "source_present": source_present,
        "locator_token": locator_token,
        "locator_present": locator_present,
        "fixture_citation_key": fixture["citation_key"],
        "punctuation_and_citation_form_are_observational": True,
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
        "component": "direct-citation-source",
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

    found_count = sum(1 for present in token_presence.values() if present)
    print(
        "VALIDATION-EVIDENCE direct-citation-source-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" source_tokens={found_count}/{len(source_tokens)}"
        + f" locator={locator_token}"
        + f" locator_present={str(locator_present).lower()}"
    )
    print(
        f"VALIDATION-EVIDENCE rule={RULE_ID} status={evidence[0]['status']} "
        f"expected={json.dumps(values, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(measured, ensure_ascii=False, sort_keys=True)}"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

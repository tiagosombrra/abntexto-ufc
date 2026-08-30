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

SCENARIO = ROOT / "standards" / "indirect-citation-source-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-citations.json"
RULESET_ID = "citations.indirect-source"
RULE_ID = "citation.indirect.source"


def fail(message: str) -> None:
    raise SystemExit(f"Indirect citation source oracle failed: {message}")


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
    return " ".join(normalize(word.text) for word in words)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N6 indirect-citation source attribution from a final PDF."
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
        or scenario.get("component") != "indirect-citation-source"
        or scenario.get("locator_ruleset") != RULESET_ID
    ):
        fail("invalid scenario schema/phase/component/ruleset")

    if scenario.get("rules") != [RULE_ID]:
        fail(f"indirect citation source rule scope drift: {scenario.get('rules')}")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == RULESET_ID
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    if locator_matches[0].get("rule_ids") != [RULE_ID]:
        fail(f"locator rule scope drift: {locator_matches[0].get('rule_ids')}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")

    values = rule.get("values")
    if values != {"source_required": True}:
        fail(f"contract drift for {RULE_ID}: {values}")

    markers = scenario.get("markers")
    required_markers = {"body_before", "source_before", "body_after"}
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    fixture = scenario.get("fixture")
    required_fixture = {"citation_key", "source_tokens", "controlled_paraphrase"}
    if not isinstance(fixture, dict) or set(fixture) != required_fixture:
        fail("invalid fixture specification")
    if not isinstance(fixture.get("citation_key"), str) or not fixture["citation_key"]:
        fail("fixture citation_key must be a non-empty string")
    source_tokens = fixture.get("source_tokens")
    if (
        not isinstance(source_tokens, list)
        or not source_tokens
        or not all(isinstance(token, str) and token for token in source_tokens)
    ):
        fail("fixture source_tokens must be a non-empty string list")
    if fixture.get("controlled_paraphrase") is not True:
        fail("fixture must explicitly declare controlled_paraphrase=true")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    source_page = page_with_marker(pages, markers["source_before"])
    for key in ("body_before", "body_after"):
        page = page_with_marker(pages, markers[key])
        if page.index != source_page.index:
            fail(f"controlled indirect-citation markers span pages: {key}={page.index}")

    body_before_index, _ = word_with_marker(source_page, markers["body_before"])
    source_before_index, _ = word_with_marker(source_page, markers["source_before"])
    body_after_index, _ = word_with_marker(source_page, markers["body_after"])

    if not (body_before_index < source_before_index < body_after_index):
        fail(
            "unexpected marker order: "
            f"body_before={body_before_index}, source_before={source_before_index}, "
            f"body_after={body_after_index}"
        )

    paraphrase_words = list(source_page.words[body_before_index + 1 : source_before_index])
    source_words = list(source_page.words[source_before_index + 1 : body_after_index])
    if not paraphrase_words:
        fail("controlled paraphrase window is empty")
    if not source_words:
        fail("generated citation source window is empty")

    paraphrase_text = normalized_words(paraphrase_words)
    source_text = normalized_words(source_words)

    normalized_tokens = {token: normalize(token) for token in source_tokens}
    contamination = {
        token: normalized in paraphrase_text
        for token, normalized in normalized_tokens.items()
    }
    if any(contamination.values()):
        fail(
            "controlled paraphrase text contains source-identification tokens: "
            + json.dumps(contamination, ensure_ascii=False, sort_keys=True)
        )

    source_token_presence = {
        token: normalized in source_text
        for token, normalized in normalized_tokens.items()
    }
    source_present = all(source_token_presence.values())

    evidence = [
        {
            "rule_id": RULE_ID,
            "status": "PASS" if source_present else "FAIL",
            "expected": values,
            "measured": {
                "page": source_page.index,
                "fixture_citation_key": fixture["citation_key"],
                "source_present": source_present,
                "source_tokens": source_token_presence,
                "source_window_word_count": len(source_words),
                "same_controlled_sentence": True,
                "controlled_paraphrase_positive_applicability_only": True,
                "semantic_paraphrase_not_inferred_from_pdf": True,
                "punctuation_order_and_citation_form_are_observational": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": None,
        }
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if source_present else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "indirect-citation-source",
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

    present_count = sum(1 for present in source_token_presence.values() if present)
    print(
        "N6-EVIDENCE indirect-citation-source-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" source_tokens={present_count}/{len(source_tokens)}"
        + f" source_present={str(source_present).lower()}"
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

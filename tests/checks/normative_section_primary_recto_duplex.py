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

SCENARIO = ROOT / "standards" / "section-primary-recto-duplex-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
RULE_ID = "section.primary.recto-duplex"


def fail(message: str) -> None:
    raise SystemExit(f"Primary recto duplex validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def unique_word(pages: list[Any], marker: str) -> tuple[Any, Any]:
    wanted = normalize(marker)
    matches = [
        (page, word)
        for page in pages
        for word in page.words
        if normalize(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(f"marker {marker!r}: expected one word, found {[(p.index, w.text) for p, w in matches]}")
    return matches[0]


def record(status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": RULE_ID,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure primary-section recto evidence from a duplex final PDF.")
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

        or scenario.get("component") != "section-primary-recto-duplex"
        or scenario.get("locator_ruleset") != "sections.primary-recto-duplex"
    ):
        fail("invalid scenario schema/component/ruleset")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == scenario["locator_ruleset"]
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    locator_rules = locator_matches[0].get("rule_ids")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    contract_scope = [
        rule_id
        for rule_id in [RULE_ID]
        if rule_id in rules and rules[rule_id].get("authority") == "normative"
    ]
    if locator_rules != [RULE_ID] or scenario.get("rules") != [RULE_ID] or contract_scope != [RULE_ID]:
        fail(
            f"primary recto duplex scope drift: locator={locator_rules} "
            f"scenario={scenario.get('rules')} contract={contract_scope}"
        )

    primaries = scenario.get("primaries")
    if not isinstance(primaries, list) or len(primaries) < 3:
        fail("scenario must contain at least three controlled primary sections")
    if not all(
        isinstance(item, dict)
        and set(item) == {"title_marker", "body_marker"}
        and isinstance(item["title_marker"], str)
        and item["title_marker"]
        and isinstance(item["body_marker"], str)
        and item["body_marker"]
        for item in primaries
    ):
        fail("invalid primary-section marker specification")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    measured_primaries: list[dict[str, Any]] = []
    for item in primaries:
        title_page, _ = unique_word(pages, item["title_marker"])
        body_page, _ = unique_word(pages, item["body_marker"])
        if body_page.index != title_page.index:
            fail(
                f"fixture integrity: body marker {item['body_marker']!r} is on page {body_page.index}, "
                f"but its primary heading is on page {title_page.index}"
            )
        measured_primaries.append(
            {
                "title_marker": item["title_marker"],
                "body_marker": item["body_marker"],
                "physical_page": title_page.index,
                "is_recto": title_page.index % 2 == 1,
            }
        )

    title_pages = [item["physical_page"] for item in measured_primaries]
    if title_pages != sorted(title_pages) or len(set(title_pages)) != len(title_pages):
        fail(f"fixture integrity: primary pages are not strictly increasing: {title_pages}")

    transitions: list[dict[str, Any]] = []
    page_by_index = {page.index: page for page in pages}
    for previous, current in zip(measured_primaries, measured_primaries[1:]):
        intermediate = []
        for page_index in range(previous["physical_page"] + 1, current["physical_page"]):
            page = page_by_index.get(page_index)
            intermediate.append(
                {
                    "physical_page": page_index,
                    "word_count": len(page.words) if page is not None else None,
                }
            )
        transitions.append(
            {
                "from_page": previous["physical_page"],
                "to_page": current["physical_page"],
                "page_delta": current["physical_page"] - previous["physical_page"],
                "page_delta_is_observational": True,
                "intermediate_pages": intermediate,
                "intermediate_pages_are_observational": True,
            }
        )

    rule = rules[RULE_ID]
    expected = rule["values"]
    applicability = rule.get("applicability", {})
    passed = (
        expected.get("start_side") == "recto"
        and applicability.get("duplex") is True
        and all(item["is_recto"] for item in measured_primaries)
    )

    evidence = record(
        "PASS" if passed else "FAIL",
        expected,
        {
            "applicability": applicability,
            "primaries": measured_primaries,
            "all_primary_pages_recto": all(item["is_recto"] for item in measured_primaries),
            "transitions": transitions,
            "parity_predicate_only": True,
        },
    )
    status_counts = dict(Counter([evidence["status"]]))
    result = evidence["status"]
    payload = {
        "schema_version": 1,
        "component": "section-primary-recto-duplex",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "evidence": [evidence],
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "VALIDATION-EVIDENCE section-primary-recto-duplex-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" primaries={len(measured_primaries)} pages={','.join(str(page) for page in title_pages)}"
    )
    print(
        f"VALIDATION-EVIDENCE rule={RULE_ID} status={evidence['status']} "
        f"expected={json.dumps(expected, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(evidence['measured'], ensure_ascii=False, sort_keys=True)}"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

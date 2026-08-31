#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

SCENARIO = ROOT / "standards" / "reference-semantics-scenario.json"
LOCATOR = ROOT / "standards" / "locator-audit-references.json"
BIB_FIXTURE = ROOT / "tests" / "fixtures" / "referencias-6023-2025.bib"

RULE_ORDER = [
    "references.doi.when-present",
    "references.online.url-access",
]


def fail(message: str) -> None:
    raise SystemExit(f"reference semantics oracle failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def locator_ruleset(document: dict[str, Any], ruleset_id: str) -> dict[str, Any]:
    matches = [
        item
        for item in document.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == ruleset_id
    ]
    if len(matches) != 1:
        fail(f"locator ruleset {ruleset_id}: expected one match, found {len(matches)}")
    return matches[0]


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_entry_chunks(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", text)
    return [
        normalize_text(chunk)
        for chunk in re.split(r"\n\s*\n", normalized)
        if chunk.strip()
    ]


def unique_rendered_entry(chunks: list[str], marker: str) -> str:
    folded = marker.casefold()
    matches = [chunk for chunk in chunks if folded in chunk.casefold()]
    if len(matches) != 1:
        fail(f"rendered entry {marker!r}: expected one match, found {len(matches)}")
    return matches[0]


def bib_entry(source: str, key: str) -> str:
    pattern = re.compile(
        rf"(?ms)^@\w+\{{{re.escape(key)},\s*(.*?)(?=^@\w+\{{|\Z)"
    )
    match = pattern.search(source)
    if not match:
        fail(f"BibTeX entry not found: {key}")
    return match.group(1)


def bib_field(entry: str, field: str) -> str:
    match = re.search(
        rf"(?mi)^\s*{re.escape(field)}\s*=\s*\{{([^}}]*)\}}\s*,?\s*$",
        entry,
    )
    if not match:
        fail(f"BibTeX field {field!r} not found in controlled entry")
    return normalize_text(match.group(1))


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text).casefold()


def access_date_match(entry: str, iso_date: str) -> re.Match[str] | None:
    try:
        year, month, day = [int(part) for part in iso_date.split("-")]
    except (TypeError, ValueError) as exc:
        fail(f"invalid scenario access date {iso_date!r}: {exc}")
    if month != 8:
        fail("controlled access-date matcher currently expects the August fixture")

    # Accept common localized or numeric renderings without freezing punctuation.
    month_token = r"(?:0?8|ago(?:sto)?\.?|aug(?:ust)?\.?)"
    pattern = re.compile(
        rf"\b0?{day}\b\s*(?:de\s+)?{month_token}\s*(?:de\s+)?\b{year}\b",
        re.IGNORECASE,
    )
    return pattern.search(normalize_text(entry))


def audit_compatibility_boundary(scenario: dict[str, Any]) -> dict[str, Any]:
    boundary = scenario.get("compatibility_boundary")
    if not isinstance(boundary, dict):
        fail("compatibility_boundary must be an object")
    relative = boundary.get("file")
    if not isinstance(relative, str) or not relative:
        fail("compatibility boundary file is missing")
    path = ROOT / relative
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read compatibility boundary {path}: {exc}")

    if boundary.get("general_doi_url_formatting") != "delegated-to-biblatex-abnt":
        fail("unexpected DOI/URL compatibility-boundary declaration")
    if boundary.get("forbid_global_doi_url_formatter_override") is not True:
        fail("global DOI/URL formatter guardrail must remain enabled")

    forbidden_patterns = {
        "doi+eprint+url macro override": r"\\(?:re)?newbibmacro\*?\s*\{doi\+eprint\+url\}",
        "DOI field formatter override": r"\\DeclareFieldFormat\s*\{doi\}",
        "URL field formatter override": r"\\DeclareFieldFormat\s*\{url\}",
    }
    violations = [
        label
        for label, pattern in forbidden_patterns.items()
        if re.search(pattern, source)
    ]
    if violations:
        fail("compatibility boundary drift: " + ", ".join(violations))

    macro_calls = len(re.findall(r"\\usebibmacro\s*\{doi\+eprint\+url\}", source))
    return {
        "status": "PASS",
        "file": relative,
        "general_doi_url_formatting": "delegated-to-biblatex-abnt",
        "global_formatter_override_detected": False,
        "custom_driver_doi_url_macro_calls": macro_calls,
        "custom_driver_macro_use_is_allowed": boundary.get(
            "custom_driver_macro_use_is_allowed"
        )
        is True,
        "normative_predicate": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate bounded DOI and online-access reference semantics."
    )
    parser.add_argument("text", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.text.is_file():
        fail(f"rendered reference text not found: {args.text}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR)
    if (
        scenario.get("schema_version") != 1

        or scenario.get("component") != "reference-semantics"
        or scenario.get("rules") != RULE_ORDER
    ):
        fail("invalid scenario schema/component/scope")

    policy = scenario.get("evidence_policy")
    if not isinstance(policy, dict) or not all(
        policy.get(key) is True
        for key in (
            "positive_applicable_cases_only",
            "entry_local_evidence",
            "full_reference_string_is_not_a_predicate",
            "engine_matrix_deferred",
        )
    ):
        fail("reference semantics evidence policy drifted")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    missing = [rule_id for rule_id in RULE_ORDER if rule_id not in rules]
    if missing:
        fail("contract rules missing: " + ", ".join(missing))

    doi_values = rules["references.doi.when-present"]["values"]
    online_values = rules["references.online.url-access"]["values"]
    if doi_values != {"doi": "include-when-present-and-applicable"}:
        fail(f"DOI contract drifted: {doi_values}")
    if online_values != {
        "url_or_equivalent_availability": True,
        "access_date_when_required": True,
    }:
        fail(f"online-access contract drifted: {online_values}")

    locator_map = scenario.get("locator_rulesets")
    if not isinstance(locator_map, dict) or set(locator_map) != set(RULE_ORDER):
        fail("locator ruleset map drifted")
    for rule_id in RULE_ORDER:
        ruleset_id = locator_map[rule_id]
        if not isinstance(ruleset_id, str):
            fail(f"locator ruleset for {rule_id} must be a string")
        ruleset = locator_ruleset(locator, ruleset_id)
        if ruleset.get("rule_ids") != [rule_id]:
            fail(f"locator scope drift for {rule_id}: {ruleset.get('rule_ids')}")
        if ruleset.get("current_locator") != rules[rule_id]["locator"]:
            fail(f"locator text drift for {rule_id}")

    entries = scenario.get("entries")
    if not isinstance(entries, dict) or set(entries) != set(RULE_ORDER):
        fail("controlled entry map drifted")

    try:
        rendered_text = args.text.read_text(encoding="utf-8")
        bib_source = BIB_FIXTURE.read_text(encoding="utf-8")
    except OSError as exc:
        fail(str(exc))
    chunks = extract_entry_chunks(rendered_text)

    doi_case = entries["references.doi.when-present"]
    online_case = entries["references.online.url-access"]
    if not isinstance(doi_case, dict) or not isinstance(online_case, dict):
        fail("controlled entry specifications must be objects")

    doi_key = doi_case.get("bib_key")
    doi_marker = doi_case.get("marker")
    expected_doi = doi_case.get("doi")
    online_key = online_case.get("bib_key")
    online_marker = online_case.get("marker")
    expected_url = online_case.get("url")
    expected_access_date = online_case.get("access_date")
    controlled_values = (
        doi_key,
        doi_marker,
        expected_doi,
        online_key,
        online_marker,
        expected_url,
        expected_access_date,
    )
    if not all(isinstance(value, str) and value for value in controlled_values):
        fail("controlled entry fields must be non-empty strings")

    doi_bib = bib_entry(bib_source, doi_key)
    online_bib = bib_entry(bib_source, online_key)
    if bib_field(doi_bib, "doi") != expected_doi:
        fail("controlled DOI fixture drifted")
    if bib_field(online_bib, "url") != expected_url:
        fail("controlled online URL fixture drifted")
    if bib_field(online_bib, "urldate") != expected_access_date:
        fail("controlled online access-date fixture drifted")

    doi_entry = unique_rendered_entry(chunks, doi_marker)
    online_entry = unique_rendered_entry(chunks, online_marker)

    doi_present = expected_doi.casefold() in doi_entry.casefold()
    url_present = compact(expected_url) in compact(online_entry)
    date_match = access_date_match(online_entry, expected_access_date)
    access_date_present = date_match is not None

    evidence = [
        {
            "rule_id": "references.doi.when-present",
            "status": "PASS" if doi_present else "FAIL",
            "expected": doi_values,
            "measured": {
                "bib_key": doi_key,
                "entry_marker": doi_marker,
                "fixture_doi": expected_doi,
                "rendered_doi_present": doi_present,
                "entry_local_evidence": True,
                "positive_applicable_case_only": True,
                "full_reference_string_not_frozen": True,
            },
            "tool": "pdftotext -layout",
            "tolerance": None,
        },
        {
            "rule_id": "references.online.url-access",
            "status": "PASS" if url_present and access_date_present else "FAIL",
            "expected": online_values,
            "measured": {
                "bib_key": online_key,
                "entry_marker": online_marker,
                "fixture_url": expected_url,
                "rendered_url_present": url_present,
                "fixture_access_date": expected_access_date,
                "rendered_access_date_present": access_date_present,
                "rendered_access_date_match": (
                    date_match.group(0) if date_match is not None else None
                ),
                "entry_local_evidence": True,
                "positive_applicable_case_only": True,
                "access_label_is_not_strengthened_into_a_predicate": True,
                "full_reference_string_not_frozen": True,
            },
            "tool": "pdftotext -layout",
            "tolerance": None,
        },
    ]

    boundary = audit_compatibility_boundary(scenario)
    status_counts = dict(Counter(item["status"] for item in evidence))
    result = (
        "PASS"
        if all(item["status"] == "PASS" for item in evidence)
        and boundary["status"] == "PASS"
        else "FAIL"
    )
    payload = {
        "schema_version": 1,
        "component": "reference-semantics",
        "source_commit_sha": args.commit_sha,
        "fixture": "tests/documents/references-6023-2025.tex",
        "bibliography_fixture": "tests/fixtures/references-6023-2025.bib",
        "rendered_engine": "lualatex",
        "engine_matrix_deferred": true,
        "result": result,
        "status_counts": status_counts,
        "compatibility_boundary": boundary,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "VALIDATION-EVIDENCE reference-semantics-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" compat_boundary={boundary['status']}"
    )
    for item in evidence:
        print(
            f"VALIDATION-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "VALIDATION-EVIDENCE compatibility-boundary "
        + json.dumps(boundary, ensure_ascii=False, sort_keys=True)
    )

    failed = [item["rule_id"] for item in evidence if item["status"] != "PASS"]
    if failed:
        fail("semantic predicates failed: " + ", ".join(failed))


if __name__ == "__main__":
    main()

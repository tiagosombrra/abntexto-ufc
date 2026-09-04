#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import load_catalog
from normative_full import full_rule_map, load_full_contract

BASE_RULE_COUNT = 100
MINIMUM_EXTENSION_COUNT = 23
ROADMAP = ROOT / "release" / "v3-roadmap.json"
ARTICLE_PROFILE = "scientific-article"
EXPECTED_ARTICLE_RULE_IDS = {
    "article.structure.required",
    "article.title.presentation",
    "article.authorship.presentation",
    "article.abstract.presentation",
    "article.abstract.length.recommended",
    "article.dates.required",
    "article.textual.required-sections",
    "article.textual.typography",
    "article.references.required-placement",
    "article.page.margins",
    "article.font.family.recommended",
    "article.pagination",
    "article.sections.continuous",
}
EXPECTED_SPECIFIC_PRECEDENCE = {
    "publisher-or-journal-author-guidelines",
    "formally-approved-course-specific-model",
}


def fail(message: str) -> None:
    raise SystemExit(f"Full normative contract failed: {message}")


def validate_article_phase_guard(rules: dict[str, dict]) -> None:
    article_rules = sorted(rule_id for rule_id in rules if rule_id.startswith("article."))
    if not article_rules:
        return

    try:
        roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read roadmap for article phase guard: {exc}")

    if roadmap.get("phase") != "V3-A1" or roadmap.get("stage") != "V3-A1":
        fail(
            "article rules are source-operational only during the bounded V3-A1 contract phase; "
            f"current phase/stage={roadmap.get('phase')}/{roadmap.get('stage')}"
        )

    if set(article_rules) != EXPECTED_ARTICLE_RULE_IDS:
        missing = sorted(EXPECTED_ARTICLE_RULE_IDS - set(article_rules))
        extra = sorted(set(article_rules) - EXPECTED_ARTICLE_RULE_IDS)
        fail(f"V3-A1 article rule set drifted; missing={missing}, extra={extra}")

    progress = roadmap.get("a1_progress")
    if not isinstance(progress, dict):
        fail("V3-A1 article rules require explicit a1_progress machine state")
    if progress.get("profile_id") != ARTICLE_PROFILE:
        fail("V3-A1 machine state does not use the canonical scientific-article profile id")
    if progress.get("runtime_article_profile_present") is not False:
        fail("V3-A1 must remain source-contract only; article runtime cannot be present")

    for rule_id in article_rules:
        rule = rules[rule_id]
        validation = rule.get("validation")
        if validation != {"mode": "manual", "checks": ["validator-source"]}:
            fail(
                f"{rule_id}: V3-A1 article rule must remain manual and traceable only through validator-source"
            )

        applicability = rule.get("applicability")
        if not isinstance(applicability, dict):
            fail(f"{rule_id}: V3-A1 article applicability block is required")
        if applicability.get("profiles") != [ARTICLE_PROFILE]:
            fail(f"{rule_id}: retired or non-canonical article profile identifier detected")
        if applicability.get("institutional_default") is not True:
            fail(f"{rule_id}: generic UFC article contract must be marked as institutional default")
        precedence = applicability.get("specific_model_precedence")
        if not isinstance(precedence, list) or set(precedence) != EXPECTED_SPECIFIC_PRECEDENCE:
            fail(f"{rule_id}: article-specific precedence boundary is incomplete or drifted")


def main() -> None:
    catalog = load_catalog()
    contract = load_full_contract(catalog)
    rules = full_rule_map(contract)

    if contract["base_rule_count"] != BASE_RULE_COUNT:
        fail(
            f"expected {BASE_RULE_COUNT} base atomic rules, "
            f"got {contract['base_rule_count']}"
        )
    extension_ids = contract["extended_rule_ids"]
    if len(rules) != contract["base_rule_count"] + len(extension_ids):
        fail("full contract count is inconsistent with base rules + extensions")
    if len(extension_ids) < MINIMUM_EXTENSION_COUNT:
        fail("full contract lost the certified extension block")
    if "project.standard" in rules:
        fail("retired project.standard umbrella returned to the active contract")

    validate_article_phase_guard(rules)

    expected = {
        "pagination.frontmatter.counted-not-numbered": {
            "counted": True,
            "number_visible": False,
        },
        "pagination.catalog-data.not-counted": {
            "counted": False,
            "number_visible": False,
        },
        "pagination.recto.position": {"position": "upper-right"},
        "pagination.verso.position": {"position": "upper-left"},
        "footnote.line-spacing": {"factor": 1.0},
        "footnote.separator.length": {
            "length_mm": 50,
            "origin": "left-margin",
        },
        "footnote.hanging-alignment": {"enabled": True},
        "section.indicator.alignment": {"alignment": "left"},
        "section.indicator.separator": {
            "separator": "single-character-space",
        },
        "section.primary.recto-duplex": {"start_side": "recto"},
        "section.multiline.hanging": {"enabled": True},
        "nature.line-spacing": {"factor": 1.0},
        "nature.block.alignment": {
            "horizontal_extent": "mid-text-block-to-right-margin",
        },
    }
    for rule_id, values in expected.items():
        rule = rules.get(rule_id)
        if not rule:
            fail(f"certified rule disappeared: {rule_id}")
        if rule["values"] != values:
            fail(f"{rule_id}: unexpected values {rule['values']}")

    for rule_id in extension_ids:
        rule = rules[rule_id]
        authority = rule.get("authority")
        if authority == "normative":
            resolution = rule.get("resolution")
            if not isinstance(resolution, dict) or resolution.get("status") != "resolved":
                fail(f"{rule_id}: unresolved normative provenance")
            if not resolution.get("governing_sources"):
                fail(f"{rule_id}: missing governing source")
        elif authority in {"project-policy", "technical-profile"}:
            if rule.get("sources") or rule.get("resolution") is not None:
                fail(f"{rule_id}: non-normative rule claims external authority")
        else:
            fail(f"{rule_id}: invalid authority {authority}")

    indicator = rules["section.indicator.alignment"]
    if set(indicator["resolution"]["governing_sources"]) != {
        "abnt-nbr-14724-2024",
        "abnt-nbr-6024-2012",
    }:
        fail(
            "section indicator must be jointly governed by current "
            "NBR 14724 and NBR 6024"
        )

    not_applicable = sorted(
        rule_id
        for rule_id in extension_ids
        if rules[rule_id]["validation"]["mode"] == "not-applicable"
    )
    for rule_id in not_applicable:
        rule = rules[rule_id]
        if rule["validation"]["checks"]:
            fail(f"{rule_id}: not-applicable validation declares executable checks")
        if not rule.get("applicability"):
            fail(f"{rule_id}: not-applicable validation lacks explicit applicability")

    runner = (ROOT / "tests" / "run.py").read_text(encoding="utf-8")
    gates = set(re.findall(r'Check\(\s*"([^"]+)"', runner))
    uncovered = sorted(
        rule_id
        for rule_id in extension_ids
        if rules[rule_id]["validation"]["mode"] != "not-applicable"
        and not (set(rules[rule_id]["validation"]["checks"]) & gates)
    )
    if uncovered:
        fail("extended executable rules without unified evidence: " + ", ".join(uncovered))

    article_count = sum(rule_id.startswith("article.") for rule_id in rules)
    print(
        "Full normative contract passed: "
        f"{len(rules)} atomic rules, {len(extension_ids)} extensions "
        f"across {len(contract.get('coverage_manifests', []))} manifests, "
        f"{len(not_applicable)} explicitly not-applicable, "
        f"{article_count} V3-A1 article rules guarded as manual source-contract predicates."
    )


if __name__ == "__main__":
    main()

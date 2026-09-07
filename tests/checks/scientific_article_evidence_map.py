#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "standards" / "coverage-rules-article.json"
MAP_PATH = ROOT / "standards" / "article-evidence-map.json"

RECOMMENDED_RULES = {
    "article.authorship.alignment.recommended",
    "article.summary.word-count.recommended",
    "article.summary.keywords.minimum.recommended",
    "article.summary.single-paragraph.recommended",
}
OPTIONAL_RULES = {
    "article.title.foreign.optional",
    "article.summary.foreign.optional",
}
JOURNAL_RULE = "article.journal-guidelines.precedence"


def fail(message: str) -> None:
    raise SystemExit(f"Scientific article evidence map failed: {message}")


def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        fail(f"{path.name}: top-level payload must be an object")
    return payload


def main() -> None:
    source_payload = load(RULES_PATH)
    evidence_payload = load(MAP_PATH)

    source_rules = source_payload.get("rules")
    evidence_rules = evidence_payload.get("rules")
    if not isinstance(source_rules, list) or not isinstance(evidence_rules, list):
        fail("both rule registries must contain a rules list")

    source_by_id: dict[str, dict] = {}
    for rule in source_rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("id"), str):
            fail("source contract contains an invalid rule entry")
        rule_id = rule["id"]
        if rule_id in source_by_id:
            fail(f"duplicate source rule id: {rule_id}")
        source_by_id[rule_id] = rule

    evidence_by_id: dict[str, dict] = {}
    for entry in evidence_rules:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            fail("evidence map contains an invalid rule entry")
        rule_id = entry["id"]
        if rule_id in evidence_by_id:
            fail(f"duplicate evidence-map rule id: {rule_id}")
        evidence_by_id[rule_id] = entry

    if len(source_by_id) != 18:
        fail(f"retained article contract must contain exactly 18 rules; measured={len(source_by_id)}")
    if set(evidence_by_id) != set(source_by_id):
        missing = sorted(set(source_by_id) - set(evidence_by_id))
        unknown = sorted(set(evidence_by_id) - set(source_by_id))
        fail(f"evidence-map identity mismatch: missing={missing} unknown={unknown}")

    policy = evidence_payload.get("policy") or {}
    expected_policy = {
        "shared_mechanism_is_proof": False,
        "executable_support_implies_proven": False,
        "recommendations_are_enforcing": False,
        "journal_precedence_remains_conditional_manual": True,
    }
    for key, expected in expected_policy.items():
        if policy.get(key) is not expected:
            fail(f"policy {key} must remain {expected}")

    owners = set()
    dispositions: dict[str, int] = {}
    for rule_id, source in source_by_id.items():
        entry = evidence_by_id[rule_id]
        if entry.get("normativity") != source.get("normativity"):
            fail(f"{rule_id}: evidence map changed normativity")
        source_validation = source.get("validation") or {}
        if entry.get("validation_mode") != source_validation.get("mode"):
            fail(f"{rule_id}: evidence map changed current validation mode")
        if entry.get("validation_promoted") is not False:
            fail(f"{rule_id}: Step 6 must not claim an unrecorded validation promotion")

        disposition = entry.get("proof_disposition")
        if not isinstance(disposition, str) or not disposition:
            fail(f"{rule_id}: proof disposition is required")
        dispositions[disposition] = dispositions.get(disposition, 0) + 1

        owner = entry.get("article_specific_owner")
        if owner is not None:
            if not isinstance(owner, str) or not owner.startswith("tests/integration/scientific-article-"):
                fail(f"{rule_id}: executable owner must be an article-specific integration gate")
            owner_path = ROOT / owner
            if not owner_path.is_file():
                fail(f"{rule_id}: declared owner does not exist: {owner}")
            owners.add(owner)

        if rule_id in RECOMMENDED_RULES:
            if entry.get("normativity") != "recommended":
                fail(f"{rule_id}: recommendation normativity changed")
            if entry.get("validation_mode") != "manual":
                fail(f"{rule_id}: recommendation must remain manual")
            if disposition != "advisory-non-enforcing-support":
                fail(f"{rule_id}: recommendation must remain non-enforcing support")
            if owner != "tests/integration/scientific-article-recommendations.sh":
                fail(f"{rule_id}: recommendation owner must be the recommendation gate")

        if rule_id in OPTIONAL_RULES:
            if entry.get("normativity") != "optional":
                fail(f"{rule_id}: optionality changed")
            if disposition != "conditional-optionality-support":
                fail(f"{rule_id}: optional rule must preserve conditional optionality support")
            if owner != "tests/integration/scientific-article-foreign-elements.sh":
                fail(f"{rule_id}: optional rule must be owned by the present/absent matrix gate")

    journal = evidence_by_id[JOURNAL_RULE]
    source_journal = source_by_id[JOURNAL_RULE]
    if journal.get("normativity") != "required-when-applicable":
        fail("journal precedence must remain required-when-applicable")
    if journal.get("validation_mode") != "conditional-manual":
        fail("journal precedence must remain conditional-manual")
    if journal.get("article_specific_owner") is not None:
        fail("journal precedence must not claim a generic executable owner")
    if journal.get("proof_disposition") != "source-applicability-only":
        fail("journal precedence must remain source/applicability only")
    source_applicability = source_journal.get("applicability") or {}
    if journal.get("applicability") != source_applicability.get("context"):
        fail("journal precedence applicability drifted from source contract")
    if journal.get("applicability") != "target-journal-submission":
        fail("journal precedence applicability must remain target-journal-submission")

    print(
        "ARTICLE-EVIDENCE-MAP-EVIDENCE status=PASS "
        f"rules={len(evidence_by_id)} owners={len(owners)} "
        f"recommended={len(RECOMMENDED_RULES)} optional={len(OPTIONAL_RULES)} "
        "journal_conditional_manual=1 validation_promotions=0 "
        f"dispositions={','.join(f'{key}:{dispositions[key]}' for key in sorted(dispositions))}"
    )


if __name__ == "__main__":
    main()

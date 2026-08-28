#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import load_catalog, source_map
from normative_full import full_rule_map, load_full_contract

LEDGER = ROOT / "release" / "n15-b2a-article-contract.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"
VERSION_POLICY = ROOT / "normativa" / "version-policy.json"
PRECEDENCE = ROOT / "normativa" / "precedence.json"

EXPECTED_RULES = {
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
RECOMMENDATIONS = {
    "article.abstract.length.recommended",
    "article.font.family.recommended",
}
ARTICLE_SOURCES = {"ufc-guia-artigos-2022", "abnt-nbr-6022-2018"}


def fail(message: str) -> None:
    raise SystemExit(f"N15-B2A article contract failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return data


def main() -> None:
    ledger = load_json(LEDGER)
    source_audit = load_json(SOURCE_AUDIT)
    version_policy = load_json(VERSION_POLICY)
    precedence = load_json(PRECEDENCE)
    catalog = load_catalog()
    sources = source_map(catalog)
    contract = load_full_contract(catalog)
    rules = full_rule_map(contract)

    if ledger.get("phase") != "N15-B2A" or ledger.get("status") != "CONTRACT_CANDIDATE":
        fail("ledger must describe the N15-B2A contract candidate")
    if ledger.get("base_main_sha") != "bc7b3bbe0e7ac21aa16efb1f0bab9a4dfb8e912e":
        fail("B2-A base main SHA drifted")
    if set(ledger.get("article_rule_ids", [])) != EXPECTED_RULES:
        fail("ledger article rule set drifted")
    if set(ledger.get("recommendation_rule_ids", [])) != RECOMMENDATIONS:
        fail("ledger recommendation set drifted")

    active_audit_ids = {
        item.get("id") for item in source_audit.get("sources", []) if isinstance(item, dict)
    }
    if "ufc-guia-artigos-2022" not in active_audit_ids:
        fail("current 2022 UFC article guide is absent from the active source registry")
    if "ufc-guia-artigos-2021" in active_audit_ids:
        fail("superseded 2021 article-guide identity remained active")
    superseded = {
        item.get("id")
        for item in source_audit.get("reviewed_superseded_sources", [])
        if isinstance(item, dict)
    }
    if "ufc-guia-artigos-2021" not in superseded:
        fail("superseded 2021 article-guide identity is not preserved as reviewed history")

    missing_sources = sorted(ARTICLE_SOURCES - set(sources))
    if missing_sources:
        fail("article authority sources were not promoted to runtime catalog: " + ", ".join(missing_sources))
    if sources["ufc-guia-artigos-2022"].get("role") != "institutional-guide":
        fail("UFC article guide must have institutional-guide runtime role")
    if sources["abnt-nbr-6022-2018"].get("role") != "technical-standard":
        fail("NBR 6022:2018 must have technical-standard runtime role")
    if "ufc-guia-artigos-2021" in precedence.get("source_roles", {}):
        fail("superseded 2021 guide identity leaked into runtime precedence")

    article_rules = {rule_id: rule for rule_id, rule in rules.items() if rule_id.startswith("article.")}
    if set(article_rules) != EXPECTED_RULES:
        fail("article.* contract set is incomplete or contains unreviewed predicates")
    for rule_id, rule in article_rules.items():
        if rule.get("phase") != "N15-B2A":
            fail(f"{rule_id}: wrong promotion phase")
        if rule.get("applicability", {}).get("profiles") != ["artigo"]:
            fail(f"{rule_id}: applicability must be isolated to the future artigo profile")
        if rule.get("validation", {}).get("checks") != ["validator-source"]:
            fail(f"{rule_id}: B2-A must remain source-contract-only")
        if rule_id in RECOMMENDATIONS:
            if rule.get("normativity") != "recommendation":
                fail(f"{rule_id}: recommendation was hardened into a mandatory requirement")
        elif rule.get("normativity") == "recommendation":
            fail(f"{rule_id}: mandatory rule was weakened into a recommendation")

    structure = article_rules["article.structure.required"]
    if structure.get("resolution", {}).get("governing_sources") != ["abnt-nbr-6022-2018"]:
        fail("article structure must be technically governed by current NBR 6022:2018")
    references = article_rules["article.references.required-placement"]
    if references.get("values", {}).get("current_reference_standard") != "ABNT NBR 6023:2025":
        fail("article references did not reconcile the current NBR 6023 edition")
    sections = article_rules["article.sections.continuous"]
    if sections.get("values", {}).get("primary_starts_new_page") is not False:
        fail("article sections must preserve continuous flow")

    policy = version_policy.get("profile_candidates", {}).get("scientific_article", {})
    if policy.get("status") != "contract-promotion-in-progress-runtime-pending":
        fail("version policy does not expose the B2-A/B2-B boundary")
    if policy.get("source_and_contract_phase") != "N15-B2A":
        fail("article source/contract phase must be N15-B2A")
    if policy.get("runtime_implementation_phase") != "N15-B2B":
        fail("article formatting implementation must remain deferred to N15-B2B")
    if policy.get("evidence_completion_phase") != "N15-B2C":
        fail("article evidence closure must remain deferred to N15-B2C")

    if (ROOT / "abntexto-ufc" / "artigos.def").exists():
        fail("B2-A introduced the LaTeX article module prematurely")
    if ledger.get("runtime", {}).get("latex_article_module_added") is not False:
        fail("ledger incorrectly claims a LaTeX runtime implementation")
    if ledger.get("runtime", {}).get("article_profile_available") is not False:
        fail("ledger incorrectly claims the article profile is already available")

    exit_criteria = ledger.get("exit_criteria", {})
    false_criteria = sorted(key for key, value in exit_criteria.items() if value is not True)
    if false_criteria:
        fail("B2-A exit criteria not satisfied: " + ", ".join(false_criteria))

    print(
        "N15-EVIDENCE article-contract "
        "status=PASS phase=N15-B2A phase_status=CONTRACT_CANDIDATE "
        f"article_rules={len(EXPECTED_RULES)} recommendations={len(RECOMMENDATIONS)} "
        "guide=UFC_ARTICLE_2022 standard=ABNT_NBR_6022_2018 "
        "latex_runtime=false next=N15-B2B"
    )


if __name__ == "__main__":
    main()

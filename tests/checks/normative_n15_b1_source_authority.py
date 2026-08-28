#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "release" / "n15-b1-source-authority.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"
VERSION_POLICY = ROOT / "normativa" / "version-policy.json"
CATALOG = ROOT / "normativa" / "catalog.json"
PRECEDENCE = ROOT / "normativa" / "precedence.json"
ATOMIC_RULES = ROOT / "normativa" / "atomic-rules.json"

EXPECTED_GUIDES = {
    "ufc-guia-trabalhos-2022",
    "ufc-guia-artigos-2021",
    "ufc-guia-citacoes-2025",
    "ufc-guia-referencias-2023",
    "ufc-guia-projetos-2019",
}
EXPECTED_ARTICLE_CANDIDATES = {
    "ufc-guia-artigos-2021",
    "abnt-nbr-6022-2018",
}


def fail(message: str) -> None:
    raise SystemExit(f"N15-B1 source authority failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return data


def rule_ids(data: dict[str, Any]) -> set[str]:
    rules = data.get("rules", [])
    if not isinstance(rules, list):
        fail("runtime catalog rules must be a list")
    return {
        str(item.get("id"))
        for item in rules
        if isinstance(item, dict) and item.get("id")
    }


def nested_rule_ids(value: Any) -> set[str]:
    ids: set[str] = set()
    if isinstance(value, dict):
        rule_id = value.get("id")
        if isinstance(rule_id, str):
            ids.add(rule_id)
        for item in value.values():
            ids.update(nested_rule_ids(item))
    elif isinstance(value, list):
        for item in value:
            ids.update(nested_rule_ids(item))
    return ids


def main() -> None:
    ledger = load_json(LEDGER)
    source_audit = load_json(SOURCE_AUDIT)
    version_policy = load_json(VERSION_POLICY)
    catalog = load_json(CATALOG)
    precedence = load_json(PRECEDENCE)
    atomic_rules = load_json(ATOMIC_RULES)

    if ledger.get("schema_version") != 1:
        fail("unsupported ledger schema_version")
    if ledger.get("phase") != "N15-B1" or ledger.get("status") != "CLOSURE_CANDIDATE":
        fail("N15-B1 must be recorded as a closure candidate")
    if ledger.get("base_main_sha") != "ab61d20c03f9b79e8d01b7913a721c85cd695491":
        fail("N15-B1 base main SHA drifted")

    if source_audit.get("scope") != "abntexto-ufc-current-sources":
        fail("source registry scope is not release-independent")
    if source_audit.get("reviewed_at") != "2026-08-28":
        fail("source registry was not reviewed for N15-B1")

    source_ids = {
        item.get("id")
        for item in source_audit.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    guides = {source_id for source_id in source_ids if source_id.startswith("ufc-guia-")}
    if guides != EXPECTED_GUIDES:
        fail(f"official UFC guide inventory drifted: {sorted(guides)}")

    article_guide = next(
        item for item in source_audit["sources"] if item.get("id") == "ufc-guia-artigos-2021"
    )
    if article_guide.get("technical_authority") is not False:
        fail("UFC article guide must not select a technical edition")
    if article_guide.get("status") != "current-institutional-with-stale-technical-citations":
        fail("UFC article guide must retain restricted institutional-guide status")

    nbr_6022 = next(
        item for item in source_audit["sources"] if item.get("id") == "abnt-nbr-6022-2018"
    )
    if nbr_6022.get("status") != "current" or nbr_6022.get("kind") != "technical-standard":
        fail("NBR 6022:2018 current technical-source classification drifted")

    cepe_2015 = next(
        item for item in source_audit["sources"] if item.get("id") == "ufc-res-17-cepe-2015"
    )
    if "program-level-presentation-directives" not in cepe_2015.get("applies_to", []):
        fail("CEPE 17/2015 PPG presentation authority is missing")

    capes_59 = next(
        item for item in source_audit["sources"] if item.get("id") == "capes-portaria-59-2017"
    )
    if capes_59.get("technical_authority") is not False:
        fail("CAPES 59/2017 acquired unsupported technical formatting authority")

    excluded = source_audit.get("reviewed_excluded_sources", [])
    mec = [item for item in excluded if item.get("id") == "mec-portaria-1224-2013"]
    if len(mec) != 1 or mec[0].get("status") != "revoked":
        fail("revoked MEC 1.224/2013 exclusion is not explicit")
    if "mec-portaria-1224-2013" in source_ids:
        fail("revoked MEC 1.224/2013 leaked into current sources")

    policy_candidates = (
        version_policy.get("profile_candidates", {})
        .get("scientific_article", {})
        .get("candidate_sources", [])
    )
    if set(policy_candidates) != EXPECTED_ARTICLE_CANDIDATES:
        fail("version policy article candidate set drifted")
    if (
        version_policy.get("profile_candidates", {})
        .get("scientific_article", {})
        .get("status")
        != "reconciled-not-runtime"
    ):
        fail("article sources must remain reconciled-not-runtime during N15-B1")

    runtime_source_ids = {
        item.get("id")
        for item in catalog.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if EXPECTED_ARTICLE_CANDIDATES & runtime_source_ids:
        fail("article candidate sources entered runtime catalog before N15-B2")
    if EXPECTED_ARTICLE_CANDIDATES & set(precedence.get("source_roles", {})):
        fail("article candidate sources entered runtime precedence before N15-B2")

    all_rule_ids = rule_ids(catalog) | nested_rule_ids(atomic_rules)
    premature = sorted(rule_id for rule_id in all_rule_ids if rule_id.startswith("article."))
    if premature:
        fail("article.* predicates were introduced during N15-B1: " + ", ".join(premature))

    authority = ledger.get("article_authority", {})
    if set(authority.get("candidate_sources", [])) != EXPECTED_ARTICLE_CANDIDATES:
        fail("B1 ledger candidate source set drifted")
    if authority.get("runtime_promotion_phase") != "N15-B2":
        fail("B1 ledger does not defer runtime promotion to N15-B2")
    if authority.get("article_predicates_added_in_b1") is not False:
        fail("B1 ledger incorrectly claims article predicate promotion")

    exit_criteria = ledger.get("exit_criteria", {})
    expected_true = {
        "five_of_five_ufc_guides_registered",
        "current_article_standard_reconciled",
        "stale_article_guide_references_mapped",
        "cepe_2015_2017_authority_relationship_modeled",
        "mec_and_capes_related_acts_classified",
        "release_independent_source_scope",
        "no_article_runtime_predicates",
        "ready_for_exact_head_source_contract",
    }
    false_criteria = sorted(key for key in expected_true if exit_criteria.get(key) is not True)
    if false_criteria:
        fail("B1 exit criteria not satisfied: " + ", ".join(false_criteria))

    print(
        "N15-EVIDENCE source-authority "
        "status=PASS phase=N15-B1 phase_status=CLOSURE_CANDIDATE "
        "ufc_guides=5/5 article_standard=ABNT_NBR_6022_2018 "
        "article_sources_runtime=false article_predicates=0 "
        "cepe_2015_program_authority=CLASSIFIED mec_1224_2013=REVOKED_EXCLUDED "
        "capes_59_2017=CONTEXTUAL_NONTECHNICAL source_scope=release-independent"
    )


if __name__ == "__main__":
    main()

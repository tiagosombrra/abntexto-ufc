#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "release" / "n15-b1-source-authority.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"

HISTORICAL_ARTICLE_CANDIDATES = {
    "ufc-guia-artigos-2021",
    "abnt-nbr-6022-2018",
}
CURRENT_GUIDES = {
    "ufc-guia-trabalhos-2022",
    "ufc-guia-artigos-2022",
    "ufc-guia-citacoes-2025",
    "ufc-guia-referencias-2023",
    "ufc-guia-projetos-2019",
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


def main() -> None:
    ledger = load_json(LEDGER)
    source_audit = load_json(SOURCE_AUDIT)

    if ledger.get("schema_version") != 1:
        fail("unsupported ledger schema_version")
    if ledger.get("phase") != "N15-B1" or ledger.get("status") != "CLOSURE_CANDIDATE":
        fail("historical N15-B1 ledger must remain a closure candidate")
    if ledger.get("base_main_sha") != "ab61d20c03f9b79e8d01b7913a721c85cd695491":
        fail("historical N15-B1 base main SHA drifted")

    authority = ledger.get("article_authority", {})
    if set(authority.get("candidate_sources", [])) != HISTORICAL_ARTICLE_CANDIDATES:
        fail("historical B1 candidate source set drifted")
    if authority.get("runtime_promotion_phase") != "N15-B2":
        fail("historical B1 ledger no longer records deferred runtime promotion")
    if authority.get("article_predicates_added_in_b1") is not False:
        fail("historical B1 ledger incorrectly claims article predicate promotion")

    if source_audit.get("scope") != "abntexto-ufc-current-sources":
        fail("current source registry scope is not release-independent")
    source_ids = {
        item.get("id")
        for item in source_audit.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    guides = {source_id for source_id in source_ids if source_id.startswith("ufc-guia-")}
    if guides != CURRENT_GUIDES:
        fail(f"current official UFC guide inventory drifted: {sorted(guides)}")
    if "ufc-guia-artigos-2021" in source_ids:
        fail("superseded B1 article-guide identity remained active")

    superseded = {
        item.get("id")
        for item in source_audit.get("reviewed_superseded_sources", [])
        if isinstance(item, dict)
    }
    if "ufc-guia-artigos-2021" not in superseded:
        fail("historical B1 article-guide identity is not preserved in superseded evidence")

    article_guide = next(
        item for item in source_audit["sources"] if item.get("id") == "ufc-guia-artigos-2022"
    )
    if article_guide.get("technical_authority") is not False:
        fail("current UFC article guide acquired technical-edition authority")
    nbr_6022 = next(
        item for item in source_audit["sources"] if item.get("id") == "abnt-nbr-6022-2018"
    )
    if nbr_6022.get("status") != "current" or nbr_6022.get("kind") != "technical-standard":
        fail("NBR 6022:2018 current technical classification drifted")

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
        fail("historical B1 exit criteria drifted: " + ", ".join(false_criteria))

    print(
        "N15-EVIDENCE source-authority "
        "status=PASS phase=N15-B1 phase_status=HISTORICAL_CERTIFIED "
        "historical_article_sources_runtime=false article_predicates_in_b1=0 "
        "current_guide=UFC_ARTICLE_2022 article_standard=ABNT_NBR_6022_2018"
    )


if __name__ == "__main__":
    main()

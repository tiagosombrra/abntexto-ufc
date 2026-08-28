#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import ACTIVE_STATUSES, load_catalog, source_map

POLICY = ROOT / "normativa" / "version-policy.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"
DOC = ROOT / "docs" / "VIGENCIA-NORMATIVA.md"
STATIC_ACTIVE_MACHINE_FILES = (
    ROOT / "normativa" / "catalog.json",
    ROOT / "normativa" / "precedence.json",
    ROOT / "normativa" / "atomic-rules.json",
    ROOT / "normativa" / "atomicity-plan.json",
    ROOT / "normativa" / "coverage-audit.json",
)


def active_machine_files() -> list[Path]:
    paths = list(STATIC_ACTIVE_MACHINE_FILES)
    paths.extend(sorted((ROOT / "normativa").glob("coverage-rules*.json")))
    return list(dict.fromkeys(paths))


def fail(message: str) -> None:
    raise SystemExit(f"Normative currency failed: {message}")


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return data


def main() -> None:
    policy = load_json(POLICY)
    source_audit = load_json(SOURCE_AUDIT)
    catalog = load_catalog()
    sources = source_map(catalog)

    if policy.get("schema_version") != 1:
        fail("unsupported version-policy schema_version")
    if policy.get("mode") != "latest-current-applicable-technical-standard-mandatory":
        fail("latest-current technical-edition policy is not mandatory")
    if policy.get("decision") != "mandatory":
        fail("version policy decision must be mandatory")

    rules = policy.get("policy")
    if not isinstance(rules, dict):
        fail("policy block is required")
    if rules.get("latest_current_technical_edition_mandatory") is not True:
        fail("latest current technical edition must be mandatory")
    if rules.get("stale_embedded_reference_can_govern") is not False:
        fail("stale embedded references must never govern")
    if rules.get("conflict_behavior") != "review-required":
        fail("current-source conflicts must require review")
    if not rules.get("profile_promotion_stages"):
        fail("profile source/contract/runtime promotion stages must be explicit")

    audited_sources = {
        source["id"]: source
        for source in source_audit.get("sources", [])
        if isinstance(source, dict) and source.get("id")
    }
    basis = policy.get("institutional_basis")
    if not isinstance(basis, list) or len(basis) < 3:
        fail("institutional basis must document general UFC, PPG and current SiBi authority")
    required_basis = {
        "ufc-res-17-cepe-2015",
        "ufc-res-17-cepe-2017",
        "ufc-normalizacao-2026",
    }
    basis_ids = {item.get("id") for item in basis if isinstance(item, dict)}
    if not required_basis <= basis_ids:
        fail("missing institutional basis: " + ", ".join(sorted(required_basis - basis_ids)))
    for source_id in required_basis:
        source = audited_sources.get(source_id)
        if not source:
            fail(f"institutional basis source is absent from source audit: {source_id}")
        if not str(source.get("status", "")).startswith("current"):
            fail(f"institutional basis source is not current: {source_id}")

    current_ids = policy.get("current_technical_sources")
    if not isinstance(current_ids, list) or not current_ids:
        fail("current_technical_sources must be non-empty")
    if "abnt-nbr-6022-2018" not in current_ids:
        fail("current article-presentation standard was not promoted into the technical set")
    for source_id in current_ids:
        source = sources.get(source_id)
        if not source:
            fail(f"current technical source is absent from runtime catalog: {source_id}")
        if source.get("kind") != "technical-standard":
            fail(f"current technical source is not a technical standard: {source_id}")
        if source.get("status") not in ACTIVE_STATUSES:
            fail(f"current technical source is not active: {source_id}")

    profile_candidates = policy.get("profile_candidates", {})
    article = profile_candidates.get("scientific_article") if isinstance(profile_candidates, dict) else None
    if not isinstance(article, dict):
        fail("scientific-article profile policy is missing")
    if article.get("status") != "contract-promotion-in-progress-runtime-pending":
        fail("scientific-article policy does not expose the B2-A contract state")
    if article.get("source_and_contract_phase") != "N15-B2A":
        fail("scientific-article source/contract phase must be N15-B2A")
    if article.get("runtime_implementation_phase") != "N15-B2B":
        fail("scientific-article LaTeX implementation must remain deferred to N15-B2B")
    if article.get("evidence_completion_phase") != "N15-B2C":
        fail("scientific-article evidence closure must remain deferred to N15-B2C")
    candidate_ids = article.get("candidate_sources")
    expected_article_sources = {"abnt-nbr-6022-2018", "ufc-guia-artigos-2022"}
    if set(candidate_ids or []) != expected_article_sources:
        fail("scientific-article authority source set drifted")
    for source_id in candidate_ids:
        audited = audited_sources.get(source_id)
        if not audited:
            fail(f"article authority source is absent from source audit: {source_id}")
        if not str(audited.get("status", "")).startswith("current"):
            fail(f"article authority source is not current: {source_id}")
        runtime = sources.get(source_id)
        if not runtime:
            fail(f"B2-A article authority source is absent from runtime catalog: {source_id}")
        if runtime.get("status") not in ACTIVE_STATUSES:
            fail(f"B2-A article authority source is not active in runtime catalog: {source_id}")

    if (ROOT / "abntexto-ufc" / "artigos.def").exists():
        fail("B2-A must not introduce the LaTeX article runtime module")

    doc = DOC.read_text(encoding="utf-8")
    supersessions = policy.get("supersessions")
    if not isinstance(supersessions, list) or not supersessions:
        fail("supersession map must be non-empty")

    machine_files = active_machine_files()
    active_text = {
        path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8")
        for path in machine_files
    }
    seen_pairs: set[tuple[str, str, str]] = set()

    for item in supersessions:
        if not isinstance(item, dict):
            fail("every supersession entry must be an object")
        context = item.get("context_source")
        old = item.get("superseded_reference")
        current = item.get("current_reference")
        current_source = item.get("current_source")
        if not all(isinstance(value, str) and value for value in (context, old, current, current_source)):
            fail("supersession entries require context_source, superseded_reference, current_reference and current_source")

        key = (context, old, current_source)
        if key in seen_pairs:
            fail(f"duplicate supersession mapping: {context} / {old} / {current_source}")
        seen_pairs.add(key)

        if context not in audited_sources:
            fail(f"unknown UFC context source: {context}")
        source = sources.get(current_source)
        if not source:
            fail(f"replacement source is absent from runtime catalog: {current_source}")
        if source.get("kind") != "technical-standard" or source.get("status") not in ACTIVE_STATUSES:
            fail(f"replacement source is not a current technical standard: {current_source}")

        if old not in doc or current not in doc:
            fail(f"human documentation does not expose mapping {old} -> {current}")

        for path, text in active_text.items():
            if old in text:
                fail(f"superseded technical edition leaked into active machine source {path}: {old}")

    required_doc_markers = (
        "Resolução nº 17/CEPE, de 02 de outubro de 2017",
        "Resolução nº 17/CEPE, de 04 de dezembro de 2015",
        "ABNT NBR 6022:2018",
        "N15-B2",
    )
    for marker in required_doc_markers:
        if marker not in doc:
            fail(f"human documentation is missing article-authority marker: {marker}")

    print(
        "Normative currency passed: "
        f"{len(current_ids)} active runtime technical standards, "
        f"{len(candidate_ids)} promoted article authority sources, "
        f"{len(supersessions)} documented UFC stale-reference mappings, "
        f"{len(machine_files)} active machine files scanned; "
        "N15-B2A contract promoted with LaTeX runtime deferred to N15-B2B."
    )


if __name__ == "__main__":
    main()

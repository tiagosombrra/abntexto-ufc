#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "normativa" / "source-audit.json"
CATALOG = ROOT / "normativa" / "catalog.json"
PRECEDENCE = ROOT / "normativa" / "precedence.json"
STATUS_POLICY = ROOT / "normativa" / "source-status-policy.json"


def fail(message: str) -> None:
    raise SystemExit(f"Normative source audit failed: {message}")


def validate_status_semantics(
    audit: dict,
    catalog: dict,
    by_id: dict[str, dict],
) -> tuple[int, int]:
    precedence = json.loads(PRECEDENCE.read_text(encoding="utf-8"))
    policy = json.loads(STATUS_POLICY.read_text(encoding="utf-8"))

    if policy.get("schema_version") != 1:
        fail("unsupported source-status-policy schema_version")
    if date.fromisoformat(policy["reviewed_at"]) < date.fromisoformat(audit["reviewed_at"]):
        fail("source-status-policy is older than the source audit")

    mappings = policy.get("registry_statuses")
    overrides = policy.get("source_overrides", {})
    if not isinstance(mappings, dict) or not mappings:
        fail("source-status-policy registry_statuses must be a non-empty object")
    if not isinstance(overrides, dict):
        fail("source-status-policy source_overrides must be an object")

    unknown_registry_statuses = sorted(
        {source["status"] for source in audit["sources"]} - set(mappings)
    )
    if unknown_registry_statuses:
        fail(
            "source-status-policy does not classify registry statuses: "
            + ", ".join(unknown_registry_statuses)
        )

    unknown_overrides = sorted(set(overrides) - set(by_id))
    if unknown_overrides:
        fail("source-status-policy has unknown source overrides: " + ", ".join(unknown_overrides))

    source_roles = precedence.get("source_roles", {})
    resolutions = precedence.get("rules", {})
    catalog_by_id = {source["id"]: source for source in catalog["sources"]}
    if set(source_roles) != set(catalog_by_id):
        fail("precedence source roles do not match the runtime catalog")

    restricted = 0
    scope_restricted = 0
    for source_id, runtime in catalog_by_id.items():
        registry = by_id[source_id]
        mapping = mappings[registry["status"]]
        override = overrides.get(source_id, {})

        allowed = override.get(
            "allowed_runtime_statuses",
            mapping.get("allowed_runtime_statuses", []),
        )
        if not isinstance(allowed, list):
            fail(f"source {source_id}: allowed_runtime_statuses must be a list")
        if runtime.get("status") not in allowed:
            fail(
                f"source {source_id}: runtime status {runtime.get('status')} is incompatible "
                f"with registry status {registry['status']}"
            )

        activity = mapping.get("runtime_activity")
        if activity == "scope-restricted":
            scope_restricted += 1
            if override.get("promotion_reviewed") is not True:
                fail(f"source {source_id}: scope-restricted source was promoted without review")

        technical_authority = mapping.get("technical_authority")
        if registry.get("technical_authority") is False or technical_authority is False:
            restricted += 1
            if registry.get("technical_authority") is not False:
                fail(f"source {source_id}: policy requires explicit technical_authority=false")
            role = source_roles[source_id]
            if role in {"technical-standard", "technical-guidance"}:
                fail(f"source {source_id}: restricted guide has technical runtime role {role}")
            for rule_id, resolution in resolutions.items():
                if resolution.get("scope") != "technical":
                    continue
                if source_id in resolution.get("governing_sources", []):
                    fail(
                        f"source {source_id}: restricted guide governs technical rule {rule_id}"
                    )

    return restricted, scope_restricted


def validate_b1_reconciliation(audit: dict, by_id: dict[str, dict]) -> None:
    article_guide = by_id.get("ufc-guia-artigos-2021")
    if not article_guide:
        fail("missing current UFC scientific-article guide")
    if article_guide.get("status") != "current-institutional-with-stale-technical-citations":
        fail("article guide must be restricted from technical-edition authority")
    if article_guide.get("technical_authority") is not False:
        fail("article guide cannot select the active ABNT edition")

    article_standard = by_id.get("abnt-nbr-6022-2018")
    if not article_standard:
        fail("missing reconciled current article-presentation technical standard")
    if article_standard.get("kind") != "technical-standard" or article_standard.get("status") != "current":
        fail("NBR 6022:2018 must be recorded as a current technical standard")

    cepe_2015 = by_id.get("ufc-res-17-cepe-2015")
    if not cepe_2015 or cepe_2015.get("status") != "current":
        fail("CEPE Resolution 17/2015 must be registered as a current institutional source")
    if "program-level-presentation-directives" not in cepe_2015.get("applies_to", []):
        fail("CEPE Resolution 17/2015 program-level presentation scope is missing")

    capes_59 = by_id.get("capes-portaria-59-2017")
    if not capes_59:
        fail("CAPES Portaria 59/2017 classification is missing")
    if capes_59.get("kind") != "external-regulation":
        fail("CAPES Portaria 59/2017 must remain an external regulation")
    if capes_59.get("technical_authority") is not False:
        fail("CAPES Portaria 59/2017 must not acquire technical formatting authority")
    if "postgraduate-program-evaluation" not in capes_59.get("applies_to", []):
        fail("CAPES Portaria 59/2017 evaluation scope is missing")

    excluded = audit.get("reviewed_excluded_sources")
    if not isinstance(excluded, list) or not excluded:
        fail("reviewed_excluded_sources must record reviewed non-current references")
    mec_records = [item for item in excluded if item.get("id") == "mec-portaria-1224-2013"]
    if len(mec_records) != 1:
        fail("MEC Portaria 1.224/2013 must have exactly one excluded-source record")
    mec = mec_records[0]
    if mec.get("status") != "revoked" or mec.get("technical_authority") is not False:
        fail("MEC Portaria 1.224/2013 must be recorded as revoked and non-technical")
    if "mec-portaria-1224-2013" in by_id:
        fail("revoked MEC Portaria 1.224/2013 leaked into the current source registry")

    candidates = audit.get("reconciled_profile_candidate_sources", {}).get("scientific-article")
    expected_candidates = {
        "ufc-guia-artigos-2021",
        "abnt-nbr-6022-2018",
        "abnt-nbr-10520-2023",
        "abnt-nbr-6023-2025",
        "abnt-nbr-6024-2012",
        "abnt-nbr-6028-2021",
        "ibge-tabular-1993",
    }
    if set(candidates or []) != expected_candidates:
        fail("scientific-article candidate source set is incomplete or drifted")


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    if audit.get("schema_version") != 1:
        fail("unsupported schema_version")
    if audit.get("scope") != "abntexto-ufc-current-sources":
        fail("unexpected release-dependent or unknown audit scope")

    reviewed = date.fromisoformat(audit["reviewed_at"])
    sources = audit.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("sources must be a non-empty list")

    by_id = {}
    for source in sources:
        source_id = source.get("id")
        if not source_id or source_id in by_id:
            fail(f"invalid or duplicate source id: {source_id}")
        by_id[source_id] = source
        for field in ("kind", "title", "publisher", "status", "checked_at"):
            if not source.get(field):
                fail(f"source {source_id}: missing {field}")
        if date.fromisoformat(source["checked_at"]) > reviewed:
            fail(f"source {source_id}: checked after audit review date")
        if source["status"] in {"superseded", "historical", "revoked"}:
            fail(f"legacy source must not remain in current inventory: {source_id}")

    catalog_ids = {source["id"] for source in catalog["sources"]}
    missing = sorted(catalog_ids - set(by_id))
    if missing:
        fail("runtime catalog sources missing from source inventory: " + ", ".join(missing))

    restricted, scope_restricted = validate_status_semantics(audit, catalog, by_id)

    expected_technical = {
        "abnt-nbr-14724-2024",
        "abnt-nbr-10520-2023",
        "abnt-nbr-6023-2025",
        "abnt-nbr-15287-2025",
        "abnt-nbr-6022-2018",
        "abnt-nbr-6028-2021",
        "abnt-nbr-6024-2012",
        "abnt-nbr-6027-2012",
        "abnt-nbr-6034-2004",
        "abnt-nbr-12225-2023",
    }
    if set(audit.get("current_technical_sources", [])) != expected_technical:
        fail("current technical standard set changed without source-authority review")

    institutional_guides = {
        "ufc-guia-trabalhos-2022",
        "ufc-guia-artigos-2021",
        "ufc-guia-citacoes-2025",
        "ufc-guia-referencias-2023",
        "ufc-guia-projetos-2019",
    }
    for source_id in institutional_guides:
        source = by_id.get(source_id)
        if not source:
            fail(f"missing current UFC guide: {source_id}")
        if source.get("status") != "current-institutional-with-stale-technical-citations":
            fail(f"UFC guide must be restricted from technical edition authority: {source_id}")
        if source.get("technical_authority") is not False:
            fail(f"UFC guide cannot define the active ABNT edition: {source_id}")

    in_2024 = by_id.get("ufc-in-2-2024")
    in_2026 = by_id.get("ufc-in-2-2026")
    if not in_2024 or not in_2026:
        fail("current UFC deposit instructions are incomplete")
    if in_2024.get("status") != "current-with-superseded-provisions":
        fail("IN 2/2024 must record partial supersession")
    overrides = in_2026.get("overrides", [])
    if not any(
        item.get("source") == "ufc-in-2-2024"
        and item.get("scope") == "visual-catalog-card-requirement"
        for item in overrides
    ):
        fail("IN 2/2026 must explicitly override the old visual catalog-card requirement")

    required_ufc = {
        "ufc-res-17-cepe-2015",
        "ufc-res-17-cepe-2017",
        "ufc-res-05-consuni-2023",
        "ufc-in-2-2024",
        "ufc-in-2-2026",
        "ufc-deposito-tcc-2026",
        "ufc-deposito-pos-2026",
        "ufc-ficha-catalografica-2026",
    }
    missing_ufc = sorted(required_ufc - set(by_id))
    if missing_ufc:
        fail("missing current UFC institutional sources: " + ", ".join(missing_ufc))

    forbidden_ids = {
        "abnt-nbr-14724-2011",
        "abnt-nbr-10520-2002",
        "abnt-nbr-6023-2018",
        "abnt-nbr-15287-2011",
        "abnt-nbr-12225-2004",
        "mec-portaria-1224-2013",
    }
    leaked = sorted(forbidden_ids & set(by_id))
    if leaked:
        fail("superseded, revoked or historical sources retained as active entries: " + ", ".join(leaked))

    validate_b1_reconciliation(audit, by_id)

    print(
        "Normative source audit passed: "
        f"{len(sources)} current/restricted sources, "
        f"{len(expected_technical)} current ABNT standards, "
        f"{len(institutional_guides)} UFC guides restricted from edition authority, "
        f"{restricted} restricted runtime sources, "
        f"{scope_restricted} scope-restricted runtime sources; "
        "N15-B1 article/graduate authority reconciliation present."
    )


if __name__ == "__main__":
    main()

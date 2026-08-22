#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_atomic import atomic_rule_map, load_atomic_contract
from normative_catalog import load_catalog

AUDIT = ROOT / "normativa" / "coverage-audit.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"

REQUIRED_DOMAINS = {
    "page-geometry",
    "typography",
    "paragraphs",
    "sections",
    "pretextual",
    "pagination",
    "footnotes",
    "toc",
    "citations",
    "references",
    "objects",
    "equations",
    "code-algorithms",
    "posttextual",
    "multivolume",
    "project",
    "deposit",
    "accessibility-distribution",
}

PRIORITY_GAPS = {
    "pagination.pretextual.counted-not-numbered",
    "pagination.catalog-data.not-counted",
    "pagination.textual.display-start",
    "footnote.separator.length",
    "footnote.hanging-alignment",
    "cover.required-fields",
    "title-page.required-fields",
    "approval.required-fields",
    "summary.required-elements",
    "summary.keywords.format",
    "section.primary.recto-duplex",
    "section.multiline.hanging",
    "citation.direct-short.presentation",
    "references.doi-url-access",
    "equation.numbering.right",
    "project.nbr15287.structure",
    "spine.presentation",
}


def fail(message: str) -> None:
    raise SystemExit(f"Normative coverage audit failed: {message}")


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    source_audit = json.loads(SOURCE_AUDIT.read_text(encoding="utf-8"))
    catalog = load_catalog()
    atomic = atomic_rule_map(load_atomic_contract(catalog))
    known_source_ids = {source["id"] for source in catalog["sources"]}
    known_source_ids |= {source["id"] for source in source_audit.get("sources", [])}

    if audit.get("schema_version") != 1:
        fail("unsupported schema_version")
    if audit.get("phase") != "N4":
        fail("unexpected phase")
    if audit.get("phase_status") not in {"in-progress", "complete"}:
        fail("invalid phase_status")

    allowed = set(audit.get("allowed_treatments", []))
    expected_allowed = {"automatic", "automatic-partial", "manual", "conditional", "not-applicable"}
    if allowed != expected_allowed:
        fail("unexpected treatment vocabulary")

    domains = audit.get("domains")
    if not isinstance(domains, dict):
        fail("domains must be an object")
    declared = set(audit.get("required_domains", []))
    if declared != REQUIRED_DOMAINS or set(domains) != REQUIRED_DOMAINS:
        missing = sorted(REQUIRED_DOMAINS - set(domains))
        extra = sorted(set(domains) - REQUIRED_DOMAINS)
        fail(f"domain coverage mismatch; missing={missing}, extra={extra}")

    runner = (ROOT / "tests" / "run.py").read_text(encoding="utf-8")
    known_gates = set(re.findall(r'Check\("([^"]+)"', runner))

    gap_ids: set[str] = set()
    for domain_id, domain in domains.items():
        existing = domain.get("existing_atomic_rules", [])
        if not isinstance(existing, list):
            fail(f"{domain_id}: existing_atomic_rules must be a list")
        unknown_atomic = sorted(set(existing) - set(atomic))
        if unknown_atomic:
            fail(f"{domain_id}: unknown atomic rules: {', '.join(unknown_atomic)}")

        gates = domain.get("gates", [])
        if not isinstance(gates, list):
            fail(f"{domain_id}: gates must be a list")
        unknown = sorted(set(gates) - known_gates)
        if unknown:
            fail(f"{domain_id}: unknown unified gates: {', '.join(unknown)}")

        gaps = domain.get("gaps", [])
        if not isinstance(gaps, list):
            fail(f"{domain_id}: gaps must be a list")
        for gap in gaps:
            gap_id = gap.get("id")
            if not isinstance(gap_id, str) or not gap_id:
                fail(f"{domain_id}: gap without id")
            if gap_id in gap_ids:
                fail(f"duplicate gap id: {gap_id}")
            if gap_id in atomic:
                fail(f"gap already exists in atomic contract: {gap_id}")
            gap_ids.add(gap_id)

            if not gap.get("requirement"):
                fail(f"{gap_id}: requirement is required")
            treatment = gap.get("planned_treatment")
            if treatment not in allowed:
                fail(f"{gap_id}: invalid planned_treatment {treatment}")

            candidate_sources = gap.get("candidate_sources")
            if not isinstance(candidate_sources, list):
                fail(f"{gap_id}: candidate_sources must be a list")
            unknown_sources = sorted(set(candidate_sources) - known_source_ids)
            if unknown_sources:
                fail(f"{gap_id}: unknown candidate sources: {', '.join(unknown_sources)}")
            if not candidate_sources and gap.get("classification") not in {"project-policy", "technical-profile"}:
                fail(f"{gap_id}: source-free gap must be explicitly project-policy or technical-profile")

    missing_priority = sorted(PRIORITY_GAPS - gap_ids)
    if missing_priority:
        fail("priority N4 gaps disappeared before promotion: " + ", ".join(missing_priority))

    if audit["phase_status"] == "complete" and gap_ids:
        fail("N4 cannot be complete while explicit gaps remain")

    print(
        "Normative coverage inventory passed: "
        f"{len(domains)} domains, {len(atomic)} atomic rules, "
        f"{len(gap_ids)} explicit N4 gaps, status={audit['phase_status']}."
    )


if __name__ == "__main__":
    main()

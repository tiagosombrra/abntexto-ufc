#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from path_resolver import ROOT, check_file, integration_file, repository_relative  # noqa: E402

TESTS = ROOT / "tests"
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from repository_paths import standard_file, standard_files  # noqa: E402


def fail(message: str) -> int:
    print(f"Path resolution contract failed: {message}")
    return 1


def duplicate_basenames(paths: list[Path]) -> list[str]:
    counts = Counter(path.name for path in paths)
    return sorted(name for name, count in counts.items() if count > 1)


def active_text_surfaces() -> list[Path]:
    excluded_roots = (
        ROOT / "docs" / "history",
        ROOT / "release" / "history",
    )
    excluded_exact = {
        "CHANGELOG.md",
        "docs/REPOSITORY-MAINTENANCE.md",
        # This contract intentionally names retired flat paths in negative
        # assertions proving that compatibility copies do not exist.
        "tests/checks/repository/path_resolution_contract.py",
    }
    text_suffixes = {
        ".cff",
        ".js",
        ".json",
        ".md",
        ".ps1",
        ".py",
        ".sh",
        ".tex",
        ".yaml",
        ".yml",
    }

    surfaces: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith(".git/"):
            continue
        if relative in excluded_exact or any(root in path.parents for root in excluded_roots):
            continue
        if path.name == "Makefile" or path.suffix.lower() in text_suffixes:
            surfaces.append(path)
    return sorted(surfaces)


def stale_flat_standard_references(standard_candidates: list[Path]) -> list[str]:
    moved = [
        path
        for path in standard_candidates
        if path.parent != ROOT / "standards"
    ]
    findings: list[str] = []
    surfaces = active_text_surfaces()

    for authority in moved:
        legacy = f"standards/{authority.name}"
        current = authority.relative_to(ROOT).as_posix()
        for surface in surfaces:
            text = surface.read_text(encoding="utf-8", errors="replace")
            composed_patterns = (
                legacy,
                f'ROOT / "standards" / "{authority.name}"',
                f"ROOT / 'standards' / '{authority.name}'",
            )
            if any(pattern in text for pattern in composed_patterns):
                source = surface.relative_to(ROOT).as_posix()
                findings.append(
                    f"{source}: stale flat standards path {legacy}; current authority is {current}"
                )
    return sorted(set(findings))


def stale_flat_check_references(moved_paths: dict[str, str]) -> list[str]:
    findings: list[str] = []
    surfaces = active_text_surfaces()
    for filename, current in sorted(moved_paths.items()):
        legacy = f"tests/checks/{filename}"
        for surface in surfaces:
            text = surface.read_text(encoding="utf-8", errors="replace")
            if legacy in text:
                source = surface.relative_to(ROOT).as_posix()
                findings.append(
                    f"{source}: stale flat check path {legacy}; current path is {current}"
                )
    return sorted(set(findings))


def main() -> int:
    check_candidates = sorted((ROOT / "tests" / "checks").rglob("*.py"))
    integration_candidates = sorted(
        path
        for path in (ROOT / "tests" / "integration").rglob("*")
        if path.is_file() and path.suffix in {".py", ".sh"}
    )
    standard_candidates = sorted((ROOT / "standards").rglob("*.json"))

    moved_repository_checks = {
        "canonical_identity.py",
        "engineering_language.py",
        "librarian_review_contract.py",
        "linux_integration_suites.py",
        "metadata_consistency.py",
        "path_resolution_contract.py",
        "phase_governance.py",
        "repository_contract.py",
    }
    moved_distribution_checks = {
        "distribution_bundles.py",
        "public_bundles.py",
    }
    moved_validator_checks = {
        "pdf_validation_core.py",
        "validator_source.py",
    }
    moved_profile_checks = {
        "profile_matrix_contract.py",
        "scientific_article_body.py",
        "scientific_article_evidence_map.py",
        "scientific_article_front_block.py",
        "scientific_article_profile_contract.py",
        "scientific_article_recommendations_contract.py",
    }
    moved_check_paths = {
        **{
            filename: f"tests/checks/repository/{filename}"
            for filename in moved_repository_checks
        },
        **{
            filename: f"tests/checks/distribution/{filename}"
            for filename in moved_distribution_checks
        },
        **{
            filename: f"tests/checks/validator/{filename}"
            for filename in moved_validator_checks
        },
        **{
            filename: f"tests/checks/profiles/{filename}"
            for filename in moved_profile_checks
        },
    }

    duplicate_checks = duplicate_basenames(check_candidates)
    duplicate_integrations = duplicate_basenames(integration_candidates)
    duplicate_standards = duplicate_basenames(standard_candidates)
    stale_standard_paths = stale_flat_standard_references(standard_candidates)
    if stale_standard_paths:
        return fail("active stale standards references: " + " | ".join(stale_standard_paths))
    stale_check_paths = stale_flat_check_references(moved_check_paths)
    if stale_check_paths:
        return fail("active stale check references: " + " | ".join(stale_check_paths))
    if duplicate_checks:
        return fail("ambiguous check basenames: " + ", ".join(duplicate_checks))
    if duplicate_integrations:
        return fail("ambiguous integration basenames: " + ", ".join(duplicate_integrations))
    if duplicate_standards:
        return fail("ambiguous standards basenames: " + ", ".join(duplicate_standards))

    fixed_depth_root = "Path(__file__).resolve().parents" + "[2]"
    for filename, current in sorted(moved_check_paths.items()):
        source = check_file(filename)
        text = source.read_text(encoding="utf-8")
        if fixed_depth_root in text:
            return fail(f"prepared check {filename} still derives repository root by fixed depth")
        if "from path_resolver import" not in text or "ROOT" not in text:
            return fail(f"prepared check {filename} must import ROOT from tests/path_resolver.py")
        expected_source = ROOT / current
        if source != expected_source:
            return fail(f"moved check {filename} must resolve at {current}")
        if (ROOT / "tests" / "checks" / filename).exists():
            return fail(f"flat compatibility copy is forbidden for moved check {filename}")

    nested_depth_coupled = []
    for source in check_candidates:
        relative_parent = source.parent.relative_to(ROOT / "tests" / "checks")
        if relative_parent == Path("."):
            continue
        text = source.read_text(encoding="utf-8")
        if fixed_depth_root in text:
            nested_depth_coupled.append(source.relative_to(ROOT).as_posix())
    if nested_depth_coupled:
        return fail(
            "nested checks cannot derive repository root by fixed parents[2] depth: "
            + ", ".join(nested_depth_coupled)
        )

    expected = {
        "check": repository_relative(check_file("metadata_consistency.py")),
        "integration": repository_relative(integration_file("profile-matrix.sh")),
        "catalog": standard_file("catalog.json").relative_to(ROOT).as_posix(),
        "precedence": standard_file("precedence.json").relative_to(ROOT).as_posix(),
        "public_api": standard_file("public-api.json").relative_to(ROOT).as_posix(),
    }
    if expected["check"] != "tests/checks/repository/metadata_consistency.py":
        return fail("metadata consistency check must resolve under tests/checks/repository")
    if not expected["integration"].startswith("tests/integration/"):
        return fail("integration resolver escaped tests/integration")
    if not expected["catalog"].startswith("standards/"):
        return fail("standard resolver escaped standards")
    if not expected["precedence"].startswith("standards/"):
        return fail("precedence resolver escaped standards")
    if expected["public_api"] != "standards/api/public-api.json":
        return fail("public API authority must resolve under standards/api")
    if (ROOT / "standards" / "public-api.json").exists():
        return fail("flat compatibility copy is forbidden for moved public API authority")

    coverage = standard_files("coverage-rules*.json")
    if len(coverage) < 2:
        return fail("recursive standards discovery returned an implausibly small coverage set")

    static_text = (ROOT / "tests" / "static.py").read_text(encoding="utf-8")
    run_text = (ROOT / "tests" / "run.py").read_text(encoding="utf-8")
    catalog_text = (ROOT / "tools" / "normative_catalog.py").read_text(encoding="utf-8")
    atomic_text = (ROOT / "tools" / "normative_atomic.py").read_text(encoding="utf-8")
    full_text = (ROOT / "tools" / "normative_full.py").read_text(encoding="utf-8")

    if '"tests/checks/' in static_text:
        return fail("tests/static.py reintroduced flat check paths")
    if "tests/checks/" in run_text:
        return fail("tests/run.py reintroduced flat check paths")
    if '("sh", "tests/integration/' in run_text:
        return fail("tests/run.py reintroduced flat integration command paths")
    for label, text in (
        ("normative_catalog.py", catalog_text),
        ("normative_atomic.py", atomic_text),
    ):
        if 'ROOT / "standards" /' in text:
            return fail(f"{label} reintroduced flat standards authority paths")
    if ".glob(DEFAULT_COVERAGE_GLOB)" in full_text:
        return fail("normative_full.py must discover coverage manifests recursively")

    moved_rule_authorities = {
        "atomic-rules.json",
        "coverage-rules.json",
        "coverage-rules-article.json",
        "coverage-rules-citations.json",
        "coverage-rules-closure.json",
        "coverage-rules-documentary.json",
        "coverage-rules-frontmatter.json",
        "coverage-rules-project.json",
    }
    for filename in sorted(moved_rule_authorities):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "rules":
            return fail(f"rule authority {filename} must resolve under standards/rules")
        if (ROOT / "standards" / filename).exists():
            return fail(f"flat compatibility copy is forbidden for moved rule authority {filename}")

    moved_catalog_authorities = {
        "catalog.json",
        "precedence.json",
        "reference-guide-map.json",
        "source-audit.json",
        "source-status-policy.json",
        "version-policy.json",
    }
    for filename in sorted(moved_catalog_authorities):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "catalog":
            return fail(f"catalog authority {filename} must resolve under standards/catalog")
        if (ROOT / "standards" / filename).exists():
            return fail(f"flat compatibility copy is forbidden for moved catalog authority {filename}")

    moved_evidence_authorities = {
        "article-evidence-map.json",
        "evidence-contribution-policy.json",
        "evidence-registry.json",
        "false-coverage-policy.json",
        "proof-policy.json",
        "test-surface-policy.json",
        "validation-overrides.json",
        "validation-reference-policy.json",
        "vector-rule-validation-extension.json",
    }
    for filename in sorted(moved_evidence_authorities):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "evidence":
            return fail(f"evidence authority {filename} must resolve under standards/evidence")
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved evidence authority {filename}"
            )

    moved_locator_audits = {
        "locator-audit.json",
        "locator-audit-article.json",
        "locator-audit-backmatter.json",
        "locator-audit-citations.json",
        "locator-audit-deposit.json",
        "locator-audit-final.json",
        "locator-audit-layout-pagination.json",
        "locator-audit-objects-equations.json",
        "locator-audit-references.json",
        "locator-audit-sections-footnotes-nature.json",
        "locator-audit-typography-paragraphs.json",
    }
    for filename in sorted(moved_locator_audits):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "audits" / "locator":
            return fail(f"locator audit {filename} must resolve under standards/audits/locator")
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved locator audit {filename}"
            )

    moved_frontmatter_scenarios = {
        "frontmatter-acknowledgments-scenario.json",
        "frontmatter-alignment-scenarios.json",
        "frontmatter-approval-scenario.json",
        "frontmatter-cover-scenario.json",
        "frontmatter-errata-scenario.json",
        "frontmatter-lists-scenario.json",
        "frontmatter-pagination-scenario.json",
        "frontmatter-scenarios.json",
        "frontmatter-summary-scenario.json",
        "frontmatter-title-page-scenario.json",
        "frontmatter-toc-scenario.json",
    }
    for filename in sorted(moved_frontmatter_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "frontmatter":
            return fail(
                f"frontmatter scenario {filename} must resolve under standards/scenarios/frontmatter"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved frontmatter scenario {filename}"
            )

    moved_citation_scenarios = {
        "apud-presentation-scenario.json",
        "direct-citation-source-scenario.json",
        "indirect-citation-source-scenario.json",
        "long-quotation-scenario.json",
        "long-quote-reduced-size-scenario.json",
        "short-direct-citation-scenario.json",
        "ufc-citation-system-scenario.json",
    }
    for filename in sorted(moved_citation_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "citations":
            return fail(
                f"citation scenario {filename} must resolve under standards/scenarios/citations"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved citation scenario {filename}"
            )


    moved_layout_scenarios = {
        "body-paragraph-scenario.json",
        "page-margins-scenario.json",
        "pagination-geometry-scenario.json",
    }
    for filename in sorted(moved_layout_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "layout":
            return fail(
                f"layout scenario {filename} must resolve under standards/scenarios/layout"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved layout scenario {filename}"
            )

    moved_typography_scenarios = {
        "typography-scenario.json",
    }
    for filename in sorted(moved_typography_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "typography":
            return fail(
                f"typography scenario {filename} must resolve under standards/scenarios/typography"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved typography scenario {filename}"
            )

    moved_footnote_scenarios = {
        "footnote-separator-scenario.json",
        "footnote-text-scenario.json",
    }
    for filename in sorted(moved_footnote_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "footnotes":
            return fail(
                f"footnote scenario {filename} must resolve under standards/scenarios/footnotes"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved footnote scenario {filename}"
            )

    moved_section_scenarios = {
        "section-hierarchy-scenario.json",
        "section-indicator-scenario.json",
        "section-multiline-hanging-scenario.json",
        "section-primary-after-spacing-scenario.json",
        "section-primary-recto-duplex-scenario.json",
        "section-unnumbered-centered-scenario.json",
        "subsection-spacing-scenario.json",
    }
    for filename in sorted(moved_section_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "sections":
            return fail(
                f"section scenario {filename} must resolve under standards/scenarios/sections"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved section scenario {filename}"
            )

    moved_backmatter_scenarios = {
        "appendix-annex-final-pdf-scenario.json",
        "index-glossary-final-pdf-scenario.json",
    }
    for filename in sorted(moved_backmatter_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "backmatter":
            return fail(
                f"backmatter scenario {filename} must resolve under standards/scenarios/backmatter"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved backmatter scenario {filename}"
            )

    moved_object_scenarios = {
        "equation-display-final-pdf-scenario.json",
        "illustration-final-pdf-scenario.json",
        "table-ibge-vector-final-pdf-scenario.json",
        "table-typography-final-pdf-scenario.json",
    }
    for filename in sorted(moved_object_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "objects":
            return fail(
                f"object scenario {filename} must resolve under standards/scenarios/objects"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved object scenario {filename}"
            )

    moved_reference_scenarios = {
        "reference-layout-scenario.json",
        "reference-semantics-scenario.json",
    }
    for filename in sorted(moved_reference_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "references":
            return fail(
                f"reference scenario {filename} must resolve under standards/scenarios/references"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved reference scenario {filename}"
            )

    moved_research_project_scenarios = {
        "research-project-structure-final-pdf-scenario.json",
    }
    for filename in sorted(moved_research_project_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "research-project":
            return fail(
                f"research-project scenario {filename} must resolve under standards/scenarios/research-project"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved research-project scenario {filename}"
            )

    moved_negative_scenarios = {
        "negative-paths.json",
    }
    for filename in sorted(moved_negative_scenarios):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "scenarios" / "negative":
            return fail(
                f"negative scenario {filename} must resolve under standards/scenarios/negative"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved negative scenario {filename}"
            )


    moved_migration_authorities = {
        "atomicity-plan.json",
        "rule-migrations.json",
    }
    for filename in sorted(moved_migration_authorities):
        resolved = standard_file(filename)
        if resolved.parent != ROOT / "standards" / "migrations":
            return fail(
                f"migration authority {filename} must resolve under standards/migrations"
            )
        if (ROOT / "standards" / filename).exists():
            return fail(
                f"flat compatibility copy is forbidden for moved migration authority {filename}"
            )

    unexpected_root_authorities = sorted(
        path.name
        for path in (ROOT / "standards").iterdir()
        if path.is_file() and path.name != "README.md"
    )
    if unexpected_root_authorities:
        return fail(
            "standards root must contain only README.md plus semantic directories: "
            + ", ".join(unexpected_root_authorities)
        )

    web_lite_text = (ROOT / "tests" / "integration" / "web-lite-e2e.py").read_text(
        encoding="utf-8"
    )
    if 'standard_file("catalog.json")' not in web_lite_text:
        return fail("Web/Lite E2E must resolve catalog.json through the canonical standards resolver")
    if 'ROOT / "standards" / "catalog.json"' in web_lite_text:
        return fail("Web/Lite E2E reintroduced the retired flat catalog path")

    print(
        "PATH-RESOLUTION-EVIDENCE status=PASS "
        f"checks={len(check_candidates)} integrations={len(integration_candidates)} "
        f"standards={len(standard_candidates)} coverage_manifests={len(coverage)} "
        f"identity=basename unique=true recursive=true ambiguity=fail-closed repository_checks={len(moved_repository_checks)} distribution_checks={len(moved_distribution_checks)} validator_checks={len(moved_validator_checks)} profile_checks={len(moved_profile_checks)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

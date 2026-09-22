#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"
TOOLS = ROOT / "tools"

for path in (TESTS, TOOLS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from path_resolver import check_file, integration_file, repository_relative  # noqa: E402
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
        "tests/checks/path_resolution_contract.py",
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


def main() -> int:
    check_candidates = sorted((ROOT / "tests" / "checks").rglob("*.py"))
    integration_candidates = sorted(
        path
        for path in (ROOT / "tests" / "integration").rglob("*")
        if path.is_file() and path.suffix in {".py", ".sh"}
    )
    standard_candidates = sorted((ROOT / "standards").rglob("*.json"))

    duplicate_checks = duplicate_basenames(check_candidates)
    duplicate_integrations = duplicate_basenames(integration_candidates)
    duplicate_standards = duplicate_basenames(standard_candidates)
    stale_standard_paths = stale_flat_standard_references(standard_candidates)
    if stale_standard_paths:
        return fail("active stale standards references: " + " | ".join(stale_standard_paths))
    if duplicate_checks:
        return fail("ambiguous check basenames: " + ", ".join(duplicate_checks))
    if duplicate_integrations:
        return fail("ambiguous integration basenames: " + ", ".join(duplicate_integrations))
    if duplicate_standards:
        return fail("ambiguous standards basenames: " + ", ".join(duplicate_standards))

    expected = {
        "check": repository_relative(check_file("metadata_consistency.py")),
        "integration": repository_relative(integration_file("profile-matrix.sh")),
        "catalog": standard_file("catalog.json").relative_to(ROOT).as_posix(),
        "precedence": standard_file("precedence.json").relative_to(ROOT).as_posix(),
        "public_api": standard_file("public-api.json").relative_to(ROOT).as_posix(),
    }
    if not expected["check"].startswith("tests/checks/"):
        return fail("check resolver escaped tests/checks")
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
        "identity=basename unique=true recursive=true ambiguity=fail-closed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

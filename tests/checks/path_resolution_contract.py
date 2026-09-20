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
    }
    if not expected["check"].startswith("tests/checks/"):
        return fail("check resolver escaped tests/checks")
    if not expected["integration"].startswith("tests/integration/"):
        return fail("integration resolver escaped tests/integration")
    if not expected["catalog"].startswith("standards/"):
        return fail("standard resolver escaped standards")
    if not expected["precedence"].startswith("standards/"):
        return fail("precedence resolver escaped standards")

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

    print(
        "PATH-RESOLUTION-EVIDENCE status=PASS "
        f"checks={len(check_candidates)} integrations={len(integration_candidates)} "
        f"standards={len(standard_candidates)} coverage_manifests={len(coverage)} "
        "identity=basename unique=true recursive=true ambiguity=fail-closed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

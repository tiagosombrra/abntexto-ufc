#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from integration_suites import SUITES, infer_suites  # noqa: E402
import run as validation_run  # noqa: E402

WORKFLOW = ROOT / ".github" / "workflows" / "linux-integration.yml"
ROADMAP = ROOT / "release" / "v3-roadmap.json"


def fail(message: str) -> None:
    raise SystemExit(f"Linux integration suite contract failed: {message}")


def main() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    known_checks = {check.name for check in validation_run.CHECKS}

    if SUITES.get("complete") != ("*",):
        fail("complete suite must remain the wildcard full PR integration contract")

    for suite, checks in SUITES.items():
        if checks == ("*",):
            continue
        unknown = sorted(set(checks) - known_checks)
        if unknown:
            fail(f"suite {suite!r} references unknown checks: {', '.join(unknown)}")

    required_manual_choices = ("auto", *SUITES.keys())
    missing_choices = [
        choice
        for choice in required_manual_choices
        if f"          - {choice}\n" not in workflow
    ]
    if missing_choices:
        fail("workflow_dispatch scope choices are missing: " + ", ".join(missing_choices))

    for token in (
        "tests/integration_suites.py --base",
        "tests/run.py --mode pr --suite",
        "manual-auto-fail-closed",
        "documentation-only",
    ):
        if token not in workflow:
            fail(f"workflow is missing scoped orchestration token: {token}")

    if infer_suites(["docs/ROADMAP-V3.0.0.md"]) != ():
        fail("documentation-only changes must not trigger heavy Linux integration")
    if infer_suites(["tests/integration/scientific-article-profile.sh"]) != ("article",):
        fail("article-specific integration changes must select the article suite")
    if infer_suites(["abntexto-ufc/objects.def"]) != ("objects",):
        fail("object runtime changes must select the objects suite")
    if infer_suites(["unknown/technical.file"]) != ("complete",):
        fail("unknown technical paths must fail closed to complete")

    phase = roadmap.get("phase")
    if phase in {"scientific-article", "final-certification", "release"}:
        article_checks = set(SUITES.get("article", ()))
        if "scientific-article-profile" not in article_checks:
            fail("article suite must include the executable scientific-article-profile gate")
        if "validator-source" not in article_checks:
            fail("article suite must retain the source/authority contract gate")

    print(
        "LINUX-SUITE-EVIDENCE status=PASS "
        f"suites={len(SUITES)} checks={len(known_checks)} "
        f"manual_choices={len(required_manual_choices)} phase={phase} "
        "unknown_path_fallback=complete article_executable=true"
    )


if __name__ == "__main__":
    main()

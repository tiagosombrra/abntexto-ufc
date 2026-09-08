#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from integration_suites import (  # noqa: E402
    SUITES,
    infer_suites,
    release_candidate_requires_complete,
    select_suites,
)
import run as validation_run  # noqa: E402

WORKFLOW = ROOT / ".github" / "workflows" / "linux-integration.yml"
ROADMAP = ROOT / "release" / "v3-roadmap.json"
PROFILE_MATRIX = ROOT / "tests" / "integration" / "profile-matrix.sh"
ARTICLE_PROFILE = ROOT / "tests" / "integration" / "scientific-article-profile.sh"


def fail(message: str) -> None:
    raise SystemExit(f"Linux integration suite contract failed: {message}")


def main() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    profile_matrix = PROFILE_MATRIX.read_text(encoding="utf-8")
    article_profile = ARTICLE_PROFILE.read_text(encoding="utf-8")
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
        "github.event.before",
        "github.event.after",
        "incremental-push",
        "git cat-file -e",
        "missing-before-full-pr",
        "tests/integration_suites.py --base",
        "tests/run.py --mode pr --suite",
        "manual-auto-fail-closed",
        "documentation-only",
    ):
        if token not in workflow:
            fail(f"workflow is missing scoped orchestration token: {token}")

    if infer_suites(["docs/ROADMAP-V3.0.0.md"]) != ():
        fail("documentation-only changes must remain a pure auto-scope skip when no candidate override applies")
    if infer_suites(["tests/run.py"]) != ("smoke",):
        fail("orchestration-only changes must select smoke")
    if infer_suites(
        ["tests/run.py", "tests/integration/scientific-article-foreign-elements.sh"]
    ) != ("article",):
        fail("orchestration plus article changes must select article, not complete")
    if infer_suites(
        ["tests/run.py", "tests/integration/scientific-article-body.sh"]
    ) != ("article",):
        fail("orchestration plus Step 4 article changes must select article, not complete")
    if infer_suites(
        ["tests/run.py", "tests/integration/scientific-article-recommendations.sh"]
    ) != ("article",):
        fail("orchestration plus Step 5 article changes must select article, not complete")
    if infer_suites(["abntexto-ufc/objects.def"]) != ("objects",):
        fail("object runtime changes must select the objects suite")
    if infer_suites(["unknown/technical.file"]) != ("complete",):
        fail("unknown technical paths must fail closed to complete")

    phase = roadmap.get("phase")
    release_candidate_override = False
    if phase == "release":
        release_candidate_override = release_candidate_requires_complete()
        if not release_candidate_override:
            fail("active Release phase must expose an active non-temporary candidate marker")
        for paths in (
            ["docs/ROADMAP-V3.0.0.md"],
            ["tests/integration_suites.py"],
            ["tests/integration_suites.py", "docs/V3-RELEASE-PHASE.md"],
        ):
            if select_suites(paths, release_candidate_active=True) != ("complete",):
                fail("active Release candidate must override incremental path scope to complete")

    if phase in {"scientific-article", "final-certification", "release"}:
        required_article_checks = {
            "validator-source",
            "scientific-article-profile",
            "scientific-article-front-block",
            "scientific-article-foreign-elements",
            "scientific-article-body",
            "scientific-article-recommendations",
        }
        article_checks = set(SUITES.get("article", ()))
        missing_article = sorted(required_article_checks - article_checks)
        if missing_article:
            fail("article suite is missing executable checks: " + ", ".join(missing_article))

    if "scientific-article-profile.sh" in profile_matrix:
        fail("non-article profile matrix must not hide the article gate")
    for chained in (
        "scientific-article-front-block.sh",
        "scientific-article-foreign-elements.sh",
        "scientific-article-body.sh",
        "scientific-article-recommendations.sh",
    ):
        if chained in article_profile:
            fail(f"article profile gate must not chain {chained}")

    print(
        "LINUX-SUITE-EVIDENCE status=PASS "
        f"suites={len(SUITES)} checks={len(known_checks)} "
        f"manual_choices={len(required_manual_choices)} phase={phase} "
        "incremental_sync=true missing_before_fallback=full-pr "
        "unknown_path_fallback=complete article_first_class=true "
        "step4_registered=true step5_registered=true "
        f"release_candidate_override={str(release_candidate_override).lower()}"
    )


if __name__ == "__main__":
    main()

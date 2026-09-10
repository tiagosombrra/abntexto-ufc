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
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "linux-release-check.yml"
ROADMAP = ROOT / "release" / "v3-roadmap.json"
PROFILE_MATRIX = ROOT / "tests" / "integration" / "profile-matrix.sh"
ARTICLE_PROFILE = ROOT / "tests" / "integration" / "scientific-article-profile.sh"
DISTRIBUTION_BUNDLES = ROOT / "tests" / "integration" / "distribution-bundles.sh"
RELEASE_REVIEW_PAIRS = ROOT / "tests" / "integration" / "release-review-pairs.sh"
RELEASE_CANDIDATE_MARKER = "release/v3-release-candidate.json"
CORRECTION_STATE = "release/v3.0.1-final-corrections.json"
RELEASE_WORKFLOW_PATH = ".github/workflows/linux-release-check.yml"
DISTRIBUTION_BUILDER = "tools/build-public-bundles.py"
DISTRIBUTION_WRAPPER = "tools/build-distribution-bundles.py"
DISTRIBUTION_GATE = "tests/integration/distribution-bundles.sh"


def fail(message: str) -> None:
    raise SystemExit(f"Linux integration suite contract failed: {message}")


def main() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    release_workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
    roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    profile_matrix = PROFILE_MATRIX.read_text(encoding="utf-8")
    article_profile = ARTICLE_PROFILE.read_text(encoding="utf-8")
    distribution_bundles = DISTRIBUTION_BUNDLES.read_text(encoding="utf-8")
    release_review_pairs = RELEASE_REVIEW_PAIRS.read_text(encoding="utf-8")
    known_checks = {check.name for check in validation_run.CHECKS}

    if SUITES.get("complete") != ("*",):
        fail("complete suite must remain the wildcard full PR integration contract")
    if SUITES.get("distribution") != ("distribution-bundles",):
        fail("distribution suite must remain a first-class PR-only public bundle gate")

    for suite, checks in SUITES.items():
        if checks == ("*",):
            continue
        unknown = sorted(set(checks) - known_checks)
        if unknown:
            fail(f"suite {suite!r} references unknown checks: {', '.join(unknown)}")

    distribution_checks = [check for check in validation_run.CHECKS if check.name == "distribution-bundles"]
    if len(distribution_checks) != 1:
        fail("validation runner must register exactly one distribution-bundles check")
    if distribution_checks[0].modes != ("pr",):
        fail("distribution-bundles runner check must remain PR-only; make release-check owns the release execution")

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
        "git diff --name-only \"$BASE_SHA\" \"$HEAD_SHA\"",
        "release_candidate_marker=release/v3-release-candidate.json",
        "release-candidate-full-pr",
        "unzip",
        "git config --global --add safe.directory \"$PWD\"",
    ):
        if token not in workflow:
            fail(f"workflow is missing scoped orchestration token: {token}")

    release_required_tokens = (
        RELEASE_CANDIDATE_MARKER,
        "github.event.pull_request.head.sha",
        "SOURCE_COMMIT_SHA",
        "SOURCE_DATE_EPOCH",
        "git rev-parse HEAD",
        "make release-check",
        "Validate canonical release reference provenance",
        "artifacts/validation/release-reference-pdf.pdf",
        "artifacts/validation/release-reference-reproducibility.json",
        "CANONICAL-REFERENCE-EVIDENCE status=PASS",
        "template/main.tex",
        "independent_clean_builds",
        "identical_sha256",
        "Upload canonical reference PDF",
        "canonical-reference-${{ github.run_id }}",
        "make distribution-bundles",
        "Read release version",
        "id: release-version",
        'version=$(make --no-print-directory version)',
        "steps.release-version.outputs.version",
        "RELEASE_VERSION",
        'dist/abntexto-ufc-$RELEASE_VERSION.zip',
        "dist/abntexto-ufc-${{ steps.release-version.outputs.version }}.zip",
        "dist/abntexto-ufc-template-${{ steps.release-version.outputs.version }}.zip",
        "dist/abntexto-ufc-overleaf-${{ steps.release-version.outputs.version }}.zip",
        "tests/integration/release-review-pairs.sh",
        "Upload seven-profile review pairs",
        "artifacts/release-review-pairs/**",
        "Upload certified distribution assets",
        "dist/SHA256SUMS",
    )
    missing_release_tokens = [token for token in release_required_tokens if token not in release_workflow]
    if missing_release_tokens:
        fail(
            "Linux release check is missing candidate provenance/dynamic-artifact tokens: "
            + ", ".join(missing_release_tokens)
        )
    if "dist/abntexto-ufc-ctan-" in release_workflow:
        fail("Release workflow must not reintroduce a redundant separate CTAN archive.")

    version_capture_surfaces = {
        "release workflow": release_workflow,
        "distribution bundle gate": distribution_bundles,
        "review-pair generator": release_review_pairs,
    }
    for surface, text in version_capture_surfaces.items():
        if "$(make version)" in text:
            fail(f"{surface} contains recursion-unsafe make version capture")
        if "make --no-print-directory version" not in text:
            fail(f"{surface} must capture the canonical version without GNU Make directory chatter")

    if infer_suites(["docs/ROADMAP-V3.0.0.md"]) != ():
        fail("documentation-only changes must not trigger heavy Linux integration")
    if infer_suites([CORRECTION_STATE]) != ():
        fail("active correction machine-state updates must not trigger heavy Linux integration by themselves")
    if infer_suites(["tests/run.py"]) != ("smoke",):
        fail("orchestration-only changes must select smoke")
    if infer_suites([RELEASE_WORKFLOW_PATH]) != ("smoke",):
        fail("release-workflow-only changes must select smoke; Linux Release Check supplies the heavy R2 execution path")
    if infer_suites([DISTRIBUTION_BUILDER]) != ("distribution",):
        fail("public bundle builder changes must select the distribution suite")
    if infer_suites([DISTRIBUTION_WRAPPER]) != ("distribution",):
        fail("distribution wrapper changes must select the distribution suite")
    if infer_suites([DISTRIBUTION_GATE]) != ("distribution",):
        fail("distribution gate changes must select the distribution suite")
    if infer_suites(["tests/run.py", DISTRIBUTION_BUILDER]) != ("distribution",):
        fail("orchestration plus distribution changes must select distribution, not complete")
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
    if infer_suites([RELEASE_CANDIDATE_MARKER]) != ("complete",):
        fail("Release phase-end candidate marker must force complete Linux integration")
    if infer_suites([RELEASE_WORKFLOW_PATH, RELEASE_CANDIDATE_MARKER]) != ("complete",):
        fail("Release marker must dominate release-workflow orchestration and force complete Linux integration")
    if infer_suites(["tests/integration_suites.py", RELEASE_CANDIDATE_MARKER]) != ("complete",):
        fail("Release marker plus orchestration changes must force complete Linux integration")

    phase = roadmap.get("phase")
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
        "unknown_path_fallback=complete article_first_class=true distribution_first_class=true "
        "distribution_release_owner=make-release-check step4_registered=true step5_registered=true "
        "release_candidate_forces_complete=true release_check_pr_trigger=true "
        "release_candidate_head_checkout=true canonical_ctan_archive=true "
        "release_version_source=makefile recursion_safe_version_capture=true "
        "human_review_pairs_retained=true release_marker_full_pr_dominates_incremental=true "
        "release_assets_retained=true correction_state_docs_only=true "
        "canonical_reference_artifact=true release_workflow_orchestration_smoke=true "
        "mounted_checkout_safe_directory=true"
    )


if __name__ == "__main__":
    main()

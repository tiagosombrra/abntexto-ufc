#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from integration_suites import SUITES, infer_suites  # noqa: E402
from path_resolver import integration_file, repository_relative  # noqa: E402
import run as validation_run  # noqa: E402

WORKFLOW = ROOT / ".github" / "workflows" / "linux-integration.yml"
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "linux-release-check.yml"
INTEGRATION_SCOPE_HELPER = ROOT / "tools" / "ci" / "select-integration-scope.py"
WEB_LITE_HELPER = ROOT / "tools" / "ci" / "run-web-lite-e2e.sh"
RELEASE_REFERENCE_HELPER = ROOT / "tools" / "ci" / "validate-release-reference.py"
RELEASE_ASSET_HELPER = ROOT / "tools" / "ci" / "validate-release-assets.py"
PKGCHECK_DOWNLOAD_HELPER = ROOT / "tools" / "ci" / "validate-pkgcheck-download.py"
CTAN_CERT_HELPER = ROOT / "tools" / "ci" / "certify-ctan-package.sh"
RELEASE_SUMMARY_HELPER = ROOT / "tools" / "ci" / "render-release-summary.sh"
PROFILE_MATRIX = integration_file("profile-matrix.sh")
ARTICLE_PROFILE = integration_file("scientific-article-profile.sh")
DISTRIBUTION_BUNDLES = integration_file("distribution-bundles.sh")
RELEASE_REVIEW_PAIRS = integration_file("release-review-pairs.sh")
RELEASE_CANDIDATE_MARKER = "release/v3-release-candidate.json"
CORRECTION_STATE = "release/history/v3/v3.0.1-final-corrections.json"
RELEASE_WORKFLOW_PATH = ".github/workflows/linux-release-check.yml"
DISTRIBUTION_BUILDER = "tools/build-public-bundles.py"
DISTRIBUTION_WRAPPER = "tools/build-distribution-bundles.py"
DISTRIBUTION_GATE = repository_relative(integration_file("distribution-bundles.sh"))


def fail(message: str) -> None:
    raise SystemExit(f"Linux integration suite contract failed: {message}")


def main() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    release_workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
    integration_scope_helper = INTEGRATION_SCOPE_HELPER.read_text(encoding="utf-8")
    web_lite_helper = WEB_LITE_HELPER.read_text(encoding="utf-8")
    release_reference_helper = RELEASE_REFERENCE_HELPER.read_text(encoding="utf-8")
    release_asset_helper = RELEASE_ASSET_HELPER.read_text(encoding="utf-8")
    pkgcheck_download_helper = PKGCHECK_DOWNLOAD_HELPER.read_text(encoding="utf-8")
    ctan_cert_helper = CTAN_CERT_HELPER.read_text(encoding="utf-8")
    release_summary_helper = RELEASE_SUMMARY_HELPER.read_text(encoding="utf-8")
    profile_matrix = PROFILE_MATRIX.read_text(encoding="utf-8")
    article_profile = ARTICLE_PROFILE.read_text(encoding="utf-8")
    distribution_bundles = DISTRIBUTION_BUNDLES.read_text(encoding="utf-8")
    release_review_pairs = RELEASE_REVIEW_PAIRS.read_text(encoding="utf-8")
    known_checks = {check.name for check in validation_run.CHECKS}

    if SUITES.get("complete") != ("*",):
        fail("complete suite must remain the wildcard full PR integration contract")
    if SUITES.get("distribution") != ("distribution-bundles",):
        fail("distribution suite must remain a first-class PR-only public bundle gate")
    if SUITES.get("web-lite") != ("validator-source", "web-lite-positive"):
        fail("web-lite suite must prepare validator sources and a stable positive reference snapshot")

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
    web_positive = [check for check in validation_run.CHECKS if check.name == "web-lite-positive"]
    if len(web_positive) != 1 or web_positive[0].modes != ("pr",) or web_positive[0].depends != ("reference",):
        fail("web-lite-positive must remain one PR-only snapshot directly dependent on reference")

    required_manual_choices = ("auto", *SUITES.keys())
    missing_choices = [
        choice
        for choice in required_manual_choices
        if f"          - {choice}\n" not in workflow
    ]
    if missing_choices:
        fail("workflow_dispatch scope choices are missing: " + ", ".join(missing_choices))

    workflow_tokens = (
        "python3 tools/ci/select-integration-scope.py",
        "tests/run.py --mode pr --suite",
        "unzip",
        'git config --global --add safe.directory "$PWD"',
        "Run Web/Lite browser E2E",
        "id: web_lite_e2e",
        "success()",
        "sh tools/ci/run-web-lite-e2e.sh",
        "${{ runner.temp }}/abntexto-ufc-web-lite/web-lite-e2e.json",
        "${{ runner.temp }}/abntexto-ufc-web-lite/web-lite-chromedriver.log",
        "WEB_LITE_EVIDENCE_DIR",
        "Upload Web/Lite browser evidence",
        "steps.web_lite_e2e.outcome != 'skipped'",
        "if-no-files-found: warn",
        "web-lite-e2e-${{ github.run_id }}",
    )
    for token in workflow_tokens:
        if token not in workflow:
            fail(f"workflow is missing scoped orchestration token: {token}")

    scope_helper_tokens = (
        'DEFAULT_MARKER = "release/v3-release-candidate.json"',
        "git_changed_paths",
        "classify_suite",
        "manual-auto-fail-closed",
        "documentation-only-full-pr",
        "release-candidate-full-pr",
        '["git", "diff", "--name-only", base, head]',
        '"tests/integration_suites.py"',
    )
    for token in scope_helper_tokens:
        if token not in integration_scope_helper:
            fail(f"integration scope helper is missing contract token: {token}")

    web_helper_tokens = (
        "artifacts/validation/web-lite-positive.pdf",
        "WEB_LITE_EVIDENCE_DIR",
        'mkdir -p "$WEB_LITE_EVIDENCE_DIR"',
        "tests/integration/web-lite-e2e.py",
    )
    for token in web_helper_tokens:
        if token not in web_lite_helper:
            fail(f"Web/Lite helper is missing contract token: {token}")

    release_required_tokens = (
        RELEASE_CANDIDATE_MARKER,
        "github.event.pull_request.head.sha",
        "SOURCE_COMMIT_SHA",
        "SOURCE_DATE_EPOCH",
        "git rev-parse HEAD",
        "make release-check",
        "Validate canonical release reference provenance",
        "python3 tools/ci/validate-release-reference.py",
        "artifacts/validation/release-reference-pdf.pdf",
        "artifacts/validation/release-reference-reproducibility.json",
        "Upload canonical reference PDF",
        "canonical-reference-${{ github.run_id }}",
        "make distribution-bundles",
        "Fetch current CTAN pkgcheck archive",
        ".ci-downloads/pkgcheck.zip",
        "python3 tools/ci/validate-pkgcheck-download.py",
        "pkgcheck-download.sha256",
        "--retry-all-errors",
        "--proto '=https'",
        "Read release version",
        "id: release-version",
        'version=$(make --no-print-directory version)',
        "steps.release-version.outputs.version",
        "RELEASE_VERSION",
        "python3 tools/ci/validate-release-assets.py",
        "sh tools/ci/certify-ctan-package.sh",
        "sh tools/ci/render-release-summary.sh",
        "dist/abntexto-ufc-${{ steps.release-version.outputs.version }}.zip",
        "dist/abntexto-ufc-template-${{ steps.release-version.outputs.version }}.zip",
        "dist/abntexto-ufc-overleaf-${{ steps.release-version.outputs.version }}.zip",
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
    release_reference_tokens = (
        "CANONICAL-REFERENCE-EVIDENCE status=PASS",
        "template/main.tex",
        "independent_clean_builds",
        "identical_sha256",
    )
    for token in release_reference_tokens:
        if token not in release_reference_helper:
            fail(f"release reference helper is missing contract token: {token}")

    release_asset_tokens = (
        'PACKAGE_ID = "abntexto-ufc"',
        'f"{PACKAGE_ID}-{version}.zip"',
        'f"{PACKAGE_ID}-template-{version}.zip"',
        'f"{PACKAGE_ID}-overleaf-{version}.zip"',
        '"SHA256SUMS"',
    )
    for token in release_asset_tokens:
        if token not in release_asset_helper:
            fail(f"release asset helper is missing contract token: {token}")

    pkgcheck_download_tokens = (
        "zipfile.ZipFile",
        "Current CTAN pkgcheck archive is corrupt",
        "PKGCHECK-DOWNLOAD-EVIDENCE status=PASS",
    )
    for token in pkgcheck_download_tokens:
        if token not in pkgcheck_download_helper:
            fail(f"pkgcheck download helper is missing contract token: {token}")

    ctan_cert_tokens = (
        "cp .ci-downloads/pkgcheck.zip /tmp/pkgcheck.zip",
        'dist/abntexto-ufc-$RELEASE_VERSION.zip',
        "tests/integration/release-review-pairs.sh",
        "FINAL-CERTIFICATION-EVIDENCE surface=ctan-pkgcheck status=PASS",
    )
    for token in ctan_cert_tokens:
        if token not in ctan_cert_helper:
            fail(f"CTAN certification helper is missing contract token: {token}")

    for token in ("## Linux release validation", "### CTAN pkgcheck", "### Maintainer visual review"):
        if token not in release_summary_helper:
            fail(f"release summary helper is missing contract token: {token}")

    if "dist/abntexto-ufc-ctan-" in release_workflow:
        fail("Release workflow must not reintroduce a redundant separate CTAN archive.")
    if "--insecure" in release_workflow or "curl -k " in release_workflow:
        fail("Release workflow must never bypass TLS verification for CTAN pkgcheck acquisition.")
    if release_workflow.count("https://mirrors.ctan.org/support/pkgcheck.zip") != 1:
        fail("Current CTAN pkgcheck must be fetched exactly once, on the host runner.")

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

    if infer_suites(["docs/ARCHITECTURE.md"]) != ():
        fail("documentation-only changes must not trigger heavy Linux integration")
    if infer_suites([CORRECTION_STATE]) != ():
        fail("historical release-state maintenance must not trigger heavy Linux integration by itself")
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
    if infer_suites(["validator/app.js"]) != ("web-lite",):
        fail("Web/Lite application changes must select the web-lite suite")
    if infer_suites(["validator/normative-catalog.js"]) != ("web-lite",):
        fail("generated Web/Lite catalog changes must select the web-lite suite")
    if infer_suites(["tests/integration/web-lite-e2e.py"]) != ("web-lite",):
        fail("browser E2E changes must select the web-lite suite")
    if infer_suites(["tests/run.py", "validator/app.js"]) != ("web-lite",):
        fail("orchestration plus Web/Lite changes must retain web-lite scope")
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
    if infer_suites(
        ["tests/run.py", "tests/integration/profiles/article/scientific-article-body.sh"]
    ) != ("article",):
        fail("nested article paths must retain article scope after taxonomy moves")
    if infer_suites(["abntexto-ufc.cls"]) != ("complete",):
        fail("canonical runtime changes must force complete integration")
    if infer_suites(["tools/ci/select-integration-scope.py"]) != ("smoke",):
        fail("integration scope helper changes must select smoke")
    if infer_suites(["tools/ci/validate-release-reference.py"]) != ("smoke",):
        fail("release helper changes must select smoke; Linux Release Check owns heavy certification")
    if infer_suites(["tools/ci/run-web-lite-e2e.sh"]) != ("web-lite",):
        fail("Web/Lite helper changes must select the web-lite suite")
    if infer_suites(["unknown/technical.file"]) != ("complete",):
        fail("unknown technical paths must fail closed to complete")
    if infer_suites([RELEASE_CANDIDATE_MARKER]) != ("complete",):
        fail("Release phase-end candidate marker must force complete Linux integration")
    if infer_suites([RELEASE_WORKFLOW_PATH, RELEASE_CANDIDATE_MARKER]) != ("complete",):
        fail("Release marker must dominate release-workflow orchestration and force complete Linux integration")
    if infer_suites(["tests/integration_suites.py", RELEASE_CANDIDATE_MARKER]) != ("complete",):
        fail("Release marker plus orchestration changes must force complete Linux integration")

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
        f"manual_choices={len(required_manual_choices)} article_runtime=active "
        "full_pr_scope=true incremental_sync=false "
        "unknown_path_fallback=complete article_first_class=true distribution_first_class=true "
        "distribution_release_owner=make-release-check step4_registered=true step5_registered=true "
        "release_candidate_forces_complete=true release_check_pr_trigger=true "
        "release_candidate_head_checkout=true canonical_ctan_archive=true "
        "release_version_source=makefile recursion_safe_version_capture=true "
        "human_review_pairs_retained=true release_marker_full_pr_dominates=true "
        "release_assets_retained=true correction_state_docs_only=true "
        "canonical_reference_artifact=true release_workflow_orchestration_smoke=true "
        "web_lite_first_class=true browser_e2e_host=true web_lite_upload_non_masking=true"
    )


if __name__ == "__main__":
    main()

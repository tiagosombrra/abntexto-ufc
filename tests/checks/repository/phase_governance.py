#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from path_resolver import ROOT  # noqa: E402
HISTORICAL_STATE = ROOT / "release" / "history" / "v3" / "v3-roadmap.json"
HISTORICAL_V302 = ROOT / "release" / "history" / "v3" / "v3.0.2-release-candidate.json"
HISTORICAL_V303 = ROOT / "release" / "history" / "v3" / "v3.0.3-release-candidate.json"
HISTORICAL_V304 = ROOT / "release" / "history" / "v3" / "v3.0.4-release-candidate.json"
ACTIVE_MARKER = ROOT / "release" / "v3-release-candidate.json"
AGENTS = ROOT / "AGENTS.md"
STATUS = ROOT / "docs" / "RELEASE-STATE.md"


def fail(message: str) -> int:
    print(f"Release governance contract failed: {message}")
    return 1


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Release governance contract failed: cannot read {path}: {exc}")
    if not isinstance(value, dict):
        raise SystemExit(f"Release governance contract failed: {path} must contain an object")
    return value


def require_tokens(path: Path, tokens: tuple[str, ...]) -> str:
    if not path.is_file():
        raise SystemExit(f"Release governance contract failed: missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise SystemExit(
                f"Release governance contract failed: {path.relative_to(ROOT)} "
                f"is missing required token {token!r}"
            )
    return text


def valid_sha(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(char in "0123456789abcdef" for char in value)
    )


def validate_historical_release(
    marker: dict[str, Any],
    version: str,
    source_sha: str,
) -> int | None:
    if marker.get("lifecycle") != "historical-release-marker":
        return fail(f"historical {version} snapshot must use historical-release-marker lifecycle")
    if marker.get("target_version") != version:
        return fail(f"historical {version} snapshot must preserve target version {version}")
    if marker.get("candidate_state") != "FROZEN":
        return fail(f"historical {version} snapshot must preserve frozen state")
    if marker.get("candidate_sha") != source_sha:
        return fail(f"historical {version} snapshot source SHA changed unexpectedly")
    if marker.get("publication_authorized") is not True:
        return fail(f"historical {version} snapshot must preserve publication authorization")
    return None


def main() -> int:
    historical = load_json(HISTORICAL_STATE)
    if historical.get("status") != "HISTORICAL":
        return fail("historical v3 roadmap must remain explicitly historical")
    if historical.get("target_version") != "3.0.1":
        return fail("historical roadmap must preserve its original v3.0.1 target identity")
    if historical.get("historical") is not True:
        return fail("historical roadmap must be explicitly classified")

    archived_v302 = load_json(HISTORICAL_V302)
    result = validate_historical_release(
        archived_v302,
        "3.0.2",
        "3a0904324e23bfc65852d730f2647ce47dc65105",
    )
    if result is not None:
        return result

    archived_v303 = load_json(HISTORICAL_V303)
    result = validate_historical_release(
        archived_v303,
        "3.0.3",
        "b98270f23b1b384773c409869dfb05d71acd8638",
    )
    if result is not None:
        return result
    if archived_v303.get("publication_state") != "PUBLISHED":
        return fail("historical v3.0.3 snapshot must preserve PUBLISHED state")
    receipt_v303 = archived_v303.get("publication_receipt")
    if not isinstance(receipt_v303, dict) or receipt_v303.get("github_release_id") != 391878053:
        return fail("historical v3.0.3 snapshot must preserve GitHub Release ID 391878053")

    archived_v304 = load_json(HISTORICAL_V304)
    result = validate_historical_release(
        archived_v304,
        "3.0.4",
        "7e176fd5472925b519d469a9a756330f4851f0b3",
    )
    if result is not None:
        return result
    if archived_v304.get("publication_state") != "PUBLISHED":
        return fail("historical v3.0.4 snapshot must preserve PUBLISHED state")
    receipt_v304 = archived_v304.get("publication_receipt")
    if not isinstance(receipt_v304, dict):
        return fail("historical v3.0.4 snapshot must preserve publication receipt")
    if receipt_v304.get("github_release_id") != 392476983:
        return fail("historical v3.0.4 snapshot must preserve GitHub Release ID 392476983")
    if receipt_v304.get("annotated_tag_object_sha") != "184b00ad2eaed8a98e6b17033e7623efb3e53571":
        return fail("historical v3.0.4 snapshot must preserve annotated tag object SHA")
    if receipt_v304.get("ctan_follow_up_issue") != 356:
        return fail("historical v3.0.4 snapshot must preserve CTAN follow-up issue #356")

    marker = load_json(ACTIVE_MARKER)
    if marker.get("schema_version") != 29:
        return fail("published v3.0.5 marker must use schema version 29")
    if marker.get("lifecycle") != "published-release-marker":
        return fail("root release marker must represent published v3.0.5")
    if marker.get("release_line") != "3.0.5" or marker.get("target_version") != "3.0.5":
        return fail("active release marker must identify v3.0.5")
    if marker.get("candidate_state") != "FROZEN":
        return fail("v3.0.5 must be frozen only after new explicit ACCEPT")
    if marker.get("candidate_sha") != "30ff9b7bc777db28584fce7e96930e748ee1a661":
        return fail("frozen candidate SHA must match exact approved publication source")
    if marker.get("publication_authorized") is not True:
        return fail("accepted frozen source must explicitly authorize subsequent publication")
    if marker.get("publication_state") != "PUBLISHED":
        return fail("published v3.0.5 must explicitly record actual GitHub publication")
    if marker.get("active_development_line") is not None:
        return fail("after v3.0.5 publication there is no automatically selected next development line")
    if marker.get("tracking_issue") != 475:
        return fail("v3.0.5 source correction must track active issue #475")
    if marker.get("authority") != "docs/RELEASE-STATE.md":
        return fail("active development marker must point to docs/RELEASE-STATE.md")

    active = marker.get("active_development_candidate")
    if not isinstance(active, dict):
        return fail("active v3.0.5 marker must contain development metadata")
    if active.get("version") != "3.0.5":
        return fail("active development metadata must identify v3.0.5")
    if active.get("entry_sha") != "57b433bb2525e9776a5e86c7b26b8412b33268eb":
        return fail("source correction must start at post-merge certified #477 main")
    if active.get("tracking_issue") != 475 or active.get("source_correction_issue") != 369:
        return fail("source correction must link #475 and #369")
    if active.get("current_change") != "release-control-freeze":
        return fail("frozen release control requires release-control-freeze")
    if active.get("runtime_source_model") != "single-canonical-class":
        return fail("v3.0.5 must preserve its single canonical runtime")
    if active.get("tracking_pr") != 478:
        return fail("corrected publication source must track PR #478 exactly")
    if active.get("prior_accepted_source_sha") != "407f279a78df3824b27585d0e86d688c19cd90ee":
        return fail("original maintainer-approved source receipt changed")
    if active.get("prior_review_artifact_id") != 11415094731:
        return fail("original maintainer-approved artifact receipt changed")
    if active.get("prior_acceptance_not_transferable") is not True:
        return fail("old-source human acceptance must remain nontransferable")
    for key in ("requires_new_exact_sha_certification", "requires_new_maintainer_accept"):
        if active.get(key) is not False:
            return fail(f"fresh candidate acceptance gate remains incomplete: {key}")

    freeze = marker.get("freeze_receipt")
    if not isinstance(freeze, dict):
        return fail("missing immutable new-source freeze receipt")
    expected = {
        "source_sha": "30ff9b7bc777db28584fce7e96930e748ee1a661",
        "source_tree_sha": "4b2a64e5c318ef761d84364877000086d51f1664",
        "review_artifact_id": 11670542808,
        "review_artifact_sha256": "8aaff1d8b317034470470d4acd10af20518e1ac791b3d7e8b7ba5231817f1886",
        "distribution_artifact_id": 11670527758,
        "distribution_artifact_sha256": "ed4eb70d1b06e09c38e70b35d505e552c90f72c9d3cc982874b79f0f2020df1c",
        "maintainer_acceptance": "ACCEPT",
        "maintainer_acceptance_date": "2026-10-10",
        "maintainer_acceptance_issue": 475,
        "annotated_tag": "v3.0.5",
        "annotated_tag_state": "CREATED",
        "github_release_state": "PUBLISHED",
        "ctan_submission_state": "NOT_SUBMITTED",
        "control_plane_base_sha": "830322177ed08b64af7e6d64e7f663f55ca9b711",
    }
    for key, value in expected.items():
        if freeze.get(key) != value:
            return fail(f"freeze source/approval/publication mismatch for {key}")
    expected_checks = {
        "static_run": 38052629167,
        "linux_integration_run": 38052629234,
        "linux_release_run": 38052629238,
        "windows_portability_run": 38055168762,
        "macos_portability_run": 38055168813,
        "linux_complete": "SCOPE=complete PASS=38 FAIL=0 SKIP=0",
        "ctan_pkgcheck": "4.1.2 PASS",
    }
    if freeze.get("source_certification") != expected_checks:
        return fail("frozen source test receipts do not match full certification")
    expected_assets = {
        "abntexto-ufc-3.0.5.zip": "b57e2f4f17d5a707e93a30f5fe701f0f14606fc39c01d6f09b6e8a3781e652e8",
        "abntexto-ufc-template-3.0.5.zip": "a6433d7e698a8e89a39761a7ea5951b267cce2169844827410fdc958da39196a",
        "abntexto-ufc-overleaf-3.0.5.zip": "082255fddec80f6e6aeee17f6781d579d3c488c8571a456018aa3524eade7e3d",
    }
    expected_published_assets = {
        **expected_assets,
        "SHA256SUMS": "6fcb6ce5c8c56cee4c08c5f719280bf36e8422d81950c052db63b4f142e9df95",
    }
    if freeze.get("certified_assets") != expected_published_assets:
        return fail("published release asset SHA256 receipt changed")
    if freeze.get("annotated_tag_object_sha") != "a3648d5b1ff572f502bb25ef11dc534df7a664d4":
        return fail("annotated tag object receipt does not match GitHub")
    if freeze.get("github_release_id") != 410584912:
        return fail("freeze receipt GitHub Release ID incorrect")
    if freeze.get("github_published_at") != "2026-10-12T12:42:11Z":
        return fail("freeze receipt GitHub published time incorrect")
    expected_ids = {
        "abntexto-ufc-3.0.5.zip": 633747960,
        "abntexto-ufc-template-3.0.5.zip": 633747953,
        "abntexto-ufc-overleaf-3.0.5.zip": 633747961,
        "SHA256SUMS": 633747954,
    }
    if freeze.get("asset_ids") != expected_ids:
        return fail("freeze receipt published asset IDs do not match GitHub")
    if "issue #475" not in str(freeze.get("maintainer_acceptance_origin", "")):
        return fail("maintainer ACCEPT must carry its issue provenance")
    if marker["candidate_sha"] != freeze["source_sha"]:
        return fail("marker must bind accepted artifact's exact source")

    published = marker.get("published_release")
    if not isinstance(published, dict):
        return fail("missing v3.0.5 published GitHub receipt")
    expected_published = {
        "version": "3.0.5",
        "tag": "v3.0.5",
        "release_id": 410584912,
        "published_at": "2026-10-12T12:42:11Z",
        "source_sha": "30ff9b7bc777db28584fce7e96930e748ee1a661",
        "source_tree_sha": "4b2a64e5c318ef761d84364877000086d51f1664",
        "annotated_tag_object_sha": "a3648d5b1ff572f502bb25ef11dc534df7a664d4",
        "immutable_by_project_policy": True,
    }
    for key, value in expected_published.items():
        if published.get(key) != value:
            return fail(f"v3.0.5 published GitHub identity mismatch for {key}")
    if published.get("assets") != expected_published_assets:
        return fail("v3.0.5 published asset hashes differ from certified immutable bytes")
    if published.get("asset_ids") != expected_ids:
        return fail("v3.0.5 GitHub asset IDs differ from server receipt")
    expected_sizes = {
        "abntexto-ufc-3.0.5.zip": 247575,
        "abntexto-ufc-template-3.0.5.zip": 628536,
        "abntexto-ufc-overleaf-3.0.5.zip": 655462,
        "SHA256SUMS": 285,
    }
    if published.get("asset_sizes") != expected_sizes:
        return fail("v3.0.5 published asset sizes changed")
    certification = published.get("certification")
    if not isinstance(certification, dict):
        return fail("v3.0.5 published release certification missing")
    expected_cert = {
        "static_contract_run": 38052629167,
        "linux_integration_run": 38052629234,
        "linux_release_check_run": 38052629238,
        "windows_portability_run": 38055168762,
        "macos_portability_run": 38055168813,
        "validation": "SCOPE=complete PASS=38 FAIL=0 SKIP=0",
        "ctan_pkgcheck": "4.1.2 PASS",
        "release_review_pairs": 7,
        "maintainer_visual_acceptance": "ACCEPT",
        "maintainer_visual_acceptance_date": "2026-10-10",
        "review_artifact_id": 11670542808,
        "review_artifact_sha256": "8aaff1d8b317034470470d4acd10af20518e1ac791b3d7e8b7ba5231817f1886",
        "distribution_artifact_id": 11670527758,
        "distribution_artifact_sha256": "ed4eb70d1b06e09c38e70b35d505e552c90f72c9d3cc982874b79f0f2020df1c",
        "control_pr": 481,
        "control_merge_sha": "9e0de03d805798650bb6972f282741ff9164b301",
        "control_postmerge_static_run": 38065763832,
        "control_postmerge_linux_integration_run": 38065763807,
        "control_postmerge_linux_release_run": 38065763818,
    }
    if certification != expected_cert:
        return fail("v3.0.5 published technical and maintainer acceptance receipt mismatch")
    if published["source_sha"] != marker["candidate_sha"] or published["source_sha"] != freeze["source_sha"]:
        return fail("published and frozen source identity must be the same approved commit")
    if published["annotated_tag_object_sha"] != freeze["annotated_tag_object_sha"]:
        return fail("GitHub tag object receipt diverges from certified frozen release")
    if published["assets"] != freeze["certified_assets"]:
        return fail("GitHub publication asset bytes diverge from frozen certification")

    previous = marker.get("previous_published_release")
    if not isinstance(previous, dict):
        return fail("previous v3.0.4 publication receipt not preserved")
    historical_v304 = {
        "version": "3.0.4",
        "tag": "v3.0.4",
        "release_id": 392476983,
        "published_at": "2026-09-20T15:29:02Z",
        "source_sha": "7e176fd5472925b519d469a9a756330f4851f0b3",
        "annotated_tag_object_sha": "184b00ad2eaed8a98e6b17033e7623efb3e53571",
        "historical_state": "release/history/v3/v3.0.4-release-candidate.json",
    }
    for key, value in historical_v304.items():
        if previous.get(key) != value:
            return fail(f"published v3.0.4 historical reference drift for {key}")
    expected_v304_assets = {
        "abntexto-ufc-3.0.4.zip": "137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec",
        "abntexto-ufc-template-3.0.4.zip": "3412c0c63a85d340ec7789da509e1f6a2994efa1974207f3d79ac402a3aa159c",
        "abntexto-ufc-overleaf-3.0.4.zip": "4967ce1407e8b42b0a77ab688edbe9e759a64827e566f52d7864cb1f6118cf92",
        "SHA256SUMS": "a1aeb3f0c75449811677aaa6b11ee954cef3a253bd492433f066ba3ffea4f4d3",
    }
    if previous.get("assets") != expected_v304_assets:
        return fail("previous v3.0.4 immutable asset hashes drifted")
    earlier = marker.get("earlier_published_release")
    if not isinstance(earlier, dict) or earlier.get("version") != "3.0.3" or earlier.get("release_id") != 391878053:
        return fail("published v3.0.3 historical reference must be preserved")
    if marker.get("historical_release_state") != "release/history/v3/v3.0.4-release-candidate.json":
        return fail("v3.0.4 historical marker path changed")

    ctan = marker.get("ctan_follow_up")
    if not isinstance(ctan, dict):
        return fail("published marker must preserve CTAN follow-up contract")
    if ctan.get("state") != "PUBLISHED" or ctan.get("issue") != 356:
        return fail("CTAN v3.0.4 follow-up must record published state under issue #356")
    if ctan.get("previous_ctan_version") != "3.0.2":
        return fail("CTAN v3.0.4 submission must preserve previous CTAN version 3.0.2")
    if ctan.get("target_version") != "3.0.4":
        return fail("CTAN submission target must remain v3.0.4")
    if ctan.get("submitted_date") != "2026-09-20":
        return fail("CTAN v3.0.4 submission date changed unexpectedly")
    if ctan.get("acceptance_state") != "ACCEPTED":
        return fail("CTAN acceptance must record the confirmed external v3.0.4 publication")
    if ctan.get("published_date") != "2026-09-22":
        return fail("CTAN v3.0.4 publication date must match the official CTAN-ann update")
    if ctan.get("sha256") != expected_v304_assets["abntexto-ufc-3.0.4.zip"]:
        return fail("CTAN v3.0.4 follow-up must bind the exact historical canonical archive")

    ctan_next = marker.get("ctan_next_release")
    if not isinstance(ctan_next, dict):
        return fail("v3.0.5 CTAN must have an independent pending submission record")
    expected_ctan_next = {
        "target_version": "3.0.5",
        "state": "SUBMITTED",
        "acceptance_state": "PENDING",
        "previous_ctan_version": "3.0.4",
        "canonical_github_release_id": 410584912,
        "canonical_github_asset_id": 633747960,
        "asset": "abntexto-ufc-3.0.5.zip",
        "sha256": expected_published_assets["abntexto-ufc-3.0.5.zip"],
        "submitted_date": "2026-10-13",
        "submission_timestamp": "2026-10-13 11:14 CEST",
        "submission_timestamp_utc": "2026-10-13T09:14Z",
        "submitter": "Tiago Guimarães Sombra",
        "submission_receipt_title": "Your contribution abntexto-ufc has been uploaded",
        "submission_receipt_message": "Your submission will be processed soon. In case of questions we will come back to you via email.",
        "tracking_issue": 484,
        "path": "/macros/latex/contrib/abntexto-ufc",
        "license": "lppl1.3c",
        "submitted_filename": "abntexto-ufc-3.0.5.zip",
    }
    for key, value in expected_ctan_next.items():
        if ctan_next.get(key) != value:
            return fail(f"v3.0.5 CTAN submitted receipt mismatch: {key}")
    if "GitHub issue #484 comment 6142389236" not in str(ctan_next.get("submission_evidence", "")):
        return fail("CTAN v3.0.5 submission must cite external upload confirmation evidence")
    if ctan_next.get("acceptance_state") != "PENDING":
        return fail("CTAN v3.0.5 cannot report acceptance before external confirmation")
    if ctan_next.get("canonical_github_asset_id") != 633747960 or ctan_next.get("sha256") != expected_published_assets["abntexto-ufc-3.0.5.zip"]:
        return fail("CTAN submitted bytes must match immutable GitHub-published canonical asset")

    agents = require_tokens(
        AGENTS,
        (
            "docs/RELEASE-STATE.md",
            "v3.0.4",
            "PUBLISHED",
            "v3.0.5",
            "FROZEN",
            "issue #475",
            "issue #356",
            "2026-09-22",
            "must never be rewritten",
            "release/history/v3/",
        ),
    )
    status = require_tokens(
        STATUS,
        (
            "Latest GitHub release",
            "`v3.0.5`",
            "`PUBLISHED`",
            "410584912",
            "`v3.0.5`",
            "FROZEN",
            "issue #475",
            "issue #356",
            "2026-09-22",
        ),
    )

    if "release/history/v3/" not in agents:
        return fail("AGENTS must identify the controlled historical release-state namespace")
    if "acceptance pending" in agents.casefold() or "acceptance/publication remains pending" in agents.casefold():
        return fail("AGENTS must not report CTAN acceptance/publication as pending after external confirmation")
    if "acceptance/publication remains pending" in status.casefold():
        return fail("RELEASE-STATE.md must not report CTAN publication as pending after external confirmation")

    print(
        "RELEASE-GOVERNANCE-EVIDENCE status=PASS "
        "published_release=3.0.5 publication_state=published "
        "source_sha=30ff9b7bc777db28584fce7e96930e748ee1a661 "
        "release_id=410584912 active_development_line=none "
        "candidate_state=frozen candidate_sha=30ff9b7bc777db28584fce7e96930e748ee1a661 publication_authorized=true publication_state=published "
        "candidate_change=release-control-freeze "
        "ctan_state=published ctan_acceptance=accepted "
        "ctan_published_date=2026-09-22 ctan_issue=356 "
        "current_authority=docs/RELEASE-STATE.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

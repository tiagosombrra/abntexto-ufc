#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
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
    if marker.get("lifecycle") != "published-release-marker":
        return fail("root release marker must represent published steady state")
    if marker.get("release_line") != "3.0.4" or marker.get("target_version") != "3.0.4":
        return fail("published release marker must identify v3.0.4")
    if marker.get("candidate_state") != "FROZEN":
        return fail("published v3.0.4 source must remain frozen")
    if marker.get("candidate_sha") != "7e176fd5472925b519d469a9a756330f4851f0b3":
        return fail("published v3.0.4 marker must bind the certified source SHA")
    if marker.get("publication_authorized") is not True:
        return fail("published v3.0.4 marker must preserve publication authorization")
    if marker.get("publication_state") != "PUBLISHED":
        return fail("root release marker must record PUBLISHED state")
    if marker.get("active_development_line") is not None:
        return fail("no future development line may be implied before it is explicitly selected")
    if marker.get("tracking_issue") != 353:
        return fail("published v3.0.4 marker must preserve release issue #353")
    if marker.get("authority") != "docs/RELEASE-STATE.md":
        return fail("published release marker must point to docs/RELEASE-STATE.md")

    published = marker.get("published_release")
    if not isinstance(published, dict):
        return fail("published v3.0.4 marker must preserve publication receipt")
    if published.get("version") != "3.0.4" or published.get("tag") != "v3.0.4":
        return fail("current published release must be v3.0.4")
    if published.get("release_id") != 392476983:
        return fail("published v3.0.4 Release ID changed unexpectedly")
    if published.get("published_at") != "2026-09-20T15:29:02Z":
        return fail("published v3.0.4 timestamp changed unexpectedly")
    if published.get("source_sha") != "7e176fd5472925b519d469a9a756330f4851f0b3":
        return fail("published v3.0.4 source SHA changed unexpectedly")
    if published.get("annotated_tag_object_sha") != "184b00ad2eaed8a98e6b17033e7623efb3e53571":
        return fail("published v3.0.4 annotated tag object SHA changed unexpectedly")

    certification = published.get("certification")
    if not isinstance(certification, dict):
        return fail("published v3.0.4 receipt must preserve certification evidence")
    expected_certification = {
        "static_contract_run": 675,
        "linux_integration_run": 582,
        "linux_release_check_run": 35510145977,
        "validation": "SCOPE=complete PASS=38 FAIL=0 SKIP=0",
        "canonical_reference_sha256": "24ec1e9eab489f8d8453c6e1b79978f8d26bf7a3ce37ec96ff676d46482e1089",
        "ctan_sha256": "137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec",
        "template_sha256": "3412c0c63a85d340ec7789da509e1f6a2994efa1974207f3d79ac402a3aa159c",
        "overleaf_sha256": "4967ce1407e8b42b0a77ab688edbe9e759a64827e566f52d7864cb1f6118cf92",
        "sha256sums_sha256": "a1aeb3f0c75449811677aaa6b11ee954cef3a253bd492433f066ba3ffea4f4d3",
        "ctan_pkgcheck": "4.1.0 PASS",
        "maintainer_visual_acceptance": "PASS",
        "maintainer_visual_acceptance_date": "2026-09-20",
    }
    for key, expected in expected_certification.items():
        if certification.get(key) != expected:
            return fail(f"published v3.0.4 certification mismatch for {key}")

    expected_assets = {
        "abntexto-ufc-3.0.4.zip": "137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec",
        "abntexto-ufc-template-3.0.4.zip": "3412c0c63a85d340ec7789da509e1f6a2994efa1974207f3d79ac402a3aa159c",
        "abntexto-ufc-overleaf-3.0.4.zip": "4967ce1407e8b42b0a77ab688edbe9e759a64827e566f52d7864cb1f6118cf92",
        "SHA256SUMS": "a1aeb3f0c75449811677aaa6b11ee954cef3a253bd492433f066ba3ffea4f4d3",
    }
    if published.get("assets") != expected_assets:
        return fail("published v3.0.4 asset receipt changed unexpectedly")

    previous = marker.get("previous_published_release")
    if not isinstance(previous, dict):
        return fail("current marker must preserve previous v3.0.3 publication reference")
    if previous.get("version") != "3.0.3" or previous.get("release_id") != 391878053:
        return fail("previous published release reference must remain v3.0.3")

    ctan = marker.get("ctan_follow_up")
    if not isinstance(ctan, dict):
        return fail("published marker must preserve CTAN follow-up contract")
    if ctan.get("state") != "SUBMITTED" or ctan.get("issue") != 356:
        return fail("CTAN v3.0.4 follow-up must record submitted state under issue #356")
    if ctan.get("previous_ctan_version") != "3.0.2":
        return fail("CTAN v3.0.4 submission must preserve previous CTAN version 3.0.2")
    if ctan.get("target_version") != "3.0.4":
        return fail("CTAN submission target must remain v3.0.4")
    if ctan.get("submitted_date") != "2026-09-20":
        return fail("CTAN v3.0.4 submission date changed unexpectedly")
    if ctan.get("acceptance_state") != "PENDING":
        return fail("CTAN acceptance must remain pending until external confirmation")
    if ctan.get("sha256") != expected_assets["abntexto-ufc-3.0.4.zip"]:
        return fail("CTAN follow-up must bind the exact published canonical archive")

    agents = require_tokens(
        AGENTS,
        (
            "docs/RELEASE-STATE.md",
            "v3.0.4",
            "PUBLISHED",
            "none selected",
            "issue #356",
            "must never be rewritten",
            "release/history/v3/",
        ),
    )
    status = require_tokens(
        STATUS,
        (
            "Latest GitHub release",
            "`v3.0.4`",
            "`PUBLISHED`",
            "392476983",
            "none selected",
            "issue #356",
        ),
    )

    if "release/history/v3/" not in agents:
        return fail("AGENTS must identify the controlled historical release-state namespace")

    print(
        "RELEASE-GOVERNANCE-EVIDENCE status=PASS "
        "published_release=3.0.4 publication_state=published "
        "source_sha=7e176fd5472925b519d469a9a756330f4851f0b3 "
        "release_id=392476983 active_development_line=none "
        "ctan_state=submitted ctan_issue=356 "
        "current_authority=docs/RELEASE-STATE.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

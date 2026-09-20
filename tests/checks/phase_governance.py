#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL_STATE = ROOT / "release" / "history" / "v3" / "v3-roadmap.json"
HISTORICAL_V302 = ROOT / "release" / "history" / "v3" / "v3.0.2-release-candidate.json"
ACTIVE_MARKER = ROOT / "release" / "v3-release-candidate.json"
AGENTS = ROOT / "AGENTS.md"
STATUS = ROOT / "docs" / "RELEASE-STATE.md"


def fail(message: str) -> int:
    print(f"Development governance contract failed: {message}")
    return 1


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Development governance contract failed: cannot read {path}: {exc}")
    if not isinstance(value, dict):
        raise SystemExit(f"Development governance contract failed: {path} must contain an object")
    return value


def require_tokens(path: Path, tokens: tuple[str, ...]) -> str:
    if not path.is_file():
        raise SystemExit(f"Development governance contract failed: missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise SystemExit(
                f"Development governance contract failed: {path.relative_to(ROOT)} "
                f"is missing required token {token!r}"
            )
    return text


def valid_sha(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(char in "0123456789abcdef" for char in value)
    )


def main() -> int:
    historical = load_json(HISTORICAL_STATE)
    if historical.get("status") != "HISTORICAL":
        return fail("historical v3 roadmap must remain explicitly historical")
    if historical.get("target_version") != "3.0.1":
        return fail("historical roadmap must preserve its original v3.0.1 target identity")
    if historical.get("historical") is not True:
        return fail("historical roadmap must be explicitly classified")

    archived_v302 = load_json(HISTORICAL_V302)
    if archived_v302.get("lifecycle") != "historical-release-marker":
        return fail("v3.0.2 release snapshot must be historical")
    if archived_v302.get("target_version") != "3.0.2":
        return fail("historical v3.0.2 snapshot must preserve target version 3.0.2")
    if archived_v302.get("candidate_state") != "FROZEN":
        return fail("historical v3.0.2 snapshot must preserve frozen state")
    if not valid_sha(archived_v302.get("candidate_sha")):
        return fail("historical v3.0.2 snapshot must preserve a valid frozen candidate SHA")
    if archived_v302.get("publication_authorized") is not True:
        return fail("historical v3.0.2 snapshot must preserve publication authorization")

    marker = load_json(ACTIVE_MARKER)
    if marker.get("development_line") != "3.0.4" or marker.get("target_version") != "3.0.4":
        return fail("active release marker must identify v3.0.4")

    candidate_state = marker.get("candidate_state")
    if candidate_state not in {"NOT_FROZEN", "FROZEN"}:
        return fail("v3.0.4 candidate state must be NOT_FROZEN or FROZEN")

    expected_lifecycle = (
        "active-release-marker" if candidate_state == "FROZEN" else "active-development-marker"
    )
    if marker.get("lifecycle") != expected_lifecycle:
        return fail(f"v3.0.4 lifecycle must be {expected_lifecycle} for {candidate_state}")

    if candidate_state == "NOT_FROZEN":
        if marker.get("candidate_sha") is not None:
            return fail("NOT_FROZEN v3.0.4 development must not expose a candidate SHA")
        if marker.get("publication_authorized") is not False:
            return fail("v3.0.4 publication must remain unauthorized before freeze")
        if marker.get("publication_state") != "UNPUBLISHED":
            return fail("NOT_FROZEN v3.0.4 development must remain UNPUBLISHED")
    else:
        if marker.get("candidate_sha") != "7e176fd5472925b519d469a9a756330f4851f0b3":
            return fail("FROZEN v3.0.4 candidate must bind the certified publication source")
        if marker.get("publication_authorized") is not True:
            return fail("FROZEN v3.0.4 candidate must be publication-authorized")
        if marker.get("publication_state") != "AUTHORIZED":
            return fail("FROZEN v3.0.4 candidate must expose AUTHORIZED publication state")

        candidate_certification = marker.get("certification")
        if not isinstance(candidate_certification, dict):
            return fail("FROZEN v3.0.4 candidate must preserve certification evidence")
        expected_candidate_evidence = {
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
        for key, expected in expected_candidate_evidence.items():
            if candidate_certification.get(key) != expected:
                return fail(f"FROZEN v3.0.4 certification mismatch for {key}")

    if marker.get("tracking_issue") != 353:
        return fail("active v3.0.4 release must track issue #353")
    if marker.get("authority") != "docs/RELEASE-STATE.md":
        return fail("active release marker must point to docs/RELEASE-STATE.md")

    active = marker.get("active_development_candidate")
    if not isinstance(active, dict):
        return fail("active v3.0.4 marker must define development entry metadata")
    if active.get("version") != "3.0.4":
        return fail("active development metadata must identify v3.0.4")
    if active.get("entry_sha") != "51bb54a013dc2fd4917880960928ad9792a2a1be":
        return fail("v3.0.4 entry must preserve the certified post-v3.0.3 steady-state SHA")
    if active.get("tracking_issue") != 353:
        return fail("active release-preparation metadata must point to issue #353")

    published = marker.get("published_release")
    if not isinstance(published, dict):
        return fail("active development marker must preserve the published v3.0.3 receipt")
    if published.get("version") != "3.0.3" or published.get("tag") != "v3.0.3":
        return fail("published baseline must remain v3.0.3")
    if published.get("source_sha") != "b98270f23b1b384773c409869dfb05d71acd8638":
        return fail("published v3.0.3 source SHA changed unexpectedly")
    if published.get("release_id") != 391878053:
        return fail("published v3.0.3 release ID changed unexpectedly")

    published_certification = published.get("certification")
    if not isinstance(published_certification, dict):
        return fail("published v3.0.3 receipt must preserve certification evidence")
    if published_certification.get("linux_release_check_run") != 35279315637:
        return fail("published v3.0.3 receipt must bind Linux Release Check run 35279315637")
    if published_certification.get("validation") != "SCOPE=complete PASS=38 FAIL=0 SKIP=0":
        return fail("published v3.0.3 receipt must preserve complete validation evidence")
    if published_certification.get("maintainer_visual_acceptance") != "PASS":
        return fail("published v3.0.3 receipt must preserve maintainer visual acceptance")

    expected_state_token = "FROZEN" if candidate_state == "FROZEN" else "NOT_FROZEN"
    agents = require_tokens(
        AGENTS,
        (
            "docs/RELEASE-STATE.md",
            "v3.0.4",
            "issue #353",
            expected_state_token,
            "must never be rewritten",
            "release/history/v3/",
        ),
    )
    status = require_tokens(
        STATUS,
        (
            "Latest GitHub release",
            "`v3.0.3`",
            "`PUBLISHED`",
            "`v3.0.4`",
            expected_state_token,
        ),
    )

    if "release/history/v3/" not in agents:
        return fail("AGENTS must identify the controlled historical release-state namespace")

    print(
        "DEVELOPMENT-GOVERNANCE-EVIDENCE status=PASS "
        "published_release=3.0.3 active_candidate=3.0.4 "
        f"candidate_state={str(candidate_state).lower()} "
        f"publication_state={str(marker.get('publication_state')).lower()} "
        "tracking_issue=353 entry_sha=51bb54a013dc2fd4917880960928ad9792a2a1be "
        "current_authority=docs/RELEASE-STATE.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

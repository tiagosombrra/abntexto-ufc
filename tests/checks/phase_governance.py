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
STATUS = ROOT / "docs" / "V3.0.3-DISTRIBUTION-CORRECTION.md"


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
    if marker.get("lifecycle") != "active-release-marker":
        return fail("active release marker lifecycle is invalid")
    if marker.get("development_line") != "3.0.3" or marker.get("target_version") != "3.0.3":
        return fail("active release marker must target the v3.0.3 development line")

    candidate_state = marker.get("candidate_state")
    candidate_sha = marker.get("candidate_sha")
    publication_authorized = marker.get("publication_authorized")
    if candidate_state == "NOT_FROZEN":
        if candidate_sha is not None:
            return fail("NOT_FROZEN candidate must not expose a candidate SHA")
        if publication_authorized is not False:
            return fail("publication must remain unauthorized before freeze")
    elif candidate_state == "FROZEN":
        if not valid_sha(candidate_sha):
            return fail("FROZEN candidate must bind one lowercase 40-hex source SHA")
        if publication_authorized is not True:
            return fail("FROZEN candidate requires explicit publication authorization")
    else:
        return fail(f"unsupported v3.0.3 candidate state: {candidate_state!r}")

    if marker.get("tracking_issue") != 328:
        return fail("active release marker must point to issue #328")
    if marker.get("authority") != "docs/V3.0.3-DISTRIBUTION-CORRECTION.md":
        return fail("active release marker must point to the v3.0.3 authority document")

    baseline = marker.get("published_baseline")
    if not isinstance(baseline, dict):
        return fail("active marker must define the previous release baseline")
    if baseline.get("version") != "3.0.2" or baseline.get("immutable") is not True:
        return fail("active marker must preserve immutable v3.0.2 release baseline")
    if baseline.get("tag") != "v3.0.2":
        return fail("active marker must preserve v3.0.2 tag identity")
    if baseline.get("historical_state") != "release/history/v3/v3.0.2-release-candidate.json":
        return fail("active marker must point to the archived v3.0.2 release snapshot")

    agents = require_tokens(
        AGENTS,
        (
            "docs/V3.0.3-DISTRIBUTION-CORRECTION.md",
            "issue #328",
            "| Current development line | `v3.0.3` |",
            "v3.0.2",
            "must never be rewritten",
            "release/history/v3/v3.0.2-release-candidate.json",
        ),
    )
    status = require_tokens(
        STATUS,
        (
            "Tracking issue: #328",
            "Implementation PR: #329",
            "template_overleaf_coat_of_arms=true",
            "ctan_institutional_marks_redistributed=false",
            "v3.0.2-release-candidate.json",
        ),
    )

    expected_status_state = f"candidate state = `{candidate_state}`"
    if expected_status_state not in status:
        return fail(f"v3.0.3 authority must document active marker state {candidate_state}")

    if candidate_state == "FROZEN":
        certification = marker.get("certification")
        if not isinstance(certification, dict):
            return fail("FROZEN candidate must preserve certification evidence")
        if certification.get("linux_release_check_run") != 35279315637:
            return fail("FROZEN v3.0.3 candidate must bind Linux Release Check run 35279315637")
        if certification.get("validation") != "SCOPE=complete PASS=38 FAIL=0 SKIP=0":
            return fail("FROZEN v3.0.3 candidate must preserve complete validation evidence")
        if certification.get("maintainer_visual_acceptance") != "PASS":
            return fail("FROZEN v3.0.3 candidate requires maintainer visual acceptance")

    if "release/history/v3/" not in agents:
        return fail("AGENTS must identify the controlled historical release-state namespace")

    marker_state = str(candidate_state).lower()
    print(
        "DEVELOPMENT-GOVERNANCE-EVIDENCE status=PASS "
        "current_line=3.0.3 issue=328 "
        "v3_0_1_roadmap=historical v3_0_2_release=historical "
        f"active_marker={marker_state} candidate_sha={candidate_sha or 'none'} "
        "current_authority=v3.0.3-distribution-correction"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

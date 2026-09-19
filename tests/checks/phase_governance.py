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
    if marker.get("lifecycle") != "published-release-marker":
        return fail("root release marker must represent the published steady state")
    if marker.get("development_line") != "3.0.3" or marker.get("target_version") != "3.0.3":
        return fail("published release marker must identify v3.0.3")
    if marker.get("candidate_state") != "FROZEN":
        return fail("published release marker must preserve FROZEN candidate state")
    candidate_sha = marker.get("candidate_sha")
    if not valid_sha(candidate_sha):
        return fail("published release marker must preserve a valid frozen source SHA")
    if marker.get("publication_authorized") is not True:
        return fail("published release marker must preserve publication authorization")
    if marker.get("publication_state") != "PUBLISHED":
        return fail("published release marker must record PUBLISHED state")
    if marker.get("tracking_issue") is not None:
        return fail("steady-state publication receipt must not expose an active tracking issue")
    if marker.get("authority") != "docs/RELEASE-STATE.md":
        return fail("published release marker must point to docs/RELEASE-STATE.md")
    if marker.get("active_development_candidate") is not None:
        return fail("no runtime development candidate may be active in post-v3.0.3 steady state")

    published = marker.get("published_release")
    if not isinstance(published, dict):
        return fail("published marker must define the GitHub publication receipt")
    if published.get("version") != "3.0.3" or published.get("tag") != "v3.0.3":
        return fail("published marker must preserve v3.0.3 release identity")
    if published.get("source_sha") != candidate_sha:
        return fail("published release source SHA must equal the frozen candidate SHA")
    if published.get("release_id") != 391878053:
        return fail("published marker must preserve GitHub Release ID 391878053")

    agents = require_tokens(
        AGENTS,
        (
            "docs/RELEASE-STATE.md",
            "v3.0.3",
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
            candidate_sha,
            "Active development candidate",
            "none",
        ),
    )

    certification = marker.get("certification")
    if not isinstance(certification, dict):
        return fail("published v3.0.3 receipt must preserve certification evidence")
    if certification.get("linux_release_check_run") != 35279315637:
        return fail("published v3.0.3 receipt must bind Linux Release Check run 35279315637")
    if certification.get("validation") != "SCOPE=complete PASS=38 FAIL=0 SKIP=0":
        return fail("published v3.0.3 receipt must preserve complete validation evidence")
    if certification.get("maintainer_visual_acceptance") != "PASS":
        return fail("published v3.0.3 receipt must preserve maintainer visual acceptance")

    if "release/history/v3/" not in agents:
        return fail("AGENTS must identify the controlled historical release-state namespace")

    print(
        "DEVELOPMENT-GOVERNANCE-EVIDENCE status=PASS "
        "published_release=3.0.3 active_candidate=none "
        "v3_0_1_roadmap=historical v3_0_2_release=historical "
        f"publication_state=published candidate_sha={candidate_sha} "
        "current_authority=docs/RELEASE-STATE.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

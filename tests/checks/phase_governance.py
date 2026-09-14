#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL_STATE = ROOT / "release" / "history" / "v3" / "v3-roadmap.json"
ACTIVE_MARKER = ROOT / "release" / "v3-release-candidate.json"
AGENTS = ROOT / "AGENTS.md"
STATUS = ROOT / "docs" / "V3.0.2-REPOSITORY-HYGIENE-STATUS.md"


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


def main() -> int:
    historical = load_json(HISTORICAL_STATE)
    if historical.get("status") != "HISTORICAL":
        return fail("historical v3 roadmap must not advertise an active v3.0.1 phase")
    if historical.get("target_version") != "3.0.1":
        return fail("historical roadmap must preserve its v3.0.1 target identity")
    if historical.get("historical") is not True:
        return fail("historical roadmap must be explicitly classified")
    if historical.get("superseded_by") != "docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md":
        return fail("historical roadmap must point to current v3.0.2 authority")
    if historical.get("current_development_line") != "3.0.2":
        return fail("historical roadmap must identify the current development line")
    if historical.get("current_tracking_issue") != 313:
        return fail("historical roadmap must point to issue #313")

    marker = load_json(ACTIVE_MARKER)
    if marker.get("lifecycle") != "active-release-marker":
        return fail("active release marker lifecycle is invalid")
    if marker.get("development_line") != "3.0.2" or marker.get("target_version") != "3.0.2":
        return fail("active release marker must target the v3.0.2 development line")
    candidate_state = marker.get("candidate_state")
    candidate_sha = marker.get("candidate_sha")
    publication_authorized = marker.get("publication_authorized")
    if candidate_state == "NOT_FROZEN":
        if candidate_sha is not None:
            return fail("NOT_FROZEN candidate must not expose a candidate SHA")
        if publication_authorized is not False:
            return fail("publication must remain unauthorized before freeze")
    elif candidate_state == "FROZEN":
        if not isinstance(candidate_sha, str) or len(candidate_sha) != 40 or any(
            char not in "0123456789abcdef" for char in candidate_sha
        ):
            return fail("FROZEN candidate must bind one lowercase 40-hex source SHA")
        if publication_authorized is not True:
            return fail("FROZEN candidate requires explicit publication authorization")
    else:
        return fail(f"unsupported v3.0.2 candidate state: {candidate_state!r}")
    if marker.get("tracking_issue") != 313:
        return fail("active release marker must point to issue #313")
    baseline = marker.get("published_baseline")
    if not isinstance(baseline, dict) or baseline.get("version") != "3.0.1" or baseline.get("immutable") is not True:
        return fail("active marker must preserve immutable v3.0.1 published baseline")

    agents = require_tokens(
        AGENTS,
        (
            "docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md",
            "issue #313",
            "| Current development line | `v3.0.2` |",
            "v3.0.1",
            "must never be rewritten",
        ),
    )
    status = require_tokens(
        STATUS,
        (
            "Tracking issue: #313",
            "P5 — Documentation/release-state cleanup",
            "P7 — Full post-cleanup regression",
            "Keep v3.0.1 tag/release/submitted CTAN bytes immutable.",
            "v3.0.2 release preparation",
        ),
    )

    if "release/history/v3/" not in agents:
        return fail("AGENTS must identify the controlled historical release-state namespace")
    if "P5 — Documentation/release-state cleanup | DONE" not in status:
        return fail("current status must record completion of the historical relocation lot")

    marker_state = str(candidate_state).lower()
    print(
        "DEVELOPMENT-GOVERNANCE-EVIDENCE status=PASS "
        "current_line=3.0.2 issue=313 "
        f"v3_0_1_roadmap=historical active_marker={marker_state} "
        f"candidate_sha={candidate_sha or 'none'} "
        "current_authority=v3.0.2-status"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

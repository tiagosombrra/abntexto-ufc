#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL_STATE = ROOT / "release" / "v3-roadmap.json"
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
        return fail("release/v3-roadmap.json must no longer advertise an active v3.0.1 phase")
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

    if "release/v3-roadmap.json" in agents and "historical" not in agents.casefold():
        return fail("AGENTS must not restore the historical roadmap as current authority")
    if "P5 — Documentation/release-state cleanup | DONE" not in status:
        return fail("current status must record completion of the historical relocation lot")

    print(
        "DEVELOPMENT-GOVERNANCE-EVIDENCE status=PASS "
        "current_line=3.0.2 issue=313 "
        "v3_0_1_roadmap=historical current_authority=v3.0.2-status"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

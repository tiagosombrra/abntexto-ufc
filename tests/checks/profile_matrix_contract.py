#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "release/v3-api-migration.json"
RUNNER = ROOT / "tests/integration/profile-matrix.sh"
FIXTURE = ROOT / "tests/smoke/base-profile.tex"
PLACEHOLDER = "@UFC_TYPE@"


def fail(message: str) -> None:
    raise SystemExit(f"Profile matrix contract failed: {message}")


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    canonical = contract["setup_values"]["type"]
    if not isinstance(canonical, list) or not canonical or not all(
        isinstance(item, str) and item for item in canonical
    ):
        fail("release/v3-api-migration.json has no canonical type list")
    if len(canonical) != len(set(canonical)):
        fail("canonical type list contains duplicates")

    runner_text = RUNNER.read_text(encoding="utf-8")
    match = re.search(r'^profiles="([^"]+)"$', runner_text, flags=re.MULTILINE)
    if match is None:
        fail("profile-matrix.sh does not declare a literal profiles list")
    declared = match.group(1).split()
    if len(declared) != len(set(declared)):
        fail("profile-matrix.sh declares duplicate profiles")
    if set(declared) != set(canonical):
        fail(
            "profile-matrix.sh does not cover the canonical type set: "
            f"declared={declared} canonical={canonical}"
        )

    fixture_text = FIXTURE.read_text(encoding="utf-8")
    placeholder_count = fixture_text.count(PLACEHOLDER)
    if placeholder_count != 1:
        fail(f"base profile fixture must contain exactly one {PLACEHOLDER}; found {placeholder_count}")

    generated_sources: set[str] = set()
    assignment_pattern = re.compile(r"^[ \t]*type[ \t]*=[ \t]*([^,\n]+)[ \t]*,", re.MULTILINE)
    for profile in canonical:
        generated = fixture_text.replace(PLACEHOLDER, profile)
        if PLACEHOLDER in generated:
            fail(f"placeholder survived generation for {profile}")
        assignments = assignment_pattern.findall(generated)
        normalized = [value.strip() for value in assignments]
        if normalized != [profile]:
            fail(f"generated type assignment is not exact for {profile}: {normalized}")
        generated_sources.add(generated)

    if len(generated_sources) != len(canonical):
        fail("canonical profile substitutions do not produce distinct generated sources")

    print(
        "PROFILE-MATRIX-GENERATOR-EVIDENCE status=PASS "
        f"profiles={len(declared)} placeholder_count={placeholder_count} "
        f"distinct_sources={len(generated_sources)} canonical_values={len(canonical)}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from integration_suites import release_candidate_requires_complete  # noqa: E402

ROADMAP = ROOT / "release" / "v3-roadmap.json"
MARKER = ROOT / "release" / "v3-release-candidate.json"
LINUX_RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "linux-release-check.yml"


def fail(message: str) -> None:
    raise SystemExit(f"Release candidate contract failed: {message}")


def main() -> None:
    roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    phase = roadmap.get("phase")

    if phase != "release":
        print(f"RELEASE-CANDIDATE-EVIDENCE status=NOT-APPLICABLE phase={phase}")
        return

    if not MARKER.is_file():
        fail("Release phase requires release/v3-release-candidate.json")

    marker = json.loads(MARKER.read_text(encoding="utf-8"))
    baseline = roadmap.get("baseline", {})
    policies = roadmap.get("policies", {})

    expected = {
        "schema_version": 1,
        "release": "3.0.0",
        "phase": "Release",
        "branch": "release/v3.0.0",
        "temporary": False,
        "distribution_artifact": False,
        "candidate_sha_is_self_referential": False,
    }
    for key, value in expected.items():
        if marker.get(key) != value:
            fail(f"marker field {key!r} must equal {value!r}")

    if marker.get("base_sha") != baseline.get("release_branch_base_sha"):
        fail("marker base_sha must match the canonical Release branch base")

    if marker.get("state") not in {"transport-probe", "candidate-active", "candidate-frozen", "accepted", "released"}:
        fail(f"unsupported Release candidate state: {marker.get('state')!r}")

    if marker.get("state") in {"transport-probe", "candidate-active", "candidate-frozen"}:
        if not release_candidate_requires_complete(MARKER):
            fail("active Release candidate marker must force complete Linux integration")

    if policies.get("release_candidate_transport_must_be_non_temporary") is not True:
        fail("machine policy must require non-temporary Release candidate transport")
    if policies.get("complete_linux_required_for_phase_end_regression") is not True:
        fail("machine policy must require complete Linux for phase-end regression")
    if policies.get("workflow_success_without_required_scope_satisfies_phase_gate") is not False:
        fail("workflow success without the required scope must not satisfy the phase gate")

    release_workflow = LINUX_RELEASE_WORKFLOW.read_text(encoding="utf-8")
    for token in (
        "release/v3-release-candidate.json",
        "github.event.pull_request.head.sha || github.sha",
        "fetch-depth: 0",
        "make release-check",
    ):
        if token not in release_workflow:
            fail(f"Linux release check is missing exact-candidate transport token: {token}")

    print(
        "RELEASE-CANDIDATE-EVIDENCE status=PASS "
        f"state={marker['state']} non_temporary=true complete_linux=true "
        "release_check_exact_head=true self_referential_sha=false"
    )


if __name__ == "__main__":
    main()

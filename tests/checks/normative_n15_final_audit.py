#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests" / "checks"))

from normative_proof_state import build_proof_matrix

AUDIT = ROOT / "release" / "final-audit.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"
N13_MANIFEST = ROOT / "normativa" / "n13-negative-paths.json"
N14_CONTRACT = ROOT / "validator" / "validation-contract.json"
N12_WORKFLOW = ROOT / ".github" / "workflows" / "latex-preflight.yml"
MAKEFILE = ROOT / "Makefile"
CLASS_FILE = ROOT / "abntexto-ufc.cls"
NORMAS = ROOT / "docs" / "NORMAS.md"

EXPECTED_BASE_SHA = "0a13f4388479f63b9af2d898d3cc0410a4a57c0f"
EXPECTED_N12_BLOB = "aca746454be3ce2e650bd2f50d70b2f42d7d31e1"
EXPECTED_GUIDES = {
    "ufc-guia-trabalhos-2022",
    "ufc-guia-citacoes-2025",
    "ufc-guia-referencias-2023",
    "ufc-guia-projetos-2019",
}
EXPECTED_PROOF = {
    "PARTIAL": 113,
    "NOT_PROVEN": 51,
    "CONDITIONAL": 10,
    "MANUAL": 6,
    "NOT_APPLICABLE": 1,
}
EXPECTED_BLOCKERS = {
    "N15-F001",
    "N15-F002",
    "N15-F003",
    "N15-F004",
    "N15-F005",
    "N15-F006",
    "N15-F013",
}


def fail(message: str) -> None:
    raise SystemExit(f"N15 unrestricted audit failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def makefile_version() -> str:
    text = MAKEFILE.read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        fail("Makefile VERSION not found")
    return match.group(1)


def class_version() -> str:
    text = CLASS_FILE.read_text(encoding="utf-8")
    match = re.search(r"\\ProvidesClass\{abntexto-ufc\}\[[^\]]* v([0-9]+\.[0-9]+\.[0-9]+) ", text)
    if not match:
        fail("abntexto-ufc.cls version not found")
    return match.group(1)


def finding(audit: dict, finding_id: str) -> dict:
    matches = [item for item in audit["findings"] if item.get("id") == finding_id]
    if len(matches) != 1:
        fail(f"expected exactly one finding {finding_id}")
    return matches[0]


def main() -> None:
    audit = load_json(AUDIT)
    if audit.get("schema_version") != 1:
        fail("unsupported final-audit schema_version")
    if audit.get("phase") != "N15-A":
        fail("phase must be N15-A")
    if audit.get("overall_n15_status") != "ACTIVE":
        fail("overall N15 must remain ACTIVE during N15-A")
    if audit.get("audit_status") != "CLOSURE_CANDIDATE":
        fail("N15-A audit must be a closure candidate before exact-head validation")
    if audit.get("audited_base_sha") != EXPECTED_BASE_SHA:
        fail("audited base SHA drifted")

    boundary = audit.get("authority_boundary", {})
    forbidden_true = (
        "this_file_is_normative",
        "normative_contract_changed",
        "locator_policy_changed",
        "oracle_tolerances_changed",
        "proof_state_changed",
        "n12_workflow_changed",
        "release_version_changed",
        "physical_branch_cleanup_performed",
    )
    for key in forbidden_true:
        if boundary.get(key) is not False:
            fail(f"authority boundary {key} must remain false")
    if boundary.get("article_scope_decision_recorded_only") is not True:
        fail("article scope must be recorded as a decision only during N15-A")

    expected_done = [f"N{index}" for index in range(15)]
    if audit.get("frozen_baseline", {}).get("roadmap_done_phases") != expected_done:
        fail("N0-N14 closed-phase ledger drifted")

    baseline = audit["frozen_baseline"]
    if baseline.get("atomic_rules") != 181 or baseline.get("normative_rules") != 170:
        fail("atomic/normative rule counts drifted")
    if baseline.get("locator_coverage") != "170/170":
        fail("locator coverage drifted")
    if baseline.get("explicit_gaps") != "46/46":
        fail("explicit-gap closure drifted")
    if baseline.get("n12_workflow_blob_sha") != EXPECTED_N12_BLOB:
        fail("ledger N12 blob does not match frozen SHA")
    if git_blob_sha1(N12_WORKFLOW) != EXPECTED_N12_BLOB:
        fail("frozen N12 workflow file changed")

    n13 = load_json(N13_MANIFEST)
    if n13.get("status") != "DONE":
        fail("N13 is not DONE")
    n14 = load_json(N14_CONTRACT)
    if n14.get("status") != "DONE":
        fail("N14 is not DONE")

    proof = build_proof_matrix()
    proof_counts = proof.get("proof_status_counts", {})
    for status, count in EXPECTED_PROOF.items():
        if proof_counts.get(status) != count:
            fail(f"proof-state {status} drifted: {proof_counts.get(status)} != {count}")
    if proof_counts.get("PROVEN", 0) != 0:
        fail("unsafe PROVEN promotion detected")
    if sum(proof_counts.values()) != 181:
        fail("proof-state rule count is not 181")

    dimensions = audit.get("audit_dimensions", [])
    if len(dimensions) != 13 or len(set(dimensions)) != 13:
        fail("audit dimension inventory must contain 13 unique dimensions")

    findings = audit.get("findings", [])
    if len(findings) != 13:
        fail(f"expected 13 audit findings, got {len(findings)}")
    ids = [item.get("id") for item in findings]
    if len(set(ids)) != len(ids):
        fail("duplicate finding id")
    if set(ids) != {f"N15-F{index:03d}" for index in range(1, 14)}:
        fail("finding inventory must contain N15-F001 through N15-F013")
    blockers = [item for item in findings if item.get("blocks_release") is True]
    if len(blockers) != 7:
        fail(f"expected seven release blockers, got {len(blockers)}")
    if {item["id"] for item in blockers} != EXPECTED_BLOCKERS:
        fail("release-blocker identity drifted")

    passes = audit.get("passes", [])
    if len(passes) != 6 or any(item.get("result") != "PASS" for item in passes):
        fail("expected six explicit PASS observations")

    source_audit = load_json(SOURCE_AUDIT)
    if source_audit.get("scope") != "abntexto-ufc-v2.1.0-current-sources":
        fail("N15-F003 no longer matches the observed source-audit scope")
    source_ids = {item.get("id") for item in source_audit.get("sources", [])}
    active_guides = {item for item in source_ids if isinstance(item, str) and item.startswith("ufc-guia-")}
    if active_guides != EXPECTED_GUIDES:
        fail(f"N15-F001 guide observation drifted: {sorted(active_guides)}")
    if any("artigo" in item for item in active_guides):
        fail("article source inclusion belongs to N15-B1, not the N15-A audit branch")

    if makefile_version() != "2.1.0" or class_version() != "2.1.0":
        fail("N15-F006 expects release surfaces to remain at 2.1.0 during N15-A")
    if "V2.1.0" not in NORMAS.read_text(encoding="utf-8"):
        fail("N15-F004 expects stale V2.1.0 release-state wording to remain observable in N15-A")

    if finding(audit, "N15-F001").get("severity") != "high":
        fail("missing article source must remain a high-severity N15-A finding")
    if finding(audit, "N15-F002").get("severity") != "high":
        fail("graduate-program authority classification must remain high-severity")
    if finding(audit, "N15-F005").get("status") != "FINDING":
        fail("issue #18 must remain an explicit N15-A finding")
    article = finding(audit, "N15-F013")
    if article.get("status") != "FINDING" or article.get("blocks_release") is not True:
        fail("article profile implementation must remain a release-blocking N15-A finding")
    if finding(audit, "N15-F008").get("status") != "DEFERRED_CLEANUP":
        fail("bulk branch cleanup must remain deferred")
    if finding(audit, "N15-F012").get("status") != "REVIEW":
        fail("planning branch must remain review-required")

    plan = audit.get("n15_plan", {})
    for phase in ("N15-B1", "N15-B2", "N15-B3", "N15-C", "N15-D"):
        if not plan.get(phase):
            fail(f"expanded N15 plan is missing {phase}")

    exit_criteria = audit.get("exit_criteria", {})
    if exit_criteria.get("dimensions_recorded") != 13:
        fail("exit criteria dimension count drifted")
    if exit_criteria.get("release_blocking_findings_identified") != 7:
        fail("exit criteria blocker count drifted")
    if exit_criteria.get("cleanup_is_deferred") is not True:
        fail("cleanup must remain deferred")
    if exit_criteria.get("closed_phases_reopened") is not False:
        fail("N15-A must not reopen closed phases")
    if exit_criteria.get("article_profile_deliberately_in_scope") is not True:
        fail("article profile must be deliberately in scope before N15-A closes")
    if exit_criteria.get("n15a_ready_to_close") is not True:
        fail("N15-A closure candidate is not marked ready")

    print(
        "N15-EVIDENCE unrestricted-audit "
        "status=PASS dimensions=13 findings=13 release_blockers=7 passes=6 "
        "cleanup_deferred=true article_profile_in_scope=true phase=N15-A "
        "phase_status=CLOSURE_CANDIDATE normative_contract_changed=false "
        "proof_state_changed=false version_promoted=false"
    )
    print(
        "N15-EVIDENCE release-readiness "
        "status=BLOCKED blockers=7 current_version=2.1.0 target_version=2.2.0 "
        "source_registry_complete=false article_profile_implemented=false "
        "reference_pdf_reproducibility=UNRESOLVED physical_cleanup_deferred=true"
    )


if __name__ == "__main__":
    main()

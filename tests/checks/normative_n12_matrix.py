#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "normativa" / "n12-matrix-reconciliation.json"


def fail(message: str) -> None:
    raise SystemExit(f"N12 matrix certification failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode()
    return hashlib.sha1(header + payload).hexdigest()


def require_tokens(path: Path, tokens: list[str]) -> str:
    if not path.is_file():
        fail(f"required file missing: {path}")
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        fail(f"{path}: required tokens missing: {missing}")
    return text


def forbid_tokens(path: Path, tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    present = [token for token in tokens if token in text]
    if present:
        fail(f"{path}: cross-axis coupling detected: {present}")


def main() -> None:
    manifest = load_json(MANIFEST)
    if manifest.get("schema_version") != 1 or manifest.get("phase") != "N12":
        fail("invalid manifest schema/phase")
    if manifest.get("scope") != "profile-engine-font-certification":
        fail("unexpected N12 scope")
    if manifest.get("coverage_model") != "factorized-orthogonal-axes":
        fail("N12 must use the factorized orthogonal-axis model")

    dimensions = manifest.get("dimensions", {})
    profiles = dimensions.get("profiles", [])
    engines = dimensions.get("engines", [])
    families = dimensions.get("font_families", [])
    expected_profiles = [
        "tccgraduacao",
        "tccespecializacao",
        "dissertacao",
        "tese",
        "projeto",
        "projetoanonimizado",
    ]
    if profiles != expected_profiles:
        fail(f"profile axis drifted: {profiles}")
    if engines != ["pdflatex", "lualatex"]:
        fail(f"engine axis drifted: {engines}")
    if families != ["times", "arial"]:
        fail(f"font-family axis drifted: {families}")

    profile_engine = list(product(profiles, engines))
    portable_font_engine = list(product(families, engines))
    literal_windows_font_engine = list(product(families, engines))
    counts = manifest.get("expected_cells", {})
    if counts.get("profile_engine") != len(profile_engine) or len(profile_engine) != 12:
        fail("profile × engine cell count must be 12")
    if counts.get("portable_font_engine") != len(portable_font_engine) or len(portable_font_engine) != 4:
        fail("portable font × engine cell count must be 4")
    if counts.get("literal_windows_font_engine") != len(literal_windows_font_engine) or len(literal_windows_font_engine) != 4:
        fail("literal Windows font × engine cell count must be 4")
    total = len(profile_engine) + len(portable_font_engine) + len(literal_windows_font_engine)
    if counts.get("total_certification_cells") != total or total != 20:
        fail(f"factorized certification total must be 20, found {total}")

    certified = manifest.get("certified_git_blobs", {})
    if not isinstance(certified, dict) or len(certified) < 10:
        fail("certified implementation/gate blob map is incomplete")
    for relative, expected_sha in certified.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"certified blob missing: {relative}")
        actual = git_blob_sha1(path)
        if actual != expected_sha:
            fail(f"certified blob drifted: {relative}: expected {expected_sha}, got {actual}")

    profile_script = ROOT / manifest["profile_engine_evidence"]["script"]
    profile_pdfa = ROOT / manifest["profile_engine_evidence"]["pdfa_script"]
    profile_fixture = ROOT / manifest["profile_engine_evidence"]["fixture"]
    require_tokens(profile_script, [
        'profiles="tccgraduacao tccespecializacao dissertacao tese projeto projetoanonimizado"',
        "for engine in pdflatex lualatex",
        "sh tests/v2-font-embedding-check.sh",
        "pdfaid:part",
        "pdfaid:conformance",
    ])
    require_tokens(profile_pdfa, [
        'profiles="tccgraduacao tccespecializacao dissertacao tese projeto projetoanonimizado"',
        "for engine in pdflatex lualatex",
        "sh tests/v2-pdfa-check.sh",
    ])
    fixture_text = require_tokens(profile_fixture, ["tipo = @UFC_TYPE@"])
    if "fonte =" in fixture_text or "fonte=" in fixture_text:
        fail("profile matrix fixture must not couple the profile axis to a font-family choice")

    font_script = ROOT / manifest["portable_font_engine_evidence"]["script"]
    require_tokens(font_script, [
        "for engine in pdflatex lualatex",
        "for family in times arial",
        "for slot in rm sf tt",
        'render_fixture "$family" sim rm',
        "strict_job=",
        "sh tests/v2-font-embedding-check.sh",
    ])

    windows_build = ROOT / manifest["literal_windows_font_engine_evidence"]["build_script"]
    windows_cert = ROOT / manifest["literal_windows_font_engine_evidence"]["certification_script"]
    require_tokens(windows_build, [
        "compile_class_case pdflatex times",
        "compile_class_case pdflatex arial",
        "compile_class_case lualatex times",
        "compile_class_case lualatex arial",
        "assert_no_text_fallback",
        "assert_text_extraction",
    ])
    require_tokens(windows_cert, [
        "for engine in pdflatex lualatex",
        "for family in times arial",
        "TimesNewRomanPSMT",
        "ArialMT",
        "assert_no_text_fallback",
        "assert_text_extraction",
        "sh tests/v2-font-embedding-check.sh",
        "sh tests/v2-pdfa-check.sh",
    ])

    orth = manifest.get("orthogonality", {})
    core = ROOT / orth["profile_key_file"]
    fonts = ROOT / orth["font_key_file"]
    require_tokens(core, [f"tipo / {profile}" for profile in profiles])
    require_tokens(fonts, ["fonte / times", "fonte / arial", "AtEndPreamble", "ufc_font_apply"])
    forbid_tokens(core, ["g_ufc_font_family_tl", "ufc_font_apply"])
    forbid_tokens(fonts, ["g_ufc_document_type_tl", "ufcIfProjectTF"])
    for relative in orth.get("profile_render_files", []):
        forbid_tokens(ROOT / relative, ["g_ufc_font_family_tl", "ufc_font_apply", "fonte / times", "fonte / arial"])

    stable = manifest.get("stable_main_evidence", {})
    workflow = ROOT / stable["workflow"]
    required_jobs = stable.get("required_job_names", [])
    workflow_text = require_tokens(workflow, required_jobs)
    for token in (
        "workflow_dispatch:",
        "V2 Windows literal font build",
        "V2 Windows literal font certification",
        "GATE_T_REQUIRED",
        "WINDOWS_BUILD",
        "WINDOWS_PDFA",
    ):
        if token not in workflow_text:
            fail(f"workflow lost N12 stable-main gate token: {token}")

    if stable.get("source_sha") != "34a723c33d6779fb8a4476c7e4d94f610e19e129":
        fail("stable-main evidence SHA drifted")
    if stable.get("workflow_run_id") != 33032198400 or stable.get("workflow_run_number") != 875:
        fail("stable-main workflow receipt drifted")
    if stable.get("event") != "workflow_dispatch":
        fail("N12 stable-main evidence must come from workflow_dispatch so Windows gates are required")
    if stable.get("observed_conclusion") != "SUCCESS":
        fail("stable-main N12 workflow receipt is not certified SUCCESS")

    observed_jobs = stable.get("observed_jobs", [])
    if sorted(observed_jobs) != sorted(required_jobs):
        fail("stable-main SUCCESS receipt does not cover every required N12 job")
    if len(required_jobs) != 9 or len(set(required_jobs)) != 9:
        fail("stable-main required job set must contain exactly nine unique jobs")

    receipts = stable.get("job_receipts", {})
    if not isinstance(receipts, dict) or set(receipts) != set(required_jobs):
        fail("stable-main job receipt keys do not match the required N12 jobs")
    receipt_ids: set[int] = set()
    for job_name in required_jobs:
        receipt = receipts.get(job_name)
        if not isinstance(receipt, dict):
            fail(f"invalid stable-main job receipt: {job_name}")
        job_id = receipt.get("job_id")
        conclusion = receipt.get("conclusion")
        if not isinstance(job_id, int) or job_id <= 0:
            fail(f"invalid stable-main job id for {job_name}: {job_id!r}")
        if conclusion != "success":
            fail(f"stable-main job receipt is not successful: {job_name}={conclusion!r}")
        if job_id in receipt_ids:
            fail(f"stable-main job receipt reuses job id {job_id}")
        receipt_ids.add(job_id)

    host = manifest.get("scope_checker_host", {})
    if host.get("check_id") != "normative-complement":
        fail("N12 scope checker must be hosted by normative-complement")
    host_script = ROOT / host.get("script", "")
    checker_path = host.get("checker")
    if not isinstance(checker_path, str) or not checker_path:
        fail("N12 scope checker path is missing")
    host_text = require_tokens(host_script, [checker_path])
    if "python3 tests/checks/normative_n12_matrix.py" not in host_text:
        fail("N12 scope checker is not directly invoked by normative-complement")

    supplemental = manifest.get("supplemental_environment", {})
    if supplemental.get("overleaf_proxy_is_core_matrix_cell") is not False:
        fail("Overleaf proxy must remain supplemental, not a core N12 matrix cell")

    policy = manifest.get("closure_policy", {})
    expected_policy = {
        "does_not_reopen_normative_predicates": True,
        "proof_state_changed": False,
        "literal_windows_identity_requires_windows_path": True,
        "full_24_cell_profile_font_cross_product_required": False,
        "factorization_requires_orthogonality_check": True,
    }
    for key, expected in expected_policy.items():
        if policy.get(key) is not expected:
            fail(f"closure policy drifted: {key}={policy.get(key)!r}")

    print(
        "N12-EVIDENCE matrix-reconciliation "
        f"profiles={len(profiles)} engines={len(engines)} families={len(families)} "
        f"profile_engine_cells={len(profile_engine)} "
        f"portable_font_engine_cells={len(portable_font_engine)} "
        f"literal_windows_font_engine_cells={len(literal_windows_font_engine)} "
        f"total_certification_cells={total}"
    )
    print("N12-EVIDENCE orthogonality status=PASS factorized_cross_product=true")
    print(
        "N12-EVIDENCE stable-main-receipt "
        f"sha={stable['source_sha']} run_id={stable['workflow_run_id']} "
        f"run_number={stable['workflow_run_number']} conclusion={stable['observed_conclusion']} "
        f"jobs={len(receipts)}"
    )
    print("N12-EVIDENCE scope-checker-host check_id=normative-complement status=PASS")
    print(
        "N12-EVIDENCE authority-boundary "
        "compatibility-certification=true normative_predicates_reopened=false proof_state_changed=false"
    )


if __name__ == "__main__":
    main()

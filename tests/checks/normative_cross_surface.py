#!/usr/bin/env python3
from __future__ import annotations

import json
import runpy
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "validator" / "validation-contract.json"
VECTORS = ROOT / "validator" / "validation-vectors.json"
WEB = ROOT / "validator" / "app.js"
CLI = ROOT / "tools" / "validate-ufc-pdf.py"

sys.path.insert(0, str(ROOT / "tools"))


def fail(message: str) -> None:
    raise SystemExit(f"N14 cross-surface validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def source_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix) and line.endswith(";"):
            return line
    fail(f"Web/Lite source line missing: {prefix}")
    raise AssertionError("unreachable")


def run_web_vectors(web: str, vectors: dict[str, Any]) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        fail("Node.js is required for Web/Lite contract vectors")

    status_line = source_line(web, 'const PASS=')
    verdict_line = source_line(web, "const verdict=")
    aliases_line = source_line(web, "const CHECK_ID_ALIASES=")
    report_line = source_line(web, "const reportCheck=")

    script = f'''
import fs from "node:fs";
{status_line}
{verdict_line}
{aliases_line}
{report_line}
const input=JSON.parse(fs.readFileSync(0,"utf8"));
const output={{
  verdicts:input.verdict_vectors.map(v=>({{id:v.id,verdict:verdict(v.checks)}})),
  aliases:input.alias_vectors.map(v=>({{canonical_id:v.canonical_id,web_id:reportCheck({{
    id:v.web_input_id,category:"",rule:"",source:"",status:PASS,evidence:"",correction:"",
    mandatory:true,level:"automático",normativeRule:"",locator:"",normativity:""
  }}).id}})),
  report:reportCheck(input.report_vector.web_input)
}};
process.stdout.write(JSON.stringify(output));
'''
    completed = subprocess.run(
        [node, "--input-type=module", "-e", script],
        cwd=ROOT,
        input=json.dumps(vectors, ensure_ascii=False),
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"Web/Lite vector execution failed: {completed.stdout}{completed.stderr}")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"Web/Lite vector output is not JSON: {exc}")
    if not isinstance(result, dict):
        fail("Web/Lite vector output must be an object")
    return result


def load_cli() -> dict[str, Any]:
    try:
        namespace = runpy.run_path(str(CLI))
    except Exception as exc:
        fail(f"cannot load CLI/Deep implementation: {exc}")
    if "Check" not in namespace or "verdict" not in namespace:
        fail("CLI/Deep Check/verdict implementation missing")
    return namespace


def main() -> None:
    contract = load_json(CONTRACT)
    vectors = load_json(VECTORS)
    if contract.get("phase") != "N14" or contract.get("status") != "DONE":
        fail("contract must represent closed N14")
    if vectors.get("schema_version") != 1 or vectors.get("phase") != "N14":
        fail("invalid vector schema/phase")

    expected = vectors.get("expected")
    verdict_vectors = vectors.get("verdict_vectors")
    alias_vectors = vectors.get("alias_vectors")
    report_vector = vectors.get("report_vector")
    if not isinstance(expected, dict):
        fail("expected vector summary must be an object")
    if not isinstance(verdict_vectors, list) or not verdict_vectors:
        fail("verdict_vectors must be a non-empty list")
    if not isinstance(alias_vectors, list) or not alias_vectors:
        fail("alias_vectors must be a non-empty list")
    if not isinstance(report_vector, dict):
        fail("report_vector must be an object")

    web_source = WEB.read_text(encoding="utf-8")
    web_result = run_web_vectors(web_source, vectors)
    cli = load_cli()
    Check = cli["Check"]
    cli_verdict = cli["verdict"]

    web_verdicts = {item["id"]: item["verdict"] for item in web_result.get("verdicts", [])}
    if len(web_verdicts) != len(verdict_vectors):
        fail("Web/Lite verdict vector count mismatch")

    for vector in verdict_vectors:
        vector_id = vector.get("id")
        checks = vector.get("checks")
        expected_verdict = vector.get("expected_verdict")
        if not isinstance(vector_id, str) or not isinstance(checks, list) or not isinstance(expected_verdict, str):
            fail("invalid verdict vector")
        cli_checks = [
            Check(
                id=str(check.get("id", "synthetic")),
                category="Synthetic",
                rule="Synthetic",
                source="N14",
                status=str(check.get("status", "")),
                evidence="synthetic",
                mandatory=bool(check.get("mandatory", True)),
            )
            for check in checks
        ]
        cli_value = cli_verdict(cli_checks)
        web_value = web_verdicts.get(vector_id)
        if web_value != expected_verdict:
            fail(f"{vector_id}: Web/Lite verdict={web_value!r} expected={expected_verdict!r}")
        if cli_value != expected_verdict:
            fail(f"{vector_id}: CLI/Deep verdict={cli_value!r} expected={expected_verdict!r}")
        if web_value != cli_value:
            fail(f"{vector_id}: cross-surface verdict drift")

    web_aliases = {item["canonical_id"]: item["web_id"] for item in web_result.get("aliases", [])}
    for vector in alias_vectors:
        canonical_id = vector.get("canonical_id")
        cli_id = vector.get("cli_id")
        if web_aliases.get(canonical_id) != canonical_id:
            fail(f"{canonical_id}: Web/Lite boundary did not emit canonical ID")
        if cli_id != canonical_id:
            fail(f"{canonical_id}: CLI/Deep ID is not canonical")

    target = contract.get("target_report_schema")
    if not isinstance(target, dict):
        fail("target_report_schema must be an object")
    required_fields = target.get("required_check_fields")
    if not isinstance(required_fields, list):
        fail("required_check_fields must be a list")

    web_report = web_result.get("report")
    cli_input = report_vector.get("cli_input")
    if not isinstance(web_report, dict) or not isinstance(cli_input, dict):
        fail("invalid synthetic report vector")
    try:
        cli_report = asdict(Check(**cli_input))
    except TypeError as exc:
        fail(f"CLI/Deep report vector cannot construct Check: {exc}")
    if list(web_report) != required_fields:
        fail(f"Web/Lite check schema drift: {list(web_report)}")
    if list(cli_report) != required_fields:
        fail(f"CLI/Deep check schema drift: {list(cli_report)}")
    if web_report != cli_report:
        fail("synthetic canonical check differs across surfaces")
    if web_report.get("id") != report_vector.get("expected_id"):
        fail("synthetic report vector did not emit expected canonical ID")

    inventory = contract.get("check_inventory")
    if not isinstance(inventory, list):
        fail("check_inventory must be a list")
    shared = [
        item
        for item in inventory
        if isinstance(item, dict) and item.get("web_id") is not None and item.get("cli_id") is not None
    ]
    for item in shared:
        canonical_id = item.get("canonical_id")
        if item.get("web_id") != canonical_id or item.get("cli_id") != canonical_id:
            fail(f"{canonical_id}: unresolved shared check identity")

    deep_ids = expected.get("deep_boundary_ids")
    if not isinstance(deep_ids, list):
        fail("deep_boundary_ids must be a list")
    deep = {
        item.get("canonical_id"): (item.get("web_mode"), item.get("cli_mode"))
        for item in inventory
        if isinstance(item, dict) and item.get("canonical_id") in deep_ids
    }
    expected_deep = {check_id: ("review-only", "automatic-deep") for check_id in deep_ids}
    if deep != expected_deep:
        fail(f"deep capability boundary drift: {deep}")

    policy = contract.get("policy")
    adoption = contract.get("adoption")
    closure = contract.get("closure")
    baseline = contract.get("baseline")
    if not all(isinstance(value, dict) for value in (policy, adoption, closure, baseline)):
        fail("contract policy/adoption/closure/baseline must be objects")

    observed = {
        "verdict_vector_count": len(verdict_vectors),
        "shared_check_count": len(shared),
        "canonical_check_count": len(inventory),
        "baseline_alias_count": baseline.get("alias_count"),
        "emitted_alias_count": adoption.get("emitted_alias_count"),
        "schema_drift_count": closure.get("schema_drift_count"),
        "deep_boundary_count": len(deep),
        "deep_boundary_ids": sorted(deep),
        "measurement_backend_equivalence_required": policy.get("measurement_backend_equivalence_required"),
        "normative_contract_changed": policy.get("normative_contract_changed"),
        "locator_policy_changed": policy.get("locator_policy_changed"),
        "oracle_tolerances_changed": policy.get("oracle_tolerances_changed"),
        "proof_state_changed": policy.get("proof_state_changed"),
    }
    normalized_expected = dict(expected)
    normalized_expected["deep_boundary_ids"] = sorted(normalized_expected.get("deep_boundary_ids", []))
    if observed != normalized_expected:
        fail(f"vector summary drift: observed={observed} expected={normalized_expected}")

    exit_criteria = contract.get("exit_criteria")
    if not isinstance(exit_criteria, list) or len(exit_criteria) != 6:
        fail("N14 exit criteria must remain six explicit conditions")
    if closure.get("exit_criteria_passed") != 6 or closure.get("exit_criteria_total") != 6:
        fail("N14 closure must record six of six exit criteria")

    print(
        "N14-EVIDENCE cross-surface-vectors "
        f"status=PASS verdict_vectors={len(verdict_vectors)} shared_checks={len(shared)} "
        f"canonical_checks={len(inventory)} baseline_aliases={baseline.get('alias_count')} "
        f"emitted_aliases={adoption.get('emitted_alias_count')} schema_drift={closure.get('schema_drift_count')} "
        f"deep_boundaries={len(deep)} backend_equivalence_required=false proof_state_changed=false"
    )
    print(
        "N14-EVIDENCE n14-closure "
        "status=PASS exit_criteria=6/6 phase_status=DONE "
        "normative_contract_changed=false locator_policy_changed=false "
        "oracle_tolerances_changed=false proof_state_changed=false"
    )


if __name__ == "__main__":
    main()

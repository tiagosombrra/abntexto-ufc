#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "standards" / "negative-paths.json"
EXPECTED_CASE_IDS = (
    "page-margins-right",
    "body-font-size",
    "short-direct-citation-quotes",
    "ibge-table-open-sides",
    "project-required-resources",
)
EXPECTED_MECHANISMS = {
    "final-pdf-geometry": "represented",
    "text-typography-extraction": "represented",
    "citation-quotation-presentation": "represented",
    "vector-rule-geometry": "represented",
    "configuration-strict-rejection": "represented",
    "semantic-structural-observers": "represented",
    "pdf-archival-validation": "represented",
}
EXPECTED_POLICY = {
    "positive_baseline_required": True,
    "compile_failure_counts_as_rejection": False,
    "target_rejection_must_be_nonzero": True,
    "failed_rule_evidence_required": True,
    "mutations_are_temporary": True,
    "normative_contract_changed": False,
    "locator_policy_changed": False,
    "validator_tolerances_changed": False,
    "proof_state_changed": False,
}


class CaseFailure(RuntimeError):
    pass


def fail(message: str) -> None:
    raise SystemExit(f"Negative-path validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    if manifest.get("schema_version") != 2:
        fail("unsupported manifest schema")
    if manifest.get("policy") != EXPECTED_POLICY:
        fail("negative-path policy drift")

    inventory = manifest.get("mechanism_inventory")
    if not isinstance(inventory, list):
        fail("mechanism_inventory must be a list")
    observed_mechanisms: dict[str, str] = {}
    represented: dict[str, set[str]] = {}
    for item in inventory:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            fail("invalid mechanism inventory item")
        mechanism_id = item["id"]
        if mechanism_id in observed_mechanisms:
            fail(f"duplicate mechanism inventory id: {mechanism_id}")
        observed_mechanisms[mechanism_id] = str(item.get("state"))
        if item.get("state") == "represented":
            represented[mechanism_id] = set(item.get("case_ids", []))
    if observed_mechanisms != EXPECTED_MECHANISMS:
        fail(f"mechanism inventory drift: {observed_mechanisms}")

    cases = manifest.get("cases")
    if not isinstance(cases, list):
        fail("cases must be a list")
    case_ids = [item.get("id") for item in cases if isinstance(item, dict)]
    if tuple(case_ids) != EXPECTED_CASE_IDS:
        fail(f"negative case scope drift: {case_ids}")

    for case in cases:
        if not isinstance(case, dict):
            fail("each negative case must be an object")
        case_id = case.get("id")
        family = case.get("family")
        if family not in represented or case_id not in represented[family]:
            fail(f"case {case_id} is not bound to represented family {family}")
        fixture = ROOT / str(case.get("fixture", ""))
        if not fixture.is_file():
            fail(f"fixture not found for {case_id}: {fixture}")
        for field in ("positive_gate", "validator"):
            command = case.get(field)
            if not isinstance(command, list) or not command or not all(isinstance(value, str) for value in command):
                fail(f"case {case_id}: {field} must be a non-empty string list")
        mutation = case.get("mutation")
        if not isinstance(mutation, dict) or mutation.get("kind") not in {"insert_before", "replace_once"}:
            fail(f"case {case_id}: invalid mutation")
        if not isinstance(mutation.get("anchor"), str) or not mutation["anchor"]:
            fail(f"case {case_id}: mutation anchor is required")
        if not isinstance(mutation.get("content"), str):
            fail(f"case {case_id}: mutation content is required")
        compile_spec = case.get("compile")
        if not isinstance(compile_spec, dict):
            fail(f"case {case_id}: compile specification is required")
        if compile_spec.get("engine") not in {"pdflatex", "lualatex"}:
            fail(f"case {case_id}: unsupported compile engine")
        passes = compile_spec.get("passes")
        if passes not in {1, 2, 3}:
            fail(f"case {case_id}: invalid compile pass count")
        biber_after_pass = compile_spec.get("biber_after_pass")
        if biber_after_pass is not None:
            if not isinstance(biber_after_pass, int) or biber_after_pass < 1 or biber_after_pass >= passes:
                fail(f"case {case_id}: invalid biber_after_pass")
        if not isinstance(case.get("expected_rule_id"), str) or not case["expected_rule_id"]:
            fail(f"case {case_id}: expected_rule_id is required")
    return cases


def output_tail(text: str, limit: int = 40) -> str:
    return "\n".join(text.splitlines()[-limit:])


def run_command(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )


def positive_rule_pass_line(output: str, rule_id: str) -> str:
    matches = [
        line
        for line in output.splitlines()
        if f"rule={rule_id}" in line and re.search(r"(?:^|\s)status=PASS(?:\s|$)", line)
    ]
    if not matches:
        raise CaseFailure(
            f"positive baseline did not emit PASS evidence for expected rule {rule_id}"
        )
    return matches[-1]


def mutate_source(source: str, mutation: dict[str, Any], case_id: str) -> str:
    anchor = mutation["anchor"]
    occurrences = source.count(anchor)
    if occurrences != 1:
        raise CaseFailure(
            f"mutation anchor for {case_id} must occur exactly once; found {occurrences}: {anchor!r}"
        )
    if mutation["kind"] == "insert_before":
        return source.replace(anchor, mutation["content"] + anchor, 1)
    return source.replace(anchor, mutation["content"], 1)


def safe_job_name(case_id: str) -> str:
    return "negative-" + re.sub(r"[^a-z0-9-]+", "-", case_id.casefold()).strip("-")


def expand_command(command: list[str], values: dict[str, str]) -> list[str]:
    return [item.format_map(values) for item in command]


def failed_rule_from_evidence(path: Path, rule_id: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CaseFailure(f"validator evidence JSON is missing or invalid: {path}: {exc}") from exc
    evidence = payload.get("evidence")
    if not isinstance(evidence, list):
        raise CaseFailure(f"validator evidence JSON has no evidence list: {path}")
    matches = [
        item
        for item in evidence
        if isinstance(item, dict) and item.get("rule_id") == rule_id
    ]
    if len(matches) != 1:
        raise CaseFailure(f"expected exactly one evidence item for {rule_id}; found {len(matches)}")
    if matches[0].get("status") != "FAIL":
        raise CaseFailure(
            f"expected rule {rule_id} to be rejected; observed status={matches[0].get('status')}"
        )
    return matches[0]


def compile_negative_fixture(
    case_id: str,
    mutated_tex: Path,
    temp_dir: Path,
    compile_spec: dict[str, Any],
    env: dict[str, str],
) -> Path:
    job = safe_job_name(case_id)
    engine = compile_spec["engine"]
    passes = int(compile_spec["passes"])
    biber_after_pass = compile_spec.get("biber_after_pass")
    compile_output = ""
    command = [
        engine,
        f"-jobname={job}",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={temp_dir}",
        str(mutated_tex),
    ]

    for pass_index in range(1, passes + 1):
        compiled = run_command(command, env=env)
        compile_output += f"\n--- latex pass {pass_index} ---\n{compiled.stdout}"
        if compiled.returncode != 0:
            raise CaseFailure(
                f"negative fixture compile failed for {case_id}; compile failure does not count as rejection\n"
                + output_tail(compile_output)
            )
        if biber_after_pass == pass_index:
            biber = run_command(
                [
                    "biber",
                    "--input-directory",
                    str(temp_dir),
                    "--output-directory",
                    str(temp_dir),
                    job,
                ],
                env=env,
            )
            compile_output += f"\n--- biber after pass {pass_index} ---\n{biber.stdout}"
            if biber.returncode != 0:
                raise CaseFailure(
                    f"negative fixture bibliography build failed for {case_id}; build failure does not count as rejection\n"
                    + output_tail(compile_output)
                )

    pdf = temp_dir / f"{job}.pdf"
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise CaseFailure(f"negative fixture did not produce a PDF for {case_id}: {pdf}")
    return pdf


def run_case(case: dict[str, Any], env: dict[str, str]) -> dict[str, Any]:
    case_id = case["id"]
    expected_rule_id = case["expected_rule_id"]
    positive_gate = list(case["positive_gate"])
    positive = run_command(positive_gate, env=env)
    if positive.returncode != 0:
        raise CaseFailure(
            f"positive baseline failed for {case_id}: {' '.join(positive_gate)}\n"
            + output_tail(positive.stdout)
        )
    positive_rule_evidence = positive_rule_pass_line(positive.stdout, expected_rule_id)

    fixture = ROOT / case["fixture"]
    mutated = mutate_source(fixture.read_text(encoding="utf-8"), case["mutation"], case_id)

    with tempfile.TemporaryDirectory(prefix=f"abntexto-ufc-{safe_job_name(case_id)}-") as temp_name:
        temp_dir = Path(temp_name)
        mutated_tex = temp_dir / fixture.name
        mutated_tex.write_text(mutated, encoding="utf-8")
        pdf = compile_negative_fixture(case_id, mutated_tex, temp_dir, case["compile"], env)

        evidence_json = temp_dir / f"{safe_job_name(case_id)}-evidence.json"
        validator_command = expand_command(
            list(case["validator"]),
            {"pdf": str(pdf), "evidence_json": str(evidence_json)},
        )
        validation = run_command(validator_command, env=env)
        if validation.returncode == 0:
            raise CaseFailure(
                f"target validator accepted the controlled violation for {case_id}: {' '.join(validator_command)}"
            )
        failed_evidence = failed_rule_from_evidence(evidence_json, expected_rule_id)

        return {
            "id": case_id,
            "family": case["family"],
            "status": "PASS",
            "fixture": case["fixture"],
            "positive_gate": positive_gate,
            "positive_rule_evidence": positive_rule_evidence,
            "positive_negative_rule_coupled": True,
            "mutation": case["mutation"],
            "compile": case["compile"],
            "validator": list(case["validator"]),
            "validator_exit_code": validation.returncode,
            "expected_rule_id": expected_rule_id,
            "failed_rule_evidence": failed_evidence,
            "compile_failure_counted_as_rejection": False,
            "temporary_mutation": True,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exercise controlled negative mutations against current normative validators."
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=ROOT / "artifacts" / "negative-paths" / "negative-paths.json",
    )
    parser.add_argument(
        "--case",
        action="append",
        dest="case_ids",
        help="Run only the selected case id. May be repeated.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = validate_manifest(load_json(MANIFEST))
    selected_ids = set(args.case_ids or EXPECTED_CASE_IDS)
    unknown = sorted(selected_ids - set(EXPECTED_CASE_IDS))
    if unknown:
        fail("unknown negative case id(s): " + ", ".join(unknown))
    selected = [case for case in cases if case["id"] in selected_ids]

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for case in selected:
        try:
            result = run_case(case, env)
            results.append(result)
            print(
                "NEGATIVE-PATH-EVIDENCE "
                f"id={result['id']} status=PASS family={result['family']} "
                f"expected_rule={result['expected_rule_id']} positive_rule=PASS "
                f"validator_exit={result['validator_exit_code']}"
            )
        except CaseFailure as exc:
            failures.append(
                {
                    "id": case["id"],
                    "family": case["family"],
                    "status": "FAIL",
                    "reason": str(exc),
                }
            )
            print(
                "NEGATIVE-PATH-EVIDENCE "
                f"id={case['id']} status=FAIL family={case['family']} "
                f"reason={json.dumps(str(exc), ensure_ascii=False)}"
            )

    payload = {
        "schema_version": 2,
        "source_commit_sha": os.environ.get("SOURCE_COMMIT_SHA", os.environ.get("GITHUB_SHA", "")),
        "result": "PASS" if not failures else "FAIL",
        "selected_case_ids": [case["id"] for case in selected],
        "passed": len(results),
        "failed": len(failures),
        "results": results,
        "failures": failures,
        "normative_contract_changed": False,
        "locator_policy_changed": False,
        "validator_tolerances_changed": False,
        "proof_state_changed": False,
    }
    output_path = args.json if args.json.is_absolute() else ROOT / args.json
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "NEGATIVE-PATH-SUMMARY "
        f"PASS={len(results)} FAIL={len(failures)} selected={len(selected)} "
        "positive_negative_rule_coupled=true proof_state_changed=false"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

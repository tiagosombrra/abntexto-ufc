#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B1_PATH = ROOT / "release/n15-b2r-b-public-api.json"
B2_PATH = ROOT / "release/n15-b2r-b2-setup-aliases.json"
B3_PATH = ROOT / "release/n15-b2r-b3-command-environment-aliases.json"
B4_PATH = ROOT / "release/n15-b2r-b4-en-pt-equivalence.json"
RUNTIME_PATH = ROOT / "abntexto-ufc/public-api.def"
N12_WORKFLOW_PATH = ROOT / ".github/workflows/latex-preflight.yml"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def require_blob(path: Path, expected: str, label: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"{label}: missing {path.relative_to(ROOT).as_posix()}")
        return
    actual = git_blob_sha(path)
    if actual != expected:
        errors.append(f"{label}: expected blob {expected}, got {actual}")


def parse_pair(value: str) -> tuple[str, str]:
    key, item = value.split("/", 1)
    return key, item


def canonical_choice_forwarding(
    runtime: str,
    legacy_source: str,
    canonical_target: str,
) -> bool:
    legacy_key, legacy_value = parse_pair(legacy_source)
    canonical_key, canonical_value = parse_pair(canonical_target)
    pattern = re.compile(
        rf"(?m)^\s*{re.escape(canonical_key)}\s*/\s*{re.escape(canonical_value)}"
        rf"\s*\.meta:n\s*=\s*\{{\s*{re.escape(legacy_key)}\s*=\s*"
        rf"{re.escape(legacy_value)}\s*\}}\s*,?"
    )
    return pattern.search(runtime) is not None


def simple_key_forwarding(runtime: str, legacy: str, canonical: str) -> bool:
    pattern = re.compile(
        rf"(?m)^\s*{re.escape(canonical)}\s*\.meta:n\s*=\s*"
        rf"\{{\s*{re.escape(legacy)}\s*=\s*\{{\s*#1\s*\}}\s*\}}\s*,?"
    )
    return pattern.search(runtime) is not None


def declaration_snippet(runtime: str, needle: str, span: int = 1200) -> str:
    index = runtime.find(needle)
    if index < 0:
        return ""
    return runtime[index : index + span]


def run_paired_gate(path: str, errors: list[str]) -> None:
    completed = subprocess.run(
        ["sh", path],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        errors.append("B4 paired EN/PT gate failed:\n" + completed.stdout[-7000:])
        return
    print(completed.stdout, end="")


def main() -> int:
    b1 = read_json(B1_PATH)
    b2 = read_json(B2_PATH)
    b3 = read_json(B3_PATH)
    b4 = read_json(B4_PATH)
    runtime = RUNTIME_PATH.read_text(encoding="utf-8")
    errors: list[str] = []

    require(b1.get("phase") == "N15-B2R-B1", "B4: invalid B1 base contract", errors)
    require(b2.get("phase") == "N15-B2R-B2", "B4: invalid B2 base contract", errors)
    require(b3.get("phase") == "N15-B2R-B3", "B4: invalid B3 base contract", errors)
    require(
        b4.get("schema_version") == 1 and b4.get("phase") == "N15-B2R-B4",
        "B4: expected N15-B2R-B4 schema 1 contract",
        errors,
    )
    require(
        b4.get("status") in {"IMPLEMENTATION_ACTIVE", "PR_CERTIFICATION_PENDING", "DONE"},
        f"B4: invalid status {b4.get('status')!r}",
        errors,
    )
    require(
        b4.get("base_main_sha") == "92f17418dfeee4d2d45456912af9f8c399457cc1",
        "B4: certified base main SHA changed",
        errors,
    )

    contracts = b4.get("base_contracts", {})
    expected_contracts = {
        "b1": (B1_PATH, "release/n15-b2r-b-public-api.json"),
        "b2": (B2_PATH, "release/n15-b2r-b2-setup-aliases.json"),
        "b3": (B3_PATH, "release/n15-b2r-b3-command-environment-aliases.json"),
    }
    for name, (path, expected_path) in expected_contracts.items():
        entry = contracts.get(name, {})
        require(entry.get("path") == expected_path, f"B4: invalid {name.upper()} contract path", errors)
        require_blob(path, entry.get("blob_sha", ""), f"B4 frozen {name.upper()} contract", errors)

    frozen_runtime = b4.get("frozen_runtime", {})
    require(
        frozen_runtime.get("path") == "abntexto-ufc/public-api.def",
        "B4: invalid frozen runtime path",
        errors,
    )
    require_blob(
        RUNTIME_PATH,
        frozen_runtime.get("blob_sha", ""),
        "B4 frozen public API runtime",
        errors,
    )

    evidence = b4.get("evidence", {})
    n12_blob = evidence.get("frozen_n12_workflow_blob", "")
    require_blob(N12_WORKFLOW_PATH, n12_blob, "B4 frozen N12 workflow", errors)
    require(evidence.get("article_runtime") is False, "B4: article runtime must remain false", errors)

    policy = b4.get("policy", {})
    require(policy.get("migration") == "additive", "B4: migration must remain additive", errors)
    for key in (
        "supported_portuguese_v2x_removal_allowed",
        "article_runtime_allowed",
        "public_api_surface_change_allowed",
        "runtime_change_allowed",
        "normative_behavior_change_allowed",
        "latex_preflight_workflow_change_allowed",
    ):
        require(policy.get(key) is False, f"B4: policy {key} must remain false", errors)
    require(
        policy.get("observable_equivalence_required") is True,
        "B4: observable equivalence must remain required",
        errors,
    )
    require(
        policy.get("raw_pdf_byte_identity_required") is False,
        "B4: raw PDF byte identity must remain non-required",
        errors,
    )

    expected_counts = b4.get("expected_counts", {})
    b3_counts = b3.get("expected_counts", {})
    for key in ("setup_keys", "setup_values", "commands", "environments", "extension_hooks"):
        require(
            expected_counts.get(key) == b3_counts.get(key),
            f"B4: public API count changed for {key}",
            errors,
        )

    setup_contract = b4.get("equivalence_contract", {}).get("setup_forwarding", {})
    key_map = b2.get("canonical_setup_key_map", {})
    same_name = {legacy for legacy, canonical in key_map.items() if legacy == canonical}
    distinct_key_map = {legacy: canonical for legacy, canonical in key_map.items() if legacy != canonical}
    require(
        len(distinct_key_map) == setup_contract.get("canonical_key_mappings"),
        "B4: canonical setup key mapping count changed",
        errors,
    )
    require(
        sorted(same_name) == sorted(setup_contract.get("retained_same-name_keys", [])),
        "B4: retained same-name setup keys changed",
        errors,
    )

    value_map = b2.get("canonical_setup_value_map", {})
    require(
        len(value_map) == setup_contract.get("canonical_value_mappings"),
        "B4: canonical setup value mapping count changed",
        errors,
    )

    sources_by_target: dict[str, list[str]] = {}
    for legacy_source, canonical_target in value_map.items():
        sources_by_target.setdefault(canonical_target, []).append(legacy_source)

    for canonical_target, legacy_sources in sorted(sources_by_target.items()):
        if not any(canonical_choice_forwarding(runtime, source, canonical_target) for source in legacy_sources):
            errors.append(
                "B4: canonical choice does not forward to an approved certified legacy identity: "
                f"{canonical_target} <- {', '.join(sorted(legacy_sources))}"
            )

    choice_legacy_keys = {parse_pair(source)[0] for source in value_map}
    for legacy, canonical in sorted(distinct_key_map.items()):
        if legacy in choice_legacy_keys:
            continue
        if not simple_key_forwarding(runtime, legacy, canonical):
            errors.append(f"B4: setup forwarding missing: {legacy} -> {canonical}")

    command_contract = b4.get("equivalence_contract", {}).get("command_forwarding", {})
    command_map = b3.get("canonical_command_map", {})
    require(
        len(command_map) == command_contract.get("canonical_wrappers"),
        "B4: canonical command wrapper count changed",
        errors,
    )
    for legacy, canonical in sorted(command_map.items()):
        snippet = declaration_snippet(runtime, canonical)
        if not snippet:
            errors.append(f"B4: canonical command declaration missing: {canonical}")
        elif legacy not in snippet:
            errors.append(f"B4: canonical command no longer forwards to {legacy}: {canonical}")

    epigraph = declaration_snippet(runtime, "\\ufcPrintEpigraph")
    for marker in ("{short}", "[curta]", "{long}", "[longa]"):
        if marker not in epigraph:
            errors.append(f"B4: epigraph special forwarding marker missing: {marker}")

    environment_contract = b4.get("equivalence_contract", {}).get("environment_forwarding", {})
    environment_map = b3.get("canonical_environment_map", {})
    require(
        len(environment_map) == environment_contract.get("canonical_wrappers"),
        "B4: canonical environment wrapper count changed",
        errors,
    )
    for legacy, canonical in sorted(environment_map.items()):
        snippet = declaration_snippet(runtime, f"{{ {canonical} }}")
        if not snippet:
            errors.append(f"B4: canonical environment declaration missing: {canonical}")
            continue
        if f"\\begin{{{legacy}}}" not in snippet or f"\\end{{{legacy}}}" not in snippet:
            errors.append(f"B4: canonical environment no longer forwards to {legacy}: {canonical}")

    for path_key in ("paired_fixture", "paired_summary_fixture", "paired_runner"):
        relative = evidence.get(path_key, "")
        require(bool(relative) and (ROOT / relative).is_file(), f"B4: evidence file missing: {path_key}", errors)

    if not errors:
        run_paired_gate(evidence["paired_runner"], errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "N15-EVIDENCE B2R-B4-CONTRACT "
        f"setup_keys={len(distinct_key_map)} "
        f"setup_values={len(value_map)} "
        f"commands={len(command_map)} "
        f"environments={len(environment_map)} "
        f"runtime_blob={frozen_runtime['blob_sha']} "
        f"n12_blob={n12_blob}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

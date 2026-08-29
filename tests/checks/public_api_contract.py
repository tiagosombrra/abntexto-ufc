#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B1_PATH = ROOT / "release/n15-b2r-b-public-api.json"
B2_PATH = ROOT / "release/n15-b2r-b2-setup-aliases.json"
B3_PATH = ROOT / "release/n15-b2r-b3-command-environment-aliases.json"

KEY_PATTERN = re.compile(
    r"(?m)^\s*([a-z][a-z0-9-]*)\s*\."
    r"(?:choice|code|meta|tl_gset)(?::[A-Za-z]+)?\s*(?::|=)"
)
VALUE_PATTERN = re.compile(
    r"(?m)^\s*([a-z][a-z0-9-]*)\s*/\s*([A-Za-z0-9-]+)\s*\."
    r"(?:code|meta)(?::[A-Za-z]+)?\s*="
)
XPARSE_COMMAND_PATTERN = re.compile(
    r"\\(?:New|Renew|Provide)(?:Expandable)?DocumentCommand"
    r"\s*\{?\s*(\\[A-Za-z@]+)"
)
STANDARD_UFC_COMMAND_PATTERN = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand)\*?"
    r"\s*\{?\s*(\\ufc[A-Za-z@]+)"
)
XPARSE_ENV_PATTERN = re.compile(
    r"\\(?:New|Renew|Provide)DocumentEnvironment"
    r"\s*\{?\s*([A-Za-z@]+)"
)
LISTINGS_ENV_PATTERN = re.compile(r"\\lstnewenvironment\s*\{([A-Za-z@]+)")
PROVIDES_CLASS_PATTERN = re.compile(r"\\ProvidesClass\{([^}]+)\}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flatten(mapping: dict[str, list[str]]) -> list[str]:
    return [item for items in mapping.values() for item in items]


def scoped_values(mapping: dict[str, list[str]]) -> set[tuple[str, str]]:
    return {
        (key, value)
        for key, values in mapping.items()
        for value in values
    }


def duplicate_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(duplicates)


def compare_sets(
    label: str,
    actual: set[str],
    expected: set[str],
    errors: list[str],
) -> None:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{label}: missing: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: unreviewed: {', '.join(extra)}")


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def pair_id(pair: tuple[str, str]) -> str:
    return f"{pair[0]}/{pair[1]}"


def parse_pair(value: str, label: str, errors: list[str]) -> tuple[str, str] | None:
    if value.count("/") != 1:
        errors.append(f"{label}: expected setup-key/value identity: {value}")
        return None
    key, item = value.split("/", 1)
    if not key or not item:
        errors.append(f"{label}: invalid setup-key/value identity: {value}")
        return None
    return key, item


def check_blob(
    path: Path,
    expected_sha: str | None,
    label: str,
    errors: list[str],
) -> None:
    if not path.is_file():
        errors.append(f"{label}: missing file {path.relative_to(ROOT).as_posix()}")
        return
    actual_sha = git_blob_sha(path.read_bytes())
    if actual_sha != expected_sha:
        errors.append(f"{label}: expected blob {expected_sha}, got {actual_sha}")


def run_smoke(path: str, label: str, errors: list[str]) -> None:
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
        errors.append(f"{label} failed:\n" + completed.stdout[-4000:])
    else:
        print(completed.stdout, end="")


def main() -> None:
    b1 = json.loads(read_text(B1_PATH))
    b2 = json.loads(read_text(B2_PATH))
    b3 = json.loads(read_text(B3_PATH))
    errors: list[str] = []

    if b1.get("schema_version") != 1 or b1.get("phase") != "N15-B2R-B1":
        errors.append("B1: expected certified N15-B2R-B1 schema 1 contract")
    if b2.get("schema_version") != 1 or b2.get("phase") != "N15-B2R-B2":
        errors.append("B2: expected certified N15-B2R-B2 schema 1 contract")
    if b3.get("schema_version") != 1 or b3.get("phase") != "N15-B2R-B3":
        errors.append("B3: expected N15-B2R-B3 schema 1 contract")

    b2_base = b2.get("base_contract", {})
    if b2_base.get("path") != "release/n15-b2r-b-public-api.json":
        errors.append("B2: base contract path is invalid")
    check_blob(B1_PATH, b2_base.get("blob_sha"), "B1 frozen contract", errors)

    b3_contracts = b3.get("base_contracts", {})
    b3_b1 = b3_contracts.get("b1", {})
    b3_b2 = b3_contracts.get("b2", {})
    if b3_b1.get("path") != "release/n15-b2r-b-public-api.json":
        errors.append("B3: B1 contract path is invalid")
    if b3_b2.get("path") != "release/n15-b2r-b2-setup-aliases.json":
        errors.append("B3: B2 contract path is invalid")
    check_blob(B1_PATH, b3_b1.get("blob_sha"), "B3 frozen B1 contract", errors)
    check_blob(B2_PATH, b3_b2.get("blob_sha"), "B3 frozen B2 contract", errors)

    b2_policy = b2.get("policy", {})
    if b2_policy.get("migration") != "additive":
        errors.append("B2: migration must remain additive")
    if b2_policy.get("supported_portuguese_v2x_removal_allowed") is not False:
        errors.append("B2: Portuguese v2.x removal must remain forbidden")
    if b2_policy.get("article_runtime_allowed") is not False:
        errors.append("B2: article runtime must remain disabled")
    if b2_policy.get("value_identity") != "setup-key/value":
        errors.append("B2: setup values must be scoped by setup key")

    b3_policy = b3.get("policy", {})
    if b3_policy.get("migration") != "additive":
        errors.append("B3: migration must remain additive")
    if b3_policy.get("supported_portuguese_v2x_removal_allowed") is not False:
        errors.append("B3: Portuguese v2.x removal must remain forbidden")
    if b3_policy.get("article_runtime_allowed") is not False:
        errors.append("B3: article runtime must remain disabled")
    if b3_policy.get("setup_surface_change_allowed") is not False:
        errors.append("B3: setup surface changes are forbidden")
    if b3_policy.get("normative_behavior_change_allowed") is not False:
        errors.append("B3: normative behavior changes are forbidden")

    source_names = list(b1["source_modules"]) + list(b2["source_modules"])
    if len(source_names) != len(set(source_names)):
        errors.append("source modules duplicated across B1 and B2 contracts")
    source_paths = [ROOT / item for item in source_names]
    missing_sources = [
        path.relative_to(ROOT).as_posix()
        for path in source_paths
        if not path.is_file()
    ]
    if missing_sources:
        errors.append("inventory: missing source modules: " + ", ".join(missing_sources))

    source_texts = {
        path.relative_to(ROOT).as_posix(): read_text(path)
        for path in source_paths
        if path.is_file()
    }
    combined = "\n".join(source_texts.values())
    public_api_text = source_texts.get(b3.get("source_module", ""), "")
    if not public_api_text:
        errors.append("B3: canonical public API source module is missing")

    # B2 setup surface remains exact during B3.
    legacy_keys_list = flatten(b1["setup_keys_by_source"])
    canonical_keys_list = flatten(b2["canonical_setup_keys_by_source"])
    if duplicate_items(legacy_keys_list):
        errors.append("legacy setup keys are duplicated")
    if duplicate_items(canonical_keys_list):
        errors.append("canonical setup keys are duplicated")

    legacy_keys = set(legacy_keys_list)
    canonical_keys = set(canonical_keys_list)
    overlap_keys = sorted(legacy_keys & canonical_keys)
    if overlap_keys:
        errors.append("canonical setup additions overlap legacy keys: " + ", ".join(overlap_keys))

    expected_keys = legacy_keys | canonical_keys
    actual_keys = set(KEY_PATTERN.findall(combined))
    compare_sets("setup keys", actual_keys, expected_keys, errors)

    for source, names in b2["canonical_setup_keys_by_source"].items():
        source_actual = set(KEY_PATTERN.findall(source_texts.get(source, "")))
        missing = sorted(set(names) - source_actual)
        if missing:
            errors.append(f"{source}: canonical setup keys missing: {', '.join(missing)}")

    legacy_values = scoped_values(b1["setup_values"])
    canonical_values = scoped_values(b2["canonical_setup_values"])
    overlap_values = sorted(legacy_values & canonical_values)
    if overlap_values:
        errors.append(
            "canonical setup values overlap legacy identities: "
            + ", ".join(pair_id(item) for item in overlap_values)
        )

    expected_values = legacy_values | canonical_values
    actual_values = set(VALUE_PATTERN.findall(combined))
    missing_values = sorted(expected_values - actual_values)
    extra_values = sorted(actual_values - expected_values)
    if missing_values:
        errors.append("setup values missing: " + ", ".join(pair_id(item) for item in missing_values))
    if extra_values:
        errors.append("setup values unreviewed: " + ", ".join(pair_id(item) for item in extra_values))

    canonical_key_map = b2.get("canonical_setup_key_map", {})
    special_keys = b2.get("setup_key_special_decisions", {})
    alias_only = {
        key
        for key, decision in special_keys.items()
        if decision.get("decision") == "compatibility_alias_only"
    }
    mapped_sources = set(canonical_key_map)
    compare_sets(
        "canonical setup key mapping coverage",
        mapped_sources | alias_only,
        legacy_keys,
        errors,
    )
    canonical_key_targets = list(canonical_key_map.values())
    duplicated_key_targets = duplicate_items(canonical_key_targets)
    if duplicated_key_targets:
        errors.append("canonical setup key targets duplicated: " + ", ".join(duplicated_key_targets))
    compare_sets(
        "canonical setup key additions",
        canonical_keys,
        set(canonical_key_targets) - legacy_keys,
        errors,
    )
    if b2.get("setup_key_review_required"):
        errors.append("B2 setup key review_required must remain empty")
    if b2.get("setup_value_review_required"):
        errors.append("B2 setup value review_required must remain empty")

    value_map = b2.get("canonical_setup_value_map", {})
    legacy_value_ids = {pair_id(item) for item in legacy_values}
    canonical_value_ids = {pair_id(item) for item in canonical_values}
    compare_sets("canonical setup value mapping coverage", set(value_map), legacy_value_ids, errors)
    for source, target in value_map.items():
        source_pair = parse_pair(source, "canonical setup value source", errors)
        target_pair = parse_pair(target, "canonical setup value target", errors)
        if source_pair is not None and source_pair not in legacy_values:
            errors.append(f"canonical setup value source is not legacy: {source}")
        if target_pair is not None and target not in canonical_value_ids:
            errors.append(f"canonical setup value target is not live: {source} -> {target}")
    missing_target_coverage = sorted(canonical_value_ids - set(value_map.values()))
    if missing_target_coverage:
        errors.append(
            "canonical setup values lack legacy behavior mapping: "
            + ", ".join(missing_target_coverage)
        )

    # B3 command migration is additive over the frozen 47-command B1 surface.
    extension_hooks = {item["name"] for item in b1.get("extension_hooks", [])}
    legacy_commands_list = flatten(b1["commands_by_source"])
    legacy_commands = set(legacy_commands_list)
    if duplicate_items(legacy_commands_list):
        errors.append("baseline commands are duplicated")

    b3_command_map = b3.get("canonical_command_map", {})
    canonical_command_targets = list(b3_command_map.values())
    canonical_commands = set(canonical_command_targets)
    duplicate_command_targets = duplicate_items(canonical_command_targets)
    if duplicate_command_targets:
        errors.append("B3 canonical command targets duplicated: " + ", ".join(duplicate_command_targets))
    overlap_commands = sorted(legacy_commands & canonical_commands)
    if overlap_commands:
        errors.append("B3 canonical commands overlap legacy commands: " + ", ".join(overlap_commands))

    migration_sources = (
        set(b1["command_classification"].get("portuguese_compatibility_api", []))
        | set(b1["command_classification"].get("project_public_review_required", []))
    )
    compare_sets("B3 command mapping sources", set(b3_command_map), migration_sources, errors)

    b1_approved_command_map = b1.get("canonical_command_map", {})
    for legacy, canonical in b1_approved_command_map.items():
        if b3_command_map.get(legacy) != canonical:
            errors.append(
                f"B3 changed B1-approved canonical command target: {legacy} -> {canonical}"
            )

    signature_targets = set(b3.get("canonical_command_signatures", {}))
    compare_sets("B3 canonical command signatures", signature_targets, canonical_commands, errors)
    if b3.get("command_review_required"):
        errors.append("B3 command review_required must be empty")

    retained_commands = set(flatten(b3.get("retained_command_classification", {})))
    compare_sets(
        "B3 command disposition coverage",
        set(b3_command_map) | retained_commands,
        legacy_commands,
        errors,
    )

    upstream_command_names = {
        item["name"]
        for item in b1.get("upstream_compatibility_surfaces", [])
        if item.get("kind") == "command"
    }
    xparse_commands = set(XPARSE_COMMAND_PATTERN.findall(combined))
    standard_ufc_commands = set(STANDARD_UFC_COMMAND_PATTERN.findall(combined))
    actual_commands = (
        xparse_commands | (standard_ufc_commands - extension_hooks)
    ) - upstream_command_names
    expected_commands = legacy_commands | canonical_commands
    compare_sets("commands", actual_commands, expected_commands, errors)

    baseline_classifications = flatten(b1["command_classification"])
    duplicate_classifications = duplicate_items(baseline_classifications)
    if duplicate_classifications:
        errors.append("B1 command classifications overlap: " + ", ".join(duplicate_classifications))
    compare_sets(
        "B1 command classification coverage",
        set(baseline_classifications),
        legacy_commands,
        errors,
    )

    for target in canonical_commands:
        if target not in public_api_text:
            errors.append(f"B3 canonical command missing from public-api.def: {target}")

    summary_target = b3_command_map.get("\\imprimirresumo")
    abstract_target = b3_command_map.get("\\imprimirabstract")
    if not summary_target or not abstract_target or summary_target == abstract_target:
        errors.append("B3 must keep summary and English abstract as distinct canonical commands")
    if "{short} { \\imprimirepigrafe[curta]" not in public_api_text:
        errors.append("B3 epigraph wrapper does not map short to curta")
    if "{long}  { \\imprimirepigrafe[longa]" not in public_api_text:
        errors.append("B3 epigraph wrapper does not map long to longa")

    # B3 environment migration keeps ufclisting as the already-English canonical surface.
    legacy_envs_list = flatten(b1["environments_by_source"])
    legacy_envs = set(legacy_envs_list)
    if duplicate_items(legacy_envs_list):
        errors.append("baseline environments are duplicated")

    b3_env_map = b3.get("canonical_environment_map", {})
    canonical_env_targets = list(b3_env_map.values())
    canonical_envs = set(canonical_env_targets)
    duplicate_env_targets = duplicate_items(canonical_env_targets)
    if duplicate_env_targets:
        errors.append("B3 canonical environment targets duplicated: " + ", ".join(duplicate_env_targets))
    overlap_envs = sorted(legacy_envs & canonical_envs)
    if overlap_envs:
        errors.append("B3 canonical environments overlap legacy environments: " + ", ".join(overlap_envs))

    retained_envs = set(b3.get("retained_environments", {}))
    compare_sets(
        "B3 environment disposition coverage",
        set(b3_env_map) | retained_envs,
        legacy_envs,
        errors,
    )
    compare_sets(
        "B3 canonical environment signatures",
        set(b3.get("canonical_environment_signatures", {})),
        canonical_envs,
        errors,
    )
    if b3.get("environment_review_required"):
        errors.append("B3 environment review_required must be empty")

    actual_envs = {
        name
        for name in (
            set(XPARSE_ENV_PATTERN.findall(combined))
            | set(LISTINGS_ENV_PATTERN.findall(combined))
        )
        if name.startswith("ufc")
    }
    expected_envs = legacy_envs | canonical_envs
    compare_sets("environments", actual_envs, expected_envs, errors)
    for target in canonical_envs:
        if target not in public_api_text:
            errors.append(f"B3 canonical environment missing from public-api.def: {target}")

    actual_hooks = {name for name in standard_ufc_commands if name.endswith("hook")}
    compare_sets("extension hooks", actual_hooks, extension_hooks, errors)

    for entrypoint in b1["class_entrypoints"]:
        path = ROOT / entrypoint["file"]
        if not path.is_file():
            errors.append(f"class entrypoint missing: {entrypoint['file']}")
            continue
        text = read_text(path)
        match = PROVIDES_CLASS_PATTERN.search(text)
        actual_name = match.group(1) if match else None
        if actual_name != entrypoint["name"]:
            errors.append(
                f"{entrypoint['file']}: expected ProvidesClass {entrypoint['name']}, "
                f"got {actual_name or 'missing'}"
            )
        if entrypoint.get("deprecated") and "deprecated" not in text.lower():
            errors.append(
                f"{entrypoint['file']}: deprecated compatibility entrypoint must emit a diagnostic"
            )

    for surface in b1.get("upstream_compatibility_surfaces", []):
        source = source_texts.get(surface["source"], "")
        if surface["name"] not in source:
            errors.append(
                "upstream compatibility surface missing: "
                f"{surface['source']}:{surface['name']}"
            )

    if ("type", "article") in actual_values or ("tipo", "artigo") in actual_values:
        errors.append("article setup value became live before N15-B2B")

    b2_counts = b2["expected_counts"]
    b2_actual_counts = {
        "legacy_setup_keys": len(legacy_keys),
        "canonical_setup_keys": len(canonical_keys),
        "setup_keys": len(actual_keys),
        "legacy_setup_values": len(legacy_values),
        "canonical_setup_values": len(canonical_values),
        "setup_values": len(actual_values),
    }
    for label in (
        "legacy_setup_keys", "canonical_setup_keys", "setup_keys",
        "legacy_setup_values", "canonical_setup_values", "setup_values",
    ):
        if b2_actual_counts[label] != b2_counts[label]:
            errors.append(
                f"B2 count {label}: expected {b2_counts[label]}, got {b2_actual_counts[label]}"
            )

    b3_counts = b3["expected_counts"]
    actual_counts = {
        "setup_keys": len(actual_keys),
        "setup_values": len(actual_values),
        "legacy_commands": len(legacy_commands),
        "canonical_commands_added": len(canonical_commands),
        "commands": len(actual_commands),
        "legacy_environments": len(legacy_envs),
        "canonical_environments_added": len(canonical_envs),
        "environments": len(actual_envs),
        "extension_hooks": len(actual_hooks),
    }
    for label, expected_count in b3_counts.items():
        actual_count = actual_counts.get(label)
        if actual_count != expected_count:
            errors.append(f"B3 count {label}: expected {expected_count}, got {actual_count}")

    frozen = b1["policy"]["frozen_workflow"]
    workflow_path = ROOT / frozen["path"]
    if not workflow_path.is_file():
        errors.append(f"frozen workflow missing: {frozen['path']}")
    else:
        actual_blob = git_blob_sha(workflow_path.read_bytes())
        if actual_blob != frozen["blob_sha"]:
            errors.append(
                f"frozen workflow blob changed: expected {frozen['blob_sha']}, got {actual_blob}"
            )

    if not errors:
        run_smoke("tests/v2-public-api-alias-check.sh", "B2 canonical setup alias smoke", errors)
    if not errors:
        run_smoke(
            "tests/v2-public-api-command-environment-check.sh",
            "B3 canonical command/environment smoke",
            errors,
        )

    if errors:
        for error in sorted(set(errors)):
            print(error)
        raise SystemExit(f"Public API contract failed with {len(set(errors))} issue(s).")

    print(
        "N15-EVIDENCE public-api "
        f"legacy_keys={len(legacy_keys)} "
        f"canonical_keys={len(canonical_keys)} "
        f"keys={len(actual_keys)} "
        f"legacy_values={len(legacy_values)} "
        f"canonical_values={len(canonical_values)} "
        f"values={len(actual_values)} "
        f"legacy_commands={len(legacy_commands)} "
        f"canonical_commands={len(canonical_commands)} "
        f"commands={len(actual_commands)} "
        f"legacy_environments={len(legacy_envs)} "
        f"canonical_environments={len(canonical_envs)} "
        f"environments={len(actual_envs)} "
        f"hooks={len(actual_hooks)} "
        "article_runtime=false "
        f"n12_blob={frozen['blob_sha']}"
    )
    print("Public API additive B1/B2/B3 contract passed.")


if __name__ == "__main__":
    main()

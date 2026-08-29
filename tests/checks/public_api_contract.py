#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = ROOT / "release/n15-b2r-b-public-api.json"
DELTA_PATH = ROOT / "release/n15-b2r-b2-setup-aliases.json"

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
LISTINGS_ENV_PATTERN = re.compile(
    r"\\lstnewenvironment\s*\{([A-Za-z@]+)"
)
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


def main() -> None:
    baseline = json.loads(read_text(BASELINE_PATH))
    delta = json.loads(read_text(DELTA_PATH))
    errors: list[str] = []

    if baseline.get("schema_version") != 1 or baseline.get("phase") != "N15-B2R-B1":
        errors.append("baseline: expected certified N15-B2R-B1 schema 1 contract")
    if delta.get("schema_version") != 1 or delta.get("phase") != "N15-B2R-B2":
        errors.append("delta: expected N15-B2R-B2 schema 1 contract")

    base_contract = delta.get("base_contract", {})
    if base_contract.get("path") != "release/n15-b2r-b-public-api.json":
        errors.append("delta: base contract path is invalid")
    actual_baseline_blob = git_blob_sha(BASELINE_PATH.read_bytes())
    expected_baseline_blob = base_contract.get("blob_sha")
    if actual_baseline_blob != expected_baseline_blob:
        errors.append(
            "B2R-B1 baseline contract changed: expected "
            f"{expected_baseline_blob}, got {actual_baseline_blob}"
        )

    policy = delta.get("policy", {})
    if policy.get("migration") != "additive":
        errors.append("delta: B2R-B2 migration must remain additive")
    if policy.get("supported_portuguese_v2x_removal_allowed") is not False:
        errors.append("delta: Portuguese v2.x removal must remain forbidden")
    if policy.get("article_runtime_allowed") is not False:
        errors.append("delta: article runtime must remain disabled during B2R-B2")
    if policy.get("value_identity") != "setup-key/value":
        errors.append("delta: setup values must be scoped by setup key")

    source_names = list(baseline["source_modules"]) + list(delta["source_modules"])
    if len(source_names) != len(set(source_names)):
        errors.append("source modules duplicated across baseline and B2R-B2 delta")
    source_paths = [ROOT / item for item in source_names]
    missing_sources = [
        path.relative_to(ROOT).as_posix()
        for path in source_paths
        if not path.is_file()
    ]
    if missing_sources:
        errors.append(
            "inventory: missing source modules: " + ", ".join(missing_sources)
        )

    source_texts = {
        path.relative_to(ROOT).as_posix(): read_text(path)
        for path in source_paths
        if path.is_file()
    }
    combined = "\n".join(source_texts.values())

    legacy_keys_list = flatten(baseline["setup_keys_by_source"])
    canonical_keys_list = flatten(delta["canonical_setup_keys_by_source"])
    legacy_key_duplicates = duplicate_items(legacy_keys_list)
    canonical_key_duplicates = duplicate_items(canonical_keys_list)
    if legacy_key_duplicates:
        errors.append(
            "legacy setup keys duplicated: " + ", ".join(legacy_key_duplicates)
        )
    if canonical_key_duplicates:
        errors.append(
            "canonical setup keys duplicated: " + ", ".join(canonical_key_duplicates)
        )

    legacy_keys = set(legacy_keys_list)
    canonical_keys = set(canonical_keys_list)
    overlap = sorted(legacy_keys & canonical_keys)
    if overlap:
        errors.append(
            "canonical setup additions overlap legacy keys: " + ", ".join(overlap)
        )

    expected_keys = legacy_keys | canonical_keys
    actual_keys = set(KEY_PATTERN.findall(combined))
    compare_sets("setup keys", actual_keys, expected_keys, errors)

    for source, names in delta["canonical_setup_keys_by_source"].items():
        source_actual = set(KEY_PATTERN.findall(source_texts.get(source, "")))
        missing = sorted(set(names) - source_actual)
        if missing:
            errors.append(
                f"{source}: canonical setup keys missing: {', '.join(missing)}"
            )

    legacy_values = scoped_values(baseline["setup_values"])
    canonical_values = scoped_values(delta["canonical_setup_values"])
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
        errors.append(
            "setup values missing: "
            + ", ".join(pair_id(item) for item in missing_values)
        )
    if extra_values:
        errors.append(
            "setup values unreviewed: "
            + ", ".join(pair_id(item) for item in extra_values)
        )

    canonical_key_map = delta.get("canonical_setup_key_map", {})
    special = delta.get("setup_key_special_decisions", {})
    alias_only = {
        key
        for key, decision in special.items()
        if decision.get("decision") == "compatibility_alias_only"
    }
    mapped_sources = set(canonical_key_map)
    if mapped_sources | alias_only != legacy_keys:
        missing = sorted(legacy_keys - mapped_sources - alias_only)
        extra = sorted((mapped_sources | alias_only) - legacy_keys)
        if missing:
            errors.append(
                "canonical setup key mapping incomplete: " + ", ".join(missing)
            )
        if extra:
            errors.append(
                "canonical setup key mapping references unknown legacy keys: "
                + ", ".join(extra)
            )

    canonical_targets = list(canonical_key_map.values())
    duplicate_targets = duplicate_items(canonical_targets)
    if duplicate_targets:
        errors.append(
            "canonical setup key targets duplicated: " + ", ".join(duplicate_targets)
        )
    unknown_targets = sorted(set(canonical_targets) - expected_keys)
    if unknown_targets:
        errors.append(
            "canonical setup key targets are not live: " + ", ".join(unknown_targets)
        )
    compare_sets(
        "canonical setup key additions",
        canonical_keys,
        set(canonical_targets) - legacy_keys,
        errors,
    )

    if delta.get("setup_key_review_required"):
        errors.append("B2R-B2 setup key review_required must be empty")
    if delta.get("setup_value_review_required"):
        errors.append("B2R-B2 setup value review_required must be empty")

    value_map = delta.get("canonical_setup_value_map", {})
    legacy_value_ids = {pair_id(item) for item in legacy_values}
    compare_sets(
        "canonical setup value mapping coverage",
        set(value_map),
        legacy_value_ids,
        errors,
    )
    canonical_value_ids = {pair_id(item) for item in canonical_values}
    for source, target in value_map.items():
        source_pair = parse_pair(source, "canonical setup value source", errors)
        target_pair = parse_pair(target, "canonical setup value target", errors)
        if source_pair is not None and source_pair not in legacy_values:
            errors.append(
                f"canonical setup value source is not legacy: {source}"
            )
        if target_pair is not None and target not in canonical_value_ids:
            errors.append(
                f"canonical setup value target is not live: {source} -> {target}"
            )
    missing_target_coverage = sorted(canonical_value_ids - set(value_map.values()))
    if missing_target_coverage:
        errors.append(
            "canonical setup values lack legacy behavior mapping: "
            + ", ".join(missing_target_coverage)
        )

    extension_hooks = {
        item["name"] for item in baseline.get("extension_hooks", [])
    }
    expected_commands_list = flatten(baseline["commands_by_source"])
    command_duplicates = duplicate_items(expected_commands_list)
    if command_duplicates:
        errors.append(
            "baseline commands duplicated: " + ", ".join(command_duplicates)
        )
    expected_commands = set(expected_commands_list)

    upstream_command_names = {
        item["name"]
        for item in baseline.get("upstream_compatibility_surfaces", [])
        if item.get("kind") == "command"
    }
    xparse_commands = set(XPARSE_COMMAND_PATTERN.findall(combined))
    standard_ufc_commands = set(STANDARD_UFC_COMMAND_PATTERN.findall(combined))
    actual_commands = (
        xparse_commands | (standard_ufc_commands - extension_hooks)
    ) - upstream_command_names
    compare_sets("commands", actual_commands, expected_commands, errors)

    classifications = flatten(baseline["command_classification"])
    classification_duplicates = duplicate_items(classifications)
    if classification_duplicates:
        errors.append(
            "command classifications overlap: "
            + ", ".join(classification_duplicates)
        )
    compare_sets(
        "command classification coverage",
        set(classifications),
        expected_commands,
        errors,
    )

    expected_envs_list = flatten(baseline["environments_by_source"])
    env_duplicates = duplicate_items(expected_envs_list)
    if env_duplicates:
        errors.append(
            "baseline environments duplicated: " + ", ".join(env_duplicates)
        )
    expected_envs = set(expected_envs_list)
    actual_envs = {
        name
        for name in (
            set(XPARSE_ENV_PATTERN.findall(combined))
            | set(LISTINGS_ENV_PATTERN.findall(combined))
        )
        if name.startswith("ufc")
    }
    compare_sets("environments", actual_envs, expected_envs, errors)

    actual_hooks = {
        name for name in standard_ufc_commands if name.endswith("hook")
    }
    compare_sets("extension hooks", actual_hooks, extension_hooks, errors)

    for entrypoint in baseline["class_entrypoints"]:
        path = ROOT / entrypoint["file"]
        if not path.is_file():
            errors.append(f"class entrypoint missing: {entrypoint['file']}")
            continue
        text = read_text(path)
        match = PROVIDES_CLASS_PATTERN.search(text)
        actual_name = match.group(1) if match else None
        if actual_name != entrypoint["name"]:
            errors.append(
                f"{entrypoint['file']}: expected ProvidesClass "
                f"{entrypoint['name']}, got {actual_name or 'missing'}"
            )
        if entrypoint.get("deprecated") and "deprecated" not in text.lower():
            errors.append(
                f"{entrypoint['file']}: deprecated compatibility entrypoint "
                "must emit a deprecation diagnostic"
            )

    for surface in baseline.get("upstream_compatibility_surfaces", []):
        source = source_texts.get(surface["source"], "")
        if surface["name"] not in source:
            errors.append(
                "upstream compatibility surface missing: "
                f"{surface['source']}:{surface['name']}"
            )

    if ("type", "article") in actual_values or ("tipo", "artigo") in actual_values:
        errors.append(
            "article setup value became live during B2R-B2; reserve activation for N15-B2B"
        )

    expected_counts = delta["expected_counts"]
    actual_counts = {
        "legacy_setup_keys": len(legacy_keys),
        "canonical_setup_keys": len(canonical_keys),
        "setup_keys": len(actual_keys),
        "legacy_setup_values": len(legacy_values),
        "canonical_setup_values": len(canonical_values),
        "setup_values": len(actual_values),
        "commands": len(actual_commands),
        "environments": len(actual_envs),
        "extension_hooks": len(actual_hooks),
    }
    for label, expected_count in expected_counts.items():
        actual_count = actual_counts.get(label)
        if actual_count != expected_count:
            errors.append(
                f"count {label}: expected {expected_count}, got {actual_count}"
            )

    frozen = baseline["policy"]["frozen_workflow"]
    workflow_path = ROOT / frozen["path"]
    if not workflow_path.is_file():
        errors.append(f"frozen workflow missing: {frozen['path']}")
    else:
        actual_blob = git_blob_sha(workflow_path.read_bytes())
        if actual_blob != frozen["blob_sha"]:
            errors.append(
                "frozen workflow blob changed: expected "
                f"{frozen['blob_sha']}, got {actual_blob}"
            )

    if not errors:
        completed = subprocess.run(
            ["sh", "tests/v2-public-api-alias-check.sh"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
        if completed.returncode != 0:
            errors.append(
                "canonical setup alias smoke failed:\n" + completed.stdout[-4000:]
            )
        else:
            print(completed.stdout, end="")

    if errors:
        for error in sorted(set(errors)):
            print(error)
        raise SystemExit(
            f"Public API contract failed with {len(set(errors))} issue(s)."
        )

    print(
        "N15-EVIDENCE public-api "
        f"legacy_keys={len(legacy_keys)} "
        f"canonical_keys={len(canonical_keys)} "
        f"keys={len(actual_keys)} "
        f"legacy_values={len(legacy_values)} "
        f"canonical_values={len(canonical_values)} "
        f"values={len(actual_values)} "
        f"commands={len(actual_commands)} "
        f"environments={len(actual_envs)} "
        f"hooks={len(actual_hooks)} "
        "article_runtime=false "
        f"n12_blob={frozen['blob_sha']}"
    )
    print("Public API additive contract passed.")


if __name__ == "__main__":
    main()

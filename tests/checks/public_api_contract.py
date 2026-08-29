#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / "release/n15-b2r-b-public-api.json"

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


def main() -> None:
    inventory = json.loads(read_text(INVENTORY_PATH))
    errors: list[str] = []

    if inventory.get("schema_version") != 1:
        errors.append("inventory: schema_version must be 1")
    if inventory.get("phase") != "N15-B2R-B1":
        errors.append("inventory: phase must be N15-B2R-B1")
    if inventory.get("policy", {}).get("value_identity") != "setup-key/value":
        errors.append("inventory: setup values must be scoped by setup key")

    source_paths = [ROOT / item for item in inventory["source_modules"]]
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

    expected_keys_list = flatten(inventory["setup_keys_by_source"])
    key_duplicates = duplicate_items(expected_keys_list)
    if key_duplicates:
        errors.append(
            "inventory setup keys duplicated: " + ", ".join(key_duplicates)
        )
    expected_keys = set(expected_keys_list)
    actual_keys = set(KEY_PATTERN.findall(combined))
    compare_sets("setup keys", actual_keys, expected_keys, errors)

    expected_value_ids_list = [
        f"{key}/{value}"
        for key, values in inventory["setup_values"].items()
        for value in values
    ]
    value_duplicates = duplicate_items(expected_value_ids_list)
    if value_duplicates:
        errors.append(
            "inventory setup key/value identities duplicated: "
            + ", ".join(value_duplicates)
        )
    expected_values = {
        (key, value)
        for key, values in inventory["setup_values"].items()
        for value in values
    }
    actual_values = set(VALUE_PATTERN.findall(combined))
    missing_values = sorted(expected_values - actual_values)
    extra_values = sorted(actual_values - expected_values)
    if missing_values:
        errors.append(
            "setup values missing: "
            + ", ".join(
                f"{key}/{value}" for key, value in missing_values
            )
        )
    if extra_values:
        errors.append(
            "setup values unreviewed: "
            + ", ".join(
                f"{key}/{value}" for key, value in extra_values
            )
        )

    extension_hooks = {
        item["name"] for item in inventory.get("extension_hooks", [])
    }
    expected_commands_list = flatten(inventory["commands_by_source"])
    command_duplicates = duplicate_items(expected_commands_list)
    if command_duplicates:
        errors.append(
            "inventory commands duplicated: " + ", ".join(command_duplicates)
        )
    expected_commands = set(expected_commands_list)

    upstream_command_names = {
        item["name"]
        for item in inventory.get("upstream_compatibility_surfaces", [])
        if item.get("kind") == "command"
    }
    xparse_commands = set(XPARSE_COMMAND_PATTERN.findall(combined))
    standard_ufc_commands = set(STANDARD_UFC_COMMAND_PATTERN.findall(combined))
    actual_commands = (
        xparse_commands | (standard_ufc_commands - extension_hooks)
    ) - upstream_command_names
    compare_sets("commands", actual_commands, expected_commands, errors)

    classification_items = flatten(inventory["command_classification"])
    classification_duplicates = duplicate_items(classification_items)
    if classification_duplicates:
        errors.append(
            "command classifications overlap: "
            + ", ".join(classification_duplicates)
        )
    compare_sets(
        "command classification coverage",
        set(classification_items),
        expected_commands,
        errors,
    )

    expected_envs_list = flatten(inventory["environments_by_source"])
    env_duplicates = duplicate_items(expected_envs_list)
    if env_duplicates:
        errors.append(
            "inventory environments duplicated: " + ", ".join(env_duplicates)
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

    for entrypoint in inventory["class_entrypoints"]:
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

    for surface in inventory.get("upstream_compatibility_surfaces", []):
        source = source_texts.get(surface["source"], "")
        token = surface["name"]
        if token not in source:
            errors.append(
                "upstream compatibility surface missing: "
                f"{surface['source']}:{token}"
            )

    canonical_key_map = inventory.get("canonical_setup_key_map", {})
    unknown_mapped_keys = sorted(set(canonical_key_map) - expected_keys)
    if unknown_mapped_keys:
        errors.append(
            "canonical setup key map references unknown keys: "
            + ", ".join(unknown_mapped_keys)
        )
    duplicate_canonical_keys = duplicate_items(list(canonical_key_map.values()))
    if duplicate_canonical_keys:
        errors.append(
            "canonical setup key names duplicated: "
            + ", ".join(duplicate_canonical_keys)
        )

    canonical_command_map = inventory.get("canonical_command_map", {})
    unknown_mapped_commands = sorted(
        set(canonical_command_map) - expected_commands
    )
    if unknown_mapped_commands:
        errors.append(
            "canonical command map references unknown commands: "
            + ", ".join(unknown_mapped_commands)
        )
    duplicate_canonical_commands = duplicate_items(
        list(canonical_command_map.values())
    )
    if duplicate_canonical_commands:
        errors.append(
            "canonical command names duplicated: "
            + ", ".join(duplicate_canonical_commands)
        )

    for item in inventory.get("reserved_future_surfaces", []):
        if item.get("canonical") == "type=article":
            if "type" in actual_keys or ("tipo", "artigo") in actual_values:
                errors.append(
                    "article naming surface became live during B2R-B1; "
                    "reserve runtime/API activation for the reviewed later step"
                )

    expected_counts = inventory["expected_counts"]
    actual_counts = {
        "class_entrypoints": len(inventory["class_entrypoints"]),
        "setup_keys": len(actual_keys),
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

    frozen = inventory["policy"]["frozen_workflow"]
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

    if errors:
        for error in sorted(set(errors)):
            print(error)
        raise SystemExit(
            f"Public API contract failed with {len(set(errors))} issue(s)."
        )

    print(
        "N15-EVIDENCE public-api "
        f"keys={len(actual_keys)} "
        f"values={len(actual_values)} "
        f"commands={len(actual_commands)} "
        f"environments={len(actual_envs)} "
        f"hooks={len(actual_hooks)} "
        "value_identity=setup-key/value "
        "article_runtime=false "
        f"n12_blob={frozen['blob_sha']}"
    )
    print("Public API baseline contract passed.")


if __name__ == "__main__":
    main()

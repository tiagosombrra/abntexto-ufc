#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "normativa" / "catalog.json"


class CatalogError(ValueError):
    pass


def load_catalog(path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError(f"cannot load normative catalog: {exc}") from exc
    validate_catalog(data)
    return data


def validate_catalog(data: dict[str, Any]) -> None:
    if data.get("schema_version") != 1:
        raise CatalogError("unsupported schema_version")

    sources = data.get("sources")
    rules = data.get("rules")
    policy = data.get("policy")
    if not isinstance(sources, list) or not sources:
        raise CatalogError("sources must be a non-empty list")
    if not isinstance(rules, list) or not rules:
        raise CatalogError("rules must be a non-empty list")
    if not isinstance(policy, dict) or not policy.get("precedence"):
        raise CatalogError("policy.precedence is required")

    source_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise CatalogError("every source must be an object")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise CatalogError("every source requires a non-empty id")
        if source_id in source_ids:
            raise CatalogError(f"duplicate source id: {source_id}")
        source_ids.add(source_id)
        for field in ("kind", "title", "publisher", "status", "checked_at"):
            if not source.get(field):
                raise CatalogError(f"source {source_id}: missing {field}")

    rule_ids: set[str] = set()
    allowed_modes = {
        "automatic",
        "automatic-deep",
        "automatic-partial",
        "automatic-policy",
        "manual",
        "conditional-manual",
    }
    for rule in rules:
        if not isinstance(rule, dict):
            raise CatalogError("every rule must be an object")
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id:
            raise CatalogError("every rule requires a non-empty id")
        if rule_id in rule_ids:
            raise CatalogError(f"duplicate rule id: {rule_id}")
        rule_ids.add(rule_id)

        for field in ("category", "requirement", "locator", "normativity", "kind"):
            if not rule.get(field):
                raise CatalogError(f"rule {rule_id}: missing {field}")

        refs = rule.get("sources")
        if not isinstance(refs, list) or not refs:
            raise CatalogError(f"rule {rule_id}: sources must be non-empty")
        unknown = sorted(set(refs) - source_ids)
        if unknown:
            raise CatalogError(f"rule {rule_id}: unknown sources: {', '.join(unknown)}")

        values = rule.get("values")
        if not isinstance(values, dict):
            raise CatalogError(f"rule {rule_id}: values must be an object")

        validation = rule.get("validation")
        if not isinstance(validation, dict):
            raise CatalogError(f"rule {rule_id}: validation must be an object")
        mode = validation.get("mode")
        if mode not in allowed_modes:
            raise CatalogError(f"rule {rule_id}: invalid validation mode: {mode}")
        checks = validation.get("checks")
        if not isinstance(checks, list) or not checks:
            raise CatalogError(f"rule {rule_id}: validation.checks must be non-empty")


def source_map(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {source["id"]: source for source in catalog["sources"]}


def rule_map(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {rule["id"]: rule for rule in catalog["rules"]}


def get_rule(catalog: dict[str, Any], rule_id: str) -> dict[str, Any]:
    try:
        return rule_map(catalog)[rule_id]
    except KeyError as exc:
        raise CatalogError(f"unknown normative rule: {rule_id}") from exc


def source_label(catalog: dict[str, Any], rule: dict[str, Any]) -> str:
    sources = source_map(catalog)
    return " / ".join(sources[source_id]["title"] for source_id in rule["sources"])


def emit_web_module(catalog: dict[str, Any], output: Path) -> None:
    payload = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "// Generated from normativa/catalog.json.\n"
        f"export const normativeCatalog={payload};\n"
        "export const normativeRules=Object.fromEntries(normativeCatalog.rules.map(rule=>[rule.id,rule]));\n"
        "export const normativeSources=Object.fromEntries(normativeCatalog.sources.map(source=>[source.id,source]));\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and export the UFC normative catalog.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--emit-web", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    catalog = load_catalog(args.catalog)
    if args.emit_web:
        emit_web_module(catalog, args.emit_web)
    print(
        f"Normative catalog valid: {len(catalog['sources'])} sources, "
        f"{len(catalog['rules'])} rules, reviewed {catalog['reviewed_at']}."
    )


if __name__ == "__main__":
    main()

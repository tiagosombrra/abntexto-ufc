#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
NORMATIVE = ROOT / "standards"
SOURCE_AUDIT = NORMATIVE / "source-audit.json"

REFERENCE_LIST_KEYS = {
    "candidate_sources",
    "constraint_sources",
    "current_technical_sources",
    "governing_sources",
    "supporting_sources",
}


def fail(message: str) -> None:
    raise SystemExit(f"Normative source reference integrity failed: {message}")


def source_ids() -> set[str]:
    data = json.loads(SOURCE_AUDIT.read_text(encoding="utf-8"))
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("source-audit.json sources must be a non-empty list")

    ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            fail("source-audit.json contains a non-object source record")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            fail("source-audit.json contains a source without a valid id")
        if source_id in ids:
            fail(f"duplicate source id in source-audit.json: {source_id}")
        ids.add(source_id)
    return ids


def iter_references(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}.{key}"
            if key == "sources" and isinstance(item, list) and all(
                isinstance(ref, str) for ref in item
            ):
                for ref in item:
                    yield item_path, ref
                continue
            if key in REFERENCE_LIST_KEYS and isinstance(item, list):
                if not all(isinstance(ref, str) for ref in item):
                    fail(f"{item_path} must contain only source ids")
                for ref in item:
                    yield item_path, ref
                continue
            if key == "source" and isinstance(item, str):
                yield item_path, item
                continue
            if key == "citation_standard" and isinstance(item, str):
                yield item_path, item
                continue
            yield from iter_references(item, item_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_references(item, f"{path}[{index}]")


def main() -> None:
    registry = source_ids()
    checked = 0
    unknown: list[str] = []

    for json_path in sorted(NORMATIVE.glob("*.json")):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        for location, source_id in iter_references(data):
            checked += 1
            if source_id not in registry:
                unknown.append(f"{json_path.name}:{location} -> {source_id}")

    if unknown:
        fail("unknown source ids: " + "; ".join(unknown))

    print(
        "Normative source reference integrity passed: "
        f"{checked} references resolve against {len(registry)} registered sources."
    )


if __name__ == "__main__":
    main()

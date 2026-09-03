#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "release/v3-api-migration.json"
CLASS = ROOT / "abntexto-ufc.cls"
REMOVED_LAYER = ROOT / "abntexto-ufc/public-api.def"
ACTIVE_ROOTS = (
    ROOT / "abntexto-ufc",
    ROOT / "template",
    ROOT / "tests/documents",
    ROOT / "tests/fixtures",
)
ACTIVE_FILES = (
    ROOT / "docs/ctan-example.tex",
    ROOT / "docs/ctan-manual.tex",
)
TEXT_SUFFIXES = {".tex", ".def", ".cls", ".sty"}


def fail(message: str) -> None:
    raise SystemExit(f"V3 API residual check failed: {message}")


def tracked_paths() -> set[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.decode("utf-8", errors="replace").strip() or "git ls-files failed")
    return {
        ROOT / item.decode("utf-8")
        for item in completed.stdout.split(b"\0")
        if item
    }


def active_sources(tracked: set[Path]) -> list[Path]:
    paths: set[Path] = set()
    for root in ACTIVE_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in TEXT_SUFFIXES and path in tracked:
                paths.add(path)
    for path in ACTIVE_FILES:
        if path.is_file() and path in tracked:
            paths.add(path)
    return sorted(paths)


def command_pattern(command: str) -> re.Pattern[str]:
    return re.compile(re.escape(command) + r"(?![A-Za-z@:_])")


def main() -> None:
    tracked = tracked_paths()
    if REMOVED_LAYER in tracked or REMOVED_LAYER.exists():
        fail("abntexto-ufc/public-api.def must be absent after R2-B5")

    class_text = CLASS.read_text(encoding="utf-8")
    if "public-api.def" in class_text:
        fail("abntexto-ufc.cls still loads the removed forwarding layer")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    removed_commands = sorted(contract["removed_portuguese_commands"])
    removed_environments = sorted(contract["public_environments"]["removed"])
    removed_hooks = sorted(contract["extension_hooks"])
    legacy_keys = {
        old: new
        for old, new in contract["legacy_setup_key_to_v3"].items()
        if old != new
    }
    legacy_values = {
        old: new
        for old, new in contract["legacy_setup_value_to_v3"].items()
        if old != new
    }

    violations: list[str] = []
    command_patterns = [(name, command_pattern(name)) for name in removed_commands]
    hook_patterns = [(name, command_pattern(name)) for name in removed_hooks]
    environment_patterns = [
        (name, re.compile(r"\\(?:begin|end)\s*\{\s*" + re.escape(name) + r"\s*\}"))
        for name in removed_environments
    ]
    setup_key_patterns = [
        (old, new, re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"\s*="))
        for old, new in sorted(legacy_keys.items())
    ]
    setup_value_patterns = [
        (
            old,
            new,
            re.compile(
                r"=\s*(?:\{\s*)?" + re.escape(old) + r"(?:\s*\})?\s*(?=[,}\n])"
            ),
        )
        for old, new in sorted(legacy_values.items())
    ]
    object_id_patterns = [
        ("codigo", re.compile(r"\\(?:legend|definelegendplace)\s*\{\s*codigo\s*\}")),
        ("algoritmo", re.compile(r"\\(?:legend|definelegendplace)\s*\{\s*algoritmo\s*\}")),
    ]

    for path in active_sources(tracked):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for name, pattern in command_patterns + hook_patterns:
            if pattern.search(text):
                violations.append(f"{relative}: removed project command/hook {name}")
        for name, pattern in environment_patterns:
            if pattern.search(text):
                violations.append(f"{relative}: removed project environment {name}")
        for old, new, pattern in setup_key_patterns:
            if pattern.search(text):
                violations.append(f"{relative}: legacy setup key {old} -> {new}")
        for old, new, pattern in setup_value_patterns:
            if pattern.search(text):
                violations.append(f"{relative}: legacy setup value {old} -> {new}")
        for old, pattern in object_id_patterns:
            if pattern.search(text):
                violations.append(f"{relative}: project-owned legacy object id {old}")

    if violations:
        fail("\n" + "\n".join(sorted(set(violations))))

    print(
        "V3-API-RESIDUAL-EVIDENCE status=PASS "
        f"active_sources={len(active_sources(tracked))} "
        f"removed_commands={len(removed_commands)} "
        f"removed_environments={len(removed_environments)} "
        f"removed_hooks={len(removed_hooks)} "
        f"legacy_setup_keys={len(legacy_keys)} legacy_setup_values={len(legacy_values)} "
        "forwarding_layer=absent runtime_aliases=0"
    )


if __name__ == "__main__":
    main()

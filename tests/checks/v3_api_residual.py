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
LATEX_ROOTS = (
    ROOT / "abntexto-ufc",
    ROOT / "template",
    ROOT / "tests/documents",
    ROOT / "tests/fixtures",
)
LATEX_FILES = (
    ROOT / "docs/ctan-example.tex",
    ROOT / "docs/ctan-manual.tex",
)
LATEX_SUFFIXES = {".tex", ".def", ".cls", ".sty"}
ENGINEERING_ROOTS = (
    ROOT / "tests/checks",
    ROOT / "tests/integration",
    ROOT / "tools",
    ROOT / "validator",
    ROOT / ".github/workflows",
)
ENGINEERING_FILES = (
    ROOT / "tests/run.py",
    ROOT / "tests/static.py",
    ROOT / "Makefile",
)
ENGINEERING_SUFFIXES = {".py", ".sh", ".ps1", ".js", ".json", ".yml", ".yaml"}
ENGINEERING_EXEMPT = {
    ROOT / "tests/checks/v3_api_residual.py",
}


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


def collect_sources(
    tracked: set[Path],
    roots: tuple[Path, ...],
    files: tuple[Path, ...],
    suffixes: set[str],
    exempt: set[Path] | None = None,
) -> list[Path]:
    excluded = exempt or set()
    paths: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if (
                path.is_file()
                and path in tracked
                and path not in excluded
                and (path.suffix in suffixes or path.name == "Makefile")
            ):
                paths.add(path)
    for path in files:
        if path.is_file() and path in tracked and path not in excluded:
            paths.add(path)
    return sorted(paths)


def command_pattern(command: str) -> re.Pattern[str]:
    return re.compile(re.escape(command) + r"(?![A-Za-z@:_])")


def engineering_key_pattern(key: str) -> re.Pattern[str]:
    # Engineering sources may legitimately use Portuguese variable names until R3-B4.
    # B3 rejects a legacy setup key only when it appears inside a quoted assignment-like
    # payload that can affect generated/runtime LaTeX.
    return re.compile(
        r"(?:['\"])"
        r"[^'\"\n]{0,240}"
        + re.escape(key)
        + r"\s*="
    )


def engineering_value_pattern(value: str) -> re.Pattern[str]:
    # Legacy document-type values are API residue only when assigned to the canonical
    # or retired setup key, not when retained as scenario labels owned by R3-B4.
    return re.compile(
        r"(?<![A-Za-z0-9_-])(?:type|tipo)\s*=\s*(?:\{\s*)?"
        + re.escape(value)
        + r"(?:\s*\})?\s*(?=[,}\n'\"])",
        flags=re.IGNORECASE,
    )


def scan_source(
    path: Path,
    text: str,
    *,
    command_patterns: list[tuple[str, re.Pattern[str]]],
    hook_patterns: list[tuple[str, re.Pattern[str]]],
    environment_patterns: list[tuple[str, re.Pattern[str]]],
    setup_key_patterns: list[tuple[str, str, re.Pattern[str]]],
    setup_value_patterns: list[tuple[str, str, re.Pattern[str]]],
    object_id_patterns: list[tuple[str, re.Pattern[str]]],
) -> list[str]:
    relative = path.relative_to(ROOT)
    violations: list[str] = []
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
    return violations


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

    command_patterns = [(name, command_pattern(name)) for name in removed_commands]
    hook_patterns = [(name, command_pattern(name)) for name in removed_hooks]
    environment_patterns = [
        (name, re.compile(r"\\(?:begin|end)\s*\{\s*" + re.escape(name) + r"\s*\}"))
        for name in removed_environments
    ]
    latex_setup_key_patterns = [
        (old, new, re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"\s*="))
        for old, new in sorted(legacy_keys.items())
    ]
    latex_setup_value_patterns = [
        (
            old,
            new,
            re.compile(
                r"=\s*(?:\{\s*)?" + re.escape(old) + r"(?:\s*\})?\s*(?=[,}\n])"
            ),
        )
        for old, new in sorted(legacy_values.items())
    ]
    engineering_setup_key_patterns = [
        (old, new, engineering_key_pattern(old))
        for old, new in sorted(legacy_keys.items())
    ]
    engineering_setup_value_patterns = [
        (old, new, engineering_value_pattern(old))
        for old, new in sorted(legacy_values.items())
    ]
    object_id_patterns = [
        ("codigo", re.compile(r"\\(?:legend|definelegendplace)\s*\{\s*codigo\s*\}")),
        ("algoritmo", re.compile(r"\\(?:legend|definelegendplace)\s*\{\s*algoritmo\s*\}")),
    ]

    latex_sources = collect_sources(tracked, LATEX_ROOTS, LATEX_FILES, LATEX_SUFFIXES)
    engineering_sources = collect_sources(
        tracked,
        ENGINEERING_ROOTS,
        ENGINEERING_FILES,
        ENGINEERING_SUFFIXES,
        ENGINEERING_EXEMPT,
    )

    violations: list[str] = []
    for path in latex_sources:
        violations.extend(
            scan_source(
                path,
                path.read_text(encoding="utf-8"),
                command_patterns=command_patterns,
                hook_patterns=hook_patterns,
                environment_patterns=environment_patterns,
                setup_key_patterns=latex_setup_key_patterns,
                setup_value_patterns=latex_setup_value_patterns,
                object_id_patterns=object_id_patterns,
            )
        )
    for path in engineering_sources:
        violations.extend(
            scan_source(
                path,
                path.read_text(encoding="utf-8"),
                command_patterns=command_patterns,
                hook_patterns=hook_patterns,
                environment_patterns=environment_patterns,
                setup_key_patterns=engineering_setup_key_patterns,
                setup_value_patterns=engineering_setup_value_patterns,
                object_id_patterns=object_id_patterns,
            )
        )

    if violations:
        fail("\n" + "\n".join(sorted(set(violations))))

    print(
        "V3-API-RESIDUAL-EVIDENCE status=PASS "
        f"latex_sources={len(latex_sources)} engineering_sources={len(engineering_sources)} "
        f"total_sources={len(latex_sources) + len(engineering_sources)} "
        f"removed_commands={len(removed_commands)} "
        f"removed_environments={len(removed_environments)} "
        f"removed_hooks={len(removed_hooks)} "
        f"legacy_setup_keys={len(legacy_keys)} legacy_setup_values={len(legacy_values)} "
        "forwarding_layer=absent runtime_aliases=0"
    )


if __name__ == "__main__":
    main()

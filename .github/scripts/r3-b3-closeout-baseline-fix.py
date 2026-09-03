#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_MAIN = "fbee5bd329f98a389c2880932af40547c8d1674e"

TEXT_FILES = [
    "README.md",
    "AGENTS.md",
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "docs/R3-HARDENING-INVENTORY.md",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
    "docs/CTAN-RELEASE.md",
]

REPLACEMENTS = [
    ("134 LaTeX and 169 behavior-affecting engineering sources (303 total)", "134 LaTeX and 168 behavior-affecting engineering sources (302 total)"),
    ("303 behavior-relevant sources (134 LaTeX + 169 engineering)", "302 behavior-relevant sources (134 LaTeX + 168 engineering)"),
    ("303 residual-scanned sources (134 LaTeX + 169 engineering)", "302 residual-scanned sources (134 LaTeX + 168 engineering)"),
    ("303-source residual gate", "302-source residual gate"),
    ("134 LaTeX + 169 engineering = 303 sources", "134 LaTeX + 168 engineering = 302 sources"),
    ("covers 303 behavior-relevant sources", "covers 302 behavior-relevant sources"),
    ("residual gate covers 303 sources", "residual gate covers 302 sources"),
    ("Residual enforcement covers 134 LaTeX plus 169 behavior-affecting engineering sources", "Residual enforcement covers 134 LaTeX plus 168 behavior-affecting engineering sources"),
]


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def patch_text_files() -> int:
    changed = 0
    for rel in TEXT_FILES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def patch_json(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0

    def walk(node):
        nonlocal changed
        if isinstance(node, dict):
            residual = node.get("residual_sources")
            if isinstance(residual, dict) and residual.get("latex") == 134 and residual.get("engineering") == 169 and residual.get("total") == 303:
                residual["engineering"] = 168
                residual["total"] = 302
                changed += 1
            for key, value in list(node.items()):
                if isinstance(value, str):
                    new_value = value
                    for old, new in REPLACEMENTS:
                        new_value = new_value.replace(old, new)
                    if new_value != value:
                        node[key] = new_value
                        changed += 1
                else:
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def assert_no_permanent_303_claims() -> None:
    patterns = [
        "169 behavior-affecting engineering sources (303 total)",
        "303 behavior-relevant sources (134 LaTeX + 169 engineering)",
        "303 residual-scanned sources (134 LaTeX + 169 engineering)",
        "303-source residual gate",
        "134 LaTeX + 169 engineering = 303 sources",
    ]
    for rel in TEXT_FILES + ["release/v3-roadmap.json", "release/v3-r3-inventory.json"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for pattern in patterns:
            if pattern in text:
                raise SystemExit(f"{rel}: stale permanent residual baseline: {pattern}")


def main() -> None:
    run("git", "fetch", "origin", "main")
    if run("git", "rev-parse", "origin/main") != EXPECTED_MAIN:
        raise SystemExit("origin/main moved; stop fail-closed")

    text_changed = patch_text_files()
    json_changes = patch_json(ROOT / "release/v3-roadmap.json") + patch_json(ROOT / "release/v3-r3-inventory.json")
    if text_changed == 0 and json_changes == 0:
        raise SystemExit("no residual-baseline repair was applied")

    assert_no_permanent_303_claims()

    subprocess.check_call(["git", "rm", ".github/scripts/r3-b3-closeout-baseline-fix.py", ".github/workflows/r3-b3-closeout-baseline-fix.yml"], cwd=ROOT)
    subprocess.check_call(["make", "static-check"], cwd=ROOT)
    subprocess.check_call(["git", "diff", "--check"], cwd=ROOT)

    subprocess.check_call(["git", "add", *TEXT_FILES, "release/v3-roadmap.json", "release/v3-r3-inventory.json"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT)
    subprocess.check_call(["git", "commit", "-m", "docs: align B3 residual baseline with permanent gate"], cwd=ROOT)
    subprocess.check_call(["git", "push", "origin", "HEAD"], cwd=ROOT)


if __name__ == "__main__":
    main()

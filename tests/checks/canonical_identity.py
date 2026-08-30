#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASS = ROOT / "abntexto-ufc.cls"
MODULE_RE = re.compile(r"\\input\{(abntexto-ufc/[^}]+\.def)\}")
LEGACY_CLASS_MESSAGE_RE = re.compile(
    r"\\Class(?:Info|Error|Warning|WarningNoLine)\{ufctex\}"
)
LEGACY_IDENTITY_RE = re.compile(
    r"(?<![A-Za-z0-9])ufctex(?![A-Za-z0-9])", re.IGNORECASE
)
TEXT_SUFFIXES = {
    ".bib",
    ".cls",
    ".def",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".tex",
    ".txt",
    ".yaml",
    ".yml",
}
LEGACY_FULL_FILE_EXEMPT = {
    "ufctex.cls",
    "docs/CHANGELOG-CTAN.md",
    "tests/v2-build-path-check.sh",
    "tests/v2-canonical-identity-check.py",
    "tests/v2-ctan-archive-check.py",
    "tests/v2-ctan-policy-check.py",
    "tests/v2-distribution-check.sh",
    "tests/v2-overleaf-bundle-check.py",
    "tests/v2-release-metadata-check.py",
    "tests/v2-release-package-check.py",
    "tests/v2-repository-audit.py",
    "tools/build-release-bundles.py",
}
LEGACY_FULL_DIRECTORY_EXEMPT = (
    "docs/history/",
)
LEGACY_DOCUMENTATION_EXEMPT = {
    "README.md": (
        re.compile(r"ufctex\.cls.*(?:shim|compat)", re.IGNORECASE),
        re.compile(r"\\documentclass\{ufctex\}"),
    ),
    "docs/README-CTAN.md": (
        re.compile(r"ufctex.*(?:deprecated|compat)", re.IGNORECASE),
    ),
    "release/n15-b2r-b-public-api.json": (
        re.compile(r'^\s*"name"\s*:\s*"ufctex"\s*,?\s*$'),
        re.compile(r'^\s*"file"\s*:\s*"ufctex\.cls"\s*,?\s*$'),
    ),
}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT}", "ls-files", "-z"], cwd=ROOT
    )
    return [ROOT / item.decode("utf-8") for item in output.split(b"\0") if item]


def is_text(path: Path) -> bool:
    return path.name in {"Makefile", "LICENSE"} or path.suffix.lower() in TEXT_SUFFIXES


def audit_global_identity(errors: list[str]) -> None:
    for path in tracked_files():
        if not is_text(path):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in LEGACY_FULL_FILE_EXEMPT:
            continue
        if relative.startswith(LEGACY_FULL_DIRECTORY_EXEMPT):
            continue

        text = path.read_text(encoding="utf-8", errors="strict")
        allowed = LEGACY_DOCUMENTATION_EXEMPT.get(relative, ())
        for line_number, line in enumerate(text.splitlines(), 1):
            if not LEGACY_IDENTITY_RE.search(line):
                continue
            if any(pattern.search(line) for pattern in allowed):
                continue
            errors.append(
                f"{relative}:{line_number}: unclassified legacy ufctex identity: {line.strip()}"
            )


def main() -> None:
    errors: list[str] = []
    class_text = CLASS.read_text(encoding="utf-8")

    if "\\input{ufctex/" in class_text:
        errors.append("abntexto-ufc.cls: canonical class loads the legacy module namespace")

    modules = MODULE_RE.findall(class_text)
    if not modules:
        errors.append("abntexto-ufc.cls: no canonical modules found")

    if len(modules) != len(set(modules)):
        errors.append("abntexto-ufc.cls: duplicate canonical module input")

    for module in modules:
        path = ROOT / module
        if not path.is_file():
            errors.append(f"{module}: loaded canonical module does not exist")
            continue

        text = path.read_text(encoding="utf-8")
        expected = f"\\ProvidesFile{{{module}}}"
        if expected not in text:
            errors.append(f"{module}: expected {expected}")
        if "\\ProvidesFile{ufctex/" in text:
            errors.append(f"{module}: legacy ProvidesFile identity")
        if LEGACY_CLASS_MESSAGE_RE.search(text):
            errors.append(f"{module}: legacy ufctex class-message identity")

    normas = (ROOT / "docs/NORMAS.md").read_text(encoding="utf-8")
    if "`ufctex/" in normas:
        errors.append("docs/NORMAS.md: legacy module path remains in CTAN documentation")

    audit_global_identity(errors)

    if errors:
        for error in errors:
            print(error)
        legacy_counts = Counter(
            error.split(":", 1)[0]
            for error in errors
            if "unclassified legacy ufctex identity" in error
        )
        if legacy_counts:
            compact = ", ".join(
                f"{filename}={count}" for filename, count in sorted(legacy_counts.items())
            )
            print(f"LEGACY_FILES {compact}")
        raise SystemExit(f"Canonical identity check failed with {len(errors)} issue(s).")

    print(f"Canonical identity check passed: {len(modules)} modules aligned.")


if __name__ == "__main__":
    main()

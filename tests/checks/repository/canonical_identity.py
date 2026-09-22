#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from collections import Counter
import sys
from pathlib import Path

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from path_resolver import ROOT  # noqa: E402
CLASS = ROOT / "abntexto-ufc.cls"
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
    # Current migration/control records legitimately identify the removed
    # legacy entrypoint while documenting its retirement.
    "release/history/v3/v3-api-migration.json",
    "docs/MIGRATING-TO-V3.md",

    # Negative assertions must name the legacy entrypoint to reject it.
    "tests/checks/repository/canonical_identity.py",
    "tests/checks/repository/repository_contract.py",
    "tests/checks/distribution/distribution_bundles.py",
    "tests/integration/distribution-bundles.sh",
    "tools/build-distribution-bundles.py",
}
LEGACY_FULL_DIRECTORY_EXEMPT = ("release/history/v3/",)
LEGACY_DOCUMENTATION_EXEMPT = {
    "docs/ARCHITECTURE.md": (
        re.compile(
            r"does not ship `ufctex\.cls`",
            re.IGNORECASE,
        ),
    ),
    # Release-control documentation may identify the rejected historical
    # package id only when recording the migration/publication response.
    "docs/CTAN-RELEASE.md": (
        re.compile(r"earlier `ufctex` submission", re.IGNORECASE),
        re.compile(r"deprecated `ufctex` wording", re.IGNORECASE),
        re.compile(r"previously attempted `ufctex` package name", re.IGNORECASE),
    ),
    "docs/history/v3/control/HANDOFF-V3.0.0.md": (
        re.compile(r"previous `ufctex` identity is replaced", re.IGNORECASE),
    ),
    "docs/history/v3/control/ROADMAP-V3.0.0.md": (
        re.compile(r"deprecated `ufctex` identity", re.IGNORECASE),
    ),
    "docs/history/v3/control/V3-CONTINUATION.md": (
        re.compile(r"stale `ufctex`", re.IGNORECASE),
    ),
    "docs/history/v3/release/V3-RELEASE-READINESS.md": (
        re.compile(r"replaces historical/deprecated `ufctex` identity", re.IGNORECASE),
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

    if class_text.count(r"\ProvidesClass{abntexto-ufc}") != 1:
        errors.append("abntexto-ufc.cls: canonical class identity must be declared exactly once")
    if re.search(r"\\input\{abntexto-ufc/[^}]+\.def\}", class_text):
        errors.append("abntexto-ufc.cls: canonical class still loads a project-owned .def module")
    if re.search(r"\\ProvidesFile\{abntexto-ufc/", class_text):
        errors.append("abntexto-ufc.cls: canonical class still contains project-module wrappers")
    if "\\input{ufctex/" in class_text:
        errors.append("abntexto-ufc.cls: canonical class loads the legacy module namespace")
    if not class_text.rstrip().endswith(r"\endinput"):
        errors.append("abntexto-ufc.cls: canonical class must terminate with \\endinput")

    runtime_paths = sorted(
        path.relative_to(ROOT).as_posix()
        for path in tracked_files()
        if path.relative_to(ROOT).as_posix().startswith("abntexto-ufc/")
    )
    if runtime_paths:
        errors.append(
            "legacy modular runtime paths remain tracked: " + ", ".join(runtime_paths)
        )

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

    print("Canonical identity check passed: single tracked abntexto-ufc.cls runtime.")




if __name__ == "__main__":
    main()

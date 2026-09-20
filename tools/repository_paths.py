#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARDS_ROOT = ROOT / "standards"


class RepositoryPathError(RuntimeError):
    pass


def unique_file(root: Path, filename: str) -> Path:
    matches = sorted(path for path in root.rglob(filename) if path.is_file())
    if not matches:
        raise RepositoryPathError(
            f"required repository file {filename!r} not found under {root.relative_to(ROOT)}"
        )
    if len(matches) != 1:
        rendered = ", ".join(path.relative_to(ROOT).as_posix() for path in matches)
        raise RepositoryPathError(f"ambiguous repository file identity {filename!r}: {rendered}")
    return matches[0]


def standard_file(filename: str) -> Path:
    return unique_file(STANDARDS_ROOT, filename)


def standard_files(pattern: str) -> list[Path]:
    matches = sorted(path for path in STANDARDS_ROOT.rglob(pattern) if path.is_file())
    if not matches:
        raise RepositoryPathError(f"no standards files match {pattern!r}")
    return matches

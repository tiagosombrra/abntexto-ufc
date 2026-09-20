#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS_ROOT = ROOT / "tests" / "checks"
INTEGRATION_ROOT = ROOT / "tests" / "integration"


class PathResolutionError(RuntimeError):
    pass


def _unique_file(root: Path, filename: str) -> Path:
    matches = sorted(path for path in root.rglob(filename) if path.is_file())
    if not matches:
        raise PathResolutionError(f"required file {filename!r} not found under {root.relative_to(ROOT)}")
    if len(matches) != 1:
        rendered = ", ".join(path.relative_to(ROOT).as_posix() for path in matches)
        raise PathResolutionError(f"ambiguous file identity {filename!r}: {rendered}")
    return matches[0]


def check_file(filename: str) -> Path:
    return _unique_file(CHECKS_ROOT, filename)


def integration_file(filename: str) -> Path:
    return _unique_file(INTEGRATION_ROOT, filename)


def repository_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

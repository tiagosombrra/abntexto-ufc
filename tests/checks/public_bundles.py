#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ID = "abntexto-ufc"
UPSTREAM_MARKER = b"[2026-05-08 1.1 Preparation of works in ABNT standards]"
MICROSOFT_FONTS = {
    "times.ttf",
    "timesbd.ttf",
    "timesi.ttf",
    "timesbi.ttf",
    "arial.ttf",
    "arialbd.ttf",
    "ariali.ttf",
    "arialbi.ttf",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def version() -> str:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        fail("Makefile VERSION not found.")
    return match.group(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive_entries(path: Path) -> dict[str, zipfile.ZipInfo]:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        fail(f"Duplicate archive entries in {path.name}.")
    for name in names:
        pure = PurePosixPath(name)
        if not name or pure.is_absolute() or ".." in pure.parts:
            fail(f"Unsafe archive path in {path.name}: {name}")
    return {info.filename: info for info in infos}


def require(entries: dict[str, zipfile.ZipInfo], required: set[str], archive_name: str) -> None:
    missing = sorted(required - entries.keys())
    if missing:
        fail(f"{archive_name} missing required entries: {', '.join(missing)}")


def reject_forbidden(entries: dict[str, zipfile.ZipInfo], archive_name: str) -> None:
    forbidden_prefixes = (
        ".github/",
        "assets/institutional/",
        "docs/",
        "release/",
        "standards/",
        "tests/",
        "tools/",
        "validator/",
    )
    forbidden_names = {"Makefile", ".gitignore"}
    for name in entries:
        normalized = name.lstrip("./")
        parts = PurePosixPath(normalized).parts
        if any(part.lower() in MICROSOFT_FONTS for part in parts):
            fail(f"{archive_name} contains a proprietary Microsoft font: {name}")
        if normalized in forbidden_names or normalized.startswith(forbidden_prefixes):
            fail(f"{archive_name} contains a development-only path: {name}")
        if "assets/institutional/" in normalized:
            fail(f"{archive_name} redistributes an institutional asset path: {name}")


def assert_public_main(archive_path: Path, entry: str) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        text = archive.read(entry).decode("utf-8")
    enabled = "  coat-of-arms = true,"
    disabled = "  coat-of-arms = false,"
    if text.count(disabled) != 1:
        fail(f"{archive_path.name}: distributed main.tex must disable the institutional mark exactly once using the canonical v3 setup key.")
    if enabled in text:
        fail(f"{archive_path.name}: distributed main.tex still enables the institutional mark.")
    legacy_tokens = ("  brasao = sim,", "  brasao = nao,")
    if any(token in text for token in legacy_tokens):
        fail(f"{archive_path.name}: distributed main.tex contains a removed v2 coat-of-arms setup key.")


def assert_upstream(archive_path: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        content = archive.read("abntexto.cls")
    if UPSTREAM_MARKER not in content:
        fail(f"{archive_path.name}: pinned upstream abntexto identity marker missing.")


def validate_template(path: Path, v: str) -> None:
    entries = archive_entries(path)
    prefix = f"{PACKAGE_ID}-template-{v}/"
    if any(not name.startswith(prefix) for name in entries):
        fail(f"{path.name}: every template entry must be rooted at {prefix}")
    required = {
        f"{prefix}main.tex",
        f"{prefix}abntexto-ufc.cls",
        f"{prefix}abntexto-ufc/core.def",
        f"{prefix}abntexto-ufc/public-api.def",
        f"{prefix}frontmatter/abstract.tex",
        f"{prefix}chapters/1-introduction.tex",
        f"{prefix}backmatter/references.bib",
        f"{prefix}figures/LICENSES.md",
        f"{prefix}figures/ufc-campus-pici.jpg",
        f"{prefix}figures/ufc-reitoria.jpg",
        f"{prefix}LICENSE",
    }
    require(entries, required, path.name)
    if f"{prefix}abntexto.cls" in entries:
        fail(f"{path.name}: standard template bundle must not vendor abntexto.cls.")
    stripped = {name[len(prefix):]: info for name, info in entries.items()}
    reject_forbidden(stripped, path.name)
    assert_public_main(path, f"{prefix}main.tex")


def validate_overleaf(path: Path) -> None:
    entries = archive_entries(path)
    required = {
        "main.tex",
        "abntexto.cls",
        "abntexto-ufc.cls",
        "abntexto-ufc/core.def",
        "abntexto-ufc/public-api.def",
        "frontmatter/abstract.tex",
        "chapters/1-introduction.tex",
        "backmatter/references.bib",
        "figures/LICENSES.md",
        "figures/ufc-campus-pici.jpg",
        "figures/ufc-reitoria.jpg",
        "LICENSE",
    }
    require(entries, required, path.name)
    if any(name.startswith(f"{PACKAGE_ID}-overleaf-") for name in entries):
        fail(f"{path.name}: Overleaf import must place main.tex at archive root.")
    reject_forbidden(entries, path.name)
    assert_public_main(path, "main.tex")
    assert_upstream(path)


def build(output: Path, upstream: Path) -> None:
    subprocess.check_call(
        [
            sys.executable,
            str(ROOT / "tools" / "build-public-bundles.py"),
            "--output",
            str(output),
            "--abntexto",
            str(upstream),
        ],
        cwd=ROOT,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate deterministic v3 public bundle structure and reproducibility.")
    parser.add_argument("--abntexto", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.abntexto.resolve()
    if not upstream.is_file():
        fail(f"Pinned upstream class not found: {upstream}")

    v = version()
    template_name = f"{PACKAGE_ID}-template-{v}.zip"
    overleaf_name = f"{PACKAGE_ID}-overleaf-{v}.zip"

    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-public-bundles-") as temp:
        root = Path(temp)
        first = root / "first"
        second = root / "second"
        build(first, upstream)
        build(second, upstream)

        expected = {template_name, overleaf_name}
        first_names = {path.name for path in first.iterdir() if path.is_file()}
        second_names = {path.name for path in second.iterdir() if path.is_file()}
        if first_names != expected or second_names != expected:
            fail(f"Unexpected public bundle artifact set: first={sorted(first_names)} second={sorted(second_names)}")

        for name in sorted(expected):
            if sha256(first / name) != sha256(second / name):
                fail(f"Public bundle is not reproducible: {name}")

        validate_template(first / template_name, v)
        validate_overleaf(first / overleaf_name)

    print("PUBLIC-BUNDLE-EVIDENCE status=PASS artifacts=2 reproducible=2 safe_paths=PASS institutional_assets=excluded canonical_setup=PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "abntexto-ufc"
MODULE_PATTERN = re.compile(r"\\input\{(abntexto-ufc/[^}]+\.def)\}")
VERSION_PATTERN = re.compile(
    r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.MULTILINE
)


def current_version() -> str:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = VERSION_PATTERN.search(text)
    if not match:
        raise SystemExit("Makefile VERSION not found.")
    return match.group(1)


def validate_release_state() -> None:
    version = current_version()
    normas = (ROOT / "docs/NORMAS.md").read_text(encoding="utf-8")
    if f"Estado da linha {version}:" not in normas:
        raise SystemExit(
            f"docs/NORMAS.md does not declare the current release line {version}."
        )

    ctan_readme = (ROOT / "docs/README-CTAN.md").read_text(encoding="utf-8")
    if not re.search(rf"^Version:\s*{re.escape(version)}\s*$", ctan_readme, re.MULTILINE):
        raise SystemExit(f"docs/README-CTAN.md does not declare Version: {version}.")

    canonical = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if f"v{version} UFC academic document class" not in canonical:
        raise SystemExit(f"abntexto-ufc.cls does not declare v{version}.")


def expected_sources() -> dict[str, Path]:
    canonical = ROOT / "abntexto-ufc.cls"
    text = canonical.read_text(encoding="utf-8")
    modules = MODULE_PATTERN.findall(text)
    if not modules:
        raise SystemExit("abntexto-ufc.cls does not load any canonical modules.")

    module_set = set(modules)
    disk_modules = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "abntexto-ufc").rglob("*")
        if path.is_file()
    }
    if disk_modules != module_set:
        missing = sorted(module_set - disk_modules)
        unreferenced = sorted(disk_modules - module_set)
        raise SystemExit(
            f"Canonical module tree mismatch: missing={missing}, unreferenced={unreferenced}"
        )

    root = f"{PACKAGE_ID}/"
    sources = {
        f"{root}README.md": ROOT / "docs/README-CTAN.md",
        f"{root}CHANGELOG.md": ROOT / "docs/CHANGELOG-CTAN.md",
        f"{root}LICENSE": ROOT / "LICENSE",
        f"{root}doc/NORMAS.md": ROOT / "docs/NORMAS.md",
        f"{root}doc/{PACKAGE_ID}-example.tex": ROOT / "docs/ctan-example.tex",
        f"{root}tex/abntexto-ufc.cls": canonical,
    }
    for module in modules:
        sources[f"{root}tex/{module}"] = ROOT / module
    return sources


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the exact CTAN archive manifest.")
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    if not args.archive.is_file():
        raise SystemExit(f"CTAN archive not found: {args.archive}")

    validate_release_state()
    expected = expected_sources()
    with zipfile.ZipFile(args.archive) as archive:
        names = {info.filename for info in archive.infolist() if not info.is_dir()}
        expected_names = set(expected)
        missing = sorted(expected_names - names)
        unexpected = sorted(names - expected_names)
        if missing or unexpected:
            raise SystemExit(
                f"CTAN archive manifest mismatch: missing={missing}, unexpected={unexpected}"
            )

        for name, source in expected.items():
            if archive.read(name) != source.read_bytes():
                raise SystemExit(f"CTAN archive payload differs from source: {name}")

    print(f"CTAN archive manifest passed: {len(expected)} files exactly allowed.")


if __name__ == "__main__":
    main()

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
CTAN_DIR = ROOT / "release" / "ctan"
REMOVED_FORWARDING_LAYER = "abntexto-ufc/public-api.def"
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


def entries(path: Path) -> dict[str, zipfile.ZipInfo]:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        fail(f"Duplicate archive entries in {path.name}.")
    for name in names:
        pure = PurePosixPath(name)
        if not name or pure.is_absolute() or ".." in pure.parts:
            fail(f"Unsafe archive path in {path.name}: {name}")
        if any(part.lower() in MICROSOFT_FONTS for part in pure.parts):
            fail(f"Proprietary Microsoft font in {path.name}: {name}")
        if "assets" in pure.parts and "institutional" in pure.parts:
            fail(f"Institutional asset path in {path.name}: {name}")
    return {info.filename: info for info in infos}


def require(archive_entries: dict[str, zipfile.ZipInfo], expected: set[str], archive_name: str) -> None:
    missing = sorted(expected - archive_entries.keys())
    if missing:
        fail(f"{archive_name} missing required entries: {', '.join(missing)}")


def reject_runtime_archive_drift(archive_entries: dict[str, zipfile.ZipInfo], prefix: str, archive_name: str) -> None:
    forbidden = (
        f"{prefix}.github/",
        f"{prefix}assets/",
        f"{prefix}docs/",
        f"{prefix}release/",
        f"{prefix}standards/",
        f"{prefix}template/",
        f"{prefix}tests/",
        f"{prefix}tools/",
        f"{prefix}validator/",
    )
    removed = f"{prefix}{REMOVED_FORWARDING_LAYER}"
    for name in archive_entries:
        if name == removed:
            fail(f"{archive_name} contains removed forwarding layer: {name}")
        if name.startswith(forbidden):
            fail(f"{archive_name} contains non-runtime development content: {name}")


def validate_class(path: Path, v: str) -> None:
    archive_entries = entries(path)
    prefix = f"{PACKAGE_ID}-{v}/"
    if any(not name.startswith(prefix) for name in archive_entries):
        fail(f"{path.name}: every entry must be rooted at {prefix}")
    require(
        archive_entries,
        {
            f"{prefix}README.md",
            f"{prefix}LICENSE",
            f"{prefix}abntexto-ufc.cls",
            f"{prefix}abntexto-ufc/core.def",
            f"{prefix}abntexto-ufc/integrations/abntexto.def",
            f"{prefix}abntexto-ufc/standards/nbr6023-2025.def",
        },
        path.name,
    )
    reject_runtime_archive_drift(archive_entries, prefix, path.name)
    if f"{prefix}abntexto.cls" in archive_entries:
        fail(f"{path.name}: class archive must keep abntexto as an external dependency.")


def validate_ctan(path: Path, v: str) -> None:
    archive_entries = entries(path)
    prefix = f"{PACKAGE_ID}/"
    if any(not name.startswith(prefix) for name in archive_entries):
        fail(f"{path.name}: every entry must be rooted at {prefix}")
    required = {
        f"{prefix}README.md",
        f"{prefix}LICENSE",
        f"{prefix}{PACKAGE_ID}.tex",
        f"{prefix}{PACKAGE_ID}.pdf",
        f"{prefix}{PACKAGE_ID}-example.tex",
        f"{prefix}abntexto-ufc.cls",
        f"{prefix}abntexto-ufc/core.def",
        f"{prefix}abntexto-ufc/integrations/abntexto.def",
        f"{prefix}abntexto-ufc/standards/nbr6023-2025.def",
    }
    require(archive_entries, required, path.name)
    if f"{prefix}{REMOVED_FORWARDING_LAYER}" in archive_entries:
        fail(f"{path.name}: removed forwarding layer must not be distributed.")

    for directory in ("doc/", "tex/", "source/"):
        if any(name.startswith(f"{prefix}{directory}") for name in archive_entries):
            fail(f"{path.name}: modest CTAN candidate must use browsing-friendly package layout, not {directory}")
    if f"{prefix}abntexto.cls" in archive_entries:
        fail(f"{path.name}: CTAN candidate must keep abntexto as an external dependency.")

    with zipfile.ZipFile(path) as archive:
        bundled_readme = archive.read(f"{prefix}README.md")
        bundled_manual = archive.read(f"{prefix}{PACKAGE_ID}.tex")
        bundled_pdf = archive.read(f"{prefix}{PACKAGE_ID}.pdf")
        bundled_example = archive.read(f"{prefix}{PACKAGE_ID}-example.tex")

    expected_readme = (CTAN_DIR / "README.md").read_bytes()
    expected_manual = (CTAN_DIR / f"{PACKAGE_ID}.tex").read_bytes()
    expected_example = (ROOT / "docs" / "ctan-example.tex").read_bytes()
    if bundled_readme != expected_readme:
        fail(f"{path.name}: CTAN README differs from the current tracked package source.")
    if bundled_manual != expected_manual:
        fail(f"{path.name}: CTAN manual source differs from the current tracked package source.")
    if bundled_example != expected_example:
        fail(f"{path.name}: CTAN example differs from the current tracked source.")
    if not bundled_pdf.startswith(b"%PDF-") or len(bundled_pdf) < 5000:
        fail(f"{path.name}: CTAN documentation PDF is missing or invalid.")

    readme_text = bundled_readme.decode("utf-8")
    required_readme_literals = (
        f"Version: {v}",
        "LaTeX Project Public License",
        "https://github.com/tiagosombrra/abntexto-ufc",
        "https://ctan.org/pkg/abntexto",
        "unofficial",
    )
    missing_literals = [item for item in required_readme_literals if item not in readme_text]
    if missing_literals:
        fail(f"{path.name}: CTAN README missing package metadata: {', '.join(missing_literals)}")


def validate_checksums(output: Path, expected_zips: set[str]) -> None:
    checksum_path = output / "SHA256SUMS"
    if not checksum_path.is_file():
        fail("SHA256SUMS is missing.")
    listed: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        parts = line.split("  ", 1)
        if len(parts) != 2:
            fail(f"Malformed SHA256SUMS line: {line}")
        digest, name = parts
        if name in listed:
            fail(f"Duplicate SHA256SUMS entry: {name}")
        listed[name] = digest
    if set(listed) != expected_zips:
        fail(f"SHA256SUMS artifact set mismatch: {sorted(set(listed) ^ expected_zips)}")
    for name, digest in listed.items():
        if sha256(output / name) != digest:
            fail(f"SHA256SUMS mismatch for {name}.")


def build(output: Path, upstream: Path) -> None:
    subprocess.check_call(
        [
            sys.executable,
            str(ROOT / "tools" / "build-distribution-bundles.py"),
            "--output",
            str(output),
            "--abntexto",
            str(upstream),
        ],
        cwd=ROOT,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate deterministic current-v3 distribution candidates.")
    parser.add_argument("--abntexto", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.abntexto.resolve()
    if not upstream.is_file():
        fail(f"Pinned upstream class not found: {upstream}")

    v = version()
    expected_zips = {
        f"{PACKAGE_ID}-{v}.zip",
        f"{PACKAGE_ID}-ctan-{v}.zip",
        f"{PACKAGE_ID}-template-{v}.zip",
        f"{PACKAGE_ID}-overleaf-{v}.zip",
    }
    expected_files = expected_zips | {"SHA256SUMS"}

    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-distribution-") as temp:
        root = Path(temp)
        first = root / "first"
        second = root / "second"
        build(first, upstream)
        build(second, upstream)

        first_files = {path.name for path in first.iterdir() if path.is_file()}
        second_files = {path.name for path in second.iterdir() if path.is_file()}
        if first_files != expected_files or second_files != expected_files:
            fail(
                f"Unexpected distribution artifact set: first={sorted(first_files)} second={sorted(second_files)}"
            )
        for name in sorted(expected_files):
            if sha256(first / name) != sha256(second / name):
                fail(f"Distribution artifact is not reproducible: {name}")

        validate_checksums(first, expected_zips)
        validate_class(first / f"{PACKAGE_ID}-{v}.zip", v)
        validate_ctan(first / f"{PACKAGE_ID}-ctan-{v}.zip", v)

    print(
        "DISTRIBUTION-BUNDLE-EVIDENCE status=PASS artifacts=5 reproducible=5 checksums=PASS "
        "class_layout=PASS ctan_layout=PASS ctan_readme=PASS documentation_pdf=PASS "
        "external_abntexto=PASS institutional_assets=excluded forwarding_layer=absent"
    )


if __name__ == "__main__":
    main()

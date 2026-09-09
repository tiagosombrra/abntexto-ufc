#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
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
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")


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
    for info in infos:
        name = info.filename
        pure = PurePosixPath(name)
        if not name or pure.is_absolute() or ".." in pure.parts:
            fail(f"Unsafe archive path in {path.name}: {name}")
        try:
            name.encode("ascii")
        except UnicodeEncodeError:
            fail(f"Non-ASCII archive path in {path.name}: {name}")
        for part in pure.parts:
            if part.startswith(".") or not SAFE_COMPONENT.fullmatch(part):
                fail(f"CTAN-unsafe filename component in {path.name}: {part}")
        if any(part.lower() in MICROSOFT_FONTS for part in pure.parts):
            fail(f"Proprietary Microsoft font in {path.name}: {name}")
        if "assets" in pure.parts and "institutional" in pure.parts:
            fail(f"Institutional asset path in {path.name}: {name}")
    return {info.filename: info for info in infos}


def require(archive_entries: dict[str, zipfile.ZipInfo], expected: set[str], archive_name: str) -> None:
    missing = sorted(expected - archive_entries.keys())
    if missing:
        fail(f"{archive_name} missing required entries: {', '.join(missing)}")


def validate_package(path: Path, v: str) -> None:
    archive_entries = entries(path)
    prefix = f"{PACKAGE_ID}/"
    if any(not name.startswith(prefix) for name in archive_entries):
        fail(f"{path.name}: every entry must be rooted at {prefix}")

    required = {
        f"{prefix}README.md",
        f"{prefix}CHANGELOG",
        f"{prefix}LICENSE",
        f"{prefix}{PACKAGE_ID}.cls",
        f"{prefix}{PACKAGE_ID}.tex",
        f"{prefix}{PACKAGE_ID}.pdf",
        f"{prefix}{PACKAGE_ID}-example.tex",
        f"{prefix}{PACKAGE_ID}-example.pdf",
        f"{prefix}abntexto-ufc/core.def",
        f"{prefix}abntexto-ufc/integrations/abntexto.def",
        f"{prefix}abntexto-ufc/standards/nbr6023-2025.def",
    }
    require(archive_entries, required, path.name)

    removed = f"{prefix}{REMOVED_FORWARDING_LAYER}"
    if removed in archive_entries:
        fail(f"{path.name}: removed forwarding layer must not be distributed.")

    # Reject only repository-level engineering directories. Runtime modules
    # legitimately live below abntexto-ufc/, including its standards/ module.
    forbidden_root_children = {".github", "tests", "artifacts", "tools", "release", "standards", "dist"}
    for name, info in archive_entries.items():
        pure = PurePosixPath(name)
        if len(pure.parts) > 1 and pure.parts[1] in forbidden_root_children:
            fail(f"{path.name}: development infrastructure leaked into CTAN package: {name}")
        if pure.name == "abntexto.cls":
            fail(f"{path.name}: package must keep abntexto as an external dependency.")
        if any(marker in pure.name.casefold() for marker in ("brasao", "coat-of-arms", "logo-ufc", "ufc-logo")):
            fail(f"{path.name}: institutional mark asset leaked into package: {name}")
        if not name.endswith("/"):
            if info.file_size == 0:
                fail(f"{path.name}: empty file is not allowed: {name}")
            mode = (info.external_attr >> 16) & 0o7777
            if mode not in (0, 0o644):
                fail(f"{path.name}: package file permissions must be 0644: {name} mode={oct(mode)}")

    files = [name for name in archive_entries if not name.endswith("/")]
    basenames = [PurePosixPath(name).name.casefold() for name in files]
    duplicates = sorted(name for name, count in Counter(basenames).items() if count > 1)
    if duplicates:
        fail(f"{path.name}: duplicate case-insensitive basenames: {', '.join(duplicates)}")

    with zipfile.ZipFile(path) as archive:
        bundled_readme = archive.read(f"{prefix}README.md")
        bundled_changelog = archive.read(f"{prefix}CHANGELOG")
        bundled_manual = archive.read(f"{prefix}{PACKAGE_ID}.tex")
        bundled_pdf = archive.read(f"{prefix}{PACKAGE_ID}.pdf")
        bundled_example = archive.read(f"{prefix}{PACKAGE_ID}-example.tex")
        bundled_example_pdf = archive.read(f"{prefix}{PACKAGE_ID}-example.pdf")

        expected_readme = (CTAN_DIR / "README.md").read_bytes()
        expected_changelog = (CTAN_DIR / "CHANGELOG").read_bytes()
        expected_manual = (CTAN_DIR / f"{PACKAGE_ID}.tex").read_bytes()
        expected_example = (ROOT / "docs" / "ctan-example.tex").read_bytes()
        if bundled_readme != expected_readme:
            fail(f"{path.name}: README differs from the tracked CTAN package source.")
        if bundled_changelog != expected_changelog:
            fail(f"{path.name}: CHANGELOG differs from the tracked CTAN package source.")
        if bundled_manual != expected_manual:
            fail(f"{path.name}: manual source differs from the tracked CTAN package source.")
        if bundled_example != expected_example:
            fail(f"{path.name}: example source differs from the tracked source.")
        if not bundled_pdf.startswith(b"%PDF-") or len(bundled_pdf) < 5000:
            fail(f"{path.name}: documentation PDF is missing or invalid.")
        if not bundled_example_pdf.startswith(b"%PDF-") or len(bundled_example_pdf) < 5000:
            fail(f"{path.name}: example PDF is missing or invalid.")

        for name in files:
            pure = PurePosixPath(name)
            if pure.suffix.casefold() in {".md", ".tex", ".cls", ".def", ".bib", ".txt"} or pure.name == "CHANGELOG":
                data = archive.read(name)
                if data.startswith(b"\xef\xbb\xbf"):
                    fail(f"{path.name}: UTF-8 BOM is not allowed: {name}")
                if b"\r" in data:
                    fail(f"{path.name}: CTAN text files must use LF line endings: {name}")

    readme_text = bundled_readme.decode("utf-8")
    required_readme_literals = (
        f"Version: {v}",
        "License: LaTeX Project Public License 1.3c or later",
        "https://github.com/tiagosombrra/abntexto-ufc",
        "https://ctan.org/pkg/abntexto",
        "No UFC logo",
        "unofficial",
    )
    missing_literals = [item for item in required_readme_literals if item.casefold() not in readme_text.casefold()]
    if missing_literals:
        fail(f"{path.name}: README missing package metadata: {', '.join(missing_literals)}")

    for forbidden in (
        "development candidate",
        "v3.0.0 está em desenvolvimento",
        "v3.0.0 ainda não foi publicada",
        "ufctex",
        "modelo-latex-ufc",
    ):
        if forbidden.casefold() in readme_text.casefold():
            fail(f"{path.name}: stale/deprecated publication text leaked into README: {forbidden}")


def validate_template(path: Path, v: str, *, overleaf: bool) -> None:
    archive_entries = entries(path)
    has_upstream = any(PurePosixPath(name).name == "abntexto.cls" for name in archive_entries)
    if overleaf and not has_upstream:
        fail(f"{path.name}: Overleaf bundle must include pinned abntexto.cls.")
    if not overleaf and has_upstream:
        fail(f"{path.name}: editable template must keep abntexto as an external dependency.")


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
    parser = argparse.ArgumentParser(description="Validate deterministic current-v3 CTAN-grade/public distribution archives.")
    parser.add_argument("--abntexto", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.abntexto.resolve()
    if not upstream.is_file():
        fail(f"Pinned upstream class not found: {upstream}")

    v = version()
    expected_zips = {
        f"{PACKAGE_ID}-{v}.zip",
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
        validate_package(first / f"{PACKAGE_ID}-{v}.zip", v)
        validate_template(first / f"{PACKAGE_ID}-template-{v}.zip", v, overleaf=False)
        validate_template(first / f"{PACKAGE_ID}-overleaf-{v}.zip", v, overleaf=True)

    print(
        "DISTRIBUTION-BUNDLE-EVIDENCE status=PASS artifacts=4 reproducible=4 checksums=PASS "
        "canonical_ctan_package=PASS ctan_upload_archives=1 ctan_readme=PASS documentation_pdf=PASS "
        "example_pdf=PASS external_abntexto=PASS institutional_assets=excluded forwarding_layer=absent"
    )


if __name__ == "__main__":
    main()

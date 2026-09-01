#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "abntexto-ufc"
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


def read_version() -> str:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", makefile, re.MULTILINE)
    if not match:
        fail("Makefile VERSION not found.")
    version = match.group(1)
    class_text = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if f"v{version} UFC academic document class" not in class_text:
        fail(f"abntexto-ufc.cls does not match VERSION {version}.")
    return version


def tracked_files() -> set[str]:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        fail("Distribution bundle generation requires a canonical Git checkout.")
    return {item.decode("utf-8") for item in output.split(b"\0") if item}


def runtime_paths(tracked: set[str]) -> list[str]:
    paths = ["abntexto-ufc.cls"]
    paths.extend(sorted(path for path in tracked if path.startswith("abntexto-ufc/") and (ROOT / path).is_file()))
    missing = [path for path in paths if path not in tracked or not (ROOT / path).is_file()]
    if missing:
        fail("Required runtime source is not tracked: " + ", ".join(missing))
    return paths


def source_date_epoch() -> int:
    value = os.environ.get("SOURCE_DATE_EPOCH")
    if value:
        return int(value)
    try:
        output = subprocess.check_output(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%ct"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return int(output)
    except Exception:
        return 315532800


def zip_datetime(epoch: int) -> tuple[int, int, int, int, int, int]:
    epoch = min(max(epoch, 315532800), 4354819198)
    tm = time.gmtime(epoch)
    second = tm.tm_sec - (tm.tm_sec % 2)
    return tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, second


def validate_arcname(name: str) -> None:
    pure = PurePosixPath(name)
    if not name or pure.is_absolute() or ".." in pure.parts:
        fail(f"Unsafe distribution archive path: {name}")
    if any(part.lower() in MICROSOFT_FONTS for part in pure.parts):
        fail(f"Proprietary Microsoft font cannot be distributed: {name}")
    if "assets" in pure.parts and "institutional" in pure.parts:
        fail(f"Institutional asset path cannot be distributed: {name}")


def mode_for(path: Path) -> int:
    return 0o755 if path.suffix in {".py", ".sh"} else 0o644


def zip_info(name: str, date_time: tuple[int, int, int, int, int, int], mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (mode & 0xFFFF) << 16
    return info


def write_zip(path: Path, entries: list[tuple[str, bytes, int]], date_time: tuple[int, int, int, int, int, int]) -> None:
    seen: set[str] = set()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content, mode in sorted(entries, key=lambda item: item[0]):
            validate_arcname(name)
            if name in seen:
                fail(f"Duplicate distribution archive path: {name}")
            seen.add(name)
            archive.writestr(zip_info(name, date_time, mode), content)
    path.write_bytes(buffer.getvalue())


def file_entry(source: Path, arcname: str) -> tuple[str, bytes, int]:
    if not source.is_file():
        fail(f"Required distribution source missing: {source.relative_to(ROOT)}")
    return arcname, source.read_bytes(), mode_for(source)


def class_entries(runtime: list[str], version: str) -> list[tuple[str, bytes, int]]:
    prefix = f"{PACKAGE_ID}-{version}/"
    entries = [
        file_entry(ROOT / "README.md", f"{prefix}README.md"),
        file_entry(ROOT / "LICENSE", f"{prefix}LICENSE"),
    ]
    for relative in runtime:
        entries.append(file_entry(ROOT / relative, f"{prefix}{relative}"))
    return entries


def ctan_entries(runtime: list[str]) -> list[tuple[str, bytes, int]]:
    prefix = f"{PACKAGE_ID}/"
    entries = [
        file_entry(ROOT / "README.md", f"{prefix}README.md"),
        file_entry(ROOT / "LICENSE", f"{prefix}LICENSE"),
        file_entry(ROOT / "docs" / "ctan-example.tex", f"{prefix}doc/{PACKAGE_ID}-example.tex"),
    ]
    for relative in runtime:
        entries.append(file_entry(ROOT / relative, f"{prefix}tex/{relative}"))
    return entries


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_checksums(output: Path, artifacts: list[Path]) -> Path:
    checksum = output / "SHA256SUMS"
    lines = [f"{sha256(path)}  {path.name}" for path in sorted(artifacts, key=lambda item: item.name)]
    checksum.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksum


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build deterministic current-v3 public, class and CTAN distribution candidates."
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--abntexto", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.abntexto.resolve()
    if not upstream.is_file():
        fail(f"Pinned upstream abntexto.cls not found: {upstream}")

    version = read_version()
    tracked = tracked_files()
    runtime = runtime_paths(tracked)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

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

    date_time = zip_datetime(source_date_epoch())
    class_zip = output / f"{PACKAGE_ID}-{version}.zip"
    ctan_zip = output / f"{PACKAGE_ID}-ctan-{version}.zip"
    write_zip(class_zip, class_entries(runtime, version), date_time)
    write_zip(ctan_zip, ctan_entries(runtime), date_time)

    artifacts = sorted(output.glob("*.zip"), key=lambda item: item.name)
    expected = {
        f"{PACKAGE_ID}-{version}.zip",
        f"{PACKAGE_ID}-ctan-{version}.zip",
        f"{PACKAGE_ID}-template-{version}.zip",
        f"{PACKAGE_ID}-overleaf-{version}.zip",
    }
    actual = {path.name for path in artifacts}
    if actual != expected:
        fail(f"Unexpected distribution artifact set: {sorted(actual ^ expected)}")

    checksum = write_checksums(output, artifacts)
    print(f"Distribution candidates generated in {output}")
    for path in artifacts + [checksum]:
        print(path.name)


if __name__ == "__main__":
    main()

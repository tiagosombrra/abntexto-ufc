#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import time
import zipfile
from pathlib import Path, PurePosixPath
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "abntexto-ufc"
TEMPLATE_DIR = ROOT / "template"
UPSTREAM_MARKER = b"[2026-05-08 1.1 Preparation of works in ABNT standards]"
REFERENCE_IMAGES = (
    Path("template/figures/ufc-campus-pici.jpg"),
    Path("template/figures/ufc-reitoria.jpg"),
)
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


def read_version() -> str:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(
        r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$",
        makefile,
        re.MULTILINE,
    )
    if not match:
        raise SystemExit("Makefile VERSION not found.")
    version = match.group(1)

    class_text = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if f"v{version} UFC academic document class" not in class_text:
        raise SystemExit(f"abntexto-ufc.cls does not match VERSION {version}.")
    return version


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
    minimum = 315532800
    maximum = 4354819198
    epoch = min(max(epoch, minimum), maximum)
    stamp = time.gmtime(epoch)
    second = stamp.tm_sec - (stamp.tm_sec % 2)
    return (
        stamp.tm_year,
        stamp.tm_mon,
        stamp.tm_mday,
        stamp.tm_hour,
        stamp.tm_min,
        second,
    )


def tracked_files(pathspec: str) -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-z", "--", pathspec],
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        raise SystemExit("Public bundle generation requires a canonical Git checkout.") from exc

    result = []
    for raw in output.split(b"\0"):
        if not raw:
            continue
        path = ROOT / raw.decode("utf-8")
        if path.is_file():
            result.append(path)
    return sorted(result)


def validate_archive_name(name: str) -> None:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts:
        raise SystemExit(f"Unsafe public bundle entry: {name}")


def file_mode(path: Path) -> int:
    return 0o755 if path.suffix in {".sh", ".py"} else 0o644


def public_main(content: bytes) -> bytes:
    text = content.decode("utf-8")
    enabled = "  brasao = sim,"
    disabled = "  brasao = nao,"
    if text.count(enabled) != 1:
        raise SystemExit("template/main.tex must enable the institutional mark exactly once in source.")
    return text.replace(enabled, disabled, 1).encode("utf-8")


def add_entry(
    entries: dict[str, tuple[bytes, int]],
    name: str,
    content: bytes,
    mode: int = 0o644,
) -> None:
    validate_archive_name(name)
    basename = PurePosixPath(name).name.lower()
    if basename in MICROSOFT_FONTS:
        raise SystemExit(f"Proprietary Microsoft font cannot be distributed: {name}")
    if name in entries:
        raise SystemExit(f"Duplicate public bundle entry: {name}")
    entries[name] = (content, mode)


def current_runtime_entries(prefix: str = "") -> dict[str, tuple[bytes, int]]:
    entries: dict[str, tuple[bytes, int]] = {}
    runtime_files = tracked_files("abntexto-ufc.cls") + tracked_files("abntexto-ufc")
    for path in runtime_files:
        relative = path.relative_to(ROOT).as_posix()
        add_entry(entries, f"{prefix}{relative}", path.read_bytes(), file_mode(path))
    add_entry(entries, f"{prefix}LICENSE", (ROOT / "LICENSE").read_bytes())
    return entries


def current_template_entries(prefix: str = "") -> dict[str, tuple[bytes, int]]:
    entries: dict[str, tuple[bytes, int]] = {}
    for path in tracked_files("template"):
        relative = path.relative_to(TEMPLATE_DIR).as_posix()
        content = public_main(path.read_bytes()) if relative == "main.tex" else path.read_bytes()
        add_entry(entries, f"{prefix}{relative}", content, file_mode(path))

    for relative in REFERENCE_IMAGES:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(
                f"Required licensed reference image missing: {relative.as_posix()}; "
                "run `make reference-assets` before building public bundles."
            )
        archive_name = path.relative_to(TEMPLATE_DIR).as_posix()
        add_entry(entries, f"{prefix}{archive_name}", path.read_bytes(), file_mode(path))
    return entries


def bundle_entries(prefix: str = "") -> dict[str, tuple[bytes, int]]:
    entries = current_template_entries(prefix)
    for name, value in current_runtime_entries(prefix).items():
        if name in entries:
            raise SystemExit(f"Template/runtime collision in public bundle: {name}")
        entries[name] = value
    return entries


def zip_bytes(
    entries: dict[str, tuple[bytes, int]],
    date_time: tuple[int, int, int, int, int, int],
) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for name in sorted(entries):
            content, mode = entries[name]
            info = zipfile.ZipInfo(name, date_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (mode & 0xFFFF) << 16
            archive.writestr(info, content)
    return buffer.getvalue()


def write_bundle(
    output: Path,
    name: str,
    entries: dict[str, tuple[bytes, int]],
    date_time: tuple[int, int, int, int, int, int],
) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    target = output / name
    target.write_bytes(zip_bytes(entries, date_time))
    return target


def build_template_bundle(
    output: Path,
    version: str,
    date_time: tuple[int, int, int, int, int, int],
) -> Path:
    archive_root = f"{PACKAGE_ID}-template-{version}/"
    entries = bundle_entries(archive_root)
    return write_bundle(
        output,
        f"{PACKAGE_ID}-template-{version}.zip",
        entries,
        date_time,
    )


def build_overleaf_bundle(
    output: Path,
    version: str,
    date_time: tuple[int, int, int, int, int, int],
    abntexto: Path,
) -> Path:
    if not abntexto.is_file():
        raise SystemExit(f"Pinned abntexto.cls not found: {abntexto}")
    upstream = abntexto.read_bytes()
    if UPSTREAM_MARKER not in upstream:
        raise SystemExit("Pinned abntexto.cls identity marker missing.")

    entries = bundle_entries()
    add_entry(entries, "abntexto.cls", upstream)
    return write_bundle(
        output,
        f"{PACKAGE_ID}-overleaf-{version}.zip",
        entries,
        date_time,
    )


def remove_previous(output: Path, filenames: Iterable[str]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        target = output / filename
        if target.exists():
            target.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build deterministic current-v3 public template and Overleaf bundles."
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--abntexto", type=Path, required=True)
    args = parser.parse_args()

    version = read_version()
    output = args.output.resolve()
    names = (
        f"{PACKAGE_ID}-template-{version}.zip",
        f"{PACKAGE_ID}-overleaf-{version}.zip",
    )
    remove_previous(output, names)

    date_time = zip_datetime(source_date_epoch())
    artifacts = (
        build_template_bundle(output, version, date_time),
        build_overleaf_bundle(output, version, date_time, args.abntexto.resolve()),
    )

    print(f"Public bundles generated in {output}")
    for artifact in artifacts:
        print(artifact.name)


if __name__ == "__main__":
    main()

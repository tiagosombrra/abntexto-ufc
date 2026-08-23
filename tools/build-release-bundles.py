#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import os
import re
import shutil
import subprocess
import time
import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

PACKAGE_ID = "abntexto-ufc"
LEGACY_CLASS = "ufctex.cls"

MICROSOFT_FONTS = {
    "times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf",
    "arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf",
}

CLASS_INPUTS = (
    "abntexto-ufc.cls",
    "abntexto-ufc",
    LEGACY_CLASS,
    "assets/institucional",
    "tools/convert-encoding-to-unicode.ps1",
    "tools/prepare-windows-fonts.ps1",
    "LICENSE",
    "README.md",
    "docs/NORMAS.md",
)

TEMPLATE_INPUTS = (
    "documento.tex",
    "1-pre-textuais",
    "2-textuais",
    "3-pos-textuais",
    "figuras",
    "assets",
    "abntexto-ufc.cls",
    "abntexto-ufc",
    LEGACY_CLASS,
    "Makefile",
    "README.md",
    "LICENSE",
    "docs/NORMAS.md",
    "tools/convert-encoding-to-unicode.ps1",
    "tools/prepare-windows-fonts.ps1",
)

DOC_SOURCE_INPUTS = (
    "documento.tex",
    "1-pre-textuais",
    "2-textuais",
    "3-pos-textuais",
    "figuras",
)


def read_version() -> str:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit("Makefile VERSION not found.")
    version = match.group(1)

    cls = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if f"v{version} UFC academic document class" not in cls:
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
    tm = time.gmtime(epoch)
    second = tm.tm_sec - (tm.tm_sec % 2)
    return (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, second)


def iter_files(specs: Iterable[str]) -> list[tuple[Path, Path]]:
    result: list[tuple[Path, Path]] = []
    seen: set[str] = set()
    for spec in specs:
        source = ROOT / spec
        if not source.exists():
            raise SystemExit(f"Required release input missing: {spec}")
        candidates = [source] if source.is_file() else sorted(path for path in source.rglob("*") if path.is_file())
        for path in candidates:
            relative = path.relative_to(ROOT)
            key = relative.as_posix()
            if key not in seen:
                result.append((path, relative))
                seen.add(key)
    return result


def file_mode(path: Path) -> int:
    return 0o755 if path.suffix in {".sh", ".py"} else 0o644


def make_info(name: str, date_time: tuple[int, int, int, int, int, int], mode: int = 0o644) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (mode & 0xFFFF) << 16
    return info


def archive_bytes(entries: list[tuple[str, bytes, int]], date_time: tuple[int, int, int, int, int, int]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content, mode in sorted(entries, key=lambda item: item[0]):
            archive.writestr(make_info(name, date_time, mode), content)
    return buffer.getvalue()


def source_entries(specs: Iterable[str], prefix: str = "") -> list[tuple[str, bytes, int]]:
    entries: list[tuple[str, bytes, int]] = []
    for path, relative in iter_files(specs):
        if path.name.lower() in MICROSOFT_FONTS:
            raise SystemExit(f"Proprietary Microsoft font cannot be distributed: {relative}")
        entries.append((f"{prefix}{relative.as_posix()}", path.read_bytes(), file_mode(path)))
    return entries


def write_archive(path: Path, entries: list[tuple[str, bytes, int]], date_time: tuple[int, int, int, int, int, int]) -> None:
    path.write_bytes(archive_bytes(entries, date_time))


def build_class_bundle(out: Path, version: str, date_time: tuple[int, int, int, int, int, int]) -> Path:
    root = f"{PACKAGE_ID}-{version}/"
    path = out / f"{PACKAGE_ID}-{version}.zip"
    write_archive(path, source_entries(CLASS_INPUTS, root), date_time)
    return path


def build_template_bundle(
    out: Path,
    version: str,
    date_time: tuple[int, int, int, int, int, int],
    abntexto: Path | None = None,
) -> Path:
    suffix = "-overleaf" if abntexto else ""
    root = "" if abntexto else f"modelo-latex-ufc-{version}/"
    path = out / f"modelo-latex-ufc{suffix}-{version}.zip"
    entries = source_entries(TEMPLATE_INPUTS, root)
    if abntexto:
        if not abntexto.is_file():
            raise SystemExit(f"Pinned abntexto.cls not found: {abntexto}")
        content = abntexto.read_bytes()
        if b"[2026-05-08 1.1 Preparation of works in ABNT standards]" not in content:
            raise SystemExit("Pinned abntexto.cls identity marker missing.")
        entries.append(("abntexto.cls", content, 0o644))
    write_archive(path, entries, date_time)
    return path


def build_ctan_bundle(
    out: Path,
    version: str,
    reference_pdf: Path,
    date_time: tuple[int, int, int, int, int, int],
) -> Path:
    if not reference_pdf.is_file():
        raise SystemExit(f"Reference PDF not found: {reference_pdf}")

    root = f"{PACKAGE_ID}/"
    entries: list[tuple[str, bytes, int]] = [
        (f"{root}README.md", (ROOT / "docs/README-CTAN.md").read_bytes(), 0o644),
        (f"{root}CHANGELOG.md", (ROOT / "docs/CHANGELOG-CTAN.md").read_bytes(), 0o644),
        (f"{root}LICENSE", (ROOT / "LICENSE").read_bytes(), 0o644),
        (f"{root}doc/NORMAS.md", (ROOT / "docs/NORMAS.md").read_bytes(), 0o644),
        (f"{root}doc/{PACKAGE_ID}-{version}-reference.pdf", reference_pdf.read_bytes(), 0o644),
    ]

    for path, relative in iter_files(("abntexto-ufc.cls", "abntexto-ufc", "assets/institucional")):
        entries.append((f"{root}tex/{relative.as_posix()}", path.read_bytes(), file_mode(path)))

    for path, relative in iter_files(DOC_SOURCE_INPUTS):
        entries.append((f"{root}doc/example/{relative.as_posix()}", path.read_bytes(), file_mode(path)))

    for path, relative in iter_files((
        "tools/convert-encoding-to-unicode.ps1",
        "tools/prepare-windows-fonts.ps1",
    )):
        entries.append((f"{root}scripts/{relative.name}", path.read_bytes(), 0o644))

    path = out / f"{PACKAGE_ID}-ctan-{version}.zip"
    write_archive(path, entries, date_time)
    return path


def write_checksums(out: Path, artifacts: list[Path]) -> Path:
    lines = []
    for path in sorted(artifacts, key=lambda item: item.name):
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    checksum_path = out / "SHA256SUMS"
    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksum_path


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Build deterministic {PACKAGE_ID} release bundles.")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--reference-pdf", type=Path, default=ROOT / "documento.pdf")
    parser.add_argument("--abntexto", type=Path)
    args = parser.parse_args()

    version = read_version()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for path in output.iterdir():
        shutil.rmtree(path) if path.is_dir() else path.unlink()

    date_time = zip_datetime(source_date_epoch())
    reference_pdf = args.reference_pdf.resolve()
    if not reference_pdf.is_file():
        raise SystemExit("documento.pdf is required; run make release-preflight first.")

    reference_out = output / f"{PACKAGE_ID}-{version}-reference.pdf"
    shutil.copyfile(reference_pdf, reference_out)

    artifacts = [
        build_class_bundle(output, version, date_time),
        build_template_bundle(output, version, date_time),
        build_ctan_bundle(output, version, reference_pdf, date_time),
        reference_out,
    ]
    if args.abntexto:
        artifacts.append(build_template_bundle(output, version, date_time, args.abntexto.resolve()))

    checksum_path = write_checksums(output, artifacts)
    print(f"Release bundles generated in {output}")
    for path in sorted(artifacts + [checksum_path], key=lambda item: item.name):
        print(path.name)


if __name__ == "__main__":
    main()

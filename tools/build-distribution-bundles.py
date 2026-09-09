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
import tempfile
import time
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "abntexto-ufc"
CTAN_DIR = ROOT / "release" / "ctan"
CTAN_EXAMPLE = ROOT / "docs" / "ctan-example.tex"
PROJECT_MODULE_INPUT_RE = re.compile(
    r"(?m)^[ \t]*\\input\{(?P<path>abntexto-ufc/[^}\r\n]+\.def)\}[ \t]*(?:%[^\r\n]*)?$"
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
FORBIDDEN_PUBLICATION_PHRASES = (
    "development candidate",
    "v3.0.0 está em desenvolvimento",
    "v3.0.0 ainda não foi publicada",
    "a versão estável publicada atualmente é a **v2.1.0**",
)
FORBIDDEN_CTAN_IDENTIFIERS = (
    "ufctex",
    "modelo-latex-ufc",
)


def fail(message: str) -> None:
    raise SystemExit(message)


def require_publication_ready_text(path: Path, *, ctan_surface: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    folded = text.casefold()
    for phrase in FORBIDDEN_PUBLICATION_PHRASES:
        if phrase.casefold() in folded:
            fail(f"Publication metadata is stale in {path.relative_to(ROOT)}: {phrase}")
    if ctan_surface:
        for identifier in FORBIDDEN_CTAN_IDENTIFIERS:
            if identifier.casefold() in folded:
                fail(
                    f"Deprecated or historical package identifier leaked into CTAN surface "
                    f"{path.relative_to(ROOT)}: {identifier}"
                )
    return text


def read_version() -> str:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", makefile, re.MULTILINE)
    if not match:
        fail("Makefile VERSION not found.")
    version = match.group(1)

    class_text = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if f"v{version} UFC academic document class" not in class_text:
        fail(f"abntexto-ufc.cls does not match VERSION {version}.")

    manual_text = require_publication_ready_text(CTAN_DIR / f"{PACKAGE_ID}.tex", ctan_surface=True)
    if f"\\newcommand{{\\version}}{{{version}}}" not in manual_text:
        fail(f"CTAN manual does not match VERSION {version}.")

    readme_text = require_publication_ready_text(CTAN_DIR / "README.md", ctan_surface=True)
    if not re.search(rf"^Version:\s*{re.escape(version)}\s*$", readme_text, re.MULTILINE):
        fail(f"CTAN README does not identify final VERSION {version} exactly.")
    if "License: LaTeX Project Public License 1.3c or later" not in readme_text:
        fail("CTAN README must state the LPPL 1.3c-or-later license explicitly.")
    if "No UFC logo" not in readme_text:
        fail("CTAN README must explicitly state that no UFC logo is distributed.")

    require_publication_ready_text(ROOT / "README.md")
    require_publication_ready_text(CTAN_EXAMPLE, ctan_surface=True)
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


def runtime_module_paths(tracked: set[str]) -> list[str]:
    paths = sorted(
        path
        for path in tracked
        if path.startswith(f"{PACKAGE_ID}/") and (ROOT / path).is_file()
    )
    unexpected = [path for path in paths if not path.endswith(".def")]
    if unexpected:
        fail("Unexpected non-module file in project runtime directory: " + ", ".join(unexpected))
    return paths


def strip_module_wrapper(relative: str, text: str) -> str:
    expected = f"\\ProvidesFile{{{relative}}}"
    if text.count(expected) != 1:
        fail(f"Project module must provide itself exactly once before CTAN inlining: {relative}")

    provides_re = re.compile(
        rf"(?m)^[ \t]*{re.escape(expected)}(?:\[[^\r\n]*\])?[ \t]*(?:%[^\r\n]*)?\r?\n?"
    )
    text, count = provides_re.subn("", text, count=1)
    if count != 1:
        fail(f"Cannot strip module ProvidesFile wrapper: {relative}")

    endinput_re = re.compile(r"(?m)^[ \t]*\\endinput[ \t]*(?:%[^\r\n]*)?(?:\r?\n)?\Z")
    match = endinput_re.search(text)
    if match is None:
        fail(f"Project module must end with \\endinput before CTAN inlining: {relative}")
    return text[: match.start()].rstrip() + "\n"


def build_monolithic_ctan_class(tracked: set[str]) -> tuple[bytes, list[str]]:
    source = ROOT / f"{PACKAGE_ID}.cls"
    if f"{PACKAGE_ID}.cls" not in tracked or not source.is_file():
        fail(f"Canonical class source is not tracked: {PACKAGE_ID}.cls")

    expected_modules = runtime_module_paths(tracked)
    expected_set = set(expected_modules)
    inlined: list[str] = []
    active: set[str] = set()

    def expand(text: str, owner: str) -> str:
        def replace(match: re.Match[str]) -> str:
            relative = match.group("path")
            if relative not in expected_set or not (ROOT / relative).is_file():
                fail(f"CTAN class references an untracked project module from {owner}: {relative}")
            if relative in active:
                fail(f"Cyclic project module input while building CTAN class: {relative}")
            if relative in inlined:
                fail(f"Project module is loaded more than once in canonical class: {relative}")

            active.add(relative)
            inlined.append(relative)
            module_text = (ROOT / relative).read_text(encoding="utf-8")
            module_text = strip_module_wrapper(relative, module_text)
            module_text = expand(module_text, relative)
            active.remove(relative)

            label = PurePosixPath(relative).with_suffix("").as_posix()
            return (
                f"% --- BEGIN inlined module: {label} ---\n"
                f"{module_text.rstrip()}\n"
                f"% --- END inlined module: {label} ---"
            )

        return PROJECT_MODULE_INPUT_RE.sub(replace, text)

    class_text = source.read_text(encoding="utf-8")
    generated = expand(class_text, f"{PACKAGE_ID}.cls")

    if PROJECT_MODULE_INPUT_RE.search(generated):
        fail("Generated CTAN class still contains a project-owned module input.")
    if re.search(rf"\\ProvidesFile\{{{re.escape(PACKAGE_ID)}/", generated):
        fail("Generated CTAN class still contains project module ProvidesFile wrappers.")

    missing = sorted(expected_set - set(inlined))
    unexpected = sorted(set(inlined) - expected_set)
    if missing or unexpected:
        fail(
            "CTAN monolithic class module coverage mismatch: "
            f"missing={missing} unexpected={unexpected}"
        )

    banner = (
        "% CTAN distribution file generated from the modular repository sources.\n"
        "% All project-owned runtime modules are inlined below; no external .def files are required.\n"
    )
    generated = banner + generated
    return generated.encode("utf-8"), inlined


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
    stamp = time.gmtime(epoch)
    second = stamp.tm_sec - (stamp.tm_sec % 2)
    return stamp.tm_year, stamp.tm_mon, stamp.tm_mday, stamp.tm_hour, stamp.tm_min, second


def validate_arcname(name: str) -> None:
    pure = PurePosixPath(name)
    if not name or pure.is_absolute() or ".." in pure.parts:
        fail(f"Unsafe distribution archive path: {name}")
    try:
        name.encode("ascii")
    except UnicodeEncodeError:
        fail(f"CTAN/public archive path must be ASCII: {name}")
    if any(part.startswith(".") for part in pure.parts):
        fail(f"Hidden archive path is not allowed: {name}")
    if any(re.search(r"\s", part) for part in pure.parts):
        fail(f"Whitespace in archive path is not allowed: {name}")
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


def write_zip(
    path: Path,
    entries: list[tuple[str, bytes, int]],
    date_time: tuple[int, int, int, int, int, int],
) -> None:
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


def bytes_entry(content: bytes, arcname: str, mode: int = 0o644) -> tuple[str, bytes, int]:
    return arcname, content, mode


def run_pdflatex(source: Path, work: Path, env: dict[str, str]) -> bytes:
    target = work / source.name
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        target.name,
    ]
    for _ in range(2):
        result = subprocess.run(
            command,
            cwd=work,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            fail(f"CTAN document build failed for {target.name}:\n" + result.stdout[-6000:])
    pdf = work / f"{target.stem}.pdf"
    if not pdf.is_file() or pdf.stat().st_size == 0:
        fail(f"CTAN document PDF was not generated: {target.name}")
    pdf_bytes = pdf.read_bytes()
    if not pdf_bytes.startswith(b"%PDF-"):
        fail(f"CTAN document output is not a PDF: {target.name}")
    return pdf_bytes


def build_ctan_documents(
    epoch: int,
    upstream: Path,
    ctan_class: bytes,
) -> tuple[bytes, bytes, bytes, bytes]:
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = str(epoch)
    env["FORCE_SOURCE_DATE"] = "1"

    manual_source = CTAN_DIR / f"{PACKAGE_ID}.tex"
    manual_bytes = manual_source.read_bytes()
    with tempfile.TemporaryDirectory(prefix=f"{PACKAGE_ID}-ctan-manual-") as temp:
        work = Path(temp)
        manual_pdf = run_pdflatex(manual_source, work, env)

    example_source = CTAN_EXAMPLE
    example_bytes = example_source.read_bytes()
    with tempfile.TemporaryDirectory(prefix=f"{PACKAGE_ID}-ctan-example-") as temp:
        work = Path(temp)
        (work / f"{PACKAGE_ID}.cls").write_bytes(ctan_class)
        shutil.copy2(upstream, work / "abntexto.cls")
        example_target = work / f"{PACKAGE_ID}-example.tex"
        example_target.write_bytes(example_bytes)
        example_pdf = run_pdflatex(example_target, work, env)
        if (work / PACKAGE_ID).exists():
            fail("CTAN example unexpectedly required the modular project runtime directory.")

    return manual_bytes, manual_pdf, example_bytes, example_pdf


def ctan_entries(
    ctan_class: bytes,
    manual_source: bytes,
    manual_pdf: bytes,
    example_source: bytes,
    example_pdf: bytes,
) -> list[tuple[str, bytes, int]]:
    prefix = f"{PACKAGE_ID}/"
    return [
        file_entry(CTAN_DIR / "README.md", f"{prefix}README.md"),
        file_entry(CTAN_DIR / "CHANGELOG", f"{prefix}CHANGELOG"),
        file_entry(ROOT / "LICENSE", f"{prefix}LICENSE"),
        bytes_entry(ctan_class, f"{prefix}{PACKAGE_ID}.cls"),
        bytes_entry(manual_source, f"{prefix}{PACKAGE_ID}.tex"),
        bytes_entry(manual_pdf, f"{prefix}{PACKAGE_ID}.pdf"),
        bytes_entry(example_source, f"{prefix}{PACKAGE_ID}-example.tex"),
        bytes_entry(example_pdf, f"{prefix}{PACKAGE_ID}-example.pdf"),
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_checksums(output: Path, artifacts: list[Path]) -> Path:
    checksum = output / "SHA256SUMS"
    lines = [f"{sha256(path)}  {path.name}" for path in sorted(artifacts, key=lambda item: item.name)]
    checksum.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksum


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build deterministic v3 CTAN, editable-template and Overleaf release archives."
    )
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--abntexto", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.abntexto.resolve()
    if not upstream.is_file():
        fail(f"Pinned upstream abntexto.cls not found: {upstream}")

    version = read_version()
    tracked = tracked_files()
    ctan_class, inlined_modules = build_monolithic_ctan_class(tracked)
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

    epoch = source_date_epoch()
    date_time = zip_datetime(epoch)
    manual_source, manual_pdf, example_source, example_pdf = build_ctan_documents(
        epoch,
        upstream,
        ctan_class,
    )

    package_zip = output / f"{PACKAGE_ID}-{version}.zip"
    write_zip(
        package_zip,
        ctan_entries(ctan_class, manual_source, manual_pdf, example_source, example_pdf),
        date_time,
    )

    artifacts = sorted(output.glob("*.zip"), key=lambda item: item.name)
    expected = {
        f"{PACKAGE_ID}-{version}.zip",
        f"{PACKAGE_ID}-template-{version}.zip",
        f"{PACKAGE_ID}-overleaf-{version}.zip",
    }
    actual = {path.name for path in artifacts}
    if actual != expected:
        fail(f"Unexpected distribution artifact set: {sorted(actual ^ expected)}")

    checksum = write_checksums(output, artifacts)
    print(
        f"CTAN monolithic class generated with {len(inlined_modules)} inlined project modules; "
        "no project .def files are distributed."
    )
    print(f"Distribution candidates generated in {output}")
    for path in artifacts + [checksum]:
        print(path.name)


if __name__ == "__main__":
    main()

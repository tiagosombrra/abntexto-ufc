#!/usr/bin/env python3
"""Fail-closed PDF evidence for the public coat-of-arms image-path option.

Use generated PNG fixtures, never actual institutional marks. Certify the
academic and research-project cover paths independently in all four locales.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import zlib

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "artifacts/integrated-i18n/coat-path"
LOCALES = {"pt": ("pt-BR", "brazilian"), "en": ("en-US", "english"),
           "es": ("es-ES", "spanish"), "fr": ("fr-FR", "french")}
PROFILES = ("undergraduate-capstone", "research-project")
CASES = ("image-a", "image-b", "missing", "disabled")
SIZES = {"image-a": (19, 13), "image-b": (23, 17)}
WARNING = re.compile(r"UFC\s+coat\s+of\s+arms\s+asset\s+not\s+found", re.I)


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    block = kind + payload
    return (struct.pack(">I", len(payload)) + block
            + struct.pack(">I", zlib.crc32(block) & 0xffffffff))


def synthetic_png(width: int, height: int, salt: int) -> bytes:
    """Create distinct reproducible RGB PNG assets with no external packages."""
    raw = b"".join(
        b"\x00" + b"".join(bytes(((x * 31 + salt) % 256,
                               (y * 29 + salt) % 256,
                               (x + 7 * y + salt) % 256))
                         for x in range(width))
        for y in range(height)
    )
    return (b"\x89PNG\r\n\x1a\n"
            + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + png_chunk(b"IDAT", zlib.compress(raw, 9))
            + png_chunk(b"IEND", b""))


def asset_path(case: str) -> str:
    name = "image-b.png" if case == "image-b" else "image-a.png"
    if case == "missing":
        name = "missing-image.png"
    return "artifacts/integrated-i18n/coat-path/" + name


def make_source(profile: str, locale: str, case: str) -> str:
    lang, _ = LOCALES[locale]
    enabled = "false" if case == "disabled" else "true"
    return "\n".join([
        rf"\DocumentMetadata{{lang={lang},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\ufcsetup{",
        f"  type={profile},",
        f"  document-language={locale},",
        "  cover=true,",
        f"  coat-of-arms={enabled},",
        f"  coat-of-arms-file={{{asset_path(case)}}},",
        "  author={Synthetic Cover Author},",
        "  title={Synthetic Cover Title},",
        "  institution={Synthetic Institute},",
        "  location={Fortaleza},",
        "  year={2026},",
        "  undergraduate-program={Synthetic Computing Program},",
        "  submission-entity={Synthetic Institute}",
        "}",
        r"\begin{document}",
        r"\ufcPrintCover",
        r"\typeout{ASSET-PROBE-BABEL=\languagename}",
        r"\typeout{ASSET-PROBE-DOCUMENT=\ufcDocumentLanguage}",
        r"\end{document}",
        "",
    ])


def check_source(source: str, profile: str, locale: str, case: str) -> None:
    if source != make_source(profile, locale, case) or source.count(r"\ufcPrintCover") != 1:
        raise ValueError("missing or altered image-path source contract")


def image_dimensions(listing: str) -> list[tuple[int, int, int]]:
    """Extract image XObjects actually referenced by pages in pdfimages -list."""
    found = []
    for line in listing.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0].isdigit() and parts[1].isdigit() and parts[2] == "image":
            found.append((int(parts[0]), int(parts[3]), int(parts[4])))
    return found


def check_result(case: str, locale: str, images: list[tuple[int, int, int]], log: str) -> None:
    _, babel = LOCALES[locale]
    if log.splitlines().count(f"ASSET-PROBE-BABEL={babel}") != 1:
        raise ValueError(f"wrong Babel locale in {locale}/{case}")
    if log.splitlines().count(f"ASSET-PROBE-DOCUMENT={locale}") != 1:
        raise ValueError(f"wrong public language value in {locale}/{case}")
    warned = bool(WARNING.search(log))
    if case in SIZES:
        if images != [(1, *SIZES[case])] or warned:
            raise ValueError(f"wrong actual rendered image or warning: {case} {images}")
    elif images or warned != (case == "missing"):
        raise ValueError(f"missing or disabled asset leaked into PDF: {case} {images}")


def negative_controls() -> int:
    """Mutate the same source and PDF predicates executed in production."""
    original = make_source("undergraduate-capstone", "en", "image-a")
    mutations = [
        original.replace("coat-of-arms=true", "coat-of-arms=false", 1),
        original.replace("image-a.png", "missing-image.png", 1),
        original.replace(r"\ufcPrintCover", "", 1),
        original.replace("document-language=en", "document-language=fr", 1),
    ]
    count = 0
    for source in mutations:
        if source == original:
            raise ValueError("ineffective source mutation")
        try:
            check_source(source, "undergraduate-capstone", "en", "image-a")
        except ValueError:
            count += 1
        else:
            raise ValueError("source mutation was accepted")
    good = "ASSET-PROBE-BABEL=english\nASSET-PROBE-DOCUMENT=en\n"
    valid = [(1, 19, 13)]
    check_result("image-a", "en", valid, good)
    check_result("disabled", "en", [], good)
    check_result("missing", "en", [],
                 good + "Class abntexto-ufc Warning: UFC coat of arms asset not found\n")
    bad = [
        ("image-a", "en", [], good),
        ("image-a", "en", [(1, 23, 17)], good),
        ("image-a", "en", valid + valid, good),
        ("disabled", "en", valid, good),
        ("missing", "en", [], good),
        ("image-a", "en", valid, good.replace("BABEL=english", "BABEL=french")),
        ("image-a", "en", valid, good.replace("DOCUMENT=en", "DOCUMENT=pt")),
    ]
    for case in bad:
        try:
            check_result(*case)
        except ValueError:
            count += 1
        else:
            raise ValueError("PDF mutation was accepted")
    if count != 11:
        raise ValueError(f"incorrect negative mutation count: {count}")
    return count


def command(args: list[str], log_file: Path | None = None) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if log_file:
        log_file.write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        raise ValueError(f"command failed: {args}: {result.stdout[-450:]} {result.stderr[-450:]}")
    return result.stdout


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    negatives = negative_controls()
    if args.preflight:
        for locale in LOCALES:
            for profile in PROFILES:
                for case in CASES:
                    check_source(make_source(profile, locale, case), profile, locale, case)
        print(f"COAT-PATH-PREFLIGHT status=PASS sources=32 negatives={negatives}")
        return
    expected_sha = os.getenv("SOURCE_COMMIT_SHA")
    source_sha = command(["git", "rev-parse", "HEAD"]).strip()
    if expected_sha and expected_sha != source_sha:
        raise ValueError("checked-out SHA does not match CI request")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for case, (width, height) in SIZES.items():
        (OUTPUT / (case + ".png")).write_bytes(
            synthetic_png(width, height, 11 if case == "image-a" else 37))
    if (OUTPUT / "missing-image.png").exists():
        raise ValueError("negative fixture path unexpectedly exists")
    entries = []
    for locale in LOCALES:
        for profile in PROFILES:
            for case in CASES:
                name = f"coat-{profile}-{locale}-{case}"
                source = make_source(profile, locale, case)
                check_source(source, profile, locale, case)
                tex = OUTPUT / (name + ".tex")
                tex.write_text(source, encoding="utf-8")
                command(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                         "-file-line-error", f"-jobname={name}",
                         f"-output-directory={OUTPUT}", str(tex)],
                        OUTPUT / (name + "-pdflatex.log"))
                pdf = OUTPUT / (name + ".pdf")
                log_path = OUTPUT / (name + ".log")
                if not pdf.is_file() or pdf.stat().st_size == 0 or not log_path.is_file():
                    raise ValueError(f"actual PDF or TeX log missing: {name}")
                log = log_path.read_text(encoding="utf-8", errors="replace")
                command(["qpdf", "--check", str(pdf)])
                image_list = command(["pdfimages", "-list", str(pdf)])
                images = image_dimensions(image_list)
                check_result(case, locale, images, log)
                entries.append({"name": name, "locale": locale, "profile": profile,
                                "case": case, "images": images,
                                "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                                "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                                "warning": bool(WARNING.search(log)), "status": "PASS"})
                print(f"COAT-PATH status=PASS locale={locale} profile={profile}"
                      f" case={case} images={len(images)}", flush=True)
    for locale in LOCALES:
        for profile in PROFILES:
            group = {item["case"]: item for item in entries
                     if item["locale"] == locale and item["profile"] == profile}
            if group["image-a"]["pdf_sha256"] == group["image-b"]["pdf_sha256"]:
                raise ValueError("switching custom assets left identical PDFs")
    if len(entries) != 32:
        raise ValueError("incomplete real-PDF coverage")
    manifest = {"source_sha": source_sha, "real_pdfs": len(entries),
                "negative_controls": negatives, "entries": entries}
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                           encoding="utf-8")
    print("COAT-PATH status=PASS real_pdfs=32 profiles=2 locales=4"
          " cases=4 negative_controls=11 sha256=PASS")


if __name__ == "__main__":
    main()

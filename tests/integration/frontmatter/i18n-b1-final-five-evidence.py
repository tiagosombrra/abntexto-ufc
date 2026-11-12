#!/usr/bin/env python3
"""Exercise the five remaining B1 options/core getters in real locale PDFs.

Cross-check existing positive catalog insertion; compile the disabled branch,
two font families, strict/non-strict results, initial-page valid/invalid,
and both PDFTeX/LuaTeX mathematical-font policies. This is bounded evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "artifacts/integrated-i18n"
LANGS = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PENDING_FIVE = ("catalog-card", "font", "strict-font", "initial-page",
                r"\ufcMathFontPolicy")
MARKER = "B1FIVEBODYMARKER"
POLICY = "B1-MATH-POLICY="
FONT = "B1-FONT-MARKER"


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def command(args: list[str], *, allow_error: bool = False) -> tuple[int, str]:
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", check=False)
    if not allow_error:
        require(p.returncode == 0,
                "B1 command failed " + args[0] + ": " +
                (p.stdout + p.stderr)[-850:])
    return p.returncode, p.stdout + p.stderr


def pages(pdf: Path) -> list[str]:
    count = re.search(r"(?m)^Pages:\s*(\d+)$", command(
        ["pdfinfo", str(pdf)])[1])
    require(count is not None, "PDF physical page count absent")
    extracted = command(["pdftotext", "-layout", str(pdf), "-"])[1]
    parts = extracted.split("\f")
    if parts and not parts[-1].strip():
        parts.pop()
    require(len(parts) == int(count.group(1)),
            "B1 physical page count omits empty duplex pages")
    return parts


def check_marked_pages(pages_: list[str], token: str, exists: bool) -> list[int]:
    indices = [i + 1 for i, p in enumerate(pages_) if token in p]
    require((len(indices) == 1) if exists else not indices,
            f"unexpected actual PDF marker count: {token}")
    return indices


def compile_tex(locale: str, job: str, content: str,
                *, engine: str = "pdflatex",
                expected_error: str | None = None) -> dict:
    folder = BASE / locale / "b1-final-five"
    folder.mkdir(parents=True, exist_ok=True)
    tex = folder / f"{job}.tex"
    tex.write_text(content, encoding="utf-8")
    pdf = folder / f"{job}.pdf"
    args = [engine, "-interaction=nonstopmode", "-halt-on-error",
            "-file-line-error", f"-jobname={job}",
            f"-output-directory={folder}", str(tex)]
    rc, stdout = command(args, allow_error=True)
    log = folder / f"{job}.log"
    require(log.is_file(), "B1 font/page log missing")
    if expected_error:
        # TeX may split one class-error word across lines (e.g. "Roma\\nn").
        # Match the complete error after removing whitespace, not arbitrary fragments.
        error_text = re.sub(r"\\s+", "", stdout + log.read_text(errors="replace"))
        error_expected = re.sub(r"\\s+", "", expected_error)
        require(rc != 0
                and "Classabntexto-ufcError:" in error_text
                and error_expected.lower() in error_text.lower(),
                "expected strict-font/initial-page class rejection not observed")
        return {"job": job, "source_sha256": digest(tex),
                "log_sha256": digest(log),
                "expected_rejection": expected_error, "verified": True}
    require(rc == 0 and pdf.is_file() and pdf.stat().st_size > 1000,
            "B1 successful PDF compilation was absent: " + stdout[-700:])
    command(["qpdf", "--check", str(pdf)])
    physical = pages(pdf)
    return {"job": job, "source_sha256": digest(tex),
            "pdf_sha256": digest(pdf), "log_sha256": digest(log),
            "pdf_pages": len(physical), "verified": True}


def main_source(locale: str, font: str, *, strict: bool = False,
                initial_page: int | None = None) -> str:
    require(locale in LANGS and font in ("times", "arial"),
            "invalid B1 text font case")
    setup = (f"type=scientific-article,document-language={locale},"
             f"font={font},strict-font={'true' if strict else 'false'},"
             "cover=false,catalog-card=false,coat-of-arms=false")
    if initial_page is not None:
        setup += f",initial-page={initial_page}"
    return "\n".join((
        rf"\DocumentMetadata{{lang={LANGS[locale]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{{setup}}}",
        r"\begin{document}",
        r"\textual",
        r"\thispagestyle{plain}",
        rf"\typeout{{{POLICY}\ufcMathFontPolicy}}",
        rf"\typeout{{B1-INITIAL-PAGE=\thepage}}",
        rf"\section{{{FONT}}}",
        rf"{MARKER} \(\int_0^1 x^2\, dx\).",
        r"\end{document}",
        "",
    ))


def font_effect(font: str, log: str, listing: str) -> dict:
    if font == "times":
        literal = "Using literal Times New Roman with pdfLaTeX"
        compat = "Times New Roman not prepared for pdfLaTeX; using NewTX compatibility fallback"
        expected = ("TimesNewRoman", "TeXGyreTermesX")
    else:
        literal = "Using literal Arial with pdfLaTeX"
        compat = "Arial not prepared for pdfLaTeX; using TeX Gyre Heros compatibility fallback"
        expected = ("Arial", "TeXGyreHeros")
    # TeX can wrap a class info line at column 79 without changing its meaning.
    normalized_log = re.sub(r"\s+", " ", log)
    is_literal = ("Class abntexto-ufc Info: " + literal) in normalized_log
    is_compat = ("Class abntexto-ufc Info: " + compat) in normalized_log
    require(is_literal != is_compat,
            "missing, ambiguous, or forged actual class font-policy branch")
    name = expected[0] if is_literal else expected[1]
    require(name in listing, "actual PDF does not embed chosen text font family")
    require(POLICY + "NEW-TX-MATH" in log,
            "public math font getter disagrees with PDFTeX policy")
    return {"font": font, "literal": is_literal,
            "expected_embedded_name": name,
            "math_policy": "NEW-TX-MATH"}


def catalog_case(locale: str, sha: str) -> dict:
    folder = BASE / locale / "pretextual-commands"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("source_sha") == sha
            and manifest.get("locale") == locale
            and manifest.get("status") == "BOUNDED_REAL_PDF_PASS",
            "B2 original positive catalog manifest does not match source")
    records = [r for r in manifest["records"] if r["case"] == "catalog"]
    require(len(records) == 1, "no unique real catalog case")
    row = records[0]
    tex = folder / (row["job"] + ".tex")
    pdf = folder / (row["job"] + ".pdf")
    require(digest(tex) == row["tex_sha256"]
            and digest(pdf) == row["pdf_sha256"],
            "B2 positive catalog original PDF/source SHA mismatch")
    source = tex.read_text(encoding="utf-8")
    require(source.count("catalog-card=true") == 1
            and source.count(r"\ufcPrintCatalogCard{") == 1,
            "source does not enable real catalog option")
    original_pages = pages(pdf)
    original_page = check_marked_pages(original_pages, "CATALOGPROBETEXT", True)
    require(original_page == [row["marker_page"]],
            "B2 original catalog physical page receipt drifted")
    disabled = source.replace("catalog-card=true", "catalog-card=false", 1)
    receipt = compile_tex(locale, f"b1-{locale}-catalog-disabled", disabled)
    new_pdf = BASE / locale / "b1-final-five" / (receipt["job"] + ".pdf")
    absent_pages = pages(new_pdf)
    check_marked_pages(absent_pages, "CATALOGPROBETEXT", False)
    require(len(original_pages) == len(absent_pages) + 1,
            "catalog option did not insert one physical PDF page")
    check_marked_pages(original_pages, "POSTBODYMARKER", True)
    check_marked_pages(absent_pages, "POSTBODYMARKER", True)
    return {"identifier": "catalog-card", "locale": locale,
            "enabled_pdf_sha256": row["pdf_sha256"],
            "enabled_source_sha256": row["tex_sha256"],
            "enabled_marker_page": original_page[0],
            "disabled": receipt, "positive_negative": "REAL_PDF",
            "verified": True}


def negatives() -> int:
    cases = [
        (["COVER", "CATALOGPROBETEXT", "BODY"], "CATALOGPROBETEXT", True),
        (["COVER", "BODY"], "CATALOGPROBETEXT", False),
        (["COVER", "", "BODY"], "BODY", True),
    ]
    for pg, token, state in cases:
        check_marked_pages(pg, token, state)
    alterations = [
        (["COVER", "MISSING", "BODY"], "CATALOGPROBETEXT", True),
        (["COVER", "CATALOGPROBETEXT", "BODY"], "CATALOGPROBETEXT", False),
        (["CATALOGPROBETEXT", "CATALOGPROBETEXT"], "CATALOGPROBETEXT", True),
        (["COVER", "", "BODY"], "CATALOGPROBETEXT", True),
    ]
    count = 0
    for pg, token, state in alterations:
        try:
            check_marked_pages(pg, token, state)
        except ValueError:
            count += 1
        else:
            raise ValueError("catalog missing/duplicate mutant escaped")
    require(len(PENDING_FIVE) == len(set(PENDING_FIVE)) == 5,
            "remaining five B1 identifier drift")
    require(count == 4, "remaining B1 negatives drift")
    return count


def run(locale: str) -> None:
    sha = command(["git", "rev-parse", "HEAD"])[1].strip()
    require(os.getenv("SOURCE_COMMIT_SHA") in (None, sha),
            "B1 remaining suite checkout SHA mismatch")
    folder = BASE / locale / "b1-final-five"
    results: dict[str, object] = {"catalog-card": catalog_case(locale, sha)}
    for font in ("times", "arial"):
        job = f"b1-{locale}-font-{font}"
        source = main_source(locale, font)
        result = compile_tex(locale, job, source)
        pdf = folder / (job + ".pdf")
        text = "\n".join(pages(pdf))
        require(MARKER in text and FONT in text,
                "requested text/math font case missing visible PDF body")
        log = (folder / (job + ".log")).read_text(errors="replace")
        listing = command(["pdffonts", str(pdf)])[1]
        info = font_effect(font, log, listing)
        result.update(info)
        results.setdefault("font", []).append(result)
        strict_source = main_source(locale, font, strict=True)
        literal = info["literal"]
        strict_result = compile_tex(
            locale, job + "-strict", strict_source,
            expected_error=None if literal else
            ("Times New Roman" if font == "times" else "Arial"))
        results.setdefault("strict-font", []).append(strict_result)
    # The initial page is a logical counter: check both log and actual page footer.
    initial_job = f"b1-{locale}-initial-101"
    initial = compile_tex(locale, initial_job,
                          main_source(locale, "times", initial_page=101))
    init_log = (folder / (initial_job + ".log")).read_text(errors="replace")
    require("B1-INITIAL-PAGE=101" in init_log,
            "initial-page=101 not applied to public page counter")
    init_pdf = folder / (initial_job + ".pdf")
    extracted = pages(init_pdf)
    require(MARKER in "".join(extracted)
            and re.search(r"(?m)^\s*101\s*$", extracted[0]),
            "initial-page 101 absent from actual PDF physical page footer")
    results["initial-page"] = {
        "positive": initial,
        "negative": compile_tex(
            locale, f"b1-{locale}-initial-invalid",
            main_source(locale, "times", initial_page=0),
            expected_error="Invalid initial-page"),
    }
    # Verify the public getter also chooses an installed OpenType math font.
    lua_job = f"b1-{locale}-math-lua"
    lua = compile_tex(locale, lua_job, main_source(locale, "times"),
                      engine="lualatex")
    lua_log = (folder / (lua_job + ".log")).read_text(errors="replace")
    policy = re.search(r"(?m)^" + re.escape(POLICY) +
                       r"(TEX-GYRE-TERMES-MATH|LATIN-MODERN-MATH)\s*$",
                       lua_log)
    require(policy is not None,
            "LuaLaTeX public math policy absent or unknown")
    lua_fonts = command(["pdffonts", str(folder / (lua_job + ".pdf"))])[1]
    expected_font = ("TeXGyreTermesMath" if policy.group(1) ==
                     "TEX-GYRE-TERMES-MATH" else "LatinModernMath")
    require(expected_font in lua_fonts,
            "LuaTeX public math font policy disagrees with PDF embedded fonts")
    lua.update({"math_policy": policy.group(1),
                "math_embedded_font": expected_font})
    results[r"\ufcMathFontPolicy"] = {"pdflatex_policy": "NEW-TX-MATH",
                                    "lualatex": lua}
    report = {
        "status": "BOUNDED_FIVE_B1_REAL_PDF_PASS",
        "source_sha": sha, "locale": locale,
        "identifiers": list(PENDING_FIVE), "negatives": negatives(),
        "certified_evidence": results, "human_normative_review": "PENDING",
        "ledger_promotion": "NOT_AUTOMATIC",
        "publication_authorized": False,
    }
    (folder / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"I18N-B1-FINAL status=PASS locale={locale} identifiers=5"
          " pdftex_luatex=PASS strict_font=PASS catalog=PASS"
          " initial_page=PASS real_PDF_and_SHA=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LANGS))
    args = parser.parse_args()
    count = negatives()
    if args.preflight:
        print(f"I18N-B1-FINAL-PREFLIGHT status=PASS ids=5 negatives={count}"
              " real_PDF=PENDING")
    elif args.locale:
        run(args.locale)
    else:
        raise ValueError("choose --preflight or --locale")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError,
            subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise SystemExit(f"I18N-B1-FINAL status=FAIL reason={exc}") from exc

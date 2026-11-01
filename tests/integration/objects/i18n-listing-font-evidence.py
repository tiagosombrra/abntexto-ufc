#!/usr/bin/env python3
"""Bounded real-PDF checks for listing, math-font policy, and strict-font.

This is one pdfLaTeX profile per locale, not a complete font/platform audit.
Literal Windows font availability is environment-dependent and reported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "artifacts/i18n-listing-font"
LOCALES = {
    "pt": ("pt-BR", "brazilian"),
    "en": ("en-US", "english"),
    "es": ("es-ES", "spanish"),
    "fr": ("fr-FR", "french"),
}
MATH = "NEW-TX-MATH"
REQUIRED_ARIAL = (
    "abntexto-ufc-winfonts-ready.tex", "t1arial.fd", "ts1arial.fd",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def token(locale: str, prefix: str) -> str:
    return f"{prefix}{locale.upper()}AA"


def whole(text: str, value: str) -> int:
    return len(re.findall(r"(?<!\w)" + re.escape(value) + r"(?!\w)", text))


def required_log_record(log: str, label: str, value: str) -> None:
    records = [line.strip() for line in log.splitlines() if label in line]
    if records != [f"{label}={value}"]:
        raise ValueError(f"missing, malformed or contradictory {label} log record")


def pdf_catalog_language(pdf: Path) -> str:
    raw = subprocess.check_output(
        ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)], cwd=ROOT, text=True
    )
    entries = json.loads(raw)["qpdf"]
    if len(entries) != 2 or entries[0].get("jsonversion") != 2:
        raise ValueError("unexpected qpdf JSON format")
    objects = entries[1]
    root = objects["trailer"]["value"]["/Root"]
    if not re.fullmatch(r"[1-9]\d* \d+ R", root):
        raise ValueError("invalid PDF catalog reference")
    catalog = objects["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog" or not isinstance(catalog.get("/Lang"), str):
        raise ValueError("PDF catalog or language is invalid")
    lang = catalog["/Lang"]
    if not lang.startswith("u:"):
        raise ValueError("PDF catalog language is not a Unicode string")
    return lang[2:]


def pdf_bbox_tokens(pdf: Path) -> tuple[set[str], int]:
    xml = subprocess.check_output(
        ["pdftotext", "-bbox-layout", str(pdf), "-"], cwd=ROOT
    )
    root = ET.fromstring(xml)
    words: set[str] = set()
    pages = 0
    for node in root.iter():
        kind = node.tag.rsplit("}", 1)[-1]
        if kind == "page":
            pages += 1
            width, height = float(node.attrib["width"]), float(node.attrib["height"])
            if abs(width - 595.28) > 2 or abs(height - 841.89) > 2:
                raise ValueError("non-A4 PDF page")
        elif kind == "word":
            words.add("".join(node.itertext()).strip())
    if not pages:
        raise ValueError("PDF has no pages")
    return words, pages


def source_tex(locale: str, cpp: Path) -> str:
    lang, _ = LOCALES[locale]
    rel = cpp.relative_to(ROOT).as_posix()
    return "\n".join([
        rf"\DocumentMetadata{{lang={lang},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{type=undergraduate-capstone,document-language={locale},"
        r"font=times,strict-font=false,code=listings,cover=false,coat-of-arms=false}",
        r"\begin{document}",
        r"\typeout{LISTFONT-BABEL=\languagename}",
        r"\typeout{LISTFONT-MATH=\ufcMathFontPolicy}",
        r"\typeout{LISTFONT-LANG=\ufcDocumentLanguage}",
        token(locale, "BODY"),
        r"\par\noindent\ttfamily\ufcMathFontPolicy\par",
        r"\begin{equation}E=mc^2+\alpha\end{equation}",
        rf"\ufcInputListing[language=C++]{{{rel}}}",
        r"\end{document}", "",
    ])


def strict_tex(locale: str) -> str:
    lang, _ = LOCALES[locale]
    return "\n".join([
        rf"\DocumentMetadata{{lang={lang},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{document-language={locale},font=arial,strict-font=true}}",
        r"\begin{document}",
        token(locale, "STRICT"),
        r"\end{document}", "",
    ])


def verify_positive(locale: str, source: str, cpp: str,
                    text: str, words: set[str], log: str,
                    pdf_lang: str, pages: int) -> dict:
    if locale not in LOCALES:
        raise ValueError("unknown locale")
    lang, babel = LOCALES[locale]
    src_required = (
        rf"\DocumentMetadata{{lang={lang},",
        f"document-language={locale}", "font=times", "strict-font=false",
        "code=listings", r"\ufcMathFontPolicy", r"\begin{equation}",
    )
    if any(part not in source for part in src_required):
        raise ValueError("source fixture does not exercise required options/math API")
    if source.count(r"\ufcInputListing[language=C++]") != 1:
        raise ValueError("public listing command is missing or duplicated")
    if source.count(r"\ufcMathFontPolicy") != 2:
        raise ValueError("math policy getter must be logged and printed exactly once")
    listing = token(locale, "LIST")
    body = token(locale, "BODY")
    if f"int {listing} (" not in cpp or "return 173;" not in cpp:
        raise ValueError("C++ fixture does not contain the required compiled source")
    if pdf_lang != lang or pages < 1:
        raise ValueError("real PDF language or page count mismatch")
    for label, value in (
        ("LISTFONT-BABEL", babel),
        ("LISTFONT-LANG", locale),
        ("LISTFONT-MATH", MATH),
    ):
        required_log_record(log, label, value)
    for value in (listing, body, MATH):
        if whole(text, value) != 1 or value not in words:
            raise ValueError(f"expected exact visible PDF word is absent/duplicated: {value}")
    if whole(text, "return") != 1 or "return" not in words:
        raise ValueError("actual C++ return statement is missing from PDF")
    for other in LOCALES:
        if other != locale and any(
            whole(text, token(other, kind)) for kind in ("LIST", "BODY")
        ):
            raise ValueError("foreign-locale PDF marker detected")
    return {
        "locale": locale, "pages": pages, "listing_visible": listing,
        "body_visible": body, "math_policy_visible": MATH,
        "public_identifiers": [
            r"\ufcInputListing", r"\ufcMathFontPolicy", "strict-font",
        ],
    }


def self_test() -> None:
    rejected = 0
    for locale, (_, babel) in LOCALES.items():
        listing, body = token(locale, "LIST"), token(locale, "BODY")
        source = source_tex(locale, OUTPUT / locale / "sample.cpp")
        cpp = f"int {listing} ( ) {{ return 173; }}\n"
        visible = f"{body} {MATH} int {listing}() return 173;"
        words = {body, MATH, "int", listing, "return", "173;"}
        log = (f"LISTFONT-BABEL={babel}\nLISTFONT-LANG={locale}\n"
               f"LISTFONT-MATH={MATH}\n")
        def check(src=source, code=cpp, pdf_text=visible,
                  pdf_words=words, tex_log=log,
                  metadata=LOCALES[locale][0]):
            return verify_positive(
                locale, src, code, pdf_text, pdf_words, tex_log, metadata, 1
            )
        check()
        mutations = [
            lambda: check(src=source.replace(r"\ufcInputListing[language=C++]",
                                            r"\relax[language=C++]")),
            lambda: check(src=source.replace("strict-font=false", "strict-font=true")),
            lambda: check(src=source.replace(r"\ufcMathFontPolicy", "INVALID")),
            lambda: check(code=cpp.replace("return 173;", "return 99;")),
            lambda: check(pdf_text=visible.replace(listing, f"X{listing}X")),
            lambda: check(pdf_text=visible.replace(body, f"{body}INVALID")),
            lambda: check(pdf_text=visible.replace("return", "returns")),
            lambda: check(pdf_words=words - {listing}),
            lambda: check(pdf_words=words - {MATH}),
            lambda: check(tex_log=log + f"LISTFONT-LANG={locale}\n"),
            lambda: check(tex_log=log.replace(f"LISTFONT-MATH={MATH}",
                                              f"LISTFONT-MATH={MATH}EXTRA")),
            lambda: check(tex_log=log.replace(f"LISTFONT-BABEL={babel}",
                                              "LISTFONT-BABEL=invalid")),
            lambda: check(metadata="en-NO" if locale != "en" else "pt-BR"),
        ]
        for mutate in mutations:
            try:
                mutate()
            except ValueError:
                rejected += 1
            else:
                raise ValueError(f"negative mutant accepted for {locale}")
    print(f"I18N-LISTFONT-SELFTEST status=PASS mutants_rejected={rejected}")


def build(tex: Path, folder: Path, job: str, runs: int = 1) -> tuple[int, Path]:
    stdout = folder / (job + "-stdout.log")
    code = 0
    for _ in range(runs):
        with stdout.open("w", encoding="utf-8") as out:
            proc = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", "-jobname", job,
                 "-output-directory", str(folder), str(tex)],
                cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, check=False
            )
        code = proc.returncode
        if code:
            break
    return code, stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test:
        return
    if args.locale is None:
        raise ValueError("specify --locale or --self-test")
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    expected_sha = os.environ.get("SOURCE_COMMIT_SHA", sha)
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or sha != expected_sha:
        raise ValueError("source SHA differs from exact checkout")
    locale = args.locale
    folder = OUTPUT / locale
    folder.mkdir(parents=True, exist_ok=True)
    cpp = folder / "sample.cpp"
    cpp.write_text(f"int {token(locale, 'LIST')} ( ) {{\n    return 173;\n}}\n",
                   encoding="utf-8")
    tex = folder / "list-font.tex"
    tex.write_text(source_tex(locale, cpp), encoding="utf-8")
    code, stdout = build(tex, folder, "list-font", runs=2)
    if code:
        raise ValueError("portable listing/math compilation failed:\n" +
                         "\n".join(stdout.read_text(errors="replace").splitlines()[-35:]))
    pdf = folder / "list-font.pdf"
    if not pdf.is_file():
        raise ValueError("positive PDF was not generated")
    text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"],
                                   cwd=ROOT, text=True)
    words, pages = pdf_bbox_tokens(pdf)
    texlog = (folder / "list-font.log").read_text(errors="replace")
    receipt = verify_positive(locale, tex.read_text(encoding="utf-8"),
                              cpp.read_text(encoding="utf-8"), text, words,
                              texlog, pdf_catalog_language(pdf), pages)
    receipt.update({
        "source_sha": sha,
        "pdf_sha256": digest(pdf), "tex_sha256": digest(tex),
        "cpp_sha256": digest(cpp),
        "stdout_sha256": digest(stdout),
        "texlog_sha256": digest(folder / "list-font.log"),
    })
    # The canonical pdfLaTeX Arial readiness contract requires all three files.
    prepared = {
        name: subprocess.run(["kpsewhich", name], cwd=ROOT, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             check=False).stdout.strip()
        for name in REQUIRED_ARIAL
    }
    strict = folder / "strict-font.tex"
    strict.write_text(strict_tex(locale), encoding="utf-8")
    strict_code, strict_stdout = build(strict, folder, "strict-font")
    strict_log_path = folder / "strict-font.log"
    strict_output = strict_stdout.read_text(errors="replace")
    all_prepared = all(prepared.values())
    if all_prepared:
        if strict_code != 0 or not (folder / "strict-font.pdf").is_file():
            raise ValueError("strict Arial rejected fully prepared literal font files")
        strict_outcome = "PREPARED_LITERAL_ACCEPTED"
    else:
        if strict_code == 0:
            raise ValueError("strict-font=true accepted absent Arial support")
        if "Arial support is not prepared for pdfLaTeX" not in strict_output:
            raise ValueError("strict-font rejected for a reason other than missing Arial support")
        strict_outcome = "UNPREPARED_LITERAL_REJECTED"
    receipt.update({
        "strict_font": strict_outcome,
        "strict_source_sha256": digest(strict),
        "strict_stdout_sha256": digest(strict_stdout),
        "strict_log_sha256": digest(strict_log_path) if strict_log_path.exists() else None,
        "prepared_arial_file_count": sum(bool(x) for x in prepared.values()),
        "scope": "pdfLaTeX only; one undergraduate profile; times portable, Arial strict",
        "human_visual_linguistic_review": "PENDING",
        "font_vendor_approval": "NOT_CLAIMED",
    })
    (folder / "listing-font-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"I18N-LISTFONT status=PASS locale={locale} real_pdfs=1 "
          f"source_sha={sha} math={MATH} strict={strict_outcome} human_review=PENDING")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError,
            subprocess.CalledProcessError, ET.ParseError) as exc:
        raise SystemExit(f"I18N-LISTFONT status=FAIL reason={exc}") from exc

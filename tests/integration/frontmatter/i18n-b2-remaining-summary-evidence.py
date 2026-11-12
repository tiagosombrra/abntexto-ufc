#!/usr/bin/env python3
"""Exercise direct, optional and legacy summaries in original PDFs for B2."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
LANGS = {
    "pt": ("pt-BR", "brazilian", "RESUMO"),
    "en": ("en-US", "english", "ABSTRACT"),
    "es": ("es-ES", "spanish", "RESUMEN"),
    "fr": ("fr-FR", "french", "RÉSUMÉ"),
}
TITLE = "B2TITLEMARKER"
BODY = "B2BODYMARKER"
CASES = ("direct", "legacy", "optional")
OUTPUT = ROOT / "artifacts/integrated-i18n"


def ensure(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return re.sub(r"\s+", " ", "".join(
        c for c in value if not unicodedata.combining(c)))


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def folder(locale: str) -> Path:
    return OUTPUT / locale / "b2-summary-remaining"


def support(locale: str, case: str, key: str) -> Path:
    # Keep inputs separate across cases so optional summaries cannot mutate earlier SHA receipts.
    return folder(locale) / f"b2-{locale}-{case}-input-{key}.tex"


def doc(locale: str, case: str) -> Path:
    return folder(locale) / f"b2-{locale}-{case}.tex"


def inputs(locale: str, case: str) -> dict[str, str]:
    if case == "direct":
        return {locale: "B2DIRECT" + locale.upper() + " "
                + rf"\ufcSummaryKeywordsInLanguage{{{locale}}}{{B2DIRECTKEY{locale.upper()}}}"}
    if case == "legacy":
        return {"legacypt": r"B2LEGACYPT \ufcSummaryKeywords{B2LEGACYPTKEY}",
                "legacyen": r"B2LEGACYEN \keywords{B2LEGACYENKEY}"}
    if case == "optional" and locale in ("es", "fr"):
        return {
            locale: f"B2REQUIRED{locale.upper()}",
            "pt": "B2REQUIREDPT",
            "en": "B2OPTIONALEN",
        }
    raise ValueError("unsupported B2 summary scenario")


def make_source(locale: str, case: str) -> str:
    if locale not in LANGS or case not in CASES:
        raise ValueError("unrecognized summary locale or scenario")
    lang = LANGS[locale][0]
    if case == "direct":
        commands = rf"\ufcPrintSummaryInLanguage{{{locale}}}{{{support(locale, case, locale).relative_to(ROOT).as_posix()}}}"
    elif case == "legacy":
        commands = "\n".join((
            rf"\ufcPrintSummary{{{support(locale, case, 'legacypt').relative_to(ROOT).as_posix()}}}",
            rf"\ufcPrintAbstract{{{support(locale, case, 'legacyen').relative_to(ROOT).as_posix()}}}",
        ))
    elif case == "optional" and locale in ("es", "fr"):
        commands = "\n".join((
            rf"\ufcPrintRequiredSummaries{{{support(locale, case, locale).relative_to(ROOT).as_posix()}}}{{{support(locale, case, 'pt').relative_to(ROOT).as_posix()}}}",
            rf"\ufcPrintOptionalEnglishSummary{{{support(locale, case, 'en').relative_to(ROOT).as_posix()}}}",
        ))
    else:
        raise ValueError("optional summary only applies to Spanish/French")
    return "\n".join((
        rf"\DocumentMetadata{{lang={lang},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{type=doctoral-thesis,document-language={locale},cover=false,catalog-card=false,coat-of-arms=false,title={{B2 Synthetic Summary}},author={{B2 Test Author}}}}",
        r"\begin{document}",
        r"\pretextual",
        rf"\noindent {TITLE}\clearpage",
        commands,
        r"\textual",
        rf"\section{{{BODY}}}",
        r"\typeout{B2-SUMMARY-BABEL=\languagename}",
        r"\end{document}", "",
    ))


def expected_markers(locale: str, case: str) -> dict[str, str]:
    if case == "direct":
        return {"B2DIRECT" + locale.upper(): LANGS[locale][2],
                "B2DIRECTKEY" + locale.upper(): LANGS[locale][2]}
    if case == "legacy":
        return {"B2LEGACYPT": "RESUMO", "B2LEGACYEN": "ABSTRACT"}
    if case == "optional" and locale in ("es", "fr"):
        return {"B2REQUIRED" + locale.upper(): LANGS[locale][2],
                "B2REQUIREDPT": "RESUMO", "B2OPTIONALEN": "ABSTRACT"}
    raise ValueError("unsupported B2 summary marker case")


def assert_pdf_output(locale: str, case: str, source: str, pages: list[str],
                      lang: str, babel_log: str) -> dict:
    ensure(source == make_source(locale, case),
           "B2 summary source mutated or missing public API")
    ensure(lang == LANGS[locale][0], "B2 PDF /Root/Lang mismatch")
    ensure(f"B2-SUMMARY-BABEL={LANGS[locale][1]}" in babel_log,
           "B2 summary Babel language mismatch")
    ensure(len(pages) >= 3 and fold(TITLE) in fold(pages[0])
           and fold(BODY) in fold(pages[-1]),
           "B2 summary missing title/body physical-page bracket")
    findings = {}
    for marker, heading in expected_markers(locale, case).items():
        hits = [index for index, page in enumerate(pages)
                if fold(marker) in fold(page)]
        ensure(len(hits) == 1 and 0 < hits[0] < len(pages) - 1,
               "B2 summary marker duplicated, absent or outside pretextual pages")
        ensure(fold(heading) in fold(pages[hits[0]]),
               f"B2 summary heading missing from marker page: {marker}")
        findings[marker] = {"page_number": hits[0] + 1, "heading": heading}
    return findings


def negative_controls() -> int:
    count = 0
    for locale in LANGS:
        for case in CASES:
            if case == "optional" and locale not in ("es", "fr"):
                continue
            original = make_source(locale, case)
            pages = [TITLE] + [marker + " " + heading
                for marker, heading in expected_markers(locale, case).items()] + [BODY]
            assert_pdf_output(locale, case, original, pages,
                              LANGS[locale][0],
                              "B2-SUMMARY-BABEL=" + LANGS[locale][1])
            mutations = [
                (original.replace(r"\ufcPrint", r"\relax", 1), pages, LANGS[locale][0]),
                (original, [TITLE] + ["REMOVED"] + pages[2:], LANGS[locale][0]),
                (original, pages, "pt-BR" if locale != "pt" else "en-US"),
            ]
            for src, pg, lang in mutations:
                try:
                    assert_pdf_output(locale, case, src, pg, lang,
                                      "B2-SUMMARY-BABEL=" + LANGS[locale][1])
                except ValueError:
                    count += 1
                else:
                    raise ValueError(f"B2 remaining negative escaped {locale}/{case}")
    ensure(count == 30, "B2 remaining negative count drift")
    # Every distinct case/input key must resolve to a unique source path.
    all_inputs = [
        support(locale, case, key)
        for locale in LANGS
        for case in CASES
        if case != "optional" or locale in ("es", "fr")
        for key in inputs(locale, case)
    ]
    ensure(len(all_inputs) == 18 and len(set(all_inputs)) == len(all_inputs),
           "B2 summary inputs collide across scenarios")
    return count


def run(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    ensure(proc.returncode == 0,
           f"B2 external command failed ({args[0]}): {proc.stderr[-400:]} {proc.stdout[-700:]}")
    return proc.stdout


def pdf_language(pdf: Path) -> str:
    data = json.loads(run(["qpdf", "--json=2", "--json-key=qpdf", str(pdf)]))["qpdf"]
    ensure(len(data) == 2 and data[0].get("jsonversion") == 2,
           "unknown qpdf /Root schema")
    root = data[1]["trailer"]["value"]["/Root"]
    catalog = data[1]["obj:" + root]["value"]
    ensure(catalog["/Type"] == "/Catalog", "PDF root type mismatch")
    value = catalog.get("/Lang")
    ensure(isinstance(value, str) and value.startswith("u:"),
           "PDF /Root/Lang missing")
    return value[2:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LANGS))
    args = parser.parse_args()
    negatives = negative_controls()
    if args.preflight:
        print(f"I18N-B2-SUMMARY-PREFLIGHT status=PASS scenarios=10 negatives={negatives}")
        return
    ensure(args.locale in LANGS, "locale required")
    locale = args.locale
    sha = run(["git", "rev-parse", "HEAD"]).strip()
    ensure(os.getenv("SOURCE_COMMIT_SHA") in (None, sha),
           "checkout SHA not equal to requested source")
    out = folder(locale)
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for case in CASES:
        if case == "optional" and locale not in ("es", "fr"):
            continue
        inp = inputs(locale, case)
        for key, value in inp.items():
            support(locale, case, key).write_text(value + "\n", encoding="utf-8")
        source = make_source(locale, case)
        tex = doc(locale, case)
        tex.write_text(source, encoding="utf-8")
        pdf = tex.with_suffix(".pdf")
        log = tex.with_suffix(".log")
        for _ in range(2):
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", f"-jobname={tex.stem}",
                 f"-output-directory={out}", str(tex)])
        ensure(pdf.is_file() and log.is_file(), "missing real B2 summary PDF/log")
        run(["qpdf", "--check", str(pdf)])
        extracted = run(["pdftotext", "-layout", str(pdf), "-"])
        pages = [p for p in extracted.split("\f") if p.strip()]
        observations = assert_pdf_output(
            locale, case, source, pages, pdf_language(pdf),
            log.read_text(encoding="utf-8", errors="replace"))
        records.append({
            "case": case, "locale": locale, "verified": True,
            "commands": ({
                "direct": [r"\ufcPrintSummaryInLanguage"],
                "legacy": [r"\ufcPrintSummary", r"\ufcPrintAbstract"],
                "optional": [r"\ufcPrintOptionalEnglishSummary"],
            })[case],
            "tex_sha256": checksum(tex), "pdf_sha256": checksum(pdf),
            "log_sha256": checksum(log),
            "input_sha256": {key: checksum(support(locale, case, key)) for key in inp},
            "pdf_pages": len(pages), "markers": observations,
            "catalog_lang": LANGS[locale][0],
        })
        print(f"I18N-B2-SUMMARY status=PASS locale={locale} case={case}"
              f" pages={len(pages)}", flush=True)
    report = {
        "status": "BOUNDED_REAL_PDF_PASS", "source_sha": sha, "locale": locale,
        "negative_controls": negatives, "records": records,
        "global_i18n": "PENDING", "human_normative_linguistic_review": "PENDING",
    }
    (out / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"I18N-B2-SUMMARY status=PASS locale={locale} cases={len(records)}"
          f" negatives={negatives} human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise SystemExit(f"I18N-B2-SUMMARY status=FAIL reason={exc}") from exc

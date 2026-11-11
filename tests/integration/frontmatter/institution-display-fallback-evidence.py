#!/usr/bin/env python3
"""Verify legal-vs-display institution fallback in real PDF frontmatter.

Two profiles, six configuration branches and four locales. This bounded
functional proof does not approve translations or institutional compliance.
"""
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
OUT = ROOT / "artifacts/integrated-i18n"
LOCALES = {
    "pt": ("pt-BR", "brazilian", "Universidade Federal do Ceará"),
    "en": ("en-US", "english", "Federal University of Ceará"),
    "es": ("es-ES", "spanish", "Universidad Federal de Ceará"),
    "fr": ("fr-FR", "french", "Université fédérale du Ceará"),
}
PROFILES = ("undergraduate-capstone", "research-project")
CASES = ("default", "institution-legal", "institution-display",
         "submission-legal", "submission-display", "all-explicit")
LEGAL_DEFAULT = "Universidade Federal do Ceará"
LEGAL_INST = "EXPLICIT LEGAL INSTITUTION BRAVO"
DISPLAY_INST = "EXPLICIT DISPLAY INSTITUTION CHARLIE"
LEGAL_SUB = "EXPLICIT LEGAL SUBMISSION DELTA"
DISPLAY_SUB = "EXPLICIT DISPLAY SUBMISSION ECHO"
AUTHOR = "SYNTHETIC AUTHOR"
TITLE = "SYNTHETIC FALLBACK VERIFICATION"


def config(case: str) -> dict[str, str]:
    options = {
        "default": {},
        "institution-legal": {"institution": LEGAL_INST},
        "institution-display": {"institution-display": DISPLAY_INST},
        "submission-legal": {"submission-entity": LEGAL_SUB},
        "submission-display": {"submission-entity-display": DISPLAY_SUB},
        "all-explicit": {"institution": LEGAL_INST, "institution-display": DISPLAY_INST,
                         "submission-entity": LEGAL_SUB,
                         "submission-entity-display": DISPLAY_SUB},
    }
    if case not in options:
        raise ValueError("unknown institutional configuration")
    return options[case]


def expected(locale: str, case: str) -> tuple[str, str, str, str]:
    if locale not in LOCALES:
        raise ValueError("unknown locale")
    values = config(case)
    inst = values.get("institution", LEGAL_DEFAULT)
    submission = values.get("submission-entity", LEGAL_DEFAULT)
    display_inst = values.get("institution-display", values.get("institution", LOCALES[locale][2]))
    display_sub = values.get("submission-entity-display", values.get("submission-entity", display_inst))
    return display_inst, display_sub, inst, submission


def make_source(locale: str, profile: str, case: str) -> str:
    if locale not in LOCALES or profile not in PROFILES:
        raise ValueError("unknown profile or locale")
    options = [
        f"type={profile}", f"document-language={locale}",
        "coat-of-arms=false", "cover=true", "catalog-card=false",
        f"author={{{AUTHOR}}}", f"title={{{TITLE}}}",
        "location={Fortaleza}", "year={2026}", "advisor={SYNTHETIC ADVISOR}",
    ]
    if profile == "research-project":
        options += ["project-program={SYNTHETIC RESEARCH PROGRAM}",
                    "project-type={SYNTHETIC RESEARCH PROJECT}"]
    else:
        options += ["undergraduate-program={SYNTHETIC COMPUTER SCIENCE}",
                    "undergraduate-degree={SYNTHETIC BACHELOR DEGREE}"]
    options += [f"{key}={{{value}}}" for key, value in config(case).items()]
    return "\n".join([
        rf"\DocumentMetadata{{lang={LOCALES[locale][0]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}", r"\ufcsetup{",
        "  " + ",\n  ".join(options), "}", r"\begin{document}",
        r"\ufcPrintCover", r"\ufcPrintTitlePage",
        r"\typeout{INSTITUTION-PROBE-BABEL=\languagename}",
        r"\typeout{INSTITUTION-PROBE-LANGUAGE=\ufcDocumentLanguage}",
        r"\typeout{INSTITUTION-PROBE-LEGAL-INST=\ufcMeta{institution}}",
        r"\typeout{INSTITUTION-PROBE-LEGAL-SUB=\ufcMeta{submission-entity}}",
        r"\end{document}", "",
    ])


def assert_source(source: str, locale: str, profile: str, case: str) -> None:
    if source != make_source(locale, profile, case):
        raise ValueError("generated fixture differs from required public setup")
    if source.count(r"\ufcPrintCover") != 1 or source.count(r"\ufcPrintTitlePage") != 1:
        raise ValueError("missing or duplicated frontmatter print route")


def fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"(?<=\w)-\s+(?=\w)", "", value)
    return re.sub(r"\s+", " ", value).strip()


def contains(value: str, phrase: str) -> bool:
    return fold(phrase) in fold(value)


def validate_output(locale: str, profile: str, case: str, log: str,
                    pages: list[str], catalog_lang: str) -> None:
    if locale not in LOCALES or profile not in PROFILES or case not in CASES:
        raise ValueError("invalid result coordinates")
    display_inst, display_sub, legal_inst, legal_sub = expected(locale, case)
    if len(pages) < 2 or not all(pages[:2]):
        raise ValueError("missing real PDF cover or title page")
    if catalog_lang != LOCALES[locale][0]:
        raise ValueError("PDF catalog language differs from selected locale")
    rows = log.splitlines()
    required = (
        f"INSTITUTION-PROBE-BABEL={LOCALES[locale][1]}",
        f"INSTITUTION-PROBE-LANGUAGE={locale}",
        f"INSTITUTION-PROBE-LEGAL-INST={legal_inst}",
        f"INSTITUTION-PROBE-LEGAL-SUB={legal_sub}",
    )
    for item in required:
        if rows.count(item) != 1:
            raise ValueError(f"missing, mutated or duplicate log receipt: {item}")
    # Academic profiles display the institution; projects display the submission entity.
    display = display_sub if profile == "research-project" else display_inst
    for page, label in zip(pages[:2], ("cover", "title page")):
        if not contains(page, display) or not contains(page, AUTHOR) or not contains(page, TITLE):
            raise ValueError(f"wrong institution or author on {label}: {locale}/{profile}/{case}")
        for forbidden in ({LEGAL_INST, DISPLAY_INST, LEGAL_SUB, DISPLAY_SUB} - {display}):
            if contains(page, forbidden):
                raise ValueError(f"unexpected institutional name on {label}: {forbidden}")


def qpdf_catalog(payload: dict) -> str:
    blocks = payload.get("qpdf")
    if not isinstance(blocks, list) or len(blocks) != 2 or blocks[0].get("jsonversion") != 2:
        raise ValueError("unexpected qpdf schema")
    objects = blocks[1]
    root = objects["trailer"]["value"]["/Root"]
    if not isinstance(root, str) or not re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root):
        raise ValueError("invalid PDF root object")
    catalog = objects[f"obj:{root}"]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("PDF root is not a Catalog")
    lang = catalog.get("/Lang")
    if not isinstance(lang, str) or not lang.startswith("u:"):
        raise ValueError("PDF /Root/Lang missing")
    return lang[2:]


def page_count(info: str) -> int:
    match = re.search(r"^Pages:\s*(\d+)\s*$", info, re.M)
    if not match or int(match.group(1)) < 2:
        raise ValueError("PDF physical page count missing or too small")
    return int(match.group(1))


def negative_controls() -> int:
    locale, profile, case = "en", "research-project", "all-explicit"
    original = make_source(locale, profile, case)
    assert_source(original, locale, profile, case)
    mutations = (
        original.replace("institution-display", "removed-institution-display", 1),
        original.replace("submission-entity-display", "removed-submission-entity-display", 1),
        original.replace(r"\ufcPrintCover", "", 1),
        original.replace(r"\ufcPrintTitlePage", "", 1),
    )
    count = 0
    for mutant in mutations:
        if mutant == original:
            raise ValueError("ineffective source mutation")
        try:
            assert_source(mutant, locale, profile, case)
        except ValueError:
            count += 1
        else:
            raise ValueError("modified source passed canonical fixture contract")
    _, submission, inst, sub = expected(locale, case)
    good_log = "\n".join(("INSTITUTION-PROBE-BABEL=english", "INSTITUTION-PROBE-LANGUAGE=en",
                          f"INSTITUTION-PROBE-LEGAL-INST={inst}",
                          f"INSTITUTION-PROBE-LEGAL-SUB={sub}"))
    pages = [f"{submission} {AUTHOR} {TITLE}", f"{submission} {AUTHOR} {TITLE}"]
    validate_output(locale, profile, case, good_log, pages, "en-US")
    bad = (
        (good_log.replace(f"LEGAL-INST={inst}", "LEGAL-INST=CORRUPTED"), pages, "en-US"),
        (good_log.replace(f"LEGAL-SUB={sub}", "LEGAL-SUB=CORRUPTED"), pages, "en-US"),
        (good_log + f"\nINSTITUTION-PROBE-LEGAL-SUB={sub}", pages, "en-US"),
        (good_log.replace("BABEL=english", "BABEL=french"), pages, "en-US"),
        (good_log.replace("LANGUAGE=en", "LANGUAGE=es"), pages, "en-US"),
        (good_log, [pages[0].replace(submission, inst), pages[1]], "en-US"),
        (good_log, [pages[0], pages[1].replace(submission, sub)], "en-US"),
        (good_log, [pages[0] + " " + DISPLAY_INST, pages[1]], "en-US"),
        (good_log, [pages[0], pages[1] + " " + DISPLAY_INST], "en-US"),
        (good_log, [pages[0].replace(AUTHOR, ""), pages[1]], "en-US"),
        (good_log, [pages[0], pages[1].replace(TITLE, "")], "en-US"),
        (good_log, pages, "pt-BR"),
        (good_log, [pages[0]], "en-US"),
    )
    for corrupted_log, corrupted_pages, lang in bad:
        try:
            validate_output(locale, profile, case, corrupted_log, corrupted_pages, lang)
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid PDF/log output passed negative control")
    if count != 17:
        raise ValueError(f"unexpected negative control count: {count}")
    if len(LOCALES) * len(PROFILES) * len(CASES) != 48:
        raise ValueError("unexpected institutional coverage dimensions")
    for loc in LOCALES:
        for profile in PROFILES:
            for case in CASES:
                assert_source(make_source(loc, profile, case), loc, profile, case)
    fake = {"qpdf": [{"jsonversion": 2}, {
        "trailer": {"value": {"/Root": "1 0 R"}},
        "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:en-US"}}}]}
    if qpdf_catalog(fake) != "en-US":
        raise ValueError("positive PDF catalog control failed")
    fake["qpdf"][1]["obj:1 0 R"]["value"].pop("/Lang")
    try:
        qpdf_catalog(fake)
    except ValueError:
        count += 1
    else:
        raise ValueError("missing qpdf /Root/Lang passed negative control")
    if count != 18:
        raise ValueError("PDF catalog negative control count drift")
    return count


def run(command: list[str], log_file: Path | None = None) -> str:
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    if log_file:
        log_file.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    if proc.returncode:
        raise ValueError(f"failed command {command[0]}: {proc.stderr[-700:]} {proc.stdout[-700:]}")
    return proc.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    negatives = negative_controls()
    if args.preflight:
        print(f"INSTITUTION-FALLBACK-PREFLIGHT status=PASS sources=48 negative_controls={negatives}"
              " CI_pdf_certification=PENDING")
        return
    if not args.locale:
        raise ValueError("--locale is required outside preflight")
    source_sha = run(["git", "rev-parse", "HEAD"]).strip()
    expected_sha = os.getenv("SOURCE_COMMIT_SHA")
    if expected_sha and source_sha != expected_sha:
        raise ValueError("checked-out repository differs from CI source SHA")
    folder = OUT / args.locale / "institution-fallback"
    folder.mkdir(parents=True, exist_ok=True)
    receipts: list[dict] = []
    for profile in PROFILES:
        for case in CASES:
            name = f"institution-{args.locale}-{profile}-{case}"
            tex = folder / f"{name}.tex"
            pdf = folder / f"{name}.pdf"
            content = make_source(args.locale, profile, case)
            assert_source(content, args.locale, profile, case)
            tex.write_text(content, encoding="utf-8")
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                 f"-jobname={name}", f"-output-directory={folder}", str(tex)],
                folder / f"{name}-pdflatex.log")
            if not pdf.is_file() or not pdf.stat().st_size:
                raise ValueError(f"missing rendered PDF: {name}")
            run(["qpdf", "--check", str(pdf)])
            catalog = qpdf_catalog(json.loads(run(["qpdf", "--json=2", "--json-key=qpdf", str(pdf)])))
            count = page_count(run(["pdfinfo", str(pdf)]))
            pages = [run(["pdftotext", "-layout", "-f", str(index), "-l", str(index),
                          str(pdf), "-"]) for index in (1, 2)]
            log = (folder / f"{name}.log").read_text(encoding="utf-8", errors="replace")
            validate_output(args.locale, profile, case, log, pages, catalog)
            receipts.append({
                "profile": profile, "locale": args.locale, "case": case, "job": name,
                "expected_legal_institution": expected(args.locale, case)[2],
                "expected_legal_submission": expected(args.locale, case)[3],
                "expected_cover_institution": (expected(args.locale, case)[1]
                    if profile == "research-project" else expected(args.locale, case)[0]),
                "verified_pages": [1, 2], "pdf_pages": count,
                "pdf_catalog_lang": catalog,
                "tex_sha256": hashlib.sha256(content.encode()).hexdigest(),
                "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                "log_sha256": hashlib.sha256(log.encode()).hexdigest(),
                "predicate": "page-1-cover-and-page-2-title-log-and-PDF-catalog",
                "verified": True, "human_institutional_approval": "PENDING",
            })
            print(f"INSTITUTION-FALLBACK status=PASS locale={args.locale}"
                  f" profile={profile} case={case} pdf_pages={count}", flush=True)
    if len(receipts) != len(PROFILES) * len(CASES) or len({
        (x["profile"], x["case"]) for x in receipts}) != 12:
        raise ValueError("incomplete or duplicated locale PDF coverage")
    manifest = {
        "source_sha": source_sha, "status": "BOUNDED_REAL_PDF_FALLBACK_PASS",
        "locale": args.locale, "profiles": len(PROFILES), "cases": len(CASES),
        "real_pdfs": len(receipts), "negative_controls": negatives,
        "proof_boundary": "actual cover/title PDF and legal metadata; institutional wording requires human review",
        "human_linguistic_institutional_review": "PENDING",
        "receipts": receipts,
    }
    (folder / "manifest.json").write_text(json.dumps(
        manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INSTITUTION-FALLBACK status=PASS locale={args.locale}"
          f" real_pdfs={len(receipts)} profiles={len(PROFILES)}"
          f" cases={len(CASES)} negative_controls={negatives} pdf_catalog=PASS"
          " source_pdf_hashes=PASS human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError,
            subprocess.CalledProcessError) as error:
        raise SystemExit(f"INSTITUTION-FALLBACK status=FAIL reason={error}") from error

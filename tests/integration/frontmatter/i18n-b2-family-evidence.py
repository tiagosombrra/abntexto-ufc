#!/usr/bin/env python3
"""Audit a family of public pretextual commands in original four-locale PDFs.

A command is observed only when a source-bound invocation has a corresponding
physical PDF predicate. These are scenario-level candidates, not release approval.
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
BASE = ROOT / "artifacts/integrated-i18n"
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
TITLE = "Integrated Multilingual Document"
AUTHOR = "Integrated Test Author"
BODY = "POSTBODYMARKER"
PRETEXT_TOKENS = {
    "catalog": "CATALOGPROBETEXT",
    "dedication": "DEDICATIONPROBETEXT",
    "epigraph-short": "EPIGRAPHSHORTTEXT",
    "epigraph-long": "EPIGRAPHLONGTEXT",
}
HEADINGS = {
    "pt": ("Agradecimentos", "Errata", "BANCA EXAMINADORA"),
    "en": ("Acknowledgments", "Errata", "EXAMINING COMMITTEE"),
    "es": ("Agradecimientos", "Fe de erratas", "TRIBUNAL EXAMINADOR"),
    "fr": ("Remerciements", "Errata", "JURY D'EXAMEN"),
}
ACADEMIC = "undergraduate-capstone"
ARTICLE = "scientific-article"
# Nine observations reuse the seven already compiled integrated manuscripts.
INTEGRATED = {
    r"\ufcPrintCover": (ACADEMIC, "cover"),
    r"\ufcPrintTitlePage": (ACADEMIC, "title"),
    r"\ufcPrintApprovalPage": (ACADEMIC, "approval"),
    r"\ufcPrintAcknowledgments": (ACADEMIC, "ack"),
    r"\ufcPrintErrata": (ACADEMIC, "errata"),
    r"\ufcPrintRequiredSummaries": (ACADEMIC, "required"),
    r"\ufcSummaryKeywords": (ACADEMIC, "keywords"),
    r"\ufcSummaryKeywordsInLanguage": (ARTICLE, "article-keywords"),
    r"\ufcPrintArticleTranslatedSummary": (ARTICLE, "article-translated"),
}
# Four real cases from the previously certified #585 suite exercise three APIs.
PRETEXT = {
    r"\ufcPrintCatalogCard": ("catalog",),
    r"\ufcPrintDedication": ("dedication",),
    r"\ufcPrintEpigraph": ("epigraph-short", "epigraph-long"),
}
# The legacy/optional summary cases are checked in the companion real-PDF suite.
SUMMARY_COMMANDS = (
    r"\ufcPrintSummaryInLanguage",
    r"\ufcPrintOptionalEnglishSummary",
    r"\ufcPrintSummary",
    r"\ufcPrintAbstract",
)
TOTAL_FAMILY = 16


def fold(value: str) -> str:
    normalized = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'")
    )
    cleaned = "".join(c for c in normalized if not unicodedata.combining(c))
    return re.sub(r"-(?=\s+\w)\s+", "-", re.sub(r"\s+", " ", cleaned))


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def read_original(path: Path, expected_hash: str, allowed: Path) -> bytes:
    # A manifest must never redirect the audit outside the generated artifact root.
    resolved = path.resolve()
    ensure(resolved.is_relative_to(allowed.resolve()) and resolved.is_file(),
           "artifact missing or path escapes evidence directory")
    ensure(isinstance(expected_hash, str)
           and re.fullmatch(r"[a-f0-9]{64}", expected_hash) is not None,
           "untrusted original hash receipt")
    data = resolved.read_bytes()
    ensure(digest(data) == expected_hash, "original artifact SHA256 mismatch")
    return data


def shown_pages(pdf: Path) -> list[str]:
    proc = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          cwd=ROOT, capture_output=True, text=True, check=False)
    ensure(proc.returncode == 0, "original real PDF extraction failed")
    pages = [p for p in proc.stdout.split("\f") if p.strip()]
    ensure(len(pages) >= 3, "missing physical frontmatter/body page boundaries")
    return pages


def companion(locale: str) -> str:
    return "en" if locale == "pt" else "pt"


def source_tokens(kind: str, locale: str) -> tuple[str, ...]:
    if kind == "cover":
        return (r"\ufcPrintCover",)
    if kind == "title":
        return (r"\ufcPrintTitlePage",)
    if kind == "approval":
        return (r"\ufcPrintApprovalPage",)
    if kind == "ack":
        return (r"\ufcPrintAcknowledgments{",)
    if kind == "errata":
        return (r"\ufcPrintErrata{",)
    if kind == "required":
        return (r"\ufcPrintRequiredSummaries",)
    if kind == "keywords":
        return (r"\ufcSummaryKeywords{",)
    if kind == "article-keywords":
        return (r"\ufcSummaryKeywordsInLanguage{" + locale + "}",)
    if kind == "article-translated":
        return (r"\ufcPrintArticleTranslatedSummary{" + companion(locale) + "}",)
    raise ValueError("unknown B2 command scenario")


def visible_tokens(kind: str, locale: str) -> tuple[str, ...]:
    comp = companion(locale)
    if kind in ("cover", "title"):
        return (TITLE, AUTHOR if kind == "cover" else "Integrated Advisor")
    if kind == "approval":
        return (HEADINGS[locale][2], "Integrated Examiner 2")
    if kind == "ack":
        return (HEADINGS[locale][0],
                "INTEGRATED-AUTHORED-GRATITUDE-" + locale.upper())
    if kind == "errata":
        return (HEADINGS[locale][1],
                "INTEGRATED-AUTHORED-CORRECTIONS-" + locale.upper())
    if kind == "required":
        return ("INTEGRATED-SUMMARY-" + locale.upper() + "-MAIN",
                "INTEGRATED-SUMMARY-" + comp.upper() + "-COMPANION")
    if kind == "keywords":
        return ("keyword-" + locale + "-main",
                "keyword-" + comp + "-companion")
    if kind == "article-keywords":
        return ("keyword-" + locale + "-article",
                "keyword-" + comp + "-article")
    if kind == "article-translated":
        return ("INTEGRATED-ARTICLE-PRIMARY-" + locale.upper(),
                "INTEGRATED-ARTICLE-COMPANION-" + comp.upper())
    raise ValueError("unknown B2 visible scenario")


def verify_integrated_case(kind: str, locale: str, source: str,
                           pages: list[str]) -> dict:
    needles = source_tokens(kind, locale)
    for token in needles:
        ensure(token in source, f"public command absent from source: {kind}")
    visible = visible_tokens(kind, locale)
    texts = [fold(page) for page in pages]
    if kind == "cover":
        ensure(len(texts) >= 2 and all(fold(t) in texts[0] for t in visible),
               "physical first cover lacks authored title/author")
        matching = [0]
    elif kind == "title":
        ensure(len(texts) >= 2 and all(fold(t) in texts[1] for t in visible),
               "physical second title page lacks title/advisor")
        matching = [1]
    elif kind in ("approval", "ack", "errata"):
        matching = [i for i, page in enumerate(texts)
                    if all(fold(t) in page for t in visible)]
        ensure(len(matching) == 1 and matching[0] >= 2,
               f"missing, duplicated or misplaced same-page B2 content: {kind}")
    else:
        matching = [i for i, page in enumerate(texts)
                    if any(fold(t) in page for t in visible)]
        whole = fold("\n".join(pages))
        ensure(all(fold(t) in whole for t in visible),
               f"B2 real-PDF marker missing: {kind}")
        ensure(bool(matching), "B2 visible case lacks a physical PDF page")
    return {"scenario": kind, "page_numbers": [i + 1 for i in matching],
            "expected_markers": list(visible),
            "predicate": "source-invocation-plus-real-PDF-visible-content",
            "verified": True}


def pretext_source_token(case: str) -> str:
    return {
        "catalog": r"\ufcPrintCatalogCard{",
        "dedication": r"\ufcPrintDedication{",
        "epigraph-short": r"\ufcPrintEpigraph[short]{",
        "epigraph-long": r"\ufcPrintEpigraph[long]{",
    }[case]


def verify_pretext_case(case: str, source: str, pages: list[str]) -> int:
    ensure(pretext_source_token(case) in source,
           "pretextual case does not invoke named public command")
    target = PRETEXT_TOKENS[case]
    matched = [i for i, page in enumerate(pages) if fold(target) in fold(page)]
    ensure(len(matched) == 1 and matched[0] > 0 and matched[0] < len(pages) - 1,
           "pretextual content absent, duplicated or not between title/body")
    ensure(fold(BODY) in fold("\n".join(pages[matched[0] + 1:])),
           "pretextual command erased later body")
    if case.startswith("epigraph"):
        ensure(fold("EPIGRAPHAUTHOR") in fold(pages[matched[0]]),
               "pretextual epigraph author missing")
    return matched[0] + 1


def negative_controls() -> int:
    count = 0
    for name, (_profile, kind) in INTEGRATED.items():
        source = "\n".join(source_tokens(kind, "en"))
        markers = " ".join(visible_tokens(kind, "en"))
        pages = ["COVER", "TITLE PAGE", "CONTENT"]
        if kind == "cover":
            pages[0] = markers
        elif kind == "title":
            pages[1] = markers
        else:
            pages[2] = markers
        verify_integrated_case(kind, "en", source, pages)
        for mutation in ("source", "pdf"):
            bad_source = source.replace(source_tokens(kind, "en")[0], "")
            bad_pages = list(pages)
            bad_pages[-1 if kind not in ("cover", "title") else
                      (0 if kind == "cover" else 1)] = "REMOVED CONTENT"
            try:
                verify_integrated_case(kind, "en",
                                       bad_source if mutation == "source" else source,
                                       bad_pages if mutation == "pdf" else pages)
            except ValueError:
                count += 1
            else:
                raise ValueError(f"negative B2 control escaped: {name}/{mutation}")
    for name, cases in PRETEXT.items():
        for case in cases:
            source = pretext_source_token(case) + "example}"
            middle = PRETEXT_TOKENS[case]
            if case.startswith("epigraph"):
                middle += " EPIGRAPHAUTHOR"
            pages = [TITLE, middle, BODY]
            verify_pretext_case(case, source, pages)
            for bad_source, bad_pages in (
                (source.replace(pretext_source_token(case), ""), pages),
                (source, [TITLE, "REMOVED CONTENT", BODY]),
            ):
                try:
                    verify_pretext_case(case, bad_source, bad_pages)
                except ValueError:
                    count += 1
                else:
                    raise ValueError(f"negative pretext control escaped: {case}")
    if count != 26:
        raise ValueError(f"B2 negative control total drift: {count}")
    if len(INTEGRATED) + len(PRETEXT) + len(SUMMARY_COMMANDS) != TOTAL_FAMILY:
        raise ValueError("B2 command family cardinality drift")
    if len(set(INTEGRATED) | set(PRETEXT) | set(SUMMARY_COMMANDS)) != TOTAL_FAMILY:
        raise ValueError("duplicate B2 public command")
    return count


def verify_integrated(locale: str, sha: str) -> list[dict]:
    folder = BASE / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    ensure(manifest.get("source_sha") == sha and manifest.get("locale") == locale,
           "joined real PDF manifest differs from source checkout")
    by_profile = {row["profile"]: row for row in manifest["entries"]}
    ensure(len(by_profile) == 7, "seven-profile integrated source coverage missing")
    observations = []
    for name, (profile, kind) in INTEGRATED.items():
        row = by_profile[profile]
        ensure(row["locale"] == locale and row["pdf_catalog_lang"] == LOCALES[locale],
               "profile PDF language metadata mismatch")
        src = (ROOT / row["source"]).resolve()
        text = read_original(src, row["source_sha256"], folder).decode("utf-8")
        for support in row["support_files"]:
            text += "\n" + read_original(ROOT / support["path"],
                                         support["sha256"], folder).decode("utf-8")
        pdf = (ROOT / row["pdf"]).resolve()
        read_original(pdf, row["pdf_sha256"], folder)
        proof = verify_integrated_case(kind, locale, text, shown_pages(pdf))
        observations.append({
            "identifier": name, "locale": locale, "profile": profile,
            "source": row["source"], "source_sha256": row["source_sha256"],
            "pdf": row["pdf"], "pdf_sha256": row["pdf_sha256"],
            "pdf_catalog_lang": LOCALES[locale], **proof,
        })
    return observations


def verify_pretext(locale: str, sha: str) -> list[dict]:
    folder = BASE / locale / "pretextual-commands"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    ensure(manifest.get("source_sha") == sha and manifest.get("locale") == locale
           and manifest.get("real_pdfs") == 4
           and manifest.get("negative_controls") == 18,
           "pretext real-PDF suite provenance or mutation count invalid")
    records = {r["case"]: r for r in manifest["records"]}
    ensure(set(records) == set(PRETEXT_TOKENS), "pretext case matrix incomplete")
    observations = []
    for name, cases in PRETEXT.items():
        examples = []
        for case in cases:
            r = records[case]
            ensure(r["verified"] is True and r["catalog_lang"] == LOCALES[locale],
                   "pretext original receipt not verified for locale")
            job = r["job"]
            ensure(re.fullmatch(r"pretext-[a-z]{2}-[a-z-]+", job) is not None,
                   "unexpected pretext job name")
            tex = folder / (job + ".tex")
            pdf = folder / (job + ".pdf")
            log = folder / (job + ".log")
            source = read_original(tex, r["tex_sha256"], folder).decode("utf-8")
            read_original(log, r["log_sha256"], folder)
            read_original(pdf, r["pdf_sha256"], folder)
            page = verify_pretext_case(case, source, shown_pages(pdf))
            ensure(page == r["marker_page"],
                   "pretext page differs from original physical-page receipt")
            examples.append({"case": case, "page_number": page,
                             "tex_sha256": r["tex_sha256"],
                             "pdf_sha256": r["pdf_sha256"],
                             "log_sha256": r["log_sha256"]})
        observations.append({
            "identifier": name, "locale": locale,
            "profile": "undergraduate-capstone",
            "predicate": "isolated-source-invocation-plus-real-PDF-visible-content",
            "real_pdf_cases": examples, "verified": True,
        })
    return observations


def verify_remaining(locale: str, sha: str) -> list[dict]:
    folder = BASE / locale / "b2-summary-remaining"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    ensure(manifest.get("source_sha") == sha and manifest.get("locale") == locale
           and manifest.get("negative_controls") == 30
           and manifest.get("status") == "BOUNDED_REAL_PDF_PASS",
           "remaining B2 real-PDF provenance mismatch")
    rows = {r["case"]: r for r in manifest["records"]}
    expected_cases = {"direct", "legacy"}
    if locale in ("es", "fr"):
        expected_cases.add("optional")
    ensure(set(rows) == expected_cases, "B2 remaining summary cases incomplete")
    mapping = {
        r"\ufcPrintSummaryInLanguage": ("direct", r"\ufcPrintSummaryInLanguage"),
        r"\ufcPrintSummary": ("legacy", r"\ufcPrintSummary{"),
        r"\ufcPrintAbstract": ("legacy", r"\ufcPrintAbstract{"),
        r"\ufcPrintOptionalEnglishSummary": ("optional", r"\ufcPrintOptionalEnglishSummary"),
    }
    receipts = []
    for identifier in SUMMARY_COMMANDS:
        case, source_token = mapping[identifier]
        if case == "optional" and locale not in ("es", "fr"):
            receipts.append({
                "identifier": identifier, "locale": locale,
                "status": "NOT_APPLICABLE_IN_LOCALE",
                "reason": "English optional summary is only defined for ES/FR documents",
                "verified": True,
            })
            continue
        record = rows[case]
        ensure(record["verified"] is True
               and record.get("catalog_lang") == LOCALES[locale],
               "remaining B2 output not verified for locale")
        job = f"b2-{locale}-{case}"
        tex, pdf, log = (folder / (job + "." + ext)
                         for ext in ("tex", "pdf", "log"))
        source = read_original(tex, record["tex_sha256"], folder).decode("utf-8")
        read_original(log, record["log_sha256"], folder)
        read_original(pdf, record["pdf_sha256"], folder)
        ensure(source_token in source,
               f"missing public command in original remaining source: {identifier}")
        for key, original_hash in record["input_sha256"].items():
            ensure(re.fullmatch(r"[a-z]+", key) is not None,
                   "invalid B2 summary input name")
            read_original(folder / f"b2-{locale}-{case}-input-{key}.tex", original_hash, folder)
        pages = shown_pages(pdf)
        ensure(fold("B2TITLEMARKER") in fold(pages[0])
               and fold("B2BODYMARKER") in fold(pages[-1]),
               "remaining B2 PDF lacks title/body physical-page bracket")
        markers = record["markers"]
        ensure(isinstance(markers, dict) and markers,
               "remaining B2 case missing positive PDF markers")
        for marker, visual in markers.items():
            page = visual.get("page_number")
            ensure(isinstance(page, int) and 1 < page < len(pages)
                   and fold(marker) in fold(pages[page - 1])
                   and fold(visual["heading"]) in fold(pages[page - 1]),
                   "remaining B2 marker/heading not found on original PDF page")
        receipts.append({
            "identifier": identifier, "locale": locale,
            "status": "BOUNDED_REAL_PDF_PASS", "verified": True,
            "real_pdf_case": case,
            "tex_sha256": record["tex_sha256"],
            "pdf_sha256": record["pdf_sha256"],
            "log_sha256": record["log_sha256"],
            "markers": list(markers),
        })
    return receipts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    negatives = negative_controls()
    if args.preflight:
        print(f"I18N-B2-PREFLIGHT status=PASS candidate_commands=16"
              f" negatives={negatives} real_pdf=PENDING")
        return
    if not args.locale:
        raise ValueError("locale required")
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    ensure(os.getenv("SOURCE_COMMIT_SHA") in (None, sha),
           "evidence checkout differs from expected CI SHA")
    observations = (verify_integrated(args.locale, sha)
                    + verify_pretext(args.locale, sha)
                    + verify_remaining(args.locale, sha))
    ensure(len(observations) == 16
           and len({x["identifier"] for x in observations}) == 16,
           "B2 PDF evidence does not cover 16 distinct public commands")
    report = {
        "status": "BOUNDED_B2_CANDIDATE_EVIDENCE_PASS",
        "source_sha": sha, "locale": args.locale,
        "individual_candidate_commands": 16,
        "scoped_non_applicable_locale_receipts": sum(
            1 for row in observations if row.get("status") == "NOT_APPLICABLE_IN_LOCALE"),
        "negative_controls": negatives, "observations": observations,
        "global_acceptance": "PENDING",
        "human_normative_linguistic_review": "PENDING",
        "publication_authorized": False,
        "ledger_promotion": "NOT_AUTOMATIC",
        "proof_scope": "existing undergraduate/article joined PDFs plus isolated pretextual PDFs",
    }
    target = BASE / args.locale / "b2-family-proof.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(f"I18N-B2 status=PASS locale={args.locale} candidate_commands=16"
          f" negatives={negatives} original_PDF_sha256=PASS"
          " global_i18n=PENDING human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise SystemExit(f"I18N-B2 status=FAIL reason={exc}") from exc

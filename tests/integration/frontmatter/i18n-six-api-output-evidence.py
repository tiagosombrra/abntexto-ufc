#!/usr/bin/env python3
"""Six bounded public API probes checked against 7x4 real TeX/log/PDF outputs.

This audits actual compilation artifacts from run-integrated-locale.py; it does
not infer behavior from a source reference or certify the other public APIs.
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
ARTIFACTS = ROOT / "artifacts/integrated-i18n"
LOCALES = {
    "pt": ("pt-BR", "brazilian"),
    "en": ("en-US", "english"),
    "es": ("es-ES", "spanish"),
    "fr": ("fr-FR", "french"),
}
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
DUPLEX = {"masters-thesis", "doctoral-thesis", "anonymized-research-project"}
PROJECTS = {"research-project", "anonymized-research-project"}
GETTERS = {
    r"\ufcDocumentLanguage": "INTEGRATED-I18N-API-LANGUAGE",
    r"\ufcDocumentType": "INTEGRATED-I18N-API-TYPE",
    r"\ufcPrintMode": "INTEGRATED-I18N-API-PRINT-MODE",
    r"\ufcMeta": "INTEGRATED-I18N-API-META-TITLE",
}
BRANCHES = {
    r"\ufcIfProjectTF": "PROJECT",
    r"\ufcIfAnonymizedProjectTF": "ANON",
}
TITLE = "Integrated Multilingual Document"
TOTAL = len(PROFILES) * len(GETTERS | BRANCHES)


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def check_hash(raw: bytes, claimed: str) -> None:
    if not isinstance(claimed, str) or not re.fullmatch(r"[0-9a-f]{64}", claimed):
        raise ValueError("invalid source/PDF SHA256 receipt")
    if sha256(raw) != claimed:
        raise ValueError("source/PDF SHA256 differs from compilation receipt")


def fold(value: str) -> str:
    value = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'")
    )
    value = re.sub(r"\s+", " ", "".join(
        c for c in value if not unicodedata.combining(c)
    ))
    return re.sub(r"-(?=\s+\w)\s+", "-", value)


def expected_values(locale: str, profile: str) -> tuple[dict, dict]:
    if locale not in LOCALES or profile not in PROFILES:
        raise ValueError("invalid profile/locale pair")
    routes = {
        "PROJECT": "TRUE" if profile in PROJECTS else "FALSE",
        "ANON": "TRUE" if profile == "anonymized-research-project" else "FALSE",
    }
    values = {
        r"\ufcDocumentLanguage": locale,
        r"\ufcDocumentType": profile,
        r"\ufcPrintMode": "double-sided" if profile in DUPLEX else "single-sided",
        r"\ufcMeta": TITLE,
    }
    return values, routes


def validate_output(locale: str, profile: str, source: str, log: str,
                    pdf_text: str, catalog_language: str) -> list[dict]:
    values, routes = expected_values(locale, profile)
    bcp, babel = LOCALES[locale]
    if catalog_language != bcp:
        raise ValueError("PDF /Root/Lang mismatches primary locale")
    if f"INTEGRATED-I18N-BABEL={babel}" not in log:
        raise ValueError("TeX Babel primary locale mismatch")
    marker = f"integrated-manuscript-{locale}-{profile.replace('-', '')}"
    if marker not in fold(pdf_text):
        raise ValueError("real rendered manuscript content absent")
    if r"\ufcMeta{title}" not in source:
        raise ValueError("source omits public metadata getter")
    for name in GETTERS | BRANCHES:
        if name not in source:
            raise ValueError(f"fixture missing public command {name}")
    observations = []
    for name, marker in GETTERS.items():
        expected = values[name]
        full = f"{marker}={expected}"
        if full not in log:
            raise ValueError(f"public getter wrong: {name}: {full}")
        observations.append({
            "identifier": name, "profile": profile, "locale": locale,
            "observed_value": expected,
            "output_predicate": "exact-TeX-typeout-plus-verified-PDF-catalog-and-body",
            "pdf_catalog_lang": bcp, "verified": True,
        })
    visible = fold(pdf_text)
    for name, label in BRANCHES.items():
        expected = routes[label]
        other = "FALSE" if expected == "TRUE" else "TRUE"
        if f"INTEGRATED-I18N-{label}={expected}" not in log:
            raise ValueError(f"correct public conditional log branch missing: {name}")
        if f"INTEGRATED-I18N-{label}={other}" in log:
            raise ValueError(f"wrong conditional log branch executed: {name}")
        expected_text = f"integrated-{label.lower()}-{expected.lower()}-{locale}"
        bad_text = f"integrated-{label.lower()}-{other.lower()}-{locale}"
        if expected_text not in visible or bad_text in visible:
            raise ValueError(f"wrong real PDF conditional branch: {name}")
        observations.append({
            "identifier": name, "profile": profile, "locale": locale,
            "observed_value": expected,
            "output_predicate": "exact-TeX-branch-plus-rendered-PDF-branch-and-negative",
            "pdf_catalog_lang": bcp, "verified": True,
        })
    if len(observations) != 6:
        raise ValueError("expected six public API probes per real PDF")
    return observations


def catalog_language(payload: dict) -> str:
    blocks = payload.get("qpdf")
    if not isinstance(blocks, list) or len(blocks) != 2:
        raise ValueError("invalid qpdf v2 document")
    if blocks[0].get("jsonversion") != 2:
        raise ValueError("qpdf schema drift")
    data = blocks[1]
    root = data["trailer"]["value"]["/Root"]
    if not isinstance(root, str) or not re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root):
        raise ValueError("PDF /Root missing")
    catalog = data["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("PDF root is not a catalog")
    value = catalog.get("/Lang")
    if not isinstance(value, str) or not value.startswith("u:"):
        raise ValueError("PDF /Root/Lang missing or not Unicode")
    return value[2:]


def controlled_case() -> tuple[str, str, str]:
    source = "\n".join([r"\ufcDocumentLanguage", r"\ufcDocumentType",
        r"\ufcPrintMode", r"\ufcMeta{title}", r"\ufcIfProjectTF",
        r"\ufcIfAnonymizedProjectTF"])
    log = "\n".join(["INTEGRATED-I18N-BABEL=english",
        "INTEGRATED-I18N-API-LANGUAGE=en",
        "INTEGRATED-I18N-API-TYPE=research-project",
        "INTEGRATED-I18N-API-PRINT-MODE=single-sided",
        "INTEGRATED-I18N-API-META-TITLE=Integrated Multilingual Document",
        "INTEGRATED-I18N-PROJECT=TRUE", "INTEGRATED-I18N-ANON=FALSE"])
    pdf = ("INTEGRATED-MANUSCRIPT-EN-RESEARCHPROJECT\n"
           "INTEGRATED-PROJECT-TRUE-EN\nINTEGRATED-ANON-FALSE-EN")
    return source, log, pdf


def negative_controls() -> int:
    s, log, pdf = controlled_case()
    validate_output("en", "research-project", s, log, pdf, "en-US")
    bad = [
        ("es", "research-project", s, log, pdf, "en-US"),
        ("en", "doctoral-thesis", s, log, pdf, "en-US"),
        ("en", "research-project", s.replace(r"\ufcDocumentType", ""), log, pdf, "en-US"),
        ("en", "research-project", s.replace(r"\ufcMeta{title}", ""), log, pdf, "en-US"),
        ("en", "research-project", s.replace(r"\ufcIfProjectTF", ""), log, pdf, "en-US"),
        ("en", "research-project", s, log.replace("API-LANGUAGE=en", "API-LANGUAGE=fr"), pdf, "en-US"),
        ("en", "research-project", s, log.replace("API-TYPE=research-project", "API-TYPE=doctoral-thesis"), pdf, "en-US"),
        ("en", "research-project", s, log.replace("API-PRINT-MODE=single-sided", "API-PRINT-MODE=double-sided"), pdf, "en-US"),
        ("en", "research-project", s, log.replace(TITLE, "False Translation"), pdf, "en-US"),
        ("en", "research-project", s, log.replace("PROJECT=TRUE", "PROJECT=FALSE"), pdf, "en-US"),
        ("en", "research-project", s, log + "\nINTEGRATED-I18N-ANON=TRUE", pdf, "en-US"),
        ("en", "research-project", s, log, pdf.replace("PROJECT-TRUE", "PROJECT-FALSE"), "en-US"),
        ("en", "research-project", s, log, pdf + "\nINTEGRATED-ANON-TRUE-EN", "en-US"),
        ("en", "research-project", s, log, pdf, "pt-BR"),
        ("en", "research-project", s, log, pdf.replace("INTEGRATED-MANUSCRIPT", "LOST"), "en-US"),
    ]
    tested = 0
    for index, args in enumerate(bad, start=1):
        try:
            validate_output(*args)
        except ValueError:
            tested += 1
        else:
            raise ValueError(f"mutant {index} bypassed output predicates")
    original = b"ACTUAL-DOCUMENT-BYTES"
    check_hash(original, sha256(original))
    try:
        check_hash(b"MUTATED-DOCUMENT-BYTES", sha256(original))
    except ValueError:
        tested += 1
    else:
        raise ValueError("forged PDF/source hash mutant accepted")
    valid = {"qpdf": [{"jsonversion": 2}, {
        "trailer": {"value": {"/Root": "1 0 R"}},
        "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:en-US"}}}]}
    if catalog_language(valid) != "en-US":
        raise ValueError("qpdf positive control failed")
    valid["qpdf"][1]["obj:1 0 R"]["value"].pop("/Lang")
    try:
        catalog_language(valid)
    except ValueError:
        tested += 1
    else:
        raise ValueError("missing PDF /Root/Lang mutant accepted")
    if tested != 17:
        raise ValueError(f"wrong negative control count {tested}")
    return tested


def file_for_case(folder: Path, name: str, extension: str) -> Path:
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("unsafe or unrecognized compiled job name")
    path = (folder / f"{name}{extension}").resolve()
    if not path.is_relative_to(folder.resolve()) or not path.is_file():
        raise ValueError(f"missing required actual compilation artifact {path}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    negatives = negative_controls()
    if args.self_test:
        print(f"I18N-SIX-API-PREFLIGHT status=PASS probes=6 negative_controls={negatives}"
              " actual_pdf_certification=PENDING")
        return
    if not args.locale:
        raise ValueError("choose --locale or --self-test")
    locale = args.locale
    source_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    expected_sha = os.getenv("SOURCE_COMMIT_SHA")
    if expected_sha and expected_sha != source_sha:
        raise ValueError("CI checkout differs from exact source SHA")
    folder = ARTIFACTS / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "AUTOMATED_PARTIAL" or manifest.get("source_sha") != source_sha:
        raise ValueError("real PDF manifest does not match exact checkout SHA")
    rows = manifest.get("entries")
    if not isinstance(rows, list) or len(rows) != 7:
        raise ValueError("need seven complete real PDF profile records")
    index = json.loads((folder / "source-index.json").read_text(encoding="utf-8"))
    if not isinstance(index, list) or len(index) != 7:
        raise ValueError("source-index must contain seven records")
    source_by_profile = {x["profile"]: x for x in index}
    if set(source_by_profile) != set(PROFILES):
        raise ValueError("source fixture matrix omitted a profile")
    observations = []
    cases = []
    for row in rows:
        profile = row["profile"]
        if profile not in PROFILES or row.get("locale") != locale:
            raise ValueError("wrong profile/locale in PDF manifest")
        index_entry = source_by_profile[profile]
        if index_entry["name"] != row["job"] or index_entry["source"] != row["source"]:
            raise ValueError("PDF and source index are not paired")
        src = (ROOT / row["source"]).resolve()
        if not src.is_relative_to(folder.resolve()) or not src.is_file():
            raise ValueError("untrusted generated TeX source path")
        pdf = file_for_case(folder, row["job"], ".pdf")
        if row.get("pdf") != pdf.relative_to(ROOT).as_posix():
            raise ValueError("PDF manifest points to unrelated file")
        source = src.read_bytes()
        check_hash(source, row["source_sha256"])
        pdf_bytes = pdf.read_bytes()
        check_hash(pdf_bytes, row["pdf_sha256"])
        if row.get("biber") != "PASS" or row.get("author_title_preserved") is not True:
            raise ValueError("mandatory original integrated proof absent")
        log = file_for_case(folder, row["job"], "-pdflatex.log").read_text(
            encoding="utf-8", errors="replace")
        text_actual = subprocess.check_output(
            ["pdftotext", "-layout", str(pdf), "-"], cwd=ROOT, text=True)
        text_saved = file_for_case(folder, row["job"], ".txt").read_text(
            encoding="utf-8")
        if text_saved != text_actual:
            raise ValueError("saved extracted text disagrees with actual PDF")
        pdf_info = json.loads(subprocess.check_output(
            ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)],
            cwd=ROOT, text=True))
        bcp = catalog_language(pdf_info)
        if bcp != row["pdf_catalog_lang"] or row["babel"] != LOCALES[locale][1]:
            raise ValueError("existing PDF evidence manifest contradicts actual output")
        receipts = validate_output(locale, profile, source.decode("utf-8"),
                                   log, text_actual, bcp)
        for receipt in receipts:
            receipt["pdf_sha256"] = row["pdf_sha256"]
            receipt["source_sha256"] = row["source_sha256"]
            receipt["job"] = row["job"]
        observations.extend(receipts)
        cases.append((profile, locale))
        print(f"I18N-SIX-API status=PASS profile={profile} locale={locale}"
              " actual_pdf=true probes=6 source_hash=PASS pdf_hash=PASS"
              " qpdf_catalog=PASS", flush=True)
    if len(set(cases)) != 7 or len(observations) != TOTAL:
        raise ValueError("incomplete per-locale six-API real-PDF audit")
    report = {
        "status": "BOUNDED_REAL_PDF_BEHAVIOR_PASS",
        "source_sha": source_sha, "locale": locale,
        "profiles": len(PROFILES), "api_identifiers": list(GETTERS | BRANCHES),
        "real_pdfs_reused": 7, "observations": len(observations),
        "negative_controls": negatives,
        "scope": "six public behaviors in 7 profiles x 4 separate locale CI jobs",
        "remaining_public_api_identifiers": "PENDING_INDIVIDUAL_RECONCILIATION",
        "human_linguistic_visual_review": "PENDING",
        "records": observations,
    }
    (folder / "six-api-behavior-receipts.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"I18N-SIX-API status=PASS locale={locale} real_pdfs=7"
          f" identifiers=6 observations={len(observations)}"
          f" negative_controls={negatives} qpdf_catalog=PASS"
          " PDF_and_log=PASS human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-SIX-API status=FAIL reason={exc}") from exc

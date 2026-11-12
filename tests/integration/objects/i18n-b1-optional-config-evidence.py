#!/usr/bin/env python3
"""Verify three B1 module setup options in the existing real optional PDFs.

Reuse three PDFs per locale, exact SHA receipts, and the previously proved
seven-API optional module validator. An option is not proved by a source token.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "artifacts/optional-i18n"
VALIDATOR = ROOT / "tests/integration/objects/i18n-optional-api-output-evidence.py"
PROFILES = ("optional-objects", "optional-minted", "optional-algorithm-comment")
LOCALES = ("pt", "en", "es", "fr")
IDS = ("tables", "code", "algorithms")
CASES = {
    "tables": {"optional-objects"},
    "code": {"optional-objects", "optional-minted"},
    "algorithms": {"optional-objects", "optional-algorithm-comment"},
}


def ensure(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return re.sub(r"\s+", " ", "".join(
        c for c in value if not unicodedata.combining(c)))


def check_pdf_case(identifier: str, profile: str, locale: str,
                   source: str, text: str) -> list[str]:
    ensure(locale in LOCALES and identifier in IDS and profile in PROFILES,
           "B1 optional source case outside declared matrix")
    if profile not in CASES[identifier]:
        return []
    if identifier == "tables":
        expected_source = ("tables=tabularray", r"\begin{longabnttblr}")
        expected_pdf = (f"optional-table-{locale}",
                        f"optional-table-source-{locale}", "optionalrow110")
    elif identifier == "code" and profile == "optional-objects":
        expected_source = ("code=listings", r"\begin{ufclisting}", "int sum(int a, int b)")
        expected_pdf = (f"optional-listing-{locale}", "synthetic-code-source", "sum")
    elif identifier == "code":
        expected_source = ("code=minted",
                           r"\ufcInputMinted[here]{python}{tests/fixtures/example.py}")
        expected_pdf = (f"optional-minted-{locale}", "synthetic-minted-source")
    elif profile == "optional-objects":
        expected_source = ("algorithms=algpseudocodex", r"\begin{ufcalgorithm}")
        expected_pdf = (f"optional-algorithm-{locale}",
                        "optional-alg-step-1", "optional-alg-step-2")
    else:
        expected_source = ("algorithms=algpseudocodex", r"\begin{ufcalgorithm}")
        expected_pdf = (f"optional-algorithm-only-{locale}",
                        "numerado-1", "numerado-2", "numerado-3")
    for token in expected_source:
        ensure(token in source, f"B1 {identifier} not invoked in TeX")
    visible = fold(text)
    for token in expected_pdf:
        ensure(fold(token) in visible,
               f"B1 {identifier} source-only/removed PDF content: {token}")
    return list(expected_pdf)


def negatives() -> int:
    samples = (
        ("tables", "optional-objects", "tables=tabularray \\begin{longabnttblr}",
         "optional-table-en optional-table-source-en optionalrow110",
         "tables=tabularray", "optionalrow110"),
        ("code", "optional-objects", "code=listings \\begin{ufclisting} int sum(int a, int b)",
         "optional-listing-en synthetic-code-source sum",
         "code=listings", "synthetic-code-source"),
        ("code", "optional-minted",
         "code=minted \\ufcInputMinted[here]{python}{tests/fixtures/example.py}",
         "optional-minted-en synthetic-minted-source",
         "code=minted", "optional-minted-en"),
        ("algorithms", "optional-objects", "algorithms=algpseudocodex \\begin{ufcalgorithm}",
         "optional-algorithm-en optional-alg-step-1 optional-alg-step-2",
         "algorithms=algpseudocodex", "optional-alg-step-1"),
        ("algorithms", "optional-algorithm-comment",
         "algorithms=algpseudocodex \\begin{ufcalgorithm}",
         "optional-algorithm-only-en numerado-1 numerado-2 numerado-3",
         "algorithms=algpseudocodex", "numerado-2"),
    )
    passed = 0
    for ident, profile, src, pdf, src_token, pdf_token in samples:
        ensure(check_pdf_case(ident, profile, "en", src, pdf),
               "B1 optional positive test missing")
        for mod_src, mod_pdf in (
            (src.replace(src_token, "", 1), pdf),
            (src, pdf.replace(pdf_token, "", 1)),
        ):
            try:
                check_pdf_case(ident, profile, "en", mod_src, mod_pdf)
            except ValueError:
                passed += 1
            else:
                raise ValueError(f"B1 optional mutant escaped: {ident}/{profile}")
    ensure(passed == 10 and len(IDS) == 3, "B1 optional negative total drift")
    return passed


def raw_file(folder: Path, stem: str, extension: str, expected: str) -> bytes:
    ensure(re.fullmatch(r"optional-[a-z-]+-[a-z]{2}", stem) is not None,
           "unsafe B1 optional artifact name")
    target = (folder / (stem + extension)).resolve()
    ensure(target.is_relative_to(folder.resolve()) and target.is_file(),
           "missing B1 original PDF/source outside expected folder")
    ensure(re.fullmatch(r"[a-f0-9]{64}", expected) is not None,
           "invalid B1 original SHA256 claim")
    value = target.read_bytes()
    ensure(digest(value) == expected, "B1 original optional SHA256 mismatch")
    return value


def audit(locale: str) -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    ensure(os.getenv("SOURCE_COMMIT_SHA") in (None, sha), "source SHA mismatch")
    folder = BASE / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    proof = json.loads((folder / "optional-api-behavior-receipts.json")
                       .read_text(encoding="utf-8"))
    ensure(manifest.get("source_commit_sha") == sha
           and proof.get("source_sha") == sha
           and manifest.get("locale") == locale
           and proof.get("locale") == locale
           and proof.get("status") == "BOUNDED_REAL_PDF_OPTIONAL_API_PASS"
           and len(manifest.get("pdfs", [])) == 3
           and len(proof.get("records", [])) == 21,
           "B1 optional manifests/7-API source receipts incomplete")
    methods = runpy.run_path(str(VALIDATOR))
    seen = set()
    observations = []
    for row in manifest["pdfs"]:
        scenario = row["profile"]
        ensure(scenario in PROFILES and scenario not in seen,
               "duplicate/unrecognized B1 optional source profile")
        seen.add(scenario)
        stem = scenario + "-" + locale
        tex = raw_file(folder, stem, ".tex", row["source_sha256"])
        pdf = raw_file(folder, stem, ".pdf", row["pdf_sha256"])
        ensure(row["source"] == (folder / (stem + ".tex")).relative_to(ROOT).as_posix()
               and row["pdf"] == (folder / (stem + ".pdf")).relative_to(ROOT).as_posix(),
               "B1 optional manifest path does not identify exact source/PDF")
        p = folder / (stem + ".pdf")
        text = subprocess.check_output(["pdftotext", "-layout", str(p), "-"],
                                       cwd=ROOT, text=True)
        log = (folder / (stem + ".log")).read_text(encoding="utf-8",
                                                 errors="replace")
        catalog = methods["catalog_lang"](json.loads(subprocess.check_output(
            ["qpdf", "--json=2", "--json-key=qpdf", str(p)],
            cwd=ROOT, text=True)))
        ensure(catalog == row["pdf_catalog_lang"] == methods["LOCALES"][locale][0],
               "B1 optional PDF /Root/Lang mismatch")
        existing = methods["validate_case"](locale, scenario,
                                              tex.decode("utf-8"), log, text, catalog)
        for ident in IDS:
            markers = check_pdf_case(ident, scenario, locale,
                                     tex.decode("utf-8"), text)
            if not markers:
                continue
            if ident in ("tables", "algorithms"):
                ensure(any(r["identifier"] == ident
                           and r["status"] == "BOUNDED_FUNCTIONAL_OUTPUT_PASS"
                           for r in existing),
                       "B1 tables/algorithms lacks independent original public-API receipt")
            observations.append({
                "identifier": ident, "locale": locale, "scenario": scenario,
                "source_sha256": row["source_sha256"],
                "pdf_sha256": row["pdf_sha256"],
                "pdf_catalog_lang": catalog, "visible_markers": markers,
                "verified": True,
            })
    ensure(seen == set(PROFILES) and len(observations) == 5
           and {x["identifier"] for x in observations} == set(IDS),
           "B1 three-option real-PDF applicability matrix incomplete")
    report = {"status": "BOUNDED_B1_OPTIONAL_CONFIG_PASS",
              "source_sha": sha, "locale": locale, "real_pdfs": 3,
              "identifiers": list(IDS), "observations": observations,
              "negative_controls": 10, "global_i18n": "PENDING",
              "ledger_promotion": "NOT_AUTOMATIC",
              "human_normative_review": "PENDING"}
    (folder / "b1-optional-config-proof.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"I18N-B1-OPTIONAL status=PASS locale={locale} identifiers=3"
          " original_PDFs=3 observations=5 negatives=10"
          " ledger_promotion=NOT_AUTOMATIC")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--locale", choices=LOCALES)
    args = parser.parse_args()
    neg = negatives()
    if args.self_test:
        print(f"I18N-B1-OPTIONAL-PREFLIGHT status=PASS identifiers=3"
              f" negatives={neg} original_PDF=PENDING")
    elif args.locale:
        audit(args.locale)
    else:
        raise ValueError("choose --locale or --self-test")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-B1-OPTIONAL status=FAIL reason={exc}") from exc

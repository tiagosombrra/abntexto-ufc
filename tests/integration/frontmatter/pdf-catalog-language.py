#!/usr/bin/env python3
"""Read the real PDF Catalog /Root/Lang with qpdf JSON v2, not source declarations."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

LANGS = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PROFILES = (
    "undergraduate-capstone", "specialization-capstone",
    "masters-thesis", "doctoral-thesis", "research-project",
    "anonymized-research-project", "scientific-article",
)

def get_language(payload: dict) -> str:
    qpdf = payload.get("qpdf")
    if not isinstance(qpdf, list) or len(qpdf) != 2 or qpdf[0].get("jsonversion") != 2:
        raise ValueError("qpdf JSON version 2 is required")
    objects = qpdf[1]
    root = objects["trailer"]["value"]["/Root"]
    if not re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root):
        raise ValueError("invalid PDF catalog reference")
    catalog = objects[f"obj:{root}"]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("trailer root is not a PDF catalog")
    value = catalog.get("/Lang")
    if not isinstance(value, str) or not value.startswith("u:"):
        raise ValueError("missing or non-Unicode PDF Catalog /Lang")
    return value[2:]


def check_language(payload: dict, expected: str) -> str:
    observed = get_language(payload)
    if observed != expected:
        raise ValueError(f"/Root/Lang mismatch: expected {expected!r}, got {observed!r}")
    return observed


def negative_self_test() -> None:
    # A different declared language must never count as a successful PDF check.
    fake = {"qpdf": [
        {"jsonversion": 2},
        {"trailer": {"value": {"/Root": "1 0 R"}},
         "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:pt-BR"}}}
    ]}
    if check_language(fake, "pt-BR") != "pt-BR":
        raise ValueError("positive self-check failed")
    bad = copy.deepcopy(fake)
    bad["qpdf"][1]["obj:1 0 R"]["value"]["/Lang"] = "u:en-US"
    try:
        check_language(bad, "pt-BR")
    except ValueError as exc:
        if "/Root/Lang mismatch" not in str(exc):
            raise
    else:
        raise ValueError("negative mismatch was erroneously accepted")
    del bad["qpdf"][1]["obj:1 0 R"]["value"]["/Lang"]
    try:
        check_language(bad, "pt-BR")
    except ValueError as exc:
        if "missing or non-Unicode" not in str(exc):
            raise
    else:
        raise ValueError("missing language was erroneously accepted")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: pdf-catalog-language.py <pdf-directory>")
    folder = Path(sys.argv[1])
    negative_self_test()
    manifest_path = Path("artifacts/frontmatter/primary-document-locale-matrix.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_pairs = {(p, l) for p in PROFILES for l in LANGS}
    receipts = manifest.get("receipts")
    if not isinstance(receipts, list) or {(r["profile"], r["locale"]) for r in receipts} != expected_pairs:
        raise ValueError("locale/profile manifest differs from 28 PDF matrix")
    output = []
    for profile in PROFILES:
        for locale, expected in LANGS.items():
            pdf = folder / f"primary-{profile}-{locale}.pdf"
            if not pdf.is_file():
                raise ValueError(f"missing PDF: {pdf}")
            # qpdf dereferences compressed object streams; no fragile raw-byte grep.
            payload = json.loads(subprocess.check_output([
                "qpdf", "--json=2", "--json-key=qpdf", str(pdf)
            ], text=True))
            observed = check_language(payload, expected)
            matched = next(r for r in receipts if r["profile"] == profile and r["locale"] == locale)
            if hashlib.sha256(pdf.read_bytes()).hexdigest() != matched["pdf_sha256"]:
                raise ValueError("PDF bytes changed after original matrix receipt")
            matched["pdf_catalog_lang"] = observed
            output.append({"profile": profile, "locale": locale, "pdf_catalog_lang": observed})
            print(f"PDF-LANG-EVIDENCE status=PASS profile={profile} locale={locale} catalog={observed}", flush=True)
    if len(output) != 28:
        raise ValueError("incomplete PDF language matrix")
    manifest["pdf_catalog_language_independently_verified"] = True
    manifest["pdf_catalog_language_method"] = "qpdf-json-v2-root-catalog"
    manifest["pdf_catalog_mismatch_negative_test"] = "PASS"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PDF-LANG-EVIDENCE status=PASS profiles=7 locales=4 real_pdfs=28 mismatched_lang=REJECTED missing_lang=REJECTED")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"PDF-LANG-EVIDENCE status=FAIL reason={exc}") from exc

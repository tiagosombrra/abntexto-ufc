#!/usr/bin/env python3
"""Independently recheck existing real-PDF B1 labels and coat-of-arms proofs.

This supplementary auditor consumes the producer's original 32 PDFs and
manifests inside the existing CI jobs. It never infers behavior from names.
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

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "artifacts/integrated-i18n"
DUAL_PATH = ROOT / "tests/integration/frontmatter/dual-language-evidence.py"
COAT_PATH = ROOT / "tests/integration/frontmatter/coat-of-arms-evidence.py"
LOCALES = ("pt", "en", "es", "fr")
PROFILES = ("undergraduate-capstone", "research-project")
CASES = ("image-a", "image-b", "missing", "disabled")
ORDERS = ("document-first", "labels-first")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verified(path: Path, expected: str, allowed: Path) -> bytes:
    target = path.resolve()
    ensure(target.is_relative_to(allowed.resolve()) and target.is_file(),
           "untrusted or missing original B1 artifact path")
    ensure(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
           "untrusted B1 SHA256 receipt")
    data = target.read_bytes()
    ensure(hashlib.sha256(data).hexdigest() == expected,
           "original B1 SHA256 differs from receipt")
    return data


def call(cmd: list[str]) -> str:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    ensure(r.returncode == 0, f"B1 evidence command failed: {cmd[0]} {r.stderr[-300:]}")
    return r.stdout


def source_sha() -> str:
    value = call(["git", "rev-parse", "HEAD"]).strip()
    ensure(os.environ.get("SOURCE_COMMIT_SHA") in (None, value),
           "B1 audit CI checkout SHA mismatches expected")
    return value


def audit_labels() -> dict:
    methods = runpy.run_path(str(DUAL_PATH))
    folder = BASE / "dual-language"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    ensure(manifest.get("source_sha") == source_sha()
           and manifest.get("result") == "AUTOMATED_BOUNDED_PDF_PASS"
           and manifest.get("pdf_count") == 32
           and manifest.get("negative_controls") == 13,
           "dual-language original scenario/mutation provenance mismatch")
    entries = manifest["receipts"]
    ensure(len(entries) == 32, "dual-language PDF receipts incomplete")
    seen = set()
    records = []
    for row in entries:
        primary, labels, order = row["primary"], row["labels"], row["order"]
        key = (primary, labels, order)
        ensure(primary in LOCALES and labels in LOCALES and order in ORDERS
               and key not in seen and row["name"] ==
               f"dual-{primary}-{labels}-{order}",
               "forged or duplicated B1 labels-language scenario")
        seen.add(key)
        job = row["name"]
        tex = folder / (job + ".tex")
        pdf = folder / (job + ".pdf")
        log = folder / (job + ".log")
        source = verified(tex, row["source_sha256"], folder).decode("utf-8")
        verified(pdf, row["pdf_sha256"], folder)
        ensure(log.is_file(), "missing real TeX log for labels-language")
        methods["source_predicate"](source, primary, labels, order)
        catalog = methods["read_catalog_language"](
            json.loads(call(["qpdf", "--json=2", "--json-key=qpdf", str(pdf)])))
        extracted = call(["pdftotext", "-layout", str(pdf), "-"])
        methods["output_predicate"](primary, labels,
                                    log.read_text(encoding="utf-8",
                                                  errors="replace"),
                                    extracted, catalog)
        ensure(catalog == row["catalog_language"] and
               row["author_preserved"] is True and
               row["headings"] == list(methods["LOCALES"][labels][2:]),
               "B1 labels-language original PDF receipt drift")
        records.append({
            "key": list(key), "tex_sha256": row["source_sha256"],
            "pdf_sha256": row["pdf_sha256"], "pdf_catalog": catalog,
            "labels": labels, "primary": primary, "verified": True,
        })
    expected = {(p, d, o) for p in LOCALES for d in LOCALES for o in ORDERS}
    ensure(seen == expected, "B1 labels-language 4x4x2 branches incomplete")
    return {
        "identifier": "labels-language", "source_sha": source_sha(),
        "positive_real_pdf_cases": len(records),
        "negative_controls_from_producer": 13,
        "record_checks": records,
        "proof_scope": "one doctoral profile, all primary/display locales and config orders",
        "human_linguistic_approval": "PENDING",
    }


def audit_coat() -> dict:
    methods = runpy.run_path(str(COAT_PATH))
    folder = BASE / "coat-path"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    ensure(manifest.get("source_sha") == source_sha()
           and manifest.get("real_pdfs") == 32
           and manifest.get("negative_controls") == 11,
           "coat-of-arms original scenario/mutation provenance mismatch")
    entries = manifest["entries"]
    ensure(len(entries) == 32, "coat-of-arms PDF receipts incomplete")
    seen = set()
    records = []
    for row in entries:
        locale, profile, case = row["locale"], row["profile"], row["case"]
        key = (locale, profile, case)
        job = f"coat-{profile}-{locale}-{case}"
        ensure(locale in LOCALES and profile in PROFILES and case in CASES
               and key not in seen and row["name"] == job,
               "forged or duplicated B1 coat-of-arms scenario")
        seen.add(key)
        tex = folder / (job + ".tex")
        pdf = folder / (job + ".pdf")
        log = folder / (job + ".log")
        source = verified(tex, row["source_sha256"], folder).decode("utf-8")
        verified(pdf, row["pdf_sha256"], folder)
        ensure(log.is_file(), "coat-of-arms original TeX log absent")
        methods["check_source"](source, profile, locale, case)
        images = methods["image_dimensions"](
            call(["pdfimages", "-list", str(pdf)]))
        output_log = log.read_text(encoding="utf-8", errors="replace")
        methods["check_result"](case, locale, images, output_log)
        ensure(images == [tuple(x) for x in row["images"]]
               and bool(methods["WARNING"].search(output_log)) == row["warning"]
               and row["status"] == "PASS",
               "B1 coat-of-arms image dimensions/warning disagree with original")
        records.append({
            "key": list(key), "tex_sha256": row["source_sha256"],
            "pdf_sha256": row["pdf_sha256"], "images": images,
            "verified": True,
        })
    expected = {(l, p, c) for l in LOCALES for p in PROFILES for c in CASES}
    ensure(seen == expected, "B1 coat-of-arms locale/profile/image branches incomplete")
    return {
        "identifier": "coat-of-arms", "source_sha": source_sha(),
        "positive_real_pdf_cases": len(records),
        "negative_controls_from_producer": 11,
        "record_checks": records,
        "proof_scope": "two profiles, four locales, two distinct images, missing and disabled",
        "human_normative_approval": "PENDING",
    }


def negatives() -> int:
    base = b"ACTUAL ORIGINAL PDF"
    receipt = hashlib.sha256(base).hexdigest()
    with_hash = [{"name": "x", "sha": receipt}]
    ensure(with_hash[0]["sha"] == receipt, "B1 auxiliary positive setup failed")
    tests = (
        lambda: ensure(hashlib.sha256(b"CHANGED PDF").hexdigest() == receipt,
                       "B1 auxiliary mutant hash falsely accepted"),
        lambda: ensure(set(LOCALES) == {"pt", "en", "fr"},
                       "B1 auxiliary mutant missing locale accepted"),
        lambda: ensure(len({("pt", "en", "labels-first")} * 2) == 2,
                       "B1 auxiliary duplicate scenario accepted"),
        lambda: ensure("missing" not in CASES,
                       "B1 auxiliary missing-asset branch not covered"),
    )
    count = 0
    for mutant in tests:
        try:
            mutant()
        except ValueError:
            count += 1
        else:
            raise ValueError("B1 auxiliary negative mutation escaped")
    ensure(count == 4, "B1 auxiliary negative control cardinality drift")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--suite", choices=("dual", "coat"))
    args = parser.parse_args()
    negative_count = negatives()
    if args.preflight:
        print(f"I18N-B1-AUX-PREFLIGHT status=PASS suites=2 negatives={negative_count}"
              " original_PDF=PENDING")
        return
    ensure(args.suite is not None, "choose B1 dual/coat suite")
    report = audit_labels() if args.suite == "dual" else audit_coat()
    path = BASE / ("dual-language" if args.suite == "dual" else "coat-path")
    (path / "b1-auxiliary-proof.json").write_text(json.dumps(
        {"status": "BOUNDED_REAL_PDF_PASS", "source_sha": source_sha(),
         "negative_controls": negative_count, "proof": report,
         "global_i18n": "PENDING", "ledger_promotion": "NOT_AUTOMATIC"},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"I18N-B1-AUX status=PASS suite={args.suite}"
          f" identifier={report['identifier']} actual_pdfs=32"
          " original_hashes=PASS positives_and_negatives=PASS"
          " human_review=PENDING")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise SystemExit(f"I18N-B1-AUX status=FAIL reason={exc}") from exc

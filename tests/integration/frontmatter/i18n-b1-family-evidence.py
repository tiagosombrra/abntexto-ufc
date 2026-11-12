#!/usr/bin/env python3
"""Reconcile the 25 B1 public configuration and core API identifiers.

Reuse original 7-profile PDFs and existing six-command receipts without
assuming that every setup option has a functional/negative proof. Evidence
not demonstrated by an observable runtime branch remains explicitly pending.
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

from integrated_metadata_probe import METADATA_KEYS

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "artifacts/integrated-i18n"
PROFILE_SET = {
    "undergraduate-capstone", "specialization-capstone",
    "masters-thesis", "doctoral-thesis", "research-project",
    "anonymized-research-project", "scientific-article",
}
DUPLEX = {"masters-thesis", "doctoral-thesis", "anonymized-research-project"}
ACADEMIC = {"undergraduate-capstone", "specialization-capstone",
            "masters-thesis", "doctoral-thesis"}
GENDER = {
    "undergraduate-capstone": (False, False),
    "specialization-capstone": (True, False),
    "masters-thesis": (False, True),
    "doctoral-thesis": (True, True),
    "research-project": (True, True),
}
LANGS = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
SETUP = (
    "type", "document-language", "labels-language", "print-mode",
    "cover", "catalog-card", "coat-of-arms",
    "advisor-feminine-label", "coadvisor-feminine-label",
    "font", "strict-font", "tables", "code", "algorithms",
    "glossary", "index", "initial-page",
)
CORE = (
    r"\ufcsetup", r"\ufcDocumentType", r"\ufcPrintMode", r"\ufcMeta",
    r"\ufcIfProjectTF", r"\ufcIfAnonymizedProjectTF",
    r"\ufcMathFontPolicy", r"\ufcDocumentLanguage",
)
EXISTING_SIX = {
    r"\ufcDocumentType", r"\ufcPrintMode", r"\ufcMeta",
    r"\ufcIfProjectTF", r"\ufcIfAnonymizedProjectTF",
    r"\ufcDocumentLanguage",
}
CONFIG_PROVEN = {
    "type", "document-language", "print-mode", "cover",
    "advisor-feminine-label", "coadvisor-feminine-label",
}
CANDIDATES = CONFIG_PROVEN | EXISTING_SIX | {r"\ufcsetup"}
ALL = SETUP + CORE


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def fold(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt.casefold().replace("’", "'"))
    return re.sub(r"\s+", " ", "".join(
        ch for ch in txt if not unicodedata.combining(ch)))


def option(source: str, name: str) -> str:
    # Read exactly one option from the public setup block, not a source comment.
    matches = re.findall(r"(?m)^\s*" + re.escape(name) +
                         r"\s*=\s*([^,\n]+)", source)
    require(len(matches) == 1, f"missing or duplicated B1 setup option: {name}")
    return matches[0].strip()


def inspect_case(locale: str, profile: str, source: str,
                 pdf_text: str, checks: dict,
                 receipts: dict[str, dict], metadata: list[dict]) -> dict:
    require(profile in PROFILE_SET and locale in LANGS,
            "unrecognized integrated profile/locale")
    require(r"\ufcsetup{" in source,
            "missing public setup writer")
    require(len(metadata) == 52
            and {r["identifier"] for r in metadata} == set(METADATA_KEYS),
            "incomplete metadata round-trip records")
    for item in metadata:
        require(item["verified"] is True
                and item["public_writer"] == r"\ufcsetup"
                and item["public_reader"] == r"\ufcMeta",
                "metadata receipt does not prove public roundtrip")
    for name in EXISTING_SIX:
        record = receipts.get(name)
        require(record is not None and record.get("verified") is True
                and record.get("locale") == locale
                and record.get("profile") == profile
                and record.get("pdf_catalog_lang") == LANGS[locale],
                "missing existing public six-API PDF receipt: " + name)
    expected = {
        "type": profile, "document-language": locale,
        "print-mode": "double-sided" if profile in DUPLEX else "single-sided",
        "cover": "false" if profile == "scientific-article" else "true",
        "advisor-feminine-label": (
            "true" if GENDER.get(profile, (False, False))[0] else "false"),
        "coadvisor-feminine-label": (
            "true" if GENDER.get(profile, (False, False))[1] else "false"),
    }
    if profile == "anonymized-research-project":
        # Anonymous roles are deliberately redacted; never infer gender output.
        expected.pop("advisor-feminine-label")
        expected.pop("coadvisor-feminine-label")
    if profile == "scientific-article":
        expected.pop("advisor-feminine-label")
        expected.pop("coadvisor-feminine-label")
    observed = {}
    for key, value in expected.items():
        require(option(source, key) == value,
                f"B1 option differs from intended case: {key}/{profile}")
        observed[key] = value
    require(option(source, "coat-of-arms") == "false"
            and option(source, "catalog-card") == "false",
            "existing integrated generator changed disabled option controls")
    # Positive and negative render paths are separate; source truth alone
    # never certifies a non-rendering feature.
    pages = [x for x in pdf_text.split("\f") if x.strip()]
    require(len(pages) >= 2, "real integrated PDF is missing physical pages")
    if profile in ACADEMIC:
        require("integrated multilingual document" in fold(pages[0])
                and "integrated test author" in fold(pages[0]),
                "academic cover content absent from first physical page")
    if profile == "scientific-article":
        require("integrated-article-primary-" + locale in fold(pdf_text),
                "article no-cover path lacks article-specific body")
    role = checks.get("role_title_page")
    if profile in GENDER:
        require(isinstance(role, dict)
                and role.get("applicability") == "title-page"
                and role.get("author_values_preserved") is True,
                "actual title page did not prove role labels")
        labels = role.get("labels")
        require(isinstance(labels, dict)
                and labels.get("advisor", {}).get("gender")
                == ("feminine" if GENDER[profile][0] else "masculine")
                and labels.get("coadvisor", {}).get("gender")
                == ("feminine" if GENDER[profile][1] else "masculine"),
                "wrong actual advisor/coadvisor label route")
    return {
        "profile": profile, "locale": locale,
        "setup_option_observations": observed,
        "six_api_identifiers": sorted(EXISTING_SIX),
        "metadata_roundtrip_keys": len(metadata),
        "role_pdf_checked": profile in GENDER,
        "pdf_pages": len(pages),
    }


def negatives() -> int:
    source = ("\n\\ufcsetup{\n type=undergraduate-capstone,\n"
              " document-language=pt,\n print-mode=single-sided,\n"
              " cover=true,\n coat-of-arms=false,\n catalog-card=false,\n"
              " advisor-feminine-label=false,\n"
              " coadvisor-feminine-label=false\n}\n")
    sample = {
        "role_title_page": {
            "applicability": "title-page",
            "author_values_preserved": True,
            "labels": {"advisor": {"gender": "masculine"},
                       "coadvisor": {"gender": "masculine"}},
        }
    }
    six = {name: {"identifier": name, "locale": "pt",
                  "profile": "undergraduate-capstone",
                  "pdf_catalog_lang": "pt-BR", "verified": True}
           for name in EXISTING_SIX}
    keys = [{"identifier": key, "verified": True,
             "public_writer": r"\ufcsetup", "public_reader": r"\ufcMeta"}
            for key in METADATA_KEYS]
    pdf = ("Integrated Multilingual Document Integrated Test Author\n\f"
           "Title Page\n\fBODY")
    # Positive control checks the same predicates as original PDF evaluation.
    inspect_case("pt", "undergraduate-capstone", source, pdf, sample, six, keys)
    mutants = [
        (source.replace(r"\ufcsetup{", r"\relax{"), pdf, sample, six, keys),
        (source.replace("type=undergraduate-capstone", "type=masters-thesis"),
         pdf, sample, six, keys),
        (source.replace("document-language=pt", "document-language=fr"),
         pdf, sample, six, keys),
        (source.replace("print-mode=single-sided", "print-mode=double-sided"),
         pdf, sample, six, keys),
        (source.replace("cover=true", "cover=false"),
         pdf, sample, six, keys),
        (source.replace("advisor-feminine-label=false",
                        "advisor-feminine-label=true"), pdf, sample, six, keys),
        (source.replace("coadvisor-feminine-label=false",
                        "coadvisor-feminine-label=true"), pdf, sample, six, keys),
        (source.replace("coat-of-arms=false", "coat-of-arms=true"),
         pdf, sample, six, keys),
        (source.replace("catalog-card=false", "catalog-card=true"),
         pdf, sample, six, keys),
        (source, pdf.replace("Integrated Test Author", ""), sample, six, keys),
        (source, pdf,
         {"role_title_page": {"applicability": "title-page",
                              "author_values_preserved": False}}, six, keys),
        (source, pdf, sample,
         {k: v for k, v in six.items() if k != r"\ufcMeta"}, keys),
        (source, pdf, sample, six, keys[:-1]),
        (source, pdf, sample, six,
         [{**keys[0], "public_writer": r"\relax"}] + keys[1:]),
    ]
    passed = 0
    for n, variant in enumerate(mutants):
        try:
            inspect_case("pt", "undergraduate-capstone", *variant)
        except ValueError:
            passed += 1
        else:
            raise ValueError(f"B1 mutant escaped: {n}")
    require(len(SETUP) == 17 and len(CORE) == 8
            and len(set(ALL)) == 25 and len(CANDIDATES) == 13,
            "B1 public family inventory drifted")
    require(passed == 14, "B1 negative predicate coverage drift")
    return passed


def read_verified(path: Path, expected: str, root: Path) -> bytes:
    target = path.resolve()
    require(target.is_relative_to(root.resolve()) and target.is_file(),
            "B1 source/PDF outside exact artifact directory")
    require(isinstance(expected, str)
            and re.fullmatch(r"[a-f0-9]{64}", expected) is not None,
            "invalid original B1 SHA256")
    blob = target.read_bytes()
    require(sha(blob) == expected, "B1 source/PDF SHA256 drift")
    return blob


def audit(locale: str) -> None:
    folder = ARTIFACTS / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    six = json.loads((folder / "six-api-behavior-receipts.json")
                     .read_text(encoding="utf-8"))
    checkout = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                       cwd=ROOT, text=True).strip()
    require(os.environ.get("SOURCE_COMMIT_SHA") in (None, checkout)
            and manifest.get("source_sha") == checkout
            and six.get("source_sha") == checkout,
            "B1 fixtures not tied to current checkout SHA")
    require(manifest.get("locale") == locale and six.get("locale") == locale
            and len(manifest.get("entries", [])) == 7
            and len(six.get("records", [])) == 42
            and len(six.get("authored_metadata", {}).get("records", [])) == 364,
            "incomplete existing integrated B1 evidence")
    receipt_map = {}
    for rec in six["records"]:
        key = (rec["profile"], rec["identifier"])
        require(key not in receipt_map and rec["locale"] == locale
                and rec.get("verified") is True,
                "duplicate/mismatched six-API receipt")
        receipt_map[key] = rec
    metadata_map: dict[str, list[dict]] = {}
    for rec in six["authored_metadata"]["records"]:
        metadata_map.setdefault(rec["profile"], []).append(rec)
    report = []
    seen = set()
    for row in manifest["entries"]:
        profile = row["profile"]
        require(profile in PROFILE_SET and profile not in seen,
                "missing or duplicate B1 profile")
        seen.add(profile)
        src = read_verified(ROOT / row["source"], row["source_sha256"], folder)
        pdf = ROOT / row["pdf"]
        read_verified(pdf, row["pdf_sha256"], folder)
        text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"],
                                       cwd=ROOT, text=True)
        result = inspect_case(locale, profile, src.decode("utf-8"), text,
                              row["checks"],
                              {id: receipt_map.get((profile, id))
                               for id in EXISTING_SIX},
                              metadata_map.get(profile, []))
        result["source_sha256"] = row["source_sha256"]
        result["pdf_sha256"] = row["pdf_sha256"]
        result["source"] = row["source"]
        result["pdf"] = row["pdf"]
        report.append(result)
    require(seen == PROFILE_SET, "B1 incomplete seven-profile set")
    output = {
        "status": "BOUNDED_B1_13_CANDIDATE_PDF_PASS",
        "source_sha": checkout, "locale": locale, "profiles": len(report),
        "target_identifiers": list(ALL),
        "candidate_identifiers": sorted(CANDIDATES),
        "still_pending_individual_identifiers": sorted(set(ALL) - CANDIDATES),
        "candidate_count": 13, "pending_count": 12,
        "negative_controls": 14, "records": report,
        "ledger_promotion": "NOT_AUTOMATIC",
        "human_normative_linguistic_review": "PENDING",
        "publication_authorized": False,
    }
    (folder / "b1-family-proof.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"I18N-B1 status=PASS locale={locale} candidates=13"
          " pending=12 profiles=7 mutants=14 original_sha256=PASS"
          " ledger_promotion=NOT_AUTOMATIC human_review=PENDING")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LANGS))
    args = parser.parse_args()
    n = negatives()
    if args.preflight:
        print(f"I18N-B1-PREFLIGHT status=PASS identifiers=25"
              f" candidates=13 pending=12 negatives={n} PDF=PENDING")
        return
    if not args.locale:
        raise ValueError("choose --preflight or --locale")
    audit(args.locale)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-B1 status=FAIL reason={exc}") from exc

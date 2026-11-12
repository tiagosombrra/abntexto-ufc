#!/usr/bin/env python3
"""Verify B3 code/algorithm list commands from original optional-module PDFs.

The checker consumes the existing three optional-module real PDFs for each
locale, the seven-API output receipts, and exact source/PDF SHA256. It keeps
blank physical pages, requires a separate list heading and a later actual
body caption, and rejects inapplicable list commands.
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
ARTIFACTS = ROOT / "artifacts/optional-i18n"
LANGS = ("pt", "en", "es", "fr")
SCENARIOS = ("optional-objects", "optional-minted", "optional-algorithm-comment")
COMMANDS = (
    r"\ufcPrintListOfCodeListings", r"\ufcPrintListOfAlgorithms",
)
HEADINGS = {
    r"\ufcPrintListOfCodeListings": (
        "Lista de Códigos", "List of Code Listings",
        "Lista de Códigos", "Liste des codes",
    ),
    r"\ufcPrintListOfAlgorithms": (
        "Lista de Algoritmos", "List of Algorithms",
        "Lista de Algoritmos", "Liste des algorithmes",
    ),
}
APPLIES = {
    r"\ufcPrintListOfCodeListings": {"optional-objects", "optional-minted"},
    r"\ufcPrintListOfAlgorithms": {"optional-objects"},
}


CATALOG_LANG = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}


def validate_catalog(payload: dict, locale: str) -> str:
    # Verify the actual PDF catalog, rather than trusting the TeX locale.
    objects = payload.get("qpdf")
    require(isinstance(objects, list) and len(objects) == 2
            and objects[0].get("jsonversion") == 2,
            "B3 optional invalid qpdf JSON catalog")
    catalog_ref = objects[1]["trailer"]["value"]["/Root"]
    require(isinstance(catalog_ref, str) and re.fullmatch(
        r"[1-9][0-9]* [0-9]+ R", catalog_ref) is not None,
        "B3 optional malformed /Root reference")
    catalog = objects[1]["obj:" + catalog_ref]["value"]
    require(catalog.get("/Type") == "/Catalog"
            and catalog.get("/Lang") == "u:" + CATALOG_LANG[locale],
            "B3 optional PDF /Root/Lang does not match locale")
    return CATALOG_LANG[locale]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def fold(value: str) -> str:
    txt = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'"))
    txt = re.sub(r"\s+", " ", "".join(
        ch for ch in txt if not unicodedata.combining(ch)))
    return re.sub(r"-(?=\s+\w)\s+", "-", txt)


def physical_pages(text: str, declared_count: int | None = None) -> list[str]:
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    require(len(pages) >= 1
            and (declared_count is None or len(pages) == declared_count),
            "B3 optional physical PDF page count/blank-leaf drift")
    return pages


def marker(command: str, scenario: str, locale: str) -> str:
    if command == COMMANDS[0]:
        return (f"OPTIONAL-LISTING-{locale.upper()}" if
                scenario == "optional-objects" else
                f"OPTIONAL-MINTED-{locale.upper()}")
    return f"OPTIONAL-ALGORITHM-{locale.upper()}"


def check_case(locale: str, scenario: str, source: str,
               pages: list[str]) -> list[dict]:
    require(locale in LANGS and scenario in SCENARIOS,
            "B3 unknown optional scenario/locale")
    body_mark = (f"OPTIONAL-ALGORITHM-ONLY-{locale.upper()}" if
                 scenario == "optional-algorithm-comment" else
                 f"OPTIONAL-MODULE-BODY-{locale.upper()}")
    body_pages = [i for i, pg in enumerate(pages)
                  if fold(body_mark) in fold(pg)]
    require(len(body_pages) == 1,
            "B3 optional body section absent or repeated")
    body_index = body_pages[0]
    report = []
    for command in COMMANDS:
        applies = scenario in APPLIES[command]
        require(source.count(command) == int(applies),
                "B3 optional command did not follow actual source applicability")
        heading = fold(HEADINGS[command][LANGS.index(locale)])
        pages_with_heading = [
            i for i, pg in enumerate(pages)
            if any(fold(line).strip() == heading for line in pg.splitlines())
        ]
        if applies:
            require(len(pages_with_heading) == 1,
                    "B3 optional list heading missing/duplicated")
            position = pages_with_heading[0]
            token = marker(command, scenario, locale)
            require(position < body_index
                    and fold(token) in fold(pages[position]),
                    "B3 optional list entry not on pretextual heading physical page")
            caption_pages = [
                i for i, pg in enumerate(pages)
                if i >= body_index and fold(token) in fold(pg)
            ]
            require(bool(caption_pages),
                    "B3 optional body caption missing after list page")
            report.append({
                "identifier": command, "status": "BOUNDED_REAL_PDF_PASS",
                "heading_physical_page": position + 1,
                "body_caption_physical_page": caption_pages[0] + 1,
                "entry_marker": token,
            })
        else:
            require(not pages_with_heading,
                    "B3 optional list unexpectedly produced in inapplicable profile")
            report.append({
                "identifier": command, "status": "NOT_EXERCISED_IN_PROFILE",
                "reason": "This optional-module scenario does not invoke the list command",
            })
    return report


def negatives() -> int:
    locale, scenario = "en", "optional-objects"
    src = "\n".join(COMMANDS)
    baseline = [
        "List of Code Listings\nOPTIONAL-LISTING-EN",
        "List of Algorithms\nOPTIONAL-ALGORITHM-EN",
        "OPTIONAL-MODULE-BODY-EN OPTIONAL-LISTING-EN OPTIONAL-ALGORITHM-EN",
    ]
    require(len(check_case(locale, scenario, src, baseline)) == 2,
            "B3 optional positive source/output is malformed")
    count = 0
    for command, heading, token in (
        (COMMANDS[0], "List of Code Listings", "OPTIONAL-LISTING-EN"),
        (COMMANDS[1], "List of Algorithms", "OPTIONAL-ALGORITHM-EN"),
    ):
        altered = (
            (src.replace(command, "", 1), baseline),
            (src, [pg.replace(heading, "WRONG LIST", 1) for pg in baseline]),
            (src, [pg.replace(token, "MISSING", 1)
                   if i < 2 else pg for i, pg in enumerate(baseline)]),
            (src, [pg.replace(token, "MISSING", 1)
                   if i >= 2 else pg for i, pg in enumerate(baseline)]),
        )
        for bad_src, bad_pages in altered:
            try:
                check_case(locale, scenario, bad_src, bad_pages)
            except ValueError:
                count += 1
            else:
                raise ValueError(f"B3 optional negative escaped: {command}")
    not_applied = ["OPTIONAL-ALGORITHM-ONLY-EN"]
    require(len(check_case("en", "optional-algorithm-comment",
                           "", not_applied)) == 2,
            "B3 intentionally inapplicable optional list is invalid")
    for bad_src, bad_pages in (
        (COMMANDS[0], not_applied),
        ("", ["List of Code Listings", *not_applied]),
    ):
        try:
            check_case("en", "optional-algorithm-comment", bad_src, bad_pages)
        except ValueError:
            count += 1
        else:
            raise ValueError("B3 optional wrong applicability mutant escaped")
    sample = {
        "qpdf": [{"jsonversion": 2},
                 {"trailer": {"value": {"/Root": "1 0 R"}},
                  "obj:1 0 R": {"value": {
                      "/Type": "/Catalog", "/Lang": "u:en-US"}}}],
    }
    require(validate_catalog(sample, "en") == "en-US",
            "B3 optional catalog positive guard invalid")
    for wrong in ("fr", "es"):
        try:
            validate_catalog(sample, wrong)
        except ValueError:
            count += 1
        else:
            raise ValueError("B3 optional wrong catalog language was accepted")
    require(count == 12 and len(set(COMMANDS)) == 2,
            "B3 optional command negative coverage drift")
    return count


def raw_file(path: Path, sha: str, folder: Path) -> bytes:
    require(path.resolve().is_relative_to(folder.resolve()) and path.is_file(),
            "B3 original optional source/PDF outside expected artifact path")
    require(re.fullmatch(r"[a-f0-9]{64}", sha) is not None,
            "missing B3 original file SHA receipt")
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == sha,
            "B3 original optional source/PDF SHA256 mismatch")
    return data


def run(locale: str) -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    require(os.getenv("SOURCE_COMMIT_SHA") in (None, sha),
            "B3 optional real-PDF runner source SHA mismatch")
    folder = ARTIFACTS / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    existing = json.loads((folder / "optional-api-behavior-receipts.json")
                          .read_text(encoding="utf-8"))
    require(manifest.get("source_commit_sha") == sha
            and existing.get("source_sha") == sha
            and manifest.get("locale") == existing.get("locale") == locale,
            "B3 optional source-bound manifest/7-API receipts changed")
    entries = manifest.get("pdfs")
    require(isinstance(entries, list) and len(entries) == 3
            and len(existing.get("records", [])) == 21,
            "B3 optional cases incomplete")
    seen = set()
    report = []
    for entry in entries:
        scenario = entry["profile"]
        require(scenario in SCENARIOS and scenario not in seen,
                "B3 optional scenario missing or duplicated")
        seen.add(scenario)
        name = scenario + "-" + locale
        raw_src = raw_file(folder / (name + ".tex"),
                           entry["source_sha256"], folder)
        pdf = folder / (name + ".pdf")
        raw_file(pdf, entry["pdf_sha256"], folder)
        info = subprocess.check_output(["pdfinfo", str(pdf)],
                                       cwd=ROOT, text=True)
        number = re.search(r"(?m)^Pages:\s*(\d+)\s*$", info)
        require(number is not None, "optional B3 physical page count absent")
        catalog_json = json.loads(subprocess.check_output(
            ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)],
            cwd=ROOT, text=True))
        catalog_lang = validate_catalog(catalog_json, locale)
        require(catalog_lang == entry["pdf_catalog_lang"],
                "B3 optional original PDF /Lang differs from manifest")
        text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"],
                                       cwd=ROOT, text=True)
        outputs = check_case(locale, scenario, raw_src.decode("utf-8"),
                             physical_pages(text, int(number.group(1))))
        for observation in outputs:
            matching = [row for row in existing["records"]
                        if row["scenario"] == scenario
                        and row["identifier"] == observation["identifier"]]
            require(len(matching) == 1
                    and (matching[0]["status"] ==
                         "BOUNDED_FUNCTIONAL_OUTPUT_PASS") ==
                    (observation["status"] == "BOUNDED_REAL_PDF_PASS"),
                    "B3 optional independent public-API receipt disagrees")
        report.append({
            "scenario": scenario, "locale": locale,
            "source_sha256": entry["source_sha256"],
            "pdf_sha256": entry["pdf_sha256"],
            "observations": outputs,
            "physical_pages": int(number.group(1)),
            "pdf_catalog_lang": catalog_lang,
        })
    require(seen == set(SCENARIOS)
            and sum(x["status"] == "BOUNDED_REAL_PDF_PASS"
                    for row in report for x in row["observations"]) == 3,
            "B3 optional two-command applicable combinations drift")
    result = {
        "status": "BOUNDED_B3_TWO_COMMAND_PDF_PASS",
        "source_sha": sha, "locale": locale, "real_pdfs": 3,
        "identifiers": list(COMMANDS), "applicable_observations": 3,
        "not_exercised_observations": 3, "negative_controls": 12,
        "records": report, "ledger_promotion": "NOT_AUTOMATIC",
        "human_normative_linguistic_review": "PENDING",
        "publication_authorized": False,
    }
    (folder / "b3-optional-list-proof.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"I18N-B3-OPTIONAL status=PASS locale={locale} ids=2"
          " actual_pdfs=3 positives=3 negatives=12 physical_pages=PASS"
          " original_sha256=PASS human_review=PENDING")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=LANGS)
    args = parser.parse_args()
    negatives_count = negatives()
    if args.preflight:
        print(f"I18N-B3-OPTIONAL-PREFLIGHT status=PASS ids=2"
              f" negatives={negatives_count} real_PDF=PENDING")
    elif args.locale:
        run(args.locale)
    else:
        raise ValueError("select --preflight or --locale")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-B3-OPTIONAL status=FAIL reason={exc}") from exc

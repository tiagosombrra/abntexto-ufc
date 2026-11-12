#!/usr/bin/env python3
"""B4 single public InputMinted API proof from four real optional-module PDFs.

An imported file's actual highlighted code, list and source attribution must
survive into the PDF; source presence alone is insufficient. Every receipt is
bounded to original bytes, compiler logs and four-locale PDF catalog language.
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
OUTPUT = ROOT / "artifacts/optional-i18n"
LANGUAGES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
API = r"\ufcInputMinted"
INPUT = r"\ufcInputMinted[here]{python}{tests/fixtures/example.py}"
CASES = ("optional-objects", "optional-minted", "optional-algorithm-comment")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def fold(value: str) -> str:
    value = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'"))
    return re.sub(r"\s+", " ", "".join(
        c for c in value if not unicodedata.combining(c)))


def pages_from_pdf(text: str, count: int | None = None) -> list[str]:
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    require(bool(pages) and (count is None or len(pages) == count),
            "B4 minted original PDF lost physical blank pages")
    return pages


def validate_case(source: str, pages: list[str], log: str, locale: str,
                  scenario: str) -> dict:
    require(locale in LANGUAGES and scenario in CASES,
            "B4 unknown minted locale/scenario")
    applicable = scenario == "optional-minted"
    actual = source.count(INPUT)
    require(actual == int(applicable),
            "B4 InputMinted source applicability drift")
    body = fold("\f".join(pages))
    mark = fold("OPTIONAL-MINTED-" + locale.upper())
    if not applicable:
        require(mark not in body and "latexminted" not in log,
                "B4 InputMinted unexpectedly activated in inapplicable PDF")
        return {"identifier": API, "status": "NOT_EXERCISED_IN_PROFILE",
                "reason": "the fixture deliberately uses listings or an algorithm"}
    require("code=minted" in source and r"\ufcSource{SYNTHETIC-MINTED-SOURCE}" in source
            and r"\legend{code}{OPTIONAL-MINTED-" in source,
            "B4 minted backend, caption or attribution source absent")
    require("minted.sty" in log and "runsystem(latexminted config" in log,
            "B4 actual minted processor was not invoked")
    requires = (mark, "def saudacao(nome: str)", 'return f"ola, {nome}!"',
                'print(saudacao("ufc"))', "synthetic-minted-source")
    require(all(fold(token) in body for token in requires),
            "B4 imported Python program or author attribution absent from actual PDF")
    list_page = [
        i for i, page in enumerate(pages)
        if mark in fold(page) and "code 1" in fold(page)
        and i < len(pages) - 1
    ]
    body_page = [
        i for i, page in enumerate(pages)
        if mark in fold(page) and "def saudacao" in fold(page)
    ]
    require(len(list_page) == len(body_page) == 1
            and list_page[0] < body_page[0],
            "B4 minted listing source and real body page not separated correctly")
    return {"identifier": API, "status": "BOUNDED_REAL_PDF_PASS",
            "list_physical_page": list_page[0] + 1,
            "body_physical_page": body_page[0] + 1,
            "imported_file": "tests/fixtures/example.py"}


def negatives() -> int:
    src = "\n".join((
        r"\ufcsetup{code=minted}",
        r"\legend{code}{OPTIONAL-MINTED-EN}",
        r"\ufcSource{SYNTHETIC-MINTED-SOURCE}",
        INPUT))
    pages = [
        "LIST OF CODE LISTINGS\nCode 1 — OPTIONAL-MINTED-EN",
        "OPTIONAL-MINTED-EN\n"
        "def saudacao(nome: str) -> str:\n"
        "  return f\"Olá, {nome}!\"\n"
        "print(saudacao(\"UFC\"))\n"
        "Source: SYNTHETIC-MINTED-SOURCE",
    ]
    log = "minted.sty\nrunsystem(latexminted config"
    require(validate_case(src, pages, log, "en", "optional-minted")["status"]
            == "BOUNDED_REAL_PDF_PASS", "B4 minted positive guard broken")
    mutation_set = [
        (src.replace(INPUT, ""), pages, log),
        (src.replace("code=minted", "code=listings"), pages, log),
        (src.replace("SYNTHETIC-MINTED-SOURCE", "FORGED"), pages, log),
        (src, [pages[0], pages[1].replace("def saudacao", "def missing")], log),
        (src, [pages[0], pages[1].replace("print(saudacao", "print(missing")], log),
        (src, [pages[0], pages[1].replace("SYNTHETIC-MINTED-SOURCE",
                                           "MISSING-SOURCE")], log),
        (src, [pages[1], pages[0]], log),
        (src, pages, "minted.sty only"),
        (src, pages, "runsystem(latexminted config only"),
    ]
    count = 0
    for bad_src, bad_pages, bad_log in mutation_set:
        try:
            validate_case(bad_src, bad_pages, bad_log,
                          "en", "optional-minted")
        except ValueError:
            count += 1
        else:
            raise ValueError("B4 InputMinted negative source/output control escaped")
    require(count == len(mutation_set) == 9,
            "B4 minted negative mutation count drift")
    return count


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check_file(path: Path, expected: str, folder: Path) -> bytes:
    require(path.resolve().is_relative_to(folder.resolve()) and path.is_file()
            and re.fullmatch(r"[a-f0-9]{64}", expected) is not None,
            "B4 minted original file path or hash format invalid")
    raw = path.read_bytes()
    require(sha(raw) == expected,
            "B4 minted original PDF/source bytes do not match SHA256 receipt")
    return raw


def catalog(pdf: Path, locale: str) -> None:
    data = json.loads(subprocess.check_output(
        ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)], cwd=ROOT, text=True))
    objects = data["qpdf"]
    require(len(objects) == 2 and objects[0].get("jsonversion") == 2,
            "B4 minted malformed original PDF catalog")
    root = objects[1]["trailer"]["value"]["/Root"]
    require(re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root) is not None,
            "B4 minted invalid PDF root reference")
    actual = objects[1]["obj:" + root]["value"]
    require(actual.get("/Type") == "/Catalog"
            and actual.get("/Lang") == "u:" + LANGUAGES[locale],
            "B4 minted original PDF /Root/Lang differs from expected language")


def run(locale: str) -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                     cwd=ROOT, text=True).strip()
    require(os.getenv("SOURCE_COMMIT_SHA") in (None, commit),
            "B4 original minted checkout/source SHA mismatch")
    folder = OUTPUT / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    original = json.loads((folder / "optional-api-behavior-receipts.json")
                          .read_text(encoding="utf-8"))
    require(manifest["source_commit_sha"] == original["source_sha"] == commit
            and manifest["locale"] == original["locale"] == locale,
            "B4 minted original provenance mismatch")
    records = []
    for item in manifest["pdfs"]:
        case = item["profile"]
        require(case in CASES, "B4 minted unexpected optional source scenario")
        name = case + "-" + locale
        raw = check_file(folder / (name + ".tex"), item["source_sha256"], folder)
        pdf = folder / (name + ".pdf")
        check_file(pdf, item["pdf_sha256"], folder)
        log = (folder / (name + ".log")).read_text(errors="replace")
        pages = subprocess.check_output(["pdfinfo", str(pdf)],
                                        cwd=ROOT, text=True)
        match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", pages)
        require(match is not None, "B4 minted physical PDF count missing")
        pdftxt = subprocess.check_output(
            ["pdftotext", "-layout", str(pdf), "-"], cwd=ROOT, text=True)
        compiled = pages_from_pdf(pdftxt, int(match.group(1)))
        catalog(pdf, locale)
        result = validate_case(raw.decode("utf-8"), compiled, log, locale, case)
        previous = [row for row in original["records"]
                    if row["identifier"] == API and row["scenario"] == case]
        require(len(previous) == 1
                and (previous[0]["status"] == "BOUNDED_FUNCTIONAL_OUTPUT_PASS")
                == (result["status"] == "BOUNDED_REAL_PDF_PASS"),
                "B4 minted new proof contradicts original seven-API receipt")
        records.append({"scenario": case, "locale": locale,
                        "source_sha256": item["source_sha256"],
                        "pdf_sha256": item["pdf_sha256"], "observation": result})
    require(len(records) == 3
            and sum(r["observation"]["status"] == "BOUNDED_REAL_PDF_PASS"
                    for r in records) == 1,
            "B4 minted one positive/two inapplicable receipt contract drift")
    (folder / "b4-inputminted-proof.json").write_text(json.dumps({
        "source_sha": commit, "locale": locale, "real_pdfs": 3,
        "identifier": API, "positive": 1, "not_exercised": 2,
        "negative_controls": 9, "records": records,
        "ledger_promotion": "NOT_AUTOMATIC",
        "human_normative_linguistic_review": "PENDING",
        "publication_authorized": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"I18N-B4-INPUTMINTED status=PASS locale={locale} real_pdfs=3"
          " positives=1 negatives=9 PDF_source_sha256=PASS human_review=PENDING")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LANGUAGES))
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    n = negatives()
    if args.preflight:
        print(f"I18N-B4-INPUTMINTED-PREFLIGHT status=PASS negatives={n}"
              " original_PDF=PENDING")
    elif args.locale:
        run(args.locale)
    else:
        raise ValueError("select --preflight or --locale")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-B4-INPUTMINTED status=FAIL reason={exc}") from exc

#!/usr/bin/env python3
"""Check nine B3 list/contents public commands in original integrated PDFs.

The checker reuses the seven existing profile PDFs per locale. It preserves
actual blank duplex pages, binds sources and PDF bytes to SHA256, verifies
each applicable dedicated list on one physical page, and rejects absent
entries, wrongly placed headings and invented non-applicable commands.
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
OUTPUT = ROOT / "artifacts/integrated-i18n"
LANGS = ("pt", "en", "es", "fr")
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
ACADEMIC = set(PROFILES[:4])
NONARTICLE = set(PROFILES[:-1])
LISTS = {
    "figures": (
        r"\ufcPrintListOfFigures", NONARTICLE,
        ("Lista de Figuras", "List of Figures", "Lista de Figuras", "Liste des figures"),
        "INTEGRATED-OBJECT-", True,
    ),
    "tables": (
        r"\ufcPrintListOfTables", NONARTICLE,
        ("Lista de Tabelas", "List of Tables", "Lista de Tablas", "Liste des tableaux"),
        "INTEGRATED-TABLE-", True,
    ),
    "illustrations": (
        r"\ufcPrintListOfIllustrations", ACADEMIC,
        ("Lista de Ilustrações", "List of Illustrations", "Lista de Ilustraciones",
         "Liste des illustrations"),
        "INTEGRATED-OBJECT-", True,
    ),
    "text-tables": (
        r"\ufcPrintListOfTextTables", ACADEMIC,
        ("Lista de Quadros", "List of Text Tables", "Lista de Cuadros",
         "Liste des encadrés"),
        "INTEGRATED-TEXTTABLE-", True,
    ),
    "charts": (
        r"\ufcPrintListOfCharts", ACADEMIC,
        ("Lista de Gráficos", "List of Charts", "Lista de Gráficos",
         "Liste des graphiques"),
        "INTEGRATED-CHART-", True,
    ),
    "abbreviations": (
        r"\ufcPrintListOfAbbreviationsAndAcronyms", ACADEMIC,
        ("Lista de Abreviaturas e Siglas", "List of Abbreviations and Acronyms",
         "Lista de Abreviaturas y Siglas", "Liste des abréviations et sigles"),
        "INTEGRATED-ABBREVIATION-", False,
    ),
    "symbols": (
        r"\ufcPrintListOfSymbols", ACADEMIC,
        ("Lista de Símbolos", "List of Symbols", "Lista de Símbolos",
         "Liste des symboles"),
        "INTEGRATED-SYMBOL-", False,
    ),
    "contents": (
        r"\ufcPrintTableOfContents", NONARTICLE,
        ("Sumário", "Contents", "Índice general", "Table des matières"),
        "INTEGRATED-SECTION-", True,
    ),
}
ENTRY = r"\ufcListEntry"
IDENTIFIERS = tuple(value[0] for value in LISTS.values()) + (ENTRY,)


def ensure(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def normalized(value: str) -> str:
    value = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'"))
    text = re.sub(r"\s+", " ", "".join(
        ch for ch in value if not unicodedata.combining(ch)))
    return re.sub(r"-(?=\s+\w)\s+", "-", text)


def actual_pages(raw: str, expected: int | None = None) -> list[str]:
    # Form feeds are physical pages; internal blank leaves are not optional.
    pages = raw.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    ensure(len(pages) >= 1 and (expected is None or len(pages) == expected),
           "real PDF physical page count differs from Poppler's page boundaries")
    return pages


def observe(source: str, pages: list[str], profile: str, locale: str) -> list[dict]:
    ensure(profile in PROFILES and locale in LANGS and len(pages) >= 1,
           "unsupported B3 integrated PDF case")
    body_marker = normalized(f"INTEGRATED-MANUSCRIPT-{locale}")
    body_pages = [idx for idx, pg in enumerate(pages)
                  if body_marker in normalized(pg)]
    ensure(len(body_pages) == 1,
           "real manuscript body marker absent or duplicated")
    body_index = body_pages[0]
    report = []
    for key, (command, applicable, labels, marker, body_required) in LISTS.items():
        applies = profile in applicable
        actual_count = source.count(command)
        ensure(actual_count == int(applies),
               f"B3 source command applicability drift: {profile}/{locale}/{command}")
        heading = normalized(labels[LANGS.index(locale)])
        marker_text = normalized(marker + locale.upper())
        heading_pages = [
            idx for idx, page in enumerate(pages)
            if any(normalized(line).strip() == heading for line in page.splitlines())
        ]
        if applies:
            ensure(len(heading_pages) == 1,
                   f"B3 dedicated list heading missing or duplicated: {key}/{profile}/{locale}")
            index = heading_pages[0]
            ensure(index < body_index,
                   f"B3 pretextual list is inside/after the manuscript body: {key}")
            ensure(marker_text in normalized(pages[index]),
                   f"B3 list entry absent from heading physical page: {key}/{profile}/{locale}")
            body_page = None
            if body_required:
                later = [i for i, page in enumerate(pages)
                         if i >= body_index and i > index
                         and marker_text in normalized(page)]
                ensure(bool(later),
                       f"B3 entry missing after list: {key}/{profile}/{locale}")
                body_page = later[0] + 1
            report.append({
                "identifier": command, "applicability": "BOUNDED_REAL_PDF_PASS",
                "heading_physical_page": index + 1,
                "entry_marker": marker + locale.upper(),
                "body_physical_page": body_page,
            })
        else:
            ensure(not heading_pages, f"B3 list printed outside applicable profile: {key}/{profile}")
            report.append({
                "identifier": command, "applicability": "NOT_EXERCISED_IN_PROFILE",
                "reason": "This profile does not invoke this public pretextual list",
            })
    entry_source = f"\\ufcListEntry{{INTEGRATED-TERM-{locale.upper()}}}"
    ensure(source.count(entry_source) == 1,
           "B3 public ListEntry source missing or duplicated")
    term = normalized(f"INTEGRATED-TERM-{locale.upper()}")
    definition = normalized(f"INTEGRATED-DEFINITION-{locale.upper()}")
    matches = [
        idx for idx, page in enumerate(pages)
        if term in normalized(page) and definition in normalized(page)
    ]
    ensure(len(matches) == 1 and matches[0] >= body_index,
           "B3 ListEntry term/definition missing, duplicated or outside textual body")
    report.append({
        "identifier": ENTRY, "applicability": "BOUNDED_REAL_PDF_PASS",
        "term_physical_page": matches[0] + 1,
        "entry_marker": f"INTEGRATED-TERM-{locale.upper()}",
        "definition_marker": f"INTEGRATED-DEFINITION-{locale.upper()}",
    })
    ensure(len(report) == 9, "B3 integrated command inventory drift")
    return report


def negative_controls() -> int:
    # Synthetic source/PDF mutations call the same per-list predicates.
    source = (r"\ufcPrintListOfFigures"
              "\n\\ufcListEntry{INTEGRATED-TERM-EN}{INTEGRATED-DEFINITION-EN}")
    # The isolated source tests the one list; the full positive source models
    # all eight list commands, because controls must not accept partial setup.
    source = "\n".join([
        command for command, *_ in LISTS.values()
    ]) + "\n" + source.split("\n")[-1]
    pages = [
        "TITLE",
        "List of Figures\nINTEGRATED-OBJECT-EN",
        "List of Tables\nINTEGRATED-TABLE-EN",
        "List of Illustrations\nINTEGRATED-OBJECT-EN",
        "List of Text Tables\nINTEGRATED-TEXTTABLE-EN",
        "List of Charts\nINTEGRATED-CHART-EN",
        "List of Abbreviations and Acronyms\nINTEGRATED-ABBREVIATION-EN",
        "List of Symbols\nINTEGRATED-SYMBOL-EN",
        "Contents\nINTEGRATED-SECTION-EN",
        ("INTEGRATED-MANUSCRIPT-EN-DOCTORALTHESIS "
         "INTEGRATED-OBJECT-EN INTEGRATED-TABLE-EN "
         "INTEGRATED-TEXTTABLE-EN INTEGRATED-CHART-EN "
         "INTEGRATED-SECTION-EN INTEGRATED-TERM-EN "
         "INTEGRATED-DEFINITION-EN"),
    ]
    ensure(len(observe(source, pages, "doctoral-thesis", "en")) == 9,
           "B3 positive all-list control invalid")
    count = 0
    for key, (command, _, headings, marker, _) in LISTS.items():
        loc_heading = headings[LANGS.index("en")]
        wrong_src = source.replace(command, "", 1)
        wrong_pages = [
            p.replace(loc_heading, "WRONG LIST HEADING", 1) for p in pages
        ]
        for value, content in ((wrong_src, pages), (source, wrong_pages)):
            try:
                observe(value, content, "doctoral-thesis", "en")
            except ValueError:
                count += 1
            else:
                raise ValueError(f"B3 negative {key} escaped")
    changed = [x.replace("INTEGRATED-DEFINITION-EN", "MISSING-DEFINITION")
               for x in pages]
    for bad in (changed, [pages[0], *pages[1:-1],
                          pages[-1].replace("INTEGRATED-TERM-EN", "")]):
        try:
            observe(source, bad, "doctoral-thesis", "en")
        except ValueError:
            count += 1
        else:
            raise ValueError("B3 ListEntry missing-value mutant escaped")
    # An entry in another pretextual list must not masquerade as a body caption.
    wrong_body = list(pages)
    wrong_body[-1] = wrong_body[-1].replace("INTEGRATED-OBJECT-EN", "")
    try:
        observe(source, wrong_body, "doctoral-thesis", "en")
    except ValueError:
        count += 1
    else:
        raise ValueError("B3 body caption missing after source list was accepted")
    # Pretextual headings and public definitions must never be accepted on
    # the textual body or an unrelated prelim page.
    misplaced_heading = list(pages)
    misplaced_heading[6] = misplaced_heading[6].replace(
        "List of Abbreviations and Acronyms\n", "")
    misplaced_heading[-1] += (
        "\nList of Abbreviations and Acronyms\n"
        "INTEGRATED-ABBREVIATION-EN")
    misplaced_entry = list(pages)
    misplaced_entry[-1] = misplaced_entry[-1].replace(
        "INTEGRATED-TERM-EN INTEGRATED-DEFINITION-EN", "")
    misplaced_entry[0] += (
        " INTEGRATED-TERM-EN INTEGRATED-DEFINITION-EN")
    for mutated in (misplaced_heading, misplaced_entry):
        try:
            observe(source, mutated, "doctoral-thesis", "en")
        except ValueError:
            count += 1
        else:
            raise ValueError("B3 wrong pretextual/textual physical position escaped")
    ensure(count == 21 and len(IDENTIFIERS) == len(set(IDENTIFIERS)) == 9,
           "B3 nine-command negative coverage drift")
    return count


def checked_file(path: Path, expected_hash: str, folder: Path) -> bytes:
    ensure(path.resolve().is_relative_to(folder.resolve()) and path.is_file(),
           "missing original B3 file or path outside locale artifact")
    ensure(re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None,
           "invalid B3 PDF/source SHA256")
    raw = path.read_bytes()
    ensure(hashlib.sha256(raw).hexdigest() == expected_hash,
           "B3 original PDF/source SHA256 mismatch")
    return raw


def run(locale: str) -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    ensure(os.getenv("SOURCE_COMMIT_SHA") in (None, sha), "B3 checkout SHA mismatch")
    folder = OUTPUT / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    ensure(manifest.get("locale") == locale
           and manifest.get("source_sha") == sha
           and len(manifest.get("entries", [])) == 7,
           "B3 original integrated manifest provenance drift")
    receipts = []
    seen = set()
    for row in manifest["entries"]:
        profile = row["profile"]
        ensure(profile in PROFILES and profile not in seen
               and row["locale"] == locale, "missing/duplicate B3 profile")
        seen.add(profile)
        source = checked_file(ROOT / row["source"], row["source_sha256"],
                              folder).decode("utf-8")
        pdf_path = ROOT / row["pdf"]
        checked_file(pdf_path, row["pdf_sha256"], folder)
        info = subprocess.check_output(["pdfinfo", str(pdf_path)],
                                       cwd=ROOT, text=True)
        number = re.search(r"(?m)^Pages:\s*(\d+)\s*$", info)
        ensure(number is not None, "B3 missing physical PDF pages")
        extracted = subprocess.check_output(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            cwd=ROOT, text=True)
        observed = observe(source, actual_pages(extracted, int(number.group(1))),
                           profile, locale)
        receipts.append({
            "profile": profile, "locale": locale,
            "source_sha256": row["source_sha256"],
            "pdf_sha256": row["pdf_sha256"],
            "physical_pages": int(number.group(1)),
            "observations": observed,
        })
    ensure(seen == set(PROFILES) and
           sum(item["applicability"] == "BOUNDED_REAL_PDF_PASS"
               for row in receipts for item in row["observations"]) == 45,
           "B3 complete 7-profile/9-command applicability differs")
    report = {
        "status": "BOUNDED_B3_NINE_COMMAND_PDF_PASS",
        "source_sha": sha, "locale": locale, "real_pdfs": 7,
        "identifiers": list(IDENTIFIERS),
        "positive_observations": 45, "not_exercised_in_profile": 18,
        "negative_controls": 21, "records": receipts,
        "ledger_promotion": "NOT_AUTOMATIC",
        "human_normative_linguistic_review": "PENDING",
        "publication_authorized": False,
    }
    (folder / "b3-integrated-list-proof.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"I18N-B3-INTEGRATED status=PASS locale={locale} IDs=9"
          " real_pdfs=7 positive=45 not_exercised=18 negatives=21"
          " physical_pages=PASS sha256=PASS human_review=PENDING")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=LANGS)
    args = parser.parse_args()
    negative_count = negative_controls()
    if args.preflight:
        print(f"I18N-B3-INTEGRATED-PREFLIGHT status=PASS IDs=9"
              f" negatives={negative_count} real_PDF=PENDING")
    elif args.locale:
        run(args.locale)
    else:
        raise ValueError("select --preflight or --locale")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-B3-INTEGRATED status=FAIL reason={exc}") from exc

#!/usr/bin/env python3
"""Recheck actual optional-module PDF outputs for seven bounded public APIs.

A fixture not exercising a public API is not a product feature failure.
Only applicable source, log, PDF, and language predicates produce PASS.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "artifacts/optional-i18n"
LOCALES = {
    "pt": ("pt-BR", "brazilian", "Fonte", "Nota", "Lista de Códigos", "Lista de Algoritmos", "Algoritmo"),
    "en": ("en-US", "english", "Source", "Note", "List of Code Listings", "List of Algorithms", "Algorithm"),
    "es": ("es-ES", "spanish", "Fuente", "Nota", "Lista de Códigos", "Lista de Algoritmos", "Algoritmo"),
    "fr": ("fr-FR", "french", "Source", "Note", "Liste des codes", "Liste des algorithmes", "Algorithme"),
}
SCENARIOS = ("optional-objects", "optional-minted", "optional-algorithm-comment")
ALL_APIS = (
    "tables", "algorithms", r"\ufcPrintListOfCodeListings",
    r"\ufcPrintListOfAlgorithms", r"\ufcInputMinted",
    "ufclisting", "ufcalgorithm",
)
APPLICABLE = {
    "optional-objects": (
        "tables", "algorithms", r"\ufcPrintListOfCodeListings",
        r"\ufcPrintListOfAlgorithms", "ufclisting", "ufcalgorithm",
    ),
    "optional-minted": (
        r"\ufcPrintListOfCodeListings", r"\ufcInputMinted",
    ),
    "optional-algorithm-comment": ("algorithms", "ufcalgorithm"),
}
SOURCE_TOKEN = {
    "tables": "tables=tabularray",
    "algorithms": "algorithms=algpseudocodex",
    r"\ufcPrintListOfCodeListings": r"\ufcPrintListOfCodeListings",
    r"\ufcPrintListOfAlgorithms": r"\ufcPrintListOfAlgorithms",
    r"\ufcInputMinted": r"\ufcInputMinted[here]{python}{tests/fixtures/example.py}",
    "ufclisting": r"\begin{ufclisting}[here]",
    "ufcalgorithm": r"\begin{ufcalgorithm}[here][1]",
}
TABLE_CONTINUATION = {
    "pt": ("(continua)", "(continuação)", "(conclusão)"),
    "en": ("(continued)", "(continuation)", "(concluded)"),
    "es": ("(continúa)", "(continuación)", "(conclusión)"),
    "fr": ("(à suivre)", "(suite)", "(fin)"),
}


def fold(text: str) -> str:
    text = unicodedata.normalize(
        "NFKD", text.casefold().replace("’", "'").replace("ʼ", "'"))
    text = re.sub(r"\s+", " ", "".join(
        x for x in text if not unicodedata.combining(x)))
    return re.sub(r"-(?=\s+\w)\s+", "-", text)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check_digest(data: bytes, claimed: str) -> None:
    if not isinstance(claimed, str) or not re.fullmatch("[a-f0-9]{64}", claimed):
        raise ValueError("missing/forged source or PDF digest")
    if digest(data) != claimed:
        raise ValueError("actual source or PDF bytes differ from manifest")


def required_pdf_markers(api: str, scenario: str, locale: str) -> tuple[str, ...]:
    if api not in APPLICABLE[scenario]:
        raise ValueError("attempt to certify inapplicable API/scenario")
    lang = LOCALES[locale]
    algorithm_title = lang[6]
    if api == "tables":
        return (f"optional-table-{locale}", f"optional-table-source-{locale}",
                f"optional-table-note-{locale}", "optionalrow110", lang[2] + ":",
                lang[3] + ":", *TABLE_CONTINUATION[locale])
    if api == "algorithms" or api == "ufcalgorithm":
        if scenario == "optional-algorithm-comment":
            return (f"optional-algorithm-only-{locale}", "numerado-1",
                    "numerado-2", "numerado-3", algorithm_title)
        return (f"optional-algorithm-{locale}", "optional-alg-step-1",
                "optional-alg-step-2", algorithm_title)
    if api == r"\ufcPrintListOfCodeListings":
        code_marker = ("sum", "return") if scenario == "optional-objects" else ("saudacao",)
        return (lang[4], f"optional-{'listing' if scenario == 'optional-objects' else 'minted'}-{locale}",
                *code_marker)
    if api == r"\ufcPrintListOfAlgorithms":
        return (lang[5], f"optional-algorithm-{locale}")
    if api == r"\ufcInputMinted":
        return (f"optional-minted-{locale}", "synthetic-minted-source", lang[4],
                "saudacao")
    if api == "ufclisting":
        return (f"optional-listing-{locale}", "synthetic-code-source", lang[4],
                "sum", "return")
    raise ValueError("unrecognized API")


def check_dedicated_list_pages(pdf_text: str, scenario: str, locale: str) -> None:
    """Require actual list entries on pretextual list pages, not object captions.

    The fixture's list pages precede the body. Their captions also appear
    later in the body, which cannot substitute for a missing list entry.
    """
    if scenario == "optional-algorithm-comment":
        return
    pages = [fold(page) for page in pdf_text.split("\f") if page.strip()]
    expected = [
        (LOCALES[locale][4],
         f"optional-{'listing' if scenario == 'optional-objects' else 'minted'}-{locale}"),
    ]
    if scenario == "optional-objects":
        expected.append((LOCALES[locale][5], f"optional-algorithm-{locale}"))
    if len(pages) <= len(expected):
        raise ValueError("optional pretextual list/body pages missing")
    body = f"optional-module-body-{locale}"
    for index, (heading, entry) in enumerate(expected):
        current = pages[index]
        if fold(heading) not in current:
            raise ValueError(f"missing localized list heading on dedicated page {index+1}")
        if fold(entry) not in current:
            raise ValueError(f"missing actual entry in list section {heading}/{scenario}/{locale}")
        if body in current:
            raise ValueError("document body cannot substitute for list entry page")
    if not any(body in page for page in pages[len(expected):]):
        raise ValueError("PDF lacks body after the dedicated list pages")


def validate_case(locale: str, scenario: str, source: str, log: str,
                  pdf_text: str, actual_catalog: str) -> list[dict]:
    if locale not in LOCALES or scenario not in SCENARIOS:
        raise ValueError("unsupported scenario/locale")
    expected_bcp, babel = LOCALES[locale][:2]
    if actual_catalog != expected_bcp:
        raise ValueError("real PDF catalog language differs from locale")
    if f"OPTIONAL-I18N-BABEL={babel}" not in log:
        raise ValueError("TeX did not activate expected Babel language")
    visible = fold(pdf_text)
    expected_body = (f"optional-algorithm-only-{locale}" if scenario == "optional-algorithm-comment"
                     else f"optional-module-body-{locale}")
    if expected_body not in visible:
        raise ValueError("real optional PDF body marker missing")
    check_dedicated_list_pages(pdf_text, scenario, locale)
    # The source must contain the listing code itself, not only the caption.
    # The minted fixture must point to a known file with a stable code token.
    if scenario == "optional-objects" and "int sum(int a, int b)" not in source:
        raise ValueError("actual listing source code is missing")
    if scenario == "optional-minted":
        fixture = ROOT / "tests/fixtures/example.py"
        if not fixture.is_file() or "saudacao" not in fixture.read_text(encoding="utf-8"):
            raise ValueError("minted Python code fixture is missing or changed")
    results = []
    for api in ALL_APIS:
        applied = api in APPLICABLE[scenario]
        source_present = SOURCE_TOKEN[api] in source
        if applied != source_present:
            raise ValueError(f"fixture API applicability drift: {api}/{scenario}")
        if applied:
            checks = required_pdf_markers(api, scenario, locale)
            # PDF extraction may split C++ tokens with unpredictable spaces.
            # Match code identifiers as whole lexical words, not line layout.
            absent = [marker for marker in checks
                      if (not re.search(r"(?<![a-z0-9_])" + re.escape(fold(marker))
                                       + r"(?![a-z0-9_])", visible)
                          if marker in ("sum", "return")
                          else fold(marker) not in visible)]
            if absent:
                raise ValueError(f"actual PDF missing output for {api}/{scenario}/{locale}: {absent}")
            results.append({
                "identifier": api, "scenario": scenario, "locale": locale,
                "status": "BOUNDED_FUNCTIONAL_OUTPUT_PASS",
                "pdf_predicates": checks, "pdf_catalog_lang": actual_catalog,
                "output_source": "rendered-PDF-text-plus-TeX-Babel-and-fixture-option",
            })
        else:
            results.append({
                "identifier": api, "scenario": scenario, "locale": locale,
                "status": "NOT_EXERCISED_IN_THIS_FIXTURE",
                "reason": "test scenario intentionally does not invoke this API",
            })
    if len(results) != 7:
        raise ValueError("incomplete seven-API case")
    return results


def catalog_lang(obj: dict) -> str:
    data = obj.get("qpdf")
    if not isinstance(data, list) or len(data) != 2 or data[0].get("jsonversion") != 2:
        raise ValueError("qpdf v2 schema drift")
    entry = data[1]
    root = entry["trailer"]["value"]["/Root"]
    if not isinstance(root, str) or not re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root):
        raise ValueError("invalid PDF root reference")
    catalog = entry["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("PDF root is not catalog")
    value = catalog.get("/Lang")
    if not isinstance(value, str) or not value.startswith("u:"):
        raise ValueError("missing Unicode /Root/Lang")
    return value[2:]


def negative_controls() -> int:
    failures = 0
    for scenario in SCENARIOS:
        locale = "en"
        lang = LOCALES[locale]
        source = " ".join(SOURCE_TOKEN[a] for a in APPLICABLE[scenario])
        if scenario == "optional-objects":
            source += "\nint sum(int a, int b) { return a + b; }"
        markers = set()
        for api in APPLICABLE[scenario]:
            markers.update(required_pdf_markers(api, scenario, locale))
        markers.add("OPTIONAL-ALGORITHM-ONLY-EN" if scenario == "optional-algorithm-comment"
                    else "OPTIONAL-MODULE-BODY-EN")
        list_pages = []
        if scenario != "optional-algorithm-comment":
            entry = f"optional-{'listing' if scenario == 'optional-objects' else 'minted'}-{locale}"
            list_pages.append(f"{lang[4]}\nCode 1 — {entry}")
            if scenario == "optional-objects":
                list_pages.append(f"{lang[5]}\nAlgorithm 1 — optional-algorithm-{locale}")
        body = "\f".join([*list_pages, "\n".join(markers)])
        log = "OPTIONAL-I18N-BABEL=english"
        valid = validate_case(locale, scenario, source, log, body, "en-US")
        if sum(v["status"] == "BOUNDED_FUNCTIONAL_OUTPUT_PASS" for v in valid) != len(APPLICABLE[scenario]):
            raise ValueError("negative test baseline has wrong applicability")
        for api in APPLICABLE[scenario]:
            bad_source = source.replace(SOURCE_TOKEN[api], "", 1)
            # Remove every casing of this semantic marker; generated fixture
            # markers may also occur in the uppercase document-body sentinel.
            marker = required_pdf_markers(api, scenario, locale)[0]
            bad_body = re.sub(re.escape(marker), "REMOVED", body, flags=re.IGNORECASE)
            for args in ((locale, scenario, bad_source, log, body, "en-US"),
                         (locale, scenario, source, log, bad_body, "en-US")):
                try:
                    validate_case(*args)
                except ValueError:
                    failures += 1
                else:
                    raise ValueError(f"unrejected missing source/PDF mutant: {api}")
        # A list heading alone must not count as a populated list. Remove
        # the list entry on its own page but retain its body caption and code.
        list_entries = (
            [f"optional-{'listing' if scenario == 'optional-objects' else 'minted'}-{locale}"]
            + ([f"optional-algorithm-{locale}"] if scenario == "optional-objects" else [])
            if scenario != "optional-algorithm-comment" else []
        )
        for index, entry in enumerate(list_entries):
            pages = body.split("\f")
            changed_page = re.sub(re.escape(entry), "ENTRY_REMOVED", pages[index],
                                  flags=re.IGNORECASE)
            if changed_page == pages[index]:
                raise ValueError("list-only negative mutation did not change list")
            pages[index] = changed_page
            try:
                validate_case(locale, scenario, source, log, "\f".join(pages), "en-US")
            except ValueError:
                failures += 1
            else:
                raise ValueError("missing list entry accepted despite body caption")
        # Removing only the rendered code (and retaining titles, captions,
        # source attributions and lists) must invalidate the PDF evidence.
        code_marker = ("sum" if scenario == "optional-objects" else
                       "saudacao" if scenario == "optional-minted" else None)
        if code_marker:
            stripped_pdf = re.sub(re.escape(code_marker), "CODE_REMOVED", body,
                                  flags=re.IGNORECASE)
            if stripped_pdf == body:
                raise ValueError("code-only negative mutation did not change PDF")
            try:
                validate_case(locale, scenario, source, log, stripped_pdf, "en-US")
            except ValueError:
                failures += 1
            else:
                raise ValueError("rendered code missing but test reported PASS")
        for args in ((locale, scenario, source, log, body, "pt-BR"),
                     (locale, scenario, source, "OPTIONAL-I18N-BABEL=french", body, "en-US"),
                     (locale, scenario, source, log, re.sub(
                         "OPTIONAL-ALGORITHM-ONLY-EN" if scenario == "optional-algorithm-comment"
                         else "OPTIONAL-MODULE-BODY-EN", "LOST", body,
                         flags=re.IGNORECASE), "en-US")):
            try:
                validate_case(*args)
            except ValueError:
                failures += 1
            else:
                raise ValueError("unrejected locale/Babel/content mutant")
    check_digest(b"authentic-PDF", digest(b"authentic-PDF"))
    try:
        check_digest(b"forged-PDF", digest(b"authentic-PDF"))
    except ValueError:
        failures += 1
    else:
        raise ValueError("forged PDF digest accepted")
    pdf_catalog = {"qpdf": [{"jsonversion": 2}, {
        "trailer": {"value": {"/Root": "1 0 R"}},
        "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:en-US"}}}]}
    if catalog_lang(pdf_catalog) != "en-US":
        raise ValueError("PDF catalog positive control failed")
    invalid = copy.deepcopy(pdf_catalog)
    invalid["qpdf"][1]["obj:1 0 R"]["value"].pop("/Lang")
    try:
        catalog_lang(invalid)
    except ValueError:
        failures += 1
    else:
        raise ValueError("missing PDF catalog language accepted")
    expected = 2 * sum(map(len, APPLICABLE.values())) + 3 * len(SCENARIOS) + 7
    if failures != expected:
        raise ValueError(f"wrong negative control count: {failures}/{expected}")
    return failures


def source_file(folder: Path, name: str, suffix: str) -> Path:
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("unsafe fixture name")
    path = (folder / (name + suffix)).resolve()
    if not path.is_relative_to(folder.resolve()) or not path.is_file():
        raise ValueError("PDF/source/log artifact outside locale folder or absent")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    negatives = negative_controls()
    if args.self_test:
        print(f"I18N-OPTIONAL-API-PREFLIGHT status=PASS identifiers=7"
              f" negative_controls={negatives} actual_pdf_certification=PENDING")
        return
    if not args.locale:
        raise ValueError("select --locale or --self-test")
    locale = args.locale
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    expected = os.getenv("SOURCE_COMMIT_SHA")
    if expected and expected != sha:
        raise ValueError("CI checkout SHA mismatch")
    folder = ARTIFACTS / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if (manifest.get("source_commit_sha") != sha or manifest.get("locale") != locale
            or manifest.get("status") != "AUTOMATED_PARTIAL"):
        raise ValueError("optional PDF manifest does not describe current source SHA/locale")
    entries = manifest.get("pdfs")
    if not isinstance(entries, list) or len(entries) != 3:
        raise ValueError("expected three actually compiled optional PDFs")
    observations = []
    unique_scenarios = set()
    for entry in entries:
        scenario = entry.get("profile")
        if scenario not in SCENARIOS or scenario in unique_scenarios or entry.get("locale") != locale:
            raise ValueError("duplicate/missing/invalid optional scenario")
        unique_scenarios.add(scenario)
        stem = scenario + "-" + locale
        src = source_file(folder, stem, ".tex")
        pdf = source_file(folder, stem, ".pdf")
        if (entry.get("source") != src.relative_to(ROOT).as_posix()
                or entry.get("pdf") != pdf.relative_to(ROOT).as_posix()):
            raise ValueError("manifest source/PDF does not match scenario")
        check_digest(src.read_bytes(), entry.get("source_sha256"))
        check_digest(pdf.read_bytes(), entry.get("pdf_sha256"))
        source = src.read_text(encoding="utf-8")
        log = source_file(folder, stem, ".log").read_text(
            encoding="utf-8", errors="replace")
        pdf_text = subprocess.check_output(
            ["pdftotext", "-layout", str(pdf), "-"], cwd=ROOT, text=True)
        catalog = catalog_lang(json.loads(subprocess.check_output(
            ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)],
            cwd=ROOT, text=True)))
        if catalog != entry.get("pdf_catalog_lang") or entry.get("babel") != LOCALES[locale][1]:
            raise ValueError("real PDF and recorded locale differ")
        cases = validate_case(locale, scenario, source, log, pdf_text, catalog)
        for result in cases:
            result["source_sha256"] = entry["source_sha256"]
            result["pdf_sha256"] = entry["pdf_sha256"]
            result["pdf"] = entry["pdf"]
        observations.extend(cases)
        passed = sum(item["status"] == "BOUNDED_FUNCTIONAL_OUTPUT_PASS" for item in cases)
        print(f"I18N-OPTIONAL-API status=PASS locale={locale} scenario={scenario}"
              f" actual_pdf=true applicable={passed} inapplicable={7-passed}"
              " source_hash=PASS pdf_hash=PASS qpdf_catalog=PASS", flush=True)
    if unique_scenarios != set(SCENARIOS):
        raise ValueError("one optional scenario was omitted")
    total_pass = sum(item["status"] == "BOUNDED_FUNCTIONAL_OUTPUT_PASS" for item in observations)
    total_na = sum(item["status"] == "NOT_EXERCISED_IN_THIS_FIXTURE" for item in observations)
    if len(observations) != 21 or total_pass != 10 or total_na != 11:
        raise ValueError("unexpected applicable/inapplicable optional API counts")
    report = {
        "status": "BOUNDED_REAL_PDF_OPTIONAL_API_PASS",
        "source_sha": sha, "locale": locale,
        "scenario_count": 3, "real_pdfs_reused": 3,
        "public_api_identifiers": list(ALL_APIS), "applicable_observations": total_pass,
        "not_exercised_in_this_fixture": total_na,
        "negative_controls": negatives,
        "not_claimed": "global_72_api_i18n_or_human_visual_linguistic_acceptance",
        "records": observations,
    }
    (folder / "optional-api-behavior-receipts.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"I18N-OPTIONAL-API status=PASS locale={locale} real_pdfs=3"
          " public_identifiers=7 applicable=10 not_exercised=11"
          f" negative_controls={negatives} PDF_and_Babel=PASS human_review=PENDING")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-OPTIONAL-API status=FAIL reason={exc}") from exc

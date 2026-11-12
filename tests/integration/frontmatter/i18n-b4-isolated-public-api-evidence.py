#!/usr/bin/env python3
"""Create two isolated B4 public API real-PDF probes in each language.

The original integrated and optional suites do not exercise InputListing or
legacy keywords in four languages. This suite genuinely compiles PDF/TeX
positives, includes negative controls, and retains source-bound artifacts.
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
LOCALES = {
    "pt": ("pt-BR", "Resumo", "Palavras-chave:"),
    "en": ("en-US", "Abstract", "Keywords:"),
    "es": ("es-ES", "Resumen", "Palabras clave:"),
    "fr": ("fr-FR", "Résumé", "Mots-clés:"),
}
LISTING_API = r"\ufcInputListing"
KEYWORDS_API = r"\keywords"
CPP = "tests/fixtures/example.cpp"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fold(value: str) -> str:
    value = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'"))
    return re.sub(r"\s+", " ", "".join(
        c for c in value if not unicodedata.combining(c)))


def pages(text: str, count: int | None = None) -> list[str]:
    items = text.split("\f")
    if items and not items[-1].strip():
        items.pop()
    require(bool(items) and (count is None or count == len(items)),
            "B4 isolated physical PDF page boundary mismatch")
    return items


def pdf_catalog(pdf: Path, locale: str) -> str:
    data = json.loads(subprocess.check_output([
        "qpdf", "--json=2", "--json-key=qpdf", str(pdf)
    ], cwd=ROOT, text=True))
    records = data["qpdf"]
    require(len(records) == 2 and records[0].get("jsonversion") == 2,
            "B4 isolated qpdf JSON schema drift")
    root = records[1]["trailer"]["value"]["/Root"]
    require(re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root) is not None,
            "B4 isolated invalid PDF root object")
    item = records[1]["obj:" + root]["value"]
    expected = LOCALES[locale][0]
    require(item.get("/Type") == "/Catalog"
            and item.get("/Lang") == "u:" + expected,
            "B4 isolated original PDF catalog language mismatch")
    return expected


def source_for_listing(locale: str) -> str:
    language = LOCALES[locale][0]
    return "\n".join((
        rf"\DocumentMetadata{{lang={language},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{type=scientific-article,document-language={locale},"
        r"cover=false,coat-of-arms=false,catalog-card=false,code=listings,"
        r"title={Isolated source listing test},author={Synthetic Author}}",
        r"\begin{document}",
        r"\textual",
        rf"\section{{B4-LISTING-BODY-{locale.upper()}}}",
        rf"\legend{{code}}{{B4-LISTING-CAPTION-{locale.upper()}}}",
        rf"\ufcSource{{B4-LISTING-SOURCE-{locale.upper()}}}",
        rf"\ufcInputListing[language=C++]{{{CPP}}}",
        r"\end{document}",
        "",
    ))


def source_for_keywords(locale: str, body_file: str) -> str:
    language = LOCALES[locale][0]
    return "\n".join((
        rf"\DocumentMetadata{{lang={language},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{type=doctoral-thesis,document-language={locale},"
        r"cover=false,coat-of-arms=false,catalog-card=false,"
        r"title={Legacy keywords test},author={Synthetic Author},"
        r"doctoral-graduate-program={Synthetic Program},"
        r"doctoral-degree-field={Computer Science}}",
        r"\begin{document}",
        r"\pretextual",
        rf"\ufcPrintSummaryInLanguage{{{locale}}}{{{body_file}}}",
        r"\textual",
        rf"\section{{B4-KEYWORDS-BODY-{locale.upper()}}}",
        r"\end{document}",
        "",
    ))


def validate_source(api: str, source: str, body: str, locale: str) -> None:
    require(locale in LOCALES, "unsupported B4 isolated locale")
    if api == LISTING_API:
        require(source.count(r"\ufcInputListing[language=C++]{") == 1
                and CPP in source and "code=listings" in source,
                "B4 InputListing actual external C++ import missing")
        require(r"\legend{code}{B4-LISTING-CAPTION-" in source,
                "B4 InputListing synthetic caption absent")
    elif api == KEYWORDS_API:
        require(body.count(r"\keywords{") == 1
                and ("keyword-" + locale + "-legacy") in body
                and r"\ufcPrintSummaryInLanguage{" + locale + "}" in source,
                "B4 legacy keywords must occur inside explicitly localized summary")
    else:
        raise ValueError("not a B4 isolated public identifier")


def inspect_pdf(api: str, text: str, locale: str) -> None:
    require(locale in LOCALES, "invalid B4 locale")
    output = fold(text)
    if api == LISTING_API:
        markers = (
            "b4-listing-body-" + locale,
            "b4-listing-caption-" + locale,
            "b4-listing-source-" + locale,
            "int main()", "std::cout", "ufc",
        )
        require(all(fold(marker) in output for marker in markers),
                "B4 real InputListing imported C++ program not rendered in PDF")
    elif api == KEYWORDS_API:
        label, title = LOCALES[locale][2], LOCALES[locale][1]
        markers = (
            title, label, "keyword-" + locale + "-legacy",
            "b4-keywords-body-" + locale,
        )
        require(all(fold(marker) in output for marker in markers),
                "B4 legacy keywords or localized summary label missing in PDF")
        require(not any(
            fold(LOCALES[other][2]) in output
            for other in LOCALES if other != locale
        ), "B4 wrong-language keywords label leaked into PDF")
    else:
        raise ValueError("unknown isolated B4 API")


def negatives() -> int:
    count = 0
    for locale in LOCALES:
        listing = source_for_listing(locale)
        body = "B4-KEYWORDS-CONTENT-" + locale + r" \keywords{keyword-" + locale + "-legacy.}"
        keywords = source_for_keywords(locale, "synthetic/body.tex")
        validate_source(LISTING_API, listing, "", locale)
        validate_source(KEYWORDS_API, keywords, body, locale)
        for api, bad_source, bad_body in (
            (LISTING_API, listing.replace("code=listings", "code=minted"), ""),
            (LISTING_API, listing.replace(CPP, "wrong.cpp"), ""),
            (KEYWORDS_API, keywords, body.replace(r"\keywords{", r"\wrong{")),
            (KEYWORDS_API, keywords.replace(
                r"\ufcPrintSummaryInLanguage{" + locale + "}",
                r"\ufcPrintSummaryInLanguage{en}"), body),
        ):
            try:
                validate_source(api, bad_source, bad_body, locale)
            except ValueError:
                count += 1
            else:
                raise ValueError("B4 isolated source mutation escaped")
    # Missing an actual body or summary label must invalidate PDF evidence.
    for api, bad in (
        (LISTING_API, "B4-LISTING-BODY-en B4-LISTING-CAPTION-en"),
        (KEYWORDS_API, "Abstract keyword-en-legacy B4-KEYWORDS-BODY-en"),
    ):
        try:
            inspect_pdf(api, bad, "en")
        except ValueError:
            count += 1
        else:
            raise ValueError("B4 isolated missing-PDF-output mutation escaped")
    require(count == 18 and len(pages("P1\f\fP3\f")) == 3,
            "B4 isolated source/output negative coverage drift")
    return count


def compile_one(locale: str, api: str, source: str,
                companion: tuple[str, str] | None = None) -> dict:
    folder = OUTPUT / locale / "b4-isolated"
    folder.mkdir(parents=True, exist_ok=True)
    job = f"b4-{locale}-{'listing' if api == LISTING_API else 'keywords'}"
    src = folder / (job + ".tex")
    src.write_text(source, encoding="utf-8")
    body_sha = None
    if companion:
        name, body_text = companion
        body_path = ROOT / name
        body_path.parent.mkdir(parents=True, exist_ok=True)
        body_path.write_text(body_text, encoding="utf-8")
        body_sha = sha(body_path.read_bytes())
    validate_source(api, source, companion[1] if companion else "", locale)
    for pass_number in (1, 2):
        process = subprocess.run([
            "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
            "-file-line-error", f"-jobname={job}",
            f"-output-directory={folder}", str(src),
        ], cwd=ROOT, text=True, capture_output=True, check=False)
        require(process.returncode == 0,
                f"B4 real PDF compilation failed: {api}/{locale}/pass{pass_number}: "
                + (process.stdout + process.stderr)[-850:])
    pdf = folder / (job + ".pdf")
    require(pdf.is_file() and pdf.stat().st_size > 1000,
            "B4 real PDF missing or truncated")
    subprocess.run(["qpdf", "--check", str(pdf)], check=True,
                   cwd=ROOT, capture_output=True, text=True)
    pdf_lang = pdf_catalog(pdf, locale)
    info = subprocess.check_output(["pdfinfo", str(pdf)], cwd=ROOT, text=True)
    match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", info)
    require(match is not None, "B4 real PDF physical pages absent")
    txt = subprocess.check_output(
        ["pdftotext", "-layout", str(pdf), "-"], cwd=ROOT, text=True)
    originals = pages(txt, int(match.group(1)))
    inspect_pdf(api, "\f".join(originals), locale)
    return {"identifier": api, "locale": locale, "source_sha256": sha(src.read_bytes()),
            "pdf_sha256": sha(pdf.read_bytes()), "body_sha256": body_sha,
            "pdf_catalog_lang": pdf_lang, "physical_pages": len(originals),
            "source": str(src.relative_to(ROOT)),
            "pdf": str(pdf.relative_to(ROOT)),
            "status": "BOUNDED_ISOLATED_REAL_PDF_PASS"}


def run(locale: str) -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                     cwd=ROOT, text=True).strip()
    require(os.getenv("SOURCE_COMMIT_SHA") in (None, commit),
            "B4 real-PDF isolated source SHA mismatch")
    folder = OUTPUT / locale / "b4-isolated"
    companion_path = folder / (f"b4-{locale}-keywords-body.tex")
    relative = companion_path.relative_to(ROOT).as_posix()
    body = (f"B4-KEYWORDS-CONTENT-{locale.upper()}. "
            rf"\keywords{{keyword-{locale}-legacy.}}")
    proofs = [
        compile_one(locale, LISTING_API, source_for_listing(locale)),
        compile_one(locale, KEYWORDS_API, source_for_keywords(locale, relative),
                    (relative, body)),
    ]
    (folder / "manifest.json").write_text(
        json.dumps({
            "status": "BOUNDED_B4_TWO_ISOLATED_APIS_REAL_PDF_PASS",
            "source_sha": commit, "locale": locale,
            "identifiers": [LISTING_API, KEYWORDS_API],
            "records": proofs, "negative_controls": 18,
            "human_normative_linguistic_review": "PENDING",
            "ledger_promotion": "NOT_AUTOMATIC",
            "publication_authorized": False,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"I18N-B4-ISOLATED status=PASS locale={locale} api=2"
          " actual_pdfs=2 source_PDF_sha256=PASS negatives=18 human_review=PENDING")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES))
    parser.add_argument("--preflight", action="store_true")
    a = parser.parse_args()
    n = negatives()
    if a.preflight:
        print(f"I18N-B4-ISOLATED-PREFLIGHT status=PASS IDs=2"
              f" negatives={n} actual_PDF=PENDING")
    elif a.locale:
        run(a.locale)
    else:
        raise ValueError("choose --preflight or --locale")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-B4-ISOLATED status=FAIL reason={exc}") from exc

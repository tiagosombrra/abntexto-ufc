#!/usr/bin/env python3
"""Real-PDF two-language precedence proof: document-language vs labels-language.

Bounded doctoral academic case, 4 primary locales x 4 display locales x
2 configuration orders. This does not certify 7 profiles or human translation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "artifacts/integrated-i18n/dual-language"
LOCALES = {
    "pt": ("pt-BR", "brazilian", "Agradecimentos", "Errata"),
    "en": ("en-US", "english", "Acknowledgments", "Errata"),
    "es": ("es-ES", "spanish", "Agradecimientos", "Fe de erratas"),
    "fr": ("fr-FR", "french", "Remerciements", "Errata"),
}
ORDERS = ("document-first", "labels-first")
AUTHOR = "DUAL-I18N-AUTHOR-UNCHANGED"
TITLE = "DUAL-I18N-TITLE-UNCHANGED"


def make_source(primary: str, display: str, order: str) -> str:
    if primary not in LOCALES or display not in LOCALES or order not in ORDERS:
        raise ValueError("unsupported fixture locale or order")
    language = LOCALES[primary][0]
    setup = (rf"\ufcsetup{{document-language={primary}}}",
             rf"\ufcsetup{{labels-language={display}}}")
    if order == "labels-first":
        setup = tuple(reversed(setup))
    return "\n".join([
        rf"\DocumentMetadata{{lang={language},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\ufcsetup{",
        "  type=doctoral-thesis,",
        "  coat-of-arms=false,",
        "  cover=false,",
        "  catalog-card=false,",
        f"  title={{{TITLE}}},",
        f"  author={{{AUTHOR}}},",
        "  advisor={Synthetic Advisor},",
        "  institution={Synthetic University},",
        "  doctoral-graduate-program={Synthetic Program},",
        "  doctoral-degree-field={Synthetic Computer Science},",
        "  submission-entity={Synthetic University},",
        "  location={Fortaleza},",
        "  year={2026}",
        "}",
        *setup,
        r"\begin{document}",
        r"\typeout{DUAL-BABEL=\languagename}",
        r"\typeout{DUAL-DOCUMENT=\ufcDocumentLanguage}",
        r"\pretextual",
        r"\ufcPrintTitlePage",
        r"\ufcPrintAcknowledgments{tests/fixtures/frontmatter/acknowledgments.tex}",
        r"\ufcPrintErrata{tests/fixtures/frontmatter/errata.tex}",
        r"\textual",
        r"\section{DUAL-I18N-CONTENT-UNCHANGED}",
        "DUAL-I18N-BODY-UNCHANGED.",
        r"\end{document}",
        "",
    ])


def source_predicate(text: str, primary: str, display: str, order: str) -> None:
    expected = make_source(primary, display, order)
    if text != expected:
        raise ValueError(f"fixture source differs from public setup: {primary}/{display}/{order}")
    if text.count(r"\ufcPrintAcknowledgments") != 1 or text.count(r"\ufcPrintTitlePage") != 1:
        raise ValueError("required actual PDF display route missing")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKD", text)
                  .encode("ascii", "ignore").decode("ascii").casefold()).strip()


def has_heading(text: str, phrase: str) -> bool:
    value = normalized(text)
    name = normalized(phrase)
    return re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", value) is not None


def read_catalog_language(data: dict) -> str:
    qpdf = data.get("qpdf")
    if not isinstance(qpdf, list) or len(qpdf) != 2 or qpdf[0].get("jsonversion") != 2:
        raise ValueError("qpdf catalog schema changed")
    objects = qpdf[1]
    root = objects["trailer"]["value"]["/Root"]
    if not isinstance(root, str) or not re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root):
        raise ValueError("bad PDF /Root reference")
    catalog = objects[f"obj:{root}"]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("PDF /Root is not a catalog")
    lang = catalog.get("/Lang")
    if not isinstance(lang, str) or not lang.startswith("u:"):
        raise ValueError("PDF catalog language missing")
    return lang[2:]


def output_predicate(primary: str, display: str, log: str,
                     text: str, catalog_language: str) -> None:
    bcp, babel, _, _ = LOCALES[primary]
    _, _, ack, errata = LOCALES[display]
    lines = log.splitlines()
    if lines.count(f"DUAL-BABEL={babel}") != 1:
        raise ValueError(f"wrong Babel main language for {primary}/{display}")
    if lines.count(f"DUAL-DOCUMENT={primary}") != 1:
        raise ValueError(f"public document-language getter differs: {primary}/{display}")
    if catalog_language != bcp:
        raise ValueError(f"PDF /Root/Lang differs: {primary}/{display}")
    if not has_heading(text, ack) or not has_heading(text, errata):
        raise ValueError(f"wrong actual localized PDF frontmatter: {primary}/{display}")
    for invariant in (AUTHOR, TITLE, "DUAL-I18N-CONTENT-UNCHANGED",
                      "DUAL-I18N-BODY-UNCHANGED"):
        if not has_heading(text, invariant):
            raise ValueError(f"authored content changed or missing: {invariant}")
    # No heading from any other display language may leak into the PDF.
    for locale, (_, _, other, _) in LOCALES.items():
        if locale != display and has_heading(text, other):
            raise ValueError(f"unexpected {locale} acknowledgment heading in {display} PDF")


def negative_controls() -> int:
    source = make_source("en", "fr", "document-first")
    source_predicate(source, "en", "fr", "document-first")
    mutants = [
        source.replace("document-language=en", "document-language=es", 1),
        source.replace("labels-language=fr", "labels-language=pt", 1),
        source.replace(r"\ufcPrintTitlePage", "", 1),
        source.replace(r"\ufcPrintAcknowledgments", "", 1),
        source.replace(AUTHOR, "TRANSLATED-AUTHOR", 1),
    ]
    count = 0
    for bad in mutants:
        if bad == source:
            raise ValueError("ineffective source negative control")
        try:
            source_predicate(bad, "en", "fr", "document-first")
        except ValueError:
            count += 1
        else:
            raise ValueError("source negative control was accepted")
    good_log = "DUAL-BABEL=english\nDUAL-DOCUMENT=en\n"
    good_text = f"{TITLE}\n{AUTHOR}\nRemerciements\nErrata\nDUAL-I18N-CONTENT-UNCHANGED\nDUAL-I18N-BODY-UNCHANGED"
    output_predicate("en", "fr", good_log, good_text, "en-US")
    bad_outputs = [
        ("en", "fr", good_log.replace("english", "french"), good_text, "en-US"),
        ("en", "fr", good_log.replace("DOCUMENT=en", "DOCUMENT=pt"), good_text, "en-US"),
        ("en", "fr", good_log, good_text, "fr-FR"),
        ("en", "fr", good_log, good_text.replace("Remerciements", "Acknowledgments"), "en-US"),
        ("en", "fr", good_log, good_text.replace(AUTHOR, "ALTERED-AUTHOR"), "en-US"),
        ("en", "fr", good_log, good_text + "\nAcknowledgments", "en-US"),
        ("en", "fr", good_log, good_text.replace("Errata", ""), "en-US"),
    ]
    for args in bad_outputs:
        try:
            output_predicate(*args)
        except ValueError:
            count += 1
        else:
            raise ValueError("PDF/log mutation was accepted")
    fake = {"qpdf": [{"jsonversion": 2}, {
        "trailer": {"value": {"/Root": "1 0 R"}},
        "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:en-US"}}
    }]}
    if read_catalog_language(fake) != "en-US":
        raise ValueError("positive PDF catalog test failed")
    fake["qpdf"][1]["obj:1 0 R"]["value"].pop("/Lang")
    try:
        read_catalog_language(fake)
    except ValueError:
        count += 1
    else:
        raise ValueError("missing PDF catalog language accepted")
    if count != 13:
        raise ValueError(f"negative control count changed: {count}")
    return count


def run(args: list[str], log_path: Path | None = None) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if log_path:
        log_path.write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        raise ValueError(f"command failed {args}: {result.stdout[-600:]} {result.stderr[-600:]}")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    negatives = negative_controls()
    cases = [(p, d, order) for p in LOCALES for d in LOCALES for order in ORDERS]
    if len(cases) != 32:
        raise ValueError("not all locale cross-products generated")
    if args.preflight:
        for primary, display, order in cases:
            source_predicate(make_source(primary, display, order), primary, display, order)
        print(f"DUAL-LANGUAGE-PREFLIGHT status=PASS cases=32 locales=4"
              f" orders=2 negative_controls={negatives}")
        return
    source_sha = run(["git", "rev-parse", "HEAD"]).strip()
    expected = os.getenv("SOURCE_COMMIT_SHA")
    if expected and expected != source_sha:
        raise ValueError("actual source checkout differs from requested CI SHA")
    OUT.mkdir(parents=True, exist_ok=True)
    receipts = []
    for primary, display, order in cases:
        name = f"dual-{primary}-{display}-{order}"
        tex = OUT / f"{name}.tex"
        pdf = OUT / f"{name}.pdf"
        source = make_source(primary, display, order)
        source_predicate(source, primary, display, order)
        tex.write_text(source, encoding="utf-8")
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-jobname={name}", f"-output-directory={OUT}",
             str(tex)], OUT / f"{name}.stdout")
        if not pdf.is_file() or pdf.stat().st_size == 0:
            raise ValueError(f"PDF was not produced: {name}")
        run(["qpdf", "--check", str(pdf)])
        catalog = read_catalog_language(json.loads(run(
            ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)])))
        extracted = run(["pdftotext", "-layout", str(pdf), "-"])
        pdf_log = (OUT / f"{name}.log").read_text(encoding="utf-8", errors="replace")
        output_predicate(primary, display, pdf_log, extracted, catalog)
        receipts.append({
            "name": name, "profile": "doctoral-thesis",
            "primary": primary, "labels": display, "order": order,
            "babel": LOCALES[primary][1], "catalog_language": catalog,
            "headings": list(LOCALES[display][2:]),
            "author_preserved": True,
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "scope": "actual PDF labels/primary-language precedence; human review pending",
        })
        print(f"DUAL-LANGUAGE status=PASS primary={primary} labels={display}"
              f" order={order} catalog={catalog}", flush=True)
    if len(receipts) != 32 or len({
        (x["primary"], x["labels"], x["order"]) for x in receipts}) != 32:
        raise ValueError("incomplete / duplicate dual-language actual-PDF proof")
    (OUT / "manifest.json").write_text(json.dumps({
        "source_sha": source_sha,
        "result": "AUTOMATED_BOUNDED_PDF_PASS",
        "profiles": ["doctoral-thesis"],
        "locales": list(LOCALES),
        "pdf_count": len(receipts),
        "negative_controls": negatives,
        "full_internationalization": "PENDING",
        "human_visual_linguistic_review": "PENDING",
        "receipts": receipts,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"DUAL-LANGUAGE status=PASS real_pdfs=32 locales=4"
          f" config_orders=2 negative_controls={negatives}"
          " qpdf_catalog=PASS headings=PASS author=PASS babel=PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"DUAL-LANGUAGE status=FAIL reason={error}") from error

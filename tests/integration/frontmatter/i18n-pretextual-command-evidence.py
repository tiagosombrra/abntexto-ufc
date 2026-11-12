#!/usr/bin/env python3
"""Verify catalog-card, dedication and short/long epigraph commands in real PDFs.

The command-specific proof is bounded to isolated undergraduate fixtures.
Production LaTeX, official translations and normative approval stay unchanged.
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
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
LOCALES = {
    "pt": ("pt-BR", "brazilian"),
    "en": ("en-US", "english"),
    "es": ("es-ES", "spanish"),
    "fr": ("fr-FR", "french"),
}
CASES = ("catalog", "dedication", "epigraph-short", "epigraph-long")
TOKENS = {
    "catalog": "CATALOGPROBETEXT",
    "dedication": "DEDICATIONPROBETEXT",
    "epigraph-short": "EPIGRAPHSHORTTEXT",
    "epigraph-long": "EPIGRAPHLONGTEXT",
}
TITLE = "SYNTHETICFRONTMATTERTITLE"
AUTHOR = "SYNTHETICFRONTMATTERAUTHOR"
BODY = "POSTBODYMARKER"
EPIGRAPH_AUTHOR = "EPIGRAPHAUTHOR"


def output_folder(locale: str) -> Path:
    return ROOT / "artifacts/integrated-i18n" / locale / "pretextual-commands"


def input_name(locale: str, case: str) -> Path:
    if locale not in LOCALES or case not in CASES:
        raise ValueError("invalid locale or pretextual case")
    return output_folder(locale) / f"input-{locale}-{case}.tex"


def catalog_base(locale: str) -> Path:
    return output_folder(locale) / f"catalog-support-{locale}"


def make_source(locale: str, case: str) -> str:
    if locale not in LOCALES or case not in CASES:
        raise ValueError("invalid locale/case")
    bcp, _ = LOCALES[locale]
    setup = ",".join((
        "type=undergraduate-capstone", f"document-language={locale}",
        "print-mode=single-sided", "cover=false", "coat-of-arms=false",
        f"catalog-card={'true' if case == 'catalog' else 'false'}",
        f"author={{{AUTHOR}}}", f"title={{{TITLE}}}",
        f"epigraph-author={{{EPIGRAPH_AUTHOR}}}",
    ))
    if case == "catalog":
        command = rf"\ufcPrintCatalogCard{{{catalog_base(locale).relative_to(ROOT).as_posix()}}}"
    elif case == "dedication":
        command = rf"\ufcPrintDedication{{{input_name(locale, case).relative_to(ROOT).as_posix()}}}"
    else:
        mode = case.split("-", 1)[1]
        command = rf"\ufcPrintEpigraph[{mode}]{{{input_name(locale, case).relative_to(ROOT).as_posix()}}}"
    return "\n".join((
        rf"\DocumentMetadata{{lang={bcp},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{{setup}}}",
        r"\begin{document}",
        r"\ufcPrintTitlePage",
        command,
        r"\textual",
        rf"\noindent {BODY}\par",
        r"\typeout{PRETEXT-BABEL=\languagename}",
        r"\typeout{PRETEXT-LANGUAGE=\ufcDocumentLanguage}",
        rf"\typeout{{PRETEXT-CASE={case}}}",
        r"\end{document}",
        "",
    ))


def catalog_support_source() -> str:
    return "\n".join((
        r"\documentclass[a4paper]{article}",
        r"\pagestyle{empty}",
        r"\begin{document}",
        r"\vspace*{7cm}",
        r"\begin{center}\bfseries CATALOGPROBETEXT\end{center}",
        r"\end{document}",
        "",
    ))


def validate_source(source: str, locale: str, case: str) -> None:
    if source != make_source(locale, case):
        raise ValueError("public pretextual command fixture was altered")
    command_names = (
        r"\ufcPrintCatalogCard{", r"\ufcPrintDedication{",
        r"\ufcPrintEpigraph[",
    )
    for item in command_names:
        expected = int(
            (case == "catalog" and item == command_names[0])
            or (case == "dedication" and item == command_names[1])
            or (case.startswith("epigraph-") and item == command_names[2]))
        if source.count(item) != expected:
            raise ValueError("foreign or duplicated pretextual command")


def catalog_language(data: dict) -> str:
    blocks = data.get("qpdf")
    if not isinstance(blocks, list) or len(blocks) != 2:
        raise ValueError("unknown qpdf JSON schema")
    if blocks[0].get("jsonversion") != 2:
        raise ValueError("wrong qpdf JSON version")
    root = blocks[1]["trailer"]["value"]["/Root"]
    if not isinstance(root, str) or not re.fullmatch(r"[1-9]\d* \d+ R", root):
        raise ValueError("invalid PDF root")
    catalog = blocks[1]["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("PDF root is not a catalog")
    lang = catalog.get("/Lang")
    if not isinstance(lang, str) or not lang.startswith("u:"):
        raise ValueError("PDF /Root/Lang absent")
    return lang[2:]


def marker_word_equals(pdf_word: str, token: str) -> bool:
    # Poppler can attach an opening quote to the first epigraph word.
    # Strip only typographic quote punctuation at word boundaries.
    return pdf_word.strip().strip("\\"'“”„‟«»‹›‘’") == token


def locate_marker_bbox(bbox_xml: str, token: str) -> tuple[int, float, float]:
    pages = list(ET.fromstring(bbox_xml).iter())
    actual_pages = [p for p in pages if p.tag.rsplit("}", 1)[-1] == "page"]
    found = []
    for page_index, page in enumerate(actual_pages):
        height = float(page.attrib["height"])
        for word in page.iter():
            if word.tag.rsplit("}", 1)[-1] != "word":
                continue
            if marker_word_equals("".join(word.itertext()), token):
                found.append((page_index, float(word.attrib["yMin"]), height))
    if len(found) != 1:
        raise ValueError("expected exactly one marker with PDF bounding box")
    return found[0]


def validate_output(locale: str, case: str, log: str, pages: list[str],
                    lang: str, position: tuple[int, float, float]) -> None:
    if locale not in LOCALES or case not in CASES:
        raise ValueError("invalid output coordinates")
    bcp, babel = LOCALES[locale]
    if lang != bcp:
        raise ValueError("catalog language mismatch")
    receipts = (
        f"PRETEXT-BABEL={babel}",
        f"PRETEXT-LANGUAGE={locale}",
        f"PRETEXT-CASE={case}",
    )
    for receipt in receipts:
        if log.splitlines().count(receipt) != 1:
            raise ValueError("missing or duplicated TeX locale/case receipt")
    if len(pages) < 2 or TITLE not in "".join(pages[:1]):
        raise ValueError("physical title page missing")
    token = TOKENS[case]
    hit = [i for i, text in enumerate(pages) if token in text]
    if len(hit) != 1 or pages[hit[0]].count(token) != 1:
        raise ValueError("command-specific marker absent or duplicated")
    if hit[0] == 0 or BODY not in "".join(pages[hit[0] + 1:]):
        raise ValueError("command content not placed between frontmatter and body")
    for other, forbidden in TOKENS.items():
        if other != case and forbidden in "".join(pages):
            raise ValueError("another pretextual command leaked into PDF")
    page, ymin, page_height = position
    if page != hit[0] or not 0 <= ymin < page_height:
        raise ValueError("PDF visual marker does not match extracted page")
    if case != "catalog" and ymin < page_height * 0.48:
        raise ValueError("dedication/epigraph content is above physical midpoint")
    if case.startswith("epigraph-") and pages[hit[0]].count(EPIGRAPH_AUTHOR) != 1:
        raise ValueError("epigraph author absent or duplicated")
    if case != "catalog" and "CATALOGPROBETEXT" in "".join(pages):
        raise ValueError("catalog page leaked into non-catalog scenario")


def negative_controls() -> int:
    locale, case = "en", "dedication"
    source = make_source(locale, case)
    validate_source(source, locale, case)
    alterations = (
        source.replace("document-language=en", "document-language=fr"),
        source.replace(r"\ufcPrintDedication{", r"\ufcPrintEpigraph[short]{"),
        source.replace("catalog-card=false", "catalog-card=true"),
        source.replace(r"\ufcPrintTitlePage", ""),
        source.replace(r"\ufcPrintDedication{", r"\ufcPrintDedication{}\ufcPrintDedication{"),
    )
    count = 0
    for bad in alterations:
        try:
            validate_source(bad, locale, case)
        except ValueError:
            count += 1
        else:
            raise ValueError("altered pretextual source accepted")
    good_log = "\n".join((
        "PRETEXT-BABEL=english", "PRETEXT-LANGUAGE=en",
        "PRETEXT-CASE=dedication",
    ))
    good_pages = [TITLE, TOKENS[case], BODY]
    good_position = (1, 620.0, 842.0)
    validate_output(locale, case, good_log, good_pages, "en-US", good_position)
    bad_outputs = (
        (good_log.replace("BABEL=english", "BABEL=french"), good_pages, "en-US", good_position),
        (good_log.replace("LANGUAGE=en", "LANGUAGE=fr"), good_pages, "en-US", good_position),
        (good_log.replace("CASE=dedication", "CASE=catalog"), good_pages, "en-US", good_position),
        (good_log + "\nPRETEXT-CASE=dedication", good_pages, "en-US", good_position),
        (good_log, [TITLE, "MISSING", BODY], "en-US", good_position),
        (good_log, [TITLE, TOKENS[case] * 2, BODY], "en-US", good_position),
        (good_log, [TITLE + TOKENS[case], BODY], "en-US", (0, 620.0, 842.0)),
        (good_log, [TITLE, TOKENS[case] + TOKENS["catalog"], BODY], "en-US", good_position),
        (good_log, good_pages, "pt-BR", good_position),
        (good_log, good_pages, "en-US", (1, 200.0, 842.0)),
        (good_log, good_pages, "en-US", (0, 620.0, 842.0)),
    )
    for bad in bad_outputs:
        try:
            validate_output(locale, case, *bad)
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid PDF/log/geometry accepted")
    # A genuine quotation mark must not be mistaken for an altered token.
    if not marker_word_equals("“" + TOKENS["epigraph-short"], TOKENS["epigraph-short"]):
        raise ValueError("real epigraph quotation was rejected")
    for invalid in ("X" + TOKENS["epigraph-short"], TOKENS["epigraph-short"] + "X"):
        if marker_word_equals(invalid, TOKENS["epigraph-short"]):
            raise ValueError("alphabetic collision escaped PDF word test")
        count += 1
    if count != 18:
        raise ValueError(f"negative control count drift: {count}")
    for loc in LOCALES:
        for item in CASES:
            validate_source(make_source(loc, item), loc, item)
    if len(LOCALES) * len(CASES) != 16:
        raise ValueError("frontmatter cross-product drift")
    return count


def run(command: list[str]) -> str:
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    if proc.returncode:
        raise ValueError(f"{command[0]} exited {proc.returncode}: "
                         f"{proc.stderr[-500:]} {proc.stdout[-700:]}")
    return proc.stdout


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    negatives = negative_controls()
    if args.preflight:
        print("PRETEXT-API-PREFLIGHT status=PASS sources=16"
              f" negatives={negatives} real_pdfs=PENDING", flush=True)
        return
    if not args.locale:
        raise ValueError("locale required outside preflight")
    sha = run(["git", "rev-parse", "HEAD"]).strip()
    if os.environ.get("SOURCE_COMMIT_SHA") not in (None, sha):
        raise ValueError("current Git checkout not equal to CI source SHA")
    folder = output_folder(args.locale)
    folder.mkdir(parents=True, exist_ok=True)
    # Generate a real external catalog PDF with an isolated visible marker.
    helper = catalog_base(args.locale)
    helper_tex = helper.with_suffix(".tex")
    helper_tex.write_text(catalog_support_source(), encoding="utf-8")
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
         f"-jobname={helper.name}", f"-output-directory={folder}", str(helper_tex)])
    if not helper.with_suffix(".pdf").is_file():
        raise ValueError("real catalog support PDF was not created")
    run(["qpdf", "--check", str(helper.with_suffix(".pdf"))])
    receipts = []
    for case in CASES:
        token = TOKENS[case]
        inp = input_name(args.locale, case)
        inp.write_text(token + "\n", encoding="utf-8")
        name = f"pretext-{args.locale}-{case}"
        tex, pdf, log = (folder / f"{name}.{ext}" for ext in ("tex", "pdf", "log"))
        source = make_source(args.locale, case)
        validate_source(source, args.locale, case)
        tex.write_text(source, encoding="utf-8")
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-jobname={name}",
             f"-output-directory={folder}", str(tex)])
        if not pdf.is_file() or pdf.stat().st_size <= 0:
            raise ValueError("missing or empty command PDF")
        run(["qpdf", "--check", str(pdf)])
        lang = catalog_language(json.loads(run(
            ["qpdf", "--json=2", "--json-key=qpdf", str(pdf)])))
        info = run(["pdfinfo", str(pdf)])
        count = re.search(r"^Pages:\s*(\d+)", info, re.M)
        if not count:
            raise ValueError("pdfinfo omitted physical page count")
        pages = [run(["pdftotext", "-f", str(i), "-l", str(i),
                       "-layout", str(pdf), "-"])
                 for i in range(1, int(count.group(1)) + 1)]
        bbox = run(["pdftotext", "-bbox-layout", str(pdf), "-"])
        pos = locate_marker_bbox(bbox, token)
        log_bytes = log.read_bytes()
        validate_output(args.locale, case, log_bytes.decode(
            "utf-8", errors="replace"), pages, lang, pos)
        receipts.append({
            "case": case, "command": {
                "catalog": r"\ufcPrintCatalogCard",
                "dedication": r"\ufcPrintDedication",
                "epigraph-short": r"\ufcPrintEpigraph",
                "epigraph-long": r"\ufcPrintEpigraph",
            }[case],
            "locale": args.locale, "job": name, "verified": True,
            "pdf_pages": len(pages), "marker_page": pos[0] + 1,
            "marker_ymin": pos[1], "page_height": pos[2],
            "catalog_lang": lang,
            "tex_sha256": checksum(tex),
            "pdf_sha256": checksum(pdf),
            "log_sha256": hashlib.sha256(log_bytes).hexdigest(),
            "input_sha256": checksum(inp),
            "catalog_support_pdf_sha256": checksum(helper.with_suffix(".pdf"))
            if case == "catalog" else None,
            "human_normative_linguistic_review": "PENDING",
        })
        print(f"PRETEXT-API status=PASS locale={args.locale}"
              f" case={case} pages={len(pages)}", flush=True)
    if len(receipts) != 4 or len({r["case"] for r in receipts}) != 4:
        raise ValueError("missing/duplicate case receipts")
    report = {
        "source_sha": sha, "locale": args.locale,
        "status": "BOUNDED_REAL_PDF_PASS", "real_pdfs": len(receipts),
        "negative_controls": negatives,
        "sha256_scope": "raw_original_file_bytes",
        "proof_boundary": "catalog-card file import and dedicated/epigraph short/long input in academic profile",
        "global_i18n_acceptance": "PENDING",
        "human_normative_linguistic_review": "PENDING",
        "records": receipts,
    }
    (folder / "manifest.json").write_text(json.dumps(
        report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PRETEXT-API status=PASS locale={args.locale}"
          f" real_pdfs=4 negatives={negatives} human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError, ET.ParseError) as exc:
        raise SystemExit(f"PRETEXT-API status=FAIL reason={exc}") from exc

#!/usr/bin/env python3
"""Certify three bounded pretextual APIs from real PT/EN/ES/FR PDFs.

The synthetic external catalog card is not an institution-approved catalog
record. These checks do not imply official translations or human PDF approval.
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
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "artifacts/i18n-pretextual"
LOCALES = {
    "pt": ("pt-BR", "brazilian"),
    "en": ("en-US", "english"),
    "es": ("es-ES", "spanish"),
    "fr": ("fr-FR", "french"),
}
CASES = ("single-enabled", "double-enabled", "single-disabled", "double-disabled")
APIS = (r"\ufcPrintCatalogCard", r"\ufcPrintDedication", r"\ufcPrintEpigraph")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(locale: str) -> dict[str, str]:
    suffix = locale.upper() + "AA"
    return {key: key + suffix for key in ("CARD", "DED", "EPS", "EPL", "BODY")}


def execute(args: list[str], logfile: Path) -> None:
    with logfile.open("w", encoding="utf-8") as out:
        proc = subprocess.run(args, cwd=ROOT, stdout=out,
                              stderr=subprocess.STDOUT, check=False)
    if proc.returncode:
        lines = logfile.read_text(encoding="utf-8", errors="replace").splitlines()
        raise ValueError(f"command failed {args[0]} rc={proc.returncode}:\n"
                         + "\n".join(lines[-35:]))


def catalog_lang(pdf: Path) -> str:
    raw = subprocess.check_output(["qpdf", "--json=2", "--json-key=qpdf",
                                   str(pdf)], cwd=ROOT, text=True)
    entries = json.loads(raw)["qpdf"]
    if len(entries) != 2 or entries[0].get("jsonversion") != 2:
        raise ValueError("unexpected qpdf JSON format")
    objects = entries[1]
    root = objects["trailer"]["value"]["/Root"]
    if not re.fullmatch(r"[1-9]\d* \d+ R", root):
        raise ValueError("invalid PDF Root")
    catalog = objects["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("invalid PDF catalog")
    value = catalog.get("/Lang")
    if not isinstance(value, str) or not value.startswith("u:"):
        raise ValueError("missing Unicode PDF catalog language")
    return value[2:]


def pages_and_geometry(pdf: Path, page_text: str) -> tuple[list[str], list[dict]]:
    pages = page_text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    xml = subprocess.check_output(["pdftotext", "-bbox-layout", str(pdf), "-"],
                                  cwd=ROOT)
    tree = ET.fromstring(xml)
    geometry = []
    for page in tree.iter():
        if page.tag.rsplit("}", 1)[-1] != "page":
            continue
        width, height = float(page.attrib["width"]), float(page.attrib["height"])
        if abs(width - 595.28) > 2 or abs(height - 841.89) > 2:
            raise ValueError("non-A4 page geometry")
        words = {}
        for node in page.iter():
            if node.tag.rsplit("}", 1)[-1] != "word":
                continue
            word = "".join(node.itertext()).strip()
            if word:
                words[word] = {"x": float(node.attrib["xMin"]),
                               "y": float(node.attrib["yMin"]),
                               "height": height}
        geometry.append(words)
    if len(pages) != len(geometry):
        raise ValueError("PDF extracted page count differs from bbox count")
    return pages, geometry


def verify_case(locale: str, case: str, tex: str, pages: list[str],
                bbox: list[dict], babel_log: str, lang: str) -> dict:
    if locale not in LOCALES or case not in CASES:
        raise ValueError("unknown locale/case")
    enabled = case.endswith("-enabled")
    duplex = case.startswith("double-")
    extra = case == "single-enabled"
    t = tokens(locale)
    expected = ["TITLE", "CARD" if enabled else "BLANK" if duplex else "BODY"]
    if enabled and extra:
        expected += ["DED", "EPS", "EPL", "BODY"]
    elif enabled or duplex:
        expected += ["BODY"]
    if len(pages) != len(expected) or len(bbox) != len(expected):
        raise ValueError(f"incorrect PDF page count for {case}: {len(pages)}")
    if tex.count(r"\ufcPrintCatalogCard{") != 1:
        raise ValueError("catalog card public API missing or duplicated in TeX")
    if ("catalog-card=true" if enabled else "catalog-card=false") not in tex:
        raise ValueError("catalog-card option does not match fixture")
    if ("print-mode=double-sided" if duplex else "print-mode=single-sided") not in tex:
        raise ValueError("wrong print mode in TeX")
    if f"document-language={locale}" not in tex:
        raise ValueError("wrong locale configured in TeX")
    if extra:
        for cmd in (r"\ufcPrintDedication{", r"\ufcPrintEpigraph[short]{",
                    r"\ufcPrintEpigraph[long]{"):
            if tex.count(cmd) != 1:
                raise ValueError("pretextual public API missing or duplicated")
    else:
        if r"\ufcPrintDedication{" in tex or r"\ufcPrintEpigraph[" in tex:
            raise ValueError("unexpected pretextual command in reduced fixture")
    if lang != LOCALES[locale][0]:
        raise ValueError("PDF /Root/Lang does not match source locale")
    if f"PRETEXTUAL-BABEL={LOCALES[locale][1]}" not in babel_log:
        raise ValueError("active Babel language is not the requested locale")
    if f"PRETEXTUAL-DOCUMENT-LANGUAGE={locale}" not in babel_log:
        raise ValueError("public document language does not match source locale")
    if "PRETEXTUAL-LOGICAL-BEFORE=2" not in babel_log or "PRETEXTUAL-LOGICAL-AFTER=2" not in babel_log:
        raise ValueError("catalog inclusion changed logical page count")

    for key in ("CARD", "DED", "EPS", "EPL", "BODY"):
        indices = [i for i, page in enumerate(pages) if t[key] in page]
        desired = [i for i, label in enumerate(expected) if label == key]
        occurrences = sum(page.count(t[key]) for page in pages)
        if indices != desired or occurrences != len(desired):
            raise ValueError(
                f"{key} printed on wrong page, missing or duplicated: "
                f"{indices} != {desired}, occurrences={occurrences}"
            )
    if not pages[0].strip() or any(t[key] in pages[0] for key in t):
        raise ValueError("missing title page or pretextual content leaked there")
    if "BLANK" in expected and pages[expected.index("BLANK")].strip():
        raise ValueError("duplex disabled card must preserve blank verso")
    for other in LOCALES:
        if other == locale:
            continue
        for word in tokens(other).values():
            if any(word in page for page in pages):
                raise ValueError("foreign-locale marker detected in PDF")
    placement = {}
    if extra:
        for key in ("DED", "EPS", "EPL"):
            p = expected.index(key)
            marker = bbox[p].get(t[key])
            if marker is None:
                raise ValueError("pretextual PDF word missing from actual bbox")
            if marker["y"] <= marker["height"] / 2:
                raise ValueError("pretextual content is above physical page midpoint")
            placement[key] = {"page": p + 1, "x": marker["x"], "y": marker["y"]}
        if placement["EPS"]["x"] < placement["EPL"]["x"] + 60:
            raise ValueError("short epigraph not more inset than long epigraph")
        if abs(placement["DED"]["x"] - placement["EPS"]["x"]) > 35:
            raise ValueError("dedication and short epigraph have inconsistent insets")
    return {"case": case, "locale": locale, "pages": len(pages),
            "layout": expected, "physical_placement": placement,
            "verified_commands": [
                r"\ufcPrintCatalogCard",
                *(list(APIS[1:]) if extra else []),
            ] if enabled else [r"\ufcPrintCatalogCard (disabled branch)"]}


def self_test() -> None:
    locale = "pt"
    marker = tokens(locale)
    cases = 0
    for case in CASES:
        enabled = case.endswith("-enabled")
        duplex = case.startswith("double-")
        extra = case == "single-enabled"
        keys = ["TITLE", "CARD" if enabled else "BLANK" if duplex else "BODY"]
        if enabled and extra:
            keys += ["DED", "EPS", "EPL", "BODY"]
        elif enabled or duplex:
            keys += ["BODY"]
        pages = ["TITLEPAGE"] + [marker[x] if x in marker else "" for x in keys[1:]]
        bbox = [{k: {"x": (360 if k.startswith(("EPS", "DED")) else 235),
                     "y": 510, "height": 842} for k in ([page] if page else [])}
                for page in pages]
        src = (r"\ufcPrintCatalogCard{card}" +
               ("catalog-card=true" if enabled else "catalog-card=false") +
               ("print-mode=double-sided" if duplex else "print-mode=single-sided") +
               "document-language=pt")
        if extra:
            src += r"\ufcPrintDedication{ded}\ufcPrintEpigraph[short]{short}\ufcPrintEpigraph[long]{long}"
        log = "PRETEXTUAL-BABEL=brazilian\nPRETEXTUAL-DOCUMENT-LANGUAGE=pt\nPRETEXTUAL-LOGICAL-BEFORE=2\nPRETEXTUAL-LOGICAL-AFTER=2"
        def test(source=src, shown=pages, boxes=bbox, info=log, catalog="pt-BR"):
            return verify_case(locale, case, source, shown, boxes, info, catalog)
        test()
        mutations = [
            lambda: test(source=src.replace(r"\ufcPrintCatalogCard{", r"\relax{")),
            lambda: test(source=src.replace("document-language=pt", "document-language=en")),
            lambda: test(shown=pages + ["EXTRA"]),
            lambda: test(shown=[p.replace(marker["BODY"], "") for p in pages]),
            lambda: test(shown=[p + marker["BODY"] if marker["BODY"] in p else p for p in pages]),
            lambda: test(info=log.replace("PRETEXTUAL-BABEL=brazilian", "PRETEXTUAL-BABEL=english")),
            lambda: test(catalog="en-US"),
            lambda: test(shown=[p + "CARDENAA" for p in pages]),
        ]
        if enabled:
            mutations.append(lambda: test(shown=[p.replace(marker["CARD"], "") for p in pages]))
        if extra:
            mutations += [
                lambda: test(source=src.replace(r"\ufcPrintDedication{", r"\relax{")),
                lambda: test(source=src.replace(r"\ufcPrintEpigraph[short]{", r"\relax{")),
                lambda: test(source=src.replace(r"\ufcPrintEpigraph[long]{", r"\relax{")),
                lambda: test(shown=[p + marker["DED"] if marker["DED"] in p else p for p in pages]),
                lambda: test(shown=[p.replace(marker["DED"], "") for p in pages]),
                lambda: test(boxes=[{k: {**v, "y": 100} if k == marker["EPS"] else v
                                     for k, v in d.items()} for d in bbox]),
                lambda: test(boxes=[{k: {**v, "x": 230} if k == marker["EPS"] else v
                                     for k, v in d.items()} for d in bbox]),
            ]
        for mutate in mutations:
            try:
                mutate()
            except ValueError:
                cases += 1
            else:
                raise ValueError(f"negative mutant incorrectly accepted: {case}")
    print(f"I18N-PRETEXTUAL-API-SELFTEST status=PASS mutants_rejected={cases}")


def card_tex(locale: str) -> str:
    t = tokens(locale)
    return (r"\documentclass{article}" "\n"
            r"\usepackage[paperwidth=210mm,paperheight=297mm,margin=2cm]{geometry}" "\n"
            r"\pagestyle{empty}\begin{document}\vfill\begin{center}" + "\n"
            + t["CARD"] + "\n"
            r"\end{center}\vfill\end{document}" "\n")


def manuscript(locale: str, case: str, folder: Path) -> str:
    t = tokens(locale)
    enabled = case.endswith("-enabled")
    duplex = case.startswith("double-")
    extra = case == "single-enabled"
    lines = [
        rf"\DocumentMetadata{{lang={LOCALES[locale][0]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\ufcsetup{",
        "type=undergraduate-capstone,",
        f"document-language={locale},",
        f"print-mode={'double-sided' if duplex else 'single-sided'},",
        f"catalog-card={'true' if enabled else 'false'},",
        "coat-of-arms=false,",
        "author={Synthetic Author},title={Synthetic Pretextual Audit},",
        "location={Fortaleza},year={2026},advisor={Synthetic Advisor},",
        "undergraduate-program={Computing},undergraduate-degree={Bachelor}",
        "}",
        r"\begin{document}",
        r"\pretextual",
        r"\ufcPrintTitlePage",
        r"\typeout{PRETEXTUAL-LOGICAL-BEFORE=\thepage}",
        rf"\ufcPrintCatalogCard{{{(folder / 'external-card').relative_to(ROOT).as_posix()}}}",
        r"\typeout{PRETEXTUAL-LOGICAL-AFTER=\thepage}",
    ]
    if extra:
        lines += [
            rf"\ufcPrintDedication{{{(folder / 'dedication').relative_to(ROOT).as_posix()}}}",
            rf"\ufcPrintEpigraph[short]{{{(folder / 'epigraph-short').relative_to(ROOT).as_posix()}}}",
            rf"\ufcPrintEpigraph[long]{{{(folder / 'epigraph-long').relative_to(ROOT).as_posix()}}}",
        ]
    lines += [
        r"\typeout{PRETEXTUAL-BABEL=\languagename}",
        r"\typeout{PRETEXTUAL-DOCUMENT-LANGUAGE=\ufcDocumentLanguage}",
        r"\textual",
        r"\section{Synthetic text}",
        t["BODY"],
        r"\end{document}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=tuple(LOCALES))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test:
        return
    if args.locale is None:
        raise ValueError("either --locale or --self-test must be supplied")
    locale = args.locale
    current = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                      cwd=ROOT, text=True).strip()
    source_sha = os.environ.get("SOURCE_COMMIT_SHA", current)
    if not re.fullmatch("[0-9a-f]{40}", source_sha) or current != source_sha:
        raise ValueError("source SHA is not the exact checked out commit")
    folder = OUTPUT / locale
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "external-card.tex").write_text(card_tex(locale), encoding="utf-8")
    t = tokens(locale)
    for name, key in (("dedication", "DED"), ("epigraph-short", "EPS"),
                      ("epigraph-long", "EPL")):
        (folder / (name + ".tex")).write_text(t[key] + "\n", encoding="utf-8")
    execute(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-output-directory", str(folder),
             str(folder / "external-card.tex")], folder / "card-build.log")
    card = folder / "external-card.pdf"
    if not card.is_file():
        raise ValueError("external synthetic catalog-card PDF not produced")
    result = []
    for case in CASES:
        job = "pretextual-" + case + "-" + locale
        tex = folder / (job + ".tex")
        tex.write_text(manuscript(locale, case, folder), encoding="utf-8")
        log = folder / (job + "-stdout.log")
        for _ in range(2):
            execute(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                     "-file-line-error", "-jobname", job,
                     "-output-directory", str(folder), str(tex)], log)
        pdf = folder / (job + ".pdf")
        text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"],
                                       cwd=ROOT, text=True)
        pages, bbox = pages_and_geometry(pdf, text)
        logtext = log.read_text(encoding="utf-8", errors="replace")
        lang = catalog_lang(pdf)
        receipt = verify_case(locale, case, tex.read_text(encoding="utf-8"),
                              pages, bbox, logtext, lang)
        receipt.update({
            "source_sha": source_sha, "pdf": pdf.relative_to(ROOT).as_posix(),
            "pdf_sha256": digest(pdf), "source_sha256": digest(tex),
            "log_sha256": digest(log),
            "tex_engine_log_sha256": digest(folder / (job + ".log")),
            "external_card_sha256": digest(card),
            "external_card_source_sha256": digest(folder / "external-card.tex"),
            "bbox_a4": True, "pdf_catalog_lang": lang,
            "babel": LOCALES[locale][1],
        })
        if case == "single-enabled":
            receipt["support_source_sha256"] = {
                name: digest(folder / (name + ".tex"))
                for name in ("dedication", "epigraph-short", "epigraph-long")
            }
        result.append(receipt)
        print(f"I18N-PRETEXTUAL-API status=PASS locale={locale} case={case}"
              f" pages={len(pages)} real_pdf=true source_sha={source_sha}", flush=True)
    if len(result) != 4 or len({r["pdf_sha256"] for r in result}) != 4:
        raise ValueError("incomplete or duplicate real-PDF evidence")
    manifest = {
        "status": "BOUNDED_FUNCTIONAL_REAL_PDF_PASS", "source_sha": source_sha,
        "locale": locale, "real_pdfs": 4,
        "public_apis": list(APIS),
        "scope": "one academic profile; catalog enabled/disabled and simplex/duplex; "
                 "dedication and epigraph short/long on one real simplex PDF",
        "not_exercised": "other document profiles; other pretextual and normative routes",
        "human_linguistic_visual_review": "PENDING",
        "institutional_catalog_card_approval": "NOT_CLAIMED",
        "records": result,
    }
    (folder / "pretextual-api-receipts.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"I18N-PRETEXTUAL-API status=PASS locale={locale}"
          " real_pdfs=4 api_identifiers=3 provenance=PASS"
          " human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError,
            subprocess.CalledProcessError, ET.ParseError) as exc:
        raise SystemExit(f"I18N-PRETEXTUAL-API status=FAIL reason={exc}") from exc

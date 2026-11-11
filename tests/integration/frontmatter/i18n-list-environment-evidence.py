#!/usr/bin/env python3
"""Bounded real-PDF evidence for the three core public list environments.

Every environment is isolated in one actual PDF per locale. This proves
rendering and source/runtime linkage, not linguistic or normative approval.
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
    "pt": ("pt-BR", "brazilian"),
    "en": ("en-US", "english"),
    "es": ("es-ES", "spanish"),
    "fr": ("fr-FR", "french"),
}
ENVIRONMENTS = ("ufclettereditems", "ufcdashedsubitems", "ufcdefinitionlist")
CONTENTS = {
    "ufclettereditems": (
        r"\begin{ufclettereditems}",
        r"\item LISTLETTEREDA",
        r"\item LISTLETTEREDB",
        r"\end{ufclettereditems}",
    ),
    "ufcdashedsubitems": (
        r"\begin{ufcdashedsubitems}",
        r"\item LISTDASHEDA",
        r"\item LISTDASHEDB",
        r"\end{ufcdashedsubitems}",
    ),
    "ufcdefinitionlist": (
        r"\begin{ufcdefinitionlist}",
        r"\ufcListEntry{LISTKEYA}{LISTDEFINITIONVALUEA}",
        r"\ufcListEntry{LISTKEYB}{LISTDEFINITIONVALUEB}",
        r"\end{ufcdefinitionlist}",
    ),
}
MARKERS = {
    "ufclettereditems": ("LISTLETTEREDA", "LISTLETTEREDB"),
    "ufcdashedsubitems": ("LISTDASHEDA", "LISTDASHEDB"),
    "ufcdefinitionlist": (
        "LISTKEYA", "LISTDEFINITIONVALUEA",
        "LISTKEYB", "LISTDEFINITIONVALUEB",
    ),
}


def make_source(locale: str, environment: str) -> str:
    if locale not in LOCALES or environment not in ENVIRONMENTS:
        raise ValueError("unsupported locale or list environment")
    bcp = LOCALES[locale][0]
    return "\n".join([
        rf"\DocumentMetadata{{lang={bcp},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\ufcsetup{",
        "  type=undergraduate-capstone,",
        f"  document-language={locale},",
        "  coat-of-arms=false,",
        "  cover=false,",
        "  catalog-card=false,",
        "  author={SYNTHETIC LIST AUTHOR},",
        "  title={SYNTHETIC LIST DOCUMENT}",
        "}",
        r"\begin{document}",
        r"\textual",
        *CONTENTS[environment],
        r"\typeout{LIST-ENV-BABEL=\languagename}",
        r"\typeout{LIST-ENV-LANGUAGE=\ufcDocumentLanguage}",
        r"\end{document}",
        "",
    ])


def validate_source(source: str, locale: str, environment: str) -> None:
    if source != make_source(locale, environment):
        raise ValueError("source fixture differs from required public environment")
    for name in ENVIRONMENTS:
        expected = 1 if name == environment else 0
        if source.count(r"\begin{" + name + "}") != expected:
            raise ValueError("source contains wrong environment or duplicate")
        if source.count(r"\end{" + name + "}") != expected:
            raise ValueError("source environment missing a matching end")


def fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(x for x in normalized if not unicodedata.combining(x))
    return re.sub(r"\s+", " ", normalized).casefold()


def extract_catalog_language(payload: dict) -> str:
    blocks = payload.get("qpdf")
    if (not isinstance(blocks, list) or len(blocks) != 2
            or blocks[0].get("jsonversion") != 2):
        raise ValueError("unexpected qpdf schema")
    objects = blocks[1]
    root = objects["trailer"]["value"]["/Root"]
    if not isinstance(root, str) or not re.fullmatch(r"[1-9]\d* \d+ R", root):
        raise ValueError("invalid PDF catalog reference")
    catalog = objects["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("PDF root is not a catalog")
    lang = catalog.get("/Lang")
    if not isinstance(lang, str) or not lang.startswith("u:"):
        raise ValueError("PDF catalog language not set")
    return lang[2:]


def validate_output(locale: str, environment: str, log: str,
                    pdf_text: str, catalog_lang: str) -> None:
    if locale not in LOCALES or environment not in ENVIRONMENTS:
        raise ValueError("unsupported evidence coordinates")
    bcp, babel = LOCALES[locale]
    if catalog_lang != bcp:
        raise ValueError("wrong PDF /Root/Lang")
    lines = log.splitlines()
    for receipt in (f"LIST-ENV-BABEL={babel}", f"LIST-ENV-LANGUAGE={locale}"):
        if lines.count(receipt) != 1:
            raise ValueError("missing or duplicate locale log receipt")
    value = fold(pdf_text)
    markers = MARKERS[environment]
    found = [value.find(fold(marker)) for marker in markers]
    if any(p < 0 for p in found) or found != sorted(found):
        raise ValueError("missing or out-of-order public list PDF content")
    for other, others in MARKERS.items():
        if other != environment and any(fold(marker) in value for marker in others):
            raise ValueError("content from another list environment leaked")
    if environment in ("ufclettereditems", "ufcdashedsubitems"):
        for index, token in enumerate(markers):
            rows = [row for row in pdf_text.splitlines() if token in row]
            if len(rows) != 1:
                raise ValueError("item missing or duplicated in extracted PDF")
            prefix = rows[0].split(token, 1)[0].strip()
            if environment == "ufclettereditems":
                expected_label = ("a)", "b)")[index]
                if not prefix.endswith(expected_label):
                    raise ValueError("ABNT lettered item label missing")
            elif not re.search(r"(?:-{1,3}|[—–−])\s*$", prefix):
                raise ValueError("ABNT dashed subitem label missing")
    else:
        if len(markers) != 4:
            raise ValueError("invalid definition list contract")
        for label, definition in ((markers[0], markers[1]),
                                  (markers[2], markers[3])):
            rows = [line for line in pdf_text.splitlines()
                    if label in line or definition in line]
            if len(rows) != 1 or label not in rows[0] or definition not in rows[0]:
                raise ValueError("definition label and body must share one baseline")
            separation = rows[0].index(definition) - (
                rows[0].index(label) + len(label))
            if separation < 2:
                raise ValueError("definition list label and body have no safe gap")


def negative_controls() -> int:
    locale, env = "en", "ufclettereditems"
    source = make_source(locale, env)
    validate_source(source, locale, env)
    candidates = (
        source.replace(r"\begin{ufclettereditems}", "", 1),
        source.replace(r"\end{ufclettereditems}", "", 1),
        source.replace("LISTLETTEREDB", "ALTEREDITEM", 1),
        source.replace("document-language=en", "document-language=es", 1),
    )
    count = 0
    for bad in candidates:
        try:
            validate_source(bad, locale, env)
        except ValueError:
            count += 1
        else:
            raise ValueError("source mutation was accepted")
    good_log = "LIST-ENV-BABEL=english\nLIST-ENV-LANGUAGE=en"
    good_text = "a) LISTLETTEREDA\nb) LISTLETTEREDB"
    validate_output(locale, env, good_log, good_text, "en-US")
    output_bad = (
        (good_log.replace("BABEL=english", "BABEL=french"), good_text, "en-US"),
        (good_log.replace("LANGUAGE=en", "LANGUAGE=pt"), good_text, "en-US"),
        (good_log + "\nLIST-ENV-LANGUAGE=en", good_text, "en-US"),
        (good_log, good_text.replace("a)", "-"), "en-US"),
        (good_log, good_text.replace("LISTLETTEREDB", "MISSING"), "en-US"),
        (good_log, good_text + "\nLISTDASHEDA", "en-US"),
        (good_log, "b) LISTLETTEREDB\na) LISTLETTEREDA", "en-US"),
        (good_log, good_text, "fr-FR"),
    )
    for bad in output_bad:
        try:
            validate_output(locale, env, *bad)
        except ValueError:
            count += 1
        else:
            raise ValueError("PDF/log mutation was accepted")
    definition_good = "LISTKEYA   LISTDEFINITIONVALUEA\nLISTKEYB   LISTDEFINITIONVALUEB"
    validate_output(locale, "ufcdefinitionlist", good_log, definition_good, "en-US")
    definition_bad = (
        definition_good.replace("LISTKEYA   LISTDEFINITIONVALUEA",
                                "LISTKEYA\nLISTDEFINITIONVALUEA"),
        definition_good.replace("LISTKEYA   LISTDEFINITIONVALUEA",
                                "LISTKEYALISTDEFINITIONVALUEA"),
    )
    for damaged in definition_bad:
        try:
            validate_output(locale, "ufcdefinitionlist", good_log, damaged, "en-US")
        except ValueError:
            count += 1
        else:
            raise ValueError("definition list alignment mutation was accepted")
    sample = {"qpdf": [{"jsonversion": 2}, {
        "trailer": {"value": {"/Root": "1 0 R"}},
        "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:en-US"}},
    }]}
    if extract_catalog_language(sample) != "en-US":
        raise ValueError("positive qpdf catalog control failed")
    sample["qpdf"][1]["obj:1 0 R"]["value"].pop("/Lang")
    try:
        extract_catalog_language(sample)
    except ValueError:
        count += 1
    else:
        raise ValueError("missing qpdf catalog language was accepted")
    if count != 15:
        raise ValueError(f"negative control count drift: {count}")
    for loc in LOCALES:
        for name in ENVIRONMENTS:
            validate_source(make_source(loc, name), loc, name)
    return count


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8",
                            errors="replace", capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f"failed {command[0]}: {result.stderr[-600:]} {result.stdout[-600:]}")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    count = negative_controls()
    if args.preflight:
        print(f"LIST-ENV-PREFLIGHT status=PASS sources=12 negatives={count}"
              " actual_pdfs=PENDING", flush=True)
        return
    if not args.locale:
        raise ValueError("--locale required outside preflight")
    sha = run(["git", "rev-parse", "HEAD"]).strip()
    if os.getenv("SOURCE_COMMIT_SHA") and os.environ["SOURCE_COMMIT_SHA"] != sha:
        raise ValueError("source SHA differs from exact CI checkout")
    folder = OUTPUT / args.locale / "core-list-environments"
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for environment in ENVIRONMENTS:
        name = f"list-{args.locale}-{environment}"
        tex = folder / f"{name}.tex"
        pdf = folder / f"{name}.pdf"
        tex_text = make_source(args.locale, environment)
        validate_source(tex_text, args.locale, environment)
        tex.write_text(tex_text, encoding="utf-8")
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-jobname={name}",
             f"-output-directory={folder}", str(tex)])
        if not pdf.is_file() or not pdf.stat().st_size:
            raise ValueError("expected real PDF missing")
        run(["qpdf", "--check", str(pdf)])
        catalog = extract_catalog_language(json.loads(
            run(["qpdf", "--json=2", "--json-key=qpdf", str(pdf)])))
        text = run(["pdftotext", "-layout", str(pdf), "-"])
        log_bytes = (folder / f"{name}.log").read_bytes()
        validate_output(args.locale, environment, log_bytes.decode(
            "utf-8", errors="replace"), text, catalog)
        records.append({
            "locale": args.locale, "environment": environment,
            "filename": name, "catalog_lang": catalog, "verified": True,
            "tex_sha256": hashlib.sha256(tex.read_bytes()).hexdigest(),
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "log_sha256": hashlib.sha256(log_bytes).hexdigest(),
            "markers": list(MARKERS[environment]),
            "human_linguistic_normative_review": "PENDING",
        })
        print(f"LIST-ENV status=PASS locale={args.locale}"
              f" environment={environment} real_pdf=true", flush=True)
    if len(records) != len(ENVIRONMENTS) or len({
        x["environment"] for x in records}) != len(ENVIRONMENTS):
        raise ValueError("incomplete real PDF evidence matrix")
    report = {
        "source_sha": sha, "locale": args.locale,
        "status": "BOUNDED_REAL_PDF_PASS", "real_pdfs": len(records),
        "negative_controls": count, "hash_scope": "original_file_bytes",
        "proof_boundary": "three public list environments; behavior only",
        "global_i18n_acceptance": "PENDING",
        "human_linguistic_normative_review": "PENDING",
        "records": records,
    }
    (folder / "manifest.json").write_text(json.dumps(
        report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"LIST-ENV status=PASS locale={args.locale} real_pdfs={len(records)}"
          f" environments={len(ENVIRONMENTS)} negative_controls={count}"
          " global_internationalization=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"LIST-ENV status=FAIL reason={exc}") from exc

#!/usr/bin/env python3
"""Verify three optional public environments in isolated real PDFs across locales.

This behavioral proof checks public environments, PDF text and PDF catalog;
it does not certify human translation, normative layout or unrelated modules.
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
    "pt": ("pt-BR", "brazilian", "Fonte"),
    "en": ("en-US", "english", "Source"),
    "es": ("es-ES", "spanish", "Fuente"),
    "fr": ("fr-FR", "french", "Source"),
}
ENVIRONMENTS = ("ufcobject", "ufclisting", "ufcalgorithm")
MARKERS = {
    "ufcobject": ("OBJECTVISIBLEALPHA", "OBJECTVISIBLEBETA"),
    "ufclisting": ("LISTINGVISIBLEALPHA", "LISTINGVISIBLEBETA"),
    "ufcalgorithm": ("ALGORITHMSTEPALPHA", "ALGORITHMCHECK",
                     "ALGORITHMSTEPBETA"),
}
CAPTIONS = {
    "ufcobject": "OBJECTCAPTIONPROBE",
    "ufclisting": "LISTINGCAPTIONPROBE",
    "ufcalgorithm": "ALGORITHMCAPTIONPROBE",
}
SOURCES = {
    "ufcobject": "OBJECTSOURCEPROBE",
    "ufclisting": "LISTINGSOURCEPROBE",
    "ufcalgorithm": "ALGORITHMSOURCEPROBE",
}
BODY = {
    "ufcobject": (
        r"\legend{figure}{OBJECTCAPTIONPROBE}",
        r"\ufcSource{OBJECTSOURCEPROBE}",
        r"\begin{ufcobject}[here]",
        r"  \centering\fbox{\parbox{7cm}{OBJECTVISIBLEALPHA\par OBJECTVISIBLEBETA}}",
        r"\end{ufcobject}",
    ),
    "ufclisting": (
        r"\legend{code}{LISTINGCAPTIONPROBE}",
        r"\ufcSource{LISTINGSOURCEPROBE}",
        r"\begin{ufclisting}[here]",
        "int LISTINGVISIBLEALPHA = 1;",
        "int LISTINGVISIBLEBETA = 2;",
        r"\end{ufclisting}",
    ),
    "ufcalgorithm": (
        r"\legend{algorithm}{ALGORITHMCAPTIONPROBE}",
        r"\ufcSource{ALGORITHMSOURCEPROBE}",
        r"\begin{ufcalgorithm}[here][1]",
        r"\State ALGORITHMSTEPALPHA",
        r"\While{ALGORITHMCHECK}",
        r"  \State ALGORITHMSTEPBETA",
        r"\EndWhile",
        r"\end{ufcalgorithm}",
    ),
}


def make_source(locale: str, environment: str) -> str:
    if locale not in LOCALES or environment not in ENVIRONMENTS:
        raise ValueError("unsupported locale/environment")
    language = LOCALES[locale][0]
    return "\n".join([
        rf"\DocumentMetadata{{lang={language},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        (rf"\ufcsetup{{type=doctoral-thesis,document-language={locale},"
         "cover=false,coat-of-arms=false,catalog-card=false,"
         "author={SYNTHETIC ENVIRONMENT AUTHOR},"
         "title={SYNTHETIC ENVIRONMENT TEST},"
         "code=listings,algorithms=algpseudocodex}"),
        r"\lstset{language=C,columns=fullflexible,keepspaces=true,showstringspaces=false}",
        r"\begin{document}",
        r"\textual",
        *BODY[environment],
        r"\typeout{OPTIONAL-ENV-BABEL=\languagename}",
        r"\typeout{OPTIONAL-ENV-LANGUAGE=\ufcDocumentLanguage}",
        rf"\typeout{{OPTIONAL-ENV-SELECTED={environment}}}",
        r"\end{document}",
        "",
    ])


def validate_source(source: str, locale: str, environment: str) -> None:
    if source != make_source(locale, environment):
        raise ValueError("public fixture changed or missing correct flags")
    for name in ENVIRONMENTS:
        count = 1 if name == environment else 0
        if source.count(r"\begin{" + name + "}") != count:
            raise ValueError("missing/duplicate or foreign public environment")
        if source.count(r"\end{" + name + "}") != count:
            raise ValueError("unbalanced/foreign public environment")


def fold(text: str) -> str:
    value = unicodedata.normalize("NFKD", text)
    return re.sub(r"\s+", " ", "".join(c for c in value
                  if not unicodedata.combining(c))).casefold().strip()


def validate_output(locale: str, environment: str, latex_log: str,
                    pdf_text: str, catalog_language: str) -> None:
    if locale not in LOCALES or environment not in ENVIRONMENTS:
        raise ValueError("invalid PDF evidence coordinates")
    bcp, babel, source_label = LOCALES[locale]
    if catalog_language != bcp:
        raise ValueError("PDF root language mismatch")
    lines = latex_log.splitlines()
    for expected in (f"OPTIONAL-ENV-BABEL={babel}",
                     f"OPTIONAL-ENV-LANGUAGE={locale}",
                     f"OPTIONAL-ENV-SELECTED={environment}"):
        if lines.count(expected) != 1:
            raise ValueError(f"missing/duplicate log receipt: {expected}")
    visible = fold(pdf_text)
    content = MARKERS[environment]
    offsets = [visible.find(fold(token)) for token in content]
    if any(x < 0 for x in offsets) or offsets != sorted(offsets):
        raise ValueError("missing/out-of-order environment-specific PDF content")
    for token in (*content, CAPTIONS[environment], SOURCES[environment]):
        if visible.count(fold(token)) != 1:
            raise ValueError(f"missing/duplicate visible PDF marker: {token}")
    if fold(source_label + ":") not in visible:
        raise ValueError("class-owned source label not localized in actual PDF")
    for other in ENVIRONMENTS:
        if other == environment:
            continue
        for forbidden in (*MARKERS[other], CAPTIONS[other], SOURCES[other]):
            if fold(forbidden) in visible:
                raise ValueError("foreign optional environment leaked into PDF")


def pdf_lang(catalog: dict) -> str:
    blocks = catalog.get("qpdf")
    if not isinstance(blocks, list) or len(blocks) != 2:
        raise ValueError("unsupported qpdf JSON catalog")
    if blocks[0].get("jsonversion") != 2:
        raise ValueError("unexpected qpdf JSON version")
    items = blocks[1]
    ref = items["trailer"]["value"]["/Root"]
    if not isinstance(ref, str) or not re.fullmatch(r"[1-9]\d* \d+ R", ref):
        raise ValueError("invalid PDF root reference")
    root = items["obj:" + ref]["value"]
    if root.get("/Type") != "/Catalog":
        raise ValueError("object is not PDF root catalog")
    value = root.get("/Lang")
    if not isinstance(value, str) or not value.startswith("u:"):
        raise ValueError("PDF /Root/Lang missing")
    return value[2:]


def negative_controls() -> int:
    loc, env = "en", "ufcobject"
    good_source = make_source(loc, env)
    validate_source(good_source, loc, env)
    mutations = (
        good_source.replace(r"\begin{ufcobject}[here]", "", 1),
        good_source.replace(r"\end{ufcobject}", "", 1),
        good_source.replace("OBJECTVISIBLEBETA", "BROKENVALUE", 1),
        good_source.replace("document-language=en", "document-language=es", 1),
    )
    count = 0
    for mutant in mutations:
        try:
            validate_source(mutant, loc, env)
        except ValueError:
            count += 1
        else:
            raise ValueError("source mutation escaped")
    log = "\n".join(("OPTIONAL-ENV-BABEL=english",
                     "OPTIONAL-ENV-LANGUAGE=en",
                     "OPTIONAL-ENV-SELECTED=ufcobject"))
    visible = "OBJECTCAPTIONPROBE Source: OBJECTSOURCEPROBE OBJECTVISIBLEALPHA OBJECTVISIBLEBETA"
    validate_output(loc, env, log, visible, "en-US")
    damaged = (
        (log.replace("BABEL=english", "BABEL=french"), visible, "en-US"),
        (log.replace("LANGUAGE=en", "LANGUAGE=es"), visible, "en-US"),
        (log.replace("SELECTED=ufcobject", "SELECTED=ufclisting"), visible, "en-US"),
        (log + "\nOPTIONAL-ENV-SELECTED=ufcobject", visible, "en-US"),
        (log, visible.replace("OBJECTVISIBLEALPHA", "REMOVED"), "en-US"),
        (log, visible.replace("OBJECTVISIBLEBETA", "REMOVED"), "en-US"),
        (log, visible.replace("OBJECTCAPTIONPROBE", "REMOVED"), "en-US"),
        (log, visible.replace("OBJECTSOURCEPROBE", "REMOVED"), "en-US"),
        (log, visible.replace("Source:", "NotLocalized:"), "en-US"),
        (log, visible + " LISTINGVISIBLEALPHA", "en-US"),
        (log, visible, "pt-BR"),
    )
    for item in damaged:
        try:
            validate_output(loc, env, *item)
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid PDF/log mutation escaped")
    sample = {"qpdf": [{"jsonversion": 2}, {
        "trailer": {"value": {"/Root": "1 0 R"}},
        "obj:1 0 R": {"value": {"/Type": "/Catalog", "/Lang": "u:en-US"}},
    }]}
    if pdf_lang(sample) != "en-US":
        raise ValueError("valid PDF catalog rejected")
    sample["qpdf"][1]["obj:1 0 R"]["value"].pop("/Lang")
    try:
        pdf_lang(sample)
    except ValueError:
        count += 1
    else:
        raise ValueError("missing catalog language accepted")
    # Test both remaining public environments against independent output mutations.
    for other_env in ("ufclisting", "ufcalgorithm"):
        other_log = "\n".join(("OPTIONAL-ENV-BABEL=english",
                               "OPTIONAL-ENV-LANGUAGE=en",
                               f"OPTIONAL-ENV-SELECTED={other_env}"))
        other_text = " ".join((
            CAPTIONS[other_env], "Source:", SOURCES[other_env],
            *MARKERS[other_env]))
        validate_output(loc, other_env, other_log, other_text, "en-US")
        wrong_output = (
            other_text.replace(CAPTIONS[other_env], "REMOVED"),
            other_text.replace(MARKERS[other_env][0], "REMOVED"),
            other_text + " OBJECTVISIBLEALPHA",
        )
        for altered in wrong_output:
            try:
                validate_output(loc, other_env, other_log, altered, "en-US")
            except ValueError:
                count += 1
            else:
                raise ValueError("optional environment PDF mutation escaped")
    if count != 22:
        raise ValueError(f"negative coverage drift: {count}")
    if len(LOCALES) * len(ENVIRONMENTS) != 12:
        raise ValueError("public environment cross-product drift")
    for locale in LOCALES:
        for name in ENVIRONMENTS:
            validate_source(make_source(locale, name), locale, name)
    return count


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise ValueError(f"command {command[0]} failed: {result.stderr[-650:]}"
                         f" {result.stdout[-650:]}")
    return result.stdout


def main() -> None:
    args = argparse.ArgumentParser()
    args.add_argument("--preflight", action="store_true")
    args.add_argument("--locale", choices=tuple(LOCALES))
    options = args.parse_args()
    count = negative_controls()
    if options.preflight:
        print(f"OPTIONAL-ENV-PREFLIGHT status=PASS sources=12 negatives={count}"
              " actual_pdfs=PENDING", flush=True)
        return
    if not options.locale:
        raise ValueError("--locale required to compile actual PDFs")
    sha = run(["git", "rev-parse", "HEAD"]).strip()
    expected = os.getenv("SOURCE_COMMIT_SHA")
    if expected and expected != sha:
        raise ValueError("checked-out Git SHA differs from workflow SHA")
    folder = OUTPUT / options.locale / "optional-environments"
    folder.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    for environment in ENVIRONMENTS:
        job = f"object-env-{options.locale}-{environment}"
        tex = folder / f"{job}.tex"
        pdf = folder / f"{job}.pdf"
        source = make_source(options.locale, environment)
        validate_source(source, options.locale, environment)
        tex.write_text(source, encoding="utf-8")
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-jobname={job}",
             f"-output-directory={folder}", str(tex)])
        if not pdf.exists() or pdf.stat().st_size <= 0:
            raise ValueError(f"missing/empty real PDF: {job}")
        run(["qpdf", "--check", str(pdf)])
        lang = pdf_lang(json.loads(run(["qpdf", "--json=2", "--json-key=qpdf", str(pdf)])))
        text = run(["pdftotext", "-layout", str(pdf), "-"])
        log_path = folder / f"{job}.log"
        log_bytes = log_path.read_bytes()
        validate_output(options.locale, environment,
                        log_bytes.decode("utf-8", errors="replace"), text, lang)
        records.append({
            "environment": environment, "locale": options.locale,
            "job": job, "verified": True,
            "pdf_catalog_lang": lang,
            "tex_sha256": hashlib.sha256(tex.read_bytes()).hexdigest(),
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "log_sha256": hashlib.sha256(log_bytes).hexdigest(),
            "visible_tokens": list(MARKERS[environment]),
            "visible_caption": CAPTIONS[environment],
            "human_linguistic_normative_review": "PENDING",
        })
        print(f"OPTIONAL-ENV status=PASS locale={options.locale}"
              f" environment={environment} actual_pdf=true", flush=True)
    if len(records) != len(ENVIRONMENTS) or len({
            row["environment"] for row in records}) != len(ENVIRONMENTS):
        raise ValueError("incomplete/duplicate environment receipt")
    report = {
        "source_sha": sha, "locale": options.locale, "real_pdfs": len(records),
        "negative_controls": count, "status": "BOUNDED_REAL_PDF_PASS",
        "sha256_scope": "raw_original_file_bytes",
        "global_internationalization": "PENDING",
        "human_linguistic_normative_review": "PENDING",
        "proof_boundary": "three isolated optional public environments",
        "records": records,
    }
    (folder / "manifest.json").write_text(json.dumps(
        report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OPTIONAL-ENV status=PASS locale={options.locale}"
          f" real_pdfs={len(records)} negative_controls={count}"
          " human_review=PENDING", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as error:
        raise SystemExit(f"OPTIONAL-ENV status=FAIL reason={error}") from error

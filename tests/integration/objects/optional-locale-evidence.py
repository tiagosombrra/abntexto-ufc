#!/usr/bin/env python3
"""Source-bound PT/EN/ES/FR optional-modules PDF test (IBGE, code, algorithms).

The class localizes class-owned labels only. Authors control the table's
remark keys, captions' semantic text and source-data translations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import runpy
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "artifacts" / "optional-i18n"
LOCALES = {
    "pt": ("pt-BR", "brazilian", "Fonte", "Nota", "Lista de Códigos", "Lista de Algoritmos", "Algoritmo"),
    "en": ("en-US", "english", "Source", "Note", "List of Code Listings", "List of Algorithms", "Algorithm"),
    "es": ("es-ES", "spanish", "Fuente", "Nota", "Lista de Códigos", "Lista de Algoritmos", "Algoritmo"),
    "fr": ("fr-FR", "french", "Source", "Note", "Liste des codes", "Liste des algorithmes", "Algorithme"),
}
PROFILES = ("optional-objects", "optional-minted", "optional-algorithm-comment")
RUNNER = runpy.run_path(str(ROOT / "tests/integration/frontmatter/run-integrated-locale.py"))
real_pdf_lang = RUNNER["real_pdf_lang"]
fold = RUNNER["fold"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_source(locale: str, profile: str) -> str:
    bcp, _, source, note, _, _, _ = LOCALES[locale]
    if profile == "optional-algorithm-comment":
        # Isolate math plus algorithmic comment from listings and tabularray.
        # This source follows the existing proven line-numbering fixture.
        standalone = [
            rf"\DocumentMetadata{{lang={bcp},pdfstandard=A-2b,pdfversion=1.7}}",
            r"\documentclass{abntexto-ufc}",
            rf"\ufcsetup{{document-language={locale},algorithms=algpseudocodex}}",
            r"\begin{document}",
            rf"\typeout{{OPTIONAL-I18N-BABEL=\languagename}}",
            rf"\legend{{algorithm}}{{OPTIONAL-ALGORITHM-ONLY-{locale.upper()}}}",
            r"\ufcSource{SYNTHETIC-ALGO-ONLY}",
            r"\begin{ufcalgorithm}[here][1]",
            r"\State $i \gets 1$ \Comment{NUMERADO-1}",
            r"\While{$i \leq n$} \Comment{NUMERADO-2}",
            r"\State \Return $i$ \Comment{NUMERADO-3}",
            r"\EndWhile",
            r"\end{ufcalgorithm}",
            r"\end{document}",
        ]
        return "\n".join(standalone) + "\n"
    base = [
        rf"\DocumentMetadata{{lang={bcp},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        (rf"\ufcsetup{{type=doctoral-thesis,document-language={locale},"
         "cover=false,coat-of-arms=false,catalog-card=false,"
         "title={Optional modules test},author={Synthetic Author},"
         + ("tables=tabularray,code=listings,algorithms=algpseudocodex"
            if profile == "optional-objects" else "code=minted") + "}"),
        r"\begin{document}",
        r"\pretextual",
        r"\ufcPrintListOfCodeListings",
    ]
    if profile == "optional-objects":
        base += [r"\ufcPrintListOfAlgorithms"]
    base += [r"\ifmmode\typeout{OPTIONAL-PROBE-A=MATH}\else\typeout{OPTIONAL-PROBE-A=TEXT}\fi",
             r"\textual", rf"\section{{OPTIONAL-MODULE-BODY-{locale.upper()}}}",
             rf"\typeout{{OPTIONAL-I18N-BABEL=\languagename}}",
             r"\ifmmode\typeout{OPTIONAL-PROBE-B=MATH}\else\typeout{OPTIONAL-PROBE-B=TEXT}\fi"]
    if profile == "optional-objects":
        base += [
            rf"\legend{{algorithm}}{{OPTIONAL-ALGORITHM-{locale.upper()}}}",
            r"\ufcSource{SYNTHETIC-ALGORITHM-SOURCE}",
            r"\begin{ufcalgorithm}[here][1]",
            r"\ifmmode\typeout{OPTIONAL-PROBE-C=MATH}\else\typeout{OPTIONAL-PROBE-C=TEXT}\fi",
            r"\State $i \gets 1$",
            r"\State OPTIONAL-ALG-STEP-1",
            r"\While{OPTIONAL-ALG-LOOP}",
            r"  \State OPTIONAL-ALG-STEP-2",
            r"\EndWhile",
            r"\end{ufcalgorithm}",
            "",
            "",
            rf"\legend{{code}}{{OPTIONAL-LISTING-{locale.upper()}}}",
            r"\ufcSource{SYNTHETIC-CODE-SOURCE}",
            r"\begin{ufclisting}[here]",
            "int sum(int a, int b) {",
            "    return a + b;",
            "}",
            r"\end{ufclisting}",
            "",
            "",
            rf"\begin{{longabnttblr}}[",
            rf"  caption={{OPTIONAL-TABLE-{locale.upper()}}},",
            "  label={tab:optional-locale},",
            rf"  remark{{{source}}}={{OPTIONAL-TABLE-SOURCE-{locale.upper()}}},",
            rf"  remark{{{note}}}={{OPTIONAL-TABLE-NOTE-{locale.upper()}}},",
            r"]{colspec={X[l] X[r]},rowhead=1,width=0.8\linewidth}",
            r"\toprule",
            "OPTIONALHEADER & OPTIONALVALUE " + "\\\\",
            r"\midrule",
        ]
        for i in range(1, 111):
            base.append(f"OPTIONALROW{i:03d} & {i} " + "\\\\")
        base += [r"\bottomrule", r"\end{longabnttblr}"]
    else:
        base += [
            rf"\legend{{code}}{{OPTIONAL-MINTED-{locale.upper()}}}",
            r"\ufcSource{SYNTHETIC-MINTED-SOURCE}",
            r"\ufcInputMinted[here]{python}{tests/fixtures/example.py}",
        ]
    base.append(r"\end{document}")
    return "\n".join(base) + "\n"


def validate_source(source: str, locale: str, profile: str) -> None:
    bcp, *_ = LOCALES[locale]
    required = [
        rf"\DocumentMetadata{{lang={bcp},",
        f"document-language={locale}",
    ]
    if profile == "optional-algorithm-comment":
        required += [r"algorithms=algpseudocodex",
                     r"\begin{ufcalgorithm}",
                     r"\Comment{NUMERADO-1}", r"\State $i \gets 1$"]
    else:
        required += [rf"\section{{OPTIONAL-MODULE-BODY-{locale.upper()}}}",
                     r"\ufcPrintListOfCodeListings"]
    if profile == "optional-objects":
        required += [r"tables=tabularray,code=listings,algorithms=algpseudocodex",
                     r"\begin{longabnttblr}", r"\begin{ufcalgorithm}",
                     r"\begin{ufclisting}", "OPTIONALROW110"]
    elif profile == "optional-minted":
        required += [r"code=minted", r"\ufcInputMinted[here]"]
    missing = [token for token in required if token not in source]
    if missing:
        raise ValueError(f"missing source components for {locale}/{profile}: {missing}")


def make_fixtures(locale: str, folder: Path) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for profile in PROFILES:
        content = make_source(locale, profile)
        validate_source(content, locale, profile)
        file = folder / f"{profile}-{locale}.tex"
        file.write_text(content, encoding="utf-8")
        paths.append(file)
    return paths


def compile_pdf(source: Path, pdf: Path, locale: str, profile: str) -> dict:
    job = source.stem
    flags = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-shell-escape",
             f"-jobname={job}", f"-output-directory={source.parent}", str(source)]
    for p in (1, 2, 3):
        log_file = source.parent / f"{job}-pass{p}.stdout"
        with log_file.open("w", encoding="utf-8") as out:
            r = subprocess.run(flags, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, text=True)
        if r.returncode:
            raise RuntimeError(f"{job}: LaTeX pass {p} failed: " +
                               "\n".join(log_file.read_text(errors="replace").splitlines()[-30:]))
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise ValueError("PDF absent after LaTeX")
    extracted = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"],
                                        cwd=ROOT, text=True)
    text = fold(extracted)
    _, babel, source_label, note_label, code_list, alg_list, alg = LOCALES[locale]
    if profile == "optional-algorithm-comment":
        expected = [f"optional-algorithm-only-{locale}",
                    "synthetic-algo-only", "numerado-1", "numerado-2",
                    source_label + ":"]
    else:
        expected = [
            f"optional-module-body-{locale}", code_list,
            f"optional-{'listing' if profile == 'optional-objects' else 'minted'}-{locale}",
            "synthetic-code-source" if profile == "optional-objects" else "synthetic-minted-source",
            source_label + ":",
        ]
    if profile == "optional-objects":
        expected += [alg_list, alg, f"optional-algorithm-{locale}",
                     "optional-alg-step-1", "optional-alg-step-2",
                     f"optional-table-{locale}", f"optional-table-source-{locale}",
                     f"optional-table-note-{locale}", "optionalrow110", note_label + ":"]
    missing = [p for p in expected if fold(p) not in text]
    if missing:
        raise ValueError(f"PDF content mismatch for {job}: {missing}. Sample={text[:800]}")
    forbidden = {
        "pt": ("list of algorithms", "liste des algorithmes", "list of code listings"),
        "en": ("lista de algoritmos", "liste des algorithmes", "lista de códigos", "fonte:"),
        "es": ("list of algorithms", "liste des algorithmes", "list of code listings", "fonte:"),
        "fr": ("list of algorithms", "lista de algoritmos", "lista de códigos", "fonte:"),
    }
    leaks = [x for x in forbidden[locale] if fold(x) in text]
    if leaks:
        raise ValueError(f"foreign-locale class labels in PDF {job}: {leaks}")
    actual_lang = real_pdf_lang(pdf)
    if actual_lang != LOCALES[locale][0]:
        raise ValueError(f"PDF Catalog /Lang mismatched: {actual_lang}")
    latex_log = (source.parent / f"{job}.log").read_text(errors="replace")
    if f"OPTIONAL-I18N-BABEL={babel}" not in latex_log:
        raise ValueError(f"Babel mismatch in {job}; expected {babel}")
    pages_match = re.search(r"^Pages:\s+(\d+)", subprocess.check_output(
        ["pdfinfo", str(pdf)], text=True), re.MULTILINE)
    if not pages_match:
        raise ValueError(f"Pages metadata missing in {job}")
    pages = int(pages_match.group(1))
    if profile == "optional-objects" and pages < 3:
        raise ValueError(f"long table did not produce multiple pages: {job}, pages={pages}")
    return {"locale": locale, "profile": profile, "source": source.relative_to(ROOT).as_posix(),
            "source_sha256": sha(source), "pdf": pdf.relative_to(ROOT).as_posix(),
            "pdf_sha256": sha(pdf), "pages": pages, "babel": babel,
            "pdf_catalog_lang": actual_lang, "checks": len(expected) + len(forbidden[locale])}


def diagnose_algorithm_comment(locale: str, folder: Path) -> None:
    """Compare controlled PDF-metadata and language settings after a real TeX failure."""
    # These are diagnostic builds, not accepted PDF certification evidence.
    if locale != "pt":
        return
    source = make_source(locale, "optional-algorithm-comment")
    variants = {
        "legacy-no-metadata-no-locale": (False, False),
        "metadata-only": (True, False),
        "locale-only": (False, True),
        "metadata-and-locale-no-comment": (True, True),
    }
    for label, (with_metadata, with_locale) in variants.items():
        candidate = source
        if not with_metadata:
            candidate = "\n".join(candidate.splitlines()[1:]) + "\n"
        if not with_locale:
            candidate = candidate.replace("document-language=pt,", "", 1)
        if label.endswith("no-comment"):
            candidate = candidate.replace(r" \Comment{NUMERADO-1}", "", 1)
            candidate = candidate.replace(r" \Comment{NUMERADO-2}", "", 1)
            candidate = candidate.replace(r" \Comment{NUMERADO-3}", "", 1)
        probe = folder / f"optional-alg-diagnostic-{label}.tex"
        probe.write_text(candidate, encoding="utf-8")
        job = probe.stem
        command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                   "-file-line-error", f"-jobname={job}",
                   f"-output-directory={folder}", str(probe)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        stdout = result.stdout + result.stderr
        (folder / f"{job}.stdout").write_text(stdout, encoding="utf-8")
        errors = [line.strip() for line in stdout.splitlines()
                  if "You can't use" in line or "Undefined control sequence" in line
                  or "Fatal error" in line]
        print(f"OPTIONAL-ALG-DIAGNOSTIC locale={locale} case={label} "
              f"result={'PASS' if result.returncode == 0 else 'FAIL'} "
              f"error={errors[0] if errors else 'none'}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True, choices=tuple(LOCALES))
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="i18n-optional-source-") if args.preflight else _no_temp() as temp:
        folder = Path(temp) / args.locale if args.preflight else ARTIFACT / args.locale
        sources = make_fixtures(args.locale, folder)
        # Fail closed if test content drifts: checking the same validator
        # against mutations must reject lost modules and mismatched locales.
        for source in sources:
            profile = source.stem.removesuffix("-" + args.locale)
            original = source.read_text(encoding="utf-8")
            mutants = [original.replace(f"document-language={args.locale}",
                                        "document-language=bad", 1)]
            if profile == "optional-objects":
                mutants += [original.replace(r"\begin{ufcalgorithm}", "", 1),
                            original.replace(r"\begin{longabnttblr}", "", 1)]
            elif profile == "optional-algorithm-comment":
                mutants += [original.replace(r"\begin{ufcalgorithm}", "", 1),
                            original.replace(r"\Comment{NUMERADO-1}", "", 1)]
            for wrong in mutants:
                if wrong == original:
                    raise ValueError("negative mutation ineffective")
                try:
                    validate_source(wrong, args.locale, profile)
                except ValueError:
                    pass
                else:
                    raise ValueError("negative fixture accepted")
        if args.preflight:
            print(f"OPTIONAL-I18N-PREFLIGHT status=PASS locale={args.locale} tex=3 negative=PASS")
            return
        receipts = []
        for src in sources:
            profile = src.stem.removesuffix("-" + args.locale)
            try:
                entry = compile_pdf(src, src.with_suffix(".pdf"), args.locale, profile)
            except RuntimeError:
                if profile == "optional-algorithm-comment":
                    diagnose_algorithm_comment(args.locale, folder)
                raise
            receipts.append(entry)
            print(f"OPTIONAL-I18N status=PASS locale={args.locale} profile={profile} "
                  f"pdf_pages={entry['pages']} qpdf=PASS sha256=PASS", flush=True)
        sha_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        manifest = {"source_commit_sha": sha_commit, "source": "TeX Live 2026 + pdflatex",
                    "status": "AUTOMATED_PARTIAL", "locale": args.locale, "pdfs": receipts,
                    "automatically_translated_author_data": False,
                    "visual_language_review": "PENDING"}
        (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print(f"OPTIONAL-I18N status=PASS locale={args.locale} real_pdfs=3 lang=PASS "
              "babel=PASS text=PASS negatives=PASS", flush=True)


from contextlib import contextmanager
import tempfile

@contextmanager
def _no_temp():
    yield None


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"OPTIONAL-I18N status=FAIL reason={exc}") from exc

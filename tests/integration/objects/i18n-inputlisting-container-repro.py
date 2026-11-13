#!/usr/bin/env python3
"""Reproduce nested InputListing failures with controlled factorial TeX sources.

This experimental runner NEVER certifies a public API or publishes a package.
It preserves every source/log/PDF SHA, including intentionally failed builds,
and distinguishes observed results from scientific hypotheses.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "artifacts/inputlisting-container-repro"
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PROFILES = ("scientific-article", "undergraduate-capstone")
SOURCE_CPP = "tests/fixtures/example.cpp"
ERROR_MARKER = r"File ended while scanning use of \__math_grab_dollar_delim:w"


@dataclass(frozen=True)
class Case:
    profile: str
    nested: bool
    legend: bool
    label: bool
    lstset: bool

    def name(self) -> str:
        ident = "article" if self.profile == "scientific-article" else "capstone"
        switches = [
            "nested" if self.nested else "direct",
            "legend" if self.legend else "no-legend",
            "label" if self.label else "no-label",
            "lstset" if self.lstset else "no-lstset",
        ]
        return ident + "-" + "-".join(switches)


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cases() -> list[Case]:
    result = [
        Case(profile, nested, legend, label, lstset)
        for profile, nested, legend, label, lstset in
        itertools.product(PROFILES, (False, True), (False, True),
                          (False, True), (False, True))
    ]
    if len(result) != 32 or len({c.name() for c in result}) != 32:
        raise ValueError("InputListing controlled factorial inventory drift")
    return result


def tex(case: Case, locale: str) -> str:
    if locale not in LOCALES:
        raise ValueError("unsupported document locale")
    lines = [
        rf"\DocumentMetadata{{lang={LOCALES[locale]},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{type={case.profile},document-language={locale},"
        r"code=listings,cover=false,coat-of-arms=false,catalog-card=false,"
        r"title={InputListing container reproduction},author={Synthetic Author}}",
    ]
    if case.lstset:
        lines.extend([
            r"\lstset{breaklines=true,columns=fullflexible,",
            r"  keepspaces=true,showstringspaces=false}",
        ])
    lines.extend([
        r"\begin{document}",
        r"\textual",
        rf"\section{{REPRO-BODY-{locale.upper()}}}",
    ])
    if case.legend:
        lines.extend([
            rf"\legend{{code}}{{REPRO-LEGEND-{locale.upper()}}}",
            rf"\ufcSource{{REPRO-SOURCE-{locale.upper()}}}",
        ])
    if case.label:
        lines.append(rf"\label{{cod:repro-{locale}}}")
    if case.nested:
        lines.append(r"\begin{ufcobject}[here]")
    lines.append(rf"\ufcInputListing[language=C++]{{{SOURCE_CPP}}}")
    if case.nested:
        lines.append(r"\end{ufcobject}")
    lines.extend([r"\end{document}", ""])
    return "\n".join(lines)


def preflight() -> None:
    specimen = cases()
    for locale in LOCALES:
        for case in specimen:
            value = tex(case, locale)
            if value.count(r"\ufcInputListing[language=C++]") != 1:
                raise ValueError("reproduction source omits/duplicates public import")
            if value.count(r"\begin{ufcobject}[here]") != int(case.nested):
                raise ValueError("reproduction source nested start drift")
            if value.count(r"\end{ufcobject}") != int(case.nested):
                raise ValueError("reproduction source nested closing drift")
            if value.count(r"\legend{code}") != int(case.legend):
                raise ValueError("reproduction source legend branch drift")
            if value.count(r"\lstset{") != int(case.lstset):
                raise ValueError("reproduction source listings setup drift")
            if value.count(r"\label{cod:repro") != int(case.label):
                raise ValueError("reproduction source label branch drift")
    if not (ROOT / SOURCE_CPP).is_file():
        raise ValueError("original C++ fixture absent")
    print("I18N-INPUTLISTING-REPRO-PREFLIGHT status=PASS"
          " profiles=2 context=2 legends=2 labels=2 lstset=2"
          " locales=4 scenarios_per_locale=32 global_cases=128"
          " publication_authorized=false")


def run(locale: str) -> None:
    folder = BASE / locale
    folder.mkdir(parents=True, exist_ok=True)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    results = []
    for case in cases():
        name = "repro-" + case.name()
        src = folder / (name + ".tex")
        src.write_text(tex(case, locale), encoding="utf-8")
        process = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-jobname=" + name,
             "-output-directory=" + str(folder), str(src)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        log = folder / (name + ".log")
        pdf = folder / (name + ".pdf")
        output = process.stdout + "\n" + process.stderr
        texlog = log.read_text(errors="replace") if log.is_file() else ""
        success = process.returncode == 0 and pdf.is_file()
        if success:
            check = subprocess.run(["qpdf", "--check", str(pdf)],
                                   cwd=ROOT, capture_output=True, text=True,
                                   check=False)
            if check.returncode:
                raise ValueError(f"successful compilation has invalid PDF: {name}")
        results.append({
            "case": asdict(case), "name": name,
            "status": "VALID_PDF" if success else "TEX_FAILURE",
            "math_delimiter_error": ERROR_MARKER in output or ERROR_MARKER in texlog,
            "exit_code": process.returncode,
            "source_sha256": digest(src), "log_sha256": digest(log),
            "pdf_sha256": digest(pdf),
        })
        print(f"INPUTLISTING-CASE {locale}/{name}"
              f" status={'VALID_PDF' if success else 'TEX_FAILURE'}"
              f" math_delim_error={results[-1]['math_delimiter_error']}")
    for profile in PROFILES:
        controls = [
            item for item in results
            if item["case"] == asdict(Case(profile, False, False, False, False))
        ]
        if len(controls) != 1 or controls[0]["status"] != "VALID_PDF":
            raise ValueError(f"standalone positive control failed: {profile}/{locale}")
    summary = {
        "source_sha": sha, "locale": locale, "cases": len(results),
        "valid_pdf": sum(r["status"] == "VALID_PDF" for r in results),
        "tex_failures": sum(r["status"] == "TEX_FAILURE" for r in results),
        "math_delimiter_errors": sum(r["math_delimiter_error"] for r in results),
        "observations": results,
        "interpretation": "EXPLORE_ONLY_CAUSE_NOT_ESTABLISHED",
        "ledger_promotion": "NOT_AUTHORIZED",
        "human_normative_linguistic_review": "PENDING",
        "publication_authorized": False,
    }
    (folder / "repro-manifest.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"I18N-INPUTLISTING-REPRO status=RECORDED locale={locale}"
          f" real_pdf={summary['valid_pdf']}"
          f" errors={summary['tex_failures']}"
          f" math_delimiter_errors={summary['math_delimiter_errors']}"
          " conclusion=UNDETERMINED human_review=PENDING")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    try:
        preflight()
        if args.locale and not args.preflight:
            run(args.locale)
        elif not args.preflight:
            raise ValueError("select --preflight or --locale")
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        raise SystemExit(f"I18N-INPUTLISTING-REPRO status=FAIL reason={e}") from e

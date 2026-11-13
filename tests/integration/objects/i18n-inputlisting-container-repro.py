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



def isolation_tex(profile: str, wrapper: str, importer: str) -> str:
    """Build a minimal controlled source for the wrapper-level causal experiment."""
    if profile not in PROFILES or wrapper not in ("direct", "place", "ufcobject", "minipage"):
        raise ValueError("unknown isolation profile or wrapper")
    if importer not in ("public", "native"):
        raise ValueError("unknown import command")
    head = [
        r"\DocumentMetadata{lang=pt-BR,pdfstandard=A-2b,pdfversion=1.7}",
        r"\documentclass{abntexto-ufc}",
        rf"\ufcsetup{{type={profile},document-language=pt,code=listings,"
        r"cover=false,coat-of-arms=false,catalog-card=false,"
        r"title={InputListing isolation},author={Synthetic Author}}",
        r"\begin{document}",
        r"\textual",
        r"\section{Isolation test}",
    ]
    starts = {
        "direct": None,
        "place": r"\begin{place}[here]",
        "ufcobject": r"\begin{ufcobject}[here]",
        "minipage": r"\begin{minipage}{\linewidth}",
    }
    ends = {
        "direct": None, "place": r"\end{place}",
        "ufcobject": r"\end{ufcobject}",
        "minipage": r"\end{minipage}",
    }
    if starts[wrapper]:
        head.append(starts[wrapper])
    command = r"\ufcInputListing" if importer == "public" else r"\lstinputlisting"
    head.append(command + r"[language=C++]{tests/fixtures/example.cpp}")
    if ends[wrapper]:
        head.append(ends[wrapper])
    return "\n".join(head + [r"\end{document}", ""])


def isolation_preflight() -> None:
    """Fail closed when the isolation matrix loses any controlled variant."""
    scenarios = [(profile, wrapper, importer)
                 for profile, wrapper, importer in itertools.product(
                     PROFILES, ("direct", "place", "ufcobject", "minipage"),
                     ("public", "native"))]
    if len(scenarios) != 16:
        raise ValueError("isolation matrix inventory drift")
    for profile, wrapper, importer in scenarios:
        source = isolation_tex(profile, wrapper, importer)
        if source.count(r"\lstinputlisting" if importer == "native" else r"\ufcInputListing") != 1:
            raise ValueError("isolation import drift")
        if source.count(r"\begin{place}[here]") != int(wrapper == "place"):
            raise ValueError("place wrapper drift")
        if source.count(r"\begin{ufcobject}[here]") != int(wrapper == "ufcobject"):
            raise ValueError("ufcobject wrapper drift")
        if source.count(r"\begin{minipage}") != int(wrapper == "minipage"):
            raise ValueError("minipage wrapper drift")
    print("I18N-INPUTLISTING-ISOLATION-PREFLIGHT status=PASS cases=16"
          " profiles=2 wrappers=4 importers=2 publication_authorized=false")


def run_isolation() -> None:
    """Record exact-source TeX/PDF evidence without promoting a failing API."""
    isolation_preflight()
    folder = BASE / "isolation-pt"
    folder.mkdir(parents=True, exist_ok=True)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    results = []
    for profile, wrapper, importer in itertools.product(
        PROFILES, ("direct", "place", "ufcobject", "minipage"),
        ("public", "native")
    ):
        name = "isolate-" + ("article" if profile == PROFILES[0] else "capstone")
        name += "-" + wrapper + "-" + importer
        src = folder / (name + ".tex")
        src.write_text(isolation_tex(profile, wrapper, importer), encoding="utf-8")
        process = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-jobname=" + name,
             "-output-directory=" + str(folder), str(src)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        log = folder / (name + ".log")
        pdf = folder / (name + ".pdf")
        output = process.stdout + "\n" + process.stderr
        success = process.returncode == 0 and pdf.is_file()
        if success:
            verify = subprocess.run(["qpdf", "--check", str(pdf)],
                                    cwd=ROOT, capture_output=True, text=True,
                                    check=False)
            if verify.returncode != 0:
                raise ValueError("invalid isolation PDF: " + name)
        marker = ERROR_MARKER in output or (
            log.is_file() and ERROR_MARKER in log.read_text(errors="replace"))
        results.append({
            "name": name, "profile": profile, "wrapper": wrapper,
            "importer": importer, "status": "VALID_PDF" if success else "TEX_FAILURE",
            "math_delimiter_error": bool(marker), "exit_code": process.returncode,
            "source_sha256": digest(src), "log_sha256": digest(log),
            "pdf_sha256": digest(pdf),
        })
        print(f"INPUTLISTING-ISOLATION {name}"
              f" status={'VALID_PDF' if success else 'TEX_FAILURE'}"
              f" math_delim_error={bool(marker)}")
    # Both direct and minipage imports are proven positive control paths.
    # Do not lock the inherited place failure as an expected long-term result.
    for profile in PROFILES:
        for importer in ("public", "native"):
            for wrapper in ("direct", "minipage"):
                baseline = [r for r in results if r["profile"] == profile
                            and r["wrapper"] == wrapper
                            and r["importer"] == importer]
                if len(baseline) != 1 or baseline[0]["status"] != "VALID_PDF":
                    raise ValueError("positive import control failed: "
                                     + profile + "/" + importer + "/" + wrapper)
    result = {
        "source_sha": sha, "locale": "pt", "cases": len(results),
        "observations": results,
        "conclusion": "EXPERIMENTAL_NOT_YET_RUNTIME_FIX",
        "ledger_promotion": "NOT_AUTHORIZED",
        "publication_authorized": False,
    }
    (folder / "isolation-manifest.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("I18N-INPUTLISTING-ISOLATION status=RECORDED cases=16"
          f" valid_pdf={sum(x['status'] == 'VALID_PDF' for x in results)}"
          " root_cause=NOT_YET_PROVEN publication_authorized=false")


# Experimental proposal only. It does not change the shipped class.
# The public external import gains a vertical box only inside inner horizontal mode.
# This follows the class's existing ufclisting layout strategy without changing
# pagination of direct, nonboxed imports.
CANDIDATE_PATCH = (
    r"\ExplSyntaxOn",
    r"\RenewDocumentCommand \ufcInputListing { O{} m }",
    r"  {",
    r"    \mode_if_horizontal:TF",
    r"      {",
    r"        \mode_if_inner:TF",
    r"          { \vbox{ \hsize=\linewidth \lstinputlisting[#1]{#2} } }",
    r"          { \lstinputlisting[#1]{#2} }",
    r"      }",
    r"      { \lstinputlisting[#1]{#2} }",
    r"  }",
    r"\ExplSyntaxOff",
)


def candidate_preflight() -> None:
    """Prove that the experimental patch tests only the public import path."""
    if len(CANDIDATE_PATCH) != 12:
        raise ValueError("experimental patch line inventory drift")
    if not any(r"\mode_if_inner:TF" in x for x in CANDIDATE_PATCH):
        raise ValueError("inner-horizontal candidate guard absent")
    if not any(r"\vbox" in x for x in CANDIDATE_PATCH):
        raise ValueError("vertical wrapper candidate absent")
    for profile, wrapper, legend in itertools.product(
        PROFILES, ("direct", "place", "ufcobject", "minipage"), (False, True)
    ):
        value = candidate_tex(profile, wrapper, legend)
        if value.count(r"\RenewDocumentCommand \ufcInputListing") != 1:
            raise ValueError("candidate injection drift")
        if value.count(r"\ufcInputListing[language=C++]") != 1:
            raise ValueError("candidate invocation drift")
        if value.count(r"\legend{code}") != int(legend):
            raise ValueError("candidate legend drift")
    print("I18N-INPUTLISTING-CANDIDATE-PREFLIGHT status=PASS"
          " cases=16 runtime_class_unchanged=true publication_authorized=false")


def candidate_tex(profile: str, wrapper: str, legend: bool) -> str:
    """Create a standalone source with the hypothetical localized macro patch."""
    value = isolation_tex(profile, wrapper, "public")
    entry = r"\begin{document}" + "\n"
    extra = "\n".join(CANDIDATE_PATCH) + "\n"
    if value.count(entry) != 1:
        raise ValueError("missing document entry")
    value = value.replace(entry, entry + extra, 1)
    if legend:
        before = {
            "direct": r"\ufcInputListing[language=C++]",
            "place": r"\begin{place}[here]",
            "ufcobject": r"\begin{ufcobject}[here]",
            "minipage": r"\begin{minipage}{\linewidth}",
        }[wrapper]
        value = value.replace(
            before,
            r"\legend{code}{CANDIDATE-CODE-LEGEND}" + "\n"
            + r"\ufcSource{CANDIDATE-SOURCE}" + "\n"
            + r"\label{cod:candidate-visual}" + "\n" + before,
            1,
        )
    return value


def run_candidate(real_runtime: bool = False) -> None:
    """Compile the experimental injection or the actual class implementation."""
    candidate_preflight()
    folder = BASE / ("runtime-pt" if real_runtime else "candidate-pt")
    folder.mkdir(parents=True, exist_ok=True)
    sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    results = []
    for profile, wrapper, legend in itertools.product(
        PROFILES, ("direct", "place", "ufcobject", "minipage"), (False, True)
    ):
        name = (("runtime-" if real_runtime else "candidate-")
                + ("article" if profile == PROFILES[0] else "capstone")
                + "-" + wrapper + ("-legend" if legend else "-plain"))
        source = folder / (name + ".tex")
        pdf = folder / (name + ".pdf")
        log = folder / (name + ".log")
        value = candidate_tex(profile, wrapper, legend)
        if real_runtime:
            # Test the class itself without any replacement macro in the input.
            injection = "\n".join(CANDIDATE_PATCH) + "\n"
            if value.count(injection) != 1:
                raise ValueError("missing candidate injection to remove")
            value = value.replace(injection, "", 1)
            if r"\RenewDocumentCommand \ufcInputListing" in value:
                raise ValueError("unintended runtime macro override")
        source.write_text(value, encoding="utf-8")
        process = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-jobname=" + name,
             "-output-directory=" + str(folder), str(source)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        outcome = process.stdout + "\n" + process.stderr
        valid = process.returncode == 0 and pdf.is_file()
        marker = ERROR_MARKER in outcome or (
            log.is_file() and ERROR_MARKER in log.read_text(errors="replace"))
        extracted = ""
        if valid:
            verify = subprocess.run(
                ["qpdf", "--check", str(pdf)], cwd=ROOT,
                capture_output=True, text=True, check=False,
            )
            if verify.returncode != 0:
                valid = False
            else:
                extracted = subprocess.run(
                    ["pdftotext", "-layout", str(pdf), "-"],
                    cwd=ROOT, capture_output=True, text=True, check=True,
                ).stdout
                if "main" not in extracted:
                    valid = False
                if legend and wrapper in ("place", "ufcobject"):
                    if "CANDIDATE-CODE-LEGEND" not in extracted or "CANDIDATE-SOURCE" not in extracted:
                        valid = False
        results.append({
            "name": name, "profile": profile, "wrapper": wrapper,
            "legend": legend, "valid_pdf_and_text": valid,
            "math_delimiter_error": bool(marker), "exit_code": process.returncode,
            "source_sha256": digest(source), "log_sha256": digest(log),
            "pdf_sha256": digest(pdf),
        })
        print(f"INPUTLISTING-{'RUNTIME' if real_runtime else 'CANDIDATE'} {name}"
              f" status={'PASS' if valid else 'FAIL'}"
              f" math_delim_error={bool(marker)}")
    result = {
        "source_sha": sha, "locale": "pt", "cases": len(results),
        "observations": results,
        "runtime_class_modified": real_runtime,
        "conclusion": ("DEVELOPMENT_RUNTIME_REGRESSION" if real_runtime
                       else "EXPERIMENTAL_CANDIDATE_ONLY"),
        "ledger_promotion": "NOT_AUTHORIZED",
        "publication_authorized": False,
    }
    (folder / ("runtime-manifest.json" if real_runtime else "candidate-manifest.json")).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if any(not x["valid_pdf_and_text"] for x in results):
        raise ValueError("import did not pass all real-PDF and text probes")
    label = "RUNTIME" if real_runtime else "CANDIDATE"
    print(f"I18N-INPUTLISTING-{label} status=PASS cases=16"
          f" real_pdfs=16 runtime_class_modified={str(real_runtime).lower()}"
          " publication_authorized=false")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--isolation", action="store_true")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--runtime", action="store_true")
    parser.add_argument("--locale", choices=tuple(LOCALES))
    args = parser.parse_args()
    try:
        preflight()
        isolation_preflight()
        candidate_preflight()
        if args.runtime and not args.preflight:
            run_candidate(real_runtime=True)
        elif args.candidate and not args.preflight:
            run_candidate()
        elif args.isolation and not args.preflight:
            run_isolation()
        elif args.locale and not args.preflight:
            run(args.locale)
        elif not args.preflight:
            raise ValueError("select --preflight, --isolation, --candidate, --runtime or --locale")
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        raise SystemExit(f"I18N-INPUTLISTING-REPRO status=FAIL reason={e}") from e

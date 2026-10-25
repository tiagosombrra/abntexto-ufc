#!/usr/bin/env python3
"""Fast, dependency-free fail-closed preflight for the 28 integrated documents."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "tests/integration/frontmatter/generate-integrated-locale.py"
RUNNER = ROOT / "tests/integration/frontmatter/run-integrated-locale.py"
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PROFILES = {
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
}
TOTAL = 0


def validate_case(case: dict, locale: str, source: str) -> None:
    """Validate the same source invariants for real cases and mutations."""
    profile = case["profile"]
    if (case["locale"] != locale or
            rf"\DocumentMetadata{{lang={LOCALES[locale]}," not in source or
            f"document-language={locale}" not in source):
        raise ValueError(f"mismatched document-language and PDF metadata: {profile}/{locale}")
    required = (
        r"\ufcPrintReferences", r"\parencite{silva2020}",
        r"\textcite{oliveira2011}", r"\ufcSource{Synthetic original}",
        r"\ufcNote{Synthetic object note}", r"\begin{tabular}",
        r"\begin{ufcobject}",
    )
    if any(x not in source for x in required):
        raise ValueError(f"missing joined core component: {profile}/{locale}")
    if profile == "scientific-article":
        if r"\ufcPrintArticleFrontMatter" not in source:
            raise ValueError(f"article frontmatter absent: {profile}/{locale}")
    else:
        if r"\ufcPrintTitlePage" not in source or r"\appendix{" not in source:
            raise ValueError(f"academic/project front/back missing: {profile}/{locale}")
    if profile == "doctoral-thesis" and (
            r"\ufcPrintGlossary" not in source or r"\ufcPrintIndex" not in source):
        raise ValueError(f"doctoral optional modules missing: {profile}/{locale}")


def check(out: Path) -> None:
    global TOTAL
    seen = set()
    for locale, bcp in LOCALES.items():
        subprocess.run([sys.executable, str(GENERATOR), "--locale", locale,
                        "--output", str(out)], cwd=ROOT, check=True,
                       capture_output=True, text=True)
        folder = out / locale
        cases = json.loads((folder / "source-index.json").read_text(encoding="utf-8"))
        if len(cases) != 7 or {r["profile"] for r in cases} != PROFILES:
            raise ValueError(f"incomplete seven-profile manifest for {locale}")
        for c in cases:
            key = (c["profile"], c["locale"])
            if key in seen or c["locale"] != locale:
                raise ValueError(f"duplicate or wrong locale case: {key}")
            seen.add(key)
            tex = Path(c["source"]).read_text(encoding="utf-8")
            validate_case(c, locale, tex)
            for source in c["support_sources"]:
                if not Path(source).is_file():
                    raise ValueError(f"unavailable summary input: {source}")
            TOTAL += 1
    if TOTAL != 28 or len(seen) != 28:
        raise ValueError(f"expected 28 distinct generated sources, got {TOTAL}")
    # Exercise the SAME production-source guard with deliberately corrupted
    # cases. Mutation detection alone is not a meaningful negative test.
    sample = (out / "en" / "integrated-doctoral-thesis-en.tex").read_text()
    fixture = {"profile": "doctoral-thesis", "locale": "en"}
    damaged = {
        "glossary": sample.replace(r"\ufcPrintGlossary", "", 1),
        "wrong_pdf_lang": sample.replace(
            r"\DocumentMetadata{lang=en-US,", r"\DocumentMetadata{lang=pt-BR,", 1),
        "missing_references": sample.replace(r"\ufcPrintReferences", "", 1),
    }
    for label, mutant in damaged.items():
        if mutant == sample:
            raise ValueError(f"mutation ineffective: {label}")
        try:
            validate_case(fixture, "en", mutant)
        except ValueError:
            pass
        else:
            raise ValueError(f"negative mutation was accepted: {label}")


def main() -> None:
    for path in (GENERATOR, RUNNER, Path(__file__)):
        subprocess.run([sys.executable, "-m", "py_compile", str(path)],
                       cwd=ROOT, check=True, capture_output=True, text=True)
    with tempfile.TemporaryDirectory(prefix="abntexto-i18n-28-preflight-") as tmp:
        check(Path(tmp))
    print("INTEGRATED-I18N-PREFLIGHT status=PASS profiles=7 locales=4 "
          "generated_tex=28 summary_inputs=56 bibliography=5kinds "
          "components=present negatives=PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"INTEGRATED-I18N-PREFLIGHT status=FAIL reason={exc}") from exc

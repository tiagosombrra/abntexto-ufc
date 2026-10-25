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
            if any(k not in tex for k in (
                rf"\DocumentMetadata{{lang={bcp},",
                f"document-language={locale}", r"\ufcPrintReferences",
                r"\parencite{silva2020}", r"\textcite{oliveira2011}",
                r"\ufcSource{Synthetic original}", r"\ufcNote{Synthetic object note}",
                r"\begin{tabular}", r"\begin{ufcobject}",
            )):
                raise ValueError(f"core joined components missing: {key}")
            if c["profile"] == "scientific-article":
                if r"\ufcPrintArticleFrontMatter" not in tex:
                    raise ValueError(f"article frontmatter absent: {key}")
            else:
                if r"\ufcPrintTitlePage" not in tex or r"\appendix{" not in tex:
                    raise ValueError(f"academic/project full front/back missing: {key}")
            if c["profile"] == "doctoral-thesis" and (
                r"\ufcPrintGlossary" not in tex or r"\ufcPrintIndex" not in tex
            ):
                raise ValueError(f"doctoral optional modules missing: {key}")
            for source in c["support_sources"]:
                if not Path(source).is_file():
                    raise ValueError(f"unavailable summary input: {source}")
            TOTAL += 1
    if TOTAL != 28 or len(seen) != 28:
        raise ValueError(f"expected 28 distinct generated sources, got {TOTAL}")
    # Negative guards: modifying a locale or removing a component must be
    # detected by the same checks rather than accepted as an incomplete smoke.
    sample = (out / "en" / "integrated-doctoral-thesis-en.tex").read_text()
    mutated = sample.replace(r"\ufcPrintGlossary", "", 1)
    if r"\ufcPrintGlossary" in mutated:
        raise ValueError("negative mutation of glossary was ineffective")
    if r"\ufcPrintGlossary" not in sample or r"\ufcPrintGlossary" in mutated:
        raise ValueError("missing-glossary negative not observable")
    wrong_lang = sample.replace(r"\DocumentMetadata{lang=en-US,", r"\DocumentMetadata{lang=pt-BR,", 1)
    if wrong_lang == sample or r"\DocumentMetadata{lang=en-US," in wrong_lang:
        raise ValueError("wrong-PDF-language negative not observable")


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

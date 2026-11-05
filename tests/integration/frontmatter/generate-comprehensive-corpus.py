#!/usr/bin/env python3
"""Generate 28 full-document *candidates*, never publication-ready PDFs.

Builds on the separately tested seven-profile frontmatter generator, expanding
each source into a multi-section authored manuscript. It intentionally exposes
pre-existing PDF metadata, table-list and duplex defects to the later auditor.
Passing source preflight is NOT actual-PDF or editorial certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[3]
# Repository-relative inputs avoid embedding runner-specific paths in TeX.
ARTIFACTS = Path("artifacts/comprehensive-7x4")
BASE = runpy.run_path(str(
    ROOT / "tests/integration/frontmatter/generate-integrated-locale.py"
))
PROFILES = BASE["PROFILES"]
LOCALES = tuple(BASE["LOCALES"])
MAKE_BASE_DOC = BASE["make_doc"]
DUPLEX_PROFILES = BASE["DUPLEX_PROFILES"]
PROSE = {
    "pt": (
        "Esta investigação sintética examina um sistema computacional reprodutível, "
        "com dados de entrada controlados e resultados que podem ser verificados. "
        "A análise separa a especificação dos algoritmos, a implementação e a "
        "avaliação experimental, evitando interpretações sem evidência.",
        "As tabelas apresentam observações artificiais para conferir a "
        "integridade da numeração, das fontes e da paginação. As figuras e os "
        "pseudocódigos documentam etapas complementares do processamento.",
    ),
    "en": (
        "This synthetic investigation examines a reproducible computing system "
        "with controlled input data and independently verifiable results. "
        "The analysis distinguishes algorithm specifications, implementation "
        "details and experimental evaluation, avoiding unsupported conclusions.",
        "Tables report artificial observations for checking numbering, source "
        "statements and page breaks. Figures and pseudocode document "
        "complementary stages of the computational workflow.",
    ),
    "es": (
        "Esta investigación sintética examina un sistema informático reproducible "
        "con datos de entrada controlados y resultados verificables de forma "
        "independiente. El análisis distingue la especificación algorítmica, "
        "la implementación y la evaluación experimental, sin conclusiones "
        "que carezcan de evidencia.",
        "Las tablas presentan observaciones artificiales para verificar la "
        "numeración, las fuentes y los saltos de página. Las figuras y los "
        "pseudocódigos documentan etapas complementarias del procesamiento.",
    ),
    "fr": (
        "Cette étude synthétique examine un système informatique reproductible "
        "à partir de données contrôlées et de résultats vérifiables. "
        "L'analyse distingue les spécifications algorithmiques, la mise en "
        "œuvre et l'évaluation expérimentale, sans conclusion non étayée.",
        "Les tableaux présentent des observations artificielles afin de "
        "vérifier la numérotation, les sources et les changements de page. "
        "Les figures et les pseudocodes décrivent des étapes complémentaires "
        "du traitement.",
    ),
}
TABLE_SOURCE = {"pt": "Fonte", "en": "Source", "es": "Fuente", "fr": "Source"}
INSTITUTION_DISPLAY = {
    "pt": "Universidade Federal do Ceará",
    "en": "Federal University of Ceará",
    "es": "Universidad Federal de Ceará",
    "fr": "Université fédérale du Ceará",
}
CODE_LANG = "C++"
SOURCE_FEATURES = (
    r"\subsection{", r"\subsubsection{", r"\paragraph{",
    r"\begin{equation}", r"\begin{align}", r"\footnote{",
    r"\begin{longabnttblr}", r"\begin{longtable}",
    r"\begin{ufcalgorithm}", r"\begin{ufclisting}", r"\ufcInputListing",
    r"\begin{ufcdefinitionlist}", r"\begin{ufclettereditems}",
    r"\ufcPrintReferences",
)


def sha(path: Path) -> str:
    """Hash the actual source bytes, not just a derived template name."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extra_body(profile: str, locale: str) -> str:
    """Add genuine authored content and documented optional public objects."""
    first, second = PROSE[locale]
    rows = [
        f"R4LONGROW{i:03d} & {i} " + "\\\\"
        for i in range(1, 126)
    ]
    native_rows = [
        f"R4NATIVEROW{i:03d} & {i} " + "\\\\"
        for i in range(1, 86)
    ]
    lines = [
        rf"\section{{R4-METHOD-{locale.upper()}}}",
        first,
        rf"\subsection{{R4-SUBSECTION-{locale.upper()}}}",
        second + r"\footnote{R4-FOOTNOTE synthetic and nonpersonal evidence.}",
        rf"\subsubsection{{R4-SUBSUBSECTION-{locale.upper()}}}",
        first,
        rf"\paragraph{{R4-PARAGRAPH-{locale.upper()}}}",
        second,
        rf"\subparagraph{{R4-SUBPARAGRAPH-{locale.upper()}}}",
        first,
        r"\begin{equation}\label{eq:r4-sum} S=\sum_{i=1}^{n}i=\frac{n(n+1)}{2}\end{equation}",
        r"\begin{align}a&=b+c\\b&=c+d\end{align}",
        r"Equation~\ref{eq:r4-sum} is an artificial reproducibility marker.",
        rf"\section{{R4-RESULTS-{locale.upper()}}}",
        second,
        rf"\legend{{figure}}{{R4-FIGURE-{locale.upper()}}}",
        r"\ufcSource{Synthetic original}",
        r"\begin{ufcobject}[here]",
        r"\centering\rule{6cm}{2cm}",
        r"\end{ufcobject}",
        rf"\legend{{table}}{{R4SHORT-{locale.upper()}}}",
        r"\ufcSource{Synthetic original}",
        r"\begin{ufcobject}[here]",
        r"\begin{tabular}{rr}",
        r"A & B \\",
        r"3 & 4 \\",
        r"\end{tabular}",
        r"\end{ufcobject}",
        r"\begin{longabnttblr}[",
        rf"  caption={{R4LONG-{locale.upper()} long numeric observations}},",
        rf"  label={{tab:r4-long-{locale}}},",
        rf"  remark{{{TABLE_SOURCE[locale]}}}={{R4-LONGSOURCE-{locale.upper()}}},",
        r"]{colspec={X[l] X[r]},rowhead=1,width=0.80\linewidth}",
        r"\toprule",
        r"R4LONGHEADER & R4LONGVALUE \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{longabnttblr}",
        r"\begin{longtable}{rr}",
        rf"\caption{{R4NATIVE-{locale.upper()} source caption}}\label{{tab:r4-native-{locale}}}\\",
        r"\hline",
        r"R4NATIVEHEADER & R4NATIVEVALUE \\",
        r"\hline",
        r"\endfirsthead",
        r"R4NATIVEHEADER & R4NATIVEVALUE \\",
        r"\endhead",
        *native_rows,
        r"\hline",
        r"\end{longtable}",
        rf"\section{{R4-IMPLEMENTATION-{locale.upper()}}}",
        first,
        rf"\legend{{code}}{{R4-INLINE-CODE-{locale.upper()}}}",
        r"\ufcSource{Synthetic original}",
        r"\begin{ufclisting}[here]",
        "int sum(int a, int b) {",
        "    return a + b;",
        "}",
        r"\end{ufclisting}",
        rf"\legend{{code}}{{R4-EXTERNAL-CODE-{locale.upper()}}}",
        r"\ufcSource{Synthetic original}",
        r"\begin{ufcobject}[here]",
        rf"\ufcInputListing[language={CODE_LANG}]{{tests/fixtures/example.cpp}}",
        r"\end{ufcobject}",
        rf"\legend{{algorithm}}{{R4-ALGORITHM-{locale.upper()}}}",
        r"\ufcSource{Synthetic original}",
        r"\begin{ufcalgorithm}[here][1]",
        r"\State $i \gets 1$",
        r"\While{$i \leq n$}",
        r"  \If{$A[i]=x$}",
        r"    \State \Return $i$",
        r"  \EndIf",
        r"  \State $i \gets i+1$",
        r"\EndWhile",
        r"\State \Return $-1$",
        r"\end{ufcalgorithm}",
    ]
    if profile in {"undergraduate-capstone", "specialization-capstone",
                   "masters-thesis", "doctoral-thesis"}:
        lines += [
            rf"\legend{{grafico}}{{R4-CHART-{locale.upper()}}}",
            r"\ufcSource{Synthetic original}",
            r"\begin{ufcobject}[here]",
            r"\centering\rule{5cm}{1.5cm}",
            r"\end{ufcobject}",
            rf"\legend{{quadro}}{{R4-TEXTTABLE-{locale.upper()}}}",
            r"\ufcSource{Synthetic original}",
            r"\begin{ufcobject}[here]",
            r"\centering\rule{5cm}{1.5cm}",
            r"\end{ufcobject}",
        ]
    # Multiple actual paragraphs demonstrate widow/orphan and line spacing.
    for i in range(1, 7):
        lines += [rf"\subsection{{R4-REPLICATION-{locale.upper()}-{i}}}",
                  first, second, first, second]
    lines += [rf"\section{{R4-DISCUSSION-{locale.upper()}}}", first, second]
    return "\n".join(lines) + "\n"


def generate(profile: str, locale: str, folder: Path) -> dict:
    """Expand one proven base specimen into a complete, independently hashed source."""
    name, sources = MAKE_BASE_DOC(profile, locale, folder)
    original = Path(sources[0]).read_text(encoding="utf-8")
    if original.split(r"\begin{document}", 1)[0].count(r"\ufcsetup{" + "\n") != 1:
        raise ValueError("source lost its uniquely addressable class setup")
    source = original.replace(
        "\\ufcsetup{\n",
        "\\ufcsetup{\n  tables=tabularray,\n  code=listings,\n"
        "  algorithms=algpseudocodex,\n"
        f"  institution-display={{{INSTITUTION_DISPLAY[locale]}}},\n"
        f"  submission-entity-display={{{INSTITUTION_DISPLAY[locale]}}},\n",
        1,
    )
    source = source.replace(
        "\\documentclass{abntexto-ufc}\n",
        "\\documentclass{abntexto-ufc}\n\\usepackage{amsmath}\n"
        "\\usepackage{longtable}\n", 1,
    )
    if profile != "scientific-article":
        token = r"\ufcPrintTableOfContents"
        if source.count(token) != 1:
            raise ValueError("missing source frontmatter insertion anchor")
        source = source.replace(
            token, r"\ufcPrintListOfCodeListings" + "\n"
            + r"\ufcPrintListOfAlgorithms" + "\n" + token, 1,
        )
    token = r"\ufcPrintReferences"
    if source.count(token) != 1:
        raise ValueError("missing bibliography insertion anchor")
    source = source.replace(token, extra_body(profile, locale) + token, 1)
    missing = [feature for feature in SOURCE_FEATURES if feature not in source]
    if missing:
        raise ValueError(f"incomplete R4 manuscript {profile}/{locale}: {missing}")
    variants = []
    if profile == "doctoral-thesis":
        # The native pdfLaTeX write-stream budget cannot hold every pretextual
        # list simultaneously with glossaries and imakeidx. Preserve the main
        # doctorate's glossary/index, and exercise both code/algorithm lists
        # in a separately hashed supplementary doctorate without those modules.
        variant_source = source.replace("glossary=glossaries", "glossary=none", 1)
        variant_source = variant_source.replace("index=imakeidx", "index=none", 1)
        variant_source = variant_source.replace(
            r"\newglossaryentry{integratedterm}{name={integrated term},description={synthetic term for locale testing}}" + "\n",
            "", 1,
        ).replace(r"\gls{integratedterm}\index{integrated term}", "", 1)
        variant_source = variant_source.replace(r"\ufcPrintGlossary", "", 1)
        variant_source = variant_source.replace(r"\ufcPrintIndex", "", 1)
        if (variant_source == source or "glossary=glossaries" in variant_source
                or "index=imakeidx" in variant_source):
            raise ValueError("doctoral supplementary feature split was ineffective")
        variant_name = f"comprehensive-doctoral-code-lists-{locale}"
        variant_path = folder / f"{variant_name}.tex"
        variant_path.write_text(variant_source, encoding="utf-8")
        variants.append({
            "name": variant_name, "profile": profile, "locale": locale,
            "source": str(variant_path), "source_sha256": sha(variant_path),
            "support_sources": sources[1:],
            "support_sha256": {str(p): sha(Path(p)) for p in sources[1:]},
            "glossary_enabled": False, "index_enabled": False,
            "code_algorithm_lists_printed": True,
            "proof_state": "SOURCE_PREFLIGHT_ONLY",
        })
        list_commands = (r"\ufcPrintListOfCodeListings" + "\n"
                         + r"\ufcPrintListOfAlgorithms" + "\n")
        if source.count(list_commands) != 1:
            raise ValueError("expected one doctoral optional-list pair")
        source = source.replace(list_commands, "", 1)
    fname = f"comprehensive-{profile}-{locale}"
    target = folder / f"{fname}.tex"
    target.write_text(source, encoding="utf-8")
    return {
        "name": fname, "profile": profile, "locale": locale,
        "expected_institution_display": INSTITUTION_DISPLAY[locale],
        "source": str(target), "source_sha256": sha(target),
        "support_sources": sources[1:],
        "support_sha256": {str(p): sha(Path(p)) for p in sources[1:]},
        "supplementary_variants": variants,
        "glossary_enabled": profile == "doctoral-thesis",
        "index_enabled": profile == "doctoral-thesis",
        "code_algorithm_lists_printed": profile not in {"doctoral-thesis", "scientific-article"},
        "features": {
            "multi_section": True, "subsection": True, "subsubsection": True,
            "footnotes": True, "equations": True, "aligned_equations": True,
            "short_table": True, "tabularray_multipage": True,
            "native_longtable": True, "algorithm": True,
            "inline_code": True, "external_code": True,
            "bibliography": True, "figure": True, "lists": True,
            "glossary": profile == "doctoral-thesis",
            "index": profile == "doctoral-thesis",
            "approval_page": profile in {
                "undergraduate-capstone", "specialization-capstone",
                "masters-thesis", "doctoral-thesis"},
            "article_specific_frontmatter": profile == "scientific-article",
            "anonymous_title": profile == "anonymized-research-project",
            "duplex": profile in DUPLEX_PROFILES,
        },
        "proof_state": "SOURCE_PREFLIGHT_ONLY",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=LOCALES)
    parser.add_argument("--output", type=Path, default=ARTIFACTS)
    args = parser.parse_args()
    locales = (args.locale,) if args.locale else LOCALES
    tally = 0
    for locale in locales:
        folder = args.output / locale
        folder.mkdir(parents=True, exist_ok=True)
        manifest = [generate(profile, locale, folder) for profile in PROFILES]
        if len(manifest) != 7 or len({x["profile"] for x in manifest}) != 7:
            raise ValueError("incomplete seven-profile R4 source matrix")
        path = folder / "source-index.json"
        path.write_text(json.dumps({
            "locale": locale, "source_count": len(manifest),
            "complete_pdf_certification": False, "entries": manifest,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tally += len(manifest) + sum(len(entry["supplementary_variants"]) for entry in manifest)
    print(f"R4-COMPREHENSIVE-SOURCES status=PASS sources={tally} "
          f"locales={','.join(locales)} pdf_certification=NOT_YET")
 

if __name__ == "__main__":
    main()

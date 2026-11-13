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
import subprocess
import sys

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
    "en": "Federal University of Ceara",
    "es": "Universidad Federal de Ceará",
    "fr": "Université fédérale du Ceará",
}
CODE_LANG = "C++"
STUDY_DIR = ROOT / "examples" / "canonical-mesh-study"
STUDY_FILE = STUDY_DIR / "study.json"
CONTEXT_FILE = STUDY_DIR / "profile-contexts.json"
FIGURE_OUTPUT = ROOT / "artifacts" / "canonical-mesh-study"
PROFILE_CONTEXTS = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))["profile_context"]
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
    specific = PROFILE_CONTEXTS[profile][locale]
    if len(specific) < 120:
        raise ValueError(f"Missing substantive profile-specific source: {profile}/{locale}")
    rows = [
        f"R4LONGROW{i:03d} & {i} " + "\\\\"
        for i in range(1, 126)
    ]
    native_rows = [
        f"R4NATIVEROW{i:03d} & {i} " + "\\\\"
        for i in range(1, 86)
    ]
    # Keep the final two native longtable rows together to avoid a
    # language-sensitive page containing only the repeated header and row 85.
    # Native longtable owns its page breaks; the shared class need not change.
    native_rows.insert(-1, r"\nopagebreak[4]")

    lines = [
        rf"\section{{R4-METHOD-{locale.upper()}}}",
        first,
        # One source-bound scientific method/figure/table section across types,
        # but a distinct genre-specific discussion for each academic profile.
        rf"\input{{artifacts/canonical-mesh-study/body-{locale}.tex}}",
        specific,
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



ACADEMIC_PROFILES_WITH_DEDICATION = {
    "undergraduate-capstone", "specialization-capstone",
    "masters-thesis", "doctoral-thesis",
}
DEDICATION_TEXT = {
    "pt": "Dedico este documento de ensaio à verificação rigorosa da estrutura acadêmica.",
    "en": "I dedicate this test document to rigorous verification of academic structure.",
    "es": "Dedico este documento de prueba a la verificación rigurosa de la estructura académica.",
    "fr": "Je dédie ce document de test à la vérification rigoureuse de la structure universitaire.",
}
EPIGRAPH_TEXT = {
    "pt": "Uma afirmação só se sustenta quando suas evidências podem ser examinadas.",
    "en": "A claim is only as reliable as the evidence that can be examined.",
    "es": "Una afirmación solo es fiable cuando sus pruebas pueden examinarse.",
    "fr": "Une affirmation n'est fiable que si ses preuves peuvent être examinées.",
}


def add_human_review_pretextual_elements(source: str, profile: str,
                                          locale: str, folder: Path,
                                          sources: list) -> str:
    """Exercise dedication and epigraph in applicable academic document types.

    The epigraph's long and short forms must be tested across the corpus
    without adding two epigraphs to a single scholarly manuscript.
    """
    if profile not in ACADEMIC_PROFILES_WITH_DEDICATION:
        return source

    text_dir = folder / "texts"
    text_dir.mkdir(parents=True, exist_ok=True)
    stem = f"r5-review-{profile}-{locale}"
    dedication = text_dir / f"{stem}-dedication.tex"
    epigraph = text_dir / f"{stem}-epigraph.tex"
    dedication.write_text(
        f"R5-DEDICATION-{locale.upper()}-{profile.upper()}. "
        + DEDICATION_TEXT[locale] + "\n", encoding="utf-8"
    )
    epigraph.write_text(
        f"R5-EPIGRAPH-{locale.upper()}-{profile.upper()}. "
        + EPIGRAPH_TEXT[locale] + "\n", encoding="utf-8"
    )
    sources.extend([str(dedication), str(epigraph)])

    # Restore normative frontmatter order: errata, approval, dedication,
    # acknowledgments, epigraph, followed by summaries.
    lines = source.splitlines(keepends=True)
    approval = r"\ufcPrintApprovalPage" + "\n"
    approvals = [i for i, line in enumerate(lines) if line == approval]
    if len(approvals) != 1:
        raise ValueError(f"{profile}/{locale}: approval page anchor missing")
    n = approvals[0]
    if n < 2 or not lines[n-2].startswith(r"\ufcPrintAcknowledgments{") or \
            not lines[n-1].startswith(r"\ufcPrintErrata{"):
        raise ValueError(f"{profile}/{locale}: unexpected frontmatter order")
    acknowledgment, errata = lines[n-2:n]
    mode = "long" if profile == "doctoral-thesis" else "short"
    replacement = [
        errata, approval,
        rf"\ufcPrintDedication{{{dedication.as_posix()}}}" + "\n",
        acknowledgment,
        rf"\ufcPrintEpigraph[{mode}]{{{epigraph.as_posix()}}}" + "\n",
    ]
    lines[n-2:n+1] = replacement
    result = "".join(lines)
    assert result.count(r"\ufcPrintDedication{") == 1
    assert result.count(r"\ufcPrintEpigraph[") == 1
    return result


def generate(profile: str, locale: str, folder: Path) -> dict:
    """Expand one proven base specimen into a complete, independently hashed source."""
    name, sources = MAKE_BASE_DOC(profile, locale, folder)
    original = Path(sources[0]).read_text(encoding="utf-8")
    if original.split(r"\begin{document}", 1)[0].count(r"\ufcsetup{" + "\n") != 1:
        raise ValueError("source lost its uniquely addressable class setup")
    if original.count("institution-display={" + INSTITUTION_DISPLAY[locale] + "}") != 1:
        raise ValueError("R2 source omitted unique localized institution presentation")
    if original.count("submission-entity-display={" + INSTITUTION_DISPLAY[locale] + "}") != 1:
        raise ValueError("R2 source omitted unique localized project entity presentation")
    source = add_human_review_pretextual_elements(
        original, profile, locale, folder, sources
    )
    source = source.replace(
        "\\ufcsetup{\n",
        "\\ufcsetup{\n  tables=tabularray,\n  code=listings,\n"
        "  algorithms=algpseudocodex,\n",
        1,
    )
    source = source.replace(
        "\\documentclass{abntexto-ufc}\n",
        "\\documentclass{abntexto-ufc}\n\\usepackage{amsmath}\n"
        "\\usepackage{longtable}\n\\usepackage{graphicx}\n", 1,
    )
    canonical_bib = r"\ufcAddBibliographyResource{tests/fixtures/references.bib}"
    if source.count(canonical_bib) != 1:
        raise ValueError("Missing unique bibliography resource anchor")
    source = source.replace(
        canonical_bib,
        canonical_bib + "\n"
        + r"\ufcAddBibliographyResource{examples/canonical-mesh-study/references.bib}",
        1,
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
    for required in (
        rf"\input{{artifacts/canonical-mesh-study/body-{locale}.tex}}",
        r"\ufcAddBibliographyResource{examples/canonical-mesh-study/references.bib}",
        PROFILE_CONTEXTS[profile][locale],
    ):
        if required not in source:
            raise ValueError(f"Missing verified scientific case: {profile}/{locale}")
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
            "canonical_study_id": "unit-square-structured-mesh-v1",
            "canonical_study_sha256": sha(STUDY_FILE),
            "profile_context_sha256": sha(CONTEXT_FILE),
            "generated_asset_manifest_sha256": sha(FIGURE_OUTPUT / "manifest.json"),
            "scientific_content_state": "verified_didactic_geometry_not_novel_research",
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
        "canonical_study_id": "unit-square-structured-mesh-v1",
        "canonical_study_sha256": sha(STUDY_FILE),
        "profile_context_sha256": sha(CONTEXT_FILE),
        "generated_asset_manifest_sha256": sha(FIGURE_OUTPUT / "manifest.json"),
        "scientific_content_state": "verified_didactic_geometry_not_novel_research",
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
            "dedication": profile in ACADEMIC_PROFILES_WITH_DEDICATION,
            "epigraph_short": profile in ACADEMIC_PROFILES_WITH_DEDICATION
            and profile != "doctoral-thesis",
            "epigraph_long": profile == "doctoral-thesis",
            "pretextual_order_repaired": profile in ACADEMIC_PROFILES_WITH_DEDICATION,
            "duplex": profile in DUPLEX_PROFILES,
        },
        "proof_state": "SOURCE_PREFLIGHT_ONLY",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=LOCALES)
    parser.add_argument("--output", type=Path, default=ARTIFACTS)
    args = parser.parse_args()
    # Build original vector figures, CSV and multilingual excerpts exactly
    # once before authoring all seven profiles; each R4 job verifies hashes.
    generator = ROOT / "tools" / "examples" / "generate_mesh_study.py"
    subprocess.run([sys.executable, str(generator), "--output", str(FIGURE_OUTPUT)],
                   cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(generator), "--check",
                    "--output", str(FIGURE_OUTPUT)], cwd=ROOT, check=True)
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

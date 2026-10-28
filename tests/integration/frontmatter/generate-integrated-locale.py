#!/usr/bin/env python3
"""Generate source-bound 7-profile/4-language *integrated* TeX evidence.

This is a bounded real-PDF integration test, not automatic translation of
author text or institutional approval. It deliberately uses synthetic content.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from integrated_metadata_probe import source_lines as metadata_probe_lines

PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
USER_DATES = {
    "pt": "21 de outubro de 2026",
    "en": "21 October 2026",
    "es": "21 de octubre de 2026",
    "fr": "21 octobre 2026",
}
PROJECTS = {"research-project", "anonymized-research-project"}
ACADEMIC_PROFILES = {
    "undergraduate-capstone", "specialization-capstone",
    "masters-thesis", "doctoral-thesis",
}
# Progressively exercise examiner slots 3..6 and compact-signature spacing
# at four, five, six and seven real committee signatures, respectively.
APPROVAL_LAST_EXAMINER = {
    "undergraduate-capstone": 3,
    "specialization-capstone": 4,
    "masters-thesis": 5,
    "doctoral-thesis": 6,
}
# Every academic profile is one of four flag combinations in each locale.
# The two projects also exercise metadata; the anonymized one must hide it.
ROLE_GENDERS = {
    "undergraduate-capstone": (False, False),
    "specialization-capstone": (True, False),
    "masters-thesis": (False, True),
    "doctoral-thesis": (True, True),
    "research-project": (True, True),
    "anonymized-research-project": (True, True),
    "scientific-article": (False, False),
}
DUPLEX_PROFILES = {
    "masters-thesis", "doctoral-thesis", "anonymized-research-project",
}


def routing_probe(command: str, category: str, locale: str) -> str:
    """Exercise both public branch operands in an actual TeX manuscript."""
    tag = locale.upper()
    return (
        "\\" + command
        + "{INTEGRATED-" + category + "-TRUE-" + tag
        + r". \typeout{INTEGRATED-I18N-" + category + "=TRUE}}"
        + "{INTEGRATED-" + category + "-FALSE-" + tag
        + r". \typeout{INTEGRATED-I18N-" + category + "=FALSE}}\par"
    )


def summary_text(locale: str, label: str) -> str:
    # Both historical helpers must localize *to this summary*, even when it is
    # the secondary/companion language of the primary manuscript.
    return (
        f"INTEGRATED-SUMMARY-{locale.upper()}-{label.upper()}. "
        rf"\ufcSummaryKeywords{{keyword-{locale}-{label}.}}" + "\n"
    )


def make_doc(profile: str, locale: str, target: Path) -> tuple[str, list[str]]:
    bcp = LOCALES[locale]
    # LaTeX text mode rejects raw underscore characters: keep fixture markers
    # printable, without requiring \texttt or math mode.
    code = profile.replace("-", "")
    name = f"integrated-{profile}-{locale}"
    companion = "en" if locale == "pt" else "pt"
    support = target / "texts"
    support.mkdir(parents=True, exist_ok=True)
    extra_sources: list[str] = []
    (support / (name + "-primary.tex")).write_text(
        summary_text(locale, "main"), encoding="utf-8",
    )
    (support / (name + "-secondary.tex")).write_text(
        summary_text(companion, "companion"), encoding="utf-8",
    )
    date = USER_DATES[locale]
    options = {
        "type": profile,
        "document-language": locale,
        "print-mode": "double-sided" if profile in DUPLEX_PROFILES else "single-sided",
        "cover": "false" if profile == "scientific-article" else "true",
        "coat-of-arms": "false",
        "catalog-card": "false",
        "author": "{Integrated Test Author}",
        "title": "{Integrated Multilingual Document}",
        "institution": "{Universidade Federal do Ceará}",
        "location": "{Fortaleza}",
        "year": "{2026}",
        "approval-date": "{" + date + "}",
        "submission-date": "{" + date + "}",
        "article-author-note": "{Synthetic Test Author Note}",
        "advisor": "{Integrated Advisor}",
        "coadvisor": "{Integrated Coadvisor}",
        "advisor-feminine-label": (
            "true" if ROLE_GENDERS[profile][0] else "false"
        ),
        "coadvisor-feminine-label": (
            "true" if ROLE_GENDERS[profile][1] else "false"
        ),
         "undergraduate-program": "{Computing}",
        "undergraduate-degree": "{Bachelor}",
        "specialization-program": "{Specialization in Computing}",
        "masters-graduate-program": "{Graduate Program in Computing}",
        "masters-program": "{Master of Computing}",
        "masters-degree-field": "{Computer Science}",
        "doctoral-graduate-program": "{Graduate Program in Computing}",
        "doctoral-program": "{Doctoral Program in Computing}",
        "doctoral-degree-field": "{Computer Science}",
        "project-program": "{Graduate Selection}",
        "project-identifier": "{SYNTHETIC-ANON-001}",
        "submission-entity": "{Universidade Federal do Ceará}",
    }
    if profile in ACADEMIC_PROFILES:
        for slot in range(2, APPROVAL_LAST_EXAMINER[profile] + 1):
            options[f"examiner-{slot}"] = f"{{Integrated Examiner {slot}}}"
            options[f"examiner-{slot}-institution"] = f"{{Integrated Institution {slot}}}"
            # Metadata-only unit fields are intentionally not displayed on the
            # approval page; PDF assertions must prove that they stay hidden.
            options[f"examiner-{slot}-unit"] = f"{{Integrated Hidden Unit {slot}}}"
    # Only the doctoral profile exercises the optional glossary/index paths
    # (4 real language tests); remaining profiles do not invent requirements.
    if profile == "doctoral-thesis":
        options["glossary"] = "glossaries"
        options["index"] = "imakeidx"
    setup = ",\n  ".join(f"{k}={v}" for k, v in options.items())
    lines = [
        rf"\DocumentMetadata{{lang={bcp},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\ufcsetup{",
        f"  {setup}",
        "}",
        r"\ufcAddBibliographyResource{tests/fixtures/references.bib}",
        r"\ufcAddBibliographyResource{tests/fixtures/i18n-jurisdiction.bib}",
    ]
    if profile == "doctoral-thesis":
        lines += [
            r"\newglossaryentry{integratedterm}{name={integrated term},description={synthetic term for locale testing}}",
        ]
    lines += [r"\begin{document}"]
    if profile == "scientific-article":
        lines += [
            rf"\ufcPrintArticleFrontMatter{{INTEGRATED-ARTICLE-PRIMARY-{locale.upper()}. "
            rf"\ufcSummaryKeywordsInLanguage{{{locale}}}{{keyword-{locale}-article.}}}}",
            rf"\ufcPrintArticleTranslatedSummary{{{companion}}}"
            rf"{{INTEGRATED-ARTICLE-COMPANION-{companion.upper()}. "
            rf"\ufcSummaryKeywordsInLanguage{{{companion}}}{{keyword-{companion}-article.}}}}",
        ]
    else:
        lines += [r"\pretextual", r"\ufcPrintCover", r"\ufcPrintTitlePage"]
        if profile in ACADEMIC_PROFILES:
            # Author-supplied text is synthetic and must never be translated
            # by the class. Only the public command headings are localized.
            extras = {
                "ack": f"INTEGRATED-AUTHORED-GRATITUDE-{locale.upper()}.",
                "errata": f"INTEGRATED-AUTHORED-CORRECTIONS-{locale.upper()}.",
                "abbreviations": (
                    "\\begin{ufcdefinitionlist}\n"
                    f"\\ufcListEntry{{IAA-{locale.upper()}}}"
                    f"{{INTEGRATED-ABBREVIATION-{locale.upper()}.}}\n"
                    "\\end{ufcdefinitionlist}"
                ),
                "symbols": (
                    "\\begin{ufcdefinitionlist}\n"
                    f"\\ufcListEntry{{IAS-{locale.upper()}}}"
                    f"{{INTEGRATED-SYMBOL-{locale.upper()}.}}\n"
                    "\\end{ufcdefinitionlist}"
                ),
            }
            for suffix, text in extras.items():
                source = support / f"{name}-{suffix}.tex"
                source.write_text(text + "\n", encoding="utf-8")
                extra_sources.append(str(source))
            lines += [
                rf"\ufcPrintAcknowledgments{{{support / (name + '-ack.tex')}}}",
                rf"\ufcPrintErrata{{{support / (name + '-errata.tex')}}}",
            ]
        if profile not in PROJECTS:
            lines += [
                r"\ufcPrintApprovalPage",
                rf"\ufcPrintRequiredSummaries"
                rf"{{{support / (name + '-primary.tex')}}}"
                rf"{{{support / (name + '-secondary.tex')}}}",
            ]
        lines += [r"\ufcPrintListOfFigures", r"\ufcPrintListOfTables"]
        if profile in ACADEMIC_PROFILES:
            lines += [
                r"\ufcPrintListOfIllustrations",
                r"\ufcPrintListOfTextTables",
                r"\ufcPrintListOfCharts",
                rf"\ufcPrintListOfAbbreviationsAndAcronyms{{{support / (name + '-abbreviations.tex')}}}",
                rf"\ufcPrintListOfSymbols{{{support / (name + '-symbols.tex')}}}",
            ]
        lines.append(r"\ufcPrintTableOfContents")
    lines += [
        rf"\typeout{{INTEGRATED-I18N-BABEL=\languagename}}",
        r"\typeout{INTEGRATED-I18N-API-LANGUAGE=\ufcDocumentLanguage}",
        r"\typeout{INTEGRATED-I18N-API-TYPE=\ufcDocumentType}",
        r"\typeout{INTEGRATED-I18N-API-PRINT-MODE=\ufcPrintMode}",
        r"\typeout{INTEGRATED-I18N-API-META-TITLE=\ufcMeta{title}}",
        r"\textual",
        rf"\section{{INTEGRATED-SECTION-{locale.upper()}}}",
        rf"INTEGRATED-MANUSCRIPT-{locale.upper()}-{code.upper()}.",
        routing_probe("ufcIfProjectTF", "PROJECT", locale),
        routing_probe("ufcIfAnonymizedProjectTF", "ANON", locale),
        r"\begin{ufclettereditems}",
        rf"\item INTEGRATED-LETTER-{locale.upper()}.",
        r"\item INTEGRATED-NESTED-LIST:",
        r"\begin{ufcdashedsubitems}",
        rf"\item INTEGRATED-DASH-{locale.upper()}.",
        r"\end{ufcdashedsubitems}",
        r"\end{ufclettereditems}",
        r"\begin{ufcdefinitionlist}[3cm]",
        rf"\ufcListEntry{{INTEGRATED-TERM-{locale.upper()}}}{{INTEGRATED-DEFINITION-{locale.upper()}.}}",
        r"\end{ufcdefinitionlist}",
        r"See synthetic sources \parencite{silva2020} and \textcite{oliveira2011}.",
        r"\nocite{tribunal2011,evento2025,ufc-jurisdiction-date}",
        rf"\legend{{figure}}{{INTEGRATED-OBJECT-{locale.upper()}}}",
        r"\ufcSource{Synthetic original}",
        r"\ufcNote{Synthetic object note}",
        r"\begin{ufcobject}[here]",
        r"\centering\rule{3cm}{1cm}",
        r"\end{ufcobject}",
        r"\begin{table}[h]",
        r"\centering",
        rf"\caption{{INTEGRATED-TABLE-{locale.upper()}}}",
        r"\begin{tabular}{cc} 1 & 2 \\ 3 & 4 \end{tabular}",
        r"\end{table}",
    ]
    if profile in ACADEMIC_PROFILES:
        # Populate the chart and text-table list files with real objects.
        lines += [
            rf"\legend{{grafico}}{{INTEGRATED-CHART-{locale.upper()}}}",
            r"\ufcSource{Synthetic original}",
            r"\begin{ufcobject}[here]",
            r"\centering\rule{3cm}{1cm}",
            r"\end{ufcobject}",
            rf"\legend{{quadro}}{{INTEGRATED-TEXTTABLE-{locale.upper()}}}",
            r"\ufcSource{Synthetic original}",
            r"\begin{ufcobject}[here]",
            r"\centering\rule{3cm}{1cm}",
            r"\end{ufcobject}",
        ]
    if profile == "doctoral-thesis":
        lines += [
            r"\gls{integratedterm}\index{integrated term}",
        ]
    lines += [
        r"\ufcPrintReferences",
    ]
    if profile == "doctoral-thesis":
        lines += [r"\ufcPrintGlossary"]
    if profile != "scientific-article":
        lines += [
            rf"\appendix{{INTEGRATED-APPENDIX-{locale.upper()}}}",
            rf"INTEGRATED-APPENDIX-BODY-{locale.upper()}.",
            rf"\annex{{INTEGRATED-ANNEX-{locale.upper()}}}",
            rf"INTEGRATED-ANNEX-BODY-{locale.upper()}.",
        ]
    if profile == "doctoral-thesis":
        lines += [r"\ufcPrintIndex"]
    # Probe all 52 metadata-backed authored/default values after every typeset page, without
    # changing existing labels, anonymization, bibliography or title pages.
    lines += metadata_probe_lines()
    lines += [r"\end{document}"]
    result = "\n".join(lines) + "\n"
    path = target / f"{name}.tex"
    path.write_text(result, encoding="utf-8")
    return name, [str(path), str(support / (name + "-primary.tex")),
                  str(support / (name + "-secondary.tex")), *extra_sources]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True, choices=tuple(LOCALES))
    parser.add_argument("--output", type=Path, default=Path("artifacts/integrated-i18n"))
    args = parser.parse_args()
    folder = args.output / args.locale
    folder.mkdir(parents=True, exist_ok=True)
    manifest = []
    for profile in PROFILES:
        name, sources = make_doc(profile, args.locale, folder)
        manifest.append({"profile": profile, "locale": args.locale, "name": name,
                         "source": sources[0], "support_sources": sources[1:]})
    (folder / "source-index.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"INTEGRATED-I18N-GENERATOR status=PASS locale={args.locale} real_tex={len(manifest)}")


if __name__ == "__main__":
    main()

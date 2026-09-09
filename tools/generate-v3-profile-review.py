#!/usr/bin/env python3
"""Generate deterministic source files for v3.0.0 all-profile visual review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent

RELEASED_SOURCE_SHA = "05399473827da7cf6b6c8bac36edc7115481773f"
RELEASE_TAG = "v3.0.0"

PROFILES = [
    {
        "id": "undergraduate-capstone",
        "label": "TCC de graduação",
        "kind": "academic",
        "metadata": dedent(r"""
          center = {Centro de Ciências},
          department = {Departamento de Computação},
          undergraduate-program = {Ciência da Computação},
          undergraduate-degree = {bacharel},
        """).strip(),
        "title": "Exemplo de Trabalho de Conclusão de Curso",
        "subtitle": "Validação visual do perfil de graduação",
    },
    {
        "id": "specialization-capstone",
        "label": "TCC de especialização",
        "kind": "academic",
        "metadata": dedent(r"""
          center = {Centro de Ciências},
          department = {Departamento de Computação},
          specialization-program = {Engenharia de Software},
        """).strip(),
        "title": "Exemplo de Trabalho de Conclusão de Especialização",
        "subtitle": "Validação visual do perfil de especialização",
    },
    {
        "id": "masters-thesis",
        "label": "Dissertação de mestrado",
        "kind": "academic",
        "metadata": dedent(r"""
          center = {Centro de Ciências},
          masters-graduate-program = {Programa de Pós-Graduação em Ciência da Computação},
          masters-program = {Mestrado Acadêmico em Ciência da Computação},
          masters-degree-field = {Ciência da Computação},
          masters-concentration = {Computação Gráfica},
        """).strip(),
        "title": "Exemplo de Dissertação de Mestrado",
        "subtitle": "Validação visual do perfil de mestrado",
    },
    {
        "id": "doctoral-thesis",
        "label": "Tese de doutorado",
        "kind": "academic",
        "metadata": dedent(r"""
          center = {Centro de Ciências},
          doctoral-graduate-program = {Programa de Pós-Graduação em Ciência da Computação},
          doctoral-program = {Doutorado em Ciência da Computação},
          doctoral-degree-field = {Ciência da Computação},
          doctoral-concentration = {Computação Gráfica},
        """).strip(),
        "title": "Exemplo de Tese de Doutorado",
        "subtitle": "Validação visual do perfil de doutorado",
    },
    {
        "id": "research-project",
        "label": "Projeto de pesquisa",
        "kind": "project",
        "metadata": dedent(r"""
          center = {Centro de Ciências},
          department = {Departamento de Computação},
          project-program = {Programa de Pós-Graduação em Ciência da Computação},
          project-type = {Projeto de pesquisa},
          submission-entity = {Universidade Federal do Ceará},
          project-nature-statement = {Projeto de pesquisa apresentado ao Programa de Pós-Graduação em Ciência da Computação da Universidade Federal do Ceará.},
          project-identifier = {PROJETO-2026-001},
        """).strip(),
        "title": "Exemplo de Projeto de Pesquisa",
        "subtitle": "Validação visual do perfil identificado",
    },
    {
        "id": "anonymized-research-project",
        "label": "Projeto de pesquisa anonimizado",
        "kind": "project-anonymized",
        "metadata": dedent(r"""
          center = {Centro de Ciências},
          department = {Departamento de Computação},
          project-program = {Programa de Pós-Graduação em Ciência da Computação},
          project-type = {Projeto de pesquisa},
          submission-entity = {Universidade Federal do Ceará},
          project-nature-statement = {Projeto de pesquisa anonimizado para avaliação cega no Programa de Pós-Graduação em Ciência da Computação da Universidade Federal do Ceará.},
          project-identifier = {PROJETO-ANON-2026-001},
        """).strip(),
        "title": "Exemplo de Projeto de Pesquisa Anonimizado",
        "subtitle": "Validação visual da ocultação de identidade",
    },
    {
        "id": "scientific-article",
        "label": "Artigo científico",
        "kind": "article",
        "metadata": "",
        "title": "Exemplo de Artigo Científico",
        "subtitle": "",
    },
]

BIBLIOGRAPHY = dedent(r"""
@book{lamport1994,
  author    = {Leslie Lamport},
  title     = {LaTeX: A Document Preparation System},
  edition   = {2},
  publisher = {Addison-Wesley},
  location  = {Reading, MA},
  year      = {1994}
}

@book{knuth1984,
  author    = {Donald E. Knuth},
  title     = {The TeXbook},
  publisher = {Addison-Wesley},
  location  = {Reading, MA},
  year      = {1984}
}
""").lstrip()

SUMMARY = dedent(r"""
Este documento é uma fonte controlada para inspeção visual do perfil correspondente da classe abntexto-ufc. O conteúdo é propositalmente simples e repetível, permitindo avaliar a composição dos elementos pré-textuais, do corpo e das referências sem depender de material externo.
\ufcSummaryKeywords{LaTeX; normalização; UFC; validação visual.}
""").lstrip()

ABSTRACT = dedent(r"""
This document is a controlled source for visual inspection of the corresponding abntexto-ufc profile. Its content is intentionally simple and reproducible so that front matter, body layout and references can be reviewed without external material.
\keywords{LaTeX; normalization; UFC; visual validation.}
""").lstrip()


def common_setup(profile: dict[str, str]) -> str:
    extra = profile["metadata"]
    subtitle = profile["subtitle"]
    subtitle_line = f"  subtitle = {{{subtitle}}},\n" if subtitle else ""
    anonymized = profile["kind"] == "project-anonymized"
    author = "Nome que deve permanecer oculto" if anonymized else "Ana Beatriz Silva"
    advisor = "Prof. Dr. Orientador que deve permanecer oculto" if anonymized else "Prof. Dr. Carlos Eduardo Lima"
    return dedent(
        rf"""
        \ufcsetup{{
          type = {profile['id']},
          print-mode = single-sided,
          cover = auto,
          catalog-card = false,
          coat-of-arms = false,
          font = times,
          strict-font = false,
          glossary = none,
          index = none,
          institution = {{Universidade Federal do Ceará}},
        {extra}
          author = {{{author}}},
          title = {{{profile['title']}}},
        {subtitle_line.rstrip()}
          location = {{Fortaleza}},
          year = {{2026}},
          approval-date = {{9 de setembro de 2026}},
          advisor = {{{advisor}}},
          advisor-institution = {{Universidade Federal do Ceará (UFC)}},
          advisor-unit = {{Departamento de Computação}},
          examiner-2 = {{Profa. Dra. Beatriz Martins}},
          examiner-2-unit = {{Departamento de Computação}},
          examiner-2-institution = {{Universidade Federal do Ceará (UFC)}},
          examiner-3 = {{Prof. Dr. Daniel Rocha}},
          examiner-3-unit = {{Departamento de Computação}},
          examiner-3-institution = {{Universidade Federal do Ceará (UFC)}}
        }}
        """
    ).strip()


def academic_or_project_source(profile: dict[str, str]) -> str:
    academic = profile["kind"] == "academic"
    approval = "\\ufcPrintApprovalPage\n" if academic else ""
    summaries = (
        "\\ufcPrintSummary{summary.tex}\n"
        "\\ufcPrintAbstract{abstract.tex}\n"
        if academic
        else ""
    )
    lists = (
        "\\ufcPrintListOfIllustrations\n"
        "\\ufcPrintListOfTables\n"
        if academic
        else ""
    )
    anonymity_note = (
        "Este perfil deve exibir o identificador do projeto no lugar do nome do autor e não deve revelar orientador na folha de rosto."
        if profile["kind"] == "project-anonymized"
        else "Este perfil deve apresentar os metadados institucionais e autorais definidos no fonte de revisão."
    )
    return dedent(
        rf"""
        % Generated review source for {profile['id']}.
        % Frozen implementation under review: {RELEASE_TAG} / {RELEASED_SOURCE_SHA}.
        \DocumentMetadata{{
          lang = pt-BR,
          pdfstandard = A-2b,
          pdfversion = 1.7
        }}

        \documentclass{{abntexto-ufc}}

        {common_setup(profile)}

        \ufcAddBibliographyResource{{references.bib}}

        \begin{{document}}

        \pretextual
        \ufcPrintCover
        \ufcPrintTitlePage
        {approval}{summaries}{lists}\ufcPrintTableOfContents

        \textual

        \chapter{{Introdução}}
        Este documento foi gerado exclusivamente para validar visualmente o perfil \texttt{{{profile['id']}}} da classe \texttt{{abntexto-ufc}}. {anonymity_note}

        A estrutura declarativa do LaTeX permite separar conteúdo e apresentação \parencite{{lamport1994}}. Esta referência também exercita a integração bibliográfica no PDF de revisão.

        \section{{Objetivo da inspeção}}
        A inspeção deve verificar capa, folha de rosto, elementos específicos do perfil, títulos, margens, paginação, sumário, corpo textual e referências. Qualquer elemento pertencente a outro perfil deve ser tratado como possível regressão.

        \chapter{{Superfícies de apresentação}}

        \section{{Figura controlada}}
        \begin{{figure}}[htbp]
          \centering
          \fbox{{\rule{{0pt}}{{3cm}}\rule{{0.68\textwidth}}{{0pt}}}}
          \caption{{Área gráfica controlada para inspeção de legenda e numeração}}
          \label{{fig:controle}}
        \end{{figure}}

        \section{{Tabela controlada}}
        \begin{{table}}[htbp]
          \centering
          \caption{{Itens da inspeção visual}}
          \label{{tab:controle}}
          \begin{{tabular}}{{|l|l|}}
            \hline
            Item & Estado esperado \\
            \hline
            Perfil & {profile['id']} \\
            Fonte & v3.0.0 congelada \\
            Revisão & Manual antes da CTAN \\
            \hline
          \end{{tabular}}
        \end{{table}}

        \section{{Equação controlada}}
        A Equação~\ref{{eq:controle}} permite inspecionar alinhamento e numeração:
        \begin{{equation}}
          E = mc^2.
          \label{{eq:controle}}
        \end{{equation}}

        \chapter{{Considerações finais}}
        O PDF resultante é evidência para revisão humana do perfil. A aprovação deste arquivo não deve ser inferida a partir da compilação automática.

        \nocite{{knuth1984}}
        \ufcPrintReferences

        \appendix{{Checklist curto de validação}}
        Confirmar identidade do perfil, elementos pré-textuais aplicáveis, paginação, legibilidade, ausência de recortes ou sobreposições e coerência das referências.

        \end{{document}}
        """
    ).lstrip()


def article_source(profile: dict[str, str]) -> str:
    return dedent(
        rf"""
        % Generated review source for scientific-article.
        % Frozen implementation under review: {RELEASE_TAG} / {RELEASED_SOURCE_SHA}.
        \DocumentMetadata{{
          lang = pt-BR,
          pdfstandard = A-2b,
          pdfversion = 1.7
        }}

        \documentclass{{abntexto-ufc}}

        \ufcsetup{{
          type = scientific-article,
          print-mode = single-sided,
          cover = false,
          catalog-card = false,
          coat-of-arms = false,
          font = times,
          strict-font = false,
          glossary = none,
          index = none,
          institution = {{Universidade Federal do Ceará}},
          author = {{Ana Beatriz Silva}},
          title = {{Exemplo de Artigo Científico}},
          submission-date = {{1 de setembro de 2026}},
          approval-date = {{9 de setembro de 2026}},
          article-author-note = {{Universidade Federal do Ceará (UFC). ana.silva@example.org}}
        }}

        \ufcAddBibliographyResource{{references.bib}}

        \begin{{document}}

        \ufcPrintArticleFrontMatter{{%
          Este artigo é uma fonte controlada para inspeção visual do perfil científico da classe abntexto-ufc. O documento exercita bloco inicial, resumo, palavras-chave, seções, nota de rodapé, citações e referências.
          \ufcSummaryKeywords{{artigo científico; LaTeX; UFC; validação visual.}}%
        }}

        \ufcPrintArticleForeignElements
          {{Controlled scientific-article example for visual validation}}
          {{This controlled example exercises the article-specific front block, sections, footnotes, citations and references before CTAN submission.}}

        \section{{Introdução}}
        A validação de um perfil de artigo deve observar o resultado renderizado e não apenas a compilação automática. O LaTeX separa estrutura e apresentação de forma declarativa \parencite{{lamport1994}}.

        Esta frase inclui uma nota de rodapé controlada\footnote{{A nota existe para permitir inspeção visual de tamanho, recuo e separador no perfil de artigo.}}.

        \section{{Superfícies de apresentação}}
        A Tabela~\ref{{tab:artigo}} resume o objetivo desta revisão.

        \begin{{table}}[htbp]
          \centering
          \caption{{Itens do perfil de artigo}}
          \label{{tab:artigo}}
          \begin{{tabular}}{{|l|l|}}
            \hline
            Item & Estado esperado \\
            \hline
            Capa acadêmica & Ausente \\
            Bloco inicial do artigo & Presente \\
            Referências & Presentes \\
            \hline
          \end{{tabular}}
        \end{{table}}

        \subsection{{Inspeção manual}}
        Devem ser verificados autoria, título, resumos, palavras-chave, nota, cabeçalhos, paginação, espaçamento e referências, além da ausência de elementos exclusivos de monografias, dissertações, teses ou projetos.

        \section{{Considerações finais}}
        Este PDF será aceito apenas após revisão visual explícita pelo mantenedor.

        \nocite{{knuth1984}}
        \ufcPrintReferences

        \end{{document}}
        """
    ).lstrip()


def write_profile(root: Path, profile: dict[str, str]) -> None:
    directory = root / profile["id"]
    directory.mkdir(parents=True, exist_ok=True)
    source = article_source(profile) if profile["kind"] == "article" else academic_or_project_source(profile)
    (directory / f"{profile['id']}.tex").write_text(source, encoding="utf-8", newline="\n")
    (directory / "references.bib").write_text(BIBLIOGRAPHY, encoding="utf-8", newline="\n")
    if profile["kind"] == "academic":
        (directory / "summary.tex").write_text(SUMMARY, encoding="utf-8", newline="\n")
        (directory / "abstract.tex").write_text(ABSTRACT, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.output
    root.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        write_profile(root, profile)

    index = {
        "release_tag": RELEASE_TAG,
        "released_source_sha": RELEASED_SOURCE_SHA,
        "profiles": [
            {"id": p["id"], "label": p["label"], "kind": p["kind"]}
            for p in PROFILES
        ],
    }
    (root / "profiles.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "README.txt").write_text(
        "abntexto-ufc v3.0.0 all-profile visual review\n"
        f"Released source: {RELEASED_SOURCE_SHA}\n"
        "The generated sources are review inputs; PDFs and hashes are added by CI.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated {len(PROFILES)} profile review sources in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

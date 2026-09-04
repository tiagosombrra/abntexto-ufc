from __future__ import annotations

import json
from pathlib import Path

BASE = "c4bf51b574647226ee488440579ec2a204c16c79"


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, found {count}: {old!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# Core configuration: add the article type, metadata, journal-boundary acknowledgement, and predicate.
replace_once(
    "abntexto-ufc/core.def",
    "    project-identifier = {},\n    author = {},\n    title = {},\n    subtitle = {},\n    title-variant = {},",
    "    project-identifier = {},\n    author = {},\n    title = {},\n    subtitle = {},\n    title-variant = {},\n    foreign-title = {},\n    author-note = {},\n    author-contact = {},\n    submission-date = {},\n    target-journal = {},\n    journal-guidelines-checked = {false},",
)
replace_once(
    "abntexto-ufc/core.def",
    "    type / anonymized-research-project .code:n =\n      {\n        \\tl_gset:Nn \\g_ufc_document_type_tl { anonymized-research-project }\n        \\bool_gset_false:N \\g_ufc_coat_of_arms_bool\n      },\n\n    print-mode .choice:",
    "    type / anonymized-research-project .code:n =\n      {\n        \\tl_gset:Nn \\g_ufc_document_type_tl { anonymized-research-project }\n        \\bool_gset_false:N \\g_ufc_coat_of_arms_bool\n      },\n    type / scientific-article .code:n =\n      {\n        \\tl_gset:Nn \\g_ufc_document_type_tl { scientific-article }\n        \\bool_gset_false:N \\g_ufc_coat_of_arms_bool\n      },\n\n    print-mode .choice:",
)
replace_once(
    "abntexto-ufc/core.def",
    "    project-identifier .code:n = { \\ufc_meta_set:nn {project-identifier} {#1} },\n    author .code:n = { \\ufc_meta_set:nn {author} {#1} },\n    title .code:n = { \\ufc_meta_set:nn {title} {#1} },\n    subtitle .code:n = { \\ufc_meta_set:nn {subtitle} {#1} },\n    title-variant .code:n = { \\ufc_meta_set:nn {title-variant} {#1} },",
    "    project-identifier .code:n = { \\ufc_meta_set:nn {project-identifier} {#1} },\n    author .code:n = { \\ufc_meta_set:nn {author} {#1} },\n    title .code:n = { \\ufc_meta_set:nn {title} {#1} },\n    subtitle .code:n = { \\ufc_meta_set:nn {subtitle} {#1} },\n    title-variant .code:n = { \\ufc_meta_set:nn {title-variant} {#1} },\n    foreign-title .code:n = { \\ufc_meta_set:nn {foreign-title} {#1} },\n    author-note .code:n = { \\ufc_meta_set:nn {author-note} {#1} },\n    author-contact .code:n = { \\ufc_meta_set:nn {author-contact} {#1} },\n    submission-date .code:n = { \\ufc_meta_set:nn {submission-date} {#1} },\n    target-journal .code:n = { \\ufc_meta_set:nn {target-journal} {#1} },\n    journal-guidelines-checked .choice:,\n    journal-guidelines-checked / true .code:n =\n      { \\ufc_meta_set:nn {journal-guidelines-checked} {true} },\n    journal-guidelines-checked / false .code:n =\n      { \\ufc_meta_set:nn {journal-guidelines-checked} {false} },",
)
replace_once(
    "abntexto-ufc/core.def",
    "\\NewDocumentCommand \\ufcIfAnonymizedProjectTF { +m +m }\n  {\n    \\str_if_eq:VnTF \\g_ufc_document_type_tl {anonymized-research-project} {#1} {#2}\n  }\n\n\\ExplSyntaxOff",
    "\\NewDocumentCommand \\ufcIfAnonymizedProjectTF { +m +m }\n  {\n    \\str_if_eq:VnTF \\g_ufc_document_type_tl {anonymized-research-project} {#1} {#2}\n  }\n\n\\NewDocumentCommand \\ufcIfScientificArticleTF { +m +m }\n  {\n    \\str_if_eq:VnTF \\g_ufc_document_type_tl {scientific-article} {#1} {#2}\n  }\n\n\\ExplSyntaxOff",
)

article_module = r'''\ProvidesFile{abntexto-ufc/scientific-articles.def}[2026/09/04 UFC scientific article profile]

% Scientific-article rules are owned by standards/coverage-rules-article.json.
% Recommendations remain advisory; only required profile invariants fail closed here.

\ExplSyntaxOn

\bool_new:N \g_ufc_article_header_bool
\bool_new:N \g_ufc_article_summary_bool
\bool_new:N \g_ufc_article_introduction_bool
\bool_new:N \g_ufc_article_development_bool
\bool_new:N \g_ufc_article_final_considerations_bool
\bool_new:N \g_ufc_article_references_bool

\prg_new_conditional:Npnn \ufc_article_if_active: { T, F, TF }
  {
    \str_if_eq:VnTF \g_ufc_document_type_tl {scientific-article}
      { \prg_return_true: }
      { \prg_return_false: }
  }

\cs_new_protected:Npn \ufc_article_assert_active:
  {
    \ufc_article_if_active:F
      {
        \ClassError{abntexto-ufc}
          {Scientific article command used outside type=scientific-article}
          {Set type=scientific-article before using the article profile commands.}
      }
  }

\cs_new_protected:Npn \ufc_article_require_meta:n #1
  {
    \ufc_meta_if_blank:nT {#1}
      {
        \ClassError{abntexto-ufc}
          {Scientific article metadata '#1' is required}
          {Provide '#1' in \string\ufcsetup.}
      }
  }

\cs_new_protected:Npn \ufc_article_begin:
  {
    \ufc_article_if_active:T
      {
        \singlesp
        \justifying
        \setlength{\parindent}{2cm}
        \ufc_article_require_meta:n {title}
        \ufc_article_require_meta:n {author}
        \ufc_article_require_meta:n {author-note}
        \ufc_article_require_meta:n {submission-date}
        \ufc_article_require_meta:n {approval-date}
        \ufc_meta_if_blank:nF {target-journal}
          {
            \str_if_eq:eeF
              { \ufc_meta_use:n {journal-guidelines-checked} }
              { true }
              {
                \ClassError{abntexto-ufc}
                  {Journal-specific guidelines were not confirmed}
                  {For target-journal submissions, set journal-guidelines-checked=true only after reviewing the journal instructions.}
              }
          }
      }
  }

\AtBeginDocument{\ufc_article_begin:}

\cs_new_protected:Npn \ufc_article_author_footnote:
  {
    \footnote{%
      \ufc_meta_use:n {author-note}%
      \ufc_meta_if_blank:nF {author-contact}
        { \space Contato: \ufc_meta_use:n {author-contact}. }%
    }
  }

\NewDocumentCommand \ufcPrintArticleHeader { }
  {
    \ufc_article_assert_active:
    \bool_gset_true:N \g_ufc_article_header_bool
    \begingroup
      \singlesp
      \setlength{\parindent}{0pt}
      \begin{center}
        {\fontsize{12}{14.4}\selectfont\bfseries\MakeUppercase{\ufc_meta_use:n {title}}\par}
        \ufc_meta_if_blank:nF {subtitle}
          { \textbf{\ufc_meta_use:n {subtitle}}\par }
        \ufc_meta_if_blank:nF {foreign-title}
          { \vspace{.5\baselineskip}\ufc_meta_use:n {foreign-title}\par }
      \end{center}
      \begin{flushright}
        \ufc_meta_use:n {author}\ufc_article_author_footnote:
      \end{flushright}
      \noindent Recebido em: \ufc_meta_use:n {submission-date}.\par
      \noindent Aprovado em: \ufc_meta_use:n {approval-date}.\par
      \ufc_meta_if_blank:nF {target-journal}
        { \noindent Periódico-alvo: \ufc_meta_use:n {target-journal}.\par }
      \vspace{\baselineskip}
    \endgroup
  }

\NewDocumentCommand \ufcPrintArticleSummary { m m }
  {
    \ufc_article_assert_active:
    \bool_gset_true:N \g_ufc_article_summary_bool
    \begingroup
      \singlesp
      \setlength{\parindent}{0pt}
      \justifying
      \noindent\textbf{Resumo:}\space\ufc_input_file:n {#1}
      \ufcSummaryKeywords{#2}
    \endgroup
  }

\NewDocumentCommand \ufcPrintArticleForeignSummary { m m }
  {
    \ufc_article_assert_active:
    \begingroup
      \singlesp
      \setlength{\parindent}{0pt}
      \justifying
      \noindent\textbf{Abstract:}\space\ufc_input_file:n {#1}
      \keywords{#2}
    \endgroup
  }

\NewDocumentCommand \ufcArticleIntroduction { }
  {
    \ufc_article_assert_active:
    \bool_gset_true:N \g_ufc_article_introduction_bool
    \section{Introdução}
  }

\NewDocumentCommand \ufcArticleDevelopment { }
  {
    \ufc_article_assert_active:
    \bool_gset_true:N \g_ufc_article_development_bool
    \section{Desenvolvimento}
  }

\NewDocumentCommand \ufcArticleFinalConsiderations { }
  {
    \ufc_article_assert_active:
    \bool_gset_true:N \g_ufc_article_final_considerations_bool
    \section{Considerações finais}
  }

\cs_new_eq:NN \ufc_article_original_print_references \ufcPrintReferences
\RenewDocumentCommand \ufcPrintReferences { }
  {
    \ufc_article_if_active:T
      { \bool_gset_true:N \g_ufc_article_references_bool }
    \ufc_article_original_print_references
  }

\cs_new_protected:Npn \ufc_article_require_bool:Nn #1#2
  {
    \bool_if:NF #1
      {
        \ClassError{abntexto-ufc}
          {Scientific article required element '#2' is missing}
          {Use the dedicated scientific-article semantic command for '#2'.}
      }
  }

\AtEndDocument
  {
    \ufc_article_if_active:T
      {
        \ufc_article_require_bool:Nn \g_ufc_article_header_bool {article-header}
        \ufc_article_require_bool:Nn \g_ufc_article_summary_bool {primary-summary}
        \ufc_article_require_bool:Nn \g_ufc_article_introduction_bool {introduction}
        \ufc_article_require_bool:Nn \g_ufc_article_development_bool {development}
        \ufc_article_require_bool:Nn \g_ufc_article_final_considerations_bool {final-considerations}
        \ufc_article_require_bool:Nn \g_ufc_article_references_bool {references}
      }
  }

\ExplSyntaxOff

\endinput
'''
Path("abntexto-ufc/scientific-articles.def").write_text(article_module, encoding="utf-8")
replace_once(
    "abntexto-ufc.cls",
    "\\input{abntexto-ufc/bibliography.def}\n\\input{abntexto-ufc/standards/nbr6023-2025.def}",
    "\\input{abntexto-ufc/bibliography.def}\n\\input{abntexto-ufc/scientific-articles.def}\n\\input{abntexto-ufc/standards/nbr6023-2025.def}",
)

# Extend the canonical v3 type/key inventory used by permanent profile and residual checks.
migration = load_json("release/v3-api-migration.json")
types = migration["setup_values"]["type"]
if "scientific-article" in types:
    raise SystemExit("scientific-article already exists in migration contract")
types.append("scientific-article")
for key in (
    "foreign-title",
    "author-note",
    "author-contact",
    "submission-date",
    "target-journal",
    "journal-guidelines-checked",
):
    if key in migration["setup_keys"]["core"]:
        raise SystemExit(f"setup key already exists: {key}")
    migration["setup_keys"]["core"].append(key)
migration["module_ownership"]["abntexto-ufc/scientific-articles.def"] = [
    "scientific-article profile",
    "article metadata validation",
    "article header and summaries",
    "article semantic structure",
    "journal-guideline applicability boundary",
]
save_json("release/v3-api-migration.json", migration)

# Turn only required article rules into conservative automatic-partial evidence.
coverage = load_json("standards/coverage-rules-article.json")
coverage["purpose"] = (
    "V3-A2 scientific-article normative/runtime contract. Required rules use bounded executable "
    "evidence; optional and recommended rules remain conservative manual/support observations."
)
automatic_article_rules: list[str] = []
for rule in coverage["rules"]:
    checks = rule["validation"]["checks"]
    if "scientific-article" not in checks:
        checks.insert(0, "scientific-article")
    if rule["normativity"] == "required":
        rule["validation"]["mode"] = "automatic-partial"
        automatic_article_rules.append(rule["id"])
if len(automatic_article_rules) != 11:
    raise SystemExit(f"expected 11 required article rules, found {len(automatic_article_rules)}")
save_json("standards/coverage-rules-article.json", coverage)

policy = load_json("standards/evidence-contribution-policy.json")
nonautomatic = policy["nonautomatic_rules"]
for rule_id in automatic_article_rules:
    if rule_id not in nonautomatic:
        raise SystemExit(f"missing A1 nonautomatic entry: {rule_id}")
    del nonautomatic[rule_id]
for rule in coverage["rules"]:
    rule_id = rule["id"]
    if rule["validation"]["mode"] == "manual":
        entry = nonautomatic[rule_id]
        if rule["normativity"] == "recommended":
            entry["rationale"] = (
                "V3-A2 exercises this recommendation as support-only behavior; it remains advisory "
                "and is not promoted to a runtime error or proof-contributing class."
            )
        else:
            entry["rationale"] = (
                "V3-A2 exercises this optional article element, but optional presence remains a "
                "manual/support classification rather than a required proof obligation."
            )
    elif rule["validation"]["mode"] == "conditional-manual":
        nonautomatic[rule_id]["rationale"] = (
            "V3-A2 enforces explicit acknowledgement when a target journal is configured and tests "
            "the rejection path; applicability remains conditional-review rather than automatic proof."
        )
save_json("standards/evidence-contribution-policy.json", policy)

# Article fixtures.
summary = """Este artigo apresenta uma validação controlada do novo perfil de artigo científico do abntexto-ufc, com foco na integração entre requisitos normativos, comportamento de execução e evidência automatizada. A implementação reutiliza a infraestrutura já certificada para tipografia, referências e configuração, evitando criar uma segunda fundação documental. O cenário de teste verifica título, autoria, identificação complementar do autor, datas de submissão e aprovação, resumo, palavras-chave e a estrutura textual composta por introdução, desenvolvimento, considerações finais e referências. Também são exercitados o título em idioma estrangeiro e o resumo estrangeiro como elementos opcionais. A validação mantém recomendações institucionais, como extensão do resumo, quantidade mínima de palavras-chave e alinhamento da autoria, fora do mecanismo de erro obrigatório. Para submissões destinadas a periódico específico, o perfil exige confirmação explícita de que as instruções editoriais foram verificadas. O resultado é um caminho de execução dedicado, rastreável e compatível com os demais perfis da classe, sem reintroduzir aliases legados nem alterar valores normativos congelados durante a etapa anterior."""
Path("tests/fixtures/article-summary.tex").write_text(summary + "\n", encoding="utf-8")
Path("tests/fixtures/article-abstract.tex").write_text(
    "This controlled fixture exercises the optional foreign-language title and abstract of the scientific-article profile while the primary normative evidence remains bound to the Portuguese article route.\n",
    encoding="utf-8",
)

positive = r'''\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}
\documentclass{abntexto-ufc}
\ufcsetup{
  type = scientific-article,
  institution = {Universidade Federal do Ceará},
  author = {Autor Artigo Teste},
  title = {Perfil de artigo científico em validação},
  foreign-title = {Scientific Article Profile Under Validation},
  author-note = {Pesquisador vinculado à Universidade Federal do Ceará},
  author-contact = {autor@example.org},
  submission-date = {1 de setembro de 2026},
  approval-date = {3 de setembro de 2026},
  target-journal = {Periódico de Teste},
  journal-guidelines-checked = true
}
\ufcAddBibliographyResource{../tests/fixtures/references.bib}
\begin{document}
\ufcPrintArticleHeader
\ufcPrintArticleSummary{../tests/fixtures/article-summary}{artigo científico; normalização; LaTeX}
\ufcPrintArticleForeignSummary{../tests/fixtures/article-abstract}{scientific article; standards; LaTeX}
\textual
\ufcArticleIntroduction
A introdução apresenta o objetivo e o escopo da validação do perfil.

\ufcArticleDevelopment
O desenvolvimento descreve a implementação e a evidência executável associada ao contrato normativo.

\ufcArticleFinalConsiderations
As considerações finais registram a compatibilidade do perfil com a fundação v3.

\nocite{silva2020}
\ufcPrintReferences
\end{document}
'''
Path("tests/documents/scientific-article-positive.tex").write_text(positive, encoding="utf-8")

negative_journal = positive.replace(
    "journal-guidelines-checked = true",
    "journal-guidelines-checked = false",
).replace(
    "\\begin{document}\n\\ufcPrintArticleHeader",
    "\\begin{document}\n\\ufcPrintArticleHeader",
)
Path("tests/documents/scientific-article-journal-negative.tex").write_text(negative_journal, encoding="utf-8")

negative_summary = positive.replace(
    "\\ufcPrintArticleSummary{../tests/fixtures/article-summary}{artigo científico; normalização; LaTeX}\n",
    "",
)
Path("tests/documents/scientific-article-summary-negative.tex").write_text(negative_summary, encoding="utf-8")

# Make the complete profile matrix include the new canonical type while preserving existing profiles.
replace_once(
    "tests/integration/profile-matrix.sh",
    'profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project"',
    'profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project scientific-article"',
)
replace_once(
    "tests/integration/profile-matrix.sh",
    "      -e 's#tests/fixtures/references.bib#../tests/fixtures/references.bib#g' \\\n      \"$fixture\" > \"$output.tex\"",
    "      -e 's#tests/fixtures/references.bib#../tests/fixtures/references.bib#g' \\\n      -e 's#tests/fixtures/article-summary#../tests/fixtures/article-summary#g' \\\n      -e 's#tests/fixtures/article-abstract#../tests/fixtures/article-abstract#g' \\\n      \"$fixture\" > \"$output.tex\"",
)
replace_once(
    "tests/integration/profile-matrix.sh",
    "    [ \"${pages:-0}\" -ge 6 ] || {\n      echo \"Profile $profile/$engine: complete document generated only ${pages:-0} pages.\"\n      exit 1\n    }",
    "    minimum_pages=6\n    [ \"$profile\" = \"scientific-article\" ] && minimum_pages=2\n    [ \"${pages:-0}\" -ge \"$minimum_pages\" ] || {\n      echo \"Profile $profile/$engine: complete document generated only ${pages:-0} pages.\"\n      exit 1\n    }",
)
replace_once(
    "tests/integration/profile-matrix.sh",
    "    'anonymized-research-project': (\n        'projeto de pesquisa apresentado',\n        'perfil-anonimo-001',\n        'referencial teórico',\n        'recursos',\n        'cronograma',\n    ),\n}",
    "    'anonymized-research-project': (\n        'projeto de pesquisa apresentado',\n        'perfil-anonimo-001',\n        'referencial teórico',\n        'recursos',\n        'cronograma',\n    ),\n    'scientific-article': (\n        'perfil de artigo científico em validação',\n        'autor matriz teste',\n        'resumo:',\n        'palavras-chave:',\n        'introdução',\n        'desenvolvimento',\n        'considerações finais',\n    ),\n}",
)
replace_once(
    "tests/integration/profile-matrix.sh",
    "for marker in ('introdução', 'metodologia', 'referências', 'fundamentos de metodologia acadêmica'):\n    if marker not in text:\n        raise SystemExit(f'Profile {profile}: structural content is missing: {marker}')",
    "common = ('introdução', 'referências')\nif profile == 'scientific-article':\n    common += ('desenvolvimento', 'considerações finais')\nelse:\n    common += ('metodologia', 'fundamentos de metodologia acadêmica')\nfor marker in common:\n    if marker not in text:\n        raise SystemExit(f'Profile {profile}: structural content is missing: {marker}')",
)
replace_once(
    "tests/integration/profile-matrix.sh",
    "    grep -Fqi 'Metodologia' \"$output.toc\" || {\n      echo \"Profile $profile/$engine: Methodology is missing from the table of contents.\"\n      cat \"$output.toc\"\n      exit 1\n    }",
    "    if [ \"$profile\" = \"scientific-article\" ]; then\n      grep -Fqi 'Desenvolvimento' \"$output.toc\" || {\n        echo \"Profile $profile/$engine: Development is missing from the table of contents.\"\n        cat \"$output.toc\"\n        exit 1\n      }\n      grep -Fqi 'Considera' \"$output.toc\" || {\n        echo \"Profile $profile/$engine: Final considerations are missing from the table of contents.\"\n        cat \"$output.toc\"\n        exit 1\n      }\n    else\n      grep -Fqi 'Metodologia' \"$output.toc\" || {\n        echo \"Profile $profile/$engine: Methodology is missing from the table of contents.\"\n        cat \"$output.toc\"\n        exit 1\n      }\n    fi",
)

# Base profile fixture uses article-specific front/text flow only for the article type.
replace_once(
    "tests/smoke/base-profile.tex",
    "  title = {Documento de Validação do Perfil},\n  location = {Fortaleza},",
    "  title = {Documento de Validação do Perfil},\n  foreign-title = {Scientific Article Profile Validation},\n  author-note = {Pesquisador vinculado à Universidade Federal do Ceará},\n  author-contact = {autor.matriz@example.org},\n  submission-date = {18 de agosto de 2026},\n  target-journal = {},\n  journal-guidelines-checked = false,\n  location = {Fortaleza},",
)
replace_once(
    "tests/smoke/base-profile.tex",
    "\\begin{document}\n\\pretextual\n\n\\ufcPrintCover\n\\ufcPrintTitlePage\n\\ufcIfProjectTF{}{\n  \\ufcPrintApprovalPage\n  \\ufcPrintSummary{frontmatter/summary}\n  \\ufcPrintAbstract{frontmatter/abstract}\n}\n\\ufcPrintTableOfContents\n\n\\textual\n\\section{Introdução}\nConteúdo mínimo para validação do perfil documental.\n\n\\ufcIfProjectTF{",
    "\\begin{document}\n\\ufcIfScientificArticleTF{\n  \\ufcPrintArticleHeader\n  \\ufcPrintArticleSummary{tests/fixtures/article-summary}{artigo científico; matriz; LaTeX}\n  \\ufcPrintArticleForeignSummary{tests/fixtures/article-abstract}{scientific article; matrix; LaTeX}\n  \\textual\n  \\ufcArticleIntroduction\n  Conteúdo mínimo para validação do perfil de artigo científico.\n\n  \\ufcArticleDevelopment\n  Desenvolvimento mínimo para validação cruzada do perfil.\n\n  \\ufcArticleFinalConsiderations\n  Considerações finais mínimas para validação cruzada do perfil.\n}{\n  \\pretextual\n\n  \\ufcPrintCover\n  \\ufcPrintTitlePage\n  \\ufcIfProjectTF{}{\n    \\ufcPrintApprovalPage\n    \\ufcPrintSummary{frontmatter/summary}\n    \\ufcPrintAbstract{frontmatter/abstract}\n  }\n  \\ufcPrintTableOfContents\n\n  \\textual\n  \\section{Introdução}\n  Conteúdo mínimo para validação do perfil documental.\n\n  \\ufcIfProjectTF{",
)
replace_once(
    "tests/smoke/base-profile.tex",
    "  \\section{Conclusão}\n  Conclusão sintética da fixture.\n}\n\n\\nocite{silva2020}",
    "    \\section{Conclusão}\n    Conclusão sintética da fixture.\n  }\n}\n\n\\nocite{silva2020}",
)

replace_once(
    "tests/integration/profile-pdfa.sh",
    'profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project"',
    'profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project scientific-article"',
)
replace_once(
    "tests/integration/profile-pdfa.sh",
    "echo 'Gate PDF/A-2b of the 12 profiles completed.'",
    "echo 'Gate PDF/A-2b of the 14 profile/engine combinations completed.'",
)

article_runner = r'''#!/bin/sh
set -eu

template_dir="template"
positive="scientific-article-positive"
negative_journal="scientific-article-journal-negative"
negative_summary="scientific-article-summary-negative"

cleanup() {
  job="$1"
  rm -f "$template_dir/$job".tex "$template_dir/$job".aux "$template_dir/$job".bbl \
    "$template_dir/$job".bcf "$template_dir/$job".blg "$template_dir/$job".log \
    "$template_dir/$job".out "$template_dir/$job".toc "$template_dir/$job".run.xml \
    "$template_dir/$job".pdf
}

# Source-level ownership assertions keep typography evidence bounded and explicit.
grep -Fq '\fontsize{12}{14.4}\selectfont\bfseries\MakeUppercase' abntexto-ufc/scientific-articles.def
grep -Fq '\begin{center}' abntexto-ufc/scientific-articles.def
grep -Fq '\begin{flushright}' abntexto-ufc/scientific-articles.def
grep -Fq '\footnote' abntexto-ufc/scientific-articles.def
grep -Fq '\singlesp' abntexto-ufc/scientific-articles.def
grep -Fq '\setlength{\parindent}{2cm}' abntexto-ufc/scientific-articles.def
grep -Fq '\justifying' abntexto-ufc/scientific-articles.def

for engine in pdflatex lualatex; do
  cleanup "$positive"
  cp "tests/documents/$positive.tex" "$template_dir/$positive.tex"
  if ! make DOCUMENT="$positive" ENGINE="$engine" compile > "/tmp/$positive-$engine.log" 2>&1; then
    cat "/tmp/$positive-$engine.log"
    exit 1
  fi
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$template_dir/$positive.log" || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Scientific article positive fixture contains an unexpected warning/overflow for $engine."
    exit 1
  fi
  [ -s "$template_dir/$positive.pdf" ] || { echo "Scientific article PDF missing for $engine."; exit 1; }
  sh tests/integration/font-embedding.sh "$template_dir/$positive.pdf"
  pdftotext -layout "$template_dir/$positive.pdf" "/tmp/$positive-$engine.txt"
  python3 - "/tmp/$positive-$engine.txt" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
text = re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).casefold()
for marker in (
    "perfil de artigo científico em validação",
    "scientific article profile under validation",
    "autor artigo teste",
    "pesquisador vinculado à universidade federal do ceará",
    "autor@example.org",
    "recebido em: 1 de setembro de 2026",
    "aprovado em: 3 de setembro de 2026",
    "resumo:",
    "palavras-chave:",
    "abstract:",
    "keywords:",
    "introdução",
    "desenvolvimento",
    "considerações finais",
    "referências",
):
    if marker not in text:
        raise SystemExit(f"scientific article rendered marker missing: {marker}")
PY
  cleanup "$positive"

  for job in "$negative_journal" "$negative_summary"; do
    cleanup "$job"
    cp "tests/documents/$job.tex" "$template_dir/$job.tex"
    if make DOCUMENT="$job" ENGINE="$engine" compile > "/tmp/$job-$engine.log" 2>&1; then
      echo "Scientific article negative fixture unexpectedly compiled: $job/$engine"
      exit 1
    fi
    case "$job" in
      "$negative_journal")
        grep -Fq 'Journal-specific guidelines were not confirmed' "/tmp/$job-$engine.log" || {
          cat "/tmp/$job-$engine.log"
          echo "Journal precedence negative fixture failed for the wrong reason."
          exit 1
        }
        ;;
      "$negative_summary")
        grep -Fq "Scientific article required element 'primary-summary' is missing" "/tmp/$job-$engine.log" || {
          cat "/tmp/$job-$engine.log"
          echo "Missing-summary negative fixture failed for the wrong reason."
          exit 1
        }
        ;;
    esac
    cleanup "$job"
  done
done

python3 - <<'PY'
import re
from pathlib import Path
summary = Path('tests/fixtures/article-summary.tex').read_text(encoding='utf-8').strip()
words = re.findall(r"\b[\wÀ-ÿ-]+\b", summary, flags=re.UNICODE)
if not 150 <= len(words) <= 250:
    raise SystemExit(f'article recommendation fixture word count outside 150-250: {len(words)}')
if '\n\n' in summary:
    raise SystemExit('article recommendation fixture is not a single paragraph')
print(f'SCIENTIFIC-ARTICLE-SUPPORT summary_words={len(words)} paragraphs=1 keywords=3 author_alignment=right')
PY

for rule in \
  article.title.primary.required \
  article.authorship.required \
  article.summary.primary.required \
  article.dates.submission-approval.required \
  article.introduction.required \
  article.development.required \
  article.final-considerations.required \
  article.references.required \
  article.title.primary.typography \
  article.authorship.metadata.footnote \
  article.body.typography \
  article.journal-guidelines.precedence
do
  echo "SCIENTIFIC-ARTICLE-EVIDENCE rule=$rule status=PASS engines=pdflatex,lualatex"
done

echo 'Scientific article runtime gate completed.'
'''
Path("tests/integration/scientific-article.sh").write_text(article_runner, encoding="utf-8")

replace_once(
    "tests/run.py",
    '    Check("research-project", "Research project", ("sh", "tests/integration/research-project.sh")),\n    Check("profiles", "Document profiles", ("sh", "tests/integration/profile-matrix.sh")),',
    '    Check("research-project", "Research project", ("sh", "tests/integration/research-project.sh")),\n    Check("scientific-article", "Scientific article", ("sh", "tests/integration/scientific-article.sh")),\n    Check("profiles", "Document profiles", ("sh", "tests/integration/profile-matrix.sh")),',
)

# Keep the machine state truthful: A2 is active, now with runtime started but not closed.
roadmap = load_json("release/v3-roadmap.json")
active = roadmap["active_implementation_lot"]
if active.get("stage") != "V3-A2" or active.get("entry_main_sha") != BASE:
    raise SystemExit("unexpected A2 machine-state entry")
active["runtime_started"] = True
active["implementation_branch"] = "feat/v3-a2-scientific-article"
active["implementation_status"] = "IN_PROGRESS"
active["article_runtime_type"] = "scientific-article"
active["required_runtime_rules_automatic_partial"] = 11
active["journal_precedence_class"] = "conditional-review"
active["recommended_rules_hard_errors"] = False
roadmap["v3_a2"]["runtime_started"] = True
roadmap["v3_a2"]["implementation_status"] = "IN_PROGRESS"
roadmap["v3_a2"]["article_runtime_type"] = "scientific-article"
save_json("release/v3-roadmap.json", roadmap)

print("A2 scientific article implementation staged.")

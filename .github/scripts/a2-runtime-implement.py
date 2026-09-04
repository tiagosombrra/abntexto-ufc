from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRY = "7a7562d23e8bf6c92abb635718639d617a2ed6ff"
BASE = "c4bf51b574647226ee488440579ec2a204c16c79"
INVENTORY_RUN = 33908634568
TODAY = "2026-09-04"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one match in {path}, found {count}: {old!r}")
    write(path, text.replace(old, new))


def load_json(path: str) -> dict:
    return json.loads(read(path))


def save_json(path: str, data: dict) -> None:
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


# Canonical profile state and article-specific metadata.
replace_once(
    "abntexto-ufc/core.def",
    "    title-variant = {},\n    volume = {},",
    "    title-variant = {},\n    foreign-title = {},\n    foreign-subtitle = {},\n    submission-date = {},\n    author-note = {},\n    volume = {},",
)
replace_once(
    "abntexto-ufc/core.def",
    "    type / anonymized-research-project .code:n =\n      {\n        \\tl_gset:Nn \\g_ufc_document_type_tl { anonymized-research-project }\n        \\bool_gset_false:N \\g_ufc_coat_of_arms_bool\n      },\n\n    print-mode .choice:,
",
    "    type / anonymized-research-project .code:n =\n      {\n        \\tl_gset:Nn \\g_ufc_document_type_tl { anonymized-research-project }\n        \\bool_gset_false:N \\g_ufc_coat_of_arms_bool\n      },\n    type / scientific-article .code:n =\n      {\n        \\tl_gset:Nn \\g_ufc_document_type_tl { scientific-article }\n        \\bool_gset_false:N \\g_ufc_coat_of_arms_bool\n        \\bool_gset_false:N \\g_ufc_catalog_card_bool\n      },\n\n    print-mode .choice:,
",
)
replace_once(
    "abntexto-ufc/core.def",
    "    title-variant .code:n = { \\ufc_meta_set:nn {title-variant} {#1} },\n    volume .code:n = { \\ufc_meta_set:nn {volume} {#1} },",
    "    title-variant .code:n = { \\ufc_meta_set:nn {title-variant} {#1} },\n    foreign-title .code:n = { \\ufc_meta_set:nn {foreign-title} {#1} },\n    foreign-subtitle .code:n = { \\ufc_meta_set:nn {foreign-subtitle} {#1} },\n    submission-date .code:n = { \\ufc_meta_set:nn {submission-date} {#1} },\n    author-note .code:n = { \\ufc_meta_set:nn {author-note} {#1} },\n    volume .code:n = { \\ufc_meta_set:nn {volume} {#1} },",
)
replace_once(
    "abntexto-ufc/core.def",
    "\\NewDocumentCommand \\ufcIfAnonymizedProjectTF { +m +m }\n  {\n    \\str_if_eq:VnTF \\g_ufc_document_type_tl {anonymized-research-project} {#1} {#2}\n  }\n\n\\ExplSyntaxOff",
    "\\NewDocumentCommand \\ufcIfAnonymizedProjectTF { +m +m }\n  {\n    \\str_if_eq:VnTF \\g_ufc_document_type_tl {anonymized-research-project} {#1} {#2}\n  }\n\n\\NewDocumentCommand \\ufcIfScientificArticleTF { +m +m }\n  {\n    \\str_if_eq:VnTF \\g_ufc_document_type_tl {scientific-article} {#1} {#2}\n  }\n\n\\ExplSyntaxOff",
)

# Article sections remain continuous; all existing profiles keep their page-break policy.
replace_once(
    "abntexto-ufc/layout.def",
    "\\cs_new_protected:Npn \\ufc_primary_section_break:\n  {\n    \\str_if_eq:VnTF \\g_ufc_print_mode_tl { double-sided }\n      { \\ufc_next_odd_physical_page: }\n      { \\clearpage }\n  }",
    "\\cs_new_protected:Npn \\ufc_primary_section_break:\n  {\n    \\str_if_eq:VnF \\g_ufc_document_type_tl { scientific-article }\n      {\n        \\str_if_eq:VnTF \\g_ufc_print_mode_tl { double-sided }\n          { \\ufc_next_odd_physical_page: }\n          { \\clearpage }\n      }\n  }",
)

# Load the A2-owned module only after shared bibliography/reference machinery exists.
replace_once(
    "abntexto-ufc.cls",
    "\\input{abntexto-ufc/bibliography.def}\n\\input{abntexto-ufc/standards/nbr6023-2025.def}",
    "\\input{abntexto-ufc/bibliography.def}\n\\input{abntexto-ufc/articles.def}\n\\input{abntexto-ufc/standards/nbr6023-2025.def}",
)

write(
    "abntexto-ufc/articles.def",
    r'''\ProvidesFile{abntexto-ufc/articles.def}[2026/09/04 UFC scientific article profile]

% Scientific-article behavior is owned directly by V3-A2.
% Normative mapping: docs/ARTICLE-NORMATIVE-CONTRACT.md.

\ExplSyntaxOn

\cs_new_protected:Npn \ufc_article_require_profile:
  {
    \str_if_eq:VnF \g_ufc_document_type_tl { scientific-article }
      {
        \ClassError{abntexto-ufc}
          {Scientific-article~command~used~outside~the~scientific-article~profile}
          {Set~type=scientific-article~before~using~article-specific~commands.}
      }
  }

\cs_new_protected:Npn \ufc_article_require_meta:n #1
  {
    \ufc_meta_if_blank:nT {#1}
      {
        \ClassError{abntexto-ufc}
          {Required~scientific-article~metadata~'#1'~is~missing}
          {Provide~the~required~value~through~\string\ufcsetup.}
      }
  }

\cs_new_protected:Npn \ufc_article_primary_title:
  {
    \begin{center}
      \begingroup
        \normalsize\singlesp\bfseries
        \ufc_title_text:\par
      \endgroup
      \ufc_meta_if_blank:nF {foreign-title}
        {
          \vspace{.5\baselineskip}
          \ufc_meta_use:n {foreign-title}
          \ufc_meta_if_blank:nF {foreign-subtitle}
            {:\space\ufc_meta_use:n {foreign-subtitle}}
          \par
        }
    \end{center}
  }

\cs_new_protected:Npn \ufc_article_author:
  {
    \begingroup
      \raggedleft
      \ufc_meta_use:n {author}%
      \footnote{\ufc_meta_use:n {author-note}}\par
    \endgroup
  }

\cs_new_protected:Npn \ufc_article_dates:
  {
    \par\noindent
    Submetido~em:~\ufc_meta_use:n {submission-date}.\space
    Aprovado~em:~\ufc_meta_use:n {approval-date}.\par
  }

\cs_new_protected:Npn \ufc_article_summary:n #1
  {
    \par\vspace{\baselineskip}
    \begingroup
      \singlesp
      \setlength{\parindent}{0pt}
      \justifying
      \noindent\textbf{Resumo:}\space #1\par
    \endgroup
  }

\cs_new_protected:Npn \ufc_article_foreign_summary:n #1
  {
    \par\vspace{\baselineskip}
    \begingroup
      \selectlanguage{english}
      \singlesp
      \setlength{\parindent}{0pt}
      \justifying
      \noindent\textbf{Abstract:}\space #1\par
    \endgroup
  }

\NewDocumentCommand \ufcPrintArticleFrontMatter { +m }
  {
    \ufc_article_require_profile:
    \ufc_article_require_meta:n {title}
    \ufc_article_require_meta:n {author}
    \ufc_article_require_meta:n {author-note}
    \ufc_article_require_meta:n {submission-date}
    \ufc_article_require_meta:n {approval-date}
    \ufc_article_primary_title:
    \ufc_article_author:
    \ufc_article_dates:
    \ufc_article_summary:n {#1}
  }

\NewDocumentCommand \ufcPrintArticleForeignSummary { +m }
  {
    \ufc_article_require_profile:
    \ufc_article_foreign_summary:n {#1}
  }

% The guide's article body uses the same 12 pt class size, 2 cm paragraph
% indentation and justified paragraphs as shared infrastructure, but single spacing.
% This hook runs after layout.def's general one-and-a-half-spacing default.
\AtBeginDocument
  {
    \ufcIfScientificArticleTF
      { \singlesp\justifying }
      { }
  }

\ExplSyntaxOff

\endinput
''',
)

# Make the new public type and metadata part of the canonical v3 API contract.
api = load_json("release/v3-api-migration.json")
core_keys = api["setup_keys"]["core"]
for key in ["foreign-title", "foreign-subtitle", "submission-date", "author-note"]:
    if key not in core_keys:
        insert_at = core_keys.index("volume")
        core_keys.insert(insert_at, key)
canonical_types = api["setup_values"]["type"]
if "scientific-article" not in canonical_types:
    canonical_types.append("scientific-article")
runtime_map = api.setdefault("runtime_ownership", {})
runtime_map["abntexto-ufc/articles.def"] = [
    "scientific-article front matter",
    "scientific-article body spacing and profile-specific presentation",
]
save_json("release/v3-api-migration.json", api)

# Activate the already-reconfirmed article source contract without changing authority.
policy = load_json("standards/version-policy.json")
article_policy = policy["profile_candidates"]["scientific_article"]
if article_policy.get("status") != "deferred-outside-active-foundation":
    raise SystemExit("unexpected scientific-article version-policy status")
article_policy.update(
    {
        "status": "active-current-runtime",
        "runtime_present": True,
        "activation_condition": (
            "Satisfied by V3-A1 source-contract closeout at " + ENTRY
            + " and V3-A2 activation; runtime is implemented only against the reconfirmed source set."
        ),
        "rule": (
            "Scientific-article runtime is active in V3-A2. Current source authority, precedence and "
            "requirement modalities remain those reconfirmed by V3-A1."
        ),
    }
)
policy["reviewed_at"] = TODAY
policy["purpose"] = (
    "Define the current technical-edition rule when UFC guides cite superseded ABNT editions and "
    "enforce staged profile activation from reconfirmed source contract to current runtime."
)
save_json("standards/version-policy.json", policy)

source_audit = load_json("standards/source-audit.json")
if "v3_a2_article_runtime_activation" in source_audit:
    raise SystemExit("A2 article runtime activation already recorded")
source_audit["v3_a2_article_runtime_activation"] = {
    "status": "ACTIVE",
    "reviewed_at": TODAY,
    "entry_main_sha": ENTRY,
    "implementation_base_main_sha": BASE,
    "profile": "scientific-article",
    "runtime_module": "abntexto-ufc/articles.def",
    "source_authority_changed": False,
    "rule_ids_changed": False,
    "locators_changed": False,
    "modalities_changed": False,
    "proof_state_promoted": False,
}
save_json("standards/source-audit.json", source_audit)

# Currency checker now enforces the activated A2 state instead of the historical A1 deferral.
replace_once(
    "tests/checks/normative_currency.py",
    '''    if article.get("status") != "deferred-outside-active-foundation":\n        fail("scientific-article profile must remain outside the active foundation")\n    if article.get("runtime_present") is not False:\n        fail("scientific-article runtime must remain absent from the active foundation")''',
    '''    if article.get("status") != "active-current-runtime":\n        fail("scientific-article profile must be active in the current A2 runtime")\n    if article.get("runtime_present") is not True:\n        fail("scientific-article runtime must be present after A2 activation")''',
)
replace_once(
    "tests/checks/normative_currency.py",
    '''    if (ROOT / "abntexto-ufc" / "articles.def").exists():\n        fail("scientific-article runtime appeared before foundation activation")''',
    '''    if not (ROOT / "abntexto-ufc" / "articles.def").is_file():\n        fail("scientific-article runtime module is missing after A2 activation")''',
)

# Article-specific smoke fixture. It reuses the shared bibliography and section machinery.
write(
    "tests/smoke/scientific-article-profile.tex",
    r'''\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}

\documentclass{abntexto-ufc}

\ufcsetup{
  type = @UFC_TYPE@,
  print-mode = single-sided,
  cover = false,
  catalog-card = false,
  author = {Autor Artigo Teste},
  author-note = {Universidade Federal do Ceará. Contato: autor@example.invalid},
  title = {Artigo de Validação do Perfil Científico},
  foreign-title = {Scientific Article Profile Validation},
  submission-date = {1 de setembro de 2026},
  approval-date = {2 de setembro de 2026},
  location = {Fortaleza},
  year = {2026}
}

\ufcAddBibliographyResource{tests/fixtures/references.bib}

\begin{document}
\pretextual
\ufcPrintArticleFrontMatter{%
  Este resumo valida o perfil de artigo científico sem alterar a modalidade das recomendações do contrato A1.
  \ufcSummaryKeywords{artigo científico; normalização; LaTeX}%
}
\ufcPrintArticleForeignSummary{%
  This abstract validates the optional foreign-language article element.
  \keywords{scientific article; standards; LaTeX}%
}

\textual
\section{Introdução}
Texto introdutório do artigo para validação do perfil canônico.

\section{Desenvolvimento}
Desenvolvimento sintético que reutiliza a infraestrutura compartilhada de seções, citações e objetos.

\section{Considerações finais}
Considerações finais sintéticas para fechar a estrutura textual mínima da fixture.

\nocite{silva2020}
\ufcPrintReferences
\end{document}
''',
)

# Extend the canonical profile-matrix contract to a dedicated article fixture.
write(
    "tests/checks/profile_matrix_contract.py",
    r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "release/v3-api-migration.json"
RUNNER = ROOT / "tests/integration/profile-matrix.sh"
BASE_FIXTURE = ROOT / "tests/smoke/base-profile.tex"
ARTICLE_FIXTURE = ROOT / "tests/smoke/scientific-article-profile.tex"
PLACEHOLDER = "@UFC_TYPE@"
ARTICLE_PROFILE = "scientific-article"


def fail(message: str) -> None:
    raise SystemExit(f"Profile matrix contract failed: {message}")


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    canonical = contract["setup_values"]["type"]
    if not isinstance(canonical, list) or not canonical or not all(
        isinstance(item, str) and item for item in canonical
    ):
        fail("release/v3-api-migration.json has no canonical type list")
    if len(canonical) != len(set(canonical)):
        fail("canonical type list contains duplicates")
    if ARTICLE_PROFILE not in canonical:
        fail("scientific-article is missing from the canonical type set")

    runner_text = RUNNER.read_text(encoding="utf-8")
    match = re.search(r'^profiles="([^"]+)"$', runner_text, flags=re.MULTILINE)
    if match is None:
        fail("profile-matrix.sh does not declare a literal profiles list")
    declared = match.group(1).split()
    if len(declared) != len(set(declared)):
        fail("profile-matrix.sh declares duplicate profiles")
    if set(declared) != set(canonical):
        fail(
            "profile-matrix.sh does not cover the canonical type set: "
            f"declared={declared} canonical={canonical}"
        )

    fixture_texts = {
        "base": BASE_FIXTURE.read_text(encoding="utf-8"),
        "article": ARTICLE_FIXTURE.read_text(encoding="utf-8"),
    }
    for name, text in fixture_texts.items():
        count = text.count(PLACEHOLDER)
        if count != 1:
            fail(f"{name} fixture must contain exactly one {PLACEHOLDER}; found {count}")

    assignment_pattern = re.compile(r"^[ \t]*type[ \t]*=[ \t]*([^,\n]+)[ \t]*,", re.MULTILINE)
    generated_sources: set[str] = set()
    for profile in canonical:
        fixture_text = fixture_texts["article" if profile == ARTICLE_PROFILE else "base"]
        generated = fixture_text.replace(PLACEHOLDER, profile)
        if PLACEHOLDER in generated:
            fail(f"placeholder survived generation for {profile}")
        normalized = [value.strip() for value in assignment_pattern.findall(generated)]
        if normalized != [profile]:
            fail(f"generated type assignment is not exact for {profile}: {normalized}")
        generated_sources.add(generated)

    if len(generated_sources) != len(canonical):
        fail("canonical profile substitutions do not produce distinct generated sources")

    print(
        "PROFILE-MATRIX-GENERATOR-EVIDENCE status=PASS "
        f"profiles={len(declared)} fixtures=2 distinct_sources={len(generated_sources)} "
        f"canonical_values={len(canonical)}"
    )


if __name__ == "__main__":
    main()
''',
)

write(
    "tests/integration/profile-matrix.sh",
    r'''#!/bin/sh
set -eu

base_fixture="tests/smoke/base-profile.tex"
article_fixture="tests/smoke/scientific-article-profile.tex"
template_dir="template"
profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project scientific-article"

for fixture in "$base_fixture" "$article_fixture"; do
  placeholder_count=$(awk '{ count += gsub(/@UFC_TYPE@/, "&") } END { print count + 0 }' "$fixture")
  if [ "$placeholder_count" -ne 1 ]; then
    echo "Profile matrix generation failed: $fixture must contain exactly one @UFC_TYPE@ placeholder; found $placeholder_count."
    exit 1
  fi
done

cleanup_job() {
  job="$1"
  rm -f "$template_dir/$job".tex "$template_dir/$job".aux "$template_dir/$job".bbl \
    "$template_dir/$job".bcf "$template_dir/$job".blg "$template_dir/$job".log \
    "$template_dir/$job".out "$template_dir/$job".toc "$template_dir/$job".run.xml \
    "$template_dir/$job".pdf
}

for engine in pdflatex lualatex; do
  for profile in $profiles; do
    job="perfil-${profile}-${engine}"
    output="$template_dir/$job"
    fixture="$base_fixture"
    if [ "$profile" = "scientific-article" ]; then
      fixture="$article_fixture"
    fi

    cleanup_job "$job"
    sed \
      -e "s/@UFC_TYPE@/$profile/g" \
      -e 's#tests/fixtures/references.bib#../tests/fixtures/references.bib#g' \
      "$fixture" > "$output.tex"

    if grep -Fq '@UFC_TYPE@' "$output.tex"; then
      echo "Profile matrix generation failed: placeholder survived for $profile."
      exit 1
    fi
    type_lines=$(grep -Ec '^[[:space:]]*type[[:space:]]*=' "$output.tex" || true)
    if [ "$type_lines" -ne 1 ] || ! grep -Eq "^[[:space:]]*type[[:space:]]*=[[:space:]]*$profile[[:space:]]*," "$output.tex"; then
      echo "Profile matrix generation failed: generated source does not contain exactly type = $profile,."
      cat "$output.tex"
      exit 1
    fi

    echo "Validating complete profile $profile with $engine..."
    make DOCUMENT="$job" ENGINE="$engine" compile > /tmp/abntexto-ufc-profile.log 2>&1 || {
      cat /tmp/abntexto-ufc-profile.log
      exit 1
    }
    rm -f "$output.tex"

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$output.log" || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "Preflight failed: profile $profile/$engine contains unrecognized warning or overflow."
      exit 1
    fi

    if [ -f "$output.blg" ] && grep -Eq 'WARN|ERROR' "$output.blg"; then
      cat "$output.blg"
      echo "Preflight failed: Biber reported a warning/error in $profile/$engine."
      exit 1
    fi

    [ -s "$output.pdf" ] || {
      echo "profile $profile/$engine: PDF was not generated."
      exit 1
    }

    meta="/tmp/$job-meta.xml"
    pdfinfo -meta "$output.pdf" > "$meta"
    grep -Fq '<pdfaid:part>2</pdfaid:part>' "$meta" || {
      echo "Profile $profile/$engine: PDF/A part 2 declaration is missing."
      exit 1
    }
    grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "$meta" || {
      echo "Profile $profile/$engine: PDF/A-2b declaration is missing."
      exit 1
    }

    if ! pdfinfo "$output.pdf" | awk '
      /^Page size:/ {
        width = $3 + 0
        height = $5 + 0
        if (width < 594.5 || width > 596.0 || height < 841.0 || height > 842.8)
          exit 1
        found = 1
      }
      END { if (!found) exit 1 }
    '; then
      pdfinfo "$output.pdf"
      echo "Profile $profile/$engine: page is not A4."
      exit 1
    fi

    pages=$(pdfinfo "$output.pdf" | awk '/^Pages:/ {print $2}')
    if [ "$profile" = "scientific-article" ]; then
      [ "${pages:-0}" -ge 1 ] || {
        echo "Profile $profile/$engine: article PDF has no pages."
        exit 1
      }
    else
      [ "${pages:-0}" -ge 6 ] || {
        echo "Profile $profile/$engine: complete document generated only ${pages:-0} pages."
        exit 1
      }
    fi

    sh tests/integration/font-embedding.sh "$output.pdf"

    pdftotext -layout "$output.pdf" "/tmp/$job.txt"
    python3 - "$profile" "$job" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

profile, job = sys.argv[1:3]
raw = Path(f'/tmp/{job}.txt').read_text(encoding='utf-8')
raw = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', raw)
text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw)).strip().casefold()

expected = {
    'undergraduate-capstone': (
        'curso de graduação em ciência da computação',
        'trabalho de conclusão de curso',
        'banca examinadora',
        'resumo',
        'abstract',
    ),
    'specialization-capstone': (
        'curso de especialização em computação aplicada',
        'trabalho de conclusão de curso',
        'especialista em computação aplicada',
        'banca examinadora',
    ),
    'masters-thesis': (
        'dissertação apresentada',
        'mestre em ciência da computação',
        'área de concentração: computação gráfica',
        'banca examinadora',
    ),
    'doctoral-thesis': (
        'tese apresentada',
        'doutor em ciência da computação',
        'área de concentração: computação gráfica',
        'banca examinadora',
    ),
    'research-project': (
        'projeto de pesquisa apresentado',
        'processo seletivo de teste',
        'referencial teórico',
        'recursos',
        'cronograma',
    ),
    'anonymized-research-project': (
        'projeto de pesquisa apresentado',
        'perfil-anonimo-001',
        'referencial teórico',
        'recursos',
        'cronograma',
    ),
    'scientific-article': (
        'artigo de validação do perfil científico',
        'scientific article profile validation',
        'autor artigo teste',
        'universidade federal do ceará. contato: autor@example.invalid',
        'submetido em: 1 de setembro de 2026',
        'aprovado em: 2 de setembro de 2026',
        'resumo:',
        'abstract:',
        'introdução',
        'desenvolvimento',
        'considerações finais',
        'referências',
    ),
}

for marker in expected[profile]:
    if marker not in text:
        raise SystemExit(f'Profile {profile}: semantic content is missing: {marker}')

if profile == 'scientific-article':
    for forbidden in ('banca examinadora', 'trabalho de conclusão de curso', 'dissertação apresentada', 'tese apresentada'):
        if forbidden in text:
            raise SystemExit(f'Article profile leaked non-article element: {forbidden}')
else:
    for marker in ('introdução', 'metodologia', 'referências', 'fundamentos de metodologia acadêmica'):
        if marker not in text:
            raise SystemExit(f'Profile {profile}: structural content is missing: {marker}')

if 'capítulo' in text or 'capitulo' in text:
    raise SystemExit(f'Profile {profile}: chapter-based structure reappeared.')

if profile == 'anonymized-research-project':
    for secret in ('autor matriz teste', 'prof. orientador matriz teste', 'prof. membro matriz teste'):
        if secret in text:
            raise SystemExit(f'Anonymized profile leaked protected data: {secret}')
elif profile != 'scientific-article':
    if 'autor matriz teste' not in text:
        raise SystemExit(f'Profile {profile}: expected author is missing.')

if profile in {'research-project', 'anonymized-research-project'}:
    for forbidden in ('banca examinadora', 'abstract'):
        if forbidden in text:
            raise SystemExit(f'Profile {profile}: academic-work element appeared incorrectly: {forbidden}')
PY

    if [ "$profile" != "scientific-article" ]; then
      grep -Fqi 'Introdu' "$output.toc" || {
        echo "Profile $profile/$engine: Introduction is missing from the table of contents."
        cat "$output.toc"
        exit 1
      }
      grep -Fqi 'Metodologia' "$output.toc" || {
        echo "Profile $profile/$engine: Methodology is missing from the table of contents."
        cat "$output.toc"
        exit 1
      }
      if grep -Eq '\\contentsline \{section\}\{[^}]*\*' "$output.toc"; then
        echo "Profile $profile/$engine: anomalous asterisk entry found in the table of contents."
        cat "$output.toc"
        exit 1
      fi
    fi
  done
done

echo 'Complete profile matrix gate completed.'
''',
)

replace_once(
    "tests/integration/profile-pdfa.sh",
    'profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project"',
    'profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project scientific-article"',
)
replace_once(
    "tests/integration/profile-pdfa.sh",
    "echo 'Gate PDF/A-2b of the 12 profiles completed.'",
    "echo 'Gate PDF/A-2b of the 14 profile PDFs completed.'",
)

# Record the start of A2 runtime implementation while leaving article proof states untouched.
roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-A2" or roadmap.get("stage") != "V3-A2":
    raise SystemExit("unexpected roadmap stage")
roadmap["updated_at"] = TODAY
roadmap["a2_preparation"]["runtime_implementation_started"] = True
roadmap["a2"]["runtime_implementation_started"] = True
roadmap["a2"]["runtime_lot"] = {
    "status": "ACTIVE",
    "name": "canonical scientific-article runtime and profile-matrix ownership",
    "branch": "feat/v3-a2-scientific-article-runtime",
    "implementation_base_main_sha": BASE,
    "canonical_a2_entry_main_sha": ENTRY,
    "inventory_run_id": INVENTORY_RUN,
    "proof_state_promoted": False,
}
save_json("release/v3-roadmap.json", roadmap)

# Current documentation: runtime has started, evidence promotion remains pending.
replace_once(
    "docs/NORMATIVE-BASE.md",
    "The certified v3 foundation covers academic works and research projects. V3-A1 has now reintroduced a source-backed scientific-article normative contract without adding article runtime behavior. Article rules are manual/conditional during A1 and become implementation candidates only in V3-A2. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
    "The certified non-article v3 foundation covers academic works and research projects. V3-A1 reintroduced the source-backed scientific-article normative contract, and V3-A2 now activates the canonical `scientific-article` runtime against that unchanged source set. Article proof states remain manual/conditional until article-specific rule evidence is added and validated. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
)
replace_once(
    "docs/NORMATIVE-CURRENCY.md",
    "V3-A1 reconfirmed the corrected UFC scientific-article guide (2022, corrected file dated 2023-04-27) and ABNT NBR 6022:2018 as the current article-presentation basis. The guide's embedded NBR 10520:2002 and NBR 6023:2018 references are superseded for their technical domains by NBR 10520:2023 and NBR 6023:2025. The A1 contract therefore preserves compatible institutional article guidance while using current cross-cutting technical editions. No article runtime implementation is part of A1.",
    "V3-A1 reconfirmed the corrected UFC scientific-article guide (2022, corrected file dated 2023-04-27) and ABNT NBR 6022:2018 as the current article-presentation basis. The guide's embedded NBR 10520:2002 and NBR 6023:2018 references are superseded for their technical domains by NBR 10520:2023 and NBR 6023:2025. The A1 contract therefore preserves compatible institutional article guidance while using current cross-cutting technical editions. V3-A2 activates `scientific-article` runtime from that same authority set; activation changes implementation state, not source precedence, locators, modality, or proof state.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "- `research-projects.def`: research-project behavior;\n- `objects.def`: figures, charts, tables, listings, algorithms, captions, source/note handling;",
    "- `research-projects.def`: research-project behavior;\n- `articles.def`: canonical scientific-article front matter and article-only presentation behavior, reusing shared section/reference/summary infrastructure;\n- `objects.def`: figures, charts, tables, listings, algorithms, captions, source/note handling;",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "No article runtime module, profile implementation, template branch, validator shortcut or compatibility alias is introduced in A1. Cross-cutting citation/reference/section/table machinery remains shared rather than forked.",
    "A1 introduced no article runtime module, profile implementation, template branch, validator shortcut or compatibility alias. A2 now introduces `articles.def` as direct `scientific-article` ownership while cross-cutting citation/reference/section/table machinery remains shared rather than forked. Article-specific evidence is still required before proof promotion.",
)
replace_once(
    "docs/ARTICLE-NORMATIVE-CONTRACT.md",
    "A2 may implement only the canonical `scientific-article` profile and executable tests needed to realize the A1 rule set. It must reuse the current cross-cutting citation/reference/section/table machinery rather than fork it; preserve the certified non-article foundation; keep recommendation/optional semantics distinct from requirements; add positive and negative article-specific evidence before promoting proof state; and keep journal-specific instructions as a conditional boundary. Any source conflict discovered in A2 returns to source review instead of being resolved by runtime guesswork.",
    "A2 implements only the canonical `scientific-article` profile and executable tests needed to realize the A1 rule set. The runtime lot introduces direct article ownership and reuses current citation/reference/section/summary/table machinery rather than forking it. Recommendation/optional semantics remain distinct from requirements, journal-specific instructions remain a conditional boundary, and every article proof promotion still requires current positive/negative article-specific evidence. Any source conflict discovered in A2 returns to source review instead of being resolved by runtime guesswork.",
)
replace_once(
    "docs/ARTICLE-NORMATIVE-CONTRACT.md",
    "No article runtime implementation had started at the activation checkpoint.",
    "No article runtime implementation had started at the activation checkpoint; the first A2 runtime lot now implements the canonical profile without promoting article proof state.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "- A2 runtime implementation has not started yet.",
    "- A2 runtime implementation: **STARTED** in the bounded canonical-profile lot; article proof promotion remains pending article-specific evidence.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "Begin V3-A2/#280 from `7a7562d23e8bf6c92abb635718639d617a2ed6ff`. Implement only the canonical `scientific-article` profile bounded by `docs/ARTICLE-NORMATIVE-CONTRACT.md`: reuse cross-cutting infrastructure, preserve required/optional/recommended/conditional semantics, and add article-specific fail-closed evidence before any proof-state promotion.",
    "Continue V3-A2/#280 from its exact entry `7a7562d23e8bf6c92abb635718639d617a2ed6ff`. The canonical `scientific-article` runtime/profile-matrix lot is in progress; next add article-specific fail-closed rule evidence, then promote only the rules actually proven by that evidence.",
)
replace_once(
    "README.md",
    "A1 closed through PR #281 at `7a7562d23e8bf6c92abb635718639d617a2ed6ff` after PR #279 established the current source-backed 18-rule article contract. V3-A2/#280 is now active and owns the bounded `scientific-article` implementation: required, optional, recommended and conditional semantics must remain distinct, and article proof may advance only from article-specific evidence. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
    "A1 closed through PR #281 at `7a7562d23e8bf6c92abb635718639d617a2ed6ff` after PR #279 established the current source-backed 18-rule article contract. V3-A2/#280 is active and the canonical `scientific-article` runtime/profile-matrix lot is now implemented on its bounded branch. Required, optional, recommended and conditional semantics remain distinct; article proof still advances only from article-specific evidence. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
)
replace_once(
    "AGENTS.md",
    "V3-A2/#280 is ACTIVE from that SHA; runtime implementation has not started yet. A2 must implement only canonical `scientific-article`, reuse cross-cutting infrastructure, preserve modality, and require article-specific evidence before proof promotion.",
    "V3-A2/#280 is ACTIVE from that SHA; the canonical `scientific-article` runtime/profile-matrix lot has started. A2 must reuse cross-cutting infrastructure, preserve modality, and require article-specific evidence before proof promotion.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| V3-A2 | ACTIVE | issue #280; exact entry `7a7562d23e8bf6c92abb635718639d617a2ed6ff`; A1 contract `4d018a92697e8f39e3a53b034c451e55996c84fb` | bounded `scientific-article` implementation/test contract active | implement runtime/profile + article-specific evidence; keep CTAN blocked |",
    "| V3-A2 | ACTIVE | issue #280; exact entry `7a7562d23e8bf6c92abb635718639d617a2ed6ff`; A1 contract `4d018a92697e8f39e3a53b034c451e55996c84fb` | canonical runtime/profile-matrix lot implemented; proof state unchanged | add rule-specific article evidence + safe negatives; reconcile contribution; keep CTAN blocked |",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "A2 begins from exact predecessor `7a7562d23e8bf6c92abb635718639d617a2ed6ff` and source-contract product `4d018a92697e8f39e3a53b034c451e55996c84fb` while preserving certified non-article foundation `c79f3c73f1d51a30175e8259269504d029442a1c`. A2 may implement only the canonical `scientific-article` profile. Required predicates may become enforceable only with article-specific positive evidence and safe negative rejection where applicable. Optional/recommended predicates remain non-mandatory, and journal-specific instructions remain a conditional applicability boundary.",
    "A2 begins from exact predecessor `7a7562d23e8bf6c92abb635718639d617a2ed6ff` and source-contract product `4d018a92697e8f39e3a53b034c451e55996c84fb` while preserving certified non-article foundation `c79f3c73f1d51a30175e8259269504d029442a1c`. The first bounded lot introduces the canonical `scientific-article` runtime, article-only front matter and profile-matrix coverage while reusing shared cross-cutting infrastructure. Article proof state is unchanged. The next lot must add article-specific positive evidence and safe negative rejection where applicable before any required predicate is promoted; optional/recommended predicates remain non-mandatory and journal-specific instructions remain conditional.",
)

print("A2 runtime implementation mutation prepared successfully.")

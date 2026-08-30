# Engineering Language Policy

Updated: 2026-08-30

## Rule

`abntexto-ufc` v3 uses **English as the canonical engineering language**.

This policy applies to project-owned engineering artifacts and identifiers. It does not require translating the academic document produced by the template.

## Engineering surfaces that must be English

### Repository structure

- directory names;
- project-owned filenames;
- test/fixture/checker names;
- workflow filenames;
- tool/script filenames;
- active documentation filenames.

### LaTeX project API

- `\ufcsetup` keys;
- project-owned setup values;
- public commands;
- public environments;
- project-owned hooks;
- project-owned helper/exported commands;
- project-owned internal control-sequence names;
- project-owned internal state identifiers.

### Source code

- comments;
- doc comments;
- diagnostic messages;
- exception/error messages;
- CLI help strings;
- CI step/job names;
- Makefile technical messages;
- project-owned JSON field names and schema terminology.

### Engineering documentation

- architecture descriptions;
- API documentation;
- build instructions;
- test instructions;
- release procedures;
- migration procedures;
- maintainership/handoff documentation.

## Content that may remain in Portuguese

The following is content rather than engineering nomenclature and may remain in Portuguese when appropriate:

- body text in the reference academic document;
- sample title/subtitle/author/advisor/course/program/institution values;
- dedication, acknowledgments, epigraph and summary prose;
- section headings in the academic document;
- bibliography entries;
- required Portuguese labels in a Portuguese-language UFC academic work;
- official names of institutions, units, resolutions, instructions, guides and standards;
- normative/institutional excerpts or source titles whose authoritative wording is Portuguese;
- fixture payload text when the Portuguese output itself is under test;
- validator UI strings when intentionally localized for Portuguese users.

Example:

```tex
\ufcsetup{
  type = doctoral-thesis,
  institution = {Universidade Federal do Ceará},
  doctoral-graduate-program = {Programa de Pós-Graduação em Ciência da Computação},
  title = {Título acadêmico escrito em português},
  location = {Fortaleza}
}
```

Here the engineering identifiers are English while the academic metadata values remain naturally Portuguese.

## Filename/content distinction

A file may have an English engineering filename and Portuguese academic content.

Correct:

```text
template/frontmatter/acknowledgments.tex
```

whose content may begin with Portuguese acknowledgments.

Correct:

```text
template/chapters/1-introduction.tex
```

whose rendered section may be:

```tex
\section{Introdução}
```

The filename is an engineering artifact; `Introdução` is document content.

## Comments in `.def` and `.cls`

All project-owned source comments must explain intent in English.

Preferred:

```tex
% Keep the approval-page committee block within the printable text area.
```

Not allowed in active v3 runtime:

```tex
% Mantém a banca dentro da área útil da página.
```

Comments should explain **why** a rule or workaround exists, not merely restate the code.

For standard/institutional behavior, comments should identify provenance where useful:

```tex
% NBR 6023:2025 allows the event city to be omitted in this reference form.
```

## Runtime text versus diagnostics

Rendered academic strings may be Portuguese because they are output content:

```tex
Aprovada em:
BANCA EXAMINADORA
```

Technical diagnostics must be English:

```tex
\ClassError{abntexto-ufc}
  {Unsupported~document~type}
  {Use~one~of~the~document~types~documented~in~the~public~API.}
```

## Upstream exceptions

This policy does not rename identifiers owned by external dependencies.

If `abntexto`, `biblatex-abnt`, another LaTeX package, or an institutional data source exposes an identifier that is not English, project code may reference that identifier when necessary.

Such identifiers must not be re-exported as canonical project API merely for convenience.

## Historical evidence

Git history, existing tags/releases and historical source records may contain Portuguese engineering identifiers because they describe previous versions.

Active v3 runtime and active v3 engineering documentation must not keep obsolete aliases solely to preserve that history.

## Automated enforcement

V3-R3/R4 must introduce checks that distinguish project engineering text from allowed content rather than naively rejecting every Portuguese word.

Minimum enforced invariants:

- project-owned active path names in Portuguese: 0;
- removed Portuguese v2 public API identifiers in active runtime: 0;
- project-owned active source comments in Portuguese: 0;
- project-owned active technical diagnostic strings in Portuguese: 0;
- canonical technical examples using removed Portuguese API: 0.

The checker must use scoped rules/exemptions for academic content, official source titles and upstream identifiers. A broad repository-wide Portuguese word blacklist is not acceptable because it would incorrectly reject valid Portuguese academic content.

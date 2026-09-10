\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{abntexto-ufc}[2026/09/09 v3.0.1 UFC academic document class]

% Historical UFC template: Ednardo Moreira Rodrigues and Alan Batista de Oliveira.
% Historical v2 redesign and maintenance: Tiago Guimarães Sombra.
% Historical lineage adapted from ueceTeX2 by Thiago Nascimento.
% Distributed under LPPL 1.3c or later; see LICENSE.
% Normative policy and current technical basis: docs/NORMATIVE-BASE.md.
% Always target the latest applicable ABNT edition.

\LoadClass[12pt]{abntexto}

\makeatletter
\@ifclasslater{abntexto}{2026/05/07}{}{%
  \ClassError{abntexto-ufc}
    {abntexto 1.1 or newer is required}
    {Update the TeX distribution before compiling abntexto-ufc.}%
}
\makeatother

% NBR 6023:2025 requires repeated authorship to be rendered explicitly.
\PassOptionsToPackage{repeatfields=true}{biblatex}

\input{abntexto-ufc/core.def}
\input{abntexto-ufc/fonts.def}
\input{abntexto-ufc/layout.def}
\input{abntexto-ufc/modules.def}
\input{abntexto-ufc/frontmatter.def}
\input{abntexto-ufc/institutional.def}
\input{abntexto-ufc/academic-works.def}
\input{abntexto-ufc/articles.def}
\input{abntexto-ufc/research-projects.def}
\input{abntexto-ufc/objects.def}
\input{abntexto-ufc/integrations/abntexto.def}
\input{abntexto-ufc/bibliography.def}
\input{abntexto-ufc/standards/nbr6023-2025.def}
\input{abntexto-ufc/backmatter.def}

\endinput
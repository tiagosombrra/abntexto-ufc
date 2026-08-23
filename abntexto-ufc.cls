\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{abntexto-ufc}[2026/08/23 v2.1.0 UFC academic document class]

% Historical UFC template: Ednardo Moreira Rodrigues and Alan Batista de Oliveira.
% V2 redesign and maintenance: Tiago Guimarães Sombra.
% Historical lineage adapted from ueceTeX2 by Thiago Nascimento.
% Distributed under LPPL 1.3c or later; see LICENSE.
% Normative policy and version matrix: docs/NORMAS.md.
% Always target the latest applicable ABNT edition.

\LoadClass[12pt]{abntexto}

\makeatletter
\@ifclasslater{abntexto}{2026/05/07}{}{%
  \ClassError{abntexto-ufc}
    {abntexto 1.1 or newer is required}
    {Update the TeX distribution before compiling abntexto-ufc.}%
}
\makeatother

\input{ufctex/core.def}
\input{ufctex/fontes.def}
\input{ufctex/layout.def}
\input{ufctex/modulos.def}
\input{ufctex/pretextuais.def}
\input{ufctex/institucional.def}
\input{ufctex/trabalhos.def}
\input{ufctex/projetos.def}
\input{ufctex/objetos.def}
\input{ufctex/compat-abntexto.def}
\input{ufctex/bibliografia.def}
\input{ufctex/compat-nbr6023-2025.def}
\input{ufctex/postextuais.def}

\endinput

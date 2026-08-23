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

\input{abntexto-ufc/core.def}
\input{abntexto-ufc/fontes.def}
\input{abntexto-ufc/layout.def}
\input{abntexto-ufc/modulos.def}
\input{abntexto-ufc/pretextuais.def}
\input{abntexto-ufc/institucional.def}
\input{abntexto-ufc/trabalhos.def}
\input{abntexto-ufc/projetos.def}
\input{abntexto-ufc/objetos.def}
\input{abntexto-ufc/compat-abntexto.def}
\input{abntexto-ufc/bibliografia.def}
\input{abntexto-ufc/compat-nbr6023-2025.def}
\input{abntexto-ufc/postextuais.def}

\endinput

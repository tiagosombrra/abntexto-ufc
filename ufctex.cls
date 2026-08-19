\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ufctex}[2026/08/18 v2.0.0-dev UFC academic document class]

% Normative policy and version matrix: docs/NORMAS.md.
% Always target the latest applicable ABNT edition.

\LoadClass[12pt]{abntexto}

\makeatletter
\@ifclasslater{abntexto}{2026/05/07}{}{%
  \ClassError{ufctex}
    {abntexto 1.1 or newer is required}
    {Update the TeX distribution before compiling ufctex v2.}%
}
\makeatother

\input{ufctex/core.def}
\input{ufctex/layout.def}
\input{ufctex/modulos.def}
\input{ufctex/pretextuais.def}
\input{ufctex/objetos.def}
\input{ufctex/bibliografia.def}
\input{ufctex/compat-nbr6023-2025.def}

\endinput

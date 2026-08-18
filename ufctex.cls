\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ufctex}[2026/08/18 v2.0.0-dev UFC academic document class]

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
\input{ufctex/pretextuais.def}

\endinput

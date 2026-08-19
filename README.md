# Modelo LaTeX UFC

Template comunitário para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), com uma classe própria baseada em `abntexto`.

> A V2 está em desenvolvimento como `2.0.0-dev`. A linha estável 1.x permanece preservada na branch `1.x`.

Este projeto não é um modelo oficial da UFC. Antes da entrega, confira as orientações vigentes do Sistema de Bibliotecas, do curso, do programa e do edital aplicável.

## V2

A V2 substitui a arquitetura histórica baseada diretamente em `abntex2` por:

```text
documento.tex
    |
    +-- ufctex.cls
          +-- core.def
          +-- layout.def
          +-- modulos.def
          +-- pretextuais.def
          +-- projetos.def
          +-- objetos.def
          +-- bibliografia.def
          +-- postextuais.def
          +-- compat-abntexto.def
          +-- compat-nbr6023-2025.def
          +-- compat-v1.def
```

`ufctex` requer `abntexto` 1.1 ou superior. A política normativa e a matriz de implementação estão em `docs/NORMAS.md`.

## Uso rápido

O ponto de entrada é `documento.tex`:

```tex
\documentclass{ufctex}

\ufcsetup{
  tipo = tccgraduacao,
  impressao = anverso,
  autor = {Nome Sobrenome},
  titulo = {Título do Trabalho},
  local = {Fortaleza},
  ano = {2026}
}
```

Depois:

1. escolha o perfil do documento;
2. preencha os metadados em `\ufcsetup`;
3. edite os arquivos em `1-pre-textuais`, `2-textuais` e `3-pos-textuais`;
4. mantenha `documento.tex` como arquivo principal;
5. compile e revise o PDF final.

## Perfis

| Perfil | Uso |
|---|---|
| `tccgraduacao` | trabalho de graduação |
| `tccespecializacao` | trabalho de especialização |
| `dissertacao` | dissertação de mestrado |
| `tese` | tese de doutorado |
| `projeto` | projeto de pesquisa identificado |
| `projetoanonimizado` | projeto de pesquisa com identificação pessoal suprimida |

A impressão pode ser configurada como `anverso` ou `frente-verso`.

## Estrutura textual

O perfil normativo V2 é baseado em seções. Use:

```tex
\section{Introdução}
\subsection{Fundamentação}
\subsubsection{Detalhamento}
```

`\chapter` não faz parte do perfil V2.

## Elementos pré-textuais

Exemplo:

```tex
\pretextual
\imprimircapa
\imprimirfolhaderosto
\imprimirfolhadeaprovacao
\imprimirdedicatoria{1-pre-textuais/dedicatoria}
\imprimiragradecimentos{1-pre-textuais/agradecimentos}
\imprimirepigrafe{1-pre-textuais/epigrafe}
\imprimirresumo{1-pre-textuais/resumo}
\imprimirabstract{1-pre-textuais/abstract}
\imprimirlistadeilustracoes
\imprimirlistadetabelas
\imprimirsumario
```

A Lista de Ilustrações reúne figuras, gráficos e quadros na ordem de ocorrência. Tabelas permanecem em lista própria. Listas específicas de figuras, gráficos e quadros também estão disponíveis.

## Objetos

A API principal usa as áreas de legenda do `abntexto`:

```tex
\legend{figure}{Título da figura}
\ufcfonte{Elaboração própria.}
\ufcnota{Nota opcional.}
\label{fig:exemplo}
\begin{ufcobjeto}[here]
  \centering
  \includegraphics[width=.8\linewidth]{figuras/exemplo}
\end{ufcobjeto}
```

O mesmo padrão é usado para `table`, `quadro`, `grafico`, `codigo` e `algoritmo`, conforme o módulo habilitado.

## Módulos opcionais

```tex
\ufcsetup{
  tabelas = tabularray,
  codigo = listings,
  algoritmos = algpseudocodex,
  glossario = glossaries,
  indice = imakeidx
}
```

Valores principais:

- `tabelas`: `nativo` ou `tabularray`;
- `codigo`: `nenhum`, `listings` ou `minted`;
- `algoritmos`: `nenhum` ou `algpseudocodex`;
- `glossario`: `nenhum` ou `glossaries`;
- `indice`: `nenhum` ou `imakeidx`.

`minted` exige o suporte externo correspondente no ambiente de compilação.

## Citações e referências

A V2 usa `biblatex` com Biber e estilo ABNT:

```tex
\ufcbibliografia{3-pos-textuais/referencias.bib}
```

No texto:

```tex
\textcite{chave}
\parencite{chave}
```

Ao final:

```tex
\imprimirreferencias
```

A camada `compat-nbr6023-2025.def` mantém isolados os ajustes transitórios necessários enquanto o suporte equivalente não estiver disponível no upstream.

## Pós-textuais

```tex
\imprimirreferencias
\imprimirglossario

\appendix{Título do apêndice}
\annex{Título do anexo}

\imprimirindice
```

Apêndices, anexos, glossário e índice são opcionais.

## Compilação

Fluxo padrão:

```bash
make
```

O `Makefile` usa pdfLaTeX por padrão e executa Biber, glossários e índice quando configurados pelo documento de referência.

LuaLaTeX:

```bash
make lua
```

Validação completa:

```bash
make preflight
```

A suíte V2 cobre layout, geometria do PDF, pré-textuais, objetos, bibliografia, projetos, perfis, pós-textuais e compatibilidade pública da linha anterior. O gate externo usa TeX Live 2026.

## Overleaf

Importe o projeto completo e mantenha `documento.tex` como arquivo principal. Use uma versão recente do TeX Live que contenha `abntexto` 1.1 ou superior. pdfLaTeX é o caminho padrão; LuaLaTeX também é suportado.

Caso use `minted`, habilite o fluxo exigido por esse pacote no ambiente de compilação.

## Migração da V1

A V2 é uma mudança de plataforma. Para documentos novos, não carregue `lib/preambulo.tex` nem use `abntex2` diretamente.

Principais mudanças:

| V1 | V2 |
|---|---|
| `\documentclass{abntex2}` | `\documentclass{ufctex}` |
| `\input{lib/preambulo}` | removido do documento principal |
| configuração histórica distribuída | `\ufcsetup{...}` |
| `\chapter` como nível principal | `\section` |
| helpers `\UFCfig`, `\UFCtab`, `\UFCqua` | `\legend` + `\ufcfonte` + `ufcobjeto` |
| configuração bibliográfica no preâmbulo | `\ufcbibliografia{arquivo.bib}` |

A camada `compat-v1.def` existe para facilitar transição e regressão, mas não define o estilo recomendado para documentos novos.

## Compatibilidade

A V2 é validada com pdfLaTeX e LuaLaTeX. O desenvolvimento local pode usar uma distribuição mais nova, mas a certificação do projeto é feita no ambiente definido pelo GitHub Actions com TeX Live 2026 e `abntexto` estável.

## Normas

Consulte `docs/NORMAS.md` para:

- edições normativas adotadas;
- precedência entre ABNT e requisitos institucionais;
- mapa norma → implementação;
- patches temporários de compatibilidade;
- política dos gates de validação.

Não declare conformidade apenas porque o documento compilou. A revisão final deve considerar as exigências específicas aplicáveis ao trabalho.

## Linha 1.x

A última série baseada diretamente em `abntex2` permanece disponível na branch `1.x` para manutenção e documentos legados. Novos documentos devem usar a V2 após a publicação da versão 2.0.0.

## Licença

Consulte `LICENSE`.

# ufctex

Classe LaTeX para trabalhos acadêmicos da Universidade Federal do Ceará, baseada em `abntexto`.

Versão publicada atual: **2.0.0**.

A linha 2.x reorganiza a implementação em módulos, preserva a API pública da V1 quando possível e acompanha a base normativa vigente auditada em agosto de 2026.

## Requisitos

- TeX Live 2026 recomendado para desenvolvimento e CI;
- `abntexto` 1.1 ou superior;
- `biblatex` + `biber`;
- pacotes opcionais apenas quando os módulos correspondentes forem ativados.

A versão estável pública do Overleaf consultada em 20/08/2026 ainda utiliza TeX Live 2025. Como `abntexto` 1.1 foi publicado em 2026, o ambiente estável não deve ser tratado como possuindo essa versão nativamente. A compatibilidade é exercitada em CI com TeX Live 2025 e uma cópia íntegra e pinada de `abntexto.cls` 1.1. O bundle específico para importação no Overleaf será preparado na fase de distribuição.

## Estrutura

```text
ufctex.cls
ufctex/
├── core.def
├── fontes.def
├── layout.def
├── modulos.def
├── pretextuais.def
├── institucional.def
├── projetos.def
├── trabalhos.def
├── objetos.def
├── bibliografia.def
├── compat-nbr6023-2025.def
├── postextuais.def
└── compat-v1.def
```

`fontes.def` concentra política de engine, família textual, fallback, modo estrito e família matemática complementar. `layout.def` permanece responsável por papel, margens, espaçamento e paginação.

## Configuração básica

```tex
\documentclass{ufctex}

\ufcsetup{
  tipo = tese,
  impressao = anverso,
  fonte = times,
  fonte-estrita = nao,
  ficha-catalografica = nao,
  area-concentracao = {Computação Gráfica},
  programa = {Programa de Pós-Graduação em Ciência da Computação},
  unidade-academica = {Centro de Ciências},
  grau = {Doutor},
  titulacao = {Doutorado},
  tipo-tcc = {Trabalho de Conclusão de Curso},
  edital = {Processo seletivo},
  volume = {},
  pagina-inicial = 1,
  tabelas = nativo,
  codigo = nenhum,
  algoritmos = nenhum,
  glossario = nenhum,
  indice = nenhum
}
```

## Perfis

| Perfil | Uso |
|---|---|
| `tccgraduacao` | trabalho de graduação |
| `tccespecializacao` | trabalho de especialização |
| `dissertacao` | dissertação de mestrado |
| `tese` | tese de doutorado |
| `projeto` | projeto de pesquisa identificado |
| `projetoanonimizado` | projeto de pesquisa com dados pessoais suprimidos |

A impressão pode ser `anverso` ou `frente-verso`.

## Fonte tipográfica

O Guia UFC admite **Times New Roman ou Arial**. A V2 oferece:

```tex
\ufcsetup{
  fonte = times,
  fonte-estrita = nao
}
```

Valores de `fonte`:

- `times` → Times New Roman;
- `arial` → Arial.

A chave `fonte-estrita` define a política de identidade:

- `sim`: exige a família literal solicitada; a compilação falha se o suporte necessário não estiver disponível ou se o engine não conseguir usar a fonte;
- `nao`: permite fallback de compatibilidade para portabilidade e desenvolvimento.

Em modo não estrito, os fallbacks são explicitamente tratados como substitutos e **não** como Times New Roman/Arial:

- pdfLaTeX + `times`: NewTX;
- pdfLaTeX + `arial`: TeX Gyre Heros;
- LuaLaTeX + `times`: TeX Gyre Termes;
- LuaLaTeX + `arial`: TeX Gyre Heros.

Para declarar conformidade tipográfica final com o requisito UFC, use a família literal e verifique o PDF produzido. O modo estrito existe para essa certificação.

No LuaLaTeX, Times New Roman e Arial literais são resolvidas por `fontspec` a partir das fontes disponíveis ao sistema. No pdfLaTeX, o modo estrito usa o suporte local preparado por `tools/prepare-windows-fonts.ps1`: o script gera TFM/VF/FD, encodings Unicode e `ufctex-windows.map` a partir das fontes Microsoft instaladas no Windows. As fontes proprietárias não são redistribuídas pelo `ufctex`.

Independentemente do engine, o PDF certificado deve ser autocontido: todas as fontes efetivamente utilizadas precisam aparecer como `emb=yes` em `pdffonts`. Incorporação por subconjunto é aceita; `emb=no` reprova o artefato. A validação PDF/A com veraPDF é aplicada adicionalmente nos gates de release.

`rmfamily`, `sffamily` e `ttfamily` permanecem na família institucional selecionada. Isso inclui URLs, `listings`, `minted` e outros usos de `ttfamily`.

A matemática usa uma família matemática complementar. pdfLaTeX usa NewTX Math; LuaLaTeX prefere TeX Gyre Termes Math e pode usar Latin Modern Math como fallback técnico. Essas famílias matemáticas não são apresentadas como Times New Roman ou Arial.

## Trabalhos em mais de um volume

Quando houver mais de um volume:

```tex
\ufcsetup{
  volume = {2},
  pagina-inicial = 101
}
```

`volume` é impresso na capa e na folha de rosto dos trabalhos acadêmicos. `pagina-inicial` permite manter paginação contínua entre os volumes.

## Frente e verso

No modo `frente-verso`, a V2 aplica margens espelhadas ao miolo:

- anverso: esquerda/superior 3 cm; direita/inferior 2 cm;
- verso: direita/superior 3 cm; esquerda/inferior 2 cm;
- paginação à direita no anverso e à esquerda no verso;
- pré-textuais, exceto ficha catalográfica, iniciam em anverso;
- seções textuais primárias e pós-textuais controlados pela V2 iniciam no anverso.

## Ficha catalográfica

Em 2026, a representação visual da ficha tornou-se facultativa no contexto institucional consultado. O padrão é:

```tex
ficha-catalografica = nao
```

Quando ativada:

```tex
ficha-catalografica = sim
```

use:

```tex
\imprimirfichacatalografica{caminho/para/ficha}
```

A página física destinada aos dados catalográficos não incrementa a contagem lógica e permanece sem numeração. Em `frente-verso`, a classe preserva também a paridade física correta.

A ficha é um PDF externo: sua tipografia deve ser verificada no próprio arquivo e a inclusão exige nova validação PDF/A do documento final.

## Estrutura textual

A V2 usa `\section` como nível textual primário:

```tex
\section{Introdução}
\subsection{Fundamentação}
\subsubsection{Detalhamento}
```

`\chapter` não faz parte do perfil normativo V2.

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
\imprimirlistadeabreviaturasesiglas{1-pre-textuais/lista-de-abreviaturas-e-siglas}
\imprimirlistadesimbolos{1-pre-textuais/lista-de-simbolos}
\imprimirsumario
```

A folha de aprovação gerada pela classe contém linhas e identificação da banca, mas não incorpora imagens de assinatura.

O resumo e o abstract distribuídos ficam na faixa de 150 a 500 palavras e usam palavras-chave após o texto.

Quando o trabalho decorrer de atividade financiada total ou parcialmente pela CAPES, consulte o comentário em `1-pre-textuais/agradecimentos.tex` e preserve o agradecimento obrigatório aplicável.

## Objetos

A API principal usa a infraestrutura de legenda do `abntexto`:

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

Título, Fonte e Nota são limitados à largura física do objeto e usam tamanho reduzido. A fonte deve ser informada inclusive em conteúdo de elaboração própria; fontes externas devem ser citadas conforme a NBR 10520.

A Lista de Ilustrações agrega figuras, gráficos e quadros. Tabelas permanecem em lista própria.

## Tabelas

Para tabelas numéricas, habilite:

```tex
\ufcsetup{
  tabelas = tabularray
}
```

O perfil usa `tabularray-abnt` e preserva o subconjunto tabular IBGE auditado: tabela numérica aberta nas laterais, sem grade horizontal no corpo e com regras superior, de separação do cabeçalho e inferior.

Exemplo:

```tex
\begin{tallabnttblr}
[
  caption={Indicadores},
  label={tab:indicadores},
  remark{Fonte}={Elaboração própria.},
]
{
  colspec={XX[r]},
  row{even}={bg=black!5},
}
\toprule
Item & Valor \\
\midrule
A & 10 \\
B & 12 \\
\bottomrule
\end{tallabnttblr}
```

O corpo da tabela permanece em tamanho 12. Legenda, Fonte e Nota usam tamanho reduzido uniforme. A opção de zebra é editorial e não é aplicada automaticamente.

## Código e algoritmos

Ative apenas o módulo necessário:

```tex
\ufcsetup{codigo = listings}
```

ou:

```tex
\ufcsetup{codigo = minted}
```

Para pseudocódigo:

```tex
\ufcsetup{algoritmos = algpseudocodex}
```

Código e algoritmos usam tamanho 12 por padrão e permanecem na família institucional selecionada, inclusive quando o pacote usa internamente `\ttfamily`.

## Glossário e índice

```tex
\ufcsetup{
  glossario = glossaries,
  indice = imakeidx
}
```

A V2 cria glossário e índice somente quando os módulos são ativados.

## Referências

```tex
\ufcbibliografia{referencias/referencias.bib}
```

A bibliografia usa `biblatex-abnt` e `biber`. O projeto mantém um adaptador isolado para os pontos da NBR 6023:2025 ainda não cobertos pelo upstream no escopo testado.

## PDF/A

O documento de referência usa:

```tex
\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}
```

O PDF final deve ser validado como PDF/A antes do depósito. A V2 usa PDF/A-2b como perfil técnico verificável; esse subtipo é uma decisão de implementação do projeto, não uma exigência específica atribuída à UFC.

Além da validação PDF/A, os gates verificam que todas as fontes presentes no PDF estão incorporadas. Isso vale também para recursos externos incluídos no documento final, como uma ficha catalográfica em PDF.

## Build

```bash
make compile
```

Por padrão, o engine é `pdflatex`.

Para LuaLaTeX:

```bash
make compile ENGINE=lualatex
```

Limpeza:

```bash
make clean
```

Preflight da V2:

```bash
make preflight
```

Preflight de release com PDF/A:

```bash
make release-preflight
```

## CI

O workflow principal é `.github/workflows/latex-preflight.yml`.

O gate obrigatório em TeX Live 2026 cobre:

- documento de referência;
- estrutura, layout, política de fontes e geometria;
- objetos, código, algoritmos, tabelas e bibliografia;
- matriz de seis perfis em pdfLaTeX e LuaLaTeX;
- pós-textuais e compatibilidade V1;
- 12 PDFs da matriz;
- validação PDF/A-2b dos PDFs de referência e da matriz.

O Gate T integra a validação Windows obrigatória nas branches V2: Times New Roman e Arial literais são compiladas em pdfLaTeX e LuaLaTeX, incluindo regular, negrito, itálico e negrito-itálico. Os quatro PDFs estritos são verificados quanto à identidade da família, ausência de fallback textual, extração Unicode, incorporação (`emb=yes`) e conformidade PDF/A-2b com veraPDF.

O proxy Overleaf usa TeX Live 2025 com `abntexto` 1.1 pinado para detectar incompatibilidades com o ambiente público estável. Ele integra o Gate T nas branches V2 e não substitui o smoke final dentro do serviço Overleaf.

## Compatibilidade V1

A V2 não é uma cópia estrutural da linha 1.x. O objetivo da camada `compat-v1.def` é reduzir custo de migração de conteúdo, não preservar internamente a arquitetura antiga.

APIs antigas bloqueadas ou adaptadas são cobertas por regressões próprias.

## Licença

Consulte `LICENSE`.

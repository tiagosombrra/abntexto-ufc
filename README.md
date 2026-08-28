# abntexto-ufc

Classe LaTeX para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), baseada em `abntexto`.

Versão publicada atual: **2.1.0**.

A identidade canônica atual do projeto é **`abntexto-ufc`**. O desenvolvimento da linha **2.2.0** concentra a verificação normativa e a adequação da distribuição para o CTAN.

## Requisitos

- TeX Live 2026 recomendado para desenvolvimento e CI;
- `abntexto` 1.1 ou superior;
- `biblatex` + `biber`;
- `newtx` no pdfLaTeX e fontes TeX Gyre no LuaLaTeX/XeLaTeX para os perfis portáteis;
- `tabularray-abnt` de 08/08/2025 ou mais recente quando `tabelas = tabularray`;
- pacotes opcionais apenas quando os módulos correspondentes forem ativados.

O bundle específico para Overleaf inclui uma cópia íntegra e pinada de `abntexto.cls` 1.1 quando necessário para compatibilidade com ambientes que ainda não o ofereçam.

## Estrutura

O documento de referência e os bundles completos usam o seguinte layout canônico:

```text
main.tex
frontmatter/
chapters/
backmatter/
figures/
abntexto-ufc.cls
abntexto-ufc/
├── core.def
├── fonts.def
├── layout.def
├── modules.def
├── frontmatter.def
├── institutional.def
├── academic-works.def
├── research-projects.def
├── objects.def
├── bibliography.def
├── compat-abntexto.def
├── compat-nbr6023-2025.def
└── backmatter.def
```

`main.tex` é o ponto de entrada padrão para compilação local e para importação no Overleaf. Os diretórios `frontmatter/`, `chapters/`, `backmatter/` e `figures/` organizam o conteúdo editável do exemplo. Cada responsabilidade da classe fica concentrada em um módulo interno; `compat-abntexto.def` e `compat-nbr6023-2025.def` tratam adaptações correntes ao upstream e ao escopo testado da norma de referências.

## Uso básico

Exemplo para uma tese:

```tex
\documentclass{abntexto-ufc}

\ufcsetup{
  tipo = tese,
  impressao = anverso,
  capa = auto,
  ficha-catalografica = nao,
  brasao = sim,
  fonte = times,
  fonte-estrita = nao,
  programa-doutorado = {Programa de Pós-Graduação em Ciência da Computação},
  titulo-doutor = {Ciência da Computação},
  area-doutorado = {Computação Gráfica},
  autor = {Nome Sobrenome},
  titulo = {Título do Trabalho},
  local = {Fortaleza},
  ano = {2026},
  orientador = {Prof. Dr. Nome do Orientador},
  volume = {},
  pagina-inicial = 1,
  tabelas = nativo,
  codigo = nenhum,
  algoritmos = nenhum,
  glossario = nenhum,
  indice = nenhum
}
```

Perfis disponíveis:

| Perfil | Uso |
|---|---|
| `tccgraduacao` | trabalho de graduação |
| `tccespecializacao` | trabalho de especialização |
| `dissertacao` | dissertação de mestrado |
| `tese` | tese de doutorado |
| `projeto` | projeto de pesquisa identificado |
| `projetoanonimizado` | projeto de pesquisa com dados pessoais suprimidos |

A impressão pode ser `anverso` ou `frente-verso`.

## Brasão institucional

A composição pode ser controlada por:

```tex
\ufcsetup{
  brasao = sim,
  brasao-arquivo = {caminho/para/brasao-oficial.png}
}
```

Os bundles públicos gerados de classe, template, Overleaf e CTAN não redistribuem o brasão real da UFC. Nos bundles de template e Overleaf, `main.tex` é distribuído com `brasao = nao` para compilar sem depender de um ativo institucional não incluído. O usuário pode obter o ativo oficial diretamente da Universidade e ativá-lo localmente com `brasao = sim` e `brasao-arquivo`.

A política de redistribuição do ativo institucional é independente da regra normativa de composição da capa e não remove o suporte da classe a um brasão oficial fornecido localmente.

## Tipografia

O perfil UFC admite Times New Roman ou Arial:

```tex
\ufcsetup{
  fonte = times,
  fonte-estrita = nao
}
```

Valores de `fonte`:

- `times` — Times New Roman;
- `arial` — Arial.

`fonte-estrita = sim` exige a família literal. `fonte-estrita = nao` permite fallback portátil quando a fonte literal não estiver disponível.

No LuaLaTeX, Times New Roman e Arial podem ser resolvidas via `fontspec`. No pdfLaTeX, o modo estrito usa suporte local produzido por `tools/prepare-windows-fonts.ps1` a partir das fontes Microsoft já instaladas no Windows. As fontes proprietárias não são redistribuídas pelo projeto.

O Gate T valida identidade tipográfica literal no Windows, incorporação de fontes e PDF/A-2b nos cenários certificados.

## Trabalhos em mais de um volume

```tex
\ufcsetup{
  volume = {2},
  pagina-inicial = 101
}
```

`volume` é impresso na capa e na folha de rosto. `pagina-inicial` permite manter a paginação contínua entre volumes.

## Frente e verso

No modo `frente-verso`, a classe aplica margens espelhadas e as regras correspondentes de início em anverso para os elementos controlados pelo perfil.

## Ficha catalográfica

O padrão atual é:

```tex
\ufcsetup{ficha-catalografica = nao}
```

Quando aplicável:

```tex
\ufcsetup{ficha-catalografica = sim}
\imprimirfichacatalografica{caminho/para/ficha}
```

A ficha é tratada como PDF externo; sua conformidade deve ser avaliada no documento final.

## Estrutura textual

A linha V2 usa `\section` como nível textual primário:

```tex
\section{Introdução}
\subsection{Fundamentação}
\subsubsection{Detalhamento}
```

`\chapter` não faz parte do perfil normativo V2.

## Elementos pré-textuais

```tex
\pretextual

\imprimircapa
\imprimirfolhaderosto
\imprimirerrata{frontmatter/errata}
\imprimirfolhadeaprovacao
\imprimirdedicatoria{frontmatter/dedicatoria}
\imprimiragradecimentos{frontmatter/agradecimentos}
\imprimirepigrafe{frontmatter/epigrafe}
\imprimirresumo{frontmatter/resumo}
\imprimirabstract{frontmatter/abstract}
\imprimirlistadeilustracoes
\imprimirlistadetabelas
\imprimirlistadecodigos
\imprimirlistadealgoritmos
\imprimirlistadeabreviaturasesiglas{frontmatter/lista-de-abreviaturas-e-siglas}
\imprimirlistadesimbolos{frontmatter/lista-de-simbolos}
\imprimirsumario
```

## Figuras, gráficos, quadros e outros objetos

A API principal usa a infraestrutura de objetos de `abntexto`:

```tex
\legend{figure}{Título da figura}
\ufcfonte{Elaboração própria.}
\ufcnota{Nota opcional.}
\label{fig:exemplo}
\begin{ufcobjeto}[here]
  \centering
  \includegraphics[width=.8\linewidth]{figures/exemplo}
\end{ufcobjeto}
```

O primeiro argumento de `\legend` pode ser `figure`, `grafico`, `quadro`, `codigo` ou `algoritmo`, conforme o objeto.

## Tabelas

O módulo `tabularray` pode ser ativado por:

```tex
\ufcsetup{tabelas = tabularray}
```

Linhas alternadas e outros recursos editoriais permanecem configuráveis pelo próprio ambiente e não são impostos automaticamente.

## Código-fonte e algoritmos

Código:

```tex
\ufcsetup{codigo = listings}
```

ou:

```tex
\ufcsetup{codigo = minted}
```

Algoritmos:

```tex
\ufcsetup{algoritmos = algpseudocodex}
```

Os módulos são opcionais e só carregam suas dependências quando ativados.

## Glossário e índice

```tex
\ufcsetup{
  glossario = glossaries,
  indice = imakeidx
}
```

## Referências

```tex
\ufcbibliografia{backmatter/referencias.bib}
```

A bibliografia usa `biblatex-abnt` e `biber`. Ajustes específicos ao escopo atualmente testado da NBR 6023:2025 ficam isolados em `abntexto-ufc/compat-nbr6023-2025.def`.

## PDF/A

O documento de referência usa metadados PDF/A-2b. PDF/A-2b é uma política técnica verificável do projeto e não é apresentada como requisito geral da UFC para qualquer documento.

## Build e validação

Compilação padrão:

```bash
make compile
```

LuaLaTeX:

```bash
make compile ENGINE=lualatex
```

Preflight completo:

```bash
make preflight
```

Preflight de release:

```bash
make release-preflight
```

Geração dos bundles:

```bash
make package
```

Preflight de distribuição:

```bash
make distribution-preflight
```

O repositório mantém testes de geometria, tipografia, elementos pré/pós-textuais, objetos, referências, perfis, PDF/A, Overleaf e fontes literais no Windows.

## Verificação normativa v2.2.0

A v2.2.0 evolui de uma suíte de regressão para um sistema explícito de evidência normativa. O princípio é:

```text
regra existente
  !=
fonte rastreável
  !=
evidência classificada
  !=
propriedade medida no PDF final
  !=
regra comprovada
```

Documentação ativa da auditoria:

- `docs/HANDOFF-V2.2.0.md` — estado canônico, roadmap N0–N15 e próxima ação;
- `docs/NORMAS.md` — mapa normativo humano;
- `docs/VIGENCIA-NORMATIVA.md` — política de vigência e precedência.

O histórico detalhado de evidências permanece nos PRs, Actions, `normativa/` e `tests/`. Auditorias de releases encerradas ficam em `docs/history/`. Mudanças de distribuição CTAN são tratadas separadamente de mudanças de conformidade UFC/ABNT.

## Compatibilidade com a identidade anterior

`ufctex.cls` permanece temporariamente nos bundles do projeto como **shim de compatibilidade** para documentos existentes que ainda usam:

```tex
\documentclass{ufctex}
```

Novos documentos devem usar sempre:

```tex
\documentclass{abntexto-ufc}
```

O shim legado não é distribuído como identidade do pacote CTAN e não contém uma segunda implementação dos módulos.

A release histórica v2.1.0 foi publicada sob a identidade anterior; registros e artefatos dessa release não são reescritos.

## Distribuição

A identidade atual dos novos artefatos de classe/CTAN é `abntexto-ufc`.

O repositório também produz bundles completos do modelo para uso local e Overleaf. O bundle Overleaf coloca `main.tex` na raiz do projeto importado. A candidata CTAN é deliberadamente menor e contém apenas a superfície necessária para instalar, usar e documentar a classe.

A tag `v2.2.0` só será criada após o gate final de certificação da distribuição.

## Licença

O código e a documentação do projeto são distribuídos nos termos indicados em `LICENSE` (LPPL 1.3c ou posterior). Ativos de terceiros ou institucionais têm política de licenciamento/proveniência separada e não são automaticamente cobertos pela LPPL.

# Modelo LaTeX UFC

Template comunitário para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), com classe própria `ufctex` baseada em `abntexto`.

**Versão publicada atual: 2.0.0 — 19/08/2026.** A linha 1.x baseada em `abntex2` permanece preservada na branch `1.x` para documentos legados.

Este projeto não é um modelo oficial da UFC. Antes da entrega, confira também as orientações vigentes do Sistema de Bibliotecas, do curso, do programa e do edital aplicável.

## Arquitetura V2

```text
documento.tex
    |
    +-- ufctex.cls
          +-- core.def
          +-- fontes.def
          +-- layout.def
          +-- modulos.def
          +-- pretextuais.def
          +-- institucional.def
          +-- projetos.def
          +-- trabalhos.def
          +-- objetos.def
          +-- compat-abntexto.def
          +-- bibliografia.def
          +-- compat-nbr6023-2025.def
          +-- postextuais.def
          +-- compat-v1.def
```

`ufctex` requer `abntexto` 1.1 ou superior. Quando `tabelas=tabularray` é usado, a V2 exige `tabularray-abnt` 2025-08-08 ou superior. A política normativa detalhada está em `docs/NORMAS.md`.

## Uso rápido

O arquivo principal é `documento.tex`. Para PDFs destinados a depósito, preserve `\DocumentMetadata` antes de `\documentclass`:

```tex
\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}

\documentclass{ufctex}

\ufcsetup{
  tipo = tccgraduacao,
  impressao = anverso,
  fonte = times,
  fonte-estrita = nao,
  autor = {Nome Sobrenome},
  titulo = {Título do Trabalho},
  local = {Fortaleza},
  ano = {2026}
}
```

A UFC exige PDF/A nas modalidades de depósito institucional aplicáveis. O projeto escolhe PDF/A-2b como perfil técnico verificável; não declara o subtipo 2b como imposição específica da Universidade.

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

- `sim`: exige a família literal solicitada; a compilação falha se ela não estiver disponível;
- `nao`: permite fallback de compatibilidade para portabilidade e desenvolvimento.

Em modo não estrito, os fallbacks são explicitamente tratados como substitutos e **não** como Times New Roman/Arial:

- pdfLaTeX + `times`: NewTX;
- pdfLaTeX + `arial`: TeX Gyre Heros;
- LuaLaTeX + `times`: TeX Gyre Termes;
- LuaLaTeX + `arial`: TeX Gyre Heros.

Para declarar conformidade tipográfica final com o requisito UFC, use a família literal e verifique o PDF produzido. O modo estrito existe para essa certificação.

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
- seções textuais primárias e pós-textuais controlados pela V2 iniciam em anverso.

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
  remark{Fonte}={Elaboração própria.}
]
{
  colspec={X[r] X[r]}
}
\toprule
Ano & Valor \\
\midrule
2025 & 10 \\
2026 & 12 \\
\bottomrule
\end{tallabnttblr}
```

O corpo permanece em tamanho 12; legenda, Fonte e Nota usam tamanho reduzido. Linhas alternadas por cor são opcionais e não são aplicadas por padrão:

```tex
row{even}={bg=black!5}
```

Quadros textuais continuam usando o tema `quadro` do `tabularray-abnt`.

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

`minted` exige suporte externo no ambiente de compilação. Código e algoritmos usam a família textual institucional e tamanho 12 por padrão.

## Citações e referências

A V2 usa `biblatex` + Biber com estilo ABNT:

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

A camada `compat-nbr6023-2025.def` concentra ajustes transitórios da NBR 6023:2025 enquanto o suporte equivalente não estiver disponível no upstream.

Referências próprias de um anexo devem permanecer no próprio anexo, em nota ou lista específica.

## Pós-textuais

```tex
\imprimirreferencias
\imprimirglossario

\appendix{Título do apêndice}
\input{3-pos-textuais/apendices/apendice-a}

\annex{Título do anexo}
\input{3-pos-textuais/anexos/anexo-a}

\imprimirindice
```

Os arquivos distribuídos de apêndices e anexos contêm somente o conteúdo; a abertura é feita por `\appendix` e `\annex` no documento principal.

## Compilação

Fluxo padrão:

```bash
make
```

O `Makefile` usa pdfLaTeX por padrão. Após a primeira passagem, executa apenas os processadores necessários pelos artefatos efetivamente gerados:

- `.bcf` com uma `datasource` bibliográfica → Biber;
- `.glo` não vazio → `makeglossaries`;
- `.idx` não vazio → `makeindex`.

LuaLaTeX:

```bash
make lua
```

## Validação

Gate completo de desenvolvimento:

```bash
make preflight
```

Gate de release, incluindo veraPDF:

```bash
make release-preflight
```

A suíte cobre:

- consistência dos arquivos distribuídos e ausência de fontes Microsoft versionadas;
- documento completo de referência;
- A4, margens, paginação e duplex medidos no PDF;
- política de fonte e embedding;
- pré e pós-textuais;
- orientação CAPES condicional;
- ficha catalográfica em `anverso` e `frente-verso`;
- trabalhos multivolume e continuidade de paginação;
- objetos e sua geometria;
- tabelas e subconjunto IBGE;
- código, `minted` e algoritmos;
- matemática e alinhamento de equações;
- citações, referências, fonte externa e referência própria de anexo;
- projetos;
- fluxo modular do `Makefile`;
- seis perfis completos em pdfLaTeX e LuaLaTeX.

A matriz final gera **12 PDFs** — seis perfis × dois motores — e verifica conteúdo específico, Sumário, A4, fontes incorporadas, ausência de `chapter`, warnings/overflow não reconhecidos e metadados PDF/A-2b. O gate de release passa os 12 PDFs e o documento de referência pelo veraPDF.

O CI usa TeX Live 2026. A branch de evolução contém ainda uma POC Windows separada para provar Times New Roman e Arial literais, incluindo as quatro variantes, nos dois motores e pela própria classe em modo estrito. Esse job só deve virar gate obrigatório depois de demonstrar execução reprodutível.

## Overleaf

Importe o projeto completo e mantenha `documento.tex` como arquivo principal. Use uma versão recente do TeX Live com `abntexto` 1.1 ou superior.

pdfLaTeX é o caminho padrão; LuaLaTeX também é suportado. Preserve `\DocumentMetadata` antes de `\documentclass` quando precisar de PDF/A e valide o PDF baixado com veraPDF antes do depósito.

Se Times New Roman/Arial literais não estiverem disponíveis no ambiente Overleaf, `fonte-estrita=nao` permite compilação de desenvolvimento com fallback. Isso não deve ser confundido com certificação tipográfica final da família literal.

## Migração da V1

A V2 é uma mudança de plataforma. A implementação histórica permanece na branch `1.x`; os arquivos LaTeX V1 não são distribuídos na árvore V2.

| V1 | V2 |
|---|---|
| `\documentclass{abntex2}` | `\documentclass{ufctex}` |
| `\input{lib/preambulo}` | removido |
| configuração histórica | `\ufcsetup{...}` |
| `\chapter` como nível principal | `\section` |
| `\UFCfig`, `\UFCtab`, `\UFCqua` | `\legend` + `\ufcfonte` + `ufcobjeto` |
| configuração bibliográfica histórica | `\ufcbibliografia{arquivo.bib}` |

`compat-v1.def` existe apenas como camada de transição e regressão; não define o estilo recomendado para documentos novos.

## Normas

Consulte `docs/NORMAS.md` para a matriz norma → implementação, política de precedência e gates de validação.

Não declare conformidade apenas porque o documento compilou ou porque contém metadados PDF/A. A revisão final deve considerar as exigências específicas aplicáveis e, para depósito, a validação independente do arquivo final.

## Licença

Consulte `LICENSE`.

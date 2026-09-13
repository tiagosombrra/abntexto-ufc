# Referência de comandos do abntexto-ufc

Esta é a referência de consulta da API pública da série 3. Para aprender pelo fluxo de um TCC completo, comece por `template/main.tex` e pelo [USER-GUIDE.md](USER-GUIDE.md).

A API própria do projeto usa identificadores em inglês. Comandos históricos em português da série 2 não são aliases de runtime; consulte [MIGRATING-TO-V3.md](MIGRATING-TO-V3.md) ao migrar documentos antigos.

## Configuração: \ufcsetup

Forma geral:

```tex
\ufcsetup{
  chave = valor,
  outra-chave = {texto}
}
```

### Perfil e impressão

| Chave | Valores / uso |
| --- | --- |
| `type` | `undergraduate-capstone`, `specialization-capstone`, `masters-thesis`, `doctoral-thesis`, `research-project`, `anonymized-research-project`, `scientific-article` |
| `print-mode` | `single-sided` ou `double-sided` |
| `cover` | `auto`, `true` ou `false` |
| `catalog-card` | `true` ou `false` |
| `coat-of-arms` | `true` ou `false` |
| `initial-page` | política de página inicial dos trabalhos acadêmicos quando aplicável |

### Instituição e unidade acadêmica

| Chave | Uso |
| --- | --- |
| `institution` | nome da instituição |
| `institution-acronym` | sigla institucional |
| `center` | centro, faculdade, instituto ou campus |
| `department` | departamento/unidade; pode ficar vazio |
| `coat-of-arms-file` | caminho local para o ativo institucional autorizado |

### Graduação e especialização

| Chave | Uso |
| --- | --- |
| `undergraduate-program` | curso de graduação |
| `undergraduate-degree` | grau/habilitação usada na natureza do trabalho |
| `specialization-program` | curso de especialização |

### Mestrado e doutorado

| Chave | Uso |
| --- | --- |
| `masters-graduate-program` | programa de pós-graduação |
| `masters-program` | nome complementar do mestrado quando necessário |
| `masters-degree-field` | área/título do grau de mestre |
| `masters-concentration` | área de concentração |
| `doctoral-graduate-program` | programa de pós-graduação |
| `doctoral-program` | nome complementar do doutorado quando necessário |
| `doctoral-degree-field` | área/título do grau de doutor |
| `doctoral-concentration` | área de concentração |

### Projeto de pesquisa

| Chave | Uso |
| --- | --- |
| `project-program` | programa/processo ao qual o projeto se vincula |
| `project-type` | denominação do projeto |
| `submission-entity` | entidade à qual o projeto é apresentado |
| `project-nature-statement` | substitui o texto automático da natureza |
| `project-identifier` | identificador público do perfil anonimizado |

### Autor, título e datas

| Chave | Uso |
| --- | --- |
| `author` | nome completo do autor |
| `title` | título |
| `subtitle` | subtítulo; deixe vazio quando inexistente |
| `title-variant` | variante de título usada por perfis que a suportam |
| `volume` | número/identificação de volume |
| `location` | cidade |
| `year` | ano |
| `submission-date` | data de submissão quando o perfil a utilizar |
| `approval-date` | data de aprovação |
| `article-author-note` | nota de autoria do perfil de artigo |

### Orientação e banca

| Chave | Uso |
| --- | --- |
| `advisor` | orientador |
| `advisor-institution` | instituição do orientador |
| `advisor-unit` | unidade do orientador |
| `advisor-feminine-label` | `true` ou `false` |
| `coadvisor` | coorientador |
| `coadvisor-institution` | instituição do coorientador |
| `coadvisor-unit` | unidade do coorientador |
| `coadvisor-feminine-label` | `true` ou `false` |
| `examiner-2` ... `examiner-6` | membros adicionais da banca |
| `examiner-2-institution` ... `examiner-6-institution` | instituições |
| `examiner-2-unit` ... `examiner-6-unit` | unidades acadêmicas |
| `epigraph-author` | autoria exibida na epígrafe |

### Fonte e módulos opcionais

| Chave | Valores |
| --- | --- |
| `font` | `times` ou `arial` |
| `strict-font` | `true` ou `false` |
| `tables` | `native` ou `tabularray` |
| `code` | `none`, `listings` ou `minted` |
| `algorithms` | `none` ou `algpseudocodex` |
| `glossary` | `none` ou `glossaries` |
| `index` | `none` ou `imakeidx` |

## Consultas de estado

### \ufcDocumentType

Expande para o valor atual de `type`.

### \ufcPrintMode

Expande para o modo de impressão atual.

### \ufcMeta{chave}

Retorna o metadado armazenado para a chave informada.

### \ufcIfProjectTF{verdadeiro}{falso}

Executa o primeiro argumento para `research-project` e `anonymized-research-project`; caso contrário executa o segundo.

### \ufcIfAnonymizedProjectTF{verdadeiro}{falso}

Testa especificamente `anonymized-research-project`.

### \ufcMathFontPolicy

Expõe a política matemática selecionada pelo módulo de fontes.

## Elementos pré-textuais

### \ufcPrintCover

Gera a capa quando `cover` não estiver desabilitado.

### \ufcPrintTitlePage

Gera a folha de rosto. O perfil de projeto possui composição própria.

### \ufcPrintApprovalPage

Gera a folha de aprovação dos trabalhos acadêmicos aplicáveis.

### \ufcPrintCatalogCard{arquivo}

Inclui a ficha catalográfica a partir do arquivo indicado.

### \ufcPrintErrata{arquivo}

Gera a errata.

### \ufcPrintDedication{arquivo}

Gera a dedicatória.

### \ufcPrintAcknowledgments{arquivo}

Gera os agradecimentos.

### \ufcPrintEpigraph[short|long]{arquivo}

Gera a epígrafe. O argumento opcional seleciona a composição curta ou longa.

### \ufcPrintSummary{arquivo}

Gera o resumo em português.

### \ufcSummaryKeywords{texto}

Usado dentro do arquivo de resumo para as palavras-chave.

### \ufcPrintAbstract{arquivo}

Gera o abstract em inglês.

### \keywords{texto}

Comando fornecido pela infraestrutura usada pelo projeto para as keywords do abstract.

## Listas e sumário

### \ufcPrintListOfIllustrations

Lista unificada das ilustrações suportadas pelo modelo.

### \ufcPrintListOfFigures

Lista apenas figuras.

### \ufcPrintListOfCharts

Lista gráficos.

### \ufcPrintListOfTextTables

Lista quadros.

### \ufcPrintListOfTables

Lista tabelas numéricas.

### \ufcPrintListOfCodeListings

Lista códigos-fonte identificados.

### \ufcPrintListOfAlgorithms

Lista algoritmos identificados.

### \ufcPrintListOfAbbreviationsAndAcronyms{arquivo}

Imprime a lista declarada pelo usuário.

### \ufcPrintListOfSymbols{arquivo}

Imprime a lista de símbolos.

### \ufcListEntry{rótulo}{descrição}

Entrada para listas de definição usadas nos arquivos auxiliares.

### \ufcPrintTableOfContents

Gera o sumário.

## Objetos acadêmicos

A identificação dos objetos usa `\legend`, fornecido pela infraestrutura `abntexto`, junto dos comandos próprios abaixo.

### \ufcSource{texto}

Define a fonte do objeto.

### \ufcNote{texto}

Adiciona uma nota abaixo do objeto quando necessária.

### ambiente ufcobject

```tex
\begin{ufcobject}[here]
  ...
\end{ufcobject}
```

Contêiner geral para figuras, gráficos, quadros e outros objetos compatíveis.

### ambiente ufclisting

Disponível quando `code=listings`:

```tex
\begin{ufclisting}[here]
...
\end{ufclisting}
```

### \ufcInputListing[opções]{arquivo}

Inclui um arquivo externo com `listings`.

### \ufcInputMinted[posição][opções]{linguagem}{arquivo}

Inclui um arquivo externo quando `code=minted`.

### ambiente ufcalgorithm

Disponível com `algorithms=algpseudocodex`:

```tex
\begin{ufcalgorithm}[here][1]
  ...
\end{ufcalgorithm}
```

O segundo argumento controla a política de numeração de linhas do exemplo.

## Listas textuais

### ambiente ufclettereditems

Lista de alíneas.

### ambiente ufcdashedsubitems

Subalíneas com marcador próprio, normalmente aninhadas em `ufclettereditems`.

### ambiente ufcdefinitionlist

Lista de definições. Aceita largura opcional do rótulo:

```tex
\begin{ufcdefinitionlist}[3cm]
  \ufcListEntry{API}{Interface pública da classe.}
\end{ufcdefinitionlist}
```

## Bibliografia

### \ufcAddBibliographyResource{arquivo.bib}

Registra um banco bibliográfico.

### \ufcPrintReferences

Imprime a seção de referências.

A camada de citações usa `biblatex-abnt`. Comandos como `\textcite`, `\parencite`, `\apud` e `\textapud` pertencem à infraestrutura bibliográfica integrada e devem receber chaves existentes no banco.

## Elementos pós-textuais

### \ufcPrintGlossary

Imprime o glossário quando `glossary=glossaries`.

### \ufcPrintIndex

Imprime o índice quando `index=imakeidx`.

Para apêndices e anexos, a classe preserva os comandos da infraestrutura `abntexto`:

```tex
\appendix{Título do apêndice}
\annex{Título do anexo}
```

## Comandos estruturais preservados da infraestrutura

O projeto não renomeia comandos que pertencem legitimamente às dependências. Entre os usados pelo tutorial estão:

- `\pretextual`;
- `\textual`;
- `\legend`;
- `\keywords`;
- `\appendix`;
- `\annex`.

## Exemplo mínimo completo

```tex
\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}

\documentclass{abntexto-ufc}

\ufcsetup{
  type = undergraduate-capstone,
  author = {Nome Completo do Autor},
  title = {Título do trabalho},
  location = {Fortaleza},
  year = {2026},
  advisor = {Prof. Dr. Nome do Orientador}
}

\ufcAddBibliographyResource{backmatter/references.bib}

\begin{document}

\pretextual
\ufcPrintCover
\ufcPrintTitlePage
\ufcPrintSummary{frontmatter/summary}
\ufcPrintAbstract{frontmatter/abstract}
\ufcPrintTableOfContents

\textual
\input{chapters/1-introduction}

\ufcPrintReferences

\end{document}
```

## O que esta referência não faz

Esta página descreve a API pública; ela não substitui:

- as regras acadêmicas do curso ou programa;
- a base normativa auditada do repositório;
- a documentação das dependências LaTeX;
- a revisão visual do PDF final;
- os procedimentos institucionais de depósito.

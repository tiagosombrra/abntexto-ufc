# Referência de comandos do abntexto-ufc

Esta é a referência de consulta da API pública atual. Para aprender pelo fluxo de um TCC completo, comece por `template/main.tex` e pelo [USER-GUIDE.md](USER-GUIDE.md).

A API pública própria do projeto usa os identificadores canônicos documentados nesta referência. O contrato correspondente, legível por máquina, é `standards/api/public-api.json`. O runtime não mantém aliases paralelos para APIs retiradas; esta referência descreve apenas a superfície atualmente suportada.

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
| `labels-language` | `pt` (padrão), `en`, `es`, `fr`; títulos pré-textuais, não idioma completo do manuscrito |
| `document-language` | `pt`, `en`, `es`, `fr`; quando explícita seleciona idioma Babel, resumos e **37 textos catalogados pela classe**; ausente preserva padrão PT; metadados PDF independentes |
| `print-mode` | `single-sided` ou `double-sided` |
| `cover` | `auto`, `true` ou `false` |
| `catalog-card` | `true` ou `false` |
| `coat-of-arms` | `true` ou `false` |
| `initial-page` | política de página inicial dos trabalhos acadêmicos quando aplicável |

`--page-accounting` é uma **opção do validador CLI/Deep**, não uma chave de `\ufcsetup`. O valor `pdf-first-page` (padrão) trata a página física 1 do PDF como primeiro anverso interno. Para arquivos que incluem uma **capa externa não contada**, use `--print-mode double-sided --page-accounting external-cover-first`; no Web/Lite, escolha a opção equivalente em **“Início da contagem no PDF duplex”**. Esse modo deixa a capa externa fora do teste de margens do miolo, mas mantém o teste A4, e faz a página PDF 2 corresponder ao anverso interno 1. Não desconte uma segunda página para ficha catalográfica: ela ocupa fisicamente o verso no miolo, mesmo quando não numerada. O modo com capa exige PDF com pelo menos duas páginas e impressão dupla; modelos inconsistentes são rejeitados.

### Idioma principal e versões do resumo (opt-in, v3.1.0)

A chave **document-language = pt|en|es|fr** define o idioma dos novos comandos de resumo **e das 37 chaves de textos/legendas catalogados pela classe**, de forma independente de **labels-language**. O idioma padrão para a política de resumos é PT. Quando `document-language` é informado explicitamente, os títulos gerais seguem esse idioma automaticamente, salvo configuração explícita e independente de `labels-language`. A seleção de idioma do Babel ao iniciar o documento ocorre **somente se esta chave for informada explicitamente**; na ausência da chave, a classe não sobrescreve o idioma selecionado pelo Babel, mas a inicialização das dependências pode redefinir uma seleção `\selectlanguage{english}` feita diretamente no preâmbulo para português brasileiro. Para garantir inglês, configure `document-language=en`. O autor deve configurar também o idioma do PDF em **\DocumentMetadata** antes de **\documentclass**; a classe não modifica automaticamente os metadados.

| Idioma principal | Par gerado pelo comando novo | Versão inglesa adicional |
| --- | --- | --- |
| pt | RESUMO → ABSTRACT | não se aplica |
| en | ABSTRACT → RESUMO | não se aplica |
| es | RESUMEN → RESUMO | opcional |
| fr | RÉSUMÉ → RESUMO | opcional |

A ordem é a política adotada para o projeto e exige confirmação específica do programa ou instituição no caso de uma submissão em língua estrangeira. Espanhol/francês dependem dos recursos Babel correspondentes no ambiente LaTeX; o idioma padrão não passa a depender desses pacotes. Veja [Política de idiomas dos resumos](SUMMARY-LANGUAGE-POLICY.md).

### `labels-language = pt|en|es|fr` (v3.1.0 experimental)

Seleciona exclusivamente a tradução dos títulos gerados por `\ufcPrintAcknowledgments`, `\ufcPrintErrata`, `\ufcPrintListOfIllustrations`, `\ufcPrintListOfFigures`, `\ufcPrintListOfTables`, `\ufcPrintListOfTextTables`, `\ufcPrintListOfAbbreviationsAndAcronyms`, `\ufcPrintListOfSymbols` e `\ufcPrintTableOfContents`.

**Padrão: `pt`**, preservando a saída existente; `en`, `es` e `fr` são opt-in. Idiomas inválidos causam erro de configuração. `\ufcPrintSummary` preserva o rótulo Resumo e `\ufcPrintAbstract` preserva Abstract; a seleção isolada de `labels-language` não modifica Babel, idioma do documento, títulos/cargos institucionais, PDF/A, referências nem conformidade ABNT/UFC; `document-language` explícito também traduz as expressões institucionais e cargos suportados, exceto nomes oficiais. A tradução de nomes próprios (instituição, programa) exige informação explícita nos metadados e revisão institucional.

### Tradução das frases automáticas (v3.1.0)

Ao configurar `document-language` explicitamente, a classe traduz as naturezas aplicáveis aos cinco perfis, banca, cargos de orientação, datas, legendas de objetos, referências, glossário, apêndices, anexos e Fonte/Nota. No abntexto herdado os títulos de apêndices/anexos e notas de objeto passam por `\appendixlabel`, `\annexlabel` e `\abntextonotelabel`, corrigidos no ramo de desenvolvimento. `labels-language` sozinho continua limitado aos nove títulos pré-textuais. Nomes oficiais, bibliografia gerada por dependências, conteúdo autoral e PDF `/Lang` são assuntos distintos, não traduzidos automaticamente. As traduções institucionais descritivas não constituem homologação da UFC. Consulte [a auditoria](I18N-AUDIT-2026-10-23.md).

### Instituição e unidade acadêmica

| Chave | Uso |
| --- | --- |
| `institution` | denominação jurídica da instituição; permanece inalterada em `\ufcMeta{institution}` |
| `institution-display` | nome exibido em capa e natureza acadêmica; por padrão acompanha `document-language` somente para a instituição padrão UFC; se informado, sobrepõe o nome exibido sem modificar a denominação jurídica |
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
| `submission-entity` | denominação jurídica da entidade à qual o projeto é apresentado |
| `submission-entity-display` | nome da entidade exibido no projeto; por padrão acompanha o nome exibido da UFC quando não há entidade explícita; respeita dados autorais explícitos |
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
| `examiner-2` | segundo membro da banca |
| `examiner-2-institution` | instituição do segundo membro |
| `examiner-2-unit` | unidade do segundo membro |
| `examiner-3` | terceiro membro da banca |
| `examiner-3-institution` | instituição do terceiro membro |
| `examiner-3-unit` | unidade do terceiro membro |
| `examiner-4` | quarto membro da banca |
| `examiner-4-institution` | instituição do quarto membro |
| `examiner-4-unit` | unidade do quarto membro |
| `examiner-5` | quinto membro da banca |
| `examiner-5-institution` | instituição do quinto membro |
| `examiner-5-unit` | unidade do quinto membro |
| `examiner-6` | sexto membro da banca |
| `examiner-6-institution` | instituição do sexto membro |
| `examiner-6-unit` | unidade do sexto membro |
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

`strict-font=true` exige a **família literal de texto** escolhida por `font`, e interrompe a compilação se essa família não estiver disponível ou preparada. Com `strict-font=false`, a classe permite fallbacks explícitos para compilar em ambientes portáveis; isso **não equivale à certificação tipográfica institucional**. A política da fonte matemática é independente da família de texto: consulte `\ufcMathFontPolicy`. Para instruções de fontes Microsoft em Windows, veja [WINDOWS-FONT-SUPPORT.md](WINDOWS-FONT-SUPPORT.md).

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

Expõe o identificador da política matemática selecionada pelo mecanismo TeX. Em `pdfLaTeX`, o contrato atual retorna `NEW-TX-MATH`; em `LuaLaTeX`, a política depende da disponibilidade das fontes matemáticas OpenType, não apenas do valor de `font`.

Exemplo para inspeção do log do próprio documento:

```tex
\typeout{MATH-POLICY=\ufcMathFontPolicy}
```

Isso permite auditar qual política a classe selecionou; **não comprova, sozinho, incorporação de fonte, qualidade de símbolos, PDF/A ou conformidade institucional**. A etapa P0.8D-7 verifica o identificador em quatro PDFs reais `pdfLaTeX` no cenário delimitado descrito em [I18N-COMPLETION-MATRIX.md](I18N-COMPLETION-MATRIX.md).

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

### \ufcDocumentLanguage

Consulta o idioma principal configurado em document-language.

### \ufcPrintRequiredSummaries{arquivo-principal}{arquivo-complementar}

Gera duas páginas com idiomas e títulos determinados pelo idioma principal: PT→PT+EN; EN→EN+PT; ES→ES+PT; FR→FR+PT.

### \ufcPrintSummaryInLanguage{idioma}{arquivo}

Gera uma página em pt, en, es ou fr. Durante **esta página**, os auxiliares históricos `\ufcSummaryKeywords{...}` e `\keywords{...}` recebem automaticamente o rótulo do idioma da página; fora dessa página, preservam a semântica legada PT/EN. O comando explícito `\ufcSummaryKeywordsInLanguage{idioma}{...}` continua disponível. Idiomas duplicados usando a nova API provocam erro; não combine versões duplicadas com comandos antigos.

### \ufcSummaryKeywordsInLanguage{idioma}{termos}

Imprime Palavras-chave / Keywords / Palabras clave / Mots-clés de acordo com o idioma do texto de resumo.

### \ufcPrintOptionalEnglishSummary{arquivo}

Somente para documento principal em espanhol ou francês. Complementa o par com um ABSTRACT em inglês; pt/en são rejeitados para evitar duplicação.

### \ufcPrintArticleTranslatedSummary{idioma}{texto}

No perfil scientific-article, insere uma versão traduzida identificada e rejeita o mesmo idioma do resumo principal. \ufcPrintArticleFrontMatter usa o rótulo principal escolhido por document-language; a API legada de elementos estrangeiros permanece.

### \ufcPrintSummary{arquivo}

Gera o resumo em português.

### \ufcSummaryKeywords{texto}

Historicamente gera **Palavras-chave** no `\ufcPrintSummary` português. Dentro de `\ufcPrintSummaryInLanguage{idioma}{arquivo}`, o mesmo comando agora acompanha o idioma do resumo (PT/EN/ES/FR) sem alterar o comando legado fora desse contexto.

### \ufcPrintAbstract{arquivo}

Gera o abstract em inglês.

### \keywords{texto}

Historicamente usa **Keywords** no `\ufcPrintAbstract`. Dentro de `\ufcPrintSummaryInLanguage{idioma}{arquivo}`, acompanha o idioma desse resumo (PT/EN/ES/FR), inclusive para resumos complementares. A escrita dos termos continua responsabilidade do autor; fora do resumo opt-in, este comando é fornecido pela infraestrutura histórica de ABSTRACT.

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

Inclui o conteúdo **real de um arquivo externo** pelo módulo `listings`, que deve estar habilitado em `\ufcsetup`:

```tex
\ufcsetup{code=listings}
\ufcInputListing[language=C++]{code/example.cpp}
```

**Compatibilidade de posicionamento (prévia v3.1.0, issue [#590](https://github.com/tiagosombrra/abntexto-ufc/issues/590)):** a correção em desenvolvimento permite utilizar a API pública \`\ufcInputListing\` diretamente no texto ou dentro de \`place\`, \`ufcobject\` e \`minipage\`. Quando a listagem é executada em modo horizontal interno, a classe aplica um encapsulamento vertical; na chamada direta, preserva o comportamento original de paginação. A matriz de validação compilou **64 PDFs reais** no TeX Live 2026, considerando quatro idiomas, dois perfis, quatro contextos e duas variações de legenda/fonte. Os testes verificaram integridade estrutural do PDF, código C++ visível e marcadores de legenda/fonte nos casos aplicáveis.

Para utilizar o ambiente \`ufcobject\` com o importador público:

\`\`\`tex
\legend{code}{Arquivo C++ externo}
\ufcSource{Elaboração própria.}
\label{cod:arquivo-externo}
\begin{ufcobject}[here]
  \ufcInputListing[language=C++]{code/example.cpp}
\end{ufcobject}
\`\`\`

Essa correção **não se aplica automaticamente** ao comando nativo \`\lstinputlisting\` invocado diretamente dentro do \`place\` herdado. Listagens extensas que precisam quebrar entre páginas devem permanecer fora de \`place\`/\`ufcobject\`, porque esses ambientes utilizam caixas não divisíveis. A matriz de 64 casos é uma prova funcional delimitada: não substitui a revisão de posicionamento, paginação longa, referências cruzadas, conformidade UFC/ABNT ou aceite visual e linguístico. **A correção ainda pertence à PR [#592](https://github.com/tiagosombrra/abntexto-ufc/pull/592); a v3.1.0 não foi publicada.**

O arquivo `code/example.cpp` deve existir no projeto de compilação. Traduções de títulos e legendas não alteram automaticamente a linguagem de programação nem o conteúdo do arquivo; configure suas opções de `listings` explicitamente.

Na etapa P0.8D-7, a auditoria verifica no **PDF efetivo**, e não apenas no arquivo-fonte, um identificador C++ e a expressão `return 173;`, em quatro idiomas, no perfil `undergraduate-capstone` sob `pdfLaTeX`. Essa evidência **não comprova** todos os estilos de listagem, perfis, linguagens de programação ou mecanismos TeX. Consulte [a matriz de evidências](I18N-COMPLETION-MATRIX.md).

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

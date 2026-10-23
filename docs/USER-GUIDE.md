# Guia de uso do abntexto-ufc

Este guia explica o fluxo normal de produção de um trabalho com a classe `abntexto-ufc`. O arquivo `template/main.tex` é o tutorial executável: ele mostra um TCC curto e realista. Para consulta exaustiva de chaves, comandos e ambientes, use [COMMAND-REFERENCE.md](COMMAND-REFERENCE.md).

A classe concentra decisões de apresentação, mas o autor continua responsável pelo conteúdo acadêmico, pelas fontes citadas e pelas regras específicas do curso, programa, edital ou procedimento de depósito.

## Fluxo recomendado

1. copie o Template ou importe o ZIP Overleaf da Release;
2. edite os metadados em `\ufcsetup{...}`;
3. substitua os arquivos de `frontmatter/`;
4. escreva o texto em `chapters/`;
5. mantenha as referências em `backmatter/references.bib`;
6. compile pelo fluxo completo;
7. revise o PDF e execute os validadores disponíveis;
8. antes da entrega, confira as orientações atuais da UFC e do seu curso/programa.

## Configuração principal

Toda configuração pública da classe parte de:

```tex
\ufcsetup{
  type = undergraduate-capstone,
  author = {Nome Completo do Autor},
  title = {Título do trabalho},
  location = {Fortaleza},
  year = {2026}
}
```

O tutorial mantém apenas os campos mais comuns visíveis no `main.tex`. Chaves especializadas continuam documentadas na referência de comandos.

### Idiomas e textos gerados pela classe (v3.1.0 em desenvolvimento)

Existem duas opções independentes: `labels-language=pt|en|es|fr` traduz somente os **nove títulos pré-textuais**; `document-language=pt|en|es|fr`, quando explicitamente configurada, seleciona o idioma principal Babel, as versões de resumo e **33 chaves de texto institucional/legendas geradas pela classe** (natureza, banca, orientador, datas, fontes/notas, referências, glossário, apêndices e anexos). Sem escolha explícita de `labels-language`, os nove títulos acompanham `document-language`. Sem `document-language`, o legado continua em português.

Exemplo de configuração:

```tex
\DocumentMetadata{lang=en-US,pdfstandard=A-2b,pdfversion=1.7}
\documentclass{abntexto-ufc}
\ufcsetup{
  type=doctoral-thesis,
  document-language=en,
  labels-language=en,
  institution={Universidade Federal do Ceará}
}
```

Os comandos legados `\ufcPrintSummary` e `\ufcPrintAbstract` continuam produzindo títulos fixos em português e inglês; os novos comandos multilíngues devem ser usados para outros idiomas. A tradução das frases **automáticas** não traduz os nomes oficiais de instituições, programas ou titulações, nem conteúdo do autor, referências de dependências ou metadados PDF. Os textos institucionais estrangeiros são descritivos e exigem revisão pela autoridade competente. Veja [a cobertura](INTERNATIONALIZATION-COVERAGE.md) e [a auditoria](I18N-AUDIT-2026-10-23.md).

### Política opcional de RESUMO, ABSTRACT, RESUMEN e RÉSUMÉ (v3.1.0)

A configuração **document-language=pt|en|es|fr** é independente de **labels-language**. Quando informada explicitamente, a primeira seleciona o idioma principal do texto no Babel e a política de resumos; sem essa opção, a classe não adiciona uma substituição de idioma, mas o próprio Babel pode redefinir uma seleção `\selectlanguage{english}` feita diretamente no preâmbulo para português brasileiro. Para obter inglês de forma explícita e verificável, use `document-language=en`. PT continua sendo o padrão dos novos comandos de resumo. A segunda seleciona somente os nove títulos gerais pré-textuais. Se `document-language` for explícito e `labels-language` não, os nove títulos passam automaticamente para o idioma do documento; uma escolha explícita de `labels-language` tem precedência. O par de resumos é explicitamente gerado com **\ufcPrintRequiredSummaries{arquivo-principal}{arquivo-complementar}**:

- Português: RESUMO seguido de ABSTRACT em inglês.
- Inglês: ABSTRACT seguido de RESUMO em português.
- Espanhol: RESUMEN seguido de RESUMO em português; ABSTRACT adicional é opcional.
- Francês: RÉSUMÉ seguido de RESUMO em português; ABSTRACT adicional é opcional.

Em espanhol ou francês, use **\ufcPrintOptionalEnglishSummary{arquivo-ingles}** apenas quando a versão inglesa complementar for necessária. Cada arquivo deve ter o conteúdo realmente traduzido e as palavras-chave no respectivo idioma, por meio de **\ufcSummaryKeywordsInLanguage{idioma}{termos}**. O documento deve declarar o idioma apropriado em **\DocumentMetadata** separadamente. A ordem é a política opt-in deste projeto, não uma declaração de que a ABNT estabelece automaticamente essa sequência para qualquer instituição.

Para artigos científicos, o título do resumo principal acompanha o idioma escolhido por **document-language** e uma tradução identificada pode ser acrescentada por **\ufcPrintArticleTranslatedSummary{idioma}{texto}**, sujeita às condições da revista. Os comandos antigos permanecem válidos e não mudam seus nomes ou semântica.

Consulte [Política de idiomas dos resumos](SUMMARY-LANGUAGE-POLICY.md) para exemplos completos, ressalvas quanto à UFC, limitações de conformidade e testes em PDFs reais. Nenhuma tradução automática do conteúdo ou dos dados institucionais é realizada.

### Perfis de documento

A chave `type` seleciona o perfil:

- `undergraduate-capstone`: TCC de graduação;
- `specialization-capstone`: trabalho de especialização;
- `masters-thesis`: dissertação;
- `doctoral-thesis`: tese;
- `research-project`: projeto de pesquisa;
- `anonymized-research-project`: projeto com anonimização pessoal;
- `scientific-article`: artigo científico.

Perfis controlam metadados, natureza do trabalho e elementos aplicáveis. Não adapte um perfil removendo manualmente partes internas da classe.

Nos perfis de projeto de pesquisa, a capa é opcional no contrato da NBR 15287:2025 adotado pelo projeto e a folha de rosto é obrigatória. Quando uma capa institucional UFC é produzida, o projeto usa o brasão por padrão como política de apresentação institucional. `coat-of-arms=false` permanece disponível para submissões sem marca ou processos cegos.

### Validação por tipo de documento (v3.1.0 em desenvolvimento)

Os validadores agora distinguem o **tipo de documento** (os sete valores da chave `type`) do **modo de validação** (`strict`, `portable` ou `accessibility`). Selecione sempre o tipo correspondente ao PDF; não confunda `--profile` (rigor/capacidade do validador) com `--document-type` (contrato de estrutura). Por compatibilidade, a seleção inicial é `undergraduate-capstone`.

Exemplo de validação CLI/Deep para artigo:

```bash
python3 tools/validate-ufc-pdf.py artigo.pdf --profile strict --document-type scientific-article --format json
```

A matriz única de aplicabilidade está em `validator/document-applicability.json`, com representação estática correspondente no Web/Lite. Ela distingue elementos **obrigatórios** (ausência do marcador textual resulta em `FAIL`), **opcionais** (ausência resulta em `NOT APPLICABLE`, presença requer revisão) e **não exigíveis naquele perfil** (não geram falha mesmo ausentes). Projetos de pesquisa não exigem a estrutura pré-textual de um trabalho concluído; artigos não exigem capa, folha de aprovação ou sumário do TCC.

Os testes da v3.1.0 também exercitam PDFs realmente compilados de artigo, projetos de pesquisa e um projeto anonimizado, incluindo documentos de controle deliberadamente incompletos. Eles comparam os resultados Web/Lite e CLI/Deep para os marcadores cobertos sem declarar equivalência completa entre os motores de leitura de PDF.

A verificação textual é **parcial**: encontrar uma palavra no PDF não prova que o elemento está corretamente localizado, completo ou semanticamente válido. Requisitos do periódico, condições institucionais, anonimização e elementos não cobertos pela matriz continuam sujeitos a avaliação própria. Esse mecanismo não certifica conformidade ABNT/UFC integral.

### Papel, margens e paginação

O projeto trabalha em papel A4 e aplica automaticamente as margens do perfil acadêmico. Em impressão simples, o anverso usa margens esquerda/superior de 3 cm e direita/inferior de 2 cm. Em frente e verso, a geometria é espelhada quando aplicável.

Use:

```tex
print-mode = single-sided
```

ou:

```tex
print-mode = double-sided
```

Os validadores distinguem agora o modo de impressão de seu rigor e do tipo documental. No Web/Lite, selecione **Single-sided** ou **Double-sided**; no CLI/Deep, use `--print-mode single-sided` (padrão de compatibilidade) ou `--print-mode double-sided`. Esta escolha precisa refletir o modo efetivamente utilizado na compilação e **não é inferida automaticamente do PDF**. Em `double-sided`, páginas ímpares usam `margin.recto` (esquerda 3 cm, direita 2 cm) e páginas pares usam `margin.verso` (esquerda 2 cm, direita 3 cm). Exemplo:

```bash
python3 tools/validate-ufc-pdf.py tese.pdf --profile portable --document-type doctoral-thesis --print-mode double-sided --format json
```

A verificação automática aqui mede somente limites **horizontais** do texto extraído. Não prova margens superior/inferior, organização semântica ou que o arquivo realmente foi composto para frente e verso.

Não simule margens com espaços, `\hspace`, minipages globais ou alterações locais de geometria.

### Tabelas que ocupam várias páginas

Para tabelas numéricas extensas com `tables = tabularray`, use o ambiente **`longabnttblr`**, sem envolvê-lo em um `table` flutuante. O ambiente `tallabnttblr` é destinado a tabelas que não atravessam páginas. O tema ABNT do pacote tabularray fornece os indicadores de continuação em português. Cada página da tabela deve manter sua identificação e cabeçalho; a fonte e as notas cabem ao rodapé da página de conclusão, conforme a aplicação de §8.3 das normas tabulares do IBGE. A evidência automática do projeto cobre, por enquanto, uma tabela sintética controlada com casos negativos de cabeçalho e fonte; outras tabelas ainda exigem inspeção visual.

**Limitação conhecida na quebra entre páginas:** quando se utiliza `\\bottomrule` no corpo de `longabnttblr`, o mecanismo de rodapé de linhas do `tabularray` pode repetir esse traço nas páginas intermediárias. Embora a fonte e as notas sejam corretamente reservadas para a conclusão, esse traço pode contrariar o item 8.3(d) do IBGE. A verificação vetorial da PR #500 reproduz o problema em PDF real. Até que exista uma correção testada para o ambiente padrão, **não presuma conformidade do fechamento da tabela**: examine todas as páginas do PDF. A prova experimental também demonstra a possibilidade de deslocar a linha para o modelo `lastfoot` e omitir `\\bottomrule` no corpo da tabela, mas isso ainda não constitui solução automática da classe para documentos de usuários.

### Fechamento correto em tabela longa: modo explícito v3.1

Quando `tables = tabularray`, utilize o ambiente **`ufcibgelongtblr`** para uma tabela numérica que possa atravessar páginas. Ele reutiliza a identificação e os cabeçalhos do tema ABNT, colocando o traço separador exclusivamente no `lastfoot` antes de Fonte/Nota. Não inclua `\\bottomrule` no corpo: a classe sinaliza um erro explícito porque esse comando repetiria a linha nas páginas intermediárias.

O bloco opcional `[...]` contém os metadados da tabela (título, fonte e notas). O ambiente funciona também **sem o bloco opcional**, embora nesse caso o autor continue responsável por fornecer identificação e fonte quando as normas aplicáveis as exigirem.

```tex
\ufcsetup{tables = tabularray}

\begin{ufcibgelongtblr}[
  caption = {Resultados numéricos da pesquisa},
  remark{Fonte} = {Elaboração própria.},
  remark{Nota} = {Dados ilustrativos.}
]{
  colspec = {X[l] X[r]},
  width = 0.80\linewidth,
  rowhead = 1,
}
\toprule
Indicador & Valor \\
\midrule
Amostra A & 10 \\
Amostra B & 20 \\
% Acrescente as demais linhas; não inclua \bottomrule.
\end{ufcibgelongtblr}
```

A forma sem metadados opcionais é `\begin{ufcibgelongtblr}{colspec={l r}}`, seguida das linhas e de `\end{ufcibgelongtblr}`. Essa possibilidade é um contrato de sintaxe, **não uma dispensa das exigências normativas de título ou fonte**.

O ambiente existente `longabnttblr` **não foi alterado**. Nele, um `\\bottomrule` no corpo ainda pode se repetir nas páginas intermediárias. A evidência automática do opt-in é parcial, com amostras de uma e sete páginas; revise visualmente o PDF de depósito. Larguras variáveis, tabelas complexas e exceções normativas requerem validações adicionais.

### Fonte, tamanho e espaçamento

A política institucional coberta pelo projeto admite Times New Roman ou Arial para o corpo textual. Configure:

```tex
font = times,
strict-font = false
```

ou:

```tex
font = arial,
strict-font = true
```

`strict-font=true` exige a identidade literal da família configurada; ambientes portáveis podem usar fallback somente quando a política não for estrita. A classe controla o tamanho, o espaçamento e o recuo dos parágrafos normais.

### Seções e subseções

Use a hierarquia normal do LaTeX:

```tex
\section{Introdução}
\subsection{Objetivos}
\subsubsection{Objetivo específico}
\paragraph{Detalhamento}
\subparagraph{Observação}
```

A classe mantém até cinco níveis, aplica a numeração progressiva e controla a abertura das seções primárias. Evite construir títulos manualmente com negrito e quebras de linha.

## Elementos pré-textuais

O fluxo básico é:

```tex
\pretextual

\ufcPrintCover
\ufcPrintTitlePage
\ufcPrintApprovalPage
\ufcPrintSummary{frontmatter/summary}
\ufcPrintAbstract{frontmatter/abstract}
\ufcPrintTableOfContents
```

### Capa e folha de rosto

`\ufcPrintCover` usa os metadados de `\ufcsetup`. A chave `cover=false` omite a capa quando o perfil ou edital permitir.

`\ufcPrintTitlePage` produz a folha de rosto conforme o perfil selecionado.

### Folha de aprovação

`\ufcPrintApprovalPage` usa `approval-date`, orientador, coorientador e membros da banca configurados. Para versões destinadas ao depósito digital, siga a política institucional vigente sobre assinaturas; a classe não deve ser usada para inserir imagens de assinaturas como substituto do procedimento oficial.

### Elementos pré-textuais opcionais

Os seguintes elementos são ativados apenas quando fizerem sentido no trabalho:

```tex
\ufcPrintCatalogCard{frontmatter/catalog-card}
\ufcPrintErrata{frontmatter/errata}
\ufcPrintDedication{frontmatter/dedication}
\ufcPrintAcknowledgments{frontmatter/acknowledgments}
\ufcPrintEpigraph{frontmatter/epigraph}
```

A ficha catalográfica segue o procedimento institucional aplicável. Dedicatória, agradecimentos e epígrafe não precisam aparecer em todo trabalho. Quando houver financiamento sujeito à Portaria CAPES nº 206/2018, o agradecimento exigido deve ser incluído de acordo com a condição real do trabalho.

### Resumo, abstract e palavras-chave

O arquivo do resumo termina com:

```tex
\ufcSummaryKeywords{palavra 1; palavra 2; palavra 3.}
```

O abstract usa:

```tex
\keywords{keyword 1; keyword 2; keyword 3.}
```

O projeto valida a faixa de 150 a 500 palavras aplicada ao trabalho acadêmico de referência e a apresentação prevista no contrato vigente.

### Sumário e listas

O sumário é gerado com:

```tex
\ufcPrintTableOfContents
```

Elementos pré-textuais não entram no sumário. A hierarquia visual acompanha a hierarquia das seções e os números de página permanecem alinhados à direita.

As listas são opcionais. Exemplos:

```tex
\ufcPrintListOfIllustrations
\ufcPrintListOfTables
\ufcPrintListOfCodeListings
\ufcPrintListOfAlgorithms
\ufcPrintListOfAbbreviationsAndAcronyms{frontmatter/abbreviations-and-acronyms}
\ufcPrintListOfSymbols{frontmatter/symbols}
```

Produza apenas as listas úteis para o documento real.

## Texto acadêmico

Depois dos elementos pré-textuais:

```tex
\textual
```

Divida o trabalho em arquivos pequenos, por exemplo:

```tex
\input{chapters/1-introduction}
\input{chapters/2-theoretical-background}
\input{chapters/3-methodology}
\input{chapters/4-results}
\input{chapters/5-conclusion}
```

O tutorial distribuído segue exatamente essa estrutura.

### Citações

A infraestrutura bibliográfica usa `biblatex-abnt`. Prefira comandos bibliográficos em vez de digitar autor e ano manualmente.

Forma narrativa:

```tex
\textcite{lamport1994} descreve...
```

Forma parentética:

```tex
... no processo de preparação do documento \parencite{lamport1994}.
```

Uma citação direta real deve reproduzir a fonte consultada e informar o localizador aplicável. Citações longas usam o mecanismo da classe para manter recuo, fonte e espaçamento coerentes; não simule o bloco com espaços.

### Referências

Registre a base bibliográfica:

```tex
\ufcAddBibliographyResource{backmatter/references.bib}
```

e imprima a lista ao final:

```tex
\ufcPrintReferences
```

A apresentação segue o contrato da NBR 6023:2025 adotado pelo projeto: alinhamento à esquerda, espaço simples internamente e separação entre entradas conforme a regra implementada.

### Figuras, gráficos e outros objetos

O padrão de objeto da classe separa identificação, fonte e conteúdo:

```tex
\legend{figure}{Fluxo simplificado da análise}
\ufcSource{Elaboração própria.}
\label{fig:fluxo}
\begin{ufcobject}[here]
  \centering
  \includegraphics[width=.65\linewidth]{figures/example-flow.png}
\end{ufcobject}
```

A indicação de fonte é obrigatória no escopo exercitado pelo projeto. Para fonte externa, associe também a citação correspondente quando aplicável.

### Tabelas numéricas

Com `tables=tabularray`, o tutorial usa `tallabnttblr`. Tabelas numéricas seguem a apresentação tabular adotada pelo projeto: laterais abertas e regras horizontais estruturais, sem grade completa no corpo.

### Código-fonte e algoritmos

Ative o módulo desejado em `\ufcsetup`:

```tex
code = listings,
algorithms = algpseudocodex
```

Código externo pode ser incluído com:

```tex
\ufcInputListing[language=Python]{code/analysis.py}
```

A referência completa também documenta `ufclisting`, `\ufcInputMinted` e `ufcalgorithm`. A escolha do módulo de código ou da numeração de linhas é política editorial, não uma exigência geral da ABNT.

### Equações

Use os ambientes matemáticos normais do LaTeX:

```tex
\begin{equation}
  \bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
  \label{eq:media}
\end{equation}
```

Referencie a equação com `\ref{eq:media}` quando ela precisar ser identificada no texto.

## Elementos pós-textuais

### Referências

`\ufcPrintReferences` deve aparecer depois do texto principal e antes dos demais elementos pós-textuais aplicáveis.

### Glossário

Com `glossary=glossaries`, declare as entradas em um arquivo carregado no preâmbulo e imprima:

```tex
\ufcPrintGlossary
```

Use glossário somente quando as definições realmente ajudarem o leitor.

### Apêndices e anexos

Material elaborado pelo autor:

```tex
\appendix{Instrumento de validação}
\input{backmatter/appendices/appendix-a}
```

Material externo:

```tex
\annex{Documento complementar externo}
\input{backmatter/annexes/annex-a}
```

Cada elemento inicia em página própria e recebe a apresentação de cabeçalho definida pela classe.

### Índice

O índice remissivo é opcional. Para habilitá-lo:

```tex
index = imakeidx
```

marque termos com `\index{...}` e imprima `\ufcPrintIndex`. O tutorial não gera índice por padrão.

## PDF/A e validação

O template declara os metadados PDF antes de `\documentclass`:

```tex
\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}
```

PDF/A-2b é o alvo técnico de certificação do projeto. A presença da declaração no fonte não é prova suficiente: a release valida o PDF efetivamente produzido, a incorporação de fontes e a estrutura disponível.

Para validação local profunda:

```bash
python3 tools/validate-ufc-pdf.py template/main.pdf --profile strict
```

O Web/Lite oferece verificações compatíveis com o navegador, mas não promove checks profundos indisponíveis a PASS automático.

## Compilação

No repositório:

```bash
make compile
```

O fluxo chama Biber, glossário e índice quando necessários e executa as passagens adicionais de LaTeX para estabilizar referências.

Para desenvolvimento:

```bash
make check
```

Para certificação de release:

```bash
make release-check
```

O último comando é um gate de engenharia do projeto, não uma etapa exigida de um aluno que apenas usa o template.

## Checklist de entrega

Antes de entregar:

1. confirme o perfil e os metadados;
2. remova conteúdo e arquivos demonstrativos que não pertencem ao trabalho;
3. confira todas as citações contra as fontes realmente consultadas;
4. revise referências, figuras, tabelas, códigos e equações;
5. mantenha apenas elementos pré e pós-textuais aplicáveis;
6. execute a compilação completa;
7. verifique visualmente o PDF inteiro;
8. valide PDF/A e fontes quando o procedimento de depósito exigir;
9. confira as regras atuais do curso/programa e do Sistema de Bibliotecas da UFC.

## Autoridade normativa

A rastreabilidade normativa detalhada permanece em [NORMATIVE-BASE.md](NORMATIVE-BASE.md), [NORMATIVE-CURRENCY.md](NORMATIVE-CURRENCY.md) e no contrato de máquina em `standards/`. Este guia é documentação secundária de uso e não cria requisitos novos.

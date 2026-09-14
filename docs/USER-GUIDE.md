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

Não simule margens com espaços, `\hspace`, minipages globais ou alterações locais de geometria.

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

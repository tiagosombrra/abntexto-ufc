# Base normativa da V2

Última auditoria: **2026-08-20**.

Este arquivo registra a política normativa, a classificação da auditoria e o mapa de implementação da V2 do modelo LaTeX UFC.

## Política normativa

A V2 adota a edição vigente mais recente de cada norma aplicável. Quando um guia institucional ainda citar edição substituída, a decisão segue esta ordem:

1. legislação, regulamento, instrução normativa ou resolução institucional aplicável;
2. edição vigente da norma ABNT;
3. requisito institucional específico da UFC compatível com a norma vigente;
4. Guia de Normalização da UFC mais recente aplicável;
5. comportamento de `abntexto` e demais pacotes.

O comportamento de um pacote nunca prevalece sobre requisito normativo ou institucional aplicável.

## Auditoria institucional de 2026-08-20

A página de Normalização de Trabalhos Acadêmicos do Sistema de Bibliotecas da UFC foi atualizada em 4 de março de 2026 e declara que os guias institucionais estão de acordo com as normas ABNT vigentes. Entretanto, os PDFs atualmente vinculados possuem datas e bases normativas diferentes:

| Documento UFC atualmente vinculado | Base declarada no PDF | Situação na auditoria |
|---|---|---|
| Guia de Normalização de Trabalhos Acadêmicos, 2022 | NBR 14724:2011, NBR 6023:2018, NBR 10520:2002 e NBR 12225:2004 | usar requisitos institucionais apenas quando compatíveis com as normas vigentes |
| Guia de Normalização para Elaboração de Citações, 2025 | NBR 10520:2023 e NBR 6023:2018 | NBR 10520:2023 atual; referência à NBR 6023:2018 superada pela edição de 2025 |
| Guia de Normalização para Elaboração de Referências | NBR 6023:2018 | superado pela NBR 6023:2025 |
| Guia de Normalização de Projetos de Pesquisa | NBR 15287:2011 e outras edições históricas | superado pela NBR 15287:2025 e pelas demais normas vigentes aplicáveis |

A Instrução Normativa Conjunta nº 2/2026/SIBI/PROGRAD/PRPPG, de 10 de fevereiro de 2026, tem precedência sobre disposições técnicas conflitantes de guias anteriores. Ela torna facultativa a ficha catalográfica visual para TCC, dissertação e tese depositados no Repositório Institucional e revoga disposições técnicas em contrário dos manuais e guias anteriores.

Consequentemente, a data de um PDF institucional não é tratada como prova de vigência normativa. Cada requisito é confrontado com a norma ABNT vigente e com atos institucionais posteriores.

## Normas adotadas

| Assunto | Referência | Uso principal |
|---|---|---|
| Trabalhos acadêmicos | **ABNT NBR 14724:2024**, versão corrigida de 01/04/2025 | estrutura, apresentação, paginação e elementos documentais |
| Citações | **ABNT NBR 10520:2023** | citações diretas, indiretas, autor-data e `apud` |
| Referências | **ABNT NBR 6023:2025** | elaboração e apresentação das referências |
| Projetos de pesquisa | **ABNT NBR 15287:2025** | perfis `projeto` e `projetoanonimizado` |
| Resumos | **ABNT NBR 6028:2021** | resumo, abstract e palavras-chave |
| Numeração progressiva | **ABNT NBR 6024:2012** | seções e subdivisões |
| Sumário | **ABNT NBR 6027:2012** | composição e hierarquia do Sumário |
| Índice | **ABNT NBR 6034:2004** | índice remissivo opcional |
| Lombada | **ABNT NBR 12225:2023** | requisito condicional |
| Tabelas numéricas | **IBGE, Normas de apresentação tabular, 3. ed., 1993** | estrutura de tabelas numéricas |

As edições devem ser reconfirmadas antes de cada nova versão principal do template.

## Classificação da auditoria 2026-08-20

Estados usados:

- **CONFORME**: requisito implementado e sustentado por teste próprio, implementação explícita ou comportamento upstream auditado;
- **CONFORME NO ESCOPO TESTADO**: requisito amplo cuja parcela exercitada possui evidência suficiente;
- **DIVERGENTE**: implementação atual contraria requisito vigente;
- **INCOMPLETO**: regra conhecida, mas falta decisão técnica, cobertura ou gate para a próxima release;
- **NÃO APLICÁVEL**: requisito condicional fora do escopo da distribuição corrente.

| Requisito | Estado | Evidência / decisão |
|---|---|---|
| papel A4 | **CONFORME** | `tests/v2-pdf-geometry-check.sh` mede o PDF real |
| margens anverso 3 cm esquerda/superior e 2 cm direita/inferior | **CONFORME** | `ufctex/layout.def` + gate geométrico |
| margens espelhadas no frente-verso | **CONFORME** | `ufctex/layout.def` + gate geométrico |
| fonte-base em tamanho 12 | **CONFORME** | `ufctex.cls` carrega `abntexto` em 12 pt |
| família Arial ou Times New Roman literal | **DIVERGENTE** | pdfLaTeX usa NewTX; LuaLaTeX admite fallback TeX Gyre Termes |
| variantes regular/negrito/itálico/negrito-itálico da família institucional | **INCOMPLETO** | gate atual verifica incorporação, não identidade tipográfica |
| tamanhos reduzidos uniformes nas exceções | **INCOMPLETO** | citação longa e nota já usam 10 pt; falta gate tipométrico para todas as exceções |
| recuo da primeira linha do parágrafo em 2 cm conforme guia UFC | **CONFORME** | `ufctex/layout.def` usa 2 cm e `tests/v2-layout-check.sh` mede o valor efetivo |
| ausência de espaço adicional entre parágrafos | **CONFORME** | `\parskip=0pt` |
| espaço 1,5 no corpo | **CONFORME** | `\onehalfsp` aplicado no início do documento |
| natureza do trabalho em espaço simples | **CONFORME** | capa/folha de rosto usam minipage com `\singlesp` |
| notas de rodapé em tamanho reduzido e espaço simples | **CONFORME** | `\abntsmall\singlesp` + gate de tamanho/entrelinha |
| filete de 5 cm das notas de rodapé | **CONFORME** | `\footnoterule` redefine largura para 5 cm |
| linhas subsequentes da nota alinhadas sob a primeira letra do texto | **CONFORME** | recuo suspenso implementado e medido por `tests/v2-layout-check.sh` |
| estrutura principal baseada em seções, sem capítulos | **CONFORME** | `\usechapters` gera erro e distribuição bloqueia `\chapter` |
| cinco níveis de seção e correspondência no Sumário | **CONFORME** | hierarquia definida em `layout.def` e TOC exercitado nos gates |
| início de seção primária em nova página/anverso | **CONFORME** | `\ufcPrimarySectionBreak` + testes duplex |
| alinhamento de títulos de seção com mais de uma linha | **CONFORME** | `abntexto` compõe seções numeradas com `\hangfrom`, alinhando linhas seguintes após o indicativo |
| capa e folha de rosto | **CONFORME** | perfis e pré-textuais exercitados nos dois motores |
| natureza/orientação a partir do meio da mancha gráfica | **CONFORME** | bloco textual deslocado 8 cm |
| folha de aprovação sem imagens de assinatura para depósito | **CONFORME** | classe gera linhas e identificação, sem incorporar assinaturas |
| ficha catalográfica visual facultativa | **CONFORME** | padrão `ficha-catalografica=nao` conforme IN Conjunta 2/2026 |
| ficha catalográfica não contada nem numerada | **CONFORME** | contador lógico é restaurado; duplex registra a página física não contada; gate cobre dois motores e dois modos |
| contagem dos pré-textuais e numeração somente a partir do textual | **CONFORME** | gates de paginação, ficha e geometria cobrem a sequência lógica |
| posição da paginação anverso/frente-verso | **CONFORME** | gate geométrico mede canto superior direito/esquerdo |
| paginação contínua em apêndices e anexos | **CONFORME** | pós-textuais preservam a sequência |
| trabalhos em mais de um volume | **CONFORME** | volume em capa/folha de rosto e `pagina-inicial` testados |
| dedicatória sem título | **CONFORME** | gate pré-textual verifica ausência de título |
| agradecimentos, errata, resumo, abstract e listas | **CONFORME** | títulos e presença exercitados nos gates |
| epígrafe longa em 10 pt, espaço simples e recuo de 4 cm | **CONFORME** | implementação explícita em `pretextuais.def` |
| resumo e abstract sem recuo de primeira linha | **CONFORME** | `\parindent=0pt` nos dois elementos |
| resumo/abstract entre 150 e 500 palavras | **CONFORME** | `tests/v2-reference-check.sh` conta palavras |
| palavras-chave/keywords | **CONFORME** | API e documento de referência exercitados |
| pré-textuais fora do Sumário | **CONFORME** | gate verifica que não entram no TOC |
| pré-textuais iniciando em anverso no duplex | **CONFORME** | `tests/v2-duplex-pretextual-check.sh` mede página física |
| citação autor-data, autores múltiplos, pessoa jurídica, homônimos e `apud` | **CONFORME** | `tests/v2-bibliography-check.sh` cobre os casos principais da NBR 10520:2023 |
| citação direta longa: fonte menor, simples, sem aspas, recuo de 4 cm e separação vertical | **CONFORME** | `tests/v2-normative-complement-check.sh` mede recuo/tamanho/entrelinha; `\Enquote` do `abntexto` implementa o bloco sem aspas e com `aboveEnquote`/`belowEnquote` |
| referências em espaço simples | **CONFORME** | gate mede `baselinestretch` |
| uma linha simples entre referências | **CONFORME** | gate mede `bibitemsep` e `itemsep` efetivo |
| NBR 6023:2025 | **CONFORME NO ESCOPO TESTADO** | regressões cobrem evento, e-location, data de julgamento, dados desconhecidos, suplemento, entrevista, ISSN, DOI e ORCID |
| referências próprias de anexo no próprio anexo | **INCOMPLETO** | requisito é conhecido; falta exemplo/regressão com referência bibliográfica local no anexo |
| identificação, título, fonte, legenda e nota de ilustrações dentro dos limites da ilustração | **DIVERGENTE** | `abntexto` limita o título por `legendmaxwidth=.7\linewidth`, independente de `savedplacewidth`; em ilustrações estreitas um título longo pode ultrapassar a largura do objeto |
| indicação de fonte de elaboração própria | **CONFORME** | fixtures usam e gate verifica `Fonte:` |
| fonte externa de ilustração/tabela conforme NBR 10520 | **INCOMPLETO** | API aceita texto livre; falta fixture normativa com citação externa |
| Lista de Ilustrações agregando figuras, gráficos e quadros | **CONFORME** | regressão verifica conteúdo e exclui tabelas |
| tabelas em lista própria | **CONFORME** | regressões exercitam lista de tabelas |
| apresentação tabular segundo IBGE | **INCOMPLETO** | suporte `tabularray-abnt` existe; gate não cobre regras tabulares mínimas do projeto |
| equações e fórmulas | **CONFORME NO ESCOPO TESTADO** | fixture específica verifica equação numerada e referência resolvida; posicionamento segue o ambiente `equation` do LaTeX |
| tipografia de código/listings/minted | **DIVERGENTE** | exemplo público usa `\ttfamily\small`; não foi localizada exceção institucional de família para código |
| tipografia de algoritmos | **INCOMPLETO** | falta política explícita de família/tamanho e gate correspondente |
| tipografia matemática | **INCOMPLETO** | família matemática precisa ser complementar e explicitamente documentada; Arial/Times não cobrem sozinhas o repertório matemático |
| estrutura de projetos NBR 15287:2025 | **CONFORME NO ESCOPO TESTADO** | fixture cobre introdução, problema, objetivos, justificativa, referencial, metodologia, recursos, cronograma e referências |
| projeto anonimizado sem vazamento de autor/orientador | **CONFORME** | gate semântico específico |
| glossário, apêndice, anexo e índice | **CONFORME NO ESCOPO TESTADO** | ordem, presença, TOC e início no anverso são verificados |
| ênfase tipográfica de títulos de apêndices/anexos igual à seção primária | **CONFORME** | `abntexto` implementa `\appendix`/`\annex` como seções primárias sem número, reutilizando `mainsecname` e `sectionfont` |
| agradecimento obrigatório à CAPES quando aplicável | **INCOMPLETO** | requisito é condicional ao financiamento; template deve orientar o autor, não inferir a condição |
| lombada NBR 12225:2023 | **NÃO APLICÁVEL à distribuição eletrônica corrente** | extensão condicional futura para versão física |
| PDF/A para depósito | **CONFORME** | `\DocumentMetadata` + validação independente com veraPDF |
| PDF/A-2b | **CONFORME COMO ESCOLHA TÉCNICA DO PROJETO** | não é apresentado como subtipo imposto pela UFC |

## Gate N — encerrado

A auditoria normativa de 2026 está **fechada em 20/08/2026**. Não há requisito crítico sem origem normativa ou decisão explícita.

O fechamento do Gate N não significa que a implementação atual esteja integralmente conforme. Significa que as divergências e lacunas estão identificadas, classificadas e possuem destino definido na Fase 2.

### Divergências que a Fase 2 deve corrigir

1. implementar Arial e Times New Roman literais e política explícita de fallback/erro;
2. impedir que título, fonte, legenda e nota ultrapassem os limites da ilustração;
3. remover a família monoespaçada como padrão normativo de código, salvo se surgir orientação institucional posterior que autorize explicitamente a exceção.

### Itens incompletos que a Fase 2 deve fechar

1. identidade das variantes regular/negrito/itálico/negrito-itálico;
2. uniformidade dos tamanhos reduzidos em todas as exceções;
3. exemplo e teste de referência bibliográfica própria de anexo;
4. exemplo e teste de fonte externa de ilustração/tabela conforme NBR 10520;
5. subconjunto verificável das regras tabulares do IBGE;
6. política tipográfica de algoritmos;
7. política da fonte matemática complementar;
8. orientação ao autor sobre agradecimento à CAPES quando aplicável.

Os itens corrigidos durante a própria auditoria — recuo de parágrafo, ficha catalográfica em duplex e alinhamento multilinha de notas de rodapé — não permanecem na lista de divergências.

## Requisitos institucionais UFC

### Tipografia

O Guia UFC de Trabalhos Acadêmicos atualmente vinculado exige **Arial ou Times New Roman, tamanho 12**, inclusive na capa. Prevê tamanho menor e uniforme para citações longas, notas de rodapé, paginação, ficha catalográfica, legendas e fontes de ilustrações e tabelas, recomendando tamanho 10 para essas exceções.

A V2 deve distinguir a família tipográfica literal de substitutos metricamente ou visualmente compatíveis. `NewTX` e `TeX Gyre Termes` não podem ser declaradas como Times New Roman.

Não foi localizada, na documentação institucional auditada, exceção de família para ambientes de código. Matemática é tratada separadamente porque necessita de repertório tipográfico próprio e não pode ser resolvida apenas pela família textual.

### PDF/A

As orientações de recebimento consultadas em 2026 exigem arquivo eletrônico **PDF/A** para TCC, dissertações e teses destinados ao repositório.

A V2 usa **PDF/A-2b** como perfil técnico verificável. O subtipo 2b é escolha de implementação do projeto, não requisito específico atribuído à UFC.

### Folha de aprovação

A versão destinada ao repositório deve apresentar a folha de aprovação sem assinaturas. A V2 produz identificação e linhas da banca, mas não incorpora assinaturas digitalizadas.

### Ficha catalográfica

A Instrução Normativa Conjunta nº 2/2026 torna facultativa a representação visual da ficha catalográfica para TCC, dissertações e teses. Por isso, `ficha-catalografica=nao` permanece o padrão.

Quando a ficha for incluída, a NBR 14724:2024 vigente determina que o verso da folha de rosto com os dados catalográficos **não seja contado nem numerado**. A implementação atual restaura o contador lógico e mantém a paridade física correta também no modo `frente-verso`.

Como a ficha é um PDF externo, sua inclusão pode alterar a conformidade PDF/A; o arquivo completo deve ser validado novamente com veraPDF.

### Trabalhos em mais de um volume

A identificação do volume deve aparecer quando o trabalho for dividido em mais de um volume, e a paginação permanece única e sequencial entre os volumes. A V2 oferece `volume` e `pagina-inicial`, com regressão própria.

### Frente e verso

No modo `frente-verso`:

- anverso: esquerda/superior 3 cm; direita/inferior 2 cm;
- verso: direita/superior 3 cm; esquerda/inferior 2 cm;
- numeração à direita no anverso e à esquerda no verso;
- elementos pré-textuais, exceto a página destinada aos dados catalográficos, iniciam no anverso;
- seções textuais primárias e elementos pós-textuais controlados pela V2 iniciam no anverso.

### Paginação

Os elementos pré-textuais são contados a partir da folha de rosto e não são numerados. O verso da folha de rosto destinado aos dados catalográficos não é contado nem numerado. A numeração aparece a partir da primeira página textual. Em frente e verso, a posição alterna entre o canto superior direito no anverso e o superior esquerdo no verso. Apêndices, anexos e volumes mantêm sequência contínua.

### Espaçamento

O Guia UFC orienta espaço 1,5 no corpo do trabalho e espaço simples nas exceções institucionais, incluindo citações longas, notas de rodapé, referências, legendas, ficha catalográfica e natureza do trabalho. Não deve existir espaço adicional entre parágrafos. Referências consecutivas são separadas por uma linha simples em branco.

### Resumo e abstract

O documento de referência mantém resumo e abstract entre 150 e 500 palavras, sem recuo na primeira linha, e usa palavras-chave após o texto.

### Ilustrações e tabelas

A NBR 14724:2024 determina que tipo, número, título, fonte, legenda e notas acompanhem os limites da própria ilustração. A fonte consultada deve seguir a NBR 10520; quando o objeto for do próprio autor, deve haver indicação equivalente a “Elaboração própria”.

A implementação upstream atualmente dimensiona a caixa de fonte pela largura real do objeto, mas não vincula da mesma forma a largura máxima do título. Esse ponto é correção obrigatória da Fase 2.

A Lista de Ilustrações agrega figuras, gráficos e quadros na ordem de ocorrência. Tabelas permanecem em lista própria.

### Citações

O Guia UFC de Citações de 2025 foi elaborado conforme a NBR 10520:2023. Para citações diretas com mais de três linhas, orienta parágrafo distinto, letra menor que a do texto, espaço simples, sem aspas, recomenda recuo de 4 cm e exige separação do texto anterior/posterior por espaço simples em branco.

O comando `\Enquote` do `abntexto` implementa esses aspectos; a V2 mede recuo, tamanho e entrelinha em regressão própria.

### Referências

O PDF institucional atualmente vinculado ainda usa NBR 6023:2018. Para a V2 prevalece a NBR 6023:2025. As referências usam espaçamento simples internamente e intervalo equivalente a uma linha simples entre entradas consecutivas.

A NBR 14724:2024 também determina que referências próprias de um anexo, quando houver, sejam apresentadas no próprio anexo, em nota de rodapé ou lista específica. A Fase 2 deve acrescentar exemplo público e regressão para esse caso.

### Projetos de pesquisa

O Guia UFC de Projetos atualmente vinculado ainda declara NBR 15287:2011. Para os perfis `projeto` e `projetoanonimizado`, a V2 adota NBR 15287:2025 e preserva apenas requisitos institucionais compatíveis com a edição vigente.

## Mapa de implementação

| Parte | Norma/requisito principal | Implementação |
|---|---|---|
| configuração e perfis | política UFC + normas por tipo | `ufctex/core.def` |
| tipografia | NBR 14724:2024 + requisito UFC Arial/Times New Roman | atualmente em `ufctex/layout.def`; deve migrar para módulo próprio |
| papel, margens e espaçamento | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| duplex e início no anverso | NBR 14724:2024 + UFC | `ufctex/layout.def` + regressões geométricas |
| ativos institucionais | identidade visual UFC | `ufctex/institucional.def` + `assets/institucional/` |
| capa e folha de rosto | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` + `ufctex/trabalhos.def` |
| volume e paginação contínua | NBR 14724:2024 + UFC | `ufctex/trabalhos.def` |
| ficha catalográfica | IN Conjunta 2/2026 + NBR 14724:2024 | `ufctex/trabalhos.def` + regressão dedicada |
| folha de aprovação | NBR 14724:2024 + política de depósito UFC | `ufctex/pretextuais.def` |
| dedicatória, agradecimentos, epígrafe e errata | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| resumo e abstract | NBR 6028:2021 + UFC | `ufctex/pretextuais.def` |
| listas e Sumário | NBR 14724:2024 + NBR 6027:2012 | `ufctex/pretextuais.def` + `ufctex/objetos.def` |
| seções e subdivisões | NBR 6024:2012 + UFC | `ufctex/layout.def` / `abntexto` |
| figuras, gráficos e quadros | NBR 14724:2024 + UFC | `ufctex/objetos.def` + infraestrutura `place` do `abntexto` |
| tabelas numéricas | NBR 14724:2024 + IBGE | `ufctex/objetos.def` + `tabularray-abnt` |
| código e algoritmos | extensão editorial sob política tipográfica UFC | `ufctex/objetos.def` + `ufctex/modulos.def` |
| citações | NBR 10520:2023 | `ufctex/bibliografia.def` + `abntexto` para citação longa |
| referências | NBR 6023:2025 | `ufctex/bibliografia.def` + `ufctex/compat-nbr6023-2025.def` |
| projetos | NBR 15287:2025 | `ufctex/projetos.def` |
| glossário | NBR 14724:2024 | módulo opcional |
| apêndices e anexos | NBR 14724:2024 | API pública do `abntexto` + política V2 de quebra |
| índice | NBR 6034:2004 | módulo opcional |
| PDF/A | política institucional UFC | `\DocumentMetadata` + veraPDF |
| compatibilidade V1 | transição de documentos | `ufctex/compat-v1.def` |

## Compatibilidade dos pacotes

`abntexto`, `biblatex-abnt`, `tabularray-abnt` e demais pacotes são infraestrutura. A versão de um pacote não define, isoladamente, o nível de conformidade normativa da V2.

Os ajustes necessários para NBR 6023:2025 permanecem isolados em `ufctex/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível de forma estável no upstream.

## Build e gates

`make preflight` executa consistência da distribuição, documento de referência, layout, geometria, pré-textuais, duplex, ficha catalográfica, multivolume, estruturas normativas complementares, objetos, bibliografia, projetos, matriz de seis perfis nos dois motores, pós-textuais, compatibilidade V1 e fluxo modular do Makefile.

A matriz final produz **12 PDFs**: seis perfis × dois motores. Cada PDF é verificado quanto a conteúdo específico, A4, fontes incorporadas, Sumário, ausência de `chapter`, warnings/overflow reconhecidos e declaração PDF/A-2b.

`make release-preflight` acrescenta veraPDF para o documento de referência e os 12 PDFs da matriz.

A Fase 2 deve acrescentar ou ampliar gates para:

- identidade tipográfica literal e variantes;
- tamanhos tipográficos reduzidos;
- geometria de título/fonte/nota de ilustrações;
- fonte externa de objetos conforme NBR 10520;
- referências específicas de anexos;
- subconjunto tabular IBGE;
- política tipográfica de código, algoritmos e matemática.

## Fontes institucionais de verificação

- Sistema de Bibliotecas da UFC — Normalização de trabalhos acadêmicos: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Guia de Normalização de Trabalhos Acadêmicos atualmente vinculado: https://biblioteca.ufc.br/wp-content/uploads/2022/05/guianormalizacaotrabalhosacademicos-17.05.2022.pdf
- Guia de Normalização para Elaboração de Citações 2025: https://biblioteca.ufc.br/wp-content/uploads/2025/06/guianormalizacaocitacoes2025.pdf
- Guia de Normalização para Elaboração de Referências atualmente vinculado: https://biblioteca.ufc.br/wp-content/uploads/2023/12/guianormalizacaoreferencias.pdf
- Guia de Normalização de Projetos de Pesquisa atualmente vinculado: https://biblioteca.ufc.br/wp-content/uploads/2019/10/guia-de-projetos-06.10.2019.pdf
- Sistema de Bibliotecas da UFC — Normas para recebimento de teses e dissertações: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-teses-e-dissertacoes/
- Sistema de Bibliotecas da UFC — Normas para recebimento de TCC: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-tcc/
- Instrução Normativa Conjunta nº 2/2026: https://biblioteca.ufc.br/wp-content/uploads/2026/02/instrucao-normativa-conjunta-2.pdf
- Sistema de Bibliotecas da UFC — FAQ da ficha catalográfica: https://biblioteca.ufc.br/pt/perguntas-frequentes/ficha-catalografica-2/
- Sistema de Bibliotecas da UFC — Coleção de Normas Técnicas: https://biblioteca.ufc.br/pt/colecao-de-normas-tecnicas/
- ABNT Catálogo: https://www.abntcatalogo.com.br/

## Manutenção

Antes de nova versão principal:

1. reconfirmar as edições normativas;
2. revisar páginas e guias da UFC;
3. revisar políticas de depósito e ficha catalográfica;
4. atualizar ou remover patches de compatibilidade;
5. resolver todas as divergências classificadas;
6. promover itens `INCOMPLETO` somente após evidência adequada;
7. executar `make preflight`;
8. executar `make release-preflight`;
9. confirmar `latex-preflight` no CI;
10. não declarar conformidade que não possua evidência compatível.

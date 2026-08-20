# Base normativa da V2

Última auditoria normativa: **2026-08-20**.
Estado de implementação tipográfica: **Fase 2 em validação**.

Este arquivo é a fonte única do projeto para política normativa, classificação de conformidade e vínculo entre requisito, implementação e teste.

## Política normativa

A V2 adota a edição vigente mais recente de cada norma aplicável. Quando um guia institucional ainda citar edição substituída, a decisão segue esta ordem:

1. legislação, regulamento, instrução normativa ou resolução institucional aplicável;
2. edição vigente da norma ABNT;
3. requisito institucional específico da UFC compatível com a norma vigente;
4. Guia de Normalização da UFC mais recente aplicável;
5. comportamento de `abntexto` e demais pacotes.

O comportamento de um pacote nunca prevalece sobre requisito normativo ou institucional aplicável.

## Auditoria institucional de 2026-08-20

A página de Normalização de Trabalhos Acadêmicos do Sistema de Bibliotecas da UFC foi atualizada em 4 de março de 2026 e declara que os guias institucionais estão de acordo com as normas ABNT vigentes. Os PDFs vinculados, porém, possuem datas e bases normativas diferentes.

| Documento UFC atualmente vinculado | Base declarada no PDF | Situação na auditoria |
|---|---|---|
| Guia de Normalização de Trabalhos Acadêmicos, 2022 | NBR 14724:2011, NBR 6023:2018, NBR 10520:2002 e NBR 12225:2004 | preservar requisitos institucionais somente quando compatíveis com as normas vigentes |
| Guia de Normalização para Elaboração de Citações, 2025 | NBR 10520:2023 e NBR 6023:2018 | NBR 10520:2023 atual; referência à NBR 6023:2018 superada pela edição de 2025 |
| Guia de Normalização para Elaboração de Referências | NBR 6023:2018 | superado pela NBR 6023:2025 |
| Guia de Normalização de Projetos de Pesquisa | NBR 15287:2011 e outras edições históricas | superado pela NBR 15287:2025 e pelas demais normas vigentes aplicáveis |

A Instrução Normativa Conjunta nº 2/2026/SIBI/PROGRAD/PRPPG, de 10 de fevereiro de 2026, tem precedência sobre disposições técnicas conflitantes de guias anteriores. Ela torna facultativa a ficha catalográfica visual para TCC, dissertação e tese depositados no Repositório Institucional e revoga disposições técnicas em contrário dos manuais e guias anteriores.

A data de um PDF institucional não é tratada como prova isolada de vigência normativa.

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

## Estados da matriz

- **CONFORME**: requisito implementado e sustentado por evidência/teste compatível;
- **CONFORME NO ESCOPO TESTADO**: requisito amplo cuja parcela exercitada possui evidência suficiente;
- **DIVERGENTE**: implementação atual contraria requisito vigente;
- **INCOMPLETO**: regra conhecida, mas falta decisão técnica, cobertura ou evidência exigida para a próxima release;
- **NÃO APLICÁVEL**: requisito condicional fora do escopo da distribuição corrente.

Um fallback de compatibilidade não transforma um PDF em tipograficamente conforme. Para a família textual, conformidade final exige **Arial ou Times New Roman literais** no PDF produzido.

## Matriz requisito → implementação → teste

| Requisito | Estado | Evidência / decisão |
|---|---|---|
| papel A4 | **CONFORME** | `tests/v2-pdf-geometry-check.sh` mede o PDF real |
| margens anverso 3 cm esquerda/superior e 2 cm direita/inferior | **CONFORME** | `ufctex/layout.def` + gate geométrico |
| margens espelhadas no frente-verso | **CONFORME** | `ufctex/layout.def` + gate geométrico |
| fonte-base em tamanho 12 | **CONFORME** | `abntexto` carregado em 12 pt; gates tipográficos medem o tamanho nominal |
| seleção pública `fonte=times|arial` | **CONFORME NO ESCOPO TESTADO** | `ufctex/fontes.def` + `tests/v2-font-config-check.sh` |
| política `fonte-estrita=sim|nao` | **CONFORME NO ESCOPO TESTADO** | modo estrito rejeita fonte literal ausente; modo não estrito registra fallback explicitamente |
| Times New Roman/Arial literais no PDF final | **INCOMPLETO** | implementação existe; falta fechar a POC Windows e a certificação completa do Gate T |
| variantes regular/negrito/itálico/negrito-itálico das fontes literais | **INCOMPLETO** | POC valida as quatro variantes; evidência Windows ainda precisa ser fechada |
| `rmfamily`, `sffamily` e `ttfamily` preservando a família institucional | **CONFORME NO ESCOPO TESTADO** | `fontes.def` mapeia os três slots; `v2-font-config-check.sh` exerce os três |
| tamanhos reduzidos uniformes nas exceções | **INCOMPLETO** | citação longa, nota e título de objeto já usam 10 pt; falta completar cobertura tipométrica de todas as exceções |
| recuo da primeira linha do parágrafo em 2 cm | **CONFORME** | `layout.def` + `tests/v2-layout-check.sh` |
| ausência de espaço adicional entre parágrafos | **CONFORME** | `\parskip=0pt` |
| espaço 1,5 no corpo | **CONFORME** | `\onehalfsp` aplicado no início do documento |
| natureza do trabalho em espaço simples | **CONFORME** | capa/folha de rosto usam bloco em `\singlesp` |
| notas de rodapé em tamanho reduzido e espaço simples | **CONFORME** | `\abntsmall\singlesp` + gate de tamanho/entrelinha |
| filete de 5 cm das notas de rodapé | **CONFORME** | `\footnoterule` redefine largura para 5 cm |
| linhas subsequentes da nota alinhadas sob a primeira letra do texto | **CONFORME** | recuo suspenso medido em `tests/v2-layout-check.sh` |
| estrutura principal baseada em seções, sem capítulos | **CONFORME** | `\usechapters` gera erro e distribuição bloqueia `\chapter` |
| cinco níveis de seção e correspondência no Sumário | **CONFORME** | hierarquia definida em `layout.def` e TOC exercitado nos gates |
| início de seção primária em nova página/anverso | **CONFORME** | `\ufcPrimarySectionBreak` + testes duplex |
| alinhamento de títulos de seção com mais de uma linha | **CONFORME** | `abntexto` usa composição suspensa após o indicativo; comportamento auditado |
| capa e folha de rosto | **CONFORME** | perfis e pré-textuais exercitados nos dois motores |
| natureza/orientação a partir do meio da mancha gráfica | **CONFORME** | bloco textual deslocado conforme política UFC |
| folha de aprovação sem imagens de assinatura para depósito | **CONFORME** | classe não incorpora assinaturas digitalizadas |
| ficha catalográfica visual facultativa | **CONFORME** | `ficha-catalografica=nao` é o padrão conforme IN Conjunta 2/2026 |
| ficha catalográfica não contada nem numerada | **CONFORME** | contador lógico e paridade física testados em dois motores e dois modos |
| contagem dos pré-textuais e numeração somente a partir do textual | **CONFORME** | gates de paginação, ficha e geometria |
| posição da paginação anverso/frente-verso | **CONFORME** | gate geométrico mede canto superior direito/esquerdo |
| paginação contínua em apêndices e anexos | **CONFORME** | pós-textuais preservam a sequência |
| trabalhos em mais de um volume | **CONFORME** | `volume` e `pagina-inicial` com regressão própria |
| dedicatória sem título | **CONFORME** | gate pré-textual verifica ausência de título |
| agradecimentos, errata, resumo, abstract e listas | **CONFORME** | presença e títulos exercitados nos gates |
| epígrafe longa em 10 pt, espaço simples e recuo de 4 cm | **CONFORME** | implementação explícita em `pretextuais.def` |
| resumo e abstract sem recuo de primeira linha | **CONFORME** | `\parindent=0pt` nos dois elementos |
| resumo/abstract entre 150 e 500 palavras | **CONFORME** | `tests/v2-reference-check.sh` conta palavras |
| palavras-chave/keywords | **CONFORME** | API e documento de referência exercitados |
| pré-textuais fora do Sumário | **CONFORME** | gate verifica que não entram no TOC |
| pré-textuais iniciando em anverso no duplex | **CONFORME** | `tests/v2-duplex-pretextual-check.sh` |
| citação autor-data, autores múltiplos, pessoa jurídica, homônimos e `apud` | **CONFORME** | `tests/v2-bibliography-check.sh` |
| citação direta longa: fonte menor, simples, sem aspas, recuo de 4 cm e separação vertical | **CONFORME** | `v2-normative-complement-check.sh` + comportamento auditado de `\Enquote` |
| referências em espaço simples | **CONFORME** | gate mede o espaçamento efetivo |
| uma linha simples entre referências | **CONFORME** | gate mede `bibitemsep`/`itemsep` |
| NBR 6023:2025 | **CONFORME NO ESCOPO TESTADO** | regressões cobrem os casos implementados pelo projeto |
| referências próprias de anexo no próprio anexo | **INCOMPLETO** | falta fixture com referência bibliográfica local real |
| título de ilustração limitado à largura real do objeto | **CONFORME** | `objetos.def` usa `min(legendmaxwidth,savedplacewidth)`; `v2-object-geometry-check.sh` mede objeto de 6 cm |
| título de ilustração em tamanho reduzido | **CONFORME** | `\abntsmall\singlesp` + gate tipométrico de objeto |
| fonte e nota de ilustração dentro dos limites do objeto | **INCOMPLETO** | upstream usa largura real; falta gate geométrico próprio para fonte/nota |
| indicação de fonte de elaboração própria | **CONFORME** | fixtures e gate verificam `Fonte:` |
| fonte externa de ilustração/tabela conforme NBR 10520 | **INCOMPLETO** | falta fixture com citação externa real |
| Lista de Ilustrações agregando figuras, gráficos e quadros | **CONFORME** | regressão verifica conteúdo e exclui tabelas |
| tabelas em lista própria | **CONFORME** | regressões exercitam lista de tabelas |
| apresentação tabular segundo IBGE | **INCOMPLETO** | `tabularray-abnt` existe; falta fechar subconjunto mínimo verificável do projeto |
| equações numeradas e referência resolvida | **CONFORME** | fixture normativa específica |
| número da equação alinhado à direita da mancha gráfica | **CONFORME NO ESCOPO TESTADO** | `tests/v2-math-check.sh` mede coordenada no PDF real |
| tipografia de código com `listings` | **CONFORME NO ESCOPO TESTADO** | default `\ttfamily\normalsize`; `ttfamily` é remapeada à família institucional; gate próprio |
| tipografia de código com `minted` | **CONFORME NO ESCOPO TESTADO** | default `fontfamily=tt, fontsize=\normalsize`; gate consulta a fonte renderizada na página de código via `pdffonts` |
| tipografia de algoritmos | **CONFORME NO ESCOPO TESTADO** | `ufcalgoritmo` usa tamanho normal e a família textual institucional; gate próprio |
| tipografia matemática | **CONFORME NO ESCOPO TESTADO** | matemática é complementar: NewTX Math no pdfLaTeX e TeX Gyre Termes Math no LuaLaTeX; não é declarada como Times/Arial textual |
| estrutura de projetos NBR 15287:2025 | **CONFORME NO ESCOPO TESTADO** | fixture cobre elementos exigidos no escopo do template |
| projeto anonimizado sem vazamento de autor/orientador | **CONFORME** | gate semântico específico |
| glossário, apêndice, anexo e índice | **CONFORME NO ESCOPO TESTADO** | ordem, presença, TOC e início no anverso verificados |
| ênfase tipográfica de títulos de apêndices/anexos igual à seção primária | **CONFORME** | `abntexto` reutiliza a política tipográfica da seção primária |
| agradecimento obrigatório à CAPES quando aplicável | **INCOMPLETO** | requisito depende do financiamento; template deve orientar o autor, não inferir a condição |
| lombada NBR 12225:2023 | **NÃO APLICÁVEL à distribuição eletrônica corrente** | extensão condicional futura |
| PDF/A para depósito | **CONFORME** | `\DocumentMetadata` + validação independente com veraPDF |
| PDF/A-2b | **CONFORME COMO ESCOLHA TÉCNICA DO PROJETO** | subtipo técnico do projeto, não imposição atribuída à UFC |

## Gate N — encerrado

A auditoria normativa de 2026 está **fechada em 20/08/2026**. Não há requisito crítico sem origem normativa ou decisão explícita.

O fechamento do Gate N não significa que a implementação esteja integralmente certificada. Significa que divergências e lacunas foram identificadas e encaminhadas à Fase 2.

## Fase 2 — Tipografia e fontes

### Implementado

1. módulo `ufctex/fontes.def` separado de `layout.def`;
2. API pública `fonte=times|arial`;
3. API pública `fonte-estrita=sim|nao`;
4. política explícita de fallback sem declarar substituto como Times New Roman/Arial;
5. unificação de `rmfamily`, `sffamily` e `ttfamily` na família institucional selecionada;
6. política de código `listings` e `minted` em tamanho 12 por padrão;
7. política de algoritmos em tamanho 12 por padrão;
8. política matemática complementar explícita;
9. título de objeto limitado à largura física da ilustração;
10. gates tipográficos específicos para seleção de fonte, código, `minted`, algoritmos e matemática;
11. POC Windows para fontes Microsoft literais, mantida inicialmente fora do gate obrigatório.

### Pendente para o Gate T

1. fechar a evidência Windows de Times New Roman/Arial literais nos dois motores;
2. fechar identidade das quatro variantes das famílias literais;
3. completar tamanhos reduzidos de todas as exceções;
4. medir geometricamente fonte e nota de ilustrações;
5. adicionar fonte externa de objeto com citação conforme NBR 10520;
6. adicionar referência bibliográfica própria real em anexo;
7. fechar subconjunto tabular IBGE;
8. orientar agradecimento CAPES quando aplicável;
9. executar regressão completa dos 12 PDFs;
10. executar PDF/A/veraPDF;
11. validar ambiente Overleaf;
12. tornar os gates tipográficos obrigatórios somente após a infraestrutura estar comprovada.

## Requisitos institucionais UFC

### Tipografia

O Guia UFC de Trabalhos Acadêmicos atualmente vinculado exige **Arial ou Times New Roman, tamanho 12**, inclusive na capa. Prevê tamanho menor e uniforme para citações longas, notas de rodapé, paginação, ficha catalográfica, legendas e fontes de ilustrações e tabelas, recomendando tamanho 10 para essas exceções.

A V2 distingue a fonte literal de substitutos de compatibilidade. `NewTX`, `TeX Gyre Termes` e `TeX Gyre Heros` não são declarados como Times New Roman ou Arial.

`fonte-estrita=sim` é a rota de certificação tipográfica: se a família literal solicitada não estiver disponível, a compilação deve falhar. `fonte-estrita=nao` existe para portabilidade e desenvolvimento, mas um PDF produzido com fallback não deve ser apresentado como tipograficamente conforme à exigência UFC de família literal.

Não foi localizada exceção institucional de família para código. Por isso, `listings`, `minted`, URLs e demais usos de `ttfamily` permanecem dentro da família institucional selecionada. Matemática é tratada separadamente por exigir repertório tipográfico próprio.

### Matemática

A família matemática é complementar à família textual. A V2 usa NewTX Math no pdfLaTeX e TeX Gyre Termes Math no LuaLaTeX. Essa família complementar não é descrita como “Times New Roman matemática” ou “Arial matemática”.

Equações numeradas usam algarismos arábicos entre parênteses e o gate geométrico verifica o alinhamento à direita da mancha gráfica.

### PDF/A

As orientações de recebimento consultadas em 2026 exigem arquivo eletrônico **PDF/A** para TCC, dissertações e teses destinados ao repositório.

A V2 usa **PDF/A-2b** como perfil técnico verificável. O subtipo 2b é escolha de implementação do projeto, não requisito específico atribuído à UFC.

### Folha de aprovação

A versão destinada ao repositório deve apresentar a folha de aprovação sem assinaturas. A V2 produz identificação e linhas da banca, mas não incorpora assinaturas digitalizadas.

### Ficha catalográfica

A Instrução Normativa Conjunta nº 2/2026 torna facultativa a representação visual da ficha catalográfica para TCC, dissertações e teses. Por isso, `ficha-catalografica=nao` permanece o padrão.

Quando a ficha for incluída, o verso com dados catalográficos não é contado nem numerado. A implementação restaura o contador lógico e preserva a paridade física também no modo `frente-verso`.

Como a ficha é um PDF externo, sua inclusão exige nova validação PDF/A do arquivo completo.

### Trabalhos em mais de um volume

A identificação do volume aparece quando o trabalho é dividido em mais de um volume, e a paginação permanece única e sequencial. A V2 oferece `volume` e `pagina-inicial`, com regressão própria.

### Frente e verso

No modo `frente-verso`:

- anverso: esquerda/superior 3 cm; direita/inferior 2 cm;
- verso: direita/superior 3 cm; esquerda/inferior 2 cm;
- numeração à direita no anverso e à esquerda no verso;
- elementos pré-textuais, exceto a página destinada aos dados catalográficos, iniciam no anverso;
- seções textuais primárias e elementos pós-textuais controlados pela V2 iniciam no anverso.

### Paginação

Os elementos pré-textuais são contados a partir da folha de rosto e não são numerados. O verso destinado aos dados catalográficos não é contado nem numerado. A numeração aparece a partir da primeira página textual. Apêndices, anexos e volumes mantêm sequência contínua.

### Espaçamento

O Guia UFC orienta espaço 1,5 no corpo e espaço simples nas exceções institucionais. Não deve existir espaço adicional entre parágrafos. Referências consecutivas são separadas por uma linha simples em branco.

### Ilustrações e tabelas

A NBR 14724:2024 determina que identificação, título, fonte, legenda e notas acompanhem os limites da própria ilustração. A fonte consultada deve seguir a NBR 10520; quando o objeto for do próprio autor, deve haver indicação equivalente a “Elaboração própria”.

A V2 já limita o título à largura física real do objeto e aplica tamanho reduzido. A medição geométrica de fonte e nota permanece pendente para o Gate T.

A Lista de Ilustrações agrega figuras, gráficos e quadros na ordem de ocorrência. Tabelas permanecem em lista própria.

### Citações e referências

O Guia UFC de Citações de 2025 foi elaborado conforme a NBR 10520:2023. Citações diretas longas usam parágrafo distinto, letra menor, espaço simples, sem aspas e recuo de 4 cm, com separação do texto anterior/posterior.

Para referências, prevalece a NBR 6023:2025. Referências usam espaço simples internamente e uma linha simples de separação. Referências próprias de anexo devem permanecer no próprio anexo, em nota ou lista específica; o caso bibliográfico real ainda será incluído no Gate T.

### Projetos de pesquisa

Para `projeto` e `projetoanonimizado`, a V2 adota NBR 15287:2025 e preserva somente requisitos UFC compatíveis com a edição vigente.

## Mapa de implementação

| Parte | Norma/requisito principal | Implementação |
|---|---|---|
| configuração e perfis | política UFC + normas por tipo | `ufctex/core.def` |
| tipografia textual e matemática | NBR 14724:2024 + requisito UFC Arial/Times New Roman | `ufctex/fontes.def` |
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
| figuras, gráficos e quadros | NBR 14724:2024 + UFC | `ufctex/objetos.def` + infraestrutura `place` |
| tabelas numéricas | NBR 14724:2024 + IBGE | `ufctex/objetos.def` + `tabularray-abnt` |
| código e algoritmos | requisito tipográfico UFC + extensão editorial | `ufctex/modulos.def` + `ufctex/objetos.def` |
| equações | NBR 14724:2024 | ambiente matemático + `tests/v2-math-check.sh` |
| citações | NBR 10520:2023 | `ufctex/bibliografia.def` + `abntexto` |
| referências | NBR 6023:2025 | `ufctex/bibliografia.def` + `ufctex/compat-nbr6023-2025.def` |
| projetos | NBR 15287:2025 | `ufctex/projetos.def` |
| glossário | NBR 14724:2024 | módulo opcional |
| apêndices e anexos | NBR 14724:2024 | API pública do `abntexto` + política V2 de quebra |
| índice | NBR 6034:2004 | módulo opcional |
| PDF/A | política institucional UFC | `\DocumentMetadata` + veraPDF |
| compatibilidade V1 | transição de documentos | `ufctex/compat-v1.def` |

## Compatibilidade dos pacotes

`abntexto`, `biblatex-abnt`, `tabularray-abnt` e demais pacotes são infraestrutura. A versão de um pacote não define, isoladamente, conformidade normativa da V2.

Os ajustes necessários para NBR 6023:2025 permanecem isolados em `ufctex/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível de forma estável no upstream.

## Build e gates

`make preflight` executa consistência da distribuição, documento de referência, layout, política de fontes, geometria, matemática/equações, pré-textuais, duplex, ficha catalográfica, multivolume, estruturas normativas complementares, objetos, código/algoritmos, `minted`, bibliografia, projetos, matriz de seis perfis nos dois motores, pós-textuais, compatibilidade V1 e fluxo modular do Makefile.

A matriz final produz **12 PDFs**: seis perfis × dois motores. Cada PDF é verificado quanto a conteúdo específico, A4, fontes incorporadas, Sumário, ausência de `chapter`, warnings/overflow reconhecidos e declaração PDF/A-2b.

`make release-preflight` acrescenta veraPDF para o documento de referência e os 12 PDFs da matriz.

Para o Gate T ainda faltam evidências finais de:

- fontes literais e quatro variantes no Windows;
- tamanhos reduzidos restantes;
- fonte/nota de objetos por geometria;
- fonte externa conforme NBR 10520;
- referência bibliográfica específica de anexo;
- subconjunto tabular IBGE;
- regressão integral dos 12 PDFs e PDF/A;
- ambiente Overleaf.

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

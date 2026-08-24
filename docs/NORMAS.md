# Base normativa da V2

Última auditoria normativa: **2026-08-23**.  
Estado da linha 2.2.0: **certificação de distribuição em andamento; verificação normativa N1 em progresso**.

Este documento é a referência humana do projeto para política normativa, precedência e vínculo entre requisito, implementação e teste. O catálogo atômico e a cobertura executável ficam em `normativa/` e nos checks de `tests/checks/`.

## Política normativa

A V2 adota a edição vigente mais recente de cada norma aplicável. Quando um guia institucional ainda cita edição substituída, a decisão segue esta ordem:

1. legislação, regulamento, instrução normativa ou resolução institucional aplicável;
2. edição vigente da norma ABNT;
3. requisito institucional específico da UFC compatível com a norma vigente;
4. Guia de Normalização da UFC mais recente aplicável;
5. comportamento de `abntexto` e demais pacotes.

O comportamento de um pacote nunca prevalece sobre requisito normativo ou institucional aplicável. Datas de PDFs institucionais não são tratadas, isoladamente, como prova de vigência de uma norma técnica.

## Base reconfirmada

| Assunto | Referência adotada | Escopo principal |
|---|---|---|
| Trabalhos acadêmicos | **ABNT NBR 14724:2024**, versão corrigida de 01/04/2025 | estrutura, apresentação, paginação e elementos documentais |
| Citações | **ABNT NBR 10520:2023** | citações diretas, indiretas e sistema autor-data |
| Referências | **ABNT NBR 6023:2025** | elaboração e apresentação das referências |
| Projetos de pesquisa | **ABNT NBR 15287:2025** | perfis `projeto` e `projetoanonimizado` |
| Resumos | **ABNT NBR 6028:2021** | resumo, abstract e palavras-chave |
| Numeração progressiva | **ABNT NBR 6024:2012** | seções e subdivisões |
| Sumário | **ABNT NBR 6027:2012** | composição e hierarquia do Sumário |
| Índice | **ABNT NBR 6034:2004** | índice remissivo opcional |
| Lombada | **ABNT NBR 12225:2023** | requisito condicional |
| Tabelas numéricas | **IBGE, Normas de Apresentação Tabular, 3. ed., 1993** | estrutura de tabelas numéricas |
| Ficha catalográfica | **IN Conjunta UFC nº 2/2026** | representação visual facultativa no depósito |
| Agradecimento CAPES | **Portaria CAPES nº 206/2018** | requisito condicional ao financiamento CAPES |

As edições são reconfirmadas antes de cada versão principal. O inventário de fontes, datas de consulta e precedência está em `normativa/source-audit.json`.

## Auditoria institucional UFC

A página de Normalização de Trabalhos Acadêmicos do Sistema de Bibliotecas da UFC foi revisada em 2026 e declara alinhamento às normas ABNT vigentes. Guias institucionais históricos continuam úteis para requisitos específicos da UFC, mas referências internas a edições ABNT superadas não substituem a edição vigente.

A Instrução Normativa Conjunta nº 2/2026/SIBI/PROGRAD/PRPPG torna facultativa a representação visual da ficha catalográfica para TCC, dissertação e tese depositados no Repositório Institucional.

Para depósito, o projeto considera os requisitos institucionais vigentes de PDF/A, abrangência do arquivo da capa aos anexos e folha de aprovação sem assinaturas digitalizadas. A classe não presume se o trabalho recebeu financiamento CAPES; quando aplicável, o autor deve incluir o agradecimento exigido pela Portaria CAPES nº 206/2018.

## Estados de conformidade

- **CONFORME**: requisito implementado e sustentado por evidência/teste compatível;
- **CONFORME NO ESCOPO TESTADO**: requisito amplo cuja parcela exercitada possui evidência suficiente;
- **DIVERGENTE**: implementação atual contraria requisito vigente;
- **INCOMPLETO**: regra conhecida, mas falta decisão, cobertura ou evidência necessária;
- **NÃO APLICÁVEL**: requisito condicional fora do escopo da distribuição corrente.

Fallback de compatibilidade tipográfica não torna um PDF estritamente conforme. Para a família textual, a certificação final estrita exige **Times New Roman ou Arial literais** no PDF produzido.

O PDF final também deve ser autocontido para renderização: todas as fontes efetivamente usadas devem estar incorporadas. Incorporação por subconjunto é aceita.

## Matriz requisito → implementação → teste

| Requisito | Estado | Implementação / evidência |
|---|---|---|
| papel A4 | **CONFORME** | `abntexto-ufc/layout.def`; `tests/v2-pdf-geometry-check.sh` |
| margens anverso 3 cm esquerda/superior e 2 cm direita/inferior | **CONFORME** | `abntexto-ufc/layout.def`; gate geométrico |
| margens espelhadas em frente-verso | **CONFORME** | `abntexto-ufc/layout.def`; regressões duplex |
| corpo textual em tamanho 12 | **CONFORME** | classe carregada em 12 pt; gates tipográficos |
| seleção pública `fonte=times|arial` | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/fontes.def`; font-config |
| política `fonte-estrita=sim|nao` | **CONFORME NO ESCOPO TESTADO** | modo estrito falha sem fonte literal; fallback é declarado |
| Times New Roman/Arial literais no PDF estrito | **CONFORME NO ESCOPO TESTADO** | Gate T Windows em pdfLaTeX/LuaLaTeX |
| variantes regular/negrito/itálico/negrito-itálico | **CONFORME NO ESCOPO TESTADO** | certificação Windows nos dois motores |
| todas as fontes incorporadas | **CONFORME NO ESCOPO TESTADO** | `tests/v2-font-embedding-check.sh`, perfis e Gate T |
| recuo de primeira linha em 2 cm | **CONFORME** | `abntexto-ufc/layout.def`; layout check |
| sem espaço adicional entre parágrafos | **CONFORME** | `\parskip=0pt`; layout check |
| espaçamento 1,5 no corpo | **CONFORME** | política da classe |
| exceções em espaço simples/tamanho reduzido | **CONFORME NO ESCOPO TESTADO** | citações longas, notas, paginação, objetos e tabelas exercitados |
| capa e folha de rosto | **CONFORME** | `abntexto-ufc/pretextuais.def`, `abntexto-ufc/trabalhos.def` |
| volume e paginação contínua | **CONFORME** | `abntexto-ufc/trabalhos.def`; multivolume check |
| ficha catalográfica visual facultativa | **CONFORME** | política padrão `nao`; regressão dedicada |
| folha de aprovação sem assinaturas digitalizadas | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/pretextuais.def`; validador mantém inspeção visual quando necessário |
| dedicatória, agradecimentos, epígrafe e errata | **CONFORME NO ESCOPO TESTADO** | pré-textuais + fixtures |
| resumo/abstract e palavras-chave | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/pretextuais.def`; corpus de referência |
| listas e Sumário | **CONFORME** | pré-textuais + regressão de líderes pontilhados |
| seções e subdivisões | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/layout.def`; NBR 6024 |
| figuras, gráficos e quadros | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/objetos.def`; geometria de objetos |
| tabelas numéricas | **CONFORME NO ESCOPO TESTADO** | modo nativo e `tabularray-abnt`; gate IBGE |
| código e algoritmos | **CONFORME NO ESCOPO TESTADO** | módulos opcionais + gate geométrico/tipográfico |
| equações | **CONFORME NO ESCOPO TESTADO** | ambiente matemático + math check |
| citações | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/bibliografia.def`; NBR 10520:2023 |
| referências | **CONFORME NO ESCOPO TESTADO** | `biblatex-abnt` + `compat-nbr6023-2025.def`; NBR 6023:2025 |
| projetos | **CONFORME NO ESCOPO TESTADO** | `abntexto-ufc/projetos.def`; NBR 15287:2025 |
| glossário | **CONFORME NO ESCOPO TESTADO** | módulo opcional |
| apêndices e anexos | **CONFORME NO ESCOPO TESTADO** | API pública do `abntexto` + política V2 de quebra |
| índice | **CONFORME NO ESCOPO TESTADO** | módulo opcional; NBR 6034:2004 |
| PDF/A e fontes autocontidas | **CONFORME NO ESCOPO TESTADO** | `\DocumentMetadata`, veraPDF, font embedding gates |

A cobertura detalhada e atômica não é duplicada manualmente aqui. Ela é mantida em `normativa/catalog.json`, `normativa/atomic-rules.json`, `normativa/coverage-audit.json` e verificada por `tests/checks/normative_*`.

## Tipografia

A API pública oferece `fonte=times` e `fonte=arial`. A política de identidade é controlada por `fonte-estrita`:

- `sim`: exige a família literal e reprova ausência;
- `nao`: admite fallback explicitamente identificado para portabilidade/desenvolvimento.

Fallbacks portáteis:

- pdfLaTeX + Times: NewTX;
- pdfLaTeX + Arial: TeX Gyre Heros;
- LuaLaTeX/XeLaTeX + Times: TeX Gyre Termes;
- LuaLaTeX/XeLaTeX + Arial: TeX Gyre Heros.

O Gate T Windows certifica Times New Roman e Arial literais, suas variantes, extração Unicode, incorporação e PDF/A-2b. As fontes Microsoft não são redistribuídas.

## Objetos acadêmicos

Figuras, gráficos, quadros, códigos e algoritmos usam a infraestrutura de objetos da V2. Título, Fonte e Nota são vinculados à largura física do objeto. A numeração de códigos/algoritmos permanece dentro da mancha gráfica. A Lista de Ilustrações agrega figuras, gráficos e quadros na ordem de ocorrência; tabelas permanecem em lista própria.

Para tabelas numéricas, o módulo `tabularray` requer `tabularray-abnt` datado de **2025-08-08 ou mais recente**. A alternância de linhas é uma extensão editorial opcional e não uma regra normativa automática.

## Citações e referências

O projeto aplica NBR 10520:2023 para citações. Citações diretas longas usam parágrafo distinto, letra menor, espaço simples, sem aspas e recuo institucional exercitado de 4 cm.

Para referências, prevalece a NBR 6023:2025. Ajustes necessários ao escopo testado ficam isolados em `abntexto-ufc/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível de forma estável no upstream.

## Projetos de pesquisa

Os perfis `projeto` e `projetoanonimizado` adotam NBR 15287:2025 e preservam apenas requisitos UFC compatíveis com a edição vigente. O perfil anonimizado remove dados pessoais usados na seleção sem criar uma norma institucional inexistente.

## Compatibilidade dos pacotes

`abntexto`, `biblatex-abnt`, `tabularray-abnt` e demais pacotes são infraestrutura. A versão de um pacote não define, isoladamente, conformidade normativa.

A V2 exige `abntexto` 1.1 ou superior. Para os perfis portáteis de fonte, pdfLaTeX usa NewTX/TeX Gyre e motores Unicode usam `fontspec`, `unicode-math` e famílias TeX Gyre compatíveis. Módulos opcionais são carregados somente quando ativados.

## Build e gates

`make preflight` executa a validação coordenada por `tests/run.py --mode pr`, incluindo auditoria do repositório, documento de referência, layout, fontes, geometria, matemática, pré-textuais, duplex, objetos, tabelas, código/algoritmos, bibliografia, projetos, matriz de perfis, pós-textuais, multivolume e ficha catalográfica.

`make release-preflight` usa `tests/run.py --mode release` e acrescenta certificações profundas de PDF/A. O Gate T combina Linux, proxy Overleaf e certificação Windows de fontes literais. `make distribution-preflight` ainda reconstrói e valida deterministicamente todos os bundles, inclusive compilação direta a partir do candidato CTAN extraído.

## Fontes institucionais e normativas de verificação

- Sistema de Bibliotecas da UFC — Normalização de trabalhos acadêmicos: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Guia de Normalização de Trabalhos Acadêmicos: https://biblioteca.ufc.br/wp-content/uploads/2022/05/guianormalizacaotrabalhosacademicos-17.05.2022.pdf
- Guia de Normalização para Elaboração de Citações 2025: https://biblioteca.ufc.br/wp-content/uploads/2025/06/guianormalizacaocitacoes2025.pdf
- Sistema de Bibliotecas da UFC — normas para recebimento de teses e dissertações: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-teses-e-dissertacoes/
- Sistema de Bibliotecas da UFC — normas para recebimento de TCC: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-tcc/
- Instrução Normativa Conjunta nº 2/2026: https://biblioteca.ufc.br/wp-content/uploads/2026/02/instrucao-normativa-conjunta-2.pdf
- Sistema de Bibliotecas da UFC — ficha catalográfica: https://biblioteca.ufc.br/pt/perguntas-frequentes/ficha-catalografica-2/
- Sistema de Bibliotecas da UFC — coleção de normas técnicas: https://biblioteca.ufc.br/pt/colecao-de-normas-tecnicas/
- CAPES — Portaria nº 206/2018: https://www.gov.br/capes/pt-br/centrais-de-conteudo/portaria-no-206-de-4-de-setembro-de-2018.pdf
- Catálogo ABNT: https://www.abntcatalogo.com.br/

## Manutenção

Antes de nova versão principal:

1. reconfirmar as edições normativas;
2. revisar atos, páginas e guias da UFC;
3. revisar políticas de depósito, ficha catalográfica e CAPES;
4. revisar dependências e remover adaptações upstream que deixaram de ser necessárias;
5. executar os contratos normativos e resolver divergências classificadas;
6. executar `make preflight` e `make release-preflight`;
7. confirmar Gate T, Overleaf, Windows e `distribution-preflight` no mesmo SHA;
8. não declarar conformidade sem evidência compatível.

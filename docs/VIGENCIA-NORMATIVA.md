# Política de vigência normativa

Última revisão: **2026-08-28**.

## Regra mandatória

O `abntexto-ufc` deve seguir a **edição vigente mais recente da norma técnica aplicável**. Uma edição ABNT substituída não pode governar uma regra ativa apenas porque ainda aparece citada em um Guia de Normalização da UFC.

A base institucional é:

1. **Resolução nº 17/CEPE, de 02 de outubro de 2017** — normalização dos trabalhos acadêmicos da UFC segundo normas técnicas de informação/documentação da ABNT ou modelo específico aprovado no rito institucional;
2. página vigente de Normalização de Trabalhos Acadêmicos do Sistema de Bibliotecas da UFC — os cinco guias institucionais devem ser lidos à luz das normas vigentes;
3. para stricto sensu, **Resolução nº 17/CEPE, de 04 de dezembro de 2015** — o colegiado do PPG pode definir diretrizes de apresentação dentro de seu escopo, desde que a diretriz específica seja identificada e vigente.

## Regra de decisão

Para requisito técnico:

**norma ABNT vigente → requisito UFC compatível/complementar → guia UFC → implementação**.

Para requisito institucional:

**ato UFC vigente → requisito institucional UFC vigente → guia UFC → norma técnica, quando aplicável → implementação**.

Um guia UFC que cite edição técnica antiga pode continuar fornecendo orientação institucional compatível, mas **não reativa** a edição ABNT substituída. Conflito real entre fontes atuais recebe `review-required`; o projeto não escolhe silenciosamente uma delas.

## Fontes institucionais principais

- Resolução nº 17/CEPE, de 02 de outubro de 2017;
- Resolução nº 17/CEPE, de 04 de dezembro de 2015;
- página de Normalização do SiBi/UFC;
- guias oficiais do SiBi/UFC;
- atos de depósito e instruções normativas vigentes cadastrados em `normativa/source-audit.json`.

O inventário completo, datas de consulta, status, precedência e exclusões ficam nos arquivos máquina-legíveis em `normativa/`.

## Artigo científico — estado corrente após N15-B2A

A fonte institucional ativa é:

- ID: `ufc-guia-artigos-2022`;
- título: Guia de normalização de artigo em publicação periódica da Universidade Federal do Ceará;
- edição bibliográfica: **2022**;
- arquivo corrigido atualmente publicado pelo SiBi/UFC: **27/04/2023**;
- papel: `institutional-guide`, não autoridade técnica ABNT.

A identidade anterior `ufc-guia-artigos-2021` é mantida somente como fonte revisada e superseded history, com `replaced_by = ufc-guia-artigos-2022`.

A norma técnica ativa do contrato de artigo é **ABNT NBR 6022:2018**.

N15-B2A/PR #145 já promoveu esse conjunto para catálogo/precedência e adicionou **13 predicados `article.*`** com locators e metadados de fase. Portanto, a formulação antiga de que guia/6022 estavam fora do catálogo ou de que a promoção dos predicados ainda era futura está revogada.

O que **ainda não existe** é o runtime LaTeX específico de artigo. Não há perfil público final de artigo em produção nem módulo `articles.def` carregado pela classe. Essa implementação pertence a **N15-B2B**, depois da normalização da API pública em B2R-B. O fechamento de evidência pertence a **N15-B2C**.

### Recomendações não promovidas a obrigação

No guia corrente, linguagem como `convém`, `recomenda-se` e `sugerimos` permanece recomendação. Em particular, não são hard requirements automáticos do contrato:

- resumo com 150–250 palavras;
- mínimo de três palavras-chave;
- uso de Arial ou Times apenas porque o guia recomenda essas famílias;
- alinhamento à direita da autoria quando apresentado como sugestão.

O contrato diferencia requisito obrigatório, recomendação e boundary manual/condicional.

### Fronteira com periódicos

O próprio guia UFC informa que suas orientações são requisitos mínimos e que as instruções específicas do periódico de destino devem ser consultadas antes da submissão. O futuro perfil de artigo do template será uma baseline UFC; não poderá afirmar que substitui as author guidelines de um periódico.

## Mapeamentos explícitos de supersessão técnica

Os pares abaixo são mantidos com a grafia completa exigida pelo contrato de vigência. As referências antigas aparecem aqui apenas como contexto explicativo; não governam a base técnica ativa.

- **ABNT NBR 14724:2011** → **ABNT NBR 14724:2024**;
- **ABNT NBR 6023:2018** → **ABNT NBR 6023:2025**;
- **ABNT NBR 10520:2002** → **ABNT NBR 10520:2023**;
- **ABNT NBR 12225:2004** → **ABNT NBR 12225:2023**;
- **ABNT NBR 15287:2011** → **ABNT NBR 15287:2025**.

## Mapeamento por guia UFC

| Documento institucional | Edição antiga citada | Edição técnica ativa/reconciliada | Decisão |
| --- | --- | --- | --- |
| Guia de Trabalhos Acadêmicos 2022 | ABNT NBR 14724:2011 | **ABNT NBR 14724:2024**, corrigida em 01/04/2025 | usar edição vigente |
| Guia de Trabalhos Acadêmicos 2022 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usar edição vigente |
| Guia de Trabalhos Acadêmicos 2022 | ABNT NBR 10520:2002 | **ABNT NBR 10520:2023** | usar edição vigente |
| Guia de Trabalhos Acadêmicos 2022 | ABNT NBR 12225:2004 | **ABNT NBR 12225:2023** | usar edição vigente |
| Guia de Artigo 2022/correção 2023 | ABNT NBR 10520:2002 | **ABNT NBR 10520:2023** | usar edição vigente |
| Guia de Artigo 2022/correção 2023 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usar edição vigente |
| Guia de Artigo 2022/correção 2023 | ABNT NBR 6022:2018 | **ABNT NBR 6022:2018** | edição corrente identificada |
| Guia de Citações 2025 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | atualizar somente a referência a 6023 |
| Guia de Referências 2023 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usar edição vigente |
| Guia de Projetos de Pesquisa 2019 | ABNT NBR 15287:2011 | **ABNT NBR 15287:2025** | usar edição vigente |
| Guia de Projetos de Pesquisa 2019 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usar edição vigente |
| Guia de Projetos de Pesquisa 2019 | ABNT NBR 10520:2002 | **ABNT NBR 10520:2023** | usar edição vigente |
| Guia de Projetos de Pesquisa 2019 | ABNT NBR 12225:2004 | **ABNT NBR 12225:2023** | usar edição vigente |

Normas antigas em ano podem continuar ativas se não houver substituição; o critério é vigência, não recência numérica.

## Base técnica corrente do contrato

| Assunto | Referência |
| --- | --- |
| Trabalhos acadêmicos | ABNT NBR 14724:2024, versão corrigida em 01/04/2025 |
| Artigos em publicação periódica | ABNT NBR 6022:2018 |
| Citações | ABNT NBR 10520:2023 |
| Referências | ABNT NBR 6023:2025 |
| Projetos de pesquisa | ABNT NBR 15287:2025 |
| Resumo, resenha e recensão | ABNT NBR 6028:2021 |
| Numeração progressiva | ABNT NBR 6024:2012 |
| Sumário | ABNT NBR 6027:2012 |
| Índice | ABNT NBR 6034:2004 |
| Lombada | ABNT NBR 12225:2023 |
| Tabelas numéricas | Normas de Apresentação Tabular do IBGE, 3. ed., 1993, quando aplicável |

`ABNT NBR 6022:2018` já pertence ao contrato normativo ativo; isso não significa que o runtime de artigo esteja implementado.

## Fontes revisadas e excluídas/contextuais

O projeto não concede autoridade técnica por mera presença em páginas institucionais. Exemplos já reconciliados:

- Portaria MEC nº 1.224/2013 — revogada; mantida apenas como reviewed/excluded history;
- Portaria CAPES nº 59/2017 — contextual para avaliação de programas, `technical_authority=false`;
- Resolução nº 17/CEPE, de 04 de dezembro de 2015 — autoridade institucional de governança de PPG, mas não licença genérica para inventar regras de apresentação.

## Atualização futura de norma

Quando nova edição técnica for identificada:

1. a fonte entra em revisão; não muda valores automaticamente;
2. os requisitos afetados são comparados com a nova edição;
3. regras alteradas recebem atualização explícita de fonte/predicate/locator/evidence;
4. a edição substituída sai da base técnica ativa;
5. divergências com guias UFC são registradas nesta política e nos ledgers máquina-legíveis;
6. runtime, testes, CLI/Web e documentação devem convergir antes da fase ser fechada.

## Documentação e continuidade

Esta política deve permanecer sincronizada com `normativa/version-policy.json`, `normativa/source-audit.json`, `normativa/catalog.json`, `normativa/precedence.json` e o estado descrito em `docs/HANDOFF-V2.2.0.md`.

Desatualização documental é bloqueante para fechamento de fase. Mudanças materiais em autoridade, vigência, promoção de fontes/predicados ou status de runtime devem atualizar esta documentação no mesmo ciclo de trabalho.

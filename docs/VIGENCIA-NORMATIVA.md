# Política de vigência normativa

Última revisão: **2026-08-28**.

## Regra mandatória

O abntexto-ufc deve seguir a **edição vigente mais recente da norma técnica aplicável**. Uma edição ABNT substituída não pode governar uma regra ativa apenas porque ainda aparece citada em um Guia de Normalização da UFC.

Esta decisão não é uma preferência editorial do projeto. Ela decorre da base institucional da própria UFC:

1. a **Resolução nº 17/CEPE, de 02 de outubro de 2017**, cujo art. 1º determina que a normalização dos trabalhos acadêmicos da UFC seja realizada de acordo com as normas técnicas de informação e documentação da ABNT ou por modelo específico aprovado no rito previsto pela própria resolução;
2. a página vigente **Normalização de trabalhos acadêmicos — Sistema de Bibliotecas UFC**, atualizada em 04/03/2026, que declara que os cinco Guias de Normalização da UFC estão de acordo com as **normas vigentes** da ABNT;
3. para a pós-graduação stricto sensu, a **Resolução nº 17/CEPE, de 04 de dezembro de 2015**, em vigor, atribui ao colegiado do programa, nas Normas Gerais art. 10, X, competência para definir diretrizes referentes à forma de apresentação de dissertação, tese ou trabalho equivalente.

Fontes institucionais:

- Resolução nº 17/CEPE, de 02/10/2017: https://ufc.br/images/_files/a_universidade/cepe/resolucao_cepe_2017/resolucao17_cepe_2017.pdf
- Resolução nº 17/CEPE, de 04/12/2015: https://normadigital.ufc.br/cepe/resolucao-no-17-cepe-de-04-de-dezembro-de-2015-2/
- Página de Normalização do SiBi/UFC: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Relação oficial das Resoluções CEPE de 2017: https://www.ufc.br/a-universidade/documentos-oficiais/9285-resolucoes-do-conselho-de-ensino-pesquisa-e-extensao-cepe-2017

## Regra de decisão

Para requisito técnico:

**norma ABNT vigente → requisito UFC compatível/complementar → guia UFC → implementação**.

Para requisito institucional:

**ato UFC vigente → requisito institucional UFC vigente → guia UFC → norma técnica, quando aplicável → implementação**.

Um guia UFC que contenha uma citação técnica antiga continua podendo fornecer orientação institucional compatível, mas **não reativa** a edição ABNT substituída.

Se duas fontes atuais e aplicáveis forem realmente incompatíveis, o requisito recebe `review-required`; o projeto não escolhe silenciosamente uma delas.

### Relação entre CEPE 17/2015 e CEPE 17/2017

As duas resoluções não devem ser tratadas como concorrentes genéricas:

- a **CEPE 17/2017** estabelece o regime geral de normalização: ABNT ou modelo específico formalmente aprovado; o art. 1º, §§ 2º-3º, define o rito e o comportamento na ausência de modelo específico;
- a **CEPE 17/2015** estabelece a governança dos programas stricto sensu e dá ao colegiado do PPG competência para definir diretrizes de apresentação de dissertação, tese ou equivalente.

Portanto, um PPG pode introduzir uma exceção institucional de apresentação dentro de seu escopo, mas isso exige uma **diretriz específica identificada e vigente**. A mera existência da competência do colegiado não autoriza o template a inventar uma variante nem a afastar silenciosamente a base ABNT/UFC geral. Uma regra de PPG só pode ser consumida depois de cadastrada, localizada, reconciliada e testada.

## N15-B1 — perfil de artigo científico: fontes reconciliadas, runtime ainda congelado

A página vigente do SiBi/UFC lista **cinco** guias oficiais. O quinto, que faltava ao inventário anterior, é o **Guia de Normalização de Artigo em Publicação Periódica Científica**, edição UFC 2021.

Na seção de apresentação do guia, a UFC informa como base a **ABNT NBR 6022:2018** para artigos e também cita NBR 10520:2002, NBR 6023:2018, NBR 6024:2012, NBR 6028:2021 e as normas tabulares do IBGE. A revisão N15-B1 reconciliou essa lista com a política de vigência atual:

- **ABNT NBR 6022:2018** permanece a edição corrente identificada para apresentação de artigo em publicação periódica técnica e/ou científica. A revisão pública de 28/08/2026 cruzou o guia UFC vigente, a página institucional atual da UFC e registros universitários atuais de normas; não foi identificada edição posterior substitutiva;
- a citação **ABNT NBR 10520:2002** do guia é substituída, para qualquer regra futura, pela **ABNT NBR 10520:2023**;
- a citação **ABNT NBR 6023:2018** do guia é substituída pela **ABNT NBR 6023:2025**;
- NBR 6024:2012, NBR 6028:2021 e IBGE 1993 permanecem conforme seus escopos já reconciliados.

Essa reconciliação **não implementa o perfil de artigo**. Durante N15-B1, `ufc-guia-artigos-2021` e `abnt-nbr-6022-2018` permanecem fontes reconciliadas de perfil futuro, fora de `normativa/catalog.json` e `normativa/precedence.json`. A promoção para predicados `article.*`, runtime LaTeX, locators e evidências pertence exclusivamente à **N15-B2**.

O próprio guia UFC também estabelece uma fronteira de aplicabilidade importante: suas orientações são requisitos mínimos e, antes da submissão, devem ser consultadas as diretrizes do periódico de destino. O futuro perfil UFC não poderá afirmar que substitui instruções editoriais específicas do periódico.

## Mapeamento explícito de edições citadas pela UFC

As referências antigas abaixo são mantidas nesta documentação **apenas para explicar a divergência de vigência**. Elas não pertencem à base técnica ativa.

| Documento UFC | Edição ainda citada | Edição técnica adotada/reconciliada pelo abntexto-ufc | Decisão |
|---|---|---|---|
| Guia de Trabalhos Acadêmicos, 2022 | ABNT NBR 14724:2011 | **ABNT NBR 14724:2024** (versão corrigida em 01/04/2025) | usa a edição vigente |
| Guia de Trabalhos Acadêmicos, 2022 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usa a edição vigente |
| Guia de Trabalhos Acadêmicos, 2022 | ABNT NBR 10520:2002 | **ABNT NBR 10520:2023** | usa a edição vigente |
| Guia de Trabalhos Acadêmicos, 2022 | ABNT NBR 12225:2004 | **ABNT NBR 12225:2023** | usa a edição vigente |
| Guia de Artigo Científico, 2021 | ABNT NBR 10520:2002 | **ABNT NBR 10520:2023** | fonte reconciliada em N15-B1; runtime do artigo somente em N15-B2 |
| Guia de Artigo Científico, 2021 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | fonte reconciliada em N15-B1; runtime do artigo somente em N15-B2 |
| Guia de Citações, 2025 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | a NBR 10520:2023 do próprio guia continua vigente; somente a referência à 6023 foi substituída |
| Guia de Referências, 2023 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usa a edição vigente |
| Guia de Projetos de Pesquisa, 2019 | ABNT NBR 15287:2011 | **ABNT NBR 15287:2025** | usa a edição vigente |
| Guia de Projetos de Pesquisa, 2019 | ABNT NBR 6023:2018 | **ABNT NBR 6023:2025** | usa a edição vigente |
| Guia de Projetos de Pesquisa, 2019 | ABNT NBR 10520:2002 | **ABNT NBR 10520:2023** | usa a edição vigente |
| Guia de Projetos de Pesquisa, 2019 | ABNT NBR 12225:2004 | **ABNT NBR 12225:2023** | usa a edição vigente |

As normas que continuam atuais, mesmo que tenham ano antigo, permanecem ativas. O critério é **vigência**, não o número do ano.

## Outras referências encontradas na página de recebimento de teses e dissertações

A página vigente do SiBi/UFC também referencia atos que não podem receber autoridade de formatação por mera associação documental:

- **Portaria MEC nº 1.224/2013**: tratava de manutenção e guarda do acervo acadêmico. O próprio MEC informa que foi **revogada** pela Portaria Normativa nº 22/2017 e pela Portaria nº 315/2018. Por isso, ela é registrada apenas como fonte revisada e excluída; não integra o inventário ativo e não possui autoridade técnica sobre formatação;
- **Portaria CAPES nº 59/2017**: o catálogo oficial da CAPES a marca como vigente e sua ementa é o regulamento da Avaliação Quadrienal 2017. Seu escopo é avaliação de programas de pós-graduação, não apresentação técnica de dissertações/teses. Ela é classificada como regulação externa contextual, com `technical_authority=false`;
- **Resolução nº 17/CEPE, de 04/12/2015**: ao contrário das duas referências anteriores, possui efeito institucional direto sobre a governança da apresentação nos PPGs e, por isso, foi promovida ao inventário corrente com escopo explícito de autoridade de programa.

## Normas técnicas vigentes atualmente adotadas pelo runtime

| Assunto | Norma |
|---|---|
| Trabalhos acadêmicos | ABNT NBR 14724:2024, versão corrigida em 01/04/2025 |
| Citações | ABNT NBR 10520:2023 |
| Referências | ABNT NBR 6023:2025 |
| Projetos de pesquisa | ABNT NBR 15287:2025 |
| Resumo, resenha e recensão | ABNT NBR 6028:2021 |
| Numeração progressiva de seções | ABNT NBR 6024:2012 |
| Sumário | ABNT NBR 6027:2012 |
| Índice | ABNT NBR 6034:2004 |
| Lombada | ABNT NBR 12225:2023 |
| Tabelas numéricas | Normas de apresentação tabular do IBGE, 3. ed., 1993, quando aplicável |

Fonte reconciliada, **ainda não adotada pelo runtime em N15-B1**:

| Perfil futuro | Norma |
|---|---|
| Artigo em publicação periódica técnica e/ou científica | **ABNT NBR 6022:2018** — promoção prevista para N15-B2 junto com o contrato `article.*` |

## Como uma atualização futura é tratada

Quando uma nova edição técnica for identificada:

1. a nova edição não altera automaticamente valores no template;
2. a fonte é marcada para revisão;
3. os requisitos afetados são confrontados com a nova edição;
4. regras alteradas são atualizadas e retestadas;
5. a edição substituída é removida da base técnica ativa;
6. se um guia UFC ainda citar a edição antiga, a divergência é acrescentada a este mapa;
7. CI, CLI, Web e documentação devem convergir para a mesma decisão.

O arquivo máquina-legível correspondente é `normativa/version-policy.json`. O gate `tests/checks/normative_currency.py` impede que uma edição mapeada como substituída volte a governar arquivos normativos ativos e também impede que as fontes reconciliadas do perfil de artigo entrem no runtime antes da N15-B2.

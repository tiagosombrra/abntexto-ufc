# Base normativa da V2

Última auditoria: **2026-08-19**.

Este arquivo registra a base normativa usada pela V2 do modelo LaTeX da Universidade Federal do Ceará (UFC). Ele deve ser atualizado sempre que uma norma técnica ou regra institucional aplicável for revisada.

## Política normativa

A V2 adota a **edição vigente mais recente** de cada norma.

Quando um Guia de Normalização da UFC citar uma edição antiga de uma norma ABNT que já foi substituída, o modelo deve seguir a edição ABNT vigente. O guia antigo continua sendo usado para requisitos institucionais próprios da UFC que não conflitem com a norma atual.

Ordem de decisão:

1. legislação, regulamento ou resolução institucional aplicável;
2. edição vigente mais recente da norma ABNT;
3. requisito institucional específico da UFC compatível com a norma vigente;
4. Guia de Normalização da UFC mais recente aplicável ao assunto;
5. comportamento do `abntexto` e dos demais pacotes LaTeX.

O comportamento padrão de um pacote nunca prevalece sobre uma exigência normativa.

## Normas vigentes adotadas

| Assunto | Referência adotada | Uso principal na V2 |
|---|---|---|
| Trabalhos acadêmicos | **ABNT NBR 14724:2024**, versão corrigida de 01/04/2025 | estrutura, apresentação, página, elementos pré/textuais/pós-textuais, ilustrações |
| Citações | **ABNT NBR 10520:2023** | citações diretas, indiretas, autor-data, `apud`, localização |
| Referências | **ABNT NBR 6023:2025** | elaboração e apresentação das referências |
| Projetos de pesquisa | **ABNT NBR 15287:2025** | perfil `projeto` e base estrutural de `projetoanonimizado` |
| Resumos | **ABNT NBR 6028:2021** | resumo, abstract e palavras-chave |
| Numeração progressiva | **ABNT NBR 6024:2012** | seções, subseções, alíneas e subalíneas |
| Sumário | **ABNT NBR 6027:2012** | composição e hierarquia do Sumário |
| Índice | **ABNT NBR 6034:2004** | índice remissivo opcional |
| Lombada | **ABNT NBR 12225:2023** | suporte a lombada, quando aplicável |
| Tabelas numéricas | **IBGE, Normas de apresentação tabular, 3. ed., 1993** | estrutura de tabelas de dados numéricos |

A lista acima representa as edições verificadas na data da auditoria. Antes de uma nova versão principal do template, as edições devem ser conferidas novamente na coleção Target GEDWeb disponibilizada pela UFC.

## Requisitos institucionais UFC

A UFC determina que os trabalhos sejam apresentados de acordo com as normas de documentação e informação da ABNT e mantém Guias de Normalização institucionais. Esses guias são usados para particularidades da Universidade, como composição institucional dos elementos pré-textuais e procedimentos de entrega.

Quando um guia institucional ainda citar uma edição ABNT revogada, a referência normativa da V2 é atualizada sem preservar a regra obsoleta.

Exemplos atuais:

- o Guia geral UFC de 2022 ainda foi produzido sob a NBR 14724:2011; a V2 usa a **NBR 14724:2024, versão corrigida em 2025**;
- o Guia de Referências UFC disponível foi elaborado com base na NBR 6023:2018; a V2 usa a **NBR 6023:2025**;
- o Guia de Projetos UFC foi elaborado sob a NBR 15287:2011; a V2 usa a **NBR 15287:2025**;
- o Guia de Citações UFC de 2025 já adota a **NBR 10520:2023**.

### Lista de ilustrações

A V2 oferece uma lista geral de ilustrações e mantém listas específicas por tipo. A lista geral agrega, na ordem de ocorrência no documento, figuras, gráficos e quadros; tabelas permanecem fora dessa lista e continuam em lista própria. Essa política evita que `\imprimirlistadeilustracoes` seja apenas um alias da lista de figuras e preserva as listas específicas quando o documento ou o programa exigir separação por tipo.

## Mapa de implementação

| Parte do modelo | Norma/requisito principal | Implementação |
|---|---|---|
| configuração e perfis | política UFC + normas por tipo de trabalho | `ufctex/core.def` |
| papel, margens, fonte e espaçamento | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| paginação e início de seções | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| hierarquia de seções | NBR 6024:2012 + UFC | `ufctex/layout.def` |
| alíneas e subalíneas | NBR 6024:2012 | `ufctex/layout.def` / API pública do `abntexto` |
| capa | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| folha de rosto | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| ficha catalográfica | NBR 14724:2024 + política atual da UFC | `ufctex/pretextuais.def` |
| folha de aprovação | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| dedicatória, agradecimentos, epígrafe e errata | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| resumo e abstract | NBR 6028:2021 + NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| listas pré-textuais | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` + `ufctex/objetos.def` |
| Sumário | NBR 6027:2012 + NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| figuras, gráficos e ilustrações | NBR 14724:2024 + UFC | `ufctex/objetos.def` + `ufctex/pretextuais.def` + `ufctex/compat-abntexto.def` |
| tabelas numéricas | NBR 14724:2024 + IBGE | `ufctex/objetos.def` + `tabularray-abnt` |
| quadros | NBR 14724:2024 + UFC | `ufctex/objetos.def` |
| código-fonte e algoritmos | extensão editorial compatível com NBR 14724:2024 | `ufctex/objetos.def` + `ufctex/modulos.def` |
| citações | NBR 10520:2023 + Guia UFC de Citações | `ufctex/bibliografia.def` |
| referências | NBR 6023:2025 + requisitos UFC compatíveis | `ufctex/bibliografia.def` + `ufctex/compat-nbr6023-2025.def` |
| projetos | NBR 15287:2025 + requisitos UFC compatíveis | perfil `projeto` |
| projeto anonimizado | NBR 15287:2025 + regras do edital específico | perfil `projetoanonimizado` |
| glossário | NBR 14724:2024 | módulo opcional |
| apêndices e anexos | NBR 14724:2024 | API pública do `abntexto` |
| índice | NBR 6034:2004 | módulo opcional |
| lombada | NBR 12225:2023 | módulo opcional futuro/condicional |

## Regra para divergências

Cada divergência encontrada deve ser registrada nos testes ou no código próximo ao override correspondente. Os comentários devem indicar a norma vigente, sem copiar trechos extensos ou protegidos da norma.

Exemplo:

```latex
% NBR 6023:2025: event city is optional.
\renewbibmacro*{venue}{...}
```

Não devem ser mantidos patches apenas para reproduzir uma edição antiga de um guia institucional quando eles conflitarem com a norma ABNT vigente.

## Compatibilidade dos pacotes

`abntexto`, `biblatex-abnt`, `tabularray-abnt` e outros pacotes são infraestrutura de implementação. A versão de um pacote não define, por si só, o nível de conformidade normativa da V2.

Quando um pacote ainda não implementar uma norma vigente, a V2 pode aplicar um patch mínimo, isolado e testado. Esse patch deve ser removível quando o upstream incorporar a mesma regra.

Em particular, na auditoria de 2026-08-19, o `biblatex-abnt` publicado ainda não incorporava integralmente a NBR 6023:2025; o projeto upstream mantinha uma proposta de suporte inicial em revisão. Os ajustes transitórios estão isolados em `ufctex/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível em uma versão estável do upstream.

## Gates de validação

`make preflight` é a entrada local completa da V2. Ele valida primeiro o `documento.tex` de referência e depois executa a matriz isolada de regressão: layout, geometria do PDF, pré-textuais, objetos, `minted`, citações/referências, NBR 6023:2025, projetos, seis perfis e pós-textuais/compatibilidade da API V1. A linha estável 1.x é mantida e validada separadamente em sua própria branch. O GitHub Actions deve usar os mesmos scripts e targets como gate externo em TeX Live 2026, sem introduzir validações funcionais que existam apenas no CI.

## Fontes institucionais de verificação

- Sistema de Bibliotecas da UFC — Normalização de trabalhos acadêmicos: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Sistema de Bibliotecas da UFC — Coleção de Normas Técnicas / Target GEDWeb: https://biblioteca.ufc.br/pt/colecao-de-normas-tecnicas/
- Sistema de Bibliotecas da UFC — Normas para recebimento de teses e dissertações: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-teses-e-dissertacoes/
- Sistema de Bibliotecas da UFC — Normas para recebimento de TCC: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-tcc/

## Manutenção

Antes de `v2.0.0` e de cada versão principal posterior:

1. consultar a Target GEDWeb para confirmar se houve nova edição das normas listadas;
2. revisar os Guias de Normalização da UFC;
3. atualizar esta matriz;
4. atualizar ou remover patches de compatibilidade;
5. executar `make preflight` e confirmar toda a suíte normativa;
6. não declarar conformidade com uma edição que não esteja coberta por testes.

# Base normativa da V2

Última auditoria: **2026-08-19**.

Este arquivo registra a base normativa usada pela V2 do modelo LaTeX da Universidade Federal do Ceará (UFC). Ele deve ser atualizado sempre que uma norma técnica ou regra institucional aplicável for revisada.

## Política normativa

A V2 adota a **edição vigente mais recente** de cada norma.

Quando um Guia de Normalização da UFC citar uma edição antiga de uma norma ABNT que já foi substituída, o modelo deve seguir a edição ABNT vigente. O guia institucional continua sendo usado para requisitos próprios da UFC que não conflitem com a norma atual.

Ordem de decisão:

1. legislação, regulamento, instrução normativa ou resolução institucional aplicável;
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

A lista acima representa as edições verificadas na data da auditoria. Antes de uma nova versão principal do template, as edições devem ser reconfirmadas no catálogo oficial da ABNT e, quando necessário, em uma fonte licenciada de texto integral disponível à instituição.

## Requisitos institucionais UFC

A página de normalização do Sistema de Bibliotecas da UFC, atualizada em 4 de março de 2026, informa que os Guias de Normalização institucionais estão de acordo com as normas vigentes da ABNT. Alguns PDFs históricos ainda carregam no próprio arquivo datas ou referências de edições anteriores; nesses casos, a V2 aplica a política de precedência definida acima.

### Entrega digital e PDF/A

As orientações vigentes para recebimento de TCC, dissertações e teses exigem entrega eletrônica em **PDF/A**, reunindo o trabalho completo em um único arquivo conforme a modalidade aplicável.

A V2 adota **PDF/A-2b** como perfil técnico do documento de referência. O subtipo 2b é uma decisão de implementação do projeto para produzir um PDF/A verificável; não é declarado como subtipo imposto pela UFC.

O arquivo `documento.tex` usa `\DocumentMetadata` antes de `\documentclass`, e o gate de release valida o PDF final com veraPDF. A declaração de metadados sozinha não é tratada como prova suficiente de conformidade.

### Folha de aprovação no repositório

As orientações institucionais de recebimento determinam que a folha de aprovação da versão destinada ao repositório seja apresentada **sem as assinaturas** dos componentes da banca.

A V2 produz identificação e linhas da banca, mas não incorpora assinaturas digitalizadas. A documentação orienta o usuário a não inserir imagens de assinatura na cópia destinada ao repositório quando essa política se aplicar.

### Ficha catalográfica

Em 2026, a UFC tornou facultativa a representação visual da ficha catalográfica para TCC, dissertações e teses e descontinuou o sistema CATALOG no contexto da Instrução Normativa conjunta nº 2/2026.

Por isso, `ficha-catalografica = nao` é o padrão da V2. A API de inclusão permanece disponível para casos em que uma unidade, acervo, programa ou edital específico ainda a solicite.

### Frente e verso

No modo frente-verso, a UFC adota:

- anverso: margens esquerda e superior de 3 cm; direita e inferior de 2 cm;
- verso: margens direita e superior de 3 cm; esquerda e inferior de 2 cm;
- numeração à direita no anverso e à esquerda no verso;
- início no anverso para elementos pré-textuais, exceto a ficha catalográfica, para seções textuais primárias e para elementos pós-textuais aplicáveis.

A V2 espelha as margens também durante `\pretextual` e possui regressões que medem coordenadas no PDF real e verificam o início dos elementos auditados em páginas ímpares.

### Resumo e abstract

O Guia UFC orienta resumo de trabalhos acadêmicos na faixa de **150 a 500 palavras**. O documento de referência da V2 mantém resumo e abstract nessa faixa e a suíte verifica a contagem de palavras dos arquivos de exemplo.

### Ilustrações

A fonte deve acompanhar a ilustração, inclusive quando se tratar de produção do próprio autor. A API pública usa `\ufcfonte{...}` e as fixtures normativas de objetos verificam a presença de `Fonte:` no PDF de teste.

### Referências

A apresentação institucional adotada pela V2 usa espaçamento simples dentro de cada referência e um intervalo equivalente a uma linha simples entre referências consecutivas. Além dos testes semânticos de citações e referências, a suíte registra e verifica numericamente `\baselineskip`, `\baselinestretch` e `\bibitemsep` durante a bibliografia.

### Lista de ilustrações

A V2 oferece uma lista geral de ilustrações e mantém listas específicas por tipo. A lista geral agrega, na ordem de ocorrência no documento, figuras, gráficos e quadros; tabelas permanecem fora dessa lista e continuam em lista própria. Essa política evita que `\imprimirlistadeilustracoes` seja apenas um alias da lista de figuras e preserva as listas específicas quando o documento ou o programa exigir separação por tipo.

## Mapa de implementação

| Parte do modelo | Norma/requisito principal | Implementação |
|---|---|---|
| configuração e perfis | política UFC + normas por tipo de trabalho | `ufctex/core.def` |
| papel, margens, fonte e espaçamento | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| frente-verso e início no anverso | NBR 14724:2024 + UFC | `ufctex/layout.def` + testes geométricos/duplex |
| paginação e início de seções | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| hierarquia de seções | NBR 6024:2012 + UFC | `ufctex/layout.def` |
| alíneas e subalíneas | NBR 6024:2012 | `ufctex/layout.def` / API pública do `abntexto` |
| capa | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| folha de rosto | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| ficha catalográfica | política UFC 2026 + NBR 14724:2024 | `ufctex/pretextuais.def` |
| folha de aprovação | NBR 14724:2024 + política de depósito UFC | `ufctex/pretextuais.def` |
| dedicatória, agradecimentos, epígrafe e errata | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| resumo e abstract | NBR 6028:2021 + NBR 14724:2024 + UFC | `ufctex/pretextuais.def` + gate do documento de referência |
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
| apêndices e anexos | NBR 14724:2024 | API pública do `abntexto` + política de quebra V2 quando aplicável |
| índice | NBR 6034:2004 | módulo opcional |
| PDF/A para depósito | política institucional UFC | `documento.tex` + `tests/v2-reference-check.sh` + `tests/v2-pdfa-check.sh` |
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

Na auditoria de 2026-08-19, o `biblatex-abnt` publicado ainda não incorporava integralmente a NBR 6023:2025. Os ajustes transitórios permanecem isolados em `ufctex/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível em versão estável do upstream.

## Gates de validação

`make preflight` é a entrada local completa de desenvolvimento da V2. Ele valida o `documento.tex` de referência e executa a matriz isolada de regressão: layout, geometria do PDF, pré-textuais, duplex, objetos, `minted`, citações/referências, espaçamento das referências, NBR 6023:2025, projetos, seis perfis e pós-textuais/compatibilidade da API V1.

`make release-preflight` acrescenta a validação independente PDF/A-2b com veraPDF. O script aceita uma instalação local do validator ou Docker com a imagem estável fixada pelo projeto.

No GitHub Actions, os grupos de testes podem executar em paralelo, mas o job agregado `latex-preflight` depende de todos eles. Esse nome é preservado como contrato com a proteção da branch `main`.

A linha estável 1.x é mantida e validada separadamente em sua própria branch. O CI não deve introduzir validações funcionais que não possam ser executadas pelos scripts e targets versionados no repositório, exceto a infraestrutura externa necessária ao ambiente de certificação.

## Fontes institucionais de verificação

- Sistema de Bibliotecas da UFC — Normalização de trabalhos acadêmicos: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Sistema de Bibliotecas da UFC — Normas para recebimento de teses e dissertações: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-teses-e-dissertacoes/
- Sistema de Bibliotecas da UFC — Normas para recebimento de TCC: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-tcc/
- Sistema de Bibliotecas da UFC — FAQ da ficha catalográfica: https://biblioteca.ufc.br/pt/perguntas-frequentes/ficha-catalografica-2/
- Sistema de Bibliotecas da UFC — Coleção de Normas Técnicas / Target GEDWeb: https://biblioteca.ufc.br/pt/colecao-de-normas-tecnicas/
- Sistema de Bibliotecas da UFC — aviso de indisponibilidade do Target, publicado em fevereiro de 2026: https://biblioteca.ufc.br/pt/page/2/
- ABNT Catálogo: https://www.abntcatalogo.com.br/

### Situação do Target GEDWeb

A página histórica da coleção descreve o serviço Target GEDWeb, mas aviso institucional publicado em fevereiro de 2026 informou indisponibilidade do acesso a partir de 7 de fevereiro de 2026 em razão do encerramento contratual. Enquanto o acesso institucional não for restabelecido, a manutenção da V2 não deve pressupor Target disponível.

## Manutenção

Antes de cada nova versão principal do template:

1. confirmar as edições no catálogo oficial da ABNT e, quando necessário, consultar uma fonte autorizada de texto integral disponível;
2. usar o Target GEDWeb quando o acesso institucional estiver efetivamente disponível;
3. revisar as páginas e Guias de Normalização da UFC;
4. revisar as políticas de depósito, ficha catalográfica e outros procedimentos institucionais;
5. atualizar esta matriz;
6. atualizar ou remover patches de compatibilidade;
7. executar `make preflight`;
8. executar `make release-preflight` e validar o PDF/A final;
9. confirmar o job agregado `latex-preflight` no CI;
10. não declarar conformidade com uma edição ou requisito que não esteja coberto por evidência e teste compatível.

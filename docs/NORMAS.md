# Base normativa da V2

Última auditoria: **2026-08-19**.

Este arquivo registra a política normativa e o mapa de implementação da V2 do modelo LaTeX UFC.

## Política normativa

A V2 adota a edição vigente mais recente de cada norma aplicável. Quando um guia institucional ainda citar edição substituída, a decisão segue esta ordem:

1. legislação, regulamento, instrução normativa ou resolução institucional aplicável;
2. edição vigente da norma ABNT;
3. requisito institucional específico da UFC compatível com a norma vigente;
4. Guia de Normalização da UFC mais recente aplicável;
5. comportamento de `abntexto` e demais pacotes.

O comportamento de um pacote nunca prevalece sobre requisito normativo ou institucional aplicável.

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

## Requisitos institucionais UFC

A página de normalização do Sistema de Bibliotecas da UFC foi atualizada em 4 de março de 2026 e orienta o uso das normas ABNT vigentes. PDFs históricos dos guias continuam úteis para requisitos institucionais que não conflitem com edições ABNT posteriores.

### PDF/A

As orientações de recebimento consultadas em 2026 exigem arquivo eletrônico **PDF/A** para TCC, dissertações e teses destinados ao repositório.

A V2 usa **PDF/A-2b** como perfil técnico verificável. O subtipo 2b é escolha de implementação do projeto, não requisito específico atribuído à UFC.

`documento.tex` e a matriz final de perfis usam `\DocumentMetadata` antes de `\documentclass`. A declaração XMP não é considerada prova suficiente: o gate de release usa veraPDF.

### Folha de aprovação

A versão destinada ao repositório deve apresentar a folha de aprovação sem assinaturas. A V2 produz identificação e linhas da banca, mas não incorpora assinaturas digitalizadas.

### Ficha catalográfica

Em 2026, a representação visual da ficha catalográfica tornou-se facultativa no contexto da Instrução Normativa conjunta nº 2/2026, e o serviço CATALOG foi descontinuado. Por isso:

```tex
ficha-catalografica = nao
```

é o padrão.

Quando a ficha for usada, a V2 diferencia os modos de impressão:

- `anverso`: a ficha ocupa página física, mas não incrementa a contagem lógica;
- `frente-verso`: a ficha ocupa o verso da folha de rosto e permanece na sequência contada.

A regressão `tests/v2-catalog-card-check.sh` valida os dois comportamentos com pdfLaTeX e LuaLaTeX. Como a ficha é um PDF externo, sua inclusão pode alterar a conformidade PDF/A do trabalho; o arquivo completo deve ser validado novamente com veraPDF.

### Trabalhos em mais de um volume

A identificação do volume deve aparecer quando o trabalho for dividido em mais de um volume, e a paginação permanece única e sequencial entre os volumes.

A V2 oferece:

```tex
volume = {2},
pagina-inicial = 101
```

O módulo `ufctex/trabalhos.def` aplica `volume` à capa e à folha de rosto dos trabalhos acadêmicos e preserva `pagina-inicial` após a capa. A regressão `tests/v2-multivolume-check.sh` valida o comportamento nos dois motores suportados.

### Frente e verso

No modo `frente-verso`:

- anverso: esquerda/superior 3 cm; direita/inferior 2 cm;
- verso: direita/superior 3 cm; esquerda/inferior 2 cm;
- numeração à direita no anverso e à esquerda no verso;
- elementos pré-textuais, exceto ficha catalográfica, iniciam no anverso;
- seções textuais primárias e elementos pós-textuais controlados pela V2 iniciam no anverso.

As regressões geométricas medem o PDF real, incluindo margens, paginação e paridade física.

### Resumo e abstract

O documento de referência mantém resumo e abstract entre 150 e 500 palavras. A suíte conta as palavras dos arquivos distribuídos e verifica a presença das palavras-chave.

### Ilustrações e tabelas

A fonte acompanha ilustrações e tabelas, inclusive quando o conteúdo é de elaboração própria. A API pública usa `\ufcfonte{...}`.

A Lista de Ilustrações agrega figuras, gráficos e quadros na ordem de ocorrência. Tabelas permanecem em lista própria. Listas específicas continuam disponíveis.

### Referências

As referências usam espaçamento simples internamente e intervalo equivalente a uma linha simples entre entradas consecutivas. O gate mede `\baselineskip`, `\baselinestretch` e `\bibitemsep` durante a bibliografia.

## Mapa de implementação

| Parte | Norma/requisito principal | Implementação |
|---|---|---|
| configuração e perfis | política UFC + normas por tipo | `ufctex/core.def` |
| papel, margens, fonte e espaçamento | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| duplex e início no anverso | NBR 14724:2024 + UFC | `ufctex/layout.def` + regressões geométricas |
| ativos institucionais | identidade visual UFC | `ufctex/institucional.def` + `assets/institucional/` |
| capa e folha de rosto | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` + `ufctex/trabalhos.def` |
| volume e paginação contínua | NBR 14724:2024 + UFC | `ufctex/trabalhos.def` |
| ficha catalográfica | política UFC 2026 + NBR 14724:2024 | `ufctex/trabalhos.def` |
| folha de aprovação | NBR 14724:2024 + política de depósito UFC | `ufctex/pretextuais.def` |
| dedicatória, agradecimentos, epígrafe e errata | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| resumo e abstract | NBR 6028:2021 + UFC | `ufctex/pretextuais.def` |
| listas e Sumário | NBR 14724:2024 + NBR 6027:2012 | `ufctex/pretextuais.def` + `ufctex/objetos.def` |
| seções e subdivisões | NBR 6024:2012 + UFC | `ufctex/layout.def` / `abntexto` |
| figuras, gráficos e quadros | NBR 14724:2024 + UFC | `ufctex/objetos.def` |
| tabelas numéricas | NBR 14724:2024 + IBGE | `ufctex/objetos.def` + `tabularray-abnt` |
| código e algoritmos | extensão editorial compatível | `ufctex/objetos.def` + `ufctex/modulos.def` |
| citações | NBR 10520:2023 | `ufctex/bibliografia.def` |
| referências | NBR 6023:2025 | `ufctex/bibliografia.def` + `ufctex/compat-nbr6023-2025.def` |
| projetos | NBR 15287:2025 | `ufctex/projetos.def` |
| glossário | NBR 14724:2024 | módulo opcional |
| apêndices e anexos | NBR 14724:2024 | API pública do `abntexto` + política V2 de quebra |
| índice | NBR 6034:2004 | módulo opcional |
| PDF/A | política institucional UFC | `\DocumentMetadata` + veraPDF |
| compatibilidade V1 | transição de documentos | `ufctex/compat-v1.def` |

## Compatibilidade dos pacotes

`abntexto`, `biblatex-abnt`, `tabularray-abnt` e demais pacotes são infraestrutura. A versão de um pacote não define, isoladamente, o nível de conformidade normativa da V2.

Na auditoria de 2026-08-19, os ajustes necessários para NBR 6023:2025 permanecem isolados em `ufctex/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível de forma estável no upstream.

## Build

O `Makefile` executa uma primeira passagem LaTeX e decide os processadores auxiliares pelos artefatos efetivamente produzidos:

- `.bcf` contendo uma `datasource` bibliográfica → Biber;
- `.glo` não vazio → `makeglossaries`;
- `.idx` não vazio → `makeindex`.

Assim, documentos sem fonte bibliográfica, glossário ou índice não dependem desses processadores. `tests/v2-build-path-check.sh` usa executáveis-falha deliberados para provar que processadores desnecessários não são chamados.

## Gates de validação

`make preflight` executa:

- consistência estática da distribuição;
- documento de referência;
- layout, A4, margens e paginação real;
- pré-textuais e duplex;
- ficha catalográfica nos dois modos;
- trabalhos multivolume;
- objetos, tabelas, códigos, algoritmos e `minted`;
- citações, referências e espaçamento;
- projetos;
- seis perfis completos em pdfLaTeX e LuaLaTeX;
- pós-textuais e compatibilidade pública da API V1;
- fluxo modular do `Makefile`.

A matriz de perfis produz **12 PDFs**: seis perfis × dois motores. Cada PDF é verificado quanto a conteúdo específico do perfil, A4, fontes incorporadas, Sumário, ausência de estrutura `chapter`, ausência de warnings/overflow não reconhecidos e declaração PDF/A-2b.

`make release-preflight` acrescenta veraPDF para o documento de referência e para os 12 PDFs da matriz.

No GitHub Actions, o job agregado `latex-preflight` depende de todos os grupos funcionais e permanece como contrato da proteção da branch `main`.

## Consistência da distribuição

`tests/v2-distribution-check.sh` impede a reintrodução de:

- `\chapter` e helpers V1 nos arquivos distribuídos ao usuário;
- qualquer pasta `lib/` na distribuição V2;
- referências ativas a arquivos inexistentes;
- ausência do brasão em `assets/institucional/`;
- divergência entre a versão do `Makefile`, da classe e do README;
- scripts `tests/v2-*.sh` com erro de sintaxe POSIX shell.

A linha 1.x permanece preservada em sua própria branch para documentos legados.

## Fontes institucionais de verificação

- Sistema de Bibliotecas da UFC — Normalização de trabalhos acadêmicos: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Sistema de Bibliotecas da UFC — Normas para recebimento de teses e dissertações: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-teses-e-dissertacoes/
- Sistema de Bibliotecas da UFC — Normas para recebimento de TCC: https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-tcc/
- Sistema de Bibliotecas da UFC — FAQ da ficha catalográfica: https://biblioteca.ufc.br/pt/perguntas-frequentes/ficha-catalografica-2/
- Sistema de Bibliotecas da UFC — Coleção de Normas Técnicas: https://biblioteca.ufc.br/pt/colecao-de-normas-tecnicas/
- ABNT Catálogo: https://www.abntcatalogo.com.br/

## Manutenção

Antes de nova versão principal:

1. reconfirmar as edições normativas;
2. revisar páginas e guias da UFC;
3. revisar políticas de depósito e ficha catalográfica;
4. atualizar ou remover patches de compatibilidade;
5. executar `make preflight`;
6. executar `make release-preflight`;
7. confirmar `latex-preflight` no CI;
8. não declarar conformidade que não possua evidência e teste compatível.

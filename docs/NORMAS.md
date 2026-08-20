# Base normativa da V2

Última auditoria: **2026-08-20**.

Este arquivo registra a política normativa e o mapa de implementação da V2 do modelo LaTeX UFC.

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

Consequentemente, a V2 não interpreta a data do PDF institucional como prova de vigência normativa. Cada requisito é confrontado com a norma ABNT vigente e com atos institucionais posteriores.

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

### Tipografia

O Guia UFC de Trabalhos Acadêmicos atualmente vinculado exige **Arial ou Times New Roman, tamanho 12**, inclusive na capa. Prevê tamanho menor e uniforme para citações longas, notas de rodapé, paginação, ficha catalográfica, legendas e fontes de ilustrações e tabelas, recomendando tamanho 10 para essas exceções.

A implementação V2 deve distinguir a família tipográfica literal de substitutos metricamente ou visualmente compatíveis. `NewTX` e `TeX Gyre Termes` não devem ser declaradas como Times New Roman. A identidade tipográfica será objeto de gate próprio antes da próxima release.

Ambientes de código, algoritmos e matemática permanecem em auditoria específica para determinar se há exceção institucional aplicável ou se devem seguir a família principal.

### PDF/A

As orientações de recebimento consultadas em 2026 exigem arquivo eletrônico **PDF/A** para TCC, dissertações e teses destinados ao repositório.

A V2 usa **PDF/A-2b** como perfil técnico verificável. O subtipo 2b é escolha de implementação do projeto, não requisito específico atribuído à UFC.

`documento.tex` e a matriz final de perfis usam `\DocumentMetadata` antes de `\documentclass`. A declaração XMP não é considerada prova suficiente: o gate de release usa veraPDF.

### Folha de aprovação

A versão destinada ao repositório deve apresentar a folha de aprovação sem assinaturas. A V2 produz identificação e linhas da banca, mas não incorpora assinaturas digitalizadas.

### Ficha catalográfica

A Instrução Normativa Conjunta nº 2/2026 torna facultativa a representação visual da ficha catalográfica para TCC, dissertações e teses e registra que sua ausência não impede aprovação, depósito ou divulgação. O serviço institucional de elaboração e o módulo CATALOG foram descontinuados para esses trabalhos. Por isso:

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

### Paginação

Para trabalhos em anverso, a UFC orienta contar sequencialmente as folhas a partir da folha de rosto, considerando somente o anverso; capa e ficha catalográfica não entram nessa contagem. A numeração aparece a partir da primeira folha textual, no canto superior direito.

Para frente e verso, a contagem considera as páginas a partir da folha de rosto, e a posição da numeração alterna entre canto superior direito no anverso e superior esquerdo no verso. Apêndices e anexos mantêm paginação contínua, assim como trabalhos em mais de um volume.

### Espaçamento

O Guia UFC orienta espaço 1,5 no corpo do trabalho e espaço simples nas exceções institucionais, incluindo citações longas, notas de rodapé, referências, legendas, ficha catalográfica e natureza do trabalho. Não deve existir espaço adicional entre parágrafos. Referências consecutivas são separadas por uma linha simples em branco.

### Resumo e abstract

O documento de referência mantém resumo e abstract entre 150 e 500 palavras. A suíte conta as palavras dos arquivos distribuídos e verifica a presença das palavras-chave.

### Ilustrações e tabelas

A fonte acompanha ilustrações e tabelas, inclusive quando o conteúdo é de elaboração própria. A API pública usa `\ufcfonte{...}`.

A Lista de Ilustrações agrega figuras, gráficos e quadros na ordem de ocorrência. Tabelas permanecem em lista própria. Listas específicas continuam disponíveis.

### Citações

O Guia UFC de Citações de 2025 foi elaborado conforme a NBR 10520:2023. Para citações diretas com mais de três linhas, orienta parágrafo distinto, letra menor que a do texto, espaço simples, sem aspas e recomenda recuo de 4 cm.

### Referências

O PDF institucional atualmente vinculado ainda usa NBR 6023:2018. Para a V2 prevalece a NBR 6023:2025. As referências usam espaçamento simples internamente e intervalo equivalente a uma linha simples entre entradas consecutivas. O gate mede `\baselineskip`, `\baselinestretch` e `\bibitemsep` durante a bibliografia.

### Projetos de pesquisa

O Guia UFC de Projetos atualmente vinculado ainda declara NBR 15287:2011. Para os perfis `projeto` e `projetoanonimizado`, a V2 adota NBR 15287:2025 e preserva apenas requisitos institucionais do guia que continuem compatíveis com a edição vigente.

## Mapa de implementação

| Parte | Norma/requisito principal | Implementação |
|---|---|---|
| configuração e perfis | política UFC + normas por tipo | `ufctex/core.def` |
| tipografia | NBR 14724:2024 + requisito UFC Arial/Times New Roman | auditoria em andamento; será isolada em módulo próprio antes da próxima release |
| papel, margens e espaçamento | NBR 14724:2024 + UFC | `ufctex/layout.def` |
| duplex e início no anverso | NBR 14724:2024 + UFC | `ufctex/layout.def` + regressões geométricas |
| ativos institucionais | identidade visual UFC | `ufctex/institucional.def` + `assets/institucional/` |
| capa e folha de rosto | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` + `ufctex/trabalhos.def` |
| volume e paginação contínua | NBR 14724:2024 + UFC | `ufctex/trabalhos.def` |
| ficha catalográfica | IN Conjunta 2/2026 + NBR 14724:2024 | `ufctex/trabalhos.def` |
| folha de aprovação | NBR 14724:2024 + política de depósito UFC | `ufctex/pretextuais.def` |
| dedicatória, agradecimentos, epígrafe e errata | NBR 14724:2024 + UFC | `ufctex/pretextuais.def` |
| resumo e abstract | NBR 6028:2021 + UFC | `ufctex/pretextuais.def` |
| listas e Sumário | NBR 14724:2024 + NBR 6027:2012 | `ufctex/pretextuais.def` + `ufctex/objetos.def` |
| seções e subdivisões | NBR 6024:2012 + UFC | `ufctex/layout.def` / `abntexto` |
| figuras, gráficos e quadros | NBR 14724:2024 + UFC | `ufctex/objetos.def` |
| tabelas numéricas | NBR 14724:2024 + IBGE | `ufctex/objetos.def` + `tabularray-abnt` |
| código e algoritmos | extensão editorial em auditoria tipográfica | `ufctex/objetos.def` + `ufctex/modulos.def` |
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

Os ajustes necessários para NBR 6023:2025 permanecem isolados em `ufctex/compat-nbr6023-2025.def` e possuem regressões próprias. O arquivo deve ser reduzido ou removido quando o suporte equivalente estiver disponível de forma estável no upstream.

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

A próxima release deve acrescentar um gate de **identidade tipográfica**. A simples verificação de `embedded=yes` não é suficiente para comprovar Arial ou Times New Roman literal.

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
5. executar `make preflight`;
6. executar `make release-preflight`;
7. confirmar `latex-preflight` no CI;
8. não declarar conformidade que não possua evidência e teste compatível.

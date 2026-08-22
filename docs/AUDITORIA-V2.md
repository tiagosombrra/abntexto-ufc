# Auditoria integral da candidata V2.1.0

Data: 2026-08-21.

## Escopo

A auditoria cobre arquivos rastreados pelo Git, classe e módulos V2, template distribuído, exemplos, documentação, scripts, testes, workflows e artefatos de release. O objetivo é bloquear resíduos da arquitetura anterior que não pertencem à implementação V2 corrente e fazer o documento de referência funcionar como corpus visual e semântico de regressão.

## Achados

| ID | Achado | Estado |
|---|---|---|
| A1 | `pretextuais.def` ainda procurava `lib/logo-ufc.PNG` | corrigido na Fase 4 |
| A2 | capa, folha de rosto, ficha e brasão tinham implementações duplicadas/sobrescritas entre módulos | corrigido na Fase 4 |
| A3 | exemplo principal do README usava chaves `\ufcsetup` inexistentes na API V2 | corrigido na Fase 4 |
| A4 | `errata.tex` mantinha exemplo histórico específico e tabela antiga com conteúdo alheio ao template | corrigido na Fase 4 |
| A5 | `figuras/main.cpp` usava `system("pause")`, dependente de Windows | corrigido na Fase 4 |
| A6 | `trabalhos-relacionados.tex`, apêndices e anexos eram distribuídos mas não compilados no documento base | corrigido na Fase 4 |
| A7 | documento base exercitava poucas variações de figuras, tabelas, códigos e algoritmos | ampliado na Fase 4 |
| A8 | `ufcalgoritmo` não possuía uma rota explícita e testada para suprimir números de linha | corrigido na Fase 4 (`[0]`) |
| A9 | auditoria automática não verificava todos os arquivos rastreados, chaves públicas e duplicidade de comandos internos | novo Gate A |
| A10 | `topics` do `abntexto` falhou com `\DocumentMetadata`/tagging ativo no TeX Live 2026 | substituído na API V2 por `ufcalineas`/`ufcsubalineas`, exercitados com metadata ativa |
| A11 | exemplos de figuras eram majoritariamente caixas sintéticas e não exerciam arquivos raster reais | PNG e JPEG adicionados ao corpus e aos checks de distribuição |
| A12 | teste de pacote ainda usava a expressão “Gate D” para uma etapa que não fecha o Gate D formal | corrigido para `Release package preflight` |
| A13 | regra inicial para `lib/` confundia caminho legado do projeto com o diretório legítimo do Chocolatey | regra refinada para caminhos da arquitetura anterior e pasta rastreada `lib/` |
| A14 | `algpseudocodex` ocultava `EndIf`/`EndWhile` por padrão, mas continuava consumindo seus números, produzindo linhas numeradas vazias e espaçamento irregular | `noEnd=false` aplicado; regressão exige sequência 1–8 e conteúdo visível nas linhas 5 e 7 |
| A15 | uso de fotografias institucionais reais precisava separar licença de imagem da LPPL do projeto | Reitoria e Campus do Pici usam originais CC BY-SA 4.0 com SHA-1 verificado e atribuição em `figuras/LICENCAS.md` |
| A16 | foi localizada fotografia oficial da fachada do Departamento de Computação, mas sem licença pública de redistribuição identificada | não redistribuída; corpus usa fotografia livre do Campus do Pici e identifica corretamente o DC no Bloco 910 sem afirmar que a imagem mostra sua fachada |

## Corpus de referência

O `documento.tex` passa a exercer diretamente:

- pré-textuais, incluindo errata;
- figuras estreita, intermediária e larga;
- PNG e JPEG incluídos por `\includegraphics`;
- fotografias reais da UFC com licenças próprias verificadas;
- legenda curta e longa, Fonte e Nota;
- gráfico e quadro;
- tabela nativa;
- `tabularray-abnt` com Fonte, Nota e linhas alternadas;
- C++, Python e Java com diferentes políticas de números de linha;
- algoritmos numerados e sem numeração;
- estruturas condicionais/laços com términos visíveis quando a numeração está ativa;
- equação numerada e referenciada;
- citação longa;
- alíneas, subalíneas e enumeração;
- referências, glossário e índice;
- quatro apêndices e dois anexos.

As caixas sintéticas permanecem no corpus porque permitem controlar larguras exatas independentemente do conteúdo gráfico. Os arquivos raster e as fotografias institucionais complementam essa cobertura exercitando a rota real de inclusão de imagens.

As fotografias externas não são tratadas como cobertas pela LPPL do `ufctex`. `tools/fetch-reference-images.py` baixa os originais licenciados, verifica seus SHA-1 e `figuras/LICENCAS.md` registra autoria, fonte e licença. O Gate R exige os arquivos reais no CI; o código do exemplo possui fallback apenas para clones offline que ainda não executaram `make reference-assets`.

Casos mutuamente exclusivos ou dependentes do ambiente permanecem em fixtures dedicadas: `minted`, fontes Microsoft literais, frente-verso, ficha catalográfica externa, perfis de trabalho e projetos.

## Gate A — auditoria integral

`tests/v2-repository-audit.py` verifica todos os arquivos rastreados e reprova, entre outros casos:

- caminhos ou APIs da arquitetura anterior em arquivos correntes;
- marcadores explícitos de trabalho pendente ou correção temporária;
- caminhos absolutos ligados a máquinas de desenvolvimento;
- artefatos gerados versionados por engano;
- texto fora de UTF-8 ou sem newline final;
- divergência de versão entre Makefile, classe, README CTAN e changelog;
- chaves `\ufcsetup` inexistentes em exemplos `.tex`/`.md`;
- módulo carregado mas ausente;
- definição do mesmo comando interno em múltiplos módulos.

A regra de caminhos legados diferencia referências do próprio projeto de diretórios legítimos de ferramentas externas. Uma pasta rastreada `lib/` continua proibida na V2, assim como referências conhecidas à arquitetura anterior.

## Gate R — corpus de referência

`tests/v2-reference-corpus-check.sh` valida no PDF e nos arquivos de listas que os exemplos do corpus foram efetivamente gerados e indexados. Quando `UFC_REQUIRE_REFERENCE_IMAGES=1`, também exige as duas fotografias externas e valida seus SHA-1. O gate existente de referência continua responsável por warnings, overflow, PDF/A e incorporação de fontes.

`tests/v2-algorithm-numbering-check.sh` exerce algoritmos com e sem números de linha nos dois engines e reprova números duplicados, sequência incompleta ou linhas numeradas sem conteúdo. A fixture reproduz a estrutura `While` + `If` + `EndIf` + `EndWhile` que revelou A14.

`tests/normativa/normativa-complementar.tex` exerce `ufcalineas`/`ufcsubalineas` com `\DocumentMetadata` ativo para impedir regressão da combinação que revelou A10.

Os testes de pacote de release exigem que o corpus, seus arquivos raster, as fotografias licenciadas e o arquivo de atribuição estejam presentes no template local, bundle Overleaf e candidato CTAN/TDS.

A candidata 2.1.0 só retorna à Fase 3 de distribuição após Gate A, Gate R e o `latex-preflight` completo ficarem verdes e o PDF do corpus ser inspecionado visualmente.

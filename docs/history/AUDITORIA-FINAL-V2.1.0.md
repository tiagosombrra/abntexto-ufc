# Auditoria final V2.1.0

Data: 2026-08-23.

## Escopo

A V2.1.0 foi submetida a uma auditoria normativa, visual, estrutural e de distribuição antes da tag imutável. A revisão final cobre código e arquitetura, interface pública, normas UFC/ABNT vigentes, documento de referência, testes e fixtures, CI, bundles reais, licenças e ativos, Overleaf, Windows, PDF/A, metadados de release, candidato CTAN e resíduos legados.

## Base normativa reconfirmada

A política de `docs/NORMAS.md` permanece válida: normas e atos institucionais aplicáveis, edições ABNT vigentes e requisitos UFC compatíveis. Para trabalhos acadêmicos são adotadas NBR 14724:2024 (versão corrigida de 2025), NBR 10520:2023, NBR 6023:2025, NBR 6028:2021, NBR 6024:2012, NBR 6027:2012, NBR 6034:2004, NBR 12225:2023 e, para projetos, NBR 15287:2025, além das Normas de Apresentação Tabular do IBGE e atos institucionais UFC.

O SiBi-UFC exige arquivo eletrônico PDF/A da capa aos anexos e folha de aprovação sem assinaturas para depósito. A Instrução Normativa Conjunta nº 2/2026 torna facultativa a ficha catalográfica visual em TCC, dissertação e tese.

## Achados normativos e visuais anteriores

| ID | Achado | Classificação | Ação |
|---|---|---|---|
| F1 | números de linha de códigos e algoritmos apareciam antes do limite esquerdo de 3 cm | DIVERGENTE | `objetos.def` passou a reservar margem interna quando existe numeração; gate geométrico mede o PDF |
| F2 | smoke real no Overleaf usou NewTX por ausência de Times New Roman literal | PORTABILIDADE CONFORME | documentação e validador distinguem portabilidade de certificação tipográfica; Gate T Windows certifica fontes literais |
| F3 | PDF de referência é PDF/A-2b e `pt-BR`, mas não é tagged PDF e não possui bookmarks completos | ACESSIBILIDADE AVANÇADA | perfil de acessibilidade reporta os itens sem atribuí-los indevidamente como requisito UFC |
| F4 | checks antigos não distinguiam evidência automática, heurística e revisão humana | LACUNA DE VALIDAÇÃO | validador usa estados explícitos e nível de evidência |
| F5 | listas paginadas e entradas primárias do sumário podiam sair sem líder pontilhado | DIVERGENTE | perfil UFC reativa líderes e mantém regressão dedicada |
| F6 | CI acumulava orquestração redundante e recompilações desnecessárias | EFICIÊNCIA | `tests/run.py` tornou-se o orquestrador único e a distribuição reutiliza seus artefatos |

## Gate V — validador de PDF

A V2 inclui `tools/validate-ufc-pdf.py`, a interface Web/Lite em `validator/` e regressões próprias. O modo Web/Lite processa os bytes do PDF localmente no navegador e não contém API de upload. O gate de fonte passa a bloquear também uma futura introdução de `fetch()`, além de XHR, FormData, sendBeacon e WebSocket.

O perfil portátil admite fallback tipográfico apenas como alerta. O perfil estrito reprova a ausência de Times New Roman/Arial literal e exige validação profunda de PDF/A. O perfil de acessibilidade acrescenta tagging/PDF/UA e mantém revisão humana quando a evidência automática é insuficiente.

## Gate C — CI consolidado

A interface principal de validação é `python3 tests/run.py --mode pr`, também disponível por `make check` e `make preflight`. O modo `release` acrescenta certificações profundas de PDF/A e é exposto por `make release-check` e `make release-preflight`.

Os scripts `tests/v2-*` permanecem como implementações de baixo nível. Wrappers redundantes do Makefile foram removidos após equivalência no mesmo SHA. O Gate T mantém certificação independente de Overleaf e Windows. Actions externas dos workflows são fixadas por SHA para reduzir risco de supply chain.

## Gate F — pente-fino irrestrito

O Gate F reabriu a árvore e os artefatos já certificados, sem presumir que um `PASS` anterior encerrava a revisão. Foram inspecionados o ZIP real produzido pelo `distribution-preflight`, o PDF canônico de 41 páginas renderizado integralmente, a árvore de fontes, os manifests de CI, a política normativa, a proveniência histórica e a estrutura destinada ao CTAN.

Achados e resoluções:

1. resíduos documentais de `compat-v1.def` e “compatibilidade V1” foram removidos de `docs/NORMAS.md`; a auditoria do repositório passa a impedir sua reintrodução;
2. a pendência de redistribuição do brasão foi encerrada por decisão do projeto: o ativo oficial é redistribuído sem modificação, não é declarado LPPL e permanece sujeito às regras de identidade visual da UFC;
3. o README CTAN passou a explicitar a matriz de licenças: LPPL 1.3c+ para código/documentação, CC BY-SA 4.0 para duas fotografias de referência e tratamento separado do brasão institucional;
4. o candidato CTAN foi simplificado para um layout navegável sem um `.tds.zip` interno redundante; o preflight passa a compilar um documento mínimo a partir do ZIP CTAN extraído;
5. dependências efetivas de fontes e a versão mínima de `tabularray-abnt` foram explicitadas;
6. a data de release da classe e do changelog foi alinhada a 2026-08-23 e passou a ter regressão de consistência;
7. o workflow do GitHub Pages foi fixado em SHAs imutáveis e a auditoria passa a exigir pin completo de actions externas;
8. a proveniência histórica foi preservada: template UFC original de Ednardo Moreira Rodrigues e Alan Batista de Oliveira, com linhagem parcial em `ueceTeX2` de Thiago Nascimento, e redesign/manutenção V2 por Tiago Guimarães Sombra.

O PDF de referência permaneceu visualmente íntegro em 41 páginas A4, PDF 1.7/PDF-A-2b, sem fontes não incorporadas, JavaScript, formulários, criptografia, clipping, sobreposição ou invasão aparente de margens. Tagged PDF, bookmarks e metadados bibliográficos avançados continuam classificados como melhorias de acessibilidade/metadados, não como requisito UFC falsamente atribuído.

## Critério de fechamento

O Gate F só é considerado concluído quando o SHA que contém todas as correções acima recebe, no mesmo commit, sucesso em `ufctex/reference-audit`, `ufctex/latex-preflight`, proxy Overleaf, build/certificação Windows e `ufctex/distribution-preflight`, além do check do validador Pages. Após essa certificação, o fluxo permitido é squash merge em `main`, tag imutável `v2.1.0` no SHA resultante do squash, GitHub Release e submissão do ZIP CTAN verificado.

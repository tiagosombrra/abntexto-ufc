# Base normativa da V2

Última revisão: **2026-08-28**.  
Estado do projeto: **v2.2.0 em auditoria N15; B2R-A2 ativa**.

Este documento é o mapa humano da base normativa e de sua relação com a implementação. A autoridade máquina-legível permanece em `normativa/`; evidência executável permanece em `tests/` e GitHub Actions. Este arquivo não cria requisitos novos.

## Política de precedência

O projeto aplica a edição vigente da norma técnica correspondente e não permite que uma referência antiga dentro de um guia UFC reative uma norma substituída.

Para requisito técnico:

**norma ABNT vigente → requisito UFC compatível/complementar → guia UFC → implementação**.

Para requisito institucional:

**ato UFC vigente → requisito institucional UFC vigente → guia UFC → norma técnica, quando aplicável → implementação**.

Conflitos reais entre fontes atuais recebem revisão explícita; não são resolvidos silenciosamente.

## Base técnica corrente

| Assunto | Referência adotada | Escopo |
| --- | --- | --- |
| Trabalhos acadêmicos | **ABNT NBR 14724:2024**, versão corrigida em 01/04/2025 | estrutura e apresentação |
| Artigo em publicação periódica | **ABNT NBR 6022:2018** | contrato `article.*`; runtime ainda pendente |
| Citações | **ABNT NBR 10520:2023** | citações |
| Referências | **ABNT NBR 6023:2025** | referências |
| Projetos de pesquisa | **ABNT NBR 15287:2025** | perfis de projeto |
| Resumo, resenha e recensão | **ABNT NBR 6028:2021** | resumos e palavras-chave |
| Numeração progressiva | **ABNT NBR 6024:2012** | seções |
| Sumário | **ABNT NBR 6027:2012** | sumário |
| Índice | **ABNT NBR 6034:2004** | índice |
| Lombada | **ABNT NBR 12225:2023** | requisito condicional |
| Tabelas numéricas | **IBGE, Normas de Apresentação Tabular, 3. ed., 1993** | apresentação tabular |
| Ficha catalográfica | **IN Conjunta UFC nº 2/2026** | representação visual facultativa no depósito |
| Agradecimento CAPES | **Portaria CAPES nº 206/2018** | requisito condicional |

A vigência, os IDs exatos, status e exclusões são controlados por `normativa/source-audit.json`, `normativa/version-policy.json`, `normativa/catalog.json` e `normativa/precedence.json`.

## Fontes institucionais UFC

A página vigente de Normalização do Sistema de Bibliotecas da UFC lista cinco guias. Eles são tratados como fontes institucionais dentro da política de precedência, não como substitutos da edição técnica vigente.

Para artigo científico, a fonte institucional ativa é `ufc-guia-artigos-2022`, edição bibliográfica 2022, no arquivo corrigido publicado em 27/04/2023. A identidade `ufc-guia-artigos-2021` permanece apenas como histórico superseded.

A reconciliação detalhada de vigência está em `docs/VIGENCIA-NORMATIVA.md`.

## Estado do contrato de artigo

N15-B2A/PR #145 já promoveu:

- `abnt-nbr-6022-2018`;
- `ufc-guia-artigos-2022`;
- 13 predicados `article.*`;
- locators e metadados de fase correspondentes.

Isso **não significa que o runtime do artigo já exista**. A classe ainda não oferece o perfil final de artigo. A implementação pertence a N15-B2B, depois da normalização pública de API em B2R-B.

Recomendações do guia, como 150–250 palavras no resumo, mínimo de três palavras-chave ou família tipográfica quando expressas por `convém`/`recomenda-se`, não são convertidas automaticamente em obrigação.

## Estados de evidência

A máquina usa o modelo explícito de proof state. O baseline histórico N0–N14 registrava:

- `PARTIAL=113`;
- `NOT_PROVEN=51`;
- `CONDITIONAL=10`;
- `MANUAL=6`;
- `NOT_APPLICABLE=1`;
- `PROVEN=0`.

CI verde não promove automaticamente uma regra para `PROVEN`. A força da evidência depende do tipo de observação e do vínculo fonte → predicate → locator → implementação → medição.

## Implementação canônica atual

Módulos internos ativos da classe:

```text
abntexto-ufc.cls
abntexto-ufc/
├── core.def
├── fonts.def
├── layout.def
├── modules.def
├── frontmatter.def
├── institutional.def
├── academic-works.def
├── research-projects.def
├── objects.def
├── bibliography.def
├── compat-abntexto.def
├── compat-nbr6023-2025.def
└── backmatter.def
```

Os nomes antigos dos módulos foram removidos em B2R-A1/PR #146. O `latex-preflight.yml` N12 permanece congelado; a compatibilidade histórica de hash é tratada no checker dedicado sem restaurar os paths antigos.

## Layout canônico do template em B2R-A2

A2 normaliza a superfície visível do projeto para:

```text
main.tex
frontmatter/
chapters/
backmatter/
figures/
assets/institutional/ufc-coat-of-arms.png   # source-only
```

O bundle de template e o bundle Overleaf usam o mesmo layout de conteúdo; `main.tex` fica na raiz do arquivo importável no Overleaf.

O brasão institucional real não é redistribuído nos bundles públicos. O suporte da classe a um arquivo oficial fornecido localmente permanece disponível.

## Matriz humana requisito → implementação → evidência

| Requisito / grupo | Estado resumido | Implementação / evidência principal |
| --- | --- | --- |
| A4 e margens | conforme no escopo testado | `layout.def`; geometry checks |
| fonte 12 e parágrafos | conforme no escopo testado | `fonts.def`, `layout.def`; font/layout gates |
| Times New Roman / Arial literais | conforme no escopo certificado | Gate T Windows; embedding/PDF-A checks |
| capa/folha de rosto/volume | conforme no escopo testado | `frontmatter.def`, `academic-works.def` |
| ficha catalográfica | conforme ao contrato vigente | política default + fixture dedicada |
| resumo/abstract/listas/sumário | conforme no escopo testado | `frontmatter.def`; reference/profile checks |
| seções | conforme no escopo testado | `layout.def`; NBR 6024 checks |
| figuras, gráficos, quadros | conforme no escopo testado | `objects.def`; object geometry |
| tabelas numéricas | conforme no escopo testado | `objects.def`; IBGE/tabularray checks |
| código/algoritmos | política editorial testada | módulos opcionais + typography/numbering checks |
| citações | conforme no escopo testado | `bibliography.def`; NBR 10520 checks |
| referências | conforme no escopo testado | `bibliography.def`, `compat-nbr6023-2025.def` |
| projetos | conforme no escopo testado | `research-projects.def`; profile/project checks |
| apêndices/anexos/índice | conforme no escopo testado | `backmatter.def` + checks dedicados |
| PDF/A-2b | política técnica do projeto + requisitos de depósito aplicáveis | `\DocumentMetadata`, veraPDF e validator |
| artigo científico | **contrato normativo ativo; runtime pendente** | `coverage-rules-article.json`; B2B/B2C ainda futuros |

A cobertura atômica não é duplicada manualmente aqui; consulte `normativa/atomic-rules.json`, coverage manifests, locator audit e proof-state artifacts.

## Tipografia

A API pública atual ainda usa a superfície portuguesa da v2.x, por exemplo:

```tex
\ufcsetup{
  fonte = times,
  fonte-estrita = nao
}
```

B2R-B introduzirá nomes canônicos em inglês de forma aditiva, mantendo os nomes portugueses suportados como aliases de compatibilidade em v2.x.

Fallback portátil não equivale à certificação tipográfica literal. O Gate T Windows certifica Times New Roman e Arial literais, variantes, incorporação, Unicode e PDF/A-2b. Fontes Microsoft proprietárias não são redistribuídas.

## Citações e referências

Citações seguem NBR 10520:2023 no escopo implementado. Referências seguem NBR 6023:2025. Compatibilidade temporária necessária ao escopo testado fica isolada em `abntexto-ufc/compat-nbr6023-2025.def` e deve ser reduzida quando o upstream fornecer suporte equivalente.

## Projetos de pesquisa

Os perfis `projeto` e `projetoanonimizado` adotam NBR 15287:2025. O perfil anonimizado é política do modelo para seleção/processos que exigem supressão de identificação; essa política não é apresentada como requisito ABNT geral.

## Artigo científico

O futuro runtime será uma baseline UFC para artigo em publicação periódica. Ele deve preservar a fronteira do próprio guia: instruções do periódico de destino continuam aplicáveis e podem impor requisitos adicionais/específicos.

B2B deverá implementar diferenças arquiteturais já identificadas, especialmente espaço simples, fluxo contínuo das seções primárias e paginação visível desde a primeira página conforme o contrato reconciliado.

## Build e gates

- `make preflight` — regressões coordenadas de PR;
- `make release-preflight` — regressões profundas incluindo PDF/A;
- Gate T — proxy público Overleaf + certificação Windows de fontes literais;
- `make distribution-preflight` — bundles determinísticos, hashes, licenças, CTAN smoke e Overleaf import.

O workflow `.github/workflows/latex-preflight.yml` está congelado pelo baseline N12 no blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

## Documentação e continuidade

A documentação ativa é parte do gate de release:

- `docs/HANDOFF-V2.2.0.md` — ponto canônico de retomada;
- `docs/VIGENCIA-NORMATIVA.md` — vigência/precedência;
- `docs/NAMING.md` — política de nomenclatura/API;
- `docs/B2R-NAMING-INVENTORY.md` — fase de naming ativa;
- `release/n15-b2r-a-naming-inventory.json` — ledger máquina-legível da fase.

Nenhuma fase deve ser marcada DONE se esses documentos estiverem incompatíveis com o estado real da branch, PR, CI ou próxima ação.

## Manutenção antes de release

1. reconfirmar fontes e edições vigentes;
2. revisar atos e páginas UFC relevantes;
3. atualizar contratos/locators somente com evidência adequada;
4. remover adaptações upstream obsoletas;
5. executar source contract, preflight, Gate T e Distribution no exact head;
6. verificar `behind_by=0` antes do merge;
7. sincronizar documentação antes e depois do merge/certificação;
8. somente então avançar a fase seguinte.

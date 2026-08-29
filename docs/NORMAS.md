# Base normativa da V2

Última revisão: **2026-08-29**.  
Estado do projeto: **v2.2.0 em auditoria N15; N15-B2R concluída e N15-B2B de artigo científico ativa**.

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
| Artigo em publicação periódica | **ABNT NBR 6022:2018** | contrato `article.*`; runtime N15-B2B em implementação/certificação |
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

N15-B2A/PR #145 promoveu:

- `abnt-nbr-6022-2018`;
- `ufc-guia-artigos-2022`;
- 13 predicados `article.*`;
- locators e metadados de fase correspondentes.

Depois do fechamento e recertificação integral de N15-B2R em `main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`, N15-B2B passou a implementar o runtime desse contrato em `abntexto-ufc/articles.def`.

O delta B2B é deliberadamente restrito: ativa `type=article` e `tipo=artigo`, reutiliza metadados/comandos já certificados e não modifica o `public-api.def` congelado. A evidência executável da implementação está em `tests/v2-article-check.sh` e `tests/checks/article_runtime_contract.py`; a promoção final de proof state pertence a N15-B2C.

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
├── compat-abntexto.def
├── bibliography.def
├── compat-nbr6023-2025.def
├── articles.def
├── backmatter.def
└── public-api.def
```

Os nomes antigos dos módulos foram removidos em B2R-A1/PR #146. O `public-api.def` B2R permanece congelado no blob `7b61fe70dd85ed895140f846272e097e3ded72cf`; o novo comportamento de artigo é isolado em `articles.def`. O `latex-preflight.yml` N12 permanece congelado no blob `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## Layout canônico do template

A superfície visível do projeto permanece:

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
| artigo científico | **runtime B2B implementado na branch; certificação pendente** | `coverage-rules-article.json`; `articles.def`; `v2-article-check.sh`; B2C ainda futuro |

A cobertura atômica não é duplicada manualmente aqui; consulte `normativa/atomic-rules.json`, coverage manifests, locator audit e proof-state artifacts.

## Tipografia

A API canônica v2.x usa, por exemplo:

```tex
\ufcsetup{
  font = times,
  strict-font = false
}
```

As formas portuguesas certificadas permanecem aceitas como compatibilidade aditiva.

Fallback portátil não equivale à certificação tipográfica literal. O Gate T Windows certifica Times New Roman e Arial literais, variantes, incorporação, Unicode e PDF/A-2b. Fontes Microsoft proprietárias não são redistribuídas.

## Citações e referências

Citações seguem NBR 10520:2023 no escopo implementado. Referências seguem NBR 6023:2025. Compatibilidade temporária necessária ao escopo testado fica isolada em `abntexto-ufc/compat-nbr6023-2025.def` e deve ser reduzida quando o upstream fornecer suporte equivalente.

## Projetos de pesquisa

Os perfis `projeto` e `projetoanonimizado` adotam NBR 15287:2025. O perfil anonimizado é política do modelo para seleção/processos que exigem supressão de identificação; essa política não é apresentada como requisito ABNT geral.

## Artigo científico — N15-B2B ACTIVE

O runtime é uma baseline UFC para artigo em publicação periódica. Instruções do periódico de destino continuam aplicáveis e podem impor requisitos adicionais/específicos.

O contrato B2A exige e B2B implementa no escopo automatizável:

- `type=article` com compatibilidade `tipo=artigo`;
- papel A4, margens 3 cm esquerda/superior e 2 cm direita/inferior;
- paginação arábica visível desde a primeira página, no canto superior direito;
- texto 12 pt, justificado, espaço simples e recuo de 2 cm na primeira linha;
- título na primeira página, seguido de autoria e datas de submissão/aprovação;
- resumo/palavras-chave e abstract/keywords no mesmo fluxo, sem folhas pré-textuais artificiais;
- Introdução, Desenvolvimento e Considerações finais numerados;
- seções primárias em fluxo contínuo, sem nova página automática;
- referências obrigatórias sem quebra automática de página antes do título;
- ausência de capa, folha de rosto, folha de aprovação e sumário separados para esse perfil.

A implementação não cria novos setup keys, comandos, ambientes ou hooks. `articles.def` especializa apenas comportamentos existentes quando o tipo ativo é artigo e mantém `layout.def` como proprietário das funções internas de quebra.

As recomendações de 150–250 palavras no resumo, pelo menos três palavras-chave e Arial/Times New Roman permanecem advisory, não hard errors.

## Build e gates

- `make preflight` — regressões coordenadas de PR;
- `make release-preflight` — regressões profundas incluindo PDF/A;
- Gate T — proxy público Overleaf + certificação Windows de fontes literais;
- `make distribution-preflight` — bundles determinísticos, hashes, licenças, CTAN smoke e Overleaf import.

O workflow `.github/workflows/latex-preflight.yml` está congelado pelo baseline N12 no blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

B2B integra a prova de artigo pela dependência do check `profiles` em `tests/run.py`, sem alterar o workflow congelado.

## Documentação e continuidade

A documentação ativa é parte do gate de release:

- `docs/HANDOFF-V2.2.0.md` — ponto canônico de retomada;
- `docs/VIGENCIA-NORMATIVA.md` — vigência/precedência;
- `docs/NAMING.md` — política de nomenclatura/API;
- `docs/B2R-NAMING-INVENTORY.md` — inventário histórico/final B2R;
- `release/n15-b2b-article-runtime.json` — ledger máquina-legível da fase ativa.

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

# Roadmap: exemplos científicos completos e pipeline escalonado — P0.12R

**Estado:** plano executável por evidência, não uma declaração de que v3.1.0
ou 28 PDFs estejam aprovados. Referência de rastreabilidade:
https://github.com/tiagosombrra/abntexto-ufc/issues/555

## Regras de projeto

**Uma fonte matemática, sete gêneros documentais, quatro idiomas.**
Os arquivos de dados, imagens, equações e referências procedem do estudo
canônico versionado; a argumentação, a profundidade e os elementos próprios
de cada modalidade permanecem independentes. Não aceitar números inventados,
citações bibliográficas sintéticas ou conclusões de desempenho sem ensaio real.

**Separar três produtos:**

- Documento acadêmico exemplar: fonte editável por tipo e idioma.
- Guia do usuário: configuração da classe, estrutura de pastas, exemplos,
  mensagens de erro, fontes UFC verificadas e capturas de saída.
- Corpus exaustivo de regressão: 28 perfis×idiomas, quatro variantes
  suplementares, alternativas de motor/fontes/duplex e R5 página por página.

**Não substituir validação por velocidade.** Documentos completos só recebem
ACCEPT após compilação no SHA exato, auditoria de conteúdo, paginação física,
metadados, tabelas, figuras, links e avaliação humana. Fonte compilada não é
resultado acadêmico cientificamente validado.

## Execução em quatro portas

| Porta | Quando | O que roda | Critério de aceitação |
|---|---|---|---|
| F0 — conteúdo | a cada commit de exemplo | gerador determinístico, fonte, idiomas, matemática, hashes e negativos | < 5 min no job; sem LaTeX |
| F1 — integração focal | PR com alterações de um módulo | Static contract, Linux integration em escopo selecionado por caminhos, smoke PDF do domínio | todos os required checks concluídos |
| F2 — corpus amplo | PR pronta para revisão, alteração de classe, candidato e execução manual | 28+4 PDFs em quatro jobs paralelos + recibos reais e negativos | zero FAIL no SHA exato; sem usar skip como sucesso |
| F3 — aceite/publicação | após F2 e integração na main | R5 de todas as páginas, revisão normativa, regressões motores/plataformas e verificação PDF/A externa | ACCEPT humano individual e autorização separada |

**Como tornar F0 realmente rápida:** Python stdlib, nenhum download de TeX,
nenhum Biber, apenas 3 grades estruturadas, 3 PDFs vetoriais gerados, 3 SVGs,
1 CSV, 4 seções traduzidas e um manifesto de SHA256. Recalcular cada byte e
reprovar um arquivo adulterado. Usar a infraestrutura existente
`tests/integration_suites.py` para selecionar `smoke` nos caminhos
`examples/canonical-mesh-study/`, `tools/examples/` e no teste específico.
Qualquer alteração simultânea em `abntexto-ufc.cls`, `standards/` ou release
continua a exigir `complete`. Linux integration e Static contract não são
desabilitados.

**Como reduzir F2 sem reduzir cobertura:** gerar fontes leves na etapa de
preflight; compilar PDFs somente quando a PR relevante estiver pronta ou por
disparo manual explícito; paralelizar por idioma; preservar .tex, .lot, .log,
.json, PDF, SHA e miniaturas mesmo na falha; evitar pré-compilações idênticas
em cada edição de prosa. O candidato final deve rodar F2 integralmente outra
vez; um artifact antigo não cobre um novo commit.

## Entregas e dependências

**E1 — concluída em código, aguarda CI:** `study.json`, script de geração,
dois DOIs verificados, três estudos geométricos verdadeiros, quatro idiomas,
figuras e CSV, teste negativo, workflow rápido.

**E2 — próxima mudança separada:** ligar a seção real ao gerador de sete
perfis; referenciar `examples/canonical-mesh-study/references.bib` com
Biber, substituir retângulos genéricos por malhas reais, produzir argumentos
específicos para graduação/especialização/mestrado/doutorado/projetos/artigo,
usar resultados calculados apenas onde o gênero admite resultados
realizados. Acompanhar se todas as 28 fontes foram geradas e contêm
conteúdo científico substancial. A matriz 28+4 existente deve continuar a
exercitar figuras, código, algoritmos, tabularray, longtable, glossário,
índice, páginas vazias e sumário.

**E3 — guia do usuário:** documentação independente com comandos completos,
pastas e erros frequentes, seções anotadas, imagens produzidas de verdade,
configurações de idioma, casos de projetos anonimizados e bibliografia real.
Revisar os modelos estruturais da Biblioteca UFC (Word/ODT/DOCX), sem copiar
seus textos ou inferir que modelos antigos substituem a norma mais recente.

**E4 — auditoria e publicação:** comparar PDFs por SHA, examinar todas as
páginas e variantes, identificar folhas de verso justificadas, confirmar
normas UFC/ABNT/IBGE aplicáveis, PDF/A com veraPDF, demais motores e
compatibilidade. Só então pedir aceite e autorização de release.

## Critérios contra falsa aprovação

- Fontes literárias são URLs/DOIs verificáveis, não um mock de testes legado.
- Um dado calculado deve coincidir em todas as línguas e modalidades;
  uma tabela alterada manualmente causa FAIL.
- Um projeto não apresenta resultados futuros como se executados; um artigo
  não herda elemento obrigatório de tese; um anonimizado não vaza autoria
  por PDF Info/XMP/outline/anexos.
- Cada elemento visual usa figura realmente derivada dos dados e possui
  legenda, origem e referência no texto.
- Nenhum relatório R4/R5 pode contar somente páginas com texto ou omitir
  páginas brancas sem justificativa normativa e inspeção.
- Todos os testes ficam vinculados a SHA e artefatos imutáveis.
- **v3.1.0 = UNRELEASED; publication_authorized=false.**

## Fontes UFC e literatura

- https://biblioteca.ufc.br/pt/servicos-e-produtos/templates/
- https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/
- Bommes et al. (2009), DOI 10.1145/1576246.1531383
- Shewchuk (2002), DOI 10.1016/S0925-7721(01)00047-5

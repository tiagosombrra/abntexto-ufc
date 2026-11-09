# R5 — triagem normativa de 300 folhas brancas e reconciliação das PRs

> **Status:** evidência técnica verificada em 07/11/2026, não aprovação normativa.  
> `v3.1.0 UNRELEASED`; `publication_authorized=false`.  
> Revisão humana de 1.364 páginas R4 e dos 28 exemplos E3: **PENDING**.

## Evidência original e algoritmo independente

A base é o corpus sintético de [GitHub Actions #42285583668](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/42285583668), compilado no SHA imutável
`934faec1e2d3c2670b4a791d0adcd8823c3c80a4`: quatro ZIPs PT/EN/ES/FR,
32 documentos (oito por idioma) e 1.364 páginas A4 (341 por idioma).

A triagem independente lê diretamente os quatro ZIPs **originais**, compara
cada SHA256 da fonte `.tex` e do PDF com `source-index.json` e
`pdf-receipts.json`, confere a presença de `\ufcPrintCover` na fonte,
classifica as páginas reais usando o texto selecionável e renderiza em escala
reduzida toda folha sem texto/objetos para verificar brancura.

Em **16 fontes configuradas `print-mode=double-sided`** foram observados
**300 versos brancos** (75 por idioma), 0 páginas de fólio isolado e
0 folhas brancas inesperadas. A capa externa ocupa a primeira página do PDF,
mas não é contada na parte interna. Logo, a correspondência verificada é:

| Índice físico no PDF | Significado na parte interna |
|---|---|
| 1 | Capa externa, fora da contagem |
| 2 | Primeiro anverso (página interna 1) |
| 3 | Primeiro verso (página interna 2) |
| 4 | Segundo anverso (página interna 3) |

**Todas as 300** folhas físicas ímpares brancas são **versos lógicos**,
seguidos de **anverso lógico não vazio**. A paridade é tecnicamente
coerente; **isso não prova que cada folha tenha de existir**.

## Destino da quebra de página

| Próximo elemento, depois do verso branco | Ocorrências | Norma principal a conferir |
|---|---:|---|
| Elementos pré-textuais (resumos, listas, sumário etc.) | 164 | NBR 14724:2024 / NBR 15287:2025 §5.1 |
| Folhas de aprovação | 12 | NBR 14724:2024 §4.2.1 e §5.1 |
| Seções primárias do texto | 68 | NBR 14724:2024 / NBR 15287:2025 §5.2.2 |
| Elementos pós-textuais (referências, anexos etc.) | 56 | UFC 2022 versus normas vigentes e modo digital |
| **Total** | **300** | **300 decisões humanas pendentes** |

**Escopo normativo por tipo de documento:** a **ABNT NBR 15287:2025**
é aplicável a projetos de pesquisa **com e sem anonimização**;
a **ABNT NBR 14724:2024**, com a versão corrigida em 2025, aplica-se
aos trabalhos acadêmicos dos demais perfis. A execução de referência
contabilizou **48 versos no projeto de pesquisa anonimizado**;
não se pode atribuir automaticamente os **252 versos restantes** a
dissertações, teses ou variantes doutorais sem separar os projetos
de pesquisa comuns. O auditor recalcula a distribuição por perfil
a partir de cada PDF/recibo original e compara as duas normas
antes de produzir a evidência, mantendo a decisão humana por página.
Nos 48 versos do projeto anonimizado, 16 antecedem pré-textuais,
20 antecedem seções primárias e 12 pós-textuais.

### Matriz de prioridade para decisão normativa

- **Elementos pré-textuais e seções primárias:** as NBRs vigentes
  indicam início no anverso da folha em impressão frente e verso.
  A coerência de cada transição foi verificada, mas o aceite humano
  deve confirmar se o elemento é aplicável e necessário ao perfil.
- **Pós-textuais (56 casos, dos quais 12 de projetos):** a UFC 2022
  indica início no anverso, enquanto NBR 14724:2024 e NBR 15287:2025
  recomendam uso de anverso e verso para textuais e pós-textuais.
  Não marcar como exigência automaticamente: submeter a decisão
  normativa atual ao SiBi-UFC/programa, com edição e regra registradas.
- **Depósito digital:** SiBi-UFC declara recebimento exclusivamente
  eletrônico de TCCs, dissertações e teses. Os exemplos públicos E3
  já são `single-sided` e passaram em 28/28 PDFs, 360 páginas A4.
  Não eliminar silenciosamente os versos das fixtures duplex R4:
  são configurações distintas e devem permanecer testadas.

Fontes de referência verificadas em 07/11/2026:
- [ABNT NBR 14724:2024, versão corrigida 2025](https://funesa.se.gov.br/wp-content/uploads/2025/06/TRABALHOS-ACADEMICOS.pdf), §§5.1, 5.2.2, 5.3;
- [ABNT NBR 15287:2025](https://universidadeniltonlins.com.br/wp-content/uploads/2025/06/NBR-15287_2025_Projeto-de-pesquisa.pdf), §§5.1, 5.2.2, 5.3;
- [Guia UFC 2022](https://biblioteca.ufc.br/wp-content/uploads/2022/05/guianormalizacaotrabalhosacademicos-17.05.2022.pdf), §4.1(e), **fonte histórica**, não substitui normas posteriores;
- [SiBi-UFC: recebimento eletrônico](https://biblioteca.ufc.br/pt/servicos-e-produtos/recebimento-e-divulgacao-de-dissertacoes-teses-e-tccs/), política institucional de depósito;
- [SiBi-UFC: ficha catalográfica em 2026](https://biblioteca.ufc.br/pt/perguntas-frequentes/ficha-catalografica-2/), alteração de obrigatoriedade da representação visual.

## Reconciliação serializada das PRs

O estado do GitHub em 07/11/2026 é **main**
`5d7cb996778bd9724b39f7ec01a7be09c7cfa5d7` (não alterada).
Há colisão comprovada de arquivos entre ramos independentes:

- `abntexto-ufc.cls`: **#563, #565, #566, #568 e #575**;
- `standards/evidence/test-surface-policy.json`: **#563, #566, #568, #573, #574, #575 e #576**;
- scripts PDF/metadata: #563, #566 e #568;
- arquivos do exemplo público: #574 e #575.

**Diferencial técnico do class file:** o HEAD da #568 já contém
`hyperref`, metadados Info/XMP e `Tabla`/`Tableau`, mas **não contém
todos os ajustes visuais da #566**: líder pontilhado sem espaçamento
duplo, ajuste de banca para 1,5 e cálculo adaptativo de espaçamento.
Esse déficit foi confirmado por comparação de linhas contra a
classe da #575. Portanto, **merge direto da #568 seria uma regressão
visual conhecida** mesmo que a matriz sintética anterior passe.

Sequência indicada, **não execução automática**:

1. Integrar/revalidar **#563**, com política de anonimização e bookmarks
   e seus próprios testes de metadados; confirmar branch atualizado.
2. Integrar/revalidar **#566**, retendo somente alterações ainda não
   presentes na main e preservando a melhoria visual; não reaplicar
   integralmente commits empilhados da #563.
3. Aplicar/revalidar **#565** como alteração delimitada da classe após
   a revisão visual, com teste de troca Babel ES/FR.
4. Desempilhar e rebasear **#568** sobre as alterações aceitas, trazendo
   o R4 e estudos matemáticos, **sem sobrescrever** as correções da classe
   nem os testes recém-aceitos.
5. Reconciliar **#574** (fontes acadêmicas editáveis) com o gerador
   e exemplos de #568; usar a #575 **apenas como prova diagnóstica**,
   não como PR a mesclar.
6. Integrar os controles **#573** (R5) e **#576** (veraPDF) com
   `test-surface-policy.json` consolidado. Não perder nenhum owner de CI.
7. Executar a matriz 32 PDFs sintéticos, a matriz 28 PDFs públicos,
   veraPDF, testes de metadados/legendas, checks negativos, revisões
   visuais e gate humano R5 **sobre o SHA final único da main**.

Nenhum merge/rebase foi efetuado por esta documentação. A PR #575 permanece
diagnóstica, a #576 continua draft, e a publicação da v3.1.0 segue bloqueada.

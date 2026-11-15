# R8.1 — diagnóstico controlado e correção de paginação da tabela nativa

**Estado:** defeito reproduzido no corpus original; correção editorial integrada na [PR #594](https://github.com/tiagosombrra/abntexto-ufc/pull/594) (merge `83dbaa6d1b3e6f431509c6b1bfaeb7b481044f0b`). Há recompilação e aceite **editorial/visual global delimitado** de 28 PDFs R5 posteriores, sob outro SHA e corpus de 80 linhas ([recibo do mantenedor](https://github.com/tiagosombrra/abntexto-ufc/pull/592#issuecomment-6868188102)); revisão individual por página e homologação normativa/institucional seguem pendentes.

## Evidência imutável da R8.1

- Fonte original: `a4a4665ce099d0786e92e443b95dab656b25afad`.
- Corpus: [workflow #43452221682](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/43452221682): **28 PDFs, 984 páginas**, todos com revisão humana pendente.
- Auditoria independente dos bytes originais: [workflow #43484875024](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/43484875024); checagem de 7 PDFs por idioma, hashes dos PDFs e 984 páginas físicas.
- Resultado: a tabela **nativa** `longtable` possui apenas a **linha de dados 85** na sua última página nos seis documentos de inglês e seis de espanhol que não são artigo científico (**12/28**). Nos mesmos seis perfis em português e francês, a última página da tabela contém **21 linhas de dados**. Artigos científicos não apresentam o mesmo padrão.
- O outro ambiente `longabnttblr` não produziu última página de uma única linha na matriz; porém, a extração textual de **todas as 125 linhas** desse ambiente foi inconclusiva no auditor independente. Não utilizar essa extração como prova de completude dos dados dessa tabela; conferir fonte e PDF separadamente.

## Hipótese isolada e correção integrada

O gerador R4 constrói o `longtable` nativo com 85 linhas e cabeçalhos repetidos. A quebra automática de página pode deixar apenas a última linha de dados sob o cabeçalho, conforme o espaço disponível em cada idioma.

Em `tests/integration/frontmatter/generate-comprehensive-corpus.py`, a correção **apenas editorial** coloca `\nopagebreak[4]` imediatamente após a linha 84, mantendo as últimas duas linhas juntas na paginação natural do `longtable`. Não altera `abntexto-ufc.cls`, opções públicas nem os documentos R8.1 originais.

O auditor de PDFs gerados `tools/review/build_readable_28.py` agora verifica a presença das 85 linhas por idioma e rejeita o padrão de última página com apenas a linha 85, independentemente de compilação ou aprovação normativa.

## Experimentos controlados

O runner `tools/review/r81_controlled_pagination.py` produz **12 PDFs reais**:

1. **Conteúdo idêntico** nos quatro idiomas, mudando apenas `\DocumentMetadata{lang=...}` e a configuração `document-language`.
2. **Texto traduzido realmente utilizado pelo corpus**, por meio de `PROSE` e `STRINGS` dos geradores, mantendo as 85 linhas e a estrutura do `longtable`.
3. **Texto traduzido com proteção de quebra** após a linha 84, controle positivo da correção incorporada ao gerador.

Todos os PDFs carregam marcadores invariantes `R81ROW001`–`R81ROW085`. O workflow `.github/workflows/r81-controlled-pagination.yml` mantém `report.json`, 12 fontes, PDFs e logs sem publicar nem modificar os originais. O job independente `original-pdfs-audit` baixa os quatro ZIPs da R8.1, confere o commit original e audita a paginação nativa de cada PDF.

## Gates de conclusão

- A PR #594, que adicionou a guarda editorial de quebra e o teste negativo para a última linha órfã, foi **integrada**; manter seus resultados dos 12 PDFs controlados associados às respectivas execuções e SHA, sem generalizá-los a outro corpus.
- A matriz editorial R5 de 28 PDFs foi recompilada na [execução #43519592856](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/43519592856), com **972 páginas** e tabela editorial de **80 linhas**, e recebeu [aceite editorial/visual global delimitado](https://github.com/tiagosombrra/abntexto-ufc/pull/592#issuecomment-6868188102). Esse conjunto não substitui a verificação separada do corpus R4 de **85 linhas**.
- Preservar a identidade e os hashes dos artefatos anteriores (984 páginas) e dos novos (972 páginas); verificar integridade, layout, PDF/A-2b e regressões por fonte real, sem transferir aceite entre bytes diferentes.
- A revisão por página, a revisão normativa/linguística formal e a homologação institucional permanecem pendentes. CI verde e aceite global editorial não constituem autorização de release.

**Não confundir** correção da amostra de documentação com correção do runtime. A classe comum não apresentou causa raiz demonstrada neste defeito.

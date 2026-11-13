# R8.1 — diagnóstico controlado de paginação de tabelas

**Estado:** experimento técnico; não é homologação normativa nem aprovação visual.

## Fonte da auditoria

- Corpus original de 28 PDFs da R8.1: GitHub Actions [run #43452221682](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/43452221682), commit `a4a4665ce099d0786e92e443b95dab656b25afad`.
- Os originais são imutáveis; o diagnóstico NÃO substitui os 984 julgamentos humanos pendentes.
- Diagnóstico independente: `.github/workflows/r81-controlled-pagination.yml`, com execução de `tools/review/r81_controlled_pagination.py`.

## Experimentos

1. **Conteúdo constante, idioma variável:** quatro compilados PT/EN/ES/FR com o mesmo corpo, rótulos das linhas e sequência numérica, mudando apenas a configuração de idioma e os metadados linguísticos.
2. **Texto traduzido:** quatro compilados com o mesmo número de linhas e a mesma estrutura de tabela, mas rótulos e texto anterior diferentes em cada idioma.
3. As 125 linhas da tabela recebem identificadores `R81ROW001` a `R81ROW125`; extração física por página verifica linhas ausentes/duplicadas e distribuição na página final.
4. A ocorrência de uma única linha na última página é classificada como **candidata de revisão visual**, nunca como infração normativa provada apenas por texto extraído.

O relatório `artifacts/r81-controlled-pagination/report.json`, os oito PDFs, fontes TeX e logs são retidos pelo workflow como evidência de compilação real. Para repetir:

```bash
python3 tools/review/r81_controlled_pagination.py
```

Pré-requisitos: TeX Live com `pdflatex`, `abntexto-ufc.cls` local e Poppler `pdftotext`.

## Critérios para conclusão

- Diagnóstico real dos quatro idiomas, com saída auditável; nenhum teste pode tratar erro de compilação como diferença de idioma.
- Confrontar original inglês/espanhol e controles português/francês por **mesma tabela e mesmo perfil**, nas páginas físicas dos PDFs originais.
- Se a origem for o gerador editorial, corrigir o gerador (não a classe). Se for o ambiente da classe, corrigir o runtime comum com regressão dos quatro idiomas.
- Recompilar 28 documentos e auditar paginação e regressões com SHA de fonte e novos PDFs, mantendo R8.1 original intacta.
- A eventual aprovação humana continua independente e não pode ser inferida a partir de CI verde.

**Não declarar causa definitiva ou defeito resolvido até confrontar os PDFs originais.**

# R5 — auditoria independente dos artefatos PDF (#572)

**Situação: pré-auditoria automatizada; NÃO homologado.** A versão 3.1.0
permanece sem autorização de publicação.

## Dois produtos distintos

O corpus R4 contém 28 perfis × idiomas e quatro variantes suplementares,
com identificadores sintéticos deliberados (por exemplo,
`INTEGRATED-MANUSCRIPT` e `R4-METHOD-PT`). Esses arquivos são *fixtures*
de regressão e **não devem ser distribuídos como exemplos acadêmicos finais**.

A fonte matemática em `examples/canonical-mesh-study/` contém métricas,
bibliografia e figuras reprodutíveis. A existência de resultados corretos
não substitui uma revisão editorial dos documentos inteiros.

## Execução local

Instale a dependência com `python3 -m pip install pymupdf==1.26.5`.
Depois execute `python3 tools/audit_r5_artifacts.py --self-test`.

Baixe os quatro ZIPs originais de **uma única execução** do workflow R4.
Sem modificar ou recomprimir os arquivos, execute:

```bash
python3 tools/audit_r5_artifacts.py \
  --artifact artifacts/r4-pt.zip \
  --artifact artifacts/r4-en.zip \
  --artifact artifacts/r4-es.zip \
  --artifact artifacts/r4-fr.zip \
  --output artifacts/r5-independent
```

Os caminhos acima são nomes ilustrativos para arquivos locais; o programa
não realiza downloads de GitHub. Ele verifica:

- 32 PDFs vinculados ao mesmo commit e 32 recibos;
- SHA256 do PDF e da fonte TeX contra os recibos existentes;
- páginas reais, papel A4 e ausência de autoria no PDF anônimo;
- divergências entre páginas sem texto e recibos fornecidos pelo CI;
- conteúdos rasterizados das folhas sem texto.

A saída é `inventory.json`, `pages.csv` e `gate.json`, sempre com
`publication_authorized=false`.

## Política de páginas em branco

`DUPLEX_VERSO_CANDIDATE` indica folha fisicamente branca cuja posição é
compatível com um verso não impresso em documento com capa externa e
`print-mode=double-sided`. **A classificação NÃO declara conformidade
ABNT/UFC.** Exige análise e fundamentação normativa **para cada folha**.

`UNEXPLAINED_BLANK` e `NUMBER_ONLY` são eventos que bloqueiam aceite.
`NO_EXTRACTABLE_TEXT` exige inspeção de imagens e recursos de página.
O auditor nunca aprova automaticamente uma página.

## Decisões humanas

O JSON opcional de revisão deve ter `source_commit_sha`, `reviewer` e
`documents`. Cada documento é indexado pelo nome do PDF e informa seu
`sha256`, além de um mapa `pages` com chaves `"1"`, `"2"`, etc.
Cada página exige `status` igual a `ACCEPT`, `NEEDS_CHANGES` ou
`REJECT`. Toda página vazia precisa do campo `normative_justification`
com fundamentação específica.

Execute com `--reviews revisao.json --require-r5-approval` para exigir
todas as páginas aceitas e justificadas. Um `REJECT`, uma página pendente,
uma justificativa ausente ou um hash divergente impede aprovação. **Os atuais
PDFs R4 também são bloqueados por seus marcadores sintéticos**, mesmo após
decisões positivas: eles não são modelos finais publicáveis.

O auditor não concede autorização para tag, Release, CTAN nem certificação
PDF/A ou PDF/UA. Esses pontos exigem portas de aprovação separadas.

## Fonte e resultados observados

Execução [42285583668](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/42285583668)
no commit `934faec1e2d3c2670b4a791d0adcd8823c3c80a4`:
32 PDFs, 1.364 páginas A4, 300 folhas vazias candidatas a versos duplex,
zero folhas vazias fora desse padrão e zero páginas com somente número.
**Todas as 1.364 páginas ainda exigem revisão editorial humana**, sem
inferir aceitação apenas da compilação.

Etapas seguintes: exemplos editáveis sem marcadores de regressão (#569/#570),
revisão R5 por página (#572), reconciliação #563/#565/#566/#568 e
revalidação do SHA final. Issue principal: #555.

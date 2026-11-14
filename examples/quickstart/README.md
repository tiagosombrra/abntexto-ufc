# Exemplos mínimos executáveis — v3.1.0 em desenvolvimento

Este conjunto contém quatro **fontes TeX autocontidas**, com o perfil de projeto de pesquisa, uma por idioma. Os arquivos são exclusivamente exemplos didáticos da linha v3.1.0 **não publicada**; não são documentos homologados pela UFC/ABNT nem fazem parte dos bundles públicos v3.0.5.

| Idioma | Fonte | `document-language` | `DocumentMetadata.lang` |
|---|---|---|---|
| Português | [pt.tex](pt.tex) | `pt` | `pt-BR` |
| Inglês | [en.tex](en.tex) | `en` | `en-US` |
| Espanhol | [es.tex](es.tex) | `es` | `es-ES` |
| Francês | [fr.tex](fr.tex) | `fr` | `fr-FR` |

Todos usam `cover=false`, `coat-of-arms=false` e `catalog-card=false`, evitando ativos externos. Os rótulos automáticos são configurados pelo idioma de documento; prosa acadêmica, nomes de instituições, programas e dados do autor nunca são traduzidos automaticamente.

## Compilação a partir da raiz do repositório

~~~bash
for loc in pt en es fr; do
  mkdir -p "artifacts/quickstart/$loc"
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="artifacts/quickstart/$loc" \
    "examples/quickstart/$loc.tex"
done
~~~

O teste [P0.9 four-language executable quickstarts](../../.github/workflows/p09-quickstart-four-languages.yml) compila cada fonte no TeX Live 2026, verifica texto e `/Lang` do PDF e retém os binários e hashes por SHA. Esta prova funcional limitada não substitui as matrizes R4/R5, a auditoria linguística nem a revisão normativa e editorial humana. Para trabalhos completos, use [o guia do usuário](../../docs/USER-GUIDE.md).

# Web/Lite validator

The tracked `validator/` directory is the static Web/Lite application source. It processes selected PDF bytes in the browser; the application does not upload the PDF to a project server.

## Local/static use

Serve this directory over HTTP, for example:

```bash
python3 -m http.server 8000 --directory validator
```

Then open `http://localhost:8000/`. The application loads the pinned PDF.js 6.2.108 browser modules from the tracked `validator/vendor/pdfjs/` tree. The validator runtime does not require a CDN; PDF analysis remains local in the browser.

`validator/index.html` enforces a bounded Content Security Policy: scripts, workers and connections are same-origin only; objects, frames, base-URL changes and form submissions are denied. The only `unsafe-inline` allowance is for the single tracked CSS block; Static rejects additional style attributes, inline scripts and inline event handlers.

## Vendored PDF.js

The browser runtime pins **PDF.js / pdfjs-dist 6.2.108** under [`vendor/pdfjs/`](vendor/pdfjs/).

- `pdf.mjs` and `pdf.worker.mjs` are imported byte-for-byte from the official Mozilla PDF.js `v6.2.108` generic distribution;
- `PROVENANCE.json` records the upstream tag commit, GitHub release/asset identifiers, release-asset SHA-256 and the exact hashes/sizes of the tracked runtime files;
- `LICENSE` is the upstream Apache License 2.0 text;
- vendored runtime files are generated upstream and must not be edited manually.

The main module and worker are kept at the same pinned version. Dependency updates must import a verified official release and update the fail-closed source contract together; there is no CDN fallback.

## Normative catalog

`validator/normative-catalog.js` is generated from the authoritative `standards/catalog/catalog.json` plus `standards/catalog/precedence.json`:

```bash
python3 tools/normative_catalog.py --emit-web validator/normative-catalog.js
```

Do not edit the generated module manually. `tests/checks/validator/validator_source.py` regenerates it independently and requires byte-for-byte identity, validates JavaScript syntax and fails if any relative browser import is missing.

## Idioma da interface (pt-BR) — v3.1.0 em desenvolvimento

O site principal e o Web/Lite usam **português brasileiro** por padrão (`<html lang="pt-BR">`). Títulos, identificação dos sete perfis, três modos de validação, ações, filtros, contadores, resultado visual e legendas de situação aparecem em português. Os rótulos visuais são `Aprovado`, `Falha`, `Aviso`, `Revisão manual` e `Não aplicável`; o resultado geral diferencia aprovação com ressalvas de uma certificação normativa integral.

**Somente apresentação:** os valores dos sete tipos de documentos, dos três modos de validação, dos quatro filtros e os estados de máquina (`PASS`, `FAIL`, `WARNING`, `MANUAL REVIEW`, `NOT APPLICABLE`) **não mudaram**. O relatório JavaScript e os arquivos JSON/CSV exportados continuam contendo todos os resultados e o esquema original; os textos explicativos originados das verificações técnicas e os títulos de fontes podem permanecer no idioma de origem para garantir rastreabilidade. A interface não traduz automaticamente o idioma do PDF, as cláusulas ABNT/UFC nem a API de `labels-language` do LaTeX.

O aviso de privacidade continua explícito: o PDF é analisado **localmente e não é enviado a um servidor**. A regra do Pages builder e os testes estáticos verificam a divulgação em português, os imports locais de PDF.js e a CSP intacta. O E2E produtivo em Chromium verifica `html.lang=pt-BR`, textos e rótulos acessíveis dos controles, enumerações de valores estáveis, mapeamento visual dos estados, contagem de filtros, relatórios completos e resultado negativo para PDF fora de A4. Ele também exige zero HTTP externo e nenhuma violação da CSP.

O Web/Lite é uma avaliação automatizada parcial, **não uma homologação oficial da UFC**. PDF/A profunda, incorporação de fontes e conclusões que exigem julgamento humano permanecem sinalizadas para revisão manual.

## Result review and filters (v3.1.0 development)

After running Web/Lite on a PDF, use **Show checks** to review either the full result, **Requires attention** (FAIL, WARNING, MANUAL REVIEW), **Failures only**, or **Manual review only**. The accessible counter shows the visible subset and total. Running a new PDF analysis automatically restores **All checks**, so a prior selection cannot conceal failures in the next report.

Filters **only hide or reveal rows in the browser table**. They do not change the checks array, verdict, mandatory/optional distinction, normative sources or `normative_rule` provenance, source `proof_state`, or data downloaded through **Export JSON** / **Export CSV**. Exports still contain **all** checks even when a filtered view is selected. In particular, Deep-only PDF/A and font embedding evaluations remain MANUAL REVIEW, not PASS.

The productive browser E2E exercises each filter against both an actual valid class PDF and the controlled invalid non-A4 PDF, checks visible row statuses and counter against the canonical report, verifies report completeness and the new-analysis reset. This is an interface/accessibility enhancement, **not** a stronger ABNT/UFC/IBGE compliance claim or a change to PDF/UA support.

## Browser regression

The Linux Integration `web-lite` scope compiles a real reference PDF, assembles the same `_site/validator` tree used by GitHub Pages, opens that productive package in headless Chrome, selects/uploads the PDF and runs the same `analyze` path used by the button. It then repeats the UI flow with a valid non-A4 negative PDF.

On a Web/Lite-only PR, the scoped TeX integration suite must explicitly prepare the canonical reference PDF, the six non-article profile PDFs (feeding five genuine positive/negative document-type artifacts) and two class-rendered duplex-margin PDFs **before** the browser stage. This is selected as `validator-source`, `web-lite-positive`, `profiles`, and `pdf-geometry` with their real dependencies; it is not a synthetic test fixture or an exemption. The static CI contract fails if those prerequisites are removed. On a `main` push the full 42-check suite is still mandatory.

The browser is run behind a loopback deny proxy with external DNS/background network disabled. Performance logs must show zero HTTP(S) requests outside the local test origin, and browser logs must show zero CSP violations. This proves that page load and both PDF analyses do not require external network access; there is no CDN fallback.

The E2E requires Web/Lite to keep Deep-only `font.embedded` and `pdfa.deep` in `MANUAL REVIEW`; only CLI/Deep may certify those checks automatically.

For local reproduction after a canonical/reference PDF exists, assemble the Pages package and run the same browser harness explicitly:

```bash
sh tools/ci/build-pages-site.sh
python3 tests/integration/validator/web-lite-e2e.py \
  --pdf artifacts/validation/web-lite-positive.pdf \
  --profile portable \
  --site-root _site/validator \
  --evidence /tmp/abntexto-ufc-web-lite/web-lite-e2e.json
```

The harness requires Chrome/Chromium plus a compatible `chromedriver`. It writes the JSON evidence next to a verbose `web-lite-chromedriver.log`; both should be retained when diagnosing a browser-startup failure. In CI, the `web-lite` Linux Integration scope owns this execution and stores host-side evidence under `runner.temp`.

The repository tracks `.github/workflows/pages.yml` to publish `site/` together with this `validator/` tree from canonical `main`. The Pages workflow owns deployment evidence, while the Linux Integration `web-lite` scope owns browser-level regression of the productive validator UI.

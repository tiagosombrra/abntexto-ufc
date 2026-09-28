# Web/Lite validator

The tracked `validator/` directory is the static Web/Lite application source. It processes selected PDF bytes in the browser; the application does not upload the PDF to a project server.

## Local/static use

Serve this directory over HTTP, for example:

```bash
python3 -m http.server 8000 --directory validator
```

Then open `http://localhost:8000/`. The application loads the pinned PDF.js 6.2.108 browser modules from the tracked `validator/vendor/pdfjs/` tree. The validator runtime does not require a CDN; PDF analysis remains local in the browser.

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

## Browser regression

The Linux Integration `web-lite` scope compiles a real reference PDF, preserves a stable snapshot, opens the productive `validator/index.html` UI in headless Chrome, selects/uploads the PDF and runs the same `analyze` path used by the button. It then repeats the UI flow with a valid non-A4 negative PDF.

The E2E requires Web/Lite to keep Deep-only `font.embedded` and `pdfa.deep` in `MANUAL REVIEW`; only CLI/Deep may certify those checks automatically.

For local reproduction after a canonical/reference PDF exists, run the same browser harness explicitly:

```bash
python3 tests/integration/validator/web-lite-e2e.py \
  --pdf artifacts/validation/web-lite-positive.pdf \
  --profile portable \
  --evidence /tmp/abntexto-ufc-web-lite/web-lite-e2e.json
```

The harness requires Chrome/Chromium plus a compatible `chromedriver`. It writes the JSON evidence next to a verbose `web-lite-chromedriver.log`; both should be retained when diagnosing a browser-startup failure. In CI, the `web-lite` Linux Integration scope owns this execution and stores host-side evidence under `runner.temp`.

The repository tracks `.github/workflows/pages.yml` to publish `site/` together with this `validator/` tree from canonical `main`. The Pages workflow owns deployment evidence, while the Linux Integration `web-lite` scope owns browser-level regression of the productive validator UI.

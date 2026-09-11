# Web/Lite validator

The tracked `validator/` directory is the static Web/Lite application source. It processes selected PDF bytes in the browser; the application does not upload the PDF to a project server.

## Local/static use

Serve this directory over HTTP, for example:

```bash
python3 -m http.server 8000 --directory validator
```

Then open `http://localhost:8000/`. The application loads the pinned PDF.js 6.2.108 browser modules from jsDelivr, so first load requires network access to that CDN. PDF analysis itself remains local in the browser.

## Normative catalog

`validator/normative-catalog.js` is generated from the authoritative `standards/catalog.json` plus `standards/precedence.json`:

```bash
python3 tools/normative_catalog.py --emit-web validator/normative-catalog.js
```

Do not edit the generated module manually. `tests/checks/validator_source.py` regenerates it independently and requires byte-for-byte identity, validates JavaScript syntax and fails if any relative browser import is missing.

## Browser regression

The Linux Integration `web-lite` scope compiles a real reference PDF, preserves a stable snapshot, opens the productive `validator/index.html` UI in headless Chrome, selects/uploads the PDF and runs the same `analyze` path used by the button. It then repeats the UI flow with a valid non-A4 negative PDF.

The E2E requires Web/Lite to keep Deep-only `font.embedded` and `pdfa.deep` in `MANUAL REVIEW`; only CLI/Deep may certify those checks automatically.

For local reproduction after a canonical/reference PDF exists, run the same browser harness explicitly:

```bash
python3 tests/integration/web-lite-e2e.py \
  --pdf artifacts/validation/web-lite-positive.pdf \
  --profile portable \
  --evidence /tmp/abntexto-ufc-web-lite/web-lite-e2e.json
```

The harness requires Chrome/Chromium plus a compatible `chromedriver`. It writes the JSON evidence next to a verbose `web-lite-chromedriver.log`; both should be retained when diagnosing a browser-startup failure. In CI, the `web-lite` Linux Integration scope owns this execution and stores host-side evidence under `runner.temp`.

This repository does not currently contain evidence that a public GitHub Pages deployment is configured. A static-tree/browser PASS is not a claim of public hosting.

# Vendored PDF.js runtime

This directory contains the browser runtime used by the Web/Lite validator.

## Pinned upstream release

- Component: PDF.js / `pdfjs-dist`
- Version: `6.2.108`
- Upstream repository: `mozilla/pdf.js`
- Tag: `v6.2.108`
- Tag commit: `0365cbde028bd92e58f2dab1bb70cd30ac7acfd7`
- GitHub release ID: `361333612`
- Distribution asset: `pdfjs-6.2.108-dist.zip`
- Asset ID: `493114690`
- Asset SHA-256: `7bf642d59582b475e8c48447da9b02b0108fad9742d7c2a35cb4ed6dd45e95ba`
- License: Apache-2.0

The tracked `pdf.mjs`, `pdf.worker.mjs` and `LICENSE` files were copied byte-for-byte from that verified official generic distribution. Their exact byte counts and SHA-256 values are recorded in `PROVENANCE.json` and independently pinned by `tests/checks/validator/validator_source.py`.

Do not edit generated vendor files manually. To update PDF.js, import and verify a new official release asset, keep the main module and worker on the exact same version, update provenance, and run the full Web/Lite validation path.

There is no runtime CDN fallback.

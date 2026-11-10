# R5: 28 readable manuscript PDFs for editorial review

This separate review corpus contains **seven document types per locale** (PT, EN, ES, FR), exactly 28 TeX sources and 28 compiled PDFs. It is deliberately separate from the R4 marker-based integration suite.

- `tools/review/generate_readable_28.py` generates natural-language titles, scientific paragraphs, front matter, captions, and metadata in all four languages while reusing the verified canonical structured-mesh study. The original R4 test corpus remains intact.
- `tools/review/build_readable_28.py` compiles the actual class under TeX Live 2026, runs Biber, generates the doctoral glossary and index, checks real PDF text for escaped test markers, checks that institutional covers contain an embedded coat-of-arms image, and preserves individual source/PDF SHA256 receipts.
- `.github/workflows/r5-human-readable-28.yml` builds seven documents per locale, archives the editorial source/PDF receipts, and then runs a dependent external PDF/A-2b validation job over the exact 28 completed PDF binaries from **the same source SHA and GitHub Actions run**. The workflow never grants release or human approval.
- `tools/review/verify_final_pdfa_28.py` is the fail-closed owner of the final-PDF verification stage: it checks four locales, seven profiles each, exactly 984 pages, TeX/PDF SHA256 receipts, the byte-identical accepted R8.1 class Git blob, and actual PDF page counts. It independently parses all 28 official veraPDF raw PDF/A-2b reports, preserves validator Docker image digests and rule failures, and rejects a missing/abnormal/nonconforming result. This certifies PDF/A-2b only; ABNT/UFC, PDF/UA, visual/human approval, and version publication remain separate.

This corpus **does not certify ABNT/UFC conformity**. Anonymous proposals do not embed an identifying institutional crest; journal articles do not have an institutional cover. The doctoral sample includes glossary and index; the optional listing/algorithm lists are exercised in other document types because pdfLaTeX's available write streams limit simultaneous auxiliary outputs.

Exact reproducibility: run `python3 tools/review/build_readable_28.py --locale pt` (or en/es/fr) in a TeX Live 2026 environment with `pdflatex`, `biber`, `makeglossaries`, `makeindex`, Poppler, and the repository's original assets. All outcomes remain `human_visual_approval=PENDING` and `release_authorized=false`.

The review pack shown to the user should contain **only the 28 PDFs**, in four locale directories. Technical CI logs and receipts are not part of that user-facing ZIP.

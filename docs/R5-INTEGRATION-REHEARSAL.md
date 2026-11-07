# Diagnostic-only R5 consolidation rehearsal (2026-11-07)

This is a **synthetic file-tree composition for CI**, not a Git merge, not an
authorization to merge any PR and not a publishable release.

Base main SHA: `5d7cb996778bd9724b39f7ec01a7be09c7cfa5d7`.

Source precedence, with exact reviewed commits:
1. R4 full multilingual corpus [#568](https://github.com/tiagosombrra/abntexto-ufc/pull/568): `934faec1e2d3c2670b4a791d0adcd8823c3c80a4`.
2. Retain additional visual documentation/example chapter changes [#566](https://github.com/tiagosombrra/abntexto-ufc/pull/566): `70a6a38ef20d3d64ef4a787c229a5ed8364ccd9d`.
3. Fully composed class plus 28 public examples [#575](https://github.com/tiagosombrra/abntexto-ufc/pull/575): `1ac95dd4bcdef08e3a469469b7fdcf8d0b8f8232`; its `abntexto-ufc.cls` includes #563 metadata, #565 Babel captions and #566 layout/committee fixes.
4. Independent R5 human gate and historical 300-blank replay [#573](https://github.com/tiagosombrra/abntexto-ufc/pull/573): `cf6f2d7573d0fd234f35d548bb3f5107b48e8313`.
5. External original-PDF veraPDF/A-2b gate [#576](https://github.com/tiagosombrra/abntexto-ufc/pull/576): `a3323c49c0885451d88dfe33a6e2de9ba2e2bff2`.

`standards/evidence/test-surface-policy.json` is a deterministic union
of unique registered standalone checks, dynamic assets and workflow
owners. Nothing in this branch should bypass CI or change protected main.

A green compilation on this tree does not prove a clean serial merge.
Before any merge, human review must inspect the actual inter-PR diffs,
rebase against current main, rerun the same matrix on that SHA, and
record page-by-page normative approval. R4 synthetic fixtures are never
user-facing examples. `v3.1.0 UNRELEASED`;
`publication_authorized=false`.

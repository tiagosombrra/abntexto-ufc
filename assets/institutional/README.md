# Institutional assets

This directory contains institutional visual assets used by supported GitHub user bundles.

## UFC coat of arms

`ufc-coat-of-arms.png` is treated as an institutional mark, not as project source code.

It is **not covered by the project's LPPL license**. Nothing in this repository grants independent trademark, brand or institutional-mark rights beyond the permissions that may already apply to an authorized user.

## Distribution policy

Current project policy is explicit:

- Template bundle: include the institutional PNG used by the canonical tutorial;
- Overleaf bundle: include the same institutional PNG;
- CTAN package: do **not** redistribute the institutional mark;
- proprietary Microsoft font files: do not redistribute on any surface.

The canonical Template/Overleaf tutorial uses `coat-of-arms=true`. The CTAN example uses `coat-of-arms=false`.

Tests enforce this surface-specific contract.

## Maintenance

Do not replace, rename, recompress or add institutional assets casually. A change to an institutional asset affects public bundle identity, visual output and distribution policy and therefore requires the corresponding integration/release validation.

For the current distribution architecture, see `docs/ARCHITECTURE.md` and `docs/CTAN-RELEASE.md`.

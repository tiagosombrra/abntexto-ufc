# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- R2-A entry checkpoint on `main`: `0a2c2c3879986ca27b731f54b974db12524258df`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B1 — canonical setup and internal state vocabulary**.
- Active implementation issue: **#234**.
- R2-A inventory issue #232: **DONE through the ownership inventory and closeout PR #235**.
- V3-R1 / R1-B8: **DONE**; issue #227 closed completed.
- Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and `release/v3-api-migration.json` must agree. Disagreement fails closed.

## Stable foundation

All R1 structural, distribution, static-gate, permanent-workflow and Windows/literal-font/PDF-A certification blocks are complete. Permanent validation remains `make static-check`, `make check`, and `make release-check`, orchestrated by `Static contract`, `Linux integration`, and `Linux release check`.

The final R1→R2 PR #233 passed `Static contract` run `33656361564` and `Linux integration` run `33656361474` (`PASS=30 FAIL=0 SKIP=0`) before merging at `0a2c2c3879986ca27b731f54b974db12524258df`.

## R2-A result

The ownership inventory is recorded in `docs/R2-API-OWNERSHIP.md`.

Key findings:

- `public-api.def` is loaded last and forwards canonical English surfaces to Portuguese project-owned behavior; it is transitional debt, not a final owner.
- Direct behavior already resides in responsibility modules.
- `core.def` owns the central Portuguese setup/state vocabulary consumed by layout, front matter and profile modules.
- `template/main.tex` remains a Portuguese API consumer, so template/tests migrate atomically with each owner lot.
- `integrations/abntexto.def` must move with the canonical definition-list environment because it overrides that environment for current LaTeX/ABNTexto behavior.
- Rendered Portuguese academic labels remain protected content.
- Genuine upstream non-English identifiers remain only at explicit integration boundaries.

## R2 implementation sequence

1. **R2-B1 / #234 — canonical setup and internal state vocabulary.** Direct English setup ownership; canonical document/profile state and metadata vocabulary; all state consumers/template/tests move atomically.
2. **R2-B2 — academic and front-matter public rendering API.** Direct canonical rendering commands plus layout-hook rebinding.
3. **R2-B3 — structural/object environments, optional object API and hooks.** Direct canonical environments, object APIs, extension hooks and project-owned object IDs; preserve upstream boundaries.
4. **R2-B4 — bibliography/back-matter API and plumbing internalization.** Direct bibliography/glossary/index commands and internal helper cleanup.
5. **R2-B5 — final consumer migration and forwarding-layer removal.** Remove `public-api.def`, finish residual scans, reconcile tests, and generate `docs/MIGRATING-TO-V3.md` without runtime aliases.

## Hard boundaries

- No blind global replacement.
- Producer/state consumer/template/test changes move together.
- No new compatibility alias layer.
- Preserve rendered Portuguese academic and official wording.
- Preserve normative rule IDs, expected values, tolerances, locators and proof state absent explicit new evidence.
- Do not rename genuine upstream identifiers solely for cosmetic consistency.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission during R2 implementation.

## Immediate action

Execute R2-B1 through issue #234 from canonical `main`. Start with a complete consumer inventory for core setup/state vocabulary, then change producers and consumers atomically and validate with the permanent gates.

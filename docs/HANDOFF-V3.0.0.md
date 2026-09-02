# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- R2-B1 merged checkpoint on `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B2 — academic and front-matter public rendering API**.
- Active implementation issue: **#237**.
- R2-B1 issue #234: **DONE through PR #236**.
- R2-A inventory issue #232: **DONE through ownership inventory and closeout PR #235**.
- V3-R1 / R1-B8: **DONE**; issue #227 closed completed.
- Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and `release/v3-api-migration.json` must agree. Disagreement fails closed.

## Stable foundation

All R1 structural, distribution, static-gate, permanent-workflow and Windows/literal-font/PDF-A certification blocks are complete. Permanent validation remains `make static-check`, `make check`, and `make release-check`, orchestrated by `Static contract`, `Linux integration`, and `Linux release check`.

R2-A classified direct behavior owners and upstream boundaries. R2-B1 then moved the complete canonical setup/internal-state vocabulary into those owners with all live consumers migrated atomically.

## R2-B1 closure evidence

- implementation head: `99fb58deaa1594ca19fb3a00ca9418623e5b25aa`;
- PR: #236;
- merged `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`;
- `Static contract`: run `33668283912`, PASS;
- first complete integration after migration: run `33665983360`, `PASS=24 FAIL=6 SKIP=0`, correctly fail-closed on six stale dynamic setup consumers;
- final `Linux integration`: run `33668283890`, job `100375428004`, `PASS=30 FAIL=0 SKIP=0`;
- issue #234: closed completed;
- no runtime alias layer introduced;
- no normative rule/value/tolerance/locator/proof-state change;
- no proprietary font redistribution;
- no CTAN submission.

The observational `FRONTMATTER-EVIDENCE` internal FAIL records seen inside the passing front-matter gate predate B1 and match the certified green baseline. They are not B1 regressions and remain outside this API migration lot absent new normative evidence.

## Current runtime/API state

`public-api.def` remains transitional R2 debt, but its setup-key forwarding responsibility was removed in B1. Canonical setup/state is now directly owned by `core.def`, `fonts.def`, `modules.def`, `institutional.def`, and `academic-works.def`, with canonical consumers throughout layout/front matter/profile/template/test paths.

The remaining forwarding surface is bounded to later public commands/environments and helper debt. B2 now owns the academic/front-matter rendering commands and corresponding layout-hook rebinding. B3 owns structural/object environments/APIs/hooks, B4 owns bibliography/back-matter commands and plumbing internalization, and B5 owns the final residual consumer sweep plus removal of `public-api.def`.

## R2 implementation sequence

1. **R2-B1 / #234 — DONE.** Canonical setup and internal state vocabulary directly owned and fully validated.
2. **R2-B2 / #237 — ACTIVE.** Academic and front-matter public rendering API; direct canonical commands plus layout-hook rebinding and atomic consumer migration.
3. **R2-B3 / #238 — PENDING.** Structural/object environments, optional object API, extension hooks and project-owned object IDs.
4. **R2-B4 / #239 — PENDING.** Bibliography/back-matter API and plumbing internalization.
5. **R2-B5 / #240 — PENDING.** Final consumer migration, forwarding-layer removal, residual scan and `docs/MIGRATING-TO-V3.md`.

## Hard boundaries

- No blind global replacement.
- Producer/behavior owner/template/test changes move together.
- No new compatibility alias layer.
- Preserve rendered Portuguese academic and official wording.
- Preserve normative rule IDs, expected values, tolerances, locators and proof state absent explicit new evidence.
- Do not rename genuine upstream identifiers solely for cosmetic consistency.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission during R2 implementation.

## Immediate action

Execute R2-B2 through issue #237 from canonical `main`. Inventory the exact canonical/Portuguese academic and front-matter rendering command pairs plus layout hooks, then migrate each behavior owner and all template/test consumers atomically. Run `make static-check` and the permanent `Linux integration` gate before B2 closure.

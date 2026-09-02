# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- R2-B2 merged checkpoint on `main`: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B3 — structural/object API ownership**.
- Active implementation issue: **#238**.
- R2-B2 issue #237: **DONE through PR #242**.
- R2-B1 issue #234: **DONE through PR #236**.
- R2-A inventory issue #232: **DONE through ownership inventory and closeout PR #235**.
- V3-R1 / R1-B8: **DONE**; issue #227 closed completed.
- Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and `release/v3-api-migration.json` must agree. Disagreement fails closed.

## Stable foundation

All R1 structural, distribution, static-gate, permanent-workflow and Windows/literal-font/PDF-A certification blocks are complete. Permanent validation remains `make static-check`, `make check`, and `make release-check`, orchestrated by `Static contract`, `Linux integration`, and `Linux release check`.

R2-A classified direct behavior owners and upstream boundaries. R2-B1 moved the complete canonical setup/internal-state vocabulary into those owners. R2-B2 then moved academic/front-matter rendering commands and their live consumers/hooks into direct canonical ownership.

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

## R2-B2 closure evidence

- entry `main`: `e418893ee5c89f12cc4ac8d845111c894ec946e4`;
- implementation head: `4341a2adb4633b634d1e2ad905b1731e8126354b`;
- PR: #242;
- merged `main`: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`;
- `Static contract`: run `33680378948`, PASS;
- final `Linux integration`: run `33680378846`, job `100415223907`, `PASS=30 FAIL=0 SKIP=0`;
- strengthened residual audit: run `33680252116`, job `100414804865`, PASS;
- initial executor run `33679535751` failed closed on temporary cleanup order and did not publish a product checkpoint;
- corrected executor run `33679827267`, job `100413437018`, passed;
- zero B2 Portuguese runtime commands/hooks/forwards remain;
- no runtime alias layer, normative semantic/proof-state change, proprietary font redistribution or CTAN submission.

## Current runtime/API state

`public-api.def` remains transitional R2 debt, but B1 removed setup forwarding and B2 removed academic/front-matter command forwarding. Canonical setup/state and academic/front-matter rendering behavior are now directly owned by their responsibility modules and all live B2 consumers use the canonical API.

The remaining forwarding surface is bounded to B3 structural/object environments/APIs plus B4 bibliography/back-matter commands. B3 is active and owns structural/object environments, source/note and object-list APIs, optional listing/minted APIs, extension hooks, and project-owned object IDs. B4 owns bibliography/back-matter commands and plumbing internalization. B5 owns the final residual consumer sweep plus removal of `public-api.def`.

## R2 implementation sequence

1. **R2-B1 / #234 — DONE.** Canonical setup and internal state vocabulary directly owned and fully validated.
2. **R2-B2 / #237 — DONE.** Academic/front-matter rendering API directly owned; PR #242 merged with permanent integration green.
3. **R2-B3 / #238 — ACTIVE.** Structural/object environments, optional object API, extension hooks and project-owned object IDs.
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

Execute R2-B3 through issue #238 from canonical `main`. Migrate structural environments and the definition-list ABNTexto override atomically; move object/source/note/listing/minted/algorithm APIs and extension hooks to direct canonical ownership; replace project-owned `codigo` / `algoritmo` object IDs with English project identifiers while preserving rendered Portuguese labels; migrate all live template/test consumers; and remove only B3 forwarding debt. Run the strengthened residual scan, `make static-check`, and permanent `Linux integration` before B3 closure.

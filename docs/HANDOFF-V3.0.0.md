# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-A — Runtime/API ownership inventory and migration plan**.
- R1 / R1-BLOCK-8: **DONE**.
- R1 closure issue: **#227**.
- Active R2-A issue: **#232**.
- Active trunk: **`main`**.
- Certified R1 candidate: **`9b1752565ac217c04ffa22a9ef272cdf078af380`**.
- B8 tooling checkpoint: `d2c24fc85351a410ea1f0101887b2a5228077741` (PR #230).
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main`, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and Git facts must agree; disagreement fails closed.

## Completed R1

| Stage | Status | Checkpoint / evidence |
|---|---|---|
| R1-S0 | DONE | repository sanitation/history governance |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` |
| R1-B8 | DONE | `9b1752565ac217c04ffa22a9ef272cdf078af380`; Windows `33649620219`; final inspection `33655108349` |

## Stable contracts entering R2

- `abntexto-ufc.cls` is the sole canonical class entry point.
- `public-api.def` is transitional R2 debt: canonical English API currently forwards to Portuguese behavior owners.
- Final public behavior must be owned directly by responsibility modules; removed Portuguese v2 project API must not survive as runtime aliases.
- Genuine upstream non-English identifiers may remain only at explicit integration boundaries.
- Academic/rendered Portuguese and official UFC/ABNT wording are protected domain content, not engineering-identifier debt.
- `make static-check`, `make check`, and `make release-check` remain the repository-owned validation entry points.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Public bundles exclude proprietary Microsoft fonts/institutional assets as already defined; actual CTAN submission remains separate.

## Final B8 evidence

Windows run `33649620219` built all four complete strict candidates. Artifact ID `9854415113`, digest `sha256:138b9a4e3c2969db33c512bec91b323cba339bb6ae18afc76786b59d2e0f7a21`.

Final Linux run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, full embedding and PDF/A-2b. Evidence artifact ID `9856387211`, digest `sha256:256c96e1c32d839b5b3a3e55f7a355913b7b217609c2f6e2d27104e7e12ffeeb`.

`TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not text fallback. No runtime/API or normative/proof-state change was required. No proprietary font was redistributed. No temporary B8 workflow remains.

## V3-R2 / R2-A

Issue #232 is active and `release/v3-api-migration.json` is the current migration contract.

R2-A must inventory/classify before changing behavior: remaining Portuguese project-owned setup keys/values, commands, environments, hooks, internals; `public-api.def` forwarding aliases; genuine upstream boundaries; direct owning modules; and atomic producer/consumer/test/template/doc migration lots.

## Hard boundaries

- No blind global replacement.
- Preserve rendered behavior during ownership mapping.
- Preserve normative rule IDs, values, tolerances, locators and proof state absent explicit new evidence.
- Do not replace `public-api.def` with another compatibility layer.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform or claim actual CTAN submission/acceptance during R2-A.
- Do not rerun completed heavy certification gates without current-state need.

## Immediate action

Execute R2-A issue #232 and produce the complete ownership inventory plus bounded migration-lot plan. Only then begin the first behavioral migration lot.

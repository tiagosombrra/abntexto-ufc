# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1 through V3-R5: **DONE**.
- Certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`.
- V3-A1/#275 exact entry: `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.
- V3-A1 source contract: **VALIDATED AND MERGED; canonical closeout pending**.
- A1 PR #279 merged at `4d018a92697e8f39e3a53b034c451e55996c84fb`.
- A1 source-only validation: `33894907220` — PASS.
- A1 Static contract: `33895016834` — PASS.
- A1 Linux integration: `33895016774` / job `101095498647` — `PASS=31 FAIL=0 SKIP=0`.
- Article contract: 18 rules = 17 manual + 1 conditional-manual; no article runtime/proof promotion in A1.
- Full contract observed by the PR gate: 199 rules; 188 normative; all normative rules locator-classified; zero UNASSESSED/unclassified evidence IDs.
- V3-A2/#280: **PREPARED / BLOCKED** until this A1 closeout checkpoint is merged and its immutable SHA is recorded.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Merge the A1 closeout checkpoint, capture its immutable main SHA, then perform one minimal exact-entry activation that marks V3-A1/#275 DONE and activates V3-A2/#280 from that predecessor. Do not start article runtime before that activation is canonical.

## Hard boundaries

Preserve certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` and the closed v3 API. Do not change the reconfirmed article authority, modality, rule IDs, locators, applicability or proof state without new current evidence. Do not restore historical machine identifiers or runtime aliases. Do not redistribute proprietary Microsoft fonts or perform CTAN submission. A2 must implement only the bounded `scientific-article` profile defined by `docs/ARTICLE-NORMATIVE-CONTRACT.md` and issue #280.

# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **DONE**.
- V3-R5/#272: **DONE** through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.
- Certified foundation product: `c79f3c73f1d51a30175e8259269504d029442a1c`; unchanged throughout R5.
- R5 release gate: run `33866258865` / job `101001704635` — `PASS=33 FAIL=0 SKIP=0`.
- R5 package/freeze validation: run `33869888601` / job `101013093747` — SUCCESS.
- R5 PR gates: Static `33872118250` — PASS; Linux `33872118241` / job `101020688121` — `PASS=31 FAIL=0 SKIP=0`.
- Public/distribution bundles, reproducibility, SHA-256 checksums, external-upstream semantics and institutional/proprietary asset exclusions: **PASS**.
- Validation residue: **0**.
- `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md`: unchanged through R5.
- V3-A1/#275: **ACTIVE — SOURCE CONTRACT CANDIDATE** from exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.
- A1 implementation base: `e40a56deeca8c22797398b0c95835964aefd2b15`.
- Current article authority set reconfirmed on 2026-09-04; 18 article rules are registered as 17 manual + 1 conditional-manual.
- A1 evidence is source-only (`article.source-review`); no article runtime/profile implementation or article proof promotion is allowed in A1.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Validate and merge the V3-A1 source-contract candidate. The source set and 18-rule conservative contract are now reconstructed; ABNT clause locators not directly available are recorded as partial-with-reason rather than guessed. After merge, capture the immutable A1 closeout SHA, close #275 and activate V3-A2. Do not implement article runtime before that exact-entry checkpoint.

## Hard boundaries

Preserve certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` and the closed v3 API. Do not implement article runtime/profile behavior in A1. Do not restore historical rule values, locators, source status, proof state or retired machine identifiers without current evidence. Do not redistribute proprietary Microsoft fonts or perform CTAN submission. V3-A2 remains blocked until A1 closes with a bounded implementation contract.

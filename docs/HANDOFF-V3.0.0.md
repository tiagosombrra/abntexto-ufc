# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **DONE**.
- R4 certified product: `c79f3c73f1d51a30175e8259269504d029442a1c`; certification run `33855800767` — SUCCESS.
- Exact V3-R5 entry: `0b0f5d989163dc6b1429feeb2d8a7c66988647bb` from R4 closeout PR #273.
- V3-R5/#272: **TECHNICALLY VALIDATED; canonical closeout pending**.
- Certified product invariance: **PASS** — no product-affecting path changed after `c79f3c73f1d51a30175e8259269504d029442a1c`.
- Full release gate: run `33866258865` / job `101001704635` completed `PASS=33 FAIL=0 SKIP=0`; that workflow later failed only during its initial packaging-precondition sequence, not in the release gate.
- Final package/freeze validation: run `33869888601` / job `101013093747` — SUCCESS.
- Public bundles: **PASS**; complete distribution bundles: **PASS**; reproducibility/checksums: **PASS**; institutional/proprietary asset exclusions: **PASS**.
- Tracked/untracked validation residue: **0**.
- `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md`: intentionally unchanged; no source/currency/API fact required an edit.
- V3-A1/#275: **PREPARED / BLOCKED**. Its exact entry SHA does not exist until R5 closes canonically.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Promote the validated R5 documentation/control-plane checkpoint through the permanent PR gates. After its squash merge, capture the real immutable main SHA and perform one minimal exact-entry activation that marks V3-R5 DONE and activates V3-A1/#275 from that SHA. Do not invent the A1 entry before the merge and do not start article runtime work in A1.

## Hard boundaries

Preserve certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` and the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. Do not redistribute proprietary Microsoft fonts or claim UFC homologation/CTAN acceptance. V3-A2 and actual CTAN submission remain blocked.

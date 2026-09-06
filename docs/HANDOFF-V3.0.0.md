# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-06

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Active phase | **Scientific Article** |
| Step 1 | ACCEPTED — `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1` |
| Step 2 | ACCEPTED — `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882` |
| Step 3 runtime | `81e08321222efb03626ac421fc645bd66edd5ae8` |
| Scoped migration | `336bc982d8442d572b52c4b9b78028e197c178b3`; article/profile evidence green, runner import failed |
| Runner-import synchronized checkpoint | `4f1c9a1b5c1e9d3b7a88c0271b198ef6f335422b` |
| Static on `4f1c9...` | `34030827665` — **SUCCESS** |
| Linux on `4f1c9...` | `34030827664` — failed in scope determination before integration (`fatal: bad object` for unavailable synchronize `before` SHA) |
| Current technical correction | `0a48d72c83b601c3ca8e0942f4c9b735ac5f0eb9` |
| Current batch | **Step 3 missing-before fail-closed scope fallback + synchronized acceptance** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Latest failure classification

The runner-import correction is confirmed by Static `34030827665 = SUCCESS`. Linux `34030827664` did not reach TeX or the coordinated runner. The workflow attempted an incremental diff using a PR-event `before` SHA that was not present in the checkout and terminated with `fatal: bad object`.

Classification: **Linux scope-determination robustness defect**. It is not an article runtime, authority, modality, proof-state, profile-compatibility, or runner-import failure.

The workflow must fail closed without crashing when incremental provenance is unavailable. Technical checkpoint `0a48d72c83b601c3ca8e0942f4c9b735ac5f0eb9` therefore:

1. verifies both synchronize endpoints with `git cat-file -e` before using the incremental range;
2. falls back to the authoritative full PR base/head range if either endpoint is unavailable;
3. extends the static Linux-suite contract to require this fallback;
4. keeps the six-profile non-article matrix explicitly separate from `scientific-article`;
5. records two-pass/final-pass warning evidence for optional foreign elements;
6. changes no article runtime or normative rule.

## Step 3 acceptance rule

The synchronized checkpoint containing `0a48d72...` plus this documentation must pass on the same SHA:

| Gate | Required result |
|---|---|
| Static contract | PASS, including dynamic runner loading and missing-before fallback contract |
| Linux integration | `profiles,article` PASS on a normal reachable incremental range; fallback remains available fail-closed when provenance is missing |
| Article profile | PASS under pdfLaTeX and LuaLaTeX |
| Required front block | PASS |
| Optional foreign elements | PASS for 4 scenarios × 2 engines; warnings inspected only after two-pass convergence |
| Non-article profiles | exactly 6 profiles × 2 engines PASS; `scientific-article` excluded |
| Normative state | no modality/proof-state drift |

Only after these gates are green may Step 3 become ACCEPTED and Step 4 start.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Publish the synchronized missing-before fallback checkpoint. |
| 2 | Require Static PASS. |
| 3 | Require PR Linux bounded scope `profiles,article` PASS on the same SHA. |
| 4 | Classify any failure before changing code or tests. |
| 5 | If green, update all control documents, mark Step 3 ACCEPTED, then activate Step 4. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts must remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Do not weaken normative traceability or scope fail-closed behavior.
- Do not change article authority, modality, rule IDs or proof state in this correction.
- Foreign title/summary remain independently optional.
- Article body typography remains Step 4 work.
- Recommendations remain advisory.
- Item 33 remains fail-closed.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.

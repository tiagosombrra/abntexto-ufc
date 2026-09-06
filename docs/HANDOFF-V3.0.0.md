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
| Scoped migration checkpoint | `336bc982d8442d572b52c4b9b78028e197c178b3` |
| Static on migration | `34030098936` — FAIL, runner sibling-import defect |
| Linux on migration | `34030098924` — `profiles,article`, PASS=7 FAIL=1 SKIP=0 |
| Technical correction | `4068414a2c2e1f919246438b516a6092f677925f` |
| Current batch | **Step 3 runner-import correction + synchronized scoped acceptance** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Migration-run classification

The scoped orchestration worked as designed on `336bc982...`: PR `synchronize` selected `profiles,article`, not `complete`. The executable evidence was strong:

- `ARTICLE-PROFILE-EVIDENCE`: PASS under both engines;
- `ARTICLE-FRONT-BLOCK-EVIDENCE`: PASS under both engines;
- `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE`: PASS for four optionality scenarios under both engines;
- six accepted non-article profiles: PASS under both engines;
- build-path, multivolume and catalog-card checks: PASS.

The sole failure in Linux `34030098924` was `validator-source`. Static `34030098936` stopped at the same point. `tests/checks/normative_traceability.py` dynamically loads `tests/run.py`; after the scoped-runner refactor, `tests/run.py` imported sibling `integration_suites.py` without first making its own directory importable. The result was `ModuleNotFoundError: No module named 'integration_suites'`.

Classification: **runner import-path defect**. This is not an article runtime, authority, modality, proof-state or compatibility failure. Normative traceability is not weakened.

## Current correction

Technical checkpoint `4068414a2c2e1f919246438b516a6092f677925f`:

1. makes `tests/run.py` add its own `tests/` directory to `sys.path` before importing `integration_suites`;
2. adds an explicit guard/evidence that the six-profile compatibility matrix excludes `scientific-article`;
3. records `convergence_passes=2` in foreign-element evidence, matching the corrected two-pass warning-inspection contract;
4. changes no article runtime, article authority, rule modality or proof state.

The synchronized branch checkpoint containing this technical commit plus current documentation must pass Static and bounded Linux `profiles,article` on the same SHA before Step 3 is accepted.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Publish the synchronized correction checkpoint on `feat/v3-scientific-article`. |
| 2 | Require Static PASS; `validator-source` must prove the dynamic-import path is repaired. |
| 3 | Require PR Linux `profiles,article` PASS on that same SHA. |
| 4 | If green, record exact checkpoint/run IDs and mark Step 3 ACCEPTED. |
| 5 | Activate Step 4 — textual structure and body typography. |
| 6 | Preserve `complete` for the immutable Scientific Article phase-end regression. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts must remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Do not weaken normative traceability to solve the import failure.
- Do not change article authority, modality, rule IDs or proof state in this correction.
- Foreign title/summary remain independently optional.
- Do not repurpose `title-variant`.
- Article body typography remains Step 4 work.
- Recommendations remain advisory.
- Item 33 remains fail-closed.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.

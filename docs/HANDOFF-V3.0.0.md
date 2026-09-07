# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Active phase | **Scientific Article** |
| Steps 1–4 | **ACCEPTED** |
| Step 4 acceptance checkpoint | `005956bd615042a12fb0393fddd4941b635f6ce3` |
| Static | `34119007413` — PASS |
| Linux | `34119007425` — PASS, `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| Physical body evidence | pdfLaTeX/LuaLaTeX: 12 pt, justified, 2 cm indent, `13.800 pt` single spacing |
| Negative structure evidence | missing Development rejected by rendered-heading predicate despite prose mentioning `desenvolvimento` |
| Current work | **Step 5 — recommendations and conditional applicability** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 accepted evidence

| Surface | Evidence | State |
|---|---|---|
| Supported spacing API | `\singlesp`; no deprecated-spacing warning | PASS |
| Textual-transition persistence | article-only `cmd/textual/after` route | PASS |
| pdfLaTeX body | 12 pt; indent `57.125 pt`, delta `0.432 pt`; gap `13.800 pt` | PASS |
| LuaLaTeX body | 12 pt; indent `57.125 pt`, delta `0.432 pt`; gap `13.800 pt` | PASS |
| Required structure | Introduction → Development → Final Considerations → References | PASS |
| Negative structure | missing Development rejected as missing required heading | PASS |
| Earlier Step isolation | profile/front-block/foreign-element checks remain green | PASS |
| Proof state | `proof_state_promoted=0` | preserved |

Step 4 is formally accepted. The checker correction did not change runtime, physical tolerances, authority or proof state; it only prevented incidental prose from satisfying a required structural-heading predicate.

## Step 5 scope

Step 5 preserves the modalities already frozen in the 18-rule authority contract:

| Rule family | Contract meaning |
|---|---|
| Author alignment | right alignment is recommended, not mandatory |
| Summary length | 150–250 words is recommended, not a rejection boundary |
| Keyword count | at least three keywords is recommended, not a rejection boundary |
| Summary paragraphs | one paragraph is recommended, not a rejection boundary |
| Journal precedence | required only when a target-journal submission context exists; generic UFC profile remains fallback |

Step 5 must produce executable evidence that recommendations do not become hard failures and that the journal boundary remains conditional rather than silently hard-coded into the generic profile. No authority/proof-state promotion occurs merely by documenting or testing modality.

## Acceptance gate before Step 6

1. Static contract passes on the synchronized Step 5 implementation checkpoint;
2. Linux article scope remains green;
3. recommendation-specific scenarios prove non-enforcement of recommended thresholds;
4. journal precedence remains conditional/manual and context-bound;
5. Steps 1–4 remain green;
6. no shared non-article runtime behavior changes;
7. authority IDs, locators, normativity and proof-state semantics remain unchanged.

## Immediate action

1. implement Step 5 evidence and user-facing guidance without converting recommendations into mandatory validation;
2. synchronize AGENTS, handoff, roadmap, Scientific Article plan and machine state in the same material-advance cycle;
3. run Static and article Linux on the synchronized checkpoint;
4. classify any failure before changing runtime/tests;
5. after Step 5 acceptance, activate Step 6 evidence hardening;
6. later close Scientific Article only after canonical article PDF visual review and complete phase-end regression on one immutable SHA.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize phase closure by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Recommendations must not become hard compile/validation failures.
- Target-journal instructions remain conditional applicability, not generic UFC runtime law.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.

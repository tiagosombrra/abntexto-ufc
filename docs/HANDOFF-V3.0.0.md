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
| Step 5 implementation checkpoint | `6507da00275d8a69093541d6e6cb119a1b6f6cb3` |
| Step 5 Linux | `34126602083` PASS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0`; all six article checks passed |
| Step 5 Static | `34126602062` FAIL only on Linux suite inference for mixed orchestration + article paths |
| Current work | **Step 5 — orchestration inference correction + rendered recommendation-keyword hardening** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Failure classification

The Step 5 implementation itself is green under the complete Linux regression. The Static failure is independent of article runtime and recommendation semantics. `tests/integration_suites.py` treated orchestration files as unknown technical paths after determining that the change was not orchestration-only, causing `tests/run.py` + article files to select `complete`. `tests/checks/linux_integration_suites.py` correctly rejected this behavior.

The correction must preserve these invariants:

| Case | Required scope |
|---|---|
| orchestration only | `smoke` |
| orchestration + recognized article path | `article` |
| orchestration + another recognized domain | that bounded domain/union |
| orchestration + unknown technical path | `complete` |
| force-complete shared/core/standards path | `complete` |

The Step 5 recommendation gate is also hardened so the generated PDF must contain controlled keyword markers in both the recommendation-following and outside-recommendation scenarios. This is evidence hardening only; modality and runtime law do not change.

## Step 5 acceptance gate before Step 6

1. corrected synchronized checkpoint passes Static;
2. automatic Linux selection resolves to `article` for the mixed orchestration + Step 5 change;
3. Linux `article` passes all six first-class checks;
4. both recommendation scenarios compile with pdfLaTeX and LuaLaTeX and render controlled keyword markers;
5. recommendations remain non-enforcing;
6. journal precedence remains conditional/manual and context-bound;
7. Steps 1–4 remain green;
8. no proof-state, authority, non-article runtime or librarian-review classification changes.

## Immediate action

Publish the synchronized correction checkpoint, wait for Static and Linux, classify any failure before changing code/tests, and only after both gates pass record Step 5 as **ACCEPTED** and activate Step 6 in the same documentation cycle.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize phase closure by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Recommendations must not become hard compile/validation failures.
- Target-journal instructions remain conditional applicability, not generic UFC runtime law.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.

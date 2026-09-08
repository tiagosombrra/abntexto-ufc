# V3 Final Certification — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — BOUNDED MATRIX VALIDATION TRANSPORT

## Accepted baseline

| Surface | Evidence | State |
|---|---|---|
| Scientific Article | `923d11ef...`; Static `34154045481`; complete Linux `34154045509`; PDF 5/5 visual PASS | ACCEPTED |
| Final Certification entry | `aa6cc4a...`; Static `34161228915`; Linux `34161228823` | ACCEPTED |
| Linux release baseline | `f8be323...`; release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` | ACCEPTED |
| Profile/engine matrix | six non-article profiles × two engines plus scientific article × two engines in current complete release evidence | ACCEPTED |

## Certification sequence

| Step | Work | State | Acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and branch handoff | **ACCEPTED** | accepted evidence above |
| 2 | Linux release baseline | **ACCEPTED** | accepted evidence above |
| 3 | Profile and engine matrix | **ACCEPTED** | accepted evidence above |
| 4 | Literal fonts, Unicode and embedding | ACTIVE | final-candidate literal Times New Roman/Arial identity, Unicode extraction and embedding evidence required |
| 5 | Scientific Article PDF/A certification | **IMPLEMENTED — RELEASE VALIDATION PENDING** | new permanent release gate compiles canonical article and requires veraPDF PDF/A-2b plus embedding PASS |
| 6 | Distribution/public bundles | **IMPLEMENTED — RELEASE VALIDATION PENDING** | new permanent release gate builds four distribution candidates, verifies checksums/archive integrity and rejects proprietary fonts/institutional assets |
| 7 | Deterministic release reference PDF — issue #18 | QUEUED | pinned deterministic epoch, two clean builds and identical SHA-256 while existing validation remains intact |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux, release/certification matrix and phase-specific evidence |

## Current validation transport

`make release-check` now includes the two bounded persistent gates for Steps 5 and 6 after the established release matrix. A temporary PR workflow `.github/workflows/final-cert-bounded-matrix.yml` exists only to execute that permanent command on the certification branch. It must be removed after the release run is classified and before Steps 5/6 are accepted.

No PASS is claimed for the new gates until that release execution succeeds. Any failure is classified inside Step 5 or Step 6; it does not create a new roadmap workstream.

## Closure-scope freeze

Remaining v3.0.0 certification scope is frozen to Steps 4-8. Accepted shared, librarian-review, Reference PDF and Scientific Article semantics are not reopened unless a concrete regression proves them broken. A new step/phase is permitted only if current repository authority demonstrates that no existing acceptance predicate can represent a blocker.

## Issue #18 boundary

Issue #18 remains the only explicit reproducibility blocker. It requires a deterministic release epoch, stable metadata/document ID, two controlled clean reference-PDF builds and identical SHA-256. This evidence is additive and must not change normative runtime semantics.

## Non-negotiable boundaries

- Preserve librarian review state 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW.
- Item 33 remains fail-closed and is not a hidden implementation task.
- Do not redistribute proprietary Microsoft fonts.
- Tests/validators are not weakened to obtain green status.
- CTAN/external publication remains blocked until Release.

## Phase exit

Final Certification closes only after Steps 4-7 are accepted and the complete **phase-end regression** passes on one immutable candidate. Every **material advance** updates this plan, handoff, roadmap, release readiness and machine state in the same cycle.

# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch | `cert/v3-final-certification` |
| Scientific Article PR | #286 — MERGED |
| Active phase | **Final Certification** |
| Scientific Article phase-end candidate | `923d11ef668b02ec4de3cad4906ad5ac1f527eaf` |
| Article phase-end Static | `34154045481` — SUCCESS |
| Article phase-end Linux | `34154045509` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Article PDF | build `f62ac703...`; PDF SHA-256 `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db`; 5/5 visual PASS |
| Scientific Article | **CLOSED** |
| Final Certification | **ACTIVE — BASELINE ENTRY** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Branch handoff complete

PR #286 was squash-merged into `main` as `22e3c19235fa5245505b92d919a09d31eb2bfecb`. The active certification branch `cert/v3-final-certification` was created from exactly that SHA. Certification work must now remain on this branch until the next integration boundary.

## Immediate action

| Order | Action | Acceptance |
|---:|---|---|
| 1 | Validate this branch/main synchronization checkpoint | Static green; documentation-only Linux may skip heavy work |
| 2 | Establish current Linux release baseline | run/inspect permanent release contract before modifying certification machinery |
| 3 | Inventory existing literal-font, Unicode, embedding and PDF/A proof routes | reuse accepted evidence where valid; identify only genuine gaps |
| 4 | Inventory public/distribution bundle checks | no redundant or speculative implementation |
| 5 | Implement/validate issue #18 deterministic reference-PDF proof | two clean builds, pinned epoch, identical SHA-256, existing validation preserved |
| 6 | Assemble final immutable certification candidate | all required proof surfaces bound to one SHA |
| 7 | Run Final Certification phase-end regression | required before Release can become active |

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a real certification regression is discovered.
- Do not use issue #18 to change normative semantics.
- Item 33 remains fail-closed.
- Linux release evidence does not replace literal-font/platform/PDF-A certification.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until **Release**.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted/scoped checks never authorize a phase transition by themselves.

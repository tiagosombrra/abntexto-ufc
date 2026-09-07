# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Entry synchronization | **ACCEPTED** — `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS |
| Scientific Article | **CLOSED** — candidate `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Linux release baseline execution | **PASS** — transport SHA `f8be323027b42eefcdbe3d13b2f269abdd6ec17f`; Static `34168471299`; Linux `34168471312`; release run `34168471371` |
| Release baseline result | `make release-check`: **SCOPE=complete PASS=38 FAIL=0 SKIP=0** |
| Release baseline artifact | id `10035242168`; digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604` |
| Current batch | **Release Baseline Cleanup Candidate** |
| Temporary executor | removed in this cleanup candidate; acceptance waits for this candidate's Static/Linux |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `AGENTS.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Baseline classification

The temporary executor at `f8be323...` ran the exact permanent repository release contract, not a substitute contract. Run `34168471371` completed successfully with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; the uploaded validation artifact is `10035242168` with digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604`.

Static `34168471299` and normal Linux integration `34168471312` also passed at the same transport SHA.

The temporary workflow is removed in the current cleanup candidate. Step 2 is not marked ACCEPTED until the cleanup candidate passes Static and Linux, so executor removal and repository hygiene are proven rather than inferred.

## Immediate action

| Order | Action | Acceptance |
|---:|---|---|
| 1 | Validate the cleanup candidate after removing `.github/workflows/final-cert-release-baseline.yml` | Static + Linux green |
| 2 | Record cleanup SHA/run IDs and mark Linux release baseline ACCEPTED | docs/machine state synchronized |
| 3 | Activate profile/engine certification | supported profiles and required engines inventoried against current evidence |
| 4 | Continue literal-font/Unicode/embedding, PDF/A and distribution certification | no proof substitution |
| 5 | Resolve issue #18 deterministic reference PDF | two controlled clean builds with identical SHA-256 and preserved validation |
| 6 | Execute Final Certification phase-end regression | one immutable candidate with complete matrix |

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a real certification regression is discovered.
- Do not use issue #18 to change normative semantics.
- Item 33 remains fail-closed.
- Linux release evidence does not replace literal-font/platform/PDF-A certification.
- Temporary executor removal must be validated before bounded baseline acceptance.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until **Release**.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted/scoped checks never authorize a phase transition by themselves.

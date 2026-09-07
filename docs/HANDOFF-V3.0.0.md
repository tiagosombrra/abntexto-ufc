# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Entry synchronization | **ACCEPTED** — `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS, docs-only heavy skip |
| Scientific Article | **CLOSED** — candidate `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — RELEASE BASELINE EXECUTOR ACTIVE** |
| Temporary executor | `.github/workflows/final-cert-release-baseline.yml` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Active action

The temporary workflow is transport only for the existing permanent release contract. It runs the same TeX Live 2026 environment and `make release-check` command as `.github/workflows/linux-release-check.yml`. No new certification predicate or runtime behavior is introduced.

| Order | Action | Acceptance |
|---:|---|---|
| 1 | Run temporary release-baseline executor | `make release-check` green; validation evidence uploaded |
| 2 | Classify any failure before changing code/tests | fail closed |
| 3 | Remove the temporary executor | required before baseline acceptance |
| 4 | Record baseline run and cleanup checkpoint | docs/machine state synchronized |
| 5 | Continue profile/engine/font/Unicode/embedding/PDF-A/distribution inventory | only after baseline accepted |
| 6 | Resolve issue #18 and assemble immutable final candidate | required before phase-end regression |

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a real certification regression is discovered.
- Do not use issue #18 to change normative semantics.
- Item 33 remains fail-closed.
- Linux release evidence does not replace literal-font/platform/PDF-A certification.
- Temporary executor must be removed before bounded checkpoint acceptance.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until **Release**.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted/scoped checks never authorize a phase transition by themselves.

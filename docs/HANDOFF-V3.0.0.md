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
| Scientific Article | **CLOSED** — `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Linux release baseline | **ACCEPTED** — transport `f8be323...`; release `34168471371`, `PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` |
| Release baseline artifact | id `10035242168`; digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604` |
| Profile/engine matrix | **ACCEPTED** — six non-article profiles × 2 engines plus scientific article × 2 engines |
| Current batch | **Bounded Certification Matrix — Steps 4-6** |
| Temporary executor | none active |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `AGENTS.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Frozen remaining path

| Order | Work | Acceptance |
|---:|---|---|
| 1 | Literal Times New Roman/Arial + Unicode + embedding proof | final-candidate identity/extraction/embedding evidence passes without font redistribution |
| 2 | Explicit Scientific Article PDF/A proof | article PDF/A-2b validation passes on certification candidate |
| 3 | Distribution/public bundle integrity | package/public-distribution checks pass from certification candidate |
| 4 | Issue #18 deterministic reference PDF | two controlled clean builds with identical SHA-256 and preserved validation |
| 5 | Final Certification phase-end regression | one immutable candidate with complete matrix |
| 6 | Release | final docs/checksums/tag/GitHub Release/publication verification |

This set is the closure boundary. A failing check is handled inside the corresponding row; it does not create a new roadmap workstream unless current repository authority proves that none of these acceptance predicates can represent the blocker.

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a real certification regression is discovered.
- Do not use issue #18 to change normative semantics.
- Item 33 remains fail-closed and is not a hidden release implementation task.
- Linux release evidence does not replace literal-font/platform certification.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until **Release**.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted checks never authorize a phase transition or create a new workstream by themselves.

# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED — release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` |
| Profile/engine matrix | ACCEPTED |
| Current batch | **Bounded Matrix Validation — Scientific Article PDF/A + Distribution Integrity** |
| Temporary executor | `.github/workflows/final-cert-bounded-matrix.yml` active only for current release validation; remove before acceptance |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Current material advance

Two persistent release gates were added to `make release-check`:

| Gate | Predicate |
|---|---|
| Scientific Article PDF/A | build canonical article with pdfLaTeX, require embedded fonts and veraPDF PDF/A-2b compliance |
| Distribution/public bundles | build all four v3.0.0 distribution candidates, verify SHA256SUMS, ZIP integrity/safe paths and absence of proprietary fonts/institutional assets |

They are implementation-complete but **not accepted until the temporary release transport passes**. After classification, remove the temporary workflow and require cleanup Static/Linux before marking Steps 5-6 accepted.

## Frozen remaining path

| Order | Work | Acceptance |
|---:|---|---|
| 1 | Literal Times New Roman/Arial + Unicode + embedding | final-candidate identity/extraction/embedding proof |
| 2 | Accept article PDF/A + distribution gates | release transport PASS + temporary executor removal + cleanup CI PASS |
| 3 | Issue #18 deterministic reference PDF | two controlled clean builds with identical SHA-256 and preserved validation |
| 4 | Final Certification phase-end regression | one immutable candidate with complete matrix |
| 5 | Release | final docs/checksums/tag/GitHub Release/publication verification |

A failure remains inside the row whose predicate it violates. It does not create a new roadmap workstream.

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a concrete regression is discovered.
- Item 33 remains fail-closed and is not a hidden release task.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until Release.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted checks never authorize a phase transition or create a new workstream by themselves.

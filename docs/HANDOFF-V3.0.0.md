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
| Current batch | **Step 6 canonical-checkout runner correction** |
| First bounded transport | `21455c3344...` / `34172047786`: release 38/38 + Step 5 PASS, then Git dubious-ownership failure during epoch read |
| Second bounded transport | `247e31398...` / `34173496336`: release 38/38 + Step 5 PASS, then `Distribution bundle generation requires a canonical Git checkout.` during tracked-file discovery |
| Current checkpoint validation | `247e31398...`: Static `34173496318` PASS; Linux `34173496285` PASS |
| Second failure artifact | ID `10036808737`, SHA-256 `c56e1c651ce990ddd5a301c5cf60691b1081a06b7eebe66b27503e256e28e273` |
| Temporary executor | `.github/workflows/final-cert-bounded-matrix.yml` remains active only for corrected rerun; removal required before Steps 5-6 acceptance |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Current material advance

The second transport proved that the per-command epoch correction worked: the run progressed through the complete permanent 38-check release matrix and Scientific Article PDF/A/embedding before failing later in Step 6. The remaining failure comes from `git ls-files` invoked by distribution/public-bundle tooling inside the TeX Live container, where the mounted runner checkout is not trusted by that container-local Git configuration.

The current correction is runner-scoped rather than product-scoped: both the temporary bounded transport and permanent Linux release workflow register only the current mounted checkout as a Git `safe.directory` before invoking `make release-check`. Bundle content predicates, checksums, archive safety, proprietary-font exclusion and institutional-asset exclusion remain unchanged.

## Frozen remaining path

| Order | Work | Acceptance |
|---:|---|---|
| 1 | Rerun corrected Step 6 distribution validation | same permanent `make release-check` contract PASS including distribution evidence |
| 2 | Remove temporary bounded workflow and validate cleanup | cleanup Static + Linux PASS; then Steps 5-6 accepted |
| 3 | Literal Times New Roman/Arial + Unicode + embedding | current final-candidate identity/extraction/embedding proof |
| 4 | Issue #18 deterministic reference PDF | two controlled clean builds with identical SHA-256 and preserved validation |
| 5 | Final Certification phase-end regression | one immutable candidate with complete matrix |
| 6 | Release | final docs/checksums/tag/GitHub Release/publication verification |

A failure remains inside the row whose predicate it violates. It does not create a new roadmap workstream.

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a concrete regression is discovered.
- Item 33 remains fail-closed and is not a hidden release task.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until Release.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted checks never authorize a phase transition or create a new workstream by themselves.

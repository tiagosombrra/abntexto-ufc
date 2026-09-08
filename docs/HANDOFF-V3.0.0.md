# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` before transition merge | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Release** |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` SUCCESS |
| Final complete Linux | `34239890614` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-reference reproducibility | PASS; SHA-256 `ae4d7755d18e05abd572a0ad95e5696e54302f9ac236b1efc004d46f57216479` for two builds in the accepted release-check run |
| One-shot Final Certification marker | removed in synchronized transition |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release entry — transition validation, merge #289, then release-branch synchronization** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/CTAN-RELEASE.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Final Certification acceptance

Candidate `22f7ba845...` satisfies the complete phase-end matrix. The Linux integration heavy suite actually executed at `complete` scope. The permanent Linux release check executed `make release-check`, retained all shared/article certification predicates, produced `PASS=38 FAIL=0 SKIP=0`, verified distribution integrity and passed the permanent deterministic release-reference-PDF gate. Item 33 remains fail-closed and was not converted into speculative runtime behavior.

## Immediate Release action

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate the synchronized transition commit on PR #289 | required CI green |
| 2 | Merge PR #289 | no unresolved transition regression |
| 3 | Read new `main` SHA and create the single short-lived Release task branch | branch facts synchronized |
| 4 | Update this handoff, roadmap, readiness and machine state to the Release branch | same work cycle |
| 5 | Execute the documented release checklist/tooling | preserve accepted certification evidence |
| 6 | Run the Release **phase-end regression** on one immutable candidate | required before Release closure |
| 7 | Create/verify tag, GitHub Release and any documented publication only after accepted Release candidate | verify assets/checksums |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Release publication actions must follow the repository release checklist; do not invent external publication steps.

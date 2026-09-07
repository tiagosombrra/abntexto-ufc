# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` before current PR merge | `fbf7cc4839ce318024a7d1ed517dd50fab5773ac` |
| Transition branch / PR | `feat/v3-scientific-article` / #286 |
| Active phase | **Final Certification** |
| Scientific Article phase-end candidate | `923d11ef668b02ec4de3cad4906ad5ac1f527eaf` |
| Phase-end Static | `34154045481` — SUCCESS |
| Phase-end Linux | `34154045509` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Article PDF | build `f62ac703d...`; PDF SHA-256 `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db`; 5/5 visual PASS |
| Scientific Article | **CLOSED** |
| Final Certification | **ACTIVE — ENTRY SYNCHRONIZATION** |
| Planned certification branch | `cert/v3-final-certification` after PR #286 merge |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Canonical control documents now include `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md` and `docs/V3-FINAL-CERTIFICATION.md` in addition to the roadmap, machine state, Scientific Article evidence, librarian review and release-readiness records.

## Scientific Article closure

The cleanup checkpoint `923d11ef...` passed its Static gate and, critically, the Linux orchestration selected `complete` scope. That complete run executed 36 checks and included every executable Scientific Article gate plus the shared profile/repository matrix. Combined with the already accepted provenance-bound 5-page article PDF and complete visual review, the same immutable SHA satisfies both Step 7 cleanup acceptance and Step 8 phase-end regression.

No second complete regression is required merely to repeat the same accepted candidate. The concrete candidate and run IDs are recorded in `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md`; the machine sentinel remains `one-immutable-sha`.

## Immediate action

| Order | Action | Boundary |
|---:|---|---|
| 1 | Validate this synchronized transition documentation | Static must remain green; docs-only Linux may skip heavy execution |
| 2 | Merge PR #286 | only after transition checkpoint remains green/mergeable |
| 3 | Read updated `main` SHA | this becomes the Final Certification baseline |
| 4 | Create `cert/v3-final-certification` from updated `main` | do not reuse the article branch for certification implementation |
| 5 | Synchronize branch/main facts on the new branch | documentation-only entry checkpoint first |
| 6 | Execute Final Certification plan | Linux release baseline, profiles/engines/fonts/Unicode/embedding/PDF-A/distribution and issue #18 reproducibility |
| 7 | Run Final Certification phase-end regression | one immutable SHA before Release may activate |

## Hard boundaries

- Preserve accepted non-article and Scientific Article behavior unless certification discovers a real regression.
- Do not use issue #18 to change normative semantics.
- Item 33 remains fail-closed.
- Linux release evidence does not replace literal-font/platform/PDF-A certification.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until **Release**.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted or scoped checks never authorize a phase transition by themselves.

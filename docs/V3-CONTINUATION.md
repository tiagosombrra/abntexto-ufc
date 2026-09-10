# V3 Continuation Handoff — Release Recovery 3.0.1

Updated: 2026-09-10
Status: RELEASE — COMBINED PR #302 + 3.0.1 RECOVERY / FINAL EXACT-MAIN RECERTIFICATION PENDING

This file is the shortest safe entry point for continuing v3 work from a new ChatGPT conversation, Codex session or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` — always resolve current SHA dynamically from Git |
| Active roadmap phase | **Release** |
| Recovery target | `3.0.1` |
| Recovery work branch | `release/v3.0.1-recovery` — short-lived; canonical state remains `main` |
| Publication hardening | PR #297 merged |
| Post-hardening control synchronization | PR #298 merged, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Final release-gate integration | PR #301 merged as `395899e1b2336ed268335d68e59e03452880c15e` |
| Post-v3.0.0 runtime fix | PR #302 squash-merged as `6d06d4ed42b2187b1483ea219ee055cfe975ece2`; populated unified illustration-list renderer corrected and regression-covered |
| Pre-recovery technical evidence | run `34419086322`: `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck` PASS; historical baseline only because it predates #302 and recovery bytes |
| Public `v3.0.0` | exists on `05399473827da7cf6b6c8bac36edc7115481773f`; premature/superseded for final publication |
| Final candidate semantics | exact canonical `main` SHA containing PR #302 plus the 3.0.1 recovery and fresh certification |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN upload contract | exactly one archive: `abntexto-ufc-3.0.1.zip` |
| CTAN runtime contract | exactly one generated `abntexto-ufc.cls`; zero project-owned `.def` files |
| Human gate | final PDF + `.tex` for seven supported profiles; explicit maintainer approval required |
| Tag contract | certified SHA = visually approved SHA = `v3.0.1` SHA = publication source SHA |

`docs/V3-RELEASE-RECOVERY.md` records why the recovery uses `3.0.1`, why `v3.0.0` is not silently retargeted, and why PR #302 must be included in the final candidate.

## What remains closed

- Regression Audit;
- Core Corrections;
- Reference PDF Validation;
- Scientific Article;
- Final Certification;
- consolidated librarian review: 34/34 PASS;
- accepted v3 public API and normative semantics;
- all runtime surfaces except the scoped populated unified illustration-list correction already merged through PR #302;
- CTAN monolithic-runtime design: one generated class, 14 tracked modules inlined, zero project-owned `.def` files;
- exclusion of UFC institutional marks and proprietary Microsoft fonts from CTAN.

The recovery remains inside Release. PR #302 does not reopen prior phases; it is a scoped post-v3.0.0 defect correction that must be included in the final 3.0.1 regression.

## Recovery state

The previously public `v3.0.0` GitHub Release was created before the final exact-SHA release invariant had been satisfied. Because public assets existed under that tag, the repository does not silently retarget it. Those assets are historical/superseded and are not eligible for final CTAN submission.

The pre-recovery exact-main SHA `395899e1...` passed the automated release matrix and current CTAN `pkgcheck`, but it predates both PR #302 and the 3.0.1 recovery changes. Therefore, that evidence is baseline evidence only; the recovered release requires a new exact-SHA cycle over the combined state.

PR #302 corrected populated unified illustration-list rendering in `abntexto-ufc/objects.def`. Its regression fixture now creates a real illustration entry and the gate verifies that the `.loi` entry is written and rendered without unrecognized warnings or overflows. It was squash-merged to canonical `main` as `6d06d4ed42b2187b1483ea219ee055cfe975ece2` and reconciled into the recovery branch before candidate certification.

## Required seven-profile review

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

A preliminary seven-profile set from the earlier baseline passed A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight plus assistant page-by-page inspection. It does not close the final human gate: the final pairs must be regenerated from the exact 3.0.1 candidate containing PR #302 and explicitly approved by the maintainer.

## Remaining work

1. require Static + **complete** Linux integration + Linux release/pkgcheck on the reconciled recovery branch;
2. verify that the heavy Linux integration step actually ran rather than returning a scoped skip;
3. merge the recovery branch to `main` only after the combined PR gates pass;
4. resolve the resulting exact canonical `main` SHA;
5. require Static + automatic complete Linux integration + Linux release check on that exact SHA;
6. require current CTAN `pkgcheck` output/version/archive-hash evidence for `abntexto-ufc-3.0.1.zip` and classify all warnings;
7. retain and physically audit the deterministic 3.0.1 distribution;
8. retain the seven final PDF/`.tex` pairs from that exact candidate and obtain explicit maintainer approval;
9. freeze hashes/evidence;
10. create immutable `v3.0.1` on the same certified and visually approved SHA;
11. create GitHub Release with exact frozen assets and verify re-downloaded hashes;
12. submit only `abntexto-ufc-3.0.1.zip` to CTAN;
13. preserve submission/acceptance/install evidence and close Release only after external verification.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## Windows literal-font scope

Retained Windows/literal-font evidence remains scope-valid because PR #302 and the recovery changes do not alter font runtime, font setup, engine behavior or the Windows certification contract. Any such later change forces a fresh Windows recertification.

## Local continuation

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
```

Then read:

1. `AGENTS.md`
2. `release/v3-roadmap.json`
3. `release/v3-release-candidate.json`
4. `docs/V3-CONTINUATION.md`
5. `docs/V3-RELEASE-RECOVERY.md`
6. `docs/HANDOFF-V3.0.0.md`
7. `docs/V3-RELEASE-READINESS.md`
8. `docs/V3-RELEASE-PHASE-END.md`
9. `docs/CTAN-RELEASE.md`
10. `docs/UFC-LIBRARIAN-REVIEW.md`

Every **material advance** updates affected control documents and machine state in the same work cycle. Targeted checks never replace the required **phase-end regression**. A successful workflow does not satisfy a complete gate when its heavy integration step was skipped. The public README tracks user-facing facts rather than transient CI state.

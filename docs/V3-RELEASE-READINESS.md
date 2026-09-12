# V3 Release Readiness — Recovery 3.0.1

> **Historical evidence — not current release authority.** ACTIVE/PENDING statements below belong to the phase in which this file was produced. Current v3.0.1 state is defined by `release/v3.0.1-final-corrections.json`, `docs/V3-CONTINUATION.md`, and the finalization plan. See `docs/V3.0.1-DOCUMENT-LIFECYCLE.md`.


Updated: 2026-09-10
Status: ACTIVE — RECOVERY MERGE / FINAL EXACT-MAIN RECERTIFICATION PENDING

## Phase readiness

| Phase | State | Evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF visual/PDF-A PASS |
| Final Certification | CLOSED | technical/runtime certification accepted |
| Release | **ACTIVE** | 3.0.1 recovery merge, exact-main pkgcheck, seven-profile approval and publication pending |

## Why Release is reopened at the publication boundary

A public GitHub `v3.0.0` tag and Release exist on `05399473827da7cf6b6c8bac36edc7115481773f`. The later exact-main state containing the final pkgcheck and seven-profile human-acceptance controls is `395899e1b2336ed268335d68e59e03452880c15e`.

Because the repository requires the certified SHA, visually approved SHA, tagged SHA and publication-source SHA to be identical, the existing public `v3.0.0` cannot be treated as the recovered final release. The repository will not silently retarget that tag. Recovery target is `3.0.1`; the detailed decision is in `docs/V3-RELEASE-RECOVERY.md`.

The recovery reopens exactly one accepted runtime surface: the populated unified illustration-list renderer corrected by PR #302. API semantics, normative rules, document profiles, typography, the remaining runtime modules and the 34-point librarian review remain closed.

## Accepted pre-recovery evidence

PR #297 closed publication-shape defects; PR #298 synchronized exact-main candidate controls; PR #301 integrated current CTAN `pkgcheck` and the mandatory seven-profile human visual gate. PR #302 then corrected the populated unified illustration-list renderer and was merged as `6d06d4ed42b2187b1483ea219ee055cfe975ece2`.

Exact-main run `34419086322` on `395899e1b2336ed268335d68e59e03452880c15e` reported `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck` PASS and retained validation/distribution artifacts. This is strong baseline evidence, but not final 3.0.1 evidence because it predates PR #302 and the recovery changes.

## Final 3.0.1 controls

Before the immutable `v3.0.1` tag:

1. the recovery changes including PR #302 must be merged to canonical `main`;
2. the resulting exact `main` SHA must pass Static, complete Linux integration and Linux release check;
3. current CTAN `pkgcheck` must process the exact `abntexto-ufc-3.0.1.zip` bytes and retain version/full-output/archive-hash evidence;
4. the deterministic three-ZIP distribution plus `SHA256SUMS` must be retained and physically audited;
5. PDF + corresponding `.tex` must be generated for all seven supported profiles from the same exact candidate;
6. every profile PDF must pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight;
7. the maintainer must explicitly approve all seven final pairs;
8. hashes/evidence must be frozen before tag creation and publication bytes must not be rebuilt afterward.

Required profile set:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

A preliminary set generated from the earlier baseline already passed 7/7 automated preflight and page-by-page assistant inspection. It does not close the final human gate because the final 3.0.1 pairs must come from the exact recovered candidate containing PR #302.

## Final-candidate contract

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit is allowed between final acceptance and tag creation without reopening the candidate cycle.

## Remaining gates

| Order | Gate | State |
|---:|---|---|
| 1 | Historical v3 technical/normative phases | **PASS / CLOSED** |
| 2 | Classify public `v3.0.0` mismatch and select recovery version | **PASS — 3.0.1** |
| 3 | Integrate PR #302 and prepare 3.0.1 version/control/pipeline recovery | **IN PROGRESS** |
| 4 | Merge recovery to canonical `main` | BLOCKED BY 3 |
| 5 | Static + automatic `scope=complete` Linux integration + Linux release check on exact post-merge SHA | BLOCKED BY 4 |
| 6 | Current CTAN `pkgcheck` on exact `abntexto-ufc-3.0.1.zip` and warning disposition | BLOCKED BY 5 |
| 7 | Retain and physically re-audit deterministic three-ZIP distribution + `SHA256SUMS` | BLOCKED BY 5–6 |
| 8 | Regenerate seven final PDF/`.tex` pairs and obtain explicit maintainer approval | BLOCKED BY 4–7 |
| 9 | Freeze hashes/evidence; prohibit rebuild | BLOCKED BY 5–8 |
| 10 | Create immutable `v3.0.1` on certified + visually approved SHA | BLOCKED BY 9 |
| 11 | Create GitHub 3.0.1 Release and re-download/hash-verify assets | BLOCKED BY 10 |
| 12 | Submit only `abntexto-ufc-3.0.1.zip` to CTAN and preserve receipt/acceptance evidence | BLOCKED BY 5–11 |
| 13 | Synchronize post-publication facts and close Release | BLOCKED BY 1–12 |

## Windows literal-font scope

Retained Windows literal-font certification remains scope-valid because PR #302 and the recovery changes do not alter font runtime or engine selection. A fresh Windows run becomes mandatory if font setup, engine behavior or the Windows certification contract changes before freeze.

Every **material advance** updates affected documentation and machine state in the same work cycle. Deterministic metadata/orchestration checks are performed before expensive CI. Targeted checks never replace the required **phase-end regression**. Automated green tests never substitute for explicit maintainer visual approval.

# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development and release recovery.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata, or publication state:

1. identify the actual Git branch and HEAD;
2. fetch current Git facts from `origin/main` rather than trusting a hardcoded current-main SHA in documentation;
3. read `release/v3-roadmap.json`;
4. read `docs/V3-CONTINUATION.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `docs/V3-RELEASE-READINESS.md`;
5. during **Release**, also read `docs/V3-RELEASE-RECOVERY.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
6. reconcile Git facts, machine state, handoff, roadmap, release blockers, retained-artifact provenance, tag/Release state and CTAN publication state before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.1` |
| Active phase | **Release** |
| Canonical branch | `main`; resolve its current SHA dynamically from Git |
| Recovery work branch | `release/v3.0.1-recovery` — short-lived branch only |
| Publication hardening | PR #297 merged |
| Post-hardening control synchronization | PR #298 merged, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Final release-gate integration | PR #301 merged as `395899e1b2336ed268335d68e59e03452880c15e` |
| Pre-recovery exact-main evidence | Linux release run `34419086322`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck` PASS |
| Public `v3.0.0` | exists on `05399473827da7cf6b6c8bac36edc7115481773f`; classified as premature/superseded for final publication |
| Recovery decision | do not silently retarget `v3.0.0`; recover as `v3.0.1` |
| CTAN final archive | `abntexto-ufc-3.0.1.zip` only |
| CTAN runtime | one generated `abntexto-ufc.cls`; zero project-owned `.def` files |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| Current batch | merge recovery, recertify exact main, regenerate seven review pairs, obtain maintainer approval, freeze and publish `v3.0.1` |

`docs/V3-CONTINUATION.md` is the concise operational handoff. `docs/V3-RELEASE-RECOVERY.md` is the authority for the 3.0.1 recovery decision.

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — closed
6. Release — active

The recovery does not invent a new phase. It reopens only the publication boundary inside Release.

## Engineering and Release rules

- Release is the final roadmap phase; do not invent a new phase for recovery or publication closeout.
- Project-owned technical surfaces are English; preserve the accepted v3 public API and normative/proof semantics.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary Microsoft fonts or UFC institutional marks in CTAN artifacts.
- The 34-point librarian review remains closed unless new primary authority or a demonstrated regression requires reopening an item.
- External publication is an explicit Release action and is never inferred from a build or candidate validation.
- The public `v3.0.0` tag must not be silently moved to a different commit.
- Existing `v3.0.0` GitHub Release bytes are historical/superseded and must not be submitted to CTAN as the recovered final package.
- Accepted `3.0.1` publication ZIPs must come from the exact accepted candidate artifact; do not rebuild them after acceptance.
- Do not encode a self-referential current `main` SHA as a machine invariant; current HEAD is a Git fact resolved at session start.
- Release workflow/test artifact names must derive from the canonical version source where practical rather than duplicating hard-coded release numbers.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification/release result, phase/acceptance state, artifact provenance, reproducibility state, tag/release state, candidate transport, recovery state or publication readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

The final `3.0.1` Release candidate is one immutable exact `main` SHA produced after the recovery changes are merged. The candidate must pass the complete applicable matrix before tag creation.

Minimum gates on the same exact candidate:

- Static contract;
- complete Linux integration;
- Linux release check with the complete release matrix;
- deterministic three-ZIP distribution plus `SHA256SUMS`;
- generated CTAN runtime shape `1 cls / 0 def` with all tracked runtime modules inlined exactly once;
- current CTAN `pkgcheck` on the exact `abntexto-ufc-3.0.1.zip` bytes;
- final PDF + `.tex` pairs for all seven supported profiles;
- A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight;
- explicit maintainer visual approval of all seven pairs.

Required invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## Immediate Release discipline

1. complete and merge the short-lived `release/v3.0.1-recovery` branch into canonical `main`;
2. resolve the resulting exact `main` SHA and require Static + complete Linux integration + Linux release check on that SHA;
3. retain and physically audit the resulting deterministic `3.0.1` distribution and current CTAN `pkgcheck` evidence;
4. regenerate the seven final PDF/`.tex` pairs from the exact candidate and obtain explicit maintainer approval;
5. freeze hashes/evidence and forbid rebuilds or tracked commits before tagging;
6. create immutable `v3.0.1` on the exact accepted SHA;
7. create the GitHub Release using the frozen assets and verify re-downloaded hashes;
8. submit only `abntexto-ufc-3.0.1.zip` to CTAN and retain receipt/acceptance/install evidence;
9. update final publication state and close Release only after external verification.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record the ambiguity and stop advancement. A targeted check never substitutes for the mandatory **phase-end regression**, and automated success never substitutes for explicit maintainer visual approval.

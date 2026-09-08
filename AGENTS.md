# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md` and `docs/V3-RELEASE-READINESS.md`;
4. during **Release**, also read `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers and temporary-marker/executor lifecycle before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Release** |
| Canonical `main` before transition merge | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Final Certification | **CLOSED** on `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` SUCCESS |
| Final complete Linux | `34239890614` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| One-shot Final Certification marker | removed in phase-transition commit |
| Current batch | **Release entry — transition validation and PR #289 merge** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — closed
6. Release — active

## Release scope freeze

Release is the final roadmap phase. Do not create another workstream merely because a validator exposes a defect; classify it inside Release and fail closed when needed.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal output under test, or explicit upstream/current-runtime boundaries.
- Preserve accepted v3 public API and shared/article semantics unless a concrete regression or current authority requires change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green workflow conclusion proves only that workflow's execution contract; required scope/predicates must also be verified.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary Microsoft fonts.
- Item 33 remains fail-closed and is not a hidden release implementation task.
- External publication is permitted only as an explicit Release checklist step after the accepted Release candidate is established.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification/release result, phase/acceptance state, artifact provenance, reproducibility state, tag/release state or publication readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification is accepted on `22f7ba845...`. Release must independently establish and record its own immutable phase-end candidate before Release can close.

The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the actual candidate SHA is recorded in evidence only after the commit exists.

## Immediate Release discipline

1. validate the synchronized Final Certification → Release transition;
2. merge PR #289 only after transition checks are green;
3. create one short-lived Release branch from the resulting `main`;
4. synchronize branch facts before release work;
5. follow `docs/CTAN-RELEASE.md` and repository tooling rather than inventing publication steps;
6. run Release phase-end regression before tag/GitHub Release/publication finalization;
7. verify published assets/checksums before closing Release.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.

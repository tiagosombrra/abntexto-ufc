# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/V3-RELEASE-PHASE.md`;
4. during **Release**, also read `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers and candidate/executor lifecycle before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Release** |
| Canonical `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3.0.0` / #292 |
| Final Certification | **CLOSED** on `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Release transport probe | `d1f86db10f1458ed75078239916f0de857671348` |
| Probe Static | `34253455083` SUCCESS |
| Probe Linux | `34253455068` workflow SUCCESS but **`SCOPE=smoke PASS=4 FAIL=0 SKIP=0` — not acceptable for phase-end** |
| Probe Linux release check | `34253454993` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-check artifact | ID `10067709957`; digest `2fc9a5f1dcadf330e2fb832c47e88fe00a6b0ffa2f7f5963291984f0de1f8c6e` |
| Probe deterministic reference PDF | PASS; SHA-256 `1acd4c47a1485d16c1b0cf92d074c6dc194dc8952c8f2c61709acbc6a9a503a7` |
| Current batch | **Release candidate transport repair — persistent complete-scope override and exact-head release checkout** |
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
- A green workflow conclusion proves only that workflow's execution contract; required scope and provenance predicates must also be verified.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary Microsoft fonts or UFC institutional mark assets.
- Item 33 remains fail-closed and is not a hidden release implementation task.
- External publication is permitted only as an explicit Release checklist step after the accepted Release candidate is established.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification/release result, phase/acceptance state, artifact provenance, reproducibility state, tag/release state or publication readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification is accepted on `22f7ba845...`. Release must independently establish and record its own immutable phase-end candidate before Release can close.

The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the actual candidate SHA is recorded in evidence only after the commit exists.

## Release transport defect classification

`d1f86db...` does not satisfy the Release phase-end regression even though all three workflows concluded `success`. Linux integration `34253455068` executed only the `smoke` suite because synchronize scope selection inspected the incremental push diff after the persistent Release marker had already been introduced. The machine policy explicitly rejects workflow success without the required `complete` scope.

Linux release check `34253454993` is useful bounded Release evidence, but its PR checkout used the merge ref. Release artifact provenance must be rebound to the exact PR head before final-candidate acceptance.

The repair must therefore make an active non-temporary `release/v3-release-candidate.json` at HEAD override incremental path inference to `complete`, and make the permanent Linux release check checkout the exact PR head with full Git history. Static checks must protect both properties.

## Immediate Release discipline

1. repair and statically protect persistent Release-candidate complete-scope selection and exact-head release-check checkout;
2. prove Static + **complete** Linux + Linux release check on the synchronized repair checkpoint;
3. build and verify final public/distribution artifacts and checksums from the accepted exact-head candidate route;
4. validate the extracted CTAN candidate and shipped example with the external `abntexto` dependency;
5. run the current CTAN `pkgcheck` when executable in the release environment;
6. freeze one immutable Release candidate and run Static, complete Linux, Linux release check and release-specific acceptance on it;
7. only after acceptance create/verify `v3.0.0` tag and GitHub Release, and perform any explicitly documented external publication action;
8. verify published assets/checksums before closing Release.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.

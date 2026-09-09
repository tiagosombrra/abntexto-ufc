# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata, or publication state:

1. identify the actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md` and `docs/V3-RELEASE-READINESS.md`;
4. during **Release**, also read `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers and candidate-marker/executor lifecycle before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Release** |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3-release` / #293 |
| Artifact-delivery implementation | **ACCEPTED** on `b55210acdb614fc3178e3ebf5b3a595bed8508c1` |
| Artifact-delivery Static / Linux | `34300561597` SUCCESS / `34300561605` SUCCESS, complete scope |
| Acceptance sync | `6ab4768662aa51842cf745afbf846e89b6bd466a`; Static `34303128975` SUCCESS |
| Current batch | **Release immutable phase-end candidate — marker published, regression pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — closed
6. Release — active

## Release scope freeze

Release is the final roadmap phase. Do not create another roadmap phase merely because a validator exposes a defect; classify it inside Release and fail closed when needed.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal output under test, or explicit upstream/current-runtime boundaries.
- Preserve accepted v3 public API and shared/article semantics unless a concrete regression or current authority requires change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green workflow conclusion proves only that workflow's execution contract; required scope/predicates must also be verified.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed and is not a hidden Release implementation task.
- External publication is permitted only as an explicit Release checklist step after the accepted Release candidate is established.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification/release result, phase/acceptance state, artifact provenance, reproducibility state, tag/release state, candidate transport or publication readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

Release now has one immutable candidate commit containing `release/v3-release-candidate.json` and synchronized candidate-pending state. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the actual Git candidate SHA is recorded only after the commit exists and CI is classified.

Do not amend the candidate after CI starts. Require Static contract, complete Linux integration and `Linux release check` on that same candidate.

## Artifact provenance rule

The permanent `Linux release check` hardening was accepted on `b55210ac...`. The candidate workflow must retain the exact four distribution ZIPs and `SHA256SUMS`. Those retained bytes, not rebuilt archives, are the only allowed source for the GitHub Release after candidate acceptance.

## Immediate Release discipline

1. wait for Static + complete Linux + Linux release check on the immutable candidate;
2. classify any failure before changing code/tests;
3. verify the retained candidate artifact and checksums;
4. record candidate SHA, run IDs and artifact identity in a later documentation-only synchronization commit;
5. only after acceptance create/verify `v3.0.0` tag, GitHub Release and any explicit documented publication;
6. verify published hashes before closing Release.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record the ambiguity and stop advancement.

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
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **PHASE-END REGRESSION ACCEPTED** |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS, complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Retained distribution artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Independent retained-artifact verification | exact five-file set, `SHA256SUMS` PASS and all four ZIP integrity checks PASS |
| Current batch | **Release publication — merge/tag/GitHub Release verification pending** |
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

Release phase-end regression is accepted on immutable candidate `75ead435eabe5157ed17c295ac26fce76438b0ca`. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the actual Git candidate SHA is recorded in evidence rather than self-recorded inside the candidate.

Accepted gates on the same candidate:

- Static contract `34303586782` — SUCCESS;
- Linux integration `34303586778` — SUCCESS with required complete scope;
- Linux release check `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- deterministic reference-PDF reproducibility — PASS, SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`, 450652 bytes;
- candidate-retained distribution bytes — independently downloaded and verified without rebuilding.

The phase itself remains ACTIVE until publication/verification closeout is complete.

## Artifact provenance rule

Only the retained candidate artifact from Linux release check `34303586773` may supply publication bytes. Artifact ID `10086299397` is bound to candidate `75ead435...` and has upload digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222`.

Verified inner checksums:

- `abntexto-ufc-3.0.0.zip`: `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207`
- `abntexto-ufc-ctan-3.0.0.zip`: `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60`
- `abntexto-ufc-overleaf-3.0.0.zip`: `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b`
- `abntexto-ufc-template-3.0.0.zip`: `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791`

Do not rebuild these archives for publication.

## Immediate Release discipline

1. synchronize this accepted candidate evidence in repository documentation and PR #293;
2. merge PR #293 only after the synchronization Static contract is green;
3. create `v3.0.0` tag and GitHub Release using the exact retained candidate-produced bytes;
4. verify published asset hashes against the accepted checksums;
5. perform CTAN `pkgcheck` and any actual CTAN upload only as an explicit action with receipt/evidence;
6. update documentation after every material advance and run final Release verification before marking Release CLOSED.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record the ambiguity and stop advancement.

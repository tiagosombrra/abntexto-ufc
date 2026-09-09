# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: ACCEPTED — PUBLICATION CLOSEOUT PENDING

## Purpose

This document records the immutable Release phase-end candidate and the exact evidence required before `v3.0.0` tag/GitHub Release/publication actions are finalized.

## Accepted preparation

| Preparation | Checkpoint | Evidence |
|---|---|---|
| Release candidate transport | `6a257f35b65266a1120826b816404116082b1e5c` | Static `34265429699`; Linux `34265429551`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Artifact-delivery tooling | `b55210acdb614fc3178e3ebf5b3a595bed8508c1` | Static `34300561597`; Linux `34300561605`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Acceptance control sync | `6ab4768662aa51842cf745afbf846e89b6bd466a` | Static `34303128975`; Linux documentation-only skip |

## Accepted immutable candidate

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` contains the tracked Release marker `release/v3-release-candidate.json` and the synchronized candidate state. It was not amended after CI started.

| Gate | Result |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Linux integration | `34303586778` — SUCCESS, required complete scope |
| Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Deterministic reference PDF | PASS; 2 builds; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| PDF/A / Unicode / embedding | PASS in complete release contract |
| Distribution artifacts/checksums | PASS; exact four ZIPs + `SHA256SUMS`; archive integrity PASS |
| Librarian review | remains `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`; item 33 stays fail-closed |
| Temporary executors/assets | absent from candidate/public bundles |

A workflow conclusion alone was not used as acceptance: the complete release scope and final `SCOPE=complete PASS=38 FAIL=0 SKIP=0` summary were verified from the release job log.

## Retained artifact provenance

The candidate's `Linux release check` retained:

- distribution artifact ID `10086299397`, name `abntexto-ufc-v3.0.0-distribution-34303586773`, size 11272152 bytes, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222`;
- validation artifact ID `10086298601`, name `linux-release-validation-34303586773`, size 481557 bytes, digest `sha256:124f692d571dde12754a6b084075b4acff29d47ffcfb4fb9d321cc8f1934d18c`.

The distribution artifact was downloaded after CI completion. The downloaded artifact SHA-256 matched GitHub metadata. Extraction yielded exactly:

- `abntexto-ufc-3.0.0.zip`
- `abntexto-ufc-ctan-3.0.0.zip`
- `abntexto-ufc-template-3.0.0.zip`
- `abntexto-ufc-overleaf-3.0.0.zip`
- `SHA256SUMS`

`sha256sum -c SHA256SUMS` passed for all four ZIPs, and `unzip -tq` passed for each ZIP. No archive was rebuilt during independent verification.

## Accepted publication checksums

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |

## Artifact provenance rule

The GitHub Release must use the exact candidate-produced bytes retained by release run `34303586773`. Rebuilding archives after candidate acceptance is not permitted release evidence.

## Publication boundary

The Release phase-end regression is accepted, but Release remains ACTIVE. Remaining actions are:

1. land the post-CI acceptance synchronization and merge PR #293;
2. create `v3.0.0` tag and GitHub Release using the exact retained candidate bytes;
3. verify published hashes against the accepted checksums;
4. run the current CTAN `pkgcheck`; perform/record actual CTAN submission only as an explicit action with receipt/evidence;
5. synchronize final publication facts and perform final Release verification before setting Release to CLOSED.

## Regression discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**. The accepted immutable candidate remains the Release phase-end evidence anchor through publication closeout.

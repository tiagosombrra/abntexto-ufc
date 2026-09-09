# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: ACCEPTED — PR MERGED / PUBLICATION CLOSEOUT PENDING

## Purpose

This document records the immutable Release phase-end candidate and the evidence boundary used through final publication closeout.

## Accepted immutable candidate

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` contains the tracked Release marker `release/v3-release-candidate.json`. It was not amended after CI started and remains the immutable Release phase-end evidence anchor.

| Gate | Result |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Linux integration | `34303586778` — SUCCESS, required complete scope |
| Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Deterministic reference PDF | PASS; 2 builds; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| PDF/A / Unicode / embedding | PASS in complete release contract |
| Distribution artifacts/checksums | PASS; exact four ZIPs + `SHA256SUMS`; archive integrity PASS |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`; item 33 remains fail-closed |
| Temporary executors/assets | absent from candidate/public bundles |

A workflow conclusion alone was not used as acceptance: the complete scope and `SCOPE=complete PASS=38 FAIL=0 SKIP=0` summary were verified from the release job log.

## Retained artifact provenance

The candidate's Linux release check retained:

- distribution artifact ID `10086299397`, name `abntexto-ufc-v3.0.0-distribution-34303586773`, size 11272152 bytes, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222`;
- validation artifact ID `10086298601`, name `linux-release-validation-34303586773`, size 481557 bytes, digest `sha256:124f692d571dde12754a6b084075b4acff29d47ffcfb4fb9d321cc8f1934d18c`.

The distribution artifact was independently downloaded after CI completion. The downloaded artifact SHA-256 matched GitHub metadata. Extraction yielded exactly the four expected ZIPs plus `SHA256SUMS`; `sha256sum -c SHA256SUMS` and ZIP integrity checks passed. No archive was rebuilt.

## Accepted publication checksums

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |

## Canonical merge result

Post-CI acceptance documentation was merged with Release work through PR #293. Repository settings disallow merge commits and rebase merges, so the accepted path was the repository-supported squash merge. Canonical `main` is now `add52f2183f18d6cea3e9477f2a45416a13cfc36`.

This squash merge does not replace candidate `75ead435...` as the phase-end evidence anchor and does not authorize rebuilding publication archives.

## Publication boundary

The Release phase-end regression is accepted and PR #293 is merged, but Release remains ACTIVE. Remaining actions are:

1. synchronize this merge fact in the canonical control plane;
2. create `v3.0.0` tag and GitHub Release from canonical merged state while attaching the exact retained candidate bytes;
3. verify published hashes against the accepted checksums;
4. run current CTAN `pkgcheck`; perform/record actual CTAN submission only as an explicit action with receipt/evidence;
5. synchronize final publication facts and perform final Release verification before setting Release to CLOSED.

## Regression discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**. The accepted immutable candidate remains the Release regression evidence anchor through publication closeout.

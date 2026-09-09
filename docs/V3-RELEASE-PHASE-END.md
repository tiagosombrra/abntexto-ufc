# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: ACCEPTED — PUBLICATION CLOSEOUT PENDING

## Purpose

This document records the immutable Release phase-end candidate and the evidence boundary used through final publication closeout.

## Accepted immutable candidate

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` contains the tracked Release marker `release/v3-release-candidate.json`. It was not amended after CI started and remains the immutable Release phase-end evidence anchor.

| Gate | Result |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Linux integration | `34303586778` — SUCCESS, required complete scope |
| Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Deterministic reference PDF | PASS; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| PDF/A / Unicode / embedding | PASS in complete release contract |
| Distribution artifacts/checksums | PASS; exact four ZIPs + `SHA256SUMS`; archive integrity PASS |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`; item 33 remains fail-closed |

## Retained artifact provenance

The candidate's Linux release check retained distribution artifact ID `10086299397`, name `abntexto-ufc-v3.0.0-distribution-34303586773`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222`.

The artifact was independently downloaded and verified. Extraction yielded exactly the four expected ZIPs plus `SHA256SUMS`; checksum and ZIP-integrity checks passed. No archive was rebuilt.

## Merge and synchronization result

| Event | Result |
|---|---|
| Release integration PR #293 | merged by squash as `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout synchronization PR #294 | merged as `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Canonical post-merge Static | `34333350711` — SUCCESS |
| Release work branch | `release/v3-release`, synchronized to the canonical `main` checkpoint |
| Superseded PR #292 | closed; historical evidence only |

These later control-plane commits do not replace candidate `75ead435...` as the phase-end evidence anchor and do not authorize rebuilding publication archives.

## Publication boundary

The **phase-end regression** is accepted, but Release remains ACTIVE. Remaining actions are:

1. create `v3.0.0` tag and GitHub Release from canonical `main` while attaching the exact retained candidate bytes;
2. verify published hashes against accepted checksums;
3. run current CTAN `pkgcheck`; perform/record actual CTAN submission only as an explicit action with evidence;
4. synchronize final publication facts and perform final Release verification before setting Release to `CLOSED`.

## Regression discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks never replace the accepted **phase-end regression**. The immutable candidate remains the Release evidence anchor through publication closeout.

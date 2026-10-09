# Release state

This file is the durable human-readable release-state authority for the repository.

## Published release

| Fact | State |
|---|---|
| Latest GitHub release | `v3.0.4` |
| Publication state | `PUBLISHED` |
| Published source SHA | `7e176fd5472925b519d469a9a756330f4851f0b3` |
| Annotated tag | `v3.0.4` |
| Annotated tag object SHA | `184b00ad2eaed8a98e6b17033e7623efb3e53571` |
| GitHub Release ID | `392476983` |
| Published at | `2026-09-20T15:29:02Z` |
| Maintainer visual acceptance | PASS — 2026-09-20 |
| CTAN v3.0.4 | published/accepted 2026-09-22 from the exact 2026-09-20 submission — issue #356 |
| Active development line | `v3.0.5` — candidate-source preparation, `UNRELEASED` / `NOT_FROZEN` — issue #471 / PR #472 |

The current `main` branch may contain control/documentation commits made after publication. Those commits do not alter the published v3.0.4 source, annotated tag, release assets or checksums.

## Certified v3.0.4 publication evidence

The published source `7e176fd5472925b519d469a9a756330f4851f0b3` passed:

- Static Contract #675;
- Linux Integration #582;
- Linux Release Check #233 / run `35510145977`;
- complete regression `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- CTAN `pkgcheck 4.1.0`;
- canonical-reference reproducibility;
- PDF/A-2b, embedded-font, Unicode and repository-PDF validation;
- seven supported-profile review preflights;
- explicit maintainer visual acceptance.

The annotated tag `v3.0.4` resolves exactly to that source SHA. GitHub Release ID `392476983` was published at `2026-09-20T15:29:02Z`.

Published release assets are immutable project evidence and must not be rebuilt or replaced:

- `abntexto-ufc-3.0.4.zip` — `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec`;
- `abntexto-ufc-template-3.0.4.zip` — `3412c0c63a85d340ec7789da509e1f6a2994efa1974207f3d79ac402a3aa159c`;
- `abntexto-ufc-overleaf-3.0.4.zip` — `4967ce1407e8b42b0a77ab688edbe9e759a64827e566f52d7864cb1f6118cf92`;
- `SHA256SUMS` — `a1aeb3f0c75449811677aaa6b11ee954cef3a253bd492433f066ba3ffea4f4d3`.

GitHub-reported asset digests were independently verified against those frozen values and matched exactly.

## Current repository lifecycle

GitHub publication of v3.0.4 is complete. Release issue #353 is completed and closed. Phase 10A / issue #469 selected v3.0.5 as the maintenance line and merged as `9aeed2cd57665bf4ec6d13990b88d8b779de22a1`. Phase 10B / issue #471 / PR #472 now prepares the exact publication-source candidate.

v3.0.5 remains `UNRELEASED`, `NOT_FROZEN` and `UNPUBLISHED` with no frozen candidate SHA and no publication authorization in the machine marker. Phase 10C has now received explicit maintainer ACCEPT for one exact certified source; Phase 10D must still perform a separately validated control-plane freeze before tag/publication. Phase 10B finalizes release-source content before candidate selection: the canonical changelog is dated, while `CITATION.cff` continues to describe the latest actually published release v3.0.4. The exact merged #472 SHA must be recertified before it can be offered for maintainer visual acceptance.

The root machine receipt `release/v3-release-candidate.json` represents this active development state while embedding the immutable v3.0.4 publication receipt. Completed v3.0.3 and v3.0.4 release receipts remain preserved under `release/history/v3/`, and the detailed v3.0.4 publication receipt remains under `docs/history/v3/release/`.

CTAN publication is a separate external operation tracked by issue #356. The exact `abntexto-ufc-3.0.4.zip` asset from GitHub Release v3.0.4, SHA-256 `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec`, was submitted on 2026-09-20 as an update from CTAN version 3.0.2 to 3.0.4. The official CTAN-ann update on 2026-09-22 confirms version 3.0.4 publication/acceptance. Repository control therefore records CTAN state `PUBLISHED` and acceptance state `ACCEPTED`; the submitted archive remains immutable and must not be rebuilt or replaced.

Previous GitHub release v3.0.3 remains immutable. Its machine receipt is preserved at `release/history/v3/v3.0.3-release-candidate.json`.

## Active v3.0.5 maintenance line

| Fact | State |
|---|---|
| Development version | `3.0.5` |
| Candidate-preparation entry SHA | `9aeed2cd57665bf4ec6d13990b88d8b779de22a1` |
| Tracking issue / PR | #471 / #472 |
| Candidate state | `NOT_FROZEN` |
| Candidate SHA | none |
| Publication state | `UNPUBLISHED` |
| Publication authorized | no |
| Canonical changelog | `3.0.5 — 2026-10-06` |
| Published citation metadata | remains v3.0.4 until an actual future publication |

10B prepares, but does not freeze, the publication source. After #472 merges, its exact merge SHA becomes the only source eligible for fresh Static, complete Linux Integration, Linux Release/CTAN/review-artifact and portability certification. Phase 10C then requires explicit maintainer visual acceptance of artifacts from that same SHA. Freeze, tag and publication remain prohibited until that acceptance is recorded.

## Authority order

When facts disagree, use this order:

1. current Git facts and GitHub release/tag state;
2. `release/v3-release-candidate.json` machine receipt;
3. this file;
4. current durable technical documentation;
5. controlled historical evidence under `docs/history/v3/` and `release/history/v3/`.

Closed Issues and historical release documents are audit evidence, not active authority.

## Explicit v3.0.5 maintainer ACCEPT — 2026-10-09

The maintainer explicitly approved exact certified candidate source `407f279a78df3824b27585d0e86d688c19cd90ee` and seven-profile review artifact ID `11415094731` (digest `sha256:23193aaaacdb2af7b465e4ddae17428344d1ac1d65d5dcc1b7089cf7bb342fa4`) through issue #474. The review artifact was produced by Linux Release Check #306 / run `37467235323`, with full Static #945, Linux Integration #798, Windows #20 and macOS #12 certification.

**Human acceptance is complete; freeze and publication are not.** Issue #475 owns the next step. The current `release/v3-release-candidate.json` remains `NOT_FROZEN`, `candidate_sha=null`, `publication_authorized=false` and `UNPUBLISHED` until a separate freeze-control PR and its required gates pass. The future annotated `v3.0.5` tag must peel to the accepted source SHA, not to a subsequent documentation/control commit. The retained distribution set is artifact `11416117138`; it must be verified and reused byte-for-byte without rebuilding. The published v3.0.4 tag/assets remain immutable and CTAN v3.0.5 is a separate future operation.

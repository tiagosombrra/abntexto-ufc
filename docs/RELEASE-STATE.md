# Release state

This file is the durable human-readable release-state authority for the repository.

## Published release

| Fact | State |
|---|---|
| Latest GitHub release | `v3.0.3` |
| Publication state | `PUBLISHED` |
| Frozen source SHA | `b98270f23b1b384773c409869dfb05d71acd8638` |
| Annotated tag | `v3.0.3` |
| GitHub Release ID | `391878053` |
| Published at | `2026-09-19T01:48:03Z` |
| Maintainer visual acceptance | PASS |
| CTAN v3.0.3 | deferred external follow-up |
| Active development candidate | none |

The current `main` branch may contain repository-maintenance changes made after publication. Those changes do not alter the already-published v3.0.3 source, tag, release assets or checksums.

## Certified v3.0.3 source evidence

The frozen source `b98270f23b1b384773c409869dfb05d71acd8638` passed:

- Static Contract #602;
- Linux Integration #514;
- Linux Release Check #186 / run `35279315637`;
- complete regression `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- CTAN `pkgcheck 4.1.0`;
- canonical-reference reproducibility, PDF/A-2b, embedded-font, Unicode and repository-PDF validation;
- seven supported-profile preflights;
- explicit maintainer visual acceptance.

Published release assets are immutable project evidence and must not be rebuilt or replaced:

- `abntexto-ufc-3.0.3.zip` — `315b39208c52ce2d3f18f9f8c6b3be3b4f7d574d03bf2ebb405fb3a9cb0a091a`;
- `abntexto-ufc-template-3.0.3.zip` — `89e90a49f50f28653bdce1643ffd305b345c9a61ef53804edb5f7a48828ea164`;
- `abntexto-ufc-overleaf-3.0.3.zip` — `32c32bf3e84e8d77db47fa6c433bb5f458ebc789980ae8eb554814af3cbdbb81`;
- `SHA256SUMS` — `c526a8f6cc8a51ca3cdd289e3078f23d2c747c3af1b4a55d2b5dd04c67cde95d`.

## Current repository lifecycle

The repository is in post-v3.0.3 steady state. No unreleased runtime development line is active yet.

Repository-maintenance work may improve documentation, governance, CI, repository layout and contributor experience without changing the published v3.0.3 release. Any future runtime or public-API change must open a new unreleased development line and must never retarget or mutate existing version tags/releases.

## Authority order

When facts disagree, use this order:

1. current Git facts and GitHub release/tag state;
2. `release/v3-release-candidate.json` machine receipt;
3. this file;
4. current durable technical documentation;
5. controlled historical evidence under `docs/history/v3/` and `release/history/v3/`.

Closed Issues and historical release documents are audit evidence, not active authority.

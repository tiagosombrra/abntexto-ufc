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
| Frozen release candidate | `v3.0.4` — FROZEN / publication authorized |

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

The published baseline remains v3.0.3. Repository modernization issue #335 is completed and release issue #353 now governs v3.0.4 publication.

v3.0.4 is frozen on exact certified source SHA `7e176fd5472925b519d469a9a756330f4851f0b3`. That source passed Static Contract #675, Linux Integration #582 and Linux Release Check #233 / run `35510145977`, including complete regression `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, CTAN `pkgcheck 4.1.0`, canonical-reference reproducibility, distribution validation and seven-profile preflight.

The maintainer explicitly accepted the exact final review artifacts on 2026-09-20. Publication is authorized. The later control-plane commit recording this freeze is not the publication source. Annotated tag `v3.0.4` must point exactly to the frozen SHA above, and GitHub Release publication must use only the retained certified distribution bytes from Linux Release Check #233.

Published v3.0.3 tags/releases/assets remain immutable.

## Frozen v3.0.4 candidate evidence

| Fact | State |
|---|---|
| Frozen source SHA | `7e176fd5472925b519d469a9a756330f4851f0b3` |
| Static Contract | #675 — PASS |
| Linux Integration | #582 — PASS |
| Linux Release Check | #233 / run `35510145977` — PASS |
| Complete regression | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| CTAN pkgcheck | `4.1.0 PASS` |
| Canonical reference SHA-256 | `24ec1e9eab489f8d8453c6e1b79978f8d26bf7a3ce37ec96ff676d46482e1089` |
| Seven-profile review preflight | PASS |
| Maintainer visual acceptance | PASS — 2026-09-20 |
| Candidate state | `FROZEN` |
| Publication state | `AUTHORIZED` |

Certified distribution hashes from Linux Release Check #233:

- `abntexto-ufc-3.0.4.zip` — `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec`;
- `abntexto-ufc-template-3.0.4.zip` — `3412c0c63a85d340ec7789da509e1f6a2994efa1974207f3d79ac402a3aa159c`;
- `abntexto-ufc-overleaf-3.0.4.zip` — `4967ce1407e8b42b0a77ab688edbe9e759a64827e566f52d7864cb1f6118cf92`;
- `SHA256SUMS` — `a1aeb3f0c75449811677aaa6b11ee954cef3a253bd492433f066ba3ffea4f4d3`.

Visual regression against the previously approved set found zero changed rendered pages across all 71 profile pages and the 22-page canonical reference. The maintainer then explicitly approved the exact final candidate artifacts.

These certified bytes are the only permitted GitHub Release publication assets for v3.0.4. Do not rebuild them.

## Authority order

When facts disagree, use this order:

1. current Git facts and GitHub release/tag state;
2. `release/v3-release-candidate.json` machine receipt;
3. this file;
4. current durable technical documentation;
5. controlled historical evidence under `docs/history/v3/` and `release/history/v3/`.

Closed Issues and historical release documents are audit evidence, not active authority.

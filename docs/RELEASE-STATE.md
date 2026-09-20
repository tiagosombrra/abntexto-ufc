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
| CTAN v3.0.4 | submitted 2026-09-20; acceptance/publication pending — issue #356 |
| Active development line | none selected |

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

GitHub publication of v3.0.4 is complete. Release issue #353 is completed and closed; no v3.0.5 or other future development line has been selected. Repository-wide maintenance and organization improvements are tracked separately in issue #359 and do not by themselves select a future runtime development line.

The root machine receipt `release/v3-release-candidate.json` represents the current published steady state. Completed v3.0.3 and v3.0.4 release receipts are preserved under `release/history/v3/`, and the detailed v3.0.4 publication receipt is preserved under `docs/history/v3/release/`.

CTAN publication is a separate external operation tracked by issue #356. The exact `abntexto-ufc-3.0.4.zip` asset from GitHub Release v3.0.4, SHA-256 `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec`, was submitted on 2026-09-20 as an update from the CTAN-published version 3.0.2 to 3.0.4. CTAN acceptance/publication remains pending. Do not rebuild or replace the submitted archive.

Previous GitHub release v3.0.3 remains immutable. Its machine receipt is preserved at `release/history/v3/v3.0.3-release-candidate.json`.

## Authority order

When facts disagree, use this order:

1. current Git facts and GitHub release/tag state;
2. `release/v3-release-candidate.json` machine receipt;
3. this file;
4. current durable technical documentation;
5. controlled historical evidence under `docs/history/v3/` and `release/history/v3/`.

Closed Issues and historical release documents are audit evidence, not active authority.

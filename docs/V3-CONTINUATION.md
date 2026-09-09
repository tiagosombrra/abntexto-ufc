# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE — GITHUB PUBLISHED / ALL-PROFILE VISUAL VALIDATION ACTIVE / CTAN BLOCKED

This file is the shortest safe entry point for continuing v3 work from a new ChatGPT conversation, Codex session or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Released source | `05399473827da7cf6b6c8bac36edc7115481773f` |
| Immutable tag | `v3.0.0` → `05399473827da7cf6b6c8bac36edc7115481773f` |
| GitHub Release | **PUBLISHED** — https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0 |
| Final distribution artifact | `10117679639` (`sha256:7ee1b6bf4b1d54ac041db1e624d8bfcf52a1dc43897c1542b9fd969b971f40df`) |
| Canonical CTAN upload | `abntexto-ufc-3.0.0.zip` (`sha256:d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71`) |
| CTAN runtime contract | one generated `abntexto-ufc.cls`; **zero project-owned `.def` files** |
| `pkgcheck` | **PASS** — 4.1.0, exit 0, zero warnings/errors; run `34386932488` |
| GitHub publication verification | **PASS** — run `34387825056`; evidence artifact `10118391678` |
| All-profile visual validation | **ACTIVE — seven source/PDF pairs required** |
| Maintainer acceptance | **PENDING** |
| CTAN status | **BLOCKED — do not submit before maintainer visual acceptance** |

For released-source authority, resolve `v3.0.0`; do not treat a later post-tag `main` commit as the v3.0.0 implementation.

## What publication hardening already closed

- stale v2/pre-publication text removed from public distribution documentation;
- CTAN README finalized for 3.0.0;
- package id `abntexto-ufc` established;
- UFC institutional marks and proprietary Microsoft fonts excluded fail-closed;
- canonical CTAN package reduced to one generated project-owned class file;
- all tracked `.def` runtime modules are inlined deterministically for CTAN only;
- any `.def` inside the CTAN ZIP is a hard failure;
- example compiles without the modular runtime directory;
- former NBR 6023:2025 librarian item 33 closed with primary authority and executable regression;
- `pkgcheck` passed before immutable tag creation;
- immutable `v3.0.0` and GitHub Release publication completed with byte-identical re-download verification.

## Active visual-validation scope

Generate from the frozen `v3.0.0` implementation and present both source and PDF for:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

The review artifact must include a manifest/hashes and build metadata. Automated compile success is insufficient: explicit maintainer review of the rendered pages and sources is mandatory. See `docs/V3-VISUAL-VALIDATION.md`.

## Remaining work

1. generate the seven source/PDF review pairs from the immutable v3.0.0 implementation;
2. provide them to the maintainer for visual/source inspection;
3. record explicit acceptance or findings profile by profile;
4. if a material defect is found, do not modify v3.0.0; open a correction/new-version cycle and repeat affected gates;
5. only after visual acceptance, verify the frozen CTAN ZIP SHA-256 `d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71` and submit that one archive to CTAN;
6. preserve CTAN submission receipt and package metadata;
7. after CTAN acceptance, verify catalog/install evidence;
8. update control docs/machine state and close the Release phase.

No v3.0.0 source or asset rebuild is permitted.

## Local continuation

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
git rev-parse v3.0.0^{}
```

Then read:

1. `AGENTS.md`
2. `release/v3-roadmap.json`
3. `docs/V3-CONTINUATION.md`
4. `docs/HANDOFF-V3.0.0.md`
5. `docs/ROADMAP-V3.0.0.md`
6. `docs/V3-RELEASE-READINESS.md`
7. `docs/V3-VISUAL-VALIDATION.md`
8. `docs/V3-RELEASE-PHASE-END.md`
9. `docs/CTAN-RELEASE.md`
10. `docs/UFC-LIBRARIAN-REVIEW.md`

Every material repository modification updates the affected control documents and machine state in the same work cycle. The public README is updated only when user-facing facts change; it does not track transient branch/CI state.

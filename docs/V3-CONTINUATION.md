# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE — GITHUB PUBLISHED / CTAN PENDING

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
| CTAN status | **NOT YET CLAIMED — submission/acceptance pending** |

For released-source authority, resolve `v3.0.0`; do not treat a later post-tag `main` commit as the v3.0.0 source.

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
- `pkgcheck` moved before immutable tag creation.

PR #297 final-head evidence was green: Static PASS, Linux integration PASS, Linux release check PASS with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. The generated CTAN artifact was manually audited and confirmed `1 cls / 0 def`.

## Remaining work

1. obtain the exact `abntexto-ufc-3.0.0.zip` asset from the published GitHub Release;
2. verify SHA-256 `d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71`;
3. submit only that archive to CTAN;
4. preserve submission receipt and package metadata;
5. after CTAN acceptance, verify catalog/install evidence;
6. update control docs/machine state and close the Release phase.

No v3.0.0 source or asset rebuild is permitted.

## Local continuation

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
```

Then read:

1. `AGENTS.md`
2. `release/v3-roadmap.json`
3. `docs/V3-CONTINUATION.md`
4. `docs/HANDOFF-V3.0.0.md`
5. `docs/ROADMAP-V3.0.0.md`
6. `docs/V3-RELEASE-READINESS.md`
7. `docs/V3-RELEASE-PHASE-END.md`
8. `docs/CTAN-RELEASE.md`
9. `docs/UFC-LIBRARIAN-REVIEW.md`

Every material repository modification updates the affected control documents and machine state in the same work cycle. The public README is updated only when user-facing facts change; it does not track transient branch/CI state.

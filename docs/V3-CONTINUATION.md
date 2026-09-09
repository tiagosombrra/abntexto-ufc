# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE — FINAL EXACT-MAIN RECERTIFICATION

This file is the shortest safe entry point for continuing v3 work from a new ChatGPT conversation, Codex session or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` — resolve current SHA dynamically from `origin/main` |
| Active roadmap phase | **Release** |
| Publication hardening | **MERGED** via PR #297 |
| Integration anchor | `25c6ab09dc38be9257d2912652074a48886d28f9` |
| Final candidate semantics | the exact `main` commit containing this post-merge control-plane synchronization, after it passes final recertification |
| Previous Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Previous retained artifact | ID `10086299397` — historical evidence only; never publish |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| Package id | `abntexto-ufc` |
| CTAN upload contract | exactly one archive: `abntexto-ufc-3.0.0.zip` |
| CTAN runtime contract | exactly one generated `abntexto-ufc.cls`; **zero project-owned `.def` files** |
| Tag contract | `v3.0.0` must point to the exact final certified `main` SHA |
| pkgcheck contract | current CTAN `pkgcheck` must pass before tag creation |

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

1. merge this post-merge documentation/machine-state synchronization;
2. resolve the exact resulting `origin/main` SHA;
3. run final phase-end regression on exactly that SHA;
4. retain and audit the resulting deterministic distribution;
5. run the current CTAN `pkgcheck` on the exact canonical ZIP;
6. freeze hashes/evidence;
7. create immutable `v3.0.0` on the same certified SHA;
8. create GitHub Release with exact frozen assets and verify re-downloaded hashes;
9. submit only `abntexto-ufc-3.0.0.zip` to CTAN;
10. preserve submission/acceptance evidence and close Release only after external verification.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

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

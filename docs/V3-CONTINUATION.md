# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE — FINAL HUMAN / PKGCHECK GATES

This file is the shortest safe entry point for continuing v3 work from a new ChatGPT conversation, Codex session or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` — always resolve current SHA dynamically from Git |
| Active roadmap phase | **Release** |
| Publication hardening | **MERGED** via PR #297 |
| Post-hardening control synchronization | **MERGED** via PR #298, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Active final-gate branch | `release/v3-final-human-gate-v2` until merged |
| Previous Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN upload contract | exactly one archive: `abntexto-ufc-3.0.0.zip` |
| CTAN runtime contract | exactly one generated `abntexto-ufc.cls`; **zero project-owned `.def` files** |
| pkgcheck contract | current CTAN `pkgcheck` runs inside final Linux release gate before tag |
| Human gate | final PDF + `.tex` for seven supported profiles; explicit maintainer approval required |
| Tag contract | final certified SHA = visually approved SHA = `v3.0.0` SHA = publication source SHA |

## What is already closed

- stale v2/pre-publication release text fixed;
- package id `abntexto-ufc` finalized;
- UFC marks and proprietary Microsoft font files excluded from CTAN;
- CTAN runtime reduced to one generated class with all 14 project modules inline and zero `.def` files;
- isolated CTAN example compile and deterministic distribution established;
- NBR 6023:2025 librarian item 33 closed with primary authority and executable regression;
- post-hardening exact-main baseline `25c6ab09...` passed `SCOPE=complete PASS=38 FAIL=0 SKIP=0` in run `34355988612`;
- PR #298 aligned the exact-main recertification control plane.

## Preliminary visual review

A preliminary seven-profile set was generated from the certified post-hardening baseline using the pinned Overleaf/release dependency set. All seven PDFs passed A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight and page-by-page assistant inspection.

This does **not** close the final human gate: the final pairs must be regenerated from the exact SHA that will be tagged and explicitly approved by the maintainer.

Required profiles:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

## Remaining work

1. merge `release/v3-final-human-gate-v2` through protected `main`;
2. resolve the exact resulting `origin/main` SHA;
3. require Static + automatic complete Linux integration + Linux release check on that SHA;
4. require current CTAN `pkgcheck` output/version/archive-hash evidence from that same release run and classify warnings;
5. retain and physically audit the resulting deterministic distribution;
6. regenerate the seven final PDF/`.tex` pairs from that exact candidate and obtain explicit maintainer approval;
7. freeze hashes/evidence;
8. create immutable `v3.0.0` on the same certified and visually approved SHA;
9. create GitHub Release with exact frozen assets and verify re-downloaded hashes;
10. submit only `abntexto-ufc-3.0.0.zip` to CTAN;
11. preserve submission/acceptance/install evidence and close Release only after external verification.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Windows literal-font scope

Retained Windows/literal-font evidence remains scope-valid while final changes do not alter font runtime, font setup, engine behavior or the Windows certification contract. Any such change forces a fresh Windows recertification.

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
3. `release/v3-release-candidate.json`
4. `docs/V3-CONTINUATION.md`
5. `docs/HANDOFF-V3.0.0.md`
6. `docs/V3-RELEASE-READINESS.md`
7. `docs/V3-RELEASE-PHASE-END.md`
8. `docs/CTAN-RELEASE.md`
9. `docs/UFC-LIBRARIAN-REVIEW.md`

Every material repository modification updates affected control documents and machine state in the same work cycle. The public README is updated only when user-facing facts change; it does not track transient branch/CI state.
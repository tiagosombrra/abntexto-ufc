# abntexto-ufc v3 — Canonical Handoff for Release Recovery 3.0.1

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; always resolve exact candidate SHA dynamically from Git |
| Active phase | **Release — 3.0.1 recovery / exact-main recertification pending** |
| Recovery work branch | `release/v3.0.1-recovery` — short-lived branch |
| Publication hardening | merged through PR #297 |
| Post-hardening control synchronization | merged through PR #298, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Final release-gate controls | merged through PR #301 as `395899e1b2336ed268335d68e59e03452880c15e` |
| Pre-recovery exact-main evidence | Linux release run `34419086322`: `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; current CTAN `pkgcheck` PASS |
| Public `v3.0.0` | exists on `05399473827da7cf6b6c8bac36edc7115481773f`; premature/superseded for final publication |
| Recovery target | `3.0.1`; do not silently retarget the existing `v3.0.0` tag |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN archive | one canonical upload file: `abntexto-ufc-3.0.1.zip` |
| CTAN runtime | one generated `abntexto-ufc.cls`; zero project-owned `.def` files |
| Human acceptance | seven exact-candidate PDF/`.tex` pairs require explicit maintainer approval |
| Final tag rule | certified SHA = visually approved SHA = `v3.0.1` SHA = publication source SHA |

`docs/V3-CONTINUATION.md` is the shortest continuation entry point. `docs/V3-RELEASE-RECOVERY.md` is the authority for the 3.0.1 recovery decision. Memory and hardcoded old SHAs are not Git authority.

## Accepted historical evidence

PR #297 closed the publication-shape defects and preserved the modular-source/monolithic-CTAN design. Its protected merge produced `25c6ab09dc38be9257d2912652074a48886d28f9`; exact-main run `34355988612` demonstrated `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, deterministic distribution, one generated CTAN class, zero project-owned `.def` files and all 14 tracked runtime modules inlined exactly once.

PR #298 synchronized the post-hardening control plane. PR #301 then integrated the executable current-CTAN `pkgcheck` gate and the mandatory seven-profile human visual gate. Exact-main run `34419086322` on `395899e1b2336ed268335d68e59e03452880c15e` passed the complete release matrix and current CTAN `pkgcheck` and retained both validation and distribution artifacts.

That SHA is not the recovered final candidate because the later 3.0.1 version/control changes alter class identity metadata and publication bytes. It is pre-recovery baseline evidence only.

## Release recovery boundary

A public GitHub `v3.0.0` tag and Release exist for the earlier SHA `05399473827da7cf6b6c8bac36edc7115481773f`. That public state violates the later exact-SHA publication invariant and must not be rewritten silently as if the tag had always identified the final candidate.

The recovery decision is therefore:

- preserve `v3.0.0` as historical/premature publication evidence;
- classify its public assets as superseded for final publication and ineligible for CTAN submission;
- recover under `v3.0.1`;
- preserve all previously accepted runtime, normative, API and librarian-review semantics;
- rerun the exact-SHA Release certification because version metadata and archive bytes change.

## Mandatory final seven-profile review

Before the 3.0.1 tag/freeze, present PDF and corresponding `.tex` source for:

1. undergraduate capstone;
2. specialization capstone;
3. master's thesis;
4. doctoral thesis;
5. research project;
6. anonymized research project;
7. scientific article.

All final pairs must come from the same exact 3.0.1 candidate SHA and pinned release dependency set. Required preflight includes A4, PDF/A-2b, embedded fonts and no recognized warnings/overflows. The gate closes only after explicit maintainer approval.

A preliminary set from `25c6ab09...` already passed 7/7 automated preflight and page-by-page assistant inspection. It remains preliminary because the recovered final candidate will be a later tracked state.

## CTAN package contract

```text
abntexto-ufc/
├── README.md
├── CHANGELOG
├── LICENSE
├── abntexto-ufc.cls
├── abntexto-ufc.tex
├── abntexto-ufc.pdf
├── abntexto-ufc-example.tex
└── abntexto-ufc-example.pdf
```

Hard invariants: one project-owned runtime class; zero `.def` files; no nested project runtime directory; every tracked runtime module inlined exactly once; isolated example compile; no UFC marks, proprietary Microsoft fonts, vendored `abntexto.cls` or repository engineering infrastructure in CTAN.

Only `abntexto-ufc-3.0.1.zip` is submitted to CTAN. Template and Overleaf ZIPs are GitHub Release conveniences.

## Remaining Release work

1. merge the 3.0.1 recovery changes to canonical `main`;
2. resolve the resulting exact `main` SHA;
3. require Static, automatic complete Linux integration and Linux release check — including current CTAN `pkgcheck` — on that SHA;
4. retain and physically re-audit deterministic 3.0.1 distribution bytes;
5. regenerate all seven exact-candidate PDF/`.tex` review pairs and obtain explicit maintainer approval;
6. freeze hashes/evidence;
7. create immutable `v3.0.1` on the same certified and visually approved SHA;
8. create GitHub Release and verify re-downloaded hashes;
9. submit only canonical 3.0.1 ZIP to CTAN;
10. retain receipt/acceptance/install evidence;
11. synchronize final publication facts and close Release.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## Windows/literal-font evidence

Retained Windows literal-font certification remains scope-valid because the recovery does not alter font runtime or engine behavior. Any font/engine/certification-relevant implementation change before freeze forces a fresh Windows run.

Every **material advance** updates affected documentation and machine state in the same work cycle. Targeted checks never replace the required **phase-end regression**. No build, tag or submission is treated as CTAN acceptance without explicit external evidence.

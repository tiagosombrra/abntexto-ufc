# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE — FINAL HUMAN/PUBLICATION GATES

This file is the shortest safe entry point for continuing v3 work from a new ChatGPT conversation, Codex session or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` — resolve current SHA dynamically from `origin/main` |
| Active roadmap phase | **Release** |
| Active control branch | `release/v3-final-human-gate` until merged |
| Post-hardening baseline | `25c6ab09dc38be9257d2912652074a48886d28f9` |
| Post-hardening full release run | `34355988612` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Distribution artifact | `10106606462`, digest `sha256:4eed74eaec5d076cea6fb140b533403ce065b8008a21dc80186763acad7b8340` |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN upload contract | exactly one archive: `abntexto-ufc-3.0.0.zip` |
| CTAN runtime contract | exactly one generated `abntexto-ufc.cls`; **zero project-owned `.def` files** |
| Development runtime | modular repository source retained; monolithization is CTAN-only |
| Human gate | seven PDF/`.tex` profile pairs require explicit maintainer approval before tag |
| pkgcheck contract | current announced CTAN `pkgcheck` must pass before tag |
| Tag contract | `v3.0.0` must point to the exact certified + visually approved final `main` SHA |

## What is already closed

- publication-hardening PR merged;
- NBR 6023:2025 librarian item 33 closed with executable evidence;
- complete post-merge release regression passed on `25c6ab09...`;
- scientific article PDF/A-2b gate passed;
- deterministic three-ZIP distribution passed;
- canonical CTAN package physically audited as one top-level directory with exactly eight files;
- generated CTAN class contains all 14 project runtime modules inline and ships zero `.def` files;
- no UFC marks or proprietary Microsoft font files are redistributed.

## Why another exact-main pass is still required

Release-control documentation was stale after the hardening merge and is being synchronized in `release/v3-final-human-gate`. Once this tracked change is merged, `main` will have a new SHA. The final v3 invariant therefore requires recertifying the resulting exact SHA rather than tagging the older baseline.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Final human review set

Before tag/freeze, generate and present PDF + `.tex` for:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

The final set must be tied to the eventual post-merge candidate SHA. A preliminary set from `25c6ab09...` already passed A4/PDF-A-2b/font-embedding/warning preflight and visual inspection, but it does not replace final exact-candidate approval.

## Remaining work

1. merge `release/v3-final-human-gate` through protected `main`;
2. resolve the new exact `origin/main` SHA;
3. run Static + complete Linux release regression on that SHA;
4. regenerate/audit the exact distribution and checksums;
5. run current CTAN `pkgcheck` (currently announced 4.1.0 dated 2026-08-05) and retain full evidence;
6. regenerate the seven final review pairs from that SHA and obtain explicit maintainer approval;
7. freeze publication bytes/hashes;
8. create immutable `v3.0.0` on the same SHA;
9. create GitHub Release with exact frozen assets, re-download and verify hashes;
10. submit only `abntexto-ufc-3.0.0.zip` to CTAN;
11. retain CTAN receipt/acceptance/install evidence and only then close Release.

## Windows literal-font scope

Retained Windows/literal-font certification remains valid while final changes do not alter `abntexto-ufc/fonts.def`, font setup, engine behavior or the Windows certification contract. Any such change forces a new Windows recertification.

## Local continuation

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
```

Then read, in order:

1. `AGENTS.md`
2. `release/v3-roadmap.json`
3. `release/v3-release-candidate.json`
4. `docs/V3-CONTINUATION.md`
5. `docs/V3-RELEASE-READINESS.md`
6. `docs/CTAN-RELEASE.md`
7. `docs/HANDOFF-V3.0.0.md`
8. `docs/UFC-LIBRARIAN-REVIEW.md`

Every material advance updates the relevant control documents in the same work cycle. Targeted checks never replace the exact-candidate release regression.
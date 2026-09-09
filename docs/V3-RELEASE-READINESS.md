# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — FINAL EXACT-MAIN RECERTIFICATION

## Phase readiness

| Phase | State | Evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | technical/runtime certification accepted |
| Release | **ACTIVE** | publication hardening merged; final exact-main recertification + pkgcheck/tag/publication pending |

## Completed Release hardening

PR #297 was merged through protected `main`. Its final head passed Static, Linux integration and Linux release check with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.

The merged work:

- replaced stale v2/pre-publication distribution documentation;
- finalized CTAN metadata for v3.0.0;
- closed former librarian item 33 against primary ABNT NBR 6023:2025 authority;
- made `abntexto-ufc-3.0.0.zip` the only CTAN upload archive;
- generated one monolithic `abntexto-ufc.cls` from modular project sources;
- made any project-owned `.def` in the CTAN ZIP a hard failure;
- proved isolated compilation without the modular runtime directory;
- excluded UFC marks and proprietary Microsoft fonts fail-closed;
- moved current CTAN `pkgcheck` before immutable tag creation.

The retained pre-merge CTAN artifact was manually inspected and confirmed `1 cls / 0 def`, 14/14 runtime modules inlined exactly once, no residual project-owned `.def` input, no vendored `abntexto.cls`, and no prohibited assets.

## Final-candidate contract

The integration merge commit `25c6ab09dc38be9257d2912652074a48886d28f9` is an integration anchor, not the final taggable SHA, because this control-plane synchronization intentionally follows it.

The next accepted candidate is the exact canonical `main` commit containing this synchronization after it is merged and passes final certification:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

The `Linux integration` workflow now runs automatically on `main` pushes that change `release/v3-release-candidate.json` and forces `scope=complete`, so the post-squash candidate receives complete Linux evidence on its exact SHA. No further pre-tag repository commit is allowed after candidate acceptance without starting a new candidate cycle.

## CTAN final package contract

`abntexto-ufc-3.0.0.zip` must contain exactly one top-level `abntexto-ufc/` directory and these eight files:

```text
README.md
CHANGELOG
LICENSE
abntexto-ufc.cls
abntexto-ufc.tex
abntexto-ufc.pdf
abntexto-ufc-example.tex
abntexto-ufc-example.pdf
```

Hard requirements include one project-owned runtime `.cls`, zero project-owned `.def`, no nested runtime tree, no vendored `abntexto.cls`, no UFC marks, no proprietary Microsoft fonts, no development infrastructure, and successful isolated example compilation.

## Remaining gates

| Order | Gate | State |
|---:|---|---|
| 1 | Publication-hardening integration | **PASS / MERGED** |
| 2 | Post-merge control-plane synchronization + exact-main Linux trigger | **IN PROGRESS** |
| 3 | Resolve exact resulting `main` SHA | BLOCKED BY 2 |
| 4 | Static + automatic `scope=complete` Linux integration + Linux release check on exact SHA | BLOCKED BY 3 |
| 5 | Build/retain deterministic three-ZIP distribution + `SHA256SUMS` | BLOCKED BY 4 |
| 6 | Re-audit final CTAN ZIP: one generated class, zero `.def`, isolated compile PASS | BLOCKED BY 5 |
| 7 | Run current CTAN `pkgcheck`; classify every warning | BLOCKED BY 5–6 |
| 8 | Freeze hashes/evidence; prohibit rebuild | BLOCKED BY 7 |
| 9 | Create immutable `v3.0.0` on the certified SHA | BLOCKED BY 8 |
| 10 | Create GitHub Release and re-download/hash-verify assets | BLOCKED BY 9 |
| 11 | Submit only canonical ZIP to CTAN; preserve receipt/acceptance evidence | BLOCKED BY 7–10 |
| 12 | Synchronize post-publication facts and close Release | BLOCKED BY 1–11 |

## Current blockers

- this control-plane synchronization has not yet been merged to `main`;
- the final exact-main Release candidate has not yet completed phase-end recertification;
- current CTAN `pkgcheck` has not yet passed on final package bytes;
- `v3.0.0` tag/GitHub Release and CTAN publication do not yet exist.

Every material repository advance updates affected documentation and machine state in the same work cycle. `README.md` changes only when user-facing facts change; it does not track transient CI/branch state.

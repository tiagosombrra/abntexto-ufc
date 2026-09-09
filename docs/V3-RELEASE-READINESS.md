# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — PUBLICATION HARDENING / FINAL RECERTIFICATION REQUIRED

## Phase readiness

| Phase | State | Evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | technical/runtime certification accepted |
| Release | **ACTIVE / REOPENED FOR PUBLICATION HARDENING** | prior candidate superseded for publication; new exact-main candidate required |

## Why Release was reopened

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` remains valid historical technical regression evidence, but its retained distribution bytes are **not publishable as v3.0.0 final**. The audit found two release-content defects:

1. `abntexto-ufc-3.0.0.zip` shipped a README that still instructed users to use v2.1.0 and described v3.0.0 as unpublished;
2. the CTAN README identified `3.0.0` as a `development candidate`.

Because publication bytes are immutable after acceptance, the retained artifact `10086299397` is **SUPERSEDED FOR PUBLICATION** and must never be attached to the final v3.0.0 Release or submitted to CTAN.

## Publication-hardening changes

| Surface | Current state |
|---|---|
| Active branch | `release/v3-publication-hardening` |
| Package id | `abntexto-ufc` — replaces historical/deprecated `ufctex` identity |
| Root user documentation | v3 publication-ready; stale v2 instructions removed |
| CTAN README | final 3.0.0 metadata; LPPL, maintainer, repo, dependency and no-logo statement explicit |
| CTAN package scope | reduced to one project runtime class + concise documentation + minimal example |
| CTAN archive count | **one upload archive**: `abntexto-ufc-3.0.0.zip` |
| CTAN project runtime | **one generated `abntexto-ufc.cls`** |
| CTAN project `.def` files | **0 — any `.def` in the ZIP is a hard failure** |
| Repository architecture | modular `.def` sources retained for development/testing only |
| CTAN equivalence | every tracked runtime module must be inlined exactly once into generated class |
| Isolated CTAN compile | example must compile without the modular runtime directory present |
| Redundant CTAN archive | removed; no `abntexto-ufc-ctan-3.0.0.zip` |
| Institutional marks | explicitly excluded from package and regression-tested |
| Proprietary Microsoft fonts | explicitly excluded from package and regression-tested |
| CTAN example | compiled without an institutional mark; source + PDF included |
| CHANGELOG | included in CTAN package |
| CTAN hygiene | ASCII/safe names, one root directory, LF-only text, no BOM, no empty files, 0644 files, no development infrastructure |
| pkgcheck | mandatory **before** immutable tag creation; use current CTAN version at final certification |

## Normative closure

The librarian review is now **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW**.

Former item 33 was closed against primary ABNT NBR 6023:2025 authority. The accepted behavior is now executable regression evidence:

- online references preserve `Disponível em:` and `Acesso em:` when applicable even when a DOI is present;
- consecutive repeated authorship is rendered explicitly rather than replaced by a dash/underline convention;
- legal-person authorship uses the form by which the entity is known/highlighted;
- governmental jurisdiction is retained when needed for identification, including `SÃO PAULO (Estado)` disambiguation.

The class explicitly passes `repeatfields=true` to `biblatex`, and the NBR 6023 regression exercises the closure cases under both pdfLaTeX and LuaLaTeX.

## New final-candidate contract

The next accepted Release candidate must satisfy:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

A PR head that is later squash-merged cannot be the final taggable candidate. The publication-hardening PR is therefore an integration step; after it is merged, final certification must run again on the resulting exact canonical `main` SHA.

## Remaining gates

| Order | Gate | State |
|---:|---|---|
| 1 | Publication-hardening PR: Static + complete Linux/release checks, including one-class/zero-`.def` CTAN gate | PENDING FINAL HEAD |
| 2 | Merge to protected `main`; resolve exact post-merge SHA | PENDING |
| 3 | Final phase-end regression on that exact `main` SHA | PENDING |
| 4 | Build deterministic three-ZIP distribution + `SHA256SUMS` from that exact SHA | PENDING |
| 5 | Confirm CTAN ZIP contains one generated `abntexto-ufc.cls`, zero `.def`, and passes isolated example compile | PENDING FINAL CANDIDATE |
| 6 | Run current CTAN `pkgcheck` against `abntexto-ufc-3.0.0.zip`; classify any warning | PENDING |
| 7 | Freeze hashes/evidence; no rebuild after acceptance | PENDING |
| 8 | Create immutable `v3.0.0` tag pointing to the certified SHA | BLOCKED BY 1–7 |
| 9 | Create GitHub Release; upload exact frozen bytes; re-download and hash-verify | BLOCKED BY 8 |
| 10 | Submit only `abntexto-ufc-3.0.0.zip` to CTAN and preserve receipt/acceptance evidence | BLOCKED BY 6–9 |
| 11 | Synchronize publication facts and perform final Release verification | BLOCKED BY 1–10 |

## Current blockers

- publication-hardening integration has not yet been merged and finally certified;
- no final post-merge exact-main Release candidate exists yet;
- current CTAN `pkgcheck` has not yet passed on the final archive;
- `v3.0.0` tag/GitHub Release and CTAN publication do not yet exist.

Every **material advance** must update the control plane in the same work cycle. Targeted checks do not replace the final **phase-end regression**.

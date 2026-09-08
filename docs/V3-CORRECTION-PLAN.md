# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-08  
Status: SHARED CORRECTIONS, SCIENTIFIC ARTICLE AND FINAL CERTIFICATION CLOSED — RELEASE ACTIVE

## Purpose

This document preserves the correction history produced by Regression Audit and the phase boundaries built on that corrected foundation. Active release execution is defined by `docs/V3-RELEASE-PHASE.md`, `docs/V3-RELEASE-READINESS.md`, `docs/CTAN-RELEASE.md`, the roadmap, handoff and machine state.

## Execution discipline

Every **material advance** updates the relevant implementation/review/certification/release state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace that gate.

## Accepted shared foundation

Core Corrections closed on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Reference PDF Validation closed on `b64074c64941895f97fbe0f795ce826c798d17ce` with 55/55 page-level visual PASS.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Items 1–32 and 34 are PASS. Item 33 remains a fail-closed current-authority gap.

## Scientific Article closeout

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481`, complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`, and canonical article PDF 5/5 visual PASS. PR #286 merged into main as `22e3c19235fa5245505b92d919a09d31eb2bfecb`.

## Final Certification closeout

| Surface | Accepted evidence |
|---|---|
| Immutable candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Static | `34239890649` SUCCESS |
| Complete Linux | `34239890614` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Linux release matrix | `34239890548` SUCCESS; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Literal fonts / Unicode / embedding / PDF/A | ACCEPTED |
| Scientific Article PDF/A-2b | PASS |
| Distribution bundles | integrity/checksums PASS; proprietary fonts not redistributed |
| Release reference reproducibility | PASS |
| Issue #18 | CLOSED |

## Release entry accepted

| Surface | Accepted evidence |
|---|---|
| Transition commit | `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` |
| Transition Static | `34249182526` SUCCESS |
| Transition complete Linux | `34249182417` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| PR #289 | merged |
| Release base on `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active Release branch | `release/v3.0.0` |

The transition changed control-plane phase state only and did not reopen accepted runtime, normative or librarian-review semantics.

## Current batch — Release execution

Synchronize the Release branch/control plane, revalidate the current release checklist and tooling, build/verify final public/distribution artifacts, validate the extracted CTAN candidate and shipped example, and then establish one immutable Release candidate.

No tag, GitHub Release or external publication action is allowed before that candidate passes the complete Release phase-end gate.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for disputed edge cases. It is not converted into release work merely to obtain 34 PASS results.

## Final phase gate

Release closes only after its checklist, publication verification and complete **phase-end regression** are recorded on one immutable Release candidate. No extra roadmap phase may be introduced.

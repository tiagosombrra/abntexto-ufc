# abntexto-ufc v3 — Engineering Roadmap for Release Recovery 3.0.1

Updated: 2026-09-10

## Current status

**Release is ACTIVE — 3.0.1 recovery / final exact-main recertification pending.** Publication hardening (PR #297), control synchronization (PR #298), final pkgcheck/human-gate controls (PR #301) and the scoped runtime correction (PR #302) are merged or incorporated into the recovery candidate. A public `v3.0.0` tag/Release was found to exist on an earlier SHA, so the final publication boundary is being recovered under `3.0.1` rather than silently retargeting the already-public tag.

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + article visual/PDF-A PASS |
| Final Certification | CLOSED | heavy technical matrix accepted |
| Release | **ACTIVE — RECOVERY / FINAL GATES** | merge 3.0.1 recovery, exact-main certification, current `pkgcheck`, seven-profile PDF/`.tex` approval, freeze, tag/release, verify and submit one CTAN archive |

## Current Release facts

| Predicate | Current result |
|---|---|
| Canonical branch | `main`; resolve HEAD dynamically from Git |
| Recovery target | `3.0.1` |
| Recovery work branch | `release/v3.0.1-recovery` |
| Publication-hardening PR | #297 — MERGED |
| Post-hardening control PR | #298 — MERGED, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Final release-gate PR | #301 — MERGED as `395899e1b2336ed268335d68e59e03452880c15e` |
| Post-v3.0.0 runtime correction | #302 — MERGED as `6d06d4ed42b2187b1483ea219ee055cfe975ece2`; populated unified illustration-list renderer fixed |
| Pre-recovery release evidence | run `34419086322`: `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck` PASS |
| Public `v3.0.0` | exists on `05399473827da7cf6b6c8bac36edc7115481773f`; premature/superseded for final publication |
| Librarian matrix | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN upload archive | `abntexto-ufc-3.0.1.zip` only |
| CTAN project runtime | `abntexto-ufc.cls` only |
| CTAN project `.def` files | 0 |
| Development source | modular `.def` architecture retained |
| Institutional marks/proprietary fonts | excluded from CTAN |
| Human visual acceptance | seven final PDF/`.tex` pairs, explicit maintainer approval required |
| Final `v3.0.1` tag/GitHub Release/CTAN publication | not created/not claimed |

`docs/V3-RELEASE-RECOVERY.md` records the recovery decision and the historical `v3.0.0` disposition.

## R0 — Publication documentation and package identity

**CLOSED.** Public distribution documentation is v3-oriented; `abntexto-ufc` is the canonical package identity; exactly one canonical CTAN archive is allowed; logo/font redistribution is prohibited.

## R1 — Normative item 33

**CLOSED / PASS.** Primary ABNT NBR 6023:2025 authority and executable tests cover DOI + applicable online availability/access elements, repeated authorship, legal-person authorship and jurisdiction disambiguation. The class requests `repeatfields=true` from `biblatex`.

## R2 — Monolithic CTAN runtime

**CLOSED AT INTEGRATION; 3.0.1 FINAL CANDIDATE REPROOF REQUIRED.** Repository sources remain modular; CTAN deterministically inlines all tracked project runtime modules into one generated `abntexto-ufc.cls`. Baseline evidence demonstrated 14/14 modules inlined, zero `.def`, isolated compilation, deterministic rebuild and no prohibited assets.

## R3 — Historical v3.0.0 publication mismatch

**CLASSIFIED / RECOVERY ACTIVE.** The public `v3.0.0` tag points to `05399473827da7cf6b6c8bac36edc7115481773f`, while the later final-gate exact-main state is `395899e1b2336ed268335d68e59e03452880c15e`. Because public assets existed under `v3.0.0`, the repository will not silently move that tag. Its assets are historical/superseded and ineligible for final CTAN submission. Recovery target is `3.0.1`.

## R4 — 3.0.1 recovery merge

**IN PROGRESS.** Combine the scoped PR #302 runtime correction with canonical 3.0.1 version metadata, CTAN/public documentation, machine state and final release orchestration while preserving accepted API, normative, profile and typography semantics outside that correction. Release-version capture must derive from the canonical `Makefile` version using recursion-safe output so GNU Make directory diagnostics cannot contaminate artifact names.

## R5 — Final exact-main 3.0.1 recertification

**BLOCKED BY R4.** Resolve the exact canonical `main` SHA after recovery merge and run Static, automatic `scope=complete` Linux integration and Linux release check on that same SHA. The earlier `395899e1...` PASS remains baseline evidence only because PR #302 changes runtime and 3.0.1 changes class identity metadata and publication bytes.

Required invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## R6 — CTAN `pkgcheck`

**BLOCKED BY R5.** `Linux release check` must obtain the current CTAN `pkgcheck` at execution time, run it against the exact `abntexto-ufc-3.0.1.zip` candidate and retain tool version, full output and checked ZIP SHA-256. Errors block Release; warnings require explicit disposition.

## R7 — Seven-profile maintainer visual acceptance

**BLOCKED BY R4–R6.** Generate PDF + `.tex` for undergraduate capstone, specialization capstone, master's thesis, doctoral thesis, research project, anonymized research project and scientific article. Every PDF must pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight. The maintainer must explicitly approve the seven final pairs before freeze/tag.

A preliminary 7/7 set from `25c6ab09...` passed automated preflight and page-by-page assistant inspection, but it is not final because the recovered candidate will be a later tracked state.

## R8 — Freeze, tag and GitHub Release

**BLOCKED BY R5–R7.** Freeze exact distribution hashes only after technical/pkgcheck/human acceptance; create immutable `v3.0.1` on that same SHA; attach exactly the frozen three ZIPs + `SHA256SUMS`; re-download and verify hashes.

## R9 — CTAN submission

**BLOCKED BY R6–R8.** Submit exactly `abntexto-ufc-3.0.1.zip`. Preserve receipt and later acceptance/install evidence. Do not submit the historical `abntexto-ufc-3.0.0.zip` GitHub asset as the recovered package.

## R10 — Release closeout

**BLOCKED BY R4–R9.** Synchronize final state and mark Release `CLOSED` only after publication verification.

## Operating discipline

Every **material advance** or repository modification updates affected documentation and machine state in the same work cycle. `README.md` tracks user-facing facts, not transient CI state. Deterministic release metadata and orchestration checks must be exhausted before expensive CI. Targeted checks never replace the final **phase-end regression**, automated green tests never replace explicit maintainer visual approval, and already-public tags are never silently retargeted to repair release history.

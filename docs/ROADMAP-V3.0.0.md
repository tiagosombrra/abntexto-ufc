# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-09

## Current status

**Release is ACTIVE — final exact-main recertification / human approval.** Publication hardening (PR #297) and post-hardening control synchronization (PR #298) are merged. The only taggable candidate is the exact canonical `main` SHA containing the executable current-CTAN `pkgcheck` and seven-profile human-acceptance controls and then passing the final gates.

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + article visual/PDF-A PASS |
| Final Certification | CLOSED | heavy technical matrix accepted |
| Release | **ACTIVE — FINAL GATES** | exact-main certification, current `pkgcheck`, seven-profile PDF/`.tex` approval, freeze, tag/release, verify and submit one CTAN archive |

## Current Release facts

| Predicate | Current result |
|---|---|
| Canonical branch | `main`; resolve HEAD dynamically from Git |
| Publication-hardening PR | #297 — **MERGED** |
| Post-hardening control PR | #298 — **MERGED**, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Final candidate policy | exact canonical `main` containing current `pkgcheck` + seven-profile human-acceptance gates |
| Post-hardening exact-main evidence | run `34355988612`: `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Librarian matrix | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN upload archive | `abntexto-ufc-3.0.0.zip` only |
| CTAN project runtime | **`abntexto-ufc.cls` only** |
| CTAN project `.def` files | **0** |
| Development source | modular `.def` architecture retained |
| Institutional marks/proprietary fonts | excluded from CTAN |
| Human visual acceptance | seven final PDF/`.tex` pairs, explicit maintainer approval required |
| Final tag/GitHub Release/CTAN publication | not created/not claimed |

## R0 — Publication documentation and package identity

**CLOSED.** Public distribution documentation is v3-oriented; `abntexto-ufc` replaces the historical identity; exactly one canonical CTAN archive is allowed; logo/font redistribution is prohibited.

## R1 — Normative item 33

**CLOSED / PASS.** Primary ABNT NBR 6023:2025 authority and executable tests cover DOI + applicable online availability/access elements, repeated authorship, legal-person authorship and jurisdiction disambiguation. The class requests `repeatfields=true` from `biblatex`.

## R2 — Monolithic CTAN runtime

**CLOSED AT INTEGRATION; FINAL CANDIDATE REPROOF REQUIRED.** Repository sources remain modular; CTAN deterministically inlines all tracked project runtime modules into one generated `abntexto-ufc.cls`. Baseline evidence demonstrated 14/14 modules inlined, zero `.def`, isolated compilation, deterministic rebuild and no prohibited assets.

## R3 — Final exact-main recertification

**PENDING exact candidate resolution.** Resolve the exact canonical `main` SHA containing the final release gates and run Static, automatic `scope=complete` Linux integration and Linux release check on that same SHA. No later pre-tag repository commit is allowed without reopening the cycle.

Required invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## R4 — CTAN `pkgcheck`

**PENDING exact final archive.** `Linux release check` must obtain the current CTAN `pkgcheck` at execution time, run it against the extracted canonical ZIP and retain tool version, full output and checked ZIP SHA-256. Errors block Release; warnings require explicit disposition.

## R5 — Seven-profile maintainer visual acceptance

**PENDING exact final candidate.** Generate PDF + `.tex` for undergraduate capstone, specialization capstone, master's thesis, doctoral thesis, research project, anonymized research project and scientific article. Every PDF must pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight. The maintainer must explicitly approve the seven final pairs before freeze/tag.

A preliminary 7/7 set from `25c6ab09...` passed automated preflight and page-by-page assistant inspection, but it is not final because later tracked control commits exist.

## R6 — Freeze, tag and GitHub Release

**BLOCKED by R3–R5.** Freeze exact distribution hashes only after technical/pkgcheck/human acceptance; create immutable `v3.0.0` on that same SHA; attach exactly the frozen three ZIPs + `SHA256SUMS`; re-download and verify hashes.

## R7 — CTAN submission

**BLOCKED by R4–R6.** Submit exactly `abntexto-ufc-3.0.0.zip`. Preserve receipt and later acceptance/install evidence.

## R8 — Release closeout

**BLOCKED by R3–R7.** Synchronize final state and mark Release `CLOSED` only after publication verification.

## Operating discipline

Every **material advance** or repository modification updates affected documentation and machine state in the same work cycle. `README.md` tracks user-facing facts, not transient CI state. Targeted checks never replace the final **phase-end regression**, and automated green tests never replace explicit maintainer visual approval.
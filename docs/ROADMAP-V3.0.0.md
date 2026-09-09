# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-09

## Current status

**Release is ACTIVE — final exact-main recertification.** Publication hardening was integrated by PR #297. The prior publication candidate remains superseded; the next and only taggable candidate is the exact canonical `main` commit that contains this post-merge control-plane synchronization and then passes the final release gates.

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | heavy technical matrix accepted |
| Release | **ACTIVE — FINAL RECERTIFICATION** | certify exact post-sync `main`, prove one-class/zero-`.def` CTAN runtime, pass current `pkgcheck`, freeze bytes, tag/release, verify and submit one CTAN archive |

## Current Release facts

| Predicate | Current result |
|---|---|
| Canonical branch | `main`; resolve current HEAD dynamically from Git |
| Publication-hardening PR | #297 — **MERGED** |
| Integration anchor | `25c6ab09dc38be9257d2912652074a48886d28f9` |
| Final candidate | exact `main` containing this synchronization after final recertification |
| Exact-main Linux trigger | push to `main` changing `release/v3-release-candidate.json` runs `Linux integration` with `scope=complete` |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Prior retained artifact | ID `10086299397` — historical evidence only; never publish |
| Librarian matrix | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN upload archive | `abntexto-ufc-3.0.0.zip` only |
| CTAN project runtime | **`abntexto-ufc.cls` only** |
| CTAN project `.def` files | **0** |
| Development source | modular `.def` architecture retained |
| Institutional marks | excluded from CTAN/archive contract |
| Microsoft proprietary fonts | excluded from CTAN/archive contract |
| Final tag | not created |
| GitHub Release | not created |
| CTAN publication | not claimed |

## R0 — Publication documentation and package identity

**CLOSED.** Root/CTAN documentation is v3-oriented; `abntexto-ufc` replaces the historical package identity; the canonical CTAN upload is one archive; logo/font redistribution is prohibited.

## R1 — Normative item 33

**CLOSED / PASS.** Primary ABNT NBR 6023:2025 authority and executable tests cover DOI + applicable online availability/access elements, repeated authorship, legal-person authorship, and `SÃO PAULO (Estado)` jurisdiction disambiguation. The class explicitly requests `repeatfields=true` from `biblatex`.

## R2 — Monolithic CTAN runtime

**CLOSED AT INTEGRATION; FINAL CANDIDATE REPROOF REQUIRED.** The repository stays modular. The CTAN builder recursively inlines all tracked project-owned `.def` modules into one generated `abntexto-ufc.cls`.

Canonical CTAN content:

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

Integration evidence already demonstrated: all 14 tracked runtime modules inlined exactly once, no residual project-owned `.def` input, zero `.def` files in the ZIP, isolated example compilation, deterministic rebuild and no prohibited assets.

## R3 — Final exact-main recertification

**PENDING after this synchronization is merged.** Resolve the exact resulting canonical `main` SHA and run the Release phase-end regression on that SHA. The release marker push must automatically produce `scope=complete` Linux integration on that same SHA. No subsequent pre-tag repository commit is allowed without starting a new candidate cycle.

Required invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## R4 — CTAN `pkgcheck`

**PENDING final archive.** Run the current CTAN `pkgcheck` version on the canonical ZIP before creating the immutable tag. Preserve version, full output, ZIP SHA-256 and disposition of every warning.

## R5 — Freeze, tag and GitHub Release

**BLOCKED by R3–R4.** After acceptance, freeze publication bytes/hashes, create immutable `v3.0.0` on the certified SHA, attach exactly the frozen three ZIPs + `SHA256SUMS`, then re-download and verify hashes.

## R6 — CTAN submission

**BLOCKED by R4–R5.** Submit exactly one file: `abntexto-ufc-3.0.0.zip`. Preserve receipt and later acceptance/install evidence.

## R7 — Release closeout

**BLOCKED by R3–R6.** After publication verification, synchronize roadmap/handoff/readiness/publication facts and mark Release `CLOSED`.

## Operating discipline

Every **material advance** or material repository modification must update affected documentation and machine state in the same work cycle. `README.md` is updated when user-facing facts change, not for transient branch/CI progress. Targeted checks never replace the final phase-end regression.

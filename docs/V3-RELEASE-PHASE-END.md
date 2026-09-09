# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: PASS — GITHUB PUBLICATION VERIFIED / CTAN EXTERNAL CLOSEOUT PENDING

## Purpose

This document records the completed technical Release phase-end regression for v3.0.0 and the remaining external CTAN closeout boundary. The released source is immutable at `05399473827da7cf6b6c8bac36edc7115481773f`; GitHub publication is complete and verified, while CTAN submission/acceptance is still pending explicit external evidence.

## Historical candidates

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` remains historical technical evidence but is **SUPERSEDED FOR PUBLICATION** because its retained distribution bytes contained stale release documentation.

PR #297 subsequently repaired the publication boundary. Its final head passed Static, complete Linux integration and Linux release check with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; the generated CTAN archive was manually audited as one project-owned class file and zero `.def` files. The protected squash merge produced integration anchor `25c6ab09dc38be9257d2912652074a48886d28f9`.

That integration anchor was not the final taggable candidate because the later control-plane synchronization produced the certified source SHA recorded below.

## Final candidate definition

The accepted Release candidate is `05399473827da7cf6b6c8bac36edc7115481773f`. It is the exact source commit certified by the final gates and resolved by immutable annotated tag `v3.0.0` through tag object `7354cf912ffa5abb171128554cabce61392ecd84`.

The GitHub Release uses only frozen assets produced from that source. Later post-tag documentation commits may move `main`; they do not alter the v3.0.0 source or publication bytes.

Required invariant is satisfied:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Minimum final evidence

All pre-publication technical gates are **PASS**:

1. Static contract on `05399473827da7cf6b6c8bac36edc7115481773f` — PASS;
2. automatic complete Linux integration on `05399473827da7cf6b6c8bac36edc7115481773f` — PASS;
3. Linux release check run `34383793519` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
4. applicable platform/font/PDF-A evidence — PASS;
5. deterministic three-ZIP distribution + `SHA256SUMS` — PASS;
6. canonical CTAN structural/semantic gate — PASS;
7. exactly one project-owned runtime implementation file (`abntexto-ufc.cls`) — PASS;
8. zero project-owned `.def` files and no nested runtime module directory — PASS;
9. all 14 project-owned runtime modules inlined exactly once — PASS;
10. isolated minimal CTAN example compilation — PASS;
11. CTAN `pkgcheck 4.1.0` on SHA-256 `d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71` — exit 0, 0 warnings, 0 errors/fatals;
12. frozen asset hashes and retained pre-tag evidence — PASS.

GitHub Release publication and post-publication re-download comparison are also PASS. The only remaining Release boundary is external CTAN submission/acceptance evidence.

## Canonical CTAN package

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

The CTAN package excludes project-owned `.def` files, nested modular runtime tree, institutional marks, proprietary Microsoft fonts, vendored `abntexto.cls`, CI/tests/tools/validators/evidence and repository control-plane files.

## Normative state

The librarian review is **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW**. Former item 33 has primary ABNT NBR 6023:2025 authority and executable regression evidence for DOI/online availability, repeated authorship, legal-person authorship and jurisdiction disambiguation.

## Required order

Completed:

1. protected-main control-plane synchronization;
2. exact source resolution at `05399473827da7cf6b6c8bac36edc7115481773f`;
3. Static, complete Linux integration and Linux release check;
4. final CTAN ZIP retention/manual audit;
5. current `pkgcheck` on the exact canonical bytes;
6. byte/hash freeze;
7. immutable `v3.0.0` tag;
8. GitHub Release publication and byte-identical re-download verification.

Pending:

9. submit the one canonical ZIP to CTAN and retain receipt evidence;
10. verify CTAN acceptance/catalog/install state, synchronize documentation/machine state and close Release.

Every material repository modification updates affected documentation and machine state in the same work cycle. The public README does not carry transient branch or CI state.

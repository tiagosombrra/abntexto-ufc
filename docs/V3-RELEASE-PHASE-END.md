# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: FINAL EXACT-MAIN RECERTIFICATION + HUMAN APPROVAL REQUIRED

## Purpose

This document records the final Release regression boundary after publication hardening and post-merge control synchronization, before the immutable v3.0.0 tag is created.

## Historical and integration anchors

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` remains historical technical evidence but is **SUPERSEDED FOR PUBLICATION** because its retained distribution bytes contained stale release documentation.

PR #297 repaired the publication boundary. Its protected squash merge produced `25c6ab09dc38be9257d2912652074a48886d28f9`; exact-main run `34355988612` later demonstrated `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, PDF/A and deterministic distribution gates, one generated CTAN class and zero `.def` files.

PR #298 then produced control-plane anchor `05399473827da7cf6b6c8bac36edc7115481773f`, aligning exact-main recertification triggers. The final candidate definition adds executable current-CTAN `pkgcheck` evidence and the maintainer-requested seven-profile visual gate.

## Final candidate definition

The only candidate eligible for final Release certification, human approval and immutable tag `v3.0.0` is the exact canonical `main` SHA containing the final release gates and passing all evidence below.

Required invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

No repository commit may be added between final acceptance and tag creation without reopening the candidate cycle.

## Minimum final evidence

1. Static contract on the exact candidate SHA;
2. automatic complete Linux integration on the exact candidate SHA;
3. `make release-check` on the exact candidate SHA, with `SCOPE=complete PASS=38 FAIL=0 SKIP=0` or an explicitly reviewed successor contract;
4. applicable heavy platform/font/PDF-A checks according to change-impact policy;
5. deterministic build of exactly three ZIPs plus `SHA256SUMS`;
6. canonical CTAN-grade `abntexto-ufc-3.0.0.zip` structural/semantic gate PASS;
7. exactly one project-owned runtime implementation file, generated `abntexto-ufc.cls`;
8. **zero project-owned `.def` files** and no nested runtime module directory;
9. every tracked project-owned runtime module inlined exactly once;
10. minimal CTAN example compiles using only generated class plus external `abntexto.cls`;
11. current CTAN `pkgcheck` executed by the release workflow against that exact ZIP, with version/full-output/archive-hash evidence and explicit warning disposition;
12. final PDF + corresponding `.tex` for all seven supported profiles generated from the same exact candidate;
13. A4, PDF/A-2b, font embedding and recognized-warning/overflow preflight PASS for those seven PDFs;
14. page-by-page review and **explicit maintainer visual approval** of all seven pairs;
15. frozen asset hashes and retained evidence before tag creation.

## Required seven-profile set

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- `scientific-article`.

A preliminary 7/7 set generated from `25c6ab09...` passed automated preflight and page-by-page assistant inspection. It is evidence of review readiness, not final approval, because the final exact candidate is a later tracked state.

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

The librarian review is **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW**. Former item 33 has primary ABNT NBR 6023:2025 authority and executable regression evidence.

## Required order

1. resolve the exact canonical `main` SHA containing the final release gates;
2. require Static, automatic `scope=complete` Linux integration and Linux release check, including current `pkgcheck`, on that SHA;
3. retain and physically audit the resulting final CTAN ZIP;
4. regenerate seven final PDF/`.tex` pairs and obtain explicit maintainer approval;
5. freeze hashes/evidence;
6. create immutable tag;
7. publish GitHub Release and verify re-downloaded hashes;
8. submit one canonical ZIP to CTAN and retain external evidence;
9. update post-publication state and close Release.

Every **material advance** updates affected documentation and machine state in the same work cycle. Targeted checks never replace the required **phase-end regression**. Automated success does not close the human visual gate.
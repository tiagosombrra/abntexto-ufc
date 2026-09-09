# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: FINAL EXACT-MAIN RECERTIFICATION REQUIRED

## Purpose

This document records the final Release regression boundary after publication hardening was integrated and before the immutable v3.0.0 tag is created.

## Historical candidates

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` remains historical technical evidence but is **SUPERSEDED FOR PUBLICATION** because its retained distribution bytes contained stale release documentation.

PR #297 subsequently repaired the publication boundary. Its final head passed Static, complete Linux integration and Linux release check with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; the generated CTAN archive was manually audited as one project-owned class file and zero `.def` files. The protected squash merge produced integration anchor `25c6ab09dc38be9257d2912652074a48886d28f9`.

That integration anchor is not the final taggable candidate because this control-plane synchronization intentionally follows it.

## Final candidate definition

After this synchronization is merged through protected `main`, resolve the exact resulting `main` SHA. That commit is the only candidate eligible for final Release certification and, if accepted, for immutable tag `v3.0.0`.

`Linux integration` is configured to run automatically with `scope=complete` on a `main` push that changes `release/v3-release-candidate.json`. This makes complete Linux evidence available on the exact post-squash candidate SHA rather than only on a PR head.

Required invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

No repository commit may be added between final candidate acceptance and tag creation without reopening the candidate cycle.

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
10. minimal CTAN example compiles using only the generated class plus external `abntexto.cls`;
11. current CTAN `pkgcheck` PASS or reviewed-warning result against that exact ZIP;
12. frozen asset hashes and retained evidence before tag creation.

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

1. merge this control-plane synchronization;
2. resolve exact canonical `main` SHA;
3. require Static, automatic `scope=complete` Linux integration and Linux release check on that SHA;
4. retain and manually audit the resulting final CTAN ZIP;
5. run current `pkgcheck` on the exact canonical bytes;
6. freeze hashes/evidence;
7. create immutable tag;
8. publish GitHub Release and verify re-downloaded hashes;
9. submit one canonical ZIP to CTAN and retain external evidence;
10. update post-publication state and close Release.

Every material repository modification updates affected documentation and machine state in the same work cycle. The public README does not carry transient branch or CI state.

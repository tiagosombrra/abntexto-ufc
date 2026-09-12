# V3 Release — Phase-end Regression for Recovery 3.0.1

> **Historical evidence — not current release authority.** This record may remain technically informative, but its phase/status statements are historical. Current release state is defined by the v3.0.1 continuation/finalization control plane. See `docs/V3.0.1-DOCUMENT-LIFECYCLE.md`.


Updated: 2026-09-10
Status: RECOVERY MERGE + FINAL EXACT-MAIN RECERTIFICATION + HUMAN APPROVAL REQUIRED

## Purpose

This document records the Release phase-end regression boundary after the `v3.0.0` publication mismatch was classified and the recovery target was moved to `3.0.1`.

The recovery includes the scoped PR #302 runtime correction for populated unified illustration-list rendering. Accepted API, normative, librarian-review, profile and typography semantics remain closed outside that correction. Fresh exact-SHA certification is required because both runtime and publication bytes changed.

## Historical and integration anchors

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` remains historical technical evidence but is superseded for publication because its retained distribution bytes contained stale release documentation.

PR #297 repaired the publication shape. Its protected merge produced `25c6ab09dc38be9257d2912652074a48886d28f9`; exact-main run `34355988612` demonstrated `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, deterministic distribution, one generated CTAN class and zero project-owned `.def` files.

PR #298 synchronized the control plane. PR #301 then integrated current CTAN `pkgcheck` and seven-profile human acceptance; exact-main run `34419086322` on `395899e1b2336ed268335d68e59e03452880c15e` passed `SCOPE=complete PASS=38 FAIL=0 SKIP=0` and current CTAN `pkgcheck`.

PR #302 subsequently corrected the populated unified illustration-list renderer and was squash-merged to `main` as `6d06d4ed42b2187b1483ea219ee055cfe975ece2`. Therefore all pre-#302 evidence is baseline evidence only for 3.0.1.

## Public v3.0.0 disposition

The public `v3.0.0` tag points to `05399473827da7cf6b6c8bac36edc7115481773f` and a GitHub Release exists for that tag. This predates the final exact-SHA release-gate state and violates the later invariant.

The recovery decision is fail-closed:

- do not silently retarget the public `v3.0.0` tag;
- classify its assets as historical/superseded for final publication;
- do not submit its CTAN ZIP as the recovered final package;
- recover under `v3.0.1`.

`docs/V3-RELEASE-RECOVERY.md` is the detailed recovery record.

## Final candidate definition

The only candidate eligible for final Release certification, human approval and immutable tag `v3.0.1` is the exact canonical `main` SHA produced after the combined PR #302 + recovery changes are merged and then passing all evidence below.

Required invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No repository commit may be added between final acceptance and tag creation without reopening the candidate cycle.

## Minimum final evidence

1. Static contract on the exact 3.0.1 candidate SHA;
2. automatic complete Linux integration on the exact candidate SHA;
3. `make release-check` on the exact candidate SHA, with `SCOPE=complete PASS=38 FAIL=0 SKIP=0` or an explicitly reviewed successor contract;
4. applicable heavy platform/font/PDF-A checks according to change-impact policy;
5. deterministic build of exactly three 3.0.1 ZIPs plus `SHA256SUMS`;
6. canonical CTAN-grade `abntexto-ufc-3.0.1.zip` structural/semantic gate PASS;
7. exactly one project-owned runtime implementation file, generated `abntexto-ufc.cls`;
8. zero project-owned `.def` files and no nested runtime module directory;
9. every tracked project-owned runtime module inlined exactly once;
10. minimal CTAN example compiles using only generated class plus external `abntexto.cls`;
11. current CTAN `pkgcheck` executed by the release workflow against that exact ZIP, with version/full-output/archive-hash evidence and explicit warning disposition;
12. final PDF + corresponding `.tex` for all seven supported profiles generated from the same exact candidate;
13. A4, PDF/A-2b, font embedding and recognized-warning/overflow preflight PASS for those seven PDFs;
14. page-by-page review and explicit maintainer visual approval of all seven pairs;
15. frozen asset hashes and retained evidence before tag creation.

## Required seven-profile set

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- `scientific-article`.

A preliminary 7/7 set generated from `25c6ab09...` passed automated preflight and page-by-page assistant inspection. It remains review-readiness evidence, not final approval, because the recovered final candidate is a later tracked state.

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

The librarian review remains **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW**. PR #302 does not alter accepted normative behavior.

## Required order

1. complete deterministic metadata/orchestration preflight before another expensive CI cycle;
2. merge the combined 3.0.1 recovery changes to canonical `main` only after PR gates pass;
3. resolve the resulting exact canonical `main` SHA;
4. require Static, automatic `scope=complete` Linux integration and Linux release check, including current `pkgcheck`, on that SHA;
5. retain and physically audit the resulting final 3.0.1 CTAN ZIP;
6. regenerate seven final PDF/`.tex` pairs and obtain explicit maintainer approval;
7. freeze hashes/evidence;
8. create immutable `v3.0.1`;
9. publish GitHub 3.0.1 Release and verify re-downloaded hashes;
10. submit one canonical 3.0.1 ZIP to CTAN and retain external evidence;
11. update post-publication state and close Release.

Every **material advance** updates affected documentation and machine state in the same work cycle. Deterministic errors must be caught before expensive CI where practical. Targeted checks never replace the required **phase-end regression**. Automated success does not close the human visual gate.

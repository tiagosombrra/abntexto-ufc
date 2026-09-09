# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve current SHA dynamically from Git |
| Active phase | **Release — final human/publication gates** |
| Active control branch | `release/v3-final-human-gate` until merged |
| Post-hardening baseline | `25c6ab09dc38be9257d2912652074a48886d28f9` |
| Baseline full release run | `34355988612` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Baseline distribution artifact | `10106606462`, digest `sha256:4eed74eaec5d076cea6fb140b533403ce065b8008a21dc80186763acad7b8340` |
| Prior superseded candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — historical only; never publish |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN archive | one canonical upload file: `abntexto-ufc-3.0.0.zip` |
| CTAN runtime | **one generated `abntexto-ufc.cls`; zero project-owned `.def` files** |
| Repository runtime | modular source tree retained for engineering/testing |
| Human acceptance | seven final PDF/`.tex` profile pairs require explicit maintainer approval |
| pkgcheck | current CTAN version is a pre-tag gate |
| Final tag rule | certified + visually approved source SHA must equal `v3.0.0` target SHA |

## Accepted post-hardening evidence

Exact-main baseline `25c6ab09...` has already demonstrated:

- Static contract success;
- complete release regression `38/38` with no skips/failures;
- NBR 6023:2025 item 33 PASS;
- scientific article PDF/A-2b PASS;
- deterministic three-ZIP distribution PASS;
- CTAN ZIP with one class, zero `.def`, 14 modules inline, checksum and archive-integrity PASS;
- no institutional marks or proprietary Microsoft fonts redistributed;
- reference-document reproducibility PASS.

The physical CTAN archive audit confirmed exactly eight files under `abntexto-ufc/`: README, CHANGELOG, LICENSE, class, manual `.tex`/PDF and minimal example `.tex`/PDF.

## Why the final SHA is not frozen yet

The hardening PR is already merged, but control documentation still described it as pending. This branch synchronizes those facts and adds the maintainer-requested seven-profile visual gate. Because these are tracked changes, their merge creates a new `main` SHA. Exact-SHA regression, package generation, `pkgcheck` and final visual review therefore run again on that resulting SHA before freeze/tag.

## Mandatory seven-profile review

Before `v3.0.0` is created, present the maintainer with both PDF and LaTeX source for:

1. undergraduate capstone;
2. specialization capstone;
3. master's thesis;
4. doctoral thesis;
5. research project;
6. anonymized research project;
7. scientific article.

The six non-article sources derive from the project's profile-matrix contract. The article uses the canonical scientific-article source. Every final PDF must be tied to the final candidate SHA and pass A4, PDF/A-2b, embedded-font and warning/overflow preflight.

A preliminary set generated against baseline `25c6ab09...` passed those checks and page-by-page visual inspection. It is useful for early review but does not close the final exact-candidate human gate.

## CTAN package contract

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

Hard invariants:

- exactly one project-owned runtime implementation: `abntexto-ufc.cls`;
- **zero `.def` files** in CTAN;
- no nested runtime directory;
- every tracked runtime module inlined exactly once;
- isolated example compile without modular runtime tree;
- no UFC marks, proprietary Microsoft fonts, vendored `abntexto.cls`, tests, workflows, validators or engineering state in the CTAN ZIP.

Only `abntexto-ufc-3.0.0.zip` is submitted to CTAN. Template and Overleaf ZIPs are GitHub Release conveniences.

## Remaining Release work

1. merge this final control synchronization to protected `main`;
2. resolve the exact resulting SHA;
3. rerun Static + complete Linux release contract on that SHA;
4. regenerate/audit deterministic distribution bytes;
5. run current CTAN `pkgcheck` on the exact canonical ZIP and retain version/full output/hash evidence;
6. regenerate all seven final review pairs and obtain explicit maintainer approval;
7. freeze hashes/evidence;
8. create immutable `v3.0.0` on the same SHA;
9. create GitHub Release with frozen assets and verify downloaded hashes;
10. submit only canonical ZIP to CTAN;
11. retain receipt and acceptance/install evidence;
12. synchronize final publication facts and close Release.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Windows/literal-font evidence

The retained Windows literal-font proof remains scoped valid because publication-hardening and this final documentation/control synchronization do not alter font runtime or engine selection. A fresh Windows run becomes mandatory if any font/engine/certification-relevant implementation changes before freeze.

Every material advance updates the relevant control documents in the same work cycle. No publication status is inferred from a build, tag or submission without the corresponding evidence.
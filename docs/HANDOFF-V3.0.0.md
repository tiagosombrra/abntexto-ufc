# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Active phase | **Release — maintainer all-profile visual validation pending; CTAN blocked** |
| Certified/tagged source | `05399473827da7cf6b6c8bac36edc7115481773f` |
| Immutable tag | `v3.0.0`; tag object `7354cf912ffa5abb171128554cabce61392ecd84` resolves to the certified source |
| GitHub Release | **PUBLISHED** — https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0 |
| GitHub publication evidence | run `34387825056`; artifact `10118391678` (`sha256:c8ac53d61e6fd1789748163cba6f22d334f4224c1966651baa7a11a334116abc`) |
| Final distribution artifact | `10117679639` (`sha256:7ee1b6bf4b1d54ac041db1e624d8bfcf52a1dc43897c1542b9fd969b971f40df`) |
| Canonical CTAN ZIP | `abntexto-ufc-3.0.0.zip` (`sha256:d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71`) |
| CTAN runtime | **one generated `abntexto-ufc.cls`; zero project-owned `.def` files** |
| `pkgcheck` | **PASS** — 4.1.0, exit 0, 0 warnings/errors; run `34386932488` |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| Seven-profile source/PDF generation | **ACTIVE** |
| Maintainer visual acceptance | **PENDING** |
| CTAN submission/acceptance | **BLOCKED until visual acceptance; no CTAN claim without external evidence** |

`main` may advance after the immutable tag for documentation/state/validation infrastructure. Git authority for the released implementation remains `v3.0.0` resolving to `05399473827da7cf6b6c8bac36edc7115481773f`.

## Completed publication-hardening evidence

PR #297 closed the publication defects and CTAN-shape issues. Its final head passed Static, Linux integration and Linux release check. The release check reported `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, closed former NBR 6023:2025 item 33, and produced a deterministic CTAN-grade archive with one generated class and zero project-owned `.def` files.

The retained PR artifact was manually audited before merge. The CTAN ZIP had exactly eight files below the package root, one `abntexto-ufc.cls`, zero `.def`, no vendored `abntexto.cls`, no institutional marks and no proprietary Microsoft fonts. The generated class contained all 14 tracked runtime modules exactly once and no residual project-owned `.def` input.

Final exact-main certification, `pkgcheck`, immutable tag creation and GitHub Release publication were subsequently completed on source `05399473827da7cf6b6c8bac36edc7115481773f`. Published Release assets were re-downloaded and proved byte-identical.

## CTAN package contract

The previous `ufctex` identity is replaced by `abntexto-ufc`. The CTAN-facing package is intentionally small and follows the single-class publication shape used by `abntexto-uece` where appropriate.

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

Hard invariants for the CTAN ZIP:

- exactly one project-owned runtime implementation file: `abntexto-ufc.cls`;
- **zero `.def` files**;
- no nested project runtime directory;
- every tracked runtime module is inlined exactly once;
- the minimal example compiles with only the generated class plus external `abntexto.cls` available;
- no UFC logos/marks, proprietary Microsoft fonts, vendored `abntexto.cls`, tests, workflows, validators, roadmaps or engineering evidence.

Only `abntexto-ufc-3.0.0.zip` is intended for CTAN. The editable-template and Overleaf ZIPs are GitHub Release conveniences and may preserve the modular source layout.

## Normative closure

Former librarian item 33 is **PASS** using primary ABNT NBR 6023:2025 authority and executable regression cases. The project verifies DOI plus applicable online availability/access elements, explicit repeated authorship, legal-person authorship, and jurisdiction disambiguation such as `SÃO PAULO (Estado)`.

## Mandatory maintainer visual gate

Before CTAN submission, produce and present source + rendered PDF from the frozen `v3.0.0` implementation for:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

Each pair must be traceable through a manifest containing source/PDF hashes and build metadata. Automated compile success does not close this gate; explicit maintainer acceptance is required. Detailed checklist and evidence state are in `docs/V3-VISUAL-VALIDATION.md`.

If a material runtime/presentation defect is found, `v3.0.0` must not be rebuilt, modified or retargeted. Open a correction/new-version cycle and repeat affected certification/visual gates before CTAN submission.

## Remaining Release work

1. generate the seven frozen-v3.0.0 source/PDF review pairs;
2. present them to the maintainer and record explicit visual acceptance for every profile;
3. only after acceptance, submit `abntexto-ufc-3.0.0.zip` to CTAN using the frozen GitHub Release asset;
4. preserve CTAN submission receipt and submitted-file identity/hash;
5. wait for explicit CTAN acceptance/catalog evidence; do not infer acceptance from submission;
6. verify accepted package identity/version and, when available, installation/catalog propagation;
7. synchronize post-CTAN documentation and machine state;
8. mark Release `CLOSED` only after external publication verification.

The GitHub tag and Release must not be rebuilt, replaced or retargeted.

## Mandatory operating discipline

Every **material advance** or material repository modification must update the affected documentation and machine state in the same work cycle. The public README is changed only when its user-facing facts change; it must not carry transient branch or CI state. Targeted checks never replace phase-end regression, and automated output never replaces the explicit maintainer visual gate.

# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve current SHA dynamically from Git |
| Active phase | **Release** |
| Active work branch | `release/v3-publication-hardening` |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — technical evidence retained, **SUPERSEDED FOR PUBLICATION** |
| Prior artifact | `10086299397` — reproducible historical evidence; do not publish |
| Current batch | **CTAN/publication hardening + final recertification preparation** |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN archive | one canonical upload file: `abntexto-ufc-3.0.0.zip` |
| Final tag rule | certified source SHA must equal `v3.0.0` target SHA |
| pkgcheck rule | current CTAN `pkgcheck` is a pre-tag gate |

`docs/V3-CONTINUATION.md` is the shortest continuation entry point. Never use memory or a hardcoded “current main” SHA as Git authority.

## Historical accepted technical evidence

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` previously passed:

| Gate | Historical result |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Complete Linux integration | `34303586778` — SUCCESS |
| Linux release check | `34303586773` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Reference PDF reproducibility | PASS; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65` |
| Retained artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |

Those results prove the prior technical candidate; they **do not certify the final publication bytes** because the package documentation was stale.

## Publication defect and response

The release audit found that the old canonical ZIP still told users to use v2.1.0 and that the CTAN README labeled 3.0.0 a development candidate. The response is intentionally fail-closed:

- no old artifact may be relabeled or silently rebuilt;
- `release/v3-release-candidate.json` records the old candidate as superseded for publication;
- a new candidate must be produced only after this hardening work is merged;
- the final candidate is the exact post-merge canonical `main` SHA;
- final package hashes are frozen only after full regression and current `pkgcheck`.

## CTAN package contract

The previous `ufctex` identity is replaced by `abntexto-ufc`. The canonical archive is intentionally small and modeled after the accepted `abntexto-uece` publication shape where appropriate:

```text
abntexto-ufc/
├── README.md
├── CHANGELOG
├── LICENSE
├── abntexto-ufc.cls
├── abntexto-ufc/...
├── abntexto-ufc.tex
├── abntexto-ufc.pdf
├── abntexto-ufc-example.tex
└── abntexto-ufc-example.pdf
```

Only `abntexto-ufc-3.0.0.zip` is intended for CTAN. The editable-template and Overleaf ZIPs are GitHub Release conveniences.

The CTAN package excludes UFC logos/marks, proprietary Microsoft fonts, vendored `abntexto.cls`, tests, workflows, validators, release state, roadmaps and engineering evidence.

## Normative closure

Former librarian item 33 is now PASS using primary ABNT NBR 6023:2025 authority and executable regression cases. The project now explicitly verifies:

- DOI alongside required online availability/access elements;
- explicit repetition of consecutive authorship;
- legal-person authorship by known/highlighted entity form;
- governmental jurisdiction disambiguation such as `SÃO PAULO (Estado)`.

## Remaining Release work

1. pass CI for `release/v3-publication-hardening`;
2. merge through protected `main`;
3. resolve the exact post-merge SHA;
4. execute the final **phase-end regression** on that SHA;
5. build and validate the deterministic final archive set;
6. execute current CTAN `pkgcheck` before tag creation;
7. freeze hashes and evidence;
8. create immutable `v3.0.0` on the certified SHA;
9. publish GitHub Release with exact frozen bytes and verify downloaded hashes;
10. submit only the canonical package ZIP to CTAN and retain receipt/acceptance evidence;
11. synchronize final state and close Release.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Mandatory operating discipline

Every **material advance** updates the relevant documentation and machine state in the same work cycle. Targeted checks never replace the required **phase-end regression**. No publication state is inferred from a build, tag or submission without the corresponding external evidence.

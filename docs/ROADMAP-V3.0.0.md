# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-09

## Current status

**Release is ACTIVE and has been reopened for publication hardening.** The implementation foundation remains mature, but the prior publication candidate was superseded because its packaged documentation was not final-publication quality. The CTAN-facing runtime has additionally been simplified to a single generated class file.

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | heavy technical matrix accepted |
| Release | **ACTIVE — PUBLICATION HARDENING** | integrate hardening, certify exact post-merge `main`, prove one-class/zero-`.def` CTAN runtime, pass current `pkgcheck`, freeze bytes, tag/release, verify and submit one CTAN archive |

## Current Release facts

| Predicate | Current result |
|---|---|
| Canonical branch | `main`; resolve current HEAD dynamically from Git |
| Active work branch | `release/v3-publication-hardening` |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — technically accepted, **SUPERSEDED FOR PUBLICATION** |
| Prior retained artifact | ID `10086299397` — historical evidence only; never publish as v3.0.0 final |
| Librarian matrix | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| Package id | `abntexto-ufc` |
| CTAN upload archive | `abntexto-ufc-3.0.0.zip` only |
| CTAN project runtime files | **`abntexto-ufc.cls` only** |
| CTAN project `.def` files | **0** |
| Development source | modular `.def` architecture retained |
| Redundant `-ctan-` ZIP | removed from final contract |
| Institutional marks | excluded from CTAN/archive contract |
| Microsoft proprietary fonts | excluded from CTAN/archive contract |
| Final tag | not created |
| GitHub Release | not created |
| CTAN publication | not claimed |

## Why the prior candidate is not publishable

The audit of the actual retained GitHub Actions artifact found that:

1. the canonical `abntexto-ufc-3.0.0.zip` still shipped a README centered on v2.1.0 and stated that v3.0.0 was not published;
2. the CTAN README identified version 3.0.0 as a `development candidate`.

The files were reproducible and hash-correct, but reproducibly wrong as final publication artifacts. The fail-closed response is to preserve that candidate as historical technical evidence and require a new Release phase-end candidate after publication hardening is merged.

## Publication-hardening scope

### R0 — User and CTAN documentation

**Implemented on active branch.**

- root README rewritten for v3.0.0;
- CTAN README finalized with version, maintainer, LPPL, repository, issue tracker and external dependency;
- explicit no-UFC-logo/no-institutional-mark statement;
- explicit no-proprietary-Microsoft-font statement;
- concise CTAN CHANGELOG added;
- CTAN manual finalized and old transition language removed.

### R1 — Normative item 33

**Implemented; final Release evidence pending.**

Primary ABNT NBR 6023:2025 authority closes the former deliberate gap. The executable regression covers:

- DOI together with applicable `Disponível em:` and `Acesso em:` elements;
- explicit repeated authorship;
- legal-person authorship;
- jurisdiction disambiguation such as `SÃO PAULO (Estado)`.

The class explicitly requests `repeatfields=true` from `biblatex`.

### R2 — Canonical CTAN-grade archive and monolithic runtime

**Implemented; final release-check evidence pending.**

Final public archive set:

```text
abntexto-ufc-3.0.0.zip
abntexto-ufc-template-3.0.0.zip
abntexto-ufc-overleaf-3.0.0.zip
SHA256SUMS
```

Only `abntexto-ufc-3.0.0.zip` is submitted to CTAN. Its expected content is flat below the package root:

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

The repository remains modular. For CTAN only, the builder recursively expands the canonical project-owned module inputs into one generated `abntexto-ufc.cls`, strips module wrappers and preserves canonical load order.

Acceptance requires:

- every tracked project-owned runtime `.def` module inlined exactly once;
- no project-owned `.def` file in the CTAN ZIP;
- no nested runtime module directory;
- no residual `\input{abntexto-ufc/...def}` in the generated class;
- isolated example compilation using the generated class plus external `abntexto.cls`, without the modular runtime tree;
- deterministic byte-identical distribution rebuilds.

The package gate also rejects stale publication text, deprecated `ufctex` identity, unsafe/non-ASCII filenames, hidden paths, CRLF/BOM, empty files, inappropriate modes, development infrastructure, vendored upstream class, institutional mark assets and proprietary Microsoft fonts.

### R3 — Final exact-main recertification

**PENDING after merge.**

The publication-hardening PR head is not the final candidate because `main` is squash-merge protected. After merge, resolve the exact resulting canonical SHA and run the Release phase-end regression again on that SHA.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

### R4 — CTAN `pkgcheck`

**PENDING final archive.**

Run the current CTAN `pkgcheck` version on `abntexto-ufc-3.0.0.zip` **before** creating the immutable tag. Preserve tool version, full output, checked ZIP hash and disposition of every warning.

### R5 — Freeze, tag and GitHub Release

**BLOCKED by R3–R4.**

After final acceptance:

1. freeze SHA-256 values and evidence;
2. forbid publication-byte rebuild;
3. create immutable `v3.0.0` pointing to the certified SHA;
4. attach exactly the three frozen ZIPs + `SHA256SUMS` to GitHub Release;
5. re-download and verify hashes.

### R6 — CTAN submission

**BLOCKED by R4–R5.**

Submit exactly one file: `abntexto-ufc-3.0.0.zip`. Preserve CTAN receipt and later acceptance/install evidence. Do not infer CTAN publication from successful form submission.

### R7 — Release closeout

**BLOCKED by R0–R6.**

Synchronize roadmap, handoff, readiness and publication facts, then perform final Release verification and only then mark Release `CLOSED`.

## Operating discipline

Every **material advance** must update roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks never replace the required final **phase-end regression**.

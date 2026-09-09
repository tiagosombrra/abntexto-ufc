# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — FINAL HUMAN/PUBLICATION GATES

## Phase readiness

| Phase | State | Evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | article PDF/PDF-A validation accepted |
| Final Certification | CLOSED | technical/runtime certification accepted |
| Release | **ACTIVE** | post-merge regression passed; pkgcheck + explicit maintainer visual approval + publication remain |

## Canonical publication-hardening result

The publication-hardening PR was squash-merged into `main`. Its post-merge baseline SHA is `25c6ab09dc38be9257d2912652074a48886d28f9`.

The exact post-merge Linux release run `34355988612` checked out that SHA and completed the full release contract:

- `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- scientific article PDF/A-2b gate: PASS;
- deterministic distribution gate: PASS;
- CTAN runtime: one generated `abntexto-ufc.cls`, zero project-owned `.def` files;
- 14 tracked runtime modules incorporated into the generated class;
- checksums and ZIP integrity: PASS;
- no UFC institutional marks or proprietary Microsoft fonts redistributed.

Distribution artifact `10106606462` has GitHub artifact digest `sha256:4eed74eaec5d076cea6fb140b533403ce065b8008a21dc80186763acad7b8340`.

Its canonical CTAN ZIP is `abntexto-ufc-3.0.0.zip`, with SHA-256 `2ff84bcb2c788ea2fbbea882b0bb8861b1ebb3cb3c2b121fe16fc27679851159`, and contains exactly eight files under one `abntexto-ufc/` directory: README, CHANGELOG, LICENSE, one class, manual source/PDF and example source/PDF.

## Human visual acceptance gate

Before any immutable tag or publication action, the maintainer requires an explicit visual review of all supported document profiles and their corresponding LaTeX sources.

Required review set:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

The six non-article examples must be generated from the same profile contracts exercised by the complete profile matrix. The article must use the canonical `template/scientific-article.tex` source. Every pair must be tied to the final candidate source, compiled against the pinned release dependency set, and pass A4/PDF-A/font/warning preflight before being shown for approval.

**State: PENDING EXPLICIT MAINTAINER APPROVAL.** Automated success does not satisfy this gate.

A preliminary review set was generated from post-hardening baseline `25c6ab09...` and passed local preflight for all seven profiles (A4, PDF/A-2b, fonts embedded, zero recognized warnings). Because this documentation synchronization changes repository history, the final review set must be regenerated from the eventual post-merge final candidate before tagging.

## Normative closure

The librarian review remains **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW**. Former item 33 is closed against primary ABNT NBR 6023:2025 authority and executable regression evidence, including DOI plus availability/access data, repeated authorship, legal-person authorship and jurisdiction disambiguation.

## Final candidate invariant

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

Any tracked change before tagging creates a new candidate SHA and requires the final gates that depend on exact source identity to be rerun.

## Remaining gates

| Order | Gate | State |
|---:|---|---|
| 1 | Merge this final control/documentation synchronization to protected `main` | PENDING |
| 2 | Resolve resulting exact `main` SHA | BLOCKED BY 1 |
| 3 | Static + complete Linux release regression on that exact SHA | BLOCKED BY 1–2 |
| 4 | Regenerate and audit deterministic distribution bytes from that exact SHA | BLOCKED BY 1–3 |
| 5 | Run current CTAN `pkgcheck` (announced 4.1.0 on 2026-08-05) against the exact canonical CTAN package; preserve complete output and classify warnings | BLOCKED BY 4 |
| 6 | Generate all seven final source/PDF review pairs from the exact candidate and obtain explicit maintainer visual approval | BLOCKED BY 2–4 |
| 7 | Freeze final hashes/evidence; no publication-byte rebuild after freeze | BLOCKED BY 5–6 |
| 8 | Create immutable `v3.0.0` tag on the same certified/approved SHA | BLOCKED BY 7 |
| 9 | Create GitHub Release with exact frozen assets; re-download and hash-verify | BLOCKED BY 8 |
| 10 | Submit only `abntexto-ufc-3.0.0.zip` to CTAN; retain receipt and acceptance evidence | BLOCKED BY 5–9 |
| 11 | Synchronize final publication facts and close Release only after CTAN acceptance/install evidence | BLOCKED BY 10 |

## Windows literal-font evidence scope

The retained Windows literal-font certification remains scoped evidence because publication hardening changed bibliography/package-distribution behavior, not the Windows font runtime or literal font-selection implementation. If the final candidate changes `abntexto-ufc/fonts.def`, font setup, engine behavior or the Windows certification contract, a fresh Windows/literal-font run becomes mandatory before freeze.

Every material advance updates the relevant control plane in the same work cycle. Targeted checks never replace exact-candidate release regression.
# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — FINAL EXACT-MAIN RECERTIFICATION / HUMAN APPROVAL

## Phase readiness

| Phase | State | Evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF visual/PDF-A PASS |
| Final Certification | CLOSED | technical/runtime certification accepted |
| Release | **ACTIVE** | final exact-main pkgcheck + seven-profile approval + publication pending |

## Completed Release hardening

PR #297 was squash-merged and its post-merge baseline `25c6ab09dc38be9257d2912652074a48886d28f9` passed the complete release contract. Exact-main run `34355988612` reported `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, scientific-article PDF/A-2b PASS, deterministic distribution PASS, one generated CTAN class, zero project-owned `.def` files and 14 tracked runtime modules inlined.

PR #298 was then squash-merged as `05399473827da7cf6b6c8bac36edc7115481773f`, synchronizing the final-candidate control plane and ensuring exact-main release-marker pushes force complete Linux integration.

The retained baseline CTAN artifact was physically audited as exactly eight files, `1 cls / 0 def`, no nested runtime tree, no vendored `abntexto.cls`, no institutional marks and no proprietary Microsoft fonts.

## Final controls encoded in the candidate definition

Before the immutable tag, two requirements are explicit and executable:

1. **CTAN pkgcheck:** `Linux release check` downloads the current CTAN `pkgcheck` at execution time, records `--version`, complete output and the SHA-256 of the checked canonical ZIP, and fails on tool errors. Any warnings still require explicit classification before freeze.
2. **Maintainer visual acceptance:** the final candidate must provide PDF + corresponding `.tex` for all seven supported profiles and obtain explicit maintainer approval.

Required profile set:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

A preliminary set generated from baseline `25c6ab09...` already passed A4, PDF/A-2b, embedded-font, recognized-warning/overflow and page-by-page visual checks for all seven profiles. It does **not** close the final human gate because later tracked Release-control commits require regeneration from the exact tag candidate.

## Final-candidate contract

The only eligible candidate is the exact canonical `main` SHA containing the final release gates and subsequently passing certification, current CTAN `pkgcheck` and explicit maintainer visual approval.

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

No tracked commit is allowed between final acceptance and tag creation without reopening the candidate cycle.

## Remaining gates

| Order | Gate | State |
|---:|---|---|
| 1 | Publication hardening PR #297 | **PASS / MERGED** |
| 2 | Post-hardening control-plane PR #298 | **PASS / MERGED** |
| 3 | Executable current-CTAN `pkgcheck` + seven-profile human-acceptance policy | **ENCODED IN FINAL CANDIDATE CONTRACT** |
| 4 | Resolve exact canonical `main` SHA containing final gates | PENDING |
| 5 | Static + automatic `scope=complete` Linux integration + Linux release check (including current `pkgcheck`) on exact SHA | BLOCKED BY 4 |
| 6 | Retain and physically re-audit deterministic three-ZIP distribution + `SHA256SUMS` | BLOCKED BY 5 |
| 7 | Regenerate seven final PDF/`.tex` pairs from exact candidate and obtain explicit maintainer approval | BLOCKED BY 4–6 |
| 8 | Freeze hashes/evidence; prohibit rebuild | BLOCKED BY 5–7 |
| 9 | Create immutable `v3.0.0` on certified + visually approved SHA | BLOCKED BY 8 |
| 10 | Create GitHub Release and re-download/hash-verify assets | BLOCKED BY 9 |
| 11 | Submit only canonical ZIP to CTAN; preserve receipt/acceptance evidence | BLOCKED BY 5–10 |
| 12 | Synchronize post-publication facts and close Release | BLOCKED BY 1–11 |

## Windows literal-font scope

The retained Windows literal-font certification remains scope-valid because these final changes affect Release control/workflows/documentation, not font runtime or engine selection. A fresh Windows run becomes mandatory if font setup, engine behavior or the Windows certification contract changes before freeze.

Every **material advance** updates affected documentation and machine state in the same work cycle. Targeted checks never replace the required **phase-end regression**. Automated green tests never substitute for the explicit seven-profile maintainer approval.
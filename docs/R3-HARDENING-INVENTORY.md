# V3-R3 Hardening Inventory

Updated: 2026-09-03

## Purpose

This document closes R3-A by recording the current standards, evidence, test-integrity, engineering-language, and migration-contract state before bounded R3 implementation begins. It is an engineering inventory. It does not change normative rule IDs, expected values, locators, tolerances, applicability, source authority, or proof state.

## Baseline

- R3-A source `main`: `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`.
- R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`.
- R2 post-merge release validation: run `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout/control-plane validation: Static `33747658673` PASS; Linux integration `33747658602` = `PASS=30 FAIL=0 SKIP=0`.
- R3-A planning issue: #250.

## Standards and proof baseline

The current source/contract checks are green. The baseline reports:

| Metric | Current value |
|---|---:|
| Normative/institutional sources | 19 |
| Active rules | 181 |
| Rules classified automatic | 164 |
| Manual or conditional rules | 17 |
| Project-policy / technical-profile rules | 11 |
| Runner gates | 32 |
| Registered evidence checks | 10 |
| Validator checks | 9 |
| Full-contract review date | 2026-08-28 |
| Reference-guide topics | 20 PASS / 0 FAIL |
| Object-scope uncovered rules | 0 |

No newer normative source or currency evidence was introduced by R3-A. Therefore `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain unchanged. R3 must not mutate source authority or normative values merely to make a checker green.

A coverage caveat was identified: `tests/checks/normative_coverage.py` currently proves that an executable rule names at least one known runner/validator/registered-evidence check. It does not itself prove that the named check enforces the predicate. This matters because some front-matter evidence producers are currently audit-only.

## Front-matter evidence truthfulness

The umbrella `Front matter` integration check passed, while its structured evidence included unresolved FAIL records. This is possible by design today: the front-matter evidence checkers expose `--enforce`, but the corresponding integration scripts invoke them in audit mode. An audit finding therefore does not affect the shell exit code unless another check fails.

Current unresolved records include:

| Rule / surface | Observation | R3-A classification | Owner |
|---|---|---|---|
| `dedication.line-spacing` | measured marker gap 41.4 pt vs same-document calibrated 20.7 pt | unresolved fixture/observer/runtime discrepancy; do not change runtime before discrimination | R3-B1 / #252 |
| `epigraph.short.alignment` | alignment observer FAIL | unresolved; short route lacks the explicit `\\justifying` used by dedication/long routes, but current evidence is not yet sufficient to call this a runtime defect | R3-B1 / #252 |
| `summary.paragraph.single` | vernacular source counted as 2 paragraphs, foreign as 1 | observer defect: `source_body_paragraphs()` strips legacy/upstream keyword macros but not canonical `\\ufcSummaryKeywords`, so the keyword block is counted as a second paragraph | R3-B1 / #252 |
| title-page required/order | nature/advisor/coadvisor markers not observed | fixture/extraction discrepancy requiring robust marker review before runtime changes | R3-B1 / #252 |
| approval required/order | FAIL for all academic labels | test-generator integrity failure plus possible marker issue; current matrix cannot be trusted until generation is repaired | R3-B1 / #252 |

### Approval profile generator defect

`tests/integration/frontmatter-approval-evidence.sh` still runs:

```text
sed "s/tipo = tese,/tipo = $profile,/" ...
```

The current fixture uses canonical v3 `type = doctoral-thesis`. The substitution is therefore a no-op. Files labelled as undergraduate capstone, specialization capstone, master's thesis, doctoral thesis, research project, and anonymized research project are not proven to contain the intended type variation. This also explains why project-suppression observations must not be interpreted as runtime defects until the generator is fixed.

This is a semantic test defect, not a normative finding.

## Residual API enforcement gap

`tests/checks/v3_api_residual.py` is a live permanent gate and correctly consumes `release/v3-api-migration.json`. It currently scans selected active LaTeX/runtime/template sources with suffixes `.tex`, `.def`, `.cls`, and `.sty`.

That scope does not cover project-owned integration generators such as `.sh` or other engineering sources. The stale approval `sed` expression therefore survived R2 even though it contains removed v2 project vocabulary. R3-B3 must broaden the permanent residual contract with narrow, explicit exemptions for migration documentation, machine migration mappings, negative tests, and genuine upstream boundaries.

## Engineering-language enforcement gap

`docs/ENGINEERING-LANGUAGE.md` requires English on project-owned engineering surfaces. The current repository contract enforces English-oriented paths and rejects selected Portuguese path tokens, but it does not enforce project-owned technical comments, diagnostics, UI strings, or machine identifiers.

Confirmed active examples include Portuguese technical diagnostics in front-matter integration scripts (`Auditoria ... falhou`, `Validando ...`, `Gate ... concluído`). In addition, front-matter standards/scenario applicability still uses project-owned technical profile identifiers such as `tccgraduacao`, `tccespecializacao`, `dissertacao`, `tese`, `projeto`, and `projetoanonimizado`, while the canonical v3 runtime type values are English.

These are engineering-policy findings. Rendered Portuguese academic content, official UFC/ABNT wording, bibliography data, literal Portuguese output under test, and genuine dependency-owned identifiers remain valid and must be protected from false positives.

## Migration-contract retention

| Contract | R3-A status | Reason |
|---|---|---|
| `release/v3-api-migration.json` | RETAIN | live input of the permanent v3 residual gate |
| `release/v3-test-migration.json` | REVIEW FOR CONSOLIDATION | R2 closed; no current runtime consumer demonstrated by the R3-A source audit |
| `release/v3-path-migration.json` | REVIEW FOR CONSOLIDATION | R2 closed; no current runtime consumer demonstrated by the R3-A source audit |
| `release/v3-roadmap.json` | RETAIN | canonical machine state |

R3-B4 must confirm consumers fail-closed before deleting or consolidating a closed migration contract.

## Bounded implementation lots

| Lot | Issue | Status after R3-A | Primary objective |
|---|---:|---|---|
| R3-B1 | #252 | ACTIVE | make front-matter evidence truthful and fail-closed |
| R3-B2 | #253 | PENDING | harden normative proof-state and coverage semantics |
| R3-B3 | #254 | PENDING | audit semantic test integrity and expand residual enforcement |
| R3-B4 | #255 | PENDING | enforce engineering-language policy and consolidate closed contracts |
| R3-B5 | #256 | PENDING | close R3 and establish the exact R4 certification entry |

## Boundaries

- Preserve the closed v3 API; do not add runtime compatibility aliases.
- Repair fixtures and observers before changing runtime behavior in response to an audit discrepancy.
- Do not strengthen a normative predicate from an observational artifact without source evidence.
- Do not change rule IDs, expected values, locators, tolerances, applicability, authority, or proof state without current evidence.
- Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-B1 through R3-B4.
- Heavy Windows/literal-font certification remains R4-owned.

## R3-A exit

R3-A is complete when this inventory and the five bounded issues are merged into the canonical control plane. The next implementation action is R3-B1 / issue #252.
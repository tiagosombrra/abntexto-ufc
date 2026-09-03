# R3-B2 Evidence Contribution Model

Updated: 2026-09-03

## Purpose

R3-B2 separates three concepts that were previously easy to conflate: a validation mechanism being traceable, that mechanism contributing evidence for a specific rule, and the conservative proof state assigned to the rule.

A runner gate, validator check or registered evidence identifier being known and green does not by itself establish enforcement for every rule that names it. Runtime contribution is recognized only when the coordinated validation run emits rule-specific `PASS` evidence from an evidence owner declared by that rule.

## Evidence classes

- `enforced-automatic`: a non-partial automatic rule received rule-specific `PASS` evidence from a declared owner in the current coordinated run.
- `bounded-positive`: an `automatic-partial` rule received rule-specific positive evidence from a declared owner. This does not promote the rule to `PROVEN`.
- `manual-review`: the rule legitimately retains a manual review boundary.
- `conditional-review`: the rule is meaningful only under its declared applicability or present/absent route.
- `support-only`: current observations or declared mechanisms exist, but the run does not claim rule-specific enforcement from them.
- `not-applicable`: the rule is outside the standard electronic-package applicability boundary.
- `automation-gap`: an `automatic-partial` rule lacks current rule-specific evidence from a declared owner; complete coordinated validation fails closed in this state.

## B2 policy

The 17 non-automatic rules are individually classified in `standards/evidence-contribution-policy.json`. The permanent contribution checker is `tests/checks/normative_evidence_contribution.py`.

For complete `tests/run.py` executions, the contribution checker runs after the repository checks and consumes only the current run's `artifacts/validation/checks/*.log` files. It intersects observed rule-specific evidence with each rule's declared evidence ownership and writes JSON/Markdown contribution reports.

Targeted `--only` executions intentionally do not run the global contribution closure because they exercise only a subset of evidence owners.

## Safety invariants

- Normative source authority, precedence, rule IDs, expected values, tolerances, locators and applicability remain unchanged.
- Evidence contribution does not change the proof-state defaults in `standards/proof-policy.json`.
- `automatic-partial` remains `PARTIAL`; bounded positive evidence is not equivalent to complete proof.
- Parent-inherited atomic validation is rebound only where a rule-specific gate already measures or enforces that exact dimension.
- Rule-local N4 promotions retain ownership in their canonical coverage-rule source files.
- Manual, conditional and not-applicable rules are never auto-promoted from a green gate.

## Runtime closeout criterion

A complete PR-mode run must finish with all 113 `automatic-partial` rules classified as `bounded-positive` and zero `automation-gap` entries. Non-partial automatic rules without rule-specific current-run evidence remain visible as `support-only` rather than being counted as enforced.

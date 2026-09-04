# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **TECHNICALLY CERTIFIED; exact R5 entry activation pending**.
- R4 entry predecessor: `d90a675a844724c33a5727d8d980027c46291eb0`.
- Certified product candidate: `c79f3c73f1d51a30175e8259269504d029442a1c`.
- R4 certification workflow: `33855800767` — SUCCESS.
- Preflight job: `100968686875` — PASS.
- Windows strict matrix job: `100968747942` — PASS.
- Linux final font/PDF-A job: `100970109387` — PASS.
- Cleanup job: `100970307670` — PASS; temporary workflow absent from final certification branch.
- Evidence artifact: `9930304564` / `sha256:ca21bf1771c45e2003b2448ea019b6eb7b93c8468eff1330df76340a943eeca2`.
- Windows PDF artifact: `9930280624` / `sha256:934044738f21261137014984114d33516b8601c0710107687903ad2f59a6b565`.
- Four matrix cells: literal text family PASS; Unicode extraction PASS; font embedding PASS; PDF/A-2b PASS; unexpected text substitution ABSENT.
- pdfLaTeX math policy: `NEW-TX-MATH`; LuaLaTeX math policy: independent OpenType math.
- V3-R5/#272: **PREPARED / BLOCKED** until the immutable R4 closeout merge SHA exists.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Why R4 is not marked DONE yet

The certification itself is complete, but R5 requires one exact immutable entry checkpoint. That SHA cannot be known before the closeout PR is merged. This checkpoint therefore records the real certification receipts without inventing a future SHA.

## Immediate action

Merge the validated R4 certification closeout, capture its immutable main SHA, and perform the minimal exact-entry activation that closes #267 and activates V3-R5/#272. Do not begin R5 work before that activation is canonical.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged. Do not redistribute proprietary Microsoft fonts. V3-A1/A2 scientific-article work and CTAN submission remain blocked until R5 closes.

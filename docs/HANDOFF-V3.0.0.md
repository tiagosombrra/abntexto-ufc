# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- R3-A and R3-B1 through R3-B5: **DONE**.
- R3-B5/#256 closeout: PR #268 → `d90a675a844724c33a5727d8d980027c46291eb0`.
- Final R3 product candidate: `c79f3c73f1d51a30175e8259269504d029442a1c`.
- PR #268 Static: `33825615520` — PASS.
- PR #268 Linux: `33825615541` / job `100877511446` — `PASS=31 FAIL=0 SKIP=0`.
- Exact-product release: `33824039033` / job `100872747975` — `PASS=33 FAIL=0 SKIP=0`.
- All R3-A findings: **RESOLVED**.
- Residual baseline: 305 sources (134 LaTeX + 171 engineering); retained test/check reachability: 148/148; zero orphans.
- V3-R4/#267: **ACTIVE** from exact predecessor `d90a675a844724c33a5727d8d980027c46291eb0`; certification execution has not started.
- Historical R1 certification remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; R4 must bind new certification evidence to `c79f3c73f1d51a30175e8259269504d029442a1c`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Execute V3-R4/#267 final certification on the exact current candidate. Certify literal Times New Roman and Arial across supported pdfLaTeX/LuaLaTeX routes, Unicode extraction, embedding, independent math-font policy and PDF/A-2b. Any temporary certification executor must be removed before the canonical checkpoint.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged. Do not redistribute proprietary Microsoft fonts. R5 foundation freeze, V3-A1/A2 scientific-article work, and CTAN submission remain blocked until R4 closes.

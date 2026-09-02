# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-8 — Final R1 Certification**.
- R1-BLOCK-7 status: **DONE**.
- Active B8 issue: **#227 — final R1 certification**.
- Active trunk: **`main`**.
- Latest merged B8 technical checkpoint: **`d2c24fc85351a410ea1f0101887b2a5228077741`** (PR #230).
- Last fully certified pre-B8 implementation checkpoint: `d7327db7efd5cc1e0ff9255195bcb9767d853d3e`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main` is the canonical source of truth and merge target. Short-lived branches are implementation vehicles only. Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree on phase/stage and fail closed on disagreement.

The machine state remains correctly at **V3-R1 / R1-BLOCK-8 / ACTIVE**. The additional evidence below advances B8 but does not close it.

## Completed R1 stages

| Stage | Status | Checkpoint / evidence |
|---|---|---|
| R1-S0 | DONE | repository sanitation and verified history governance |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` |
| R1-B8 | ACTIVE | strict POC/tooling path merged through `d2c24fc85351a410ea1f0101887b2a5228077741`; full candidate certification pending |

## Stable repository contracts already established

### Runtime and architecture

- `abntexto-ufc.cls` is the canonical class entry point.
- Runtime ownership is split across the current `abntexto-ufc/*.def` modules.
- Portuguese project runtime/API migration is deferred to V3-R2.
- Project-owned engineering language is English; academic/rendered Portuguese and official UFC/ABNT wording remain protected boundaries.

### Distribution

R1-B5 is DONE. `make distribution-bundles` produces deterministic class/runtime, CTAN candidate, template and Overleaf archives plus `SHA256SUMS`.

Public bundles must exclude institutional/proprietary assets. Microsoft Times New Roman and Arial binaries are never committed or redistributed. Actual CTAN submission remains a later explicit release action.

### Validation and CI

R1-B6 and R1-B7 are DONE.

Permanent entry points:

- `make static-check` — source-only, side-effect-free contract;
- `make check` — PR-oriented integration contract;
- `make release-check` — release-oriented integration contract.

Permanent workflows:

- `Static contract`;
- `Linux integration`;
- `Linux release check`.

B7 evidence includes clean TeX Live 2026 `make check` at `PASS=30 FAIL=0 SKIP=0` and merged-main `Linux release check` run `33566835570` at `PASS=32 FAIL=0 SKIP=0`, including `pdfa` and `profile-pdfa`.

The `Stable branches` ruleset currently has no required-status rule. The standing recommendation is to require `Static contract` and `Linux integration`; `Linux release check` remains post-merge/manual.

## R1-BLOCK-8 — Current state

B8 owns the final Windows/literal-font/PDF-A certification. It must not absorb V3-R2 runtime/API migration or actual CTAN submission.

### Completed B8 evidence

#### Windows/TS1 bring-up

Probe `33573481272` passed on hosted Windows Server 2025 / TeX Live 2026. The current TS1 metric vector is deterministically derived from `q-ts1-uni.enc` using `glyphlist.txt` and `texglyphlist.txt`; the probe mapped 80 slots, left 49 unsupported slots as `.notdef`, and completed `ttf2tfm` + `vptovf` against the real Windows `times.ttf`.

#### B8 tooling repair

PR #230 merged at **`d2c24fc85351a410ea1f0101887b2a5228077741`**.

Bounded changes:

- replaced the removed `ts1-winfonts.enc` dependency with current deterministic TeX Live derivation;
- repaired the font POC repository root;
- repaired Windows PDF/A checker consumers;
- removed retired V2 technical wording from the embedding checker;
- retained proprietary Microsoft fonts outside the repository/distribution.

No class/runtime/API, normative rule/value/tolerance/locator or proof-state change occurred.

#### Strict literal-font POC certification

Run **`33609817951` SUCCESS** generated all four strict artifacts on hosted Windows:

- Times New Roman × pdfLaTeX;
- Times New Roman × LuaLaTeX;
- Arial × pdfLaTeX;
- Arial × LuaLaTeX.

Linux certification job `100182981215` passed every artifact for:

- literal font identity;
- no unexpected text fallback;
- Unicode extraction;
- font embedding (`emb=yes`);
- PDF/A-2b via veraPDF 1.30.2.

Evidence artifact: `windows-font-pdfs`, artifact ID `9838603822`, digest `sha256:45fb1317a8f9eb3442ed8f7c8cfb8c32208b18d5a10adeed7b861a8e7ccff84c`.

### Remaining B8 work

The strict POC proves the platform/tooling/font path, but R1-BLOCK-8 is **not closed** yet.

Immediate technical action:

1. certify the complete `template/main.tex` candidate from canonical merged checkpoint `d2c24fc85351a410ea1f0101887b2a5228077741` (or a later canonical `main` containing only reconciled documentation changes);
2. build supported pdfLaTeX/LuaLaTeX candidate paths on hosted Windows using the certified font preparation chain;
3. inspect resulting candidate PDFs fail-closed for literal font identity where required, unexpected fallback, Unicode extraction, embedding and PDF/A-2b;
4. retain run IDs, artifact IDs and digests as machine-readable receipts;
5. reject partial certification if any required matrix leg fails.

After that proof passes:

1. reconcile `release/v3-roadmap.json` with the final R1 checkpoint and evidence;
2. update roadmap/handoff/bootstrap/public documentation to mark B8 DONE;
3. close issue #227 as completed;
4. explicitly activate the next approved phase/stage;
5. only then permit V3-R2 runtime/API migration.

## Hard boundaries for the next session

- Do not infer B8 closure from the strict POC alone.
- Do not rerun completed Linux product gates without current-state need.
- Do not change normative rule IDs, expected values, tolerances, locators or proof state without explicit new normative evidence.
- Do not redistribute Times New Roman, Arial or other proprietary Microsoft font files.
- Do not perform V3-R2 runtime/API migration during B8.
- Do not perform or claim actual CTAN submission/acceptance during B8.
- Temporary certification workflows/executors must be removed before a checkpoint.

## Immediate action

Execute the **full `template/main.tex` B8 certification** from the canonical merged B8 tooling checkpoint, then reconcile and close R1 only if the complete candidate evidence passes fail-closed.

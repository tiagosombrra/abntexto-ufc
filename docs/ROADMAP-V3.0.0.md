# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 ACTIVE — R1-BLOCK-8 final certification in progress.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 DONE → R1-B5 DONE → R1-B6 DONE → R1-B7 DONE → R1-B8 ACTIVE → R2+ BLOCKED**

Canonical repository: `tiagosombrra/abntexto-ufc`.

Active trunk: `main`.

B8 operational issue: #227.

Latest merged B8 technical checkpoint: **`d2c24fc85351a410ea1f0101887b2a5228077741`** (PR #230).

Last fully certified pre-B8 implementation checkpoint: `d7327db7efd5cc1e0ff9255195bcb9767d853d3e`.

Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority

`release/v3-roadmap.json` is the machine authority. This roadmap, `docs/HANDOFF-V3.0.0.md`, `AGENTS.md`, and the current Git facts provide the human-readable control plane. Disagreement fails closed.

The machine state remains correctly at `R1-BLOCK-8 / ACTIVE`; this document records additional B8 progress without prematurely closing the block.

## Roadmap summary

| Stage | Status | Certified / relevant checkpoint | Result | Remaining work |
|---|---|---|---|---|
| R1-S0 | DONE | repository sanitation | Active tree and history governance rebaselined | None |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` | Control plane repaired | None |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` | v3 promoted to `main` without history rewrite | None |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` | Canonical physical naming | None |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` | Legacy purge and active-tree minimization | None |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` | Semantic/path-consumer closure | None |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` | Tools, validator, metadata and engineering-language rebaseline | None |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic class/template/Overleaf/CTAN candidates and checksums | Actual CTAN submission remains a later explicit release action |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent source-only `make static-check` gate | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized remote orchestration | Optional governance action: require `Static contract` and `Linux integration` in the branch ruleset |
| R1-B8 | ACTIVE | PR #230 merged at `d2c24fc85351a410ea1f0101887b2a5228077741` | Strict Windows literal-font POC certified | Certify complete `template/main.tex` candidate from canonical merge SHA; reconcile final control plane; close #227 |
| V3-R2 | BLOCKED | — | Runtime/API internationalization and Portuguese project API migration | Starts only after R1-B8 closes |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification phase | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and current migration/user/maintainer documentation | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | Resume only against certified v3 foundation |

## Completed R1 reconstruction

### R1-BLOCK-1 — Canonical physical naming

**DONE.** Canonical class/module/repository naming was established and retired physical identities were removed from the active tree.

### R1-BLOCK-2 — Legacy purge and active-tree minimization

**DONE.** Dead compatibility/archive material was removed from the active product tree while history remained recoverable through Git evidence.

### R1-BLOCK-3 — Semantic and path-consumer closure

**DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`.

The block removed stale path/process/version identity, obsolete distribution-era implementation, obsolete project-owned validation terminology, runner/evidence defects and residual consumer inconsistencies without changing runtime/API or normative semantics.

### R1-BLOCK-4 — Tools, validator, and metadata technical rebaseline

**DONE** through `1a126c37653728941ce1ada762376c5fec69cb02`.

Key outcomes:

- active `tools/` and `validator/` ownership classified;
- `spine.conditional` fail-closed validation semantics reconciled without changing the normative rule;
- project-owned validator statuses, verdicts, diagnostics, technical taxonomy and Web/CLI engineering vocabulary normalized to English;
- academic/rendered Portuguese and official UFC/ABNT wording preserved;
- Portuguese LaTeX runtime/API migration explicitly deferred to V3-R2;
- Windows-font tooling retained as B8-owned certification infrastructure.

### R1-BLOCK-5 — Distribution and public bundle rebaseline

**DONE** at `4bc0f544020234bc14a8f2261927f65721b6eddb`.

The current deterministic distribution producer emits:

- `abntexto-ufc-3.0.0.zip`;
- `abntexto-ufc-ctan-3.0.0.zip`;
- `abntexto-ufc-template-3.0.0.zip`;
- `abntexto-ufc-overleaf-3.0.0.zip`;
- `SHA256SUMS`.

The public contract excludes institutional/proprietary assets, keeps `abntexto` external except in the self-contained Overleaf bundle, and has passed reproducibility, TeX Live installation/compilation and CTAN `pkgcheck` validation. Actual CTAN submission is not part of R1.

### R1-BLOCK-6 — Permanent cheap/static fail-closed gates

**DONE** at `4c25c27b758e4b99db11187b34b9043776566871`.

`tests/static.py` and `make static-check` are the permanent side-effect-free source-only contract. The gate remains intentionally separate from TeX/PDF, evidence-producing and platform-certification work.

### R1-BLOCK-7 — Optimized remote workflow restoration

**DONE** at `d7327db7efd5cc1e0ff9255195bcb9767d853d3e`.

Permanent workflow surface:

- `Static contract` → `make static-check`;
- `Linux integration` → `make check`;
- `Linux release check` → `make release-check`.

Certified evidence includes clean TeX Live 2026 `make check` at `PASS=30 FAIL=0 SKIP=0` and the first permanent merged-main `Linux release check`, run `33566835570`, at `PASS=32 FAIL=0 SKIP=0`, including release-only `pdfa` and `profile-pdfa`.

B7-D confirmed exactly three permanent workflows, read-only repository permissions, pinned actions, bounded concurrency and zero temporary workflow residue. The `Stable branches` ruleset currently has no required-status rule; the recommendation remains to require `Static contract` and `Linux integration`, while `Linux release check` remains post-merge/manual.

## R1-BLOCK-8 — Final R1 certification

**ACTIVE** through issue #227.

### B8 entry

B8 entered from the certified B7 checkpoint `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` after the B7→B8 control-plane transition was merged through PR #228 and reconciled through PR #229.

Scope:

- hosted Windows certification;
- literal Times New Roman and Arial identity where strict certification requires them;
- supported pdfLaTeX/LuaLaTeX matrix;
- Unicode extraction;
- font embedding;
- PDF/A-2b validation;
- machine-readable evidence receipts;
- no proprietary Microsoft font redistribution;
- no V3-R2 runtime/API migration.

### B8-A — Windows/font certification tooling bring-up

**DONE** through PR #230, merged at **`d2c24fc85351a410ea1f0101887b2a5228077741`**.

The bring-up repaired only B8-owned tooling/checker surfaces:

- replaced the removed `ts1-winfonts.enc` dependency with deterministic TS1 metric derivation from current TeX Live `q-ts1-uni.enc` plus `glyphlist.txt` / `texglyphlist.txt`;
- repaired the strict font POC repository-root calculation;
- repaired Windows PDF/A checker consumers to use current integration checkers;
- removed retired V2 engineering wording from the font-embedding checker;
- kept Microsoft font binaries external to the repository and distribution artifacts.

No `.cls` runtime/API, normative rule/value/tolerance/locator or proof-state change was made.

### B8-B — Strict literal-font POC matrix

**DONE.** Final bounded strict POC run **`33609817951` SUCCESS**.

Hosted Windows Server 2025 / TeX Live 2026 generated all four strict cases:

- Times New Roman × pdfLaTeX;
- Times New Roman × LuaLaTeX;
- Arial × pdfLaTeX;
- Arial × LuaLaTeX.

Linux certification job `100182981215` completed successfully for every artifact and verified:

- literal font identity;
- no unexpected text-font fallback;
- Unicode text extraction;
- font embedding with `emb=yes`;
- PDF/A-2b via veraPDF 1.30.2.

Evidence artifact: `windows-font-pdfs`, artifact ID `9838603822`, digest `sha256:45fb1317a8f9eb3442ed8f7c8cfb8c32208b18d5a10adeed7b861a8e7ccff84c`.

The TS1 derivation path was independently grounded by run `33573481272`, which mapped 80 slots, left 49 unsupported slots as `.notdef`, and completed `ttf2tfm` + `vptovf` against the real Windows `times.ttf`.

### B8-C — Full candidate certification

**PENDING — immediate technical action.**

Certify the complete `template/main.tex` candidate from canonical merged checkpoint `d2c24fc85351a410ea1f0101887b2a5228077741` using the now-certified Windows/font tooling.

Required proof:

1. build the complete candidate on hosted Windows for supported pdfLaTeX and LuaLaTeX paths;
2. exercise the literal Times New Roman / Arial requirements applicable to the current class/profile contract;
3. inspect resulting artifacts fail-closed on Linux for literal font identity, unexpected fallback, Unicode extraction, embedding and PDF/A-2b;
4. retain machine-readable artifact/run/digest receipts;
5. do not promote partial output if any matrix leg fails.

### B8-D — Final closeout and R2 handoff

**PENDING.** After B8-C passes:

- update `release/v3-roadmap.json` with the final certified R1 checkpoint and B8 evidence;
- update this roadmap, `docs/HANDOFF-V3.0.0.md`, `README.md`, `AGENTS.md`, and architecture/release guidance where relevant;
- close issue #227 as completed;
- transition the machine/human control plane from `V3-R1 / R1-BLOCK-8` to the explicitly approved next stage;
- only then permit V3-R2 runtime/API work.

## Immediate action

Execute **B8-C full candidate certification** from canonical `main` at or after merge checkpoint `d2c24fc85351a410ea1f0101887b2a5228077741`.

Do not rerun already-certified Linux product gates without current-state need, do not perform the V3-R2 runtime/API migration, do not redistribute proprietary Microsoft fonts, and do not perform an actual CTAN submission during this step.

#!/usr/bin/env python3

import json
from pathlib import Path

CANDIDATE = "9b1752565ac217c04ffa22a9ef272cdf078af380"
TOOLING = "d2c24fc85351a410ea1f0101887b2a5228077741"
WINDOWS_DIGEST = "138b9a4e3c2969db33c512bec91b323cba339bb6ae18afc76786b59d2e0f7a21"
EVIDENCE_DIGEST = "256c96e1c32d839b5b3a3e55f7a355913b7b217609c2f6e2d27104e7e12ffeeb"


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, got {count}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Preserve all accumulated R1 evidence and mutate only current machine state.
p = Path("release/v3-roadmap.json")
road = json.loads(p.read_text(encoding="utf-8"))
road.update({
    "updated_at": "2026-09-02",
    "status": "ACTIVE",
    "phase": "V3-R2",
    "stage": "R2-A",
    "stage_name": "runtime/API ownership inventory and migration plan",
    "last_certified_clean_checkpoint_sha": CANDIDATE,
    "r1_status": "DONE",
})
b8 = road["blocks"]["R1-BLOCK-8"]
b8.update({
    "status": "DONE",
    "b8_status": "DONE",
    "certified_candidate_sha": CANDIDATE,
    "tooling_checkpoint_sha": TOOLING,
    "b8_a_status": "DONE",
    "b8_a_pr": 230,
    "b8_b_status": "DONE",
    "b8_b_strict_poc_run_id": 33609817951,
    "b8_c_status": "DONE",
    "b8_d_status": "DONE",
    "closure_date": "2026-09-02",
    "final_certification": {
        "candidate_sha": CANDIDATE,
        "windows_source_run_id": 33649620219,
        "windows_job_id": 100313006509,
        "windows_matrix_result": "PASS",
        "windows_artifact_id": 9854415113,
        "windows_artifact_digest": WINDOWS_DIGEST,
        "linux_final_inspection_run_id": 33655108349,
        "linux_final_inspection_job_id": 100331601354,
        "linux_final_inspection_result": "PASS",
        "evidence_artifact_id": 9856387211,
        "evidence_artifact_digest": EVIDENCE_DIGEST,
        "matrix": ["times/pdflatex", "arial/pdflatex", "times/lualatex", "arial/lualatex"],
        "literal_text_family_passed": True,
        "math_font_policy_separated_from_text_family": True,
        "pdftex_math_policy": "NEW-TX-MATH",
        "unicode_extraction_passed": True,
        "font_embedding_passed": True,
        "pdfa_2b_passed": True,
        "false_positive_reconciled": "TeXGyreTermesX-Regular is a legitimate newtxmath component in pdfLaTeX, not institutional text fallback",
        "runtime_api_changed": False,
        "normative_semantics_changed": False,
        "proof_state_changed": False,
        "proprietary_fonts_redistributed": False,
        "temporary_workflows_present": False,
    },
    "operational_issue_close_after_control_plane_merge": 227,
})
road["r2"] = {
    "status": "ACTIVE",
    "stage": "R2-A",
    "stage_name": "runtime/API ownership inventory and migration plan",
    "operational_issue": 232,
    "entry_candidate_sha": CANDIDATE,
    "entry_scope": [
        "inventory remaining project-owned Portuguese runtime/API surface",
        "classify upstream non-English identifiers separately",
        "map public-api.def forwarding aliases to direct responsibility owners",
        "define bounded migration lots and atomic producer/consumer/test/template changes",
    ],
    "constraints": [
        "inventory and classification before behavioral migration",
        "preserve rendered document behavior during ownership mapping",
        "preserve normative rule IDs values tolerances locators and proof state without new evidence",
        "do not add another runtime compatibility layer",
        "do not perform actual CTAN submission",
        "do not redistribute proprietary Microsoft fonts",
    ],
}
road["next_action"] = (
    "Execute V3-R2 / R2-A through issue #232. Inventory and classify every remaining "
    "project-owned Portuguese runtime/API surface and every forwarding mapping in "
    "abntexto-ufc/public-api.def, assign direct behavior owners, and define bounded migration "
    "lots before changing runtime behavior. Preserve rendered semantics and normative proof state; "
    "do not perform actual CTAN submission or redistribute proprietary fonts."
)
p.write_text(json.dumps(road, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Activate the existing R2 migration contract.
p = Path("release/v3-api-migration.json")
api = json.loads(p.read_text(encoding="utf-8"))
api.update({
    "phase": "V3-R2",
    "status": "ACTIVE_R2_A_INVENTORY",
    "activated_at": "2026-09-02",
    "operational_issue": 232,
    "entry_certified_r1_candidate_sha": CANDIDATE,
    "current_stage": "R2-A",
    "current_stage_goal": "inventory runtime/API ownership and define bounded migration lots before behavioral changes",
})
p.write_text(json.dumps(api, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

roadmap = f'''# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-A runtime/API ownership inventory and migration planning.**

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 DONE → R1-B5 DONE → R1-B6 DONE → R1-B7 DONE → R1-B8 DONE → R2-A ACTIVE → R2-B+ PENDING**

Canonical repository: `tiagosombrra/abntexto-ufc`. Active trunk: `main`.

Certified R1 product candidate: **`{CANDIDATE}`**. R1 closure issue: #227. Active R2-A issue: #232.

## Authority

`release/v3-roadmap.json` is the machine authority. This roadmap, `docs/HANDOFF-V3.0.0.md`, `AGENTS.md`, and current Git facts form the human-readable control plane. Disagreement fails closed.

## Roadmap summary

| Stage | Status | Checkpoint / evidence | Result | Remaining work |
|---|---|---|---|---|
| R1-S0 | DONE | repository sanitation | History governance rebaselined | None |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` | Control plane repaired | None |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` | v3 promoted to `main` | None |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` | Canonical physical naming | None |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` | Legacy purge/minimization | None |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` | Semantic/path-consumer closure | None |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` | Tools/validator/metadata/language rebaseline | None |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic release/public bundles | CTAN upload is a later explicit release action |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent `make static-check` | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized workflows | Optional branch-rule enforcement |
| R1-B8 | DONE | `{CANDIDATE}`; runs `33649620219` + `33655108349` | Full Windows/font/Unicode/embedding/PDF-A certification | None |
| V3-R2 / R2-A | ACTIVE | issue #232 | Runtime/API ownership inventory and migration planning | Complete classification before behavioral migration |
| V3-R2 / R2-B+ | PENDING | — | Direct-ownership migration lots | Defined by R2-A |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification phase | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and migration/user/maintainer docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |

## Final R1-B8 certification

B8-A tooling repair merged through PR #230 at `{TOOLING}`. B8-B strict POC run `33609817951` proved the literal-font pipeline.

B8-C certified complete `template/main.tex`:

- Windows run `33649620219`, job `100313006509`: all Times New Roman/Arial × pdfLaTeX/LuaLaTeX builds PASS;
- Windows artifact `9854415113`, digest `sha256:{WINDOWS_DIGEST}`;
- final Linux inspection run `33655108349`, job `100331601354`: PASS;
- evidence artifact `9856387211`, digest `sha256:{EVIDENCE_DIGEST}`;
- literal institutional text-family identity: PASS;
- independent engine-appropriate math-font policy: PASS;
- Unicode extraction: PASS;
- font embedding (`emb=yes`): PASS;
- PDF/A-2b: PASS.

The earlier `TeXGyreTermesX-Regular` flag was a checker false positive: it is part of the pdfLaTeX `newtxmath` stack and is not institutional text-family fallback. The final inspection separates text-family identity from math-font policy.

No runtime/API, normative semantics, locator/tolerance, proof-state, or proprietary-font distribution change occurred. Temporary B8 executors were removed.

## V3-R2 — Runtime/API internationalization

### R2-A — Ownership inventory and migration plan

**ACTIVE via issue #232.** This stage is inventory/classification only. It must inventory remaining project-owned Portuguese setup keys/values, commands, environments, hooks and internal behavior owners; classify genuine upstream non-English boundaries; map every canonical English forwarding surface in `abntexto-ufc/public-api.def` to a direct responsibility owner; and define atomic producer/consumer/test/template/documentation migration lots.

`release/v3-api-migration.json` is active. `public-api.def` is transitional R2 debt. Final v3 exposes one canonical project API implemented directly by responsibility-owning modules; removed Portuguese v2 project API is not retained through runtime aliases.

### R2-A exit condition

Every remaining project-owned Portuguese runtime/API surface and every `public-api.def` forwarding mapping has an explicit classification, direct owner, migration lot and validation plan.

## Immediate action

Execute R2-A issue #232. Inventory and classify first; do not perform blind global replacement, normative semantic changes without new evidence, proprietary font redistribution, or actual CTAN submission.
'''
Path("docs/ROADMAP-V3.0.0.md").write_text(roadmap, encoding="utf-8")

handoff = f'''# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-A — Runtime/API ownership inventory and migration plan**.
- R1 / R1-BLOCK-8: **DONE**.
- R1 closure issue: **#227**.
- Active R2-A issue: **#232**.
- Active trunk: **`main`**.
- Certified R1 candidate: **`{CANDIDATE}`**.
- B8 tooling checkpoint: `{TOOLING}` (PR #230).
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main`, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and Git facts must agree; disagreement fails closed.

## Completed R1

| Stage | Status | Checkpoint / evidence |
|---|---|---|
| R1-S0 | DONE | repository sanitation/history governance |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` |
| R1-B8 | DONE | `{CANDIDATE}`; Windows `33649620219`; final inspection `33655108349` |

## Stable contracts entering R2

- `abntexto-ufc.cls` is the sole canonical class entry point.
- `public-api.def` is transitional R2 debt: canonical English API currently forwards to Portuguese behavior owners.
- Final public behavior must be owned directly by responsibility modules; removed Portuguese v2 project API must not survive as runtime aliases.
- Genuine upstream non-English identifiers may remain only at explicit integration boundaries.
- Academic/rendered Portuguese and official UFC/ABNT wording are protected domain content, not engineering-identifier debt.
- `make static-check`, `make check`, and `make release-check` remain the repository-owned validation entry points.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Public bundles exclude proprietary Microsoft fonts/institutional assets as already defined; actual CTAN submission remains separate.

## Final B8 evidence

Windows run `33649620219` built all four complete strict candidates. Artifact ID `9854415113`, digest `sha256:{WINDOWS_DIGEST}`.

Final Linux run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, full embedding and PDF/A-2b. Evidence artifact ID `9856387211`, digest `sha256:{EVIDENCE_DIGEST}`.

`TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not text fallback. No runtime/API or normative/proof-state change was required. No proprietary font was redistributed. No temporary B8 workflow remains.

## V3-R2 / R2-A

Issue #232 is active and `release/v3-api-migration.json` is the current migration contract.

R2-A must inventory/classify before changing behavior: remaining Portuguese project-owned setup keys/values, commands, environments, hooks, internals; `public-api.def` forwarding aliases; genuine upstream boundaries; direct owning modules; and atomic producer/consumer/test/template/doc migration lots.

## Hard boundaries

- No blind global replacement.
- Preserve rendered behavior during ownership mapping.
- Preserve normative rule IDs, values, tolerances, locators and proof state absent explicit new evidence.
- Do not replace `public-api.def` with another compatibility layer.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform or claim actual CTAN submission/acceptance during R2-A.
- Do not rerun completed heavy certification gates without current-state need.

## Immediate action

Execute R2-A issue #232 and produce the complete ownership inventory plus bounded migration-lot plan. Only then begin the first behavioral migration lot.
'''
Path("docs/HANDOFF-V3.0.0.md").write_text(handoff, encoding="utf-8")

replace_once(
    "README.md",
    "V3-R1 is active in **R1-BLOCK-8 — final R1 certification**. R1-BLOCK-7 is complete. The current B8 tooling checkpoint is PR #230, merged at `d2c24fc85351a410ea1f0101887b2a5228077741`.\n\nThe strict literal-font POC has already passed: hosted Windows Server 2025 / TeX Live 2026 generated Times New Roman and Arial artifacts with both pdfLaTeX and LuaLaTeX, and Linux certification verified literal font identity, Unicode extraction, font embedding and PDF/A-2b for all four artifacts. R1-BLOCK-8 remains active because the complete `template/main.tex` candidate still requires final certification from the canonical merged checkpoint before R1 can close.",
    f"**V3-R1 is DONE. V3-R2 is ACTIVE in R2-A — runtime/API ownership inventory and migration plan, tracked by issue #232.**\n\nThe certified R1 candidate is `{CANDIDATE}`. Windows run `33649620219` built the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX `template/main.tex` matrix. Final Linux inspection run `33655108349` passed literal institutional text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b for all four artifacts. No runtime/API, normative semantics or proof-state change was required, and no proprietary Microsoft font was redistributed."
)
replace_once(
    "README.md",
    "Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. During R1 the current runtime API remains unchanged while engineering surfaces are rebaselined; direct runtime/API internationalization belongs to R2.",
    "Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 preserved the runtime/API while rebuilding and certifying the foundation. R2 is now active; R2-A performs ownership inventory and migration planning before any direct runtime/API migration."
)
replace_once(
    "README.md",
    "R1-BLOCK-8 is ACTIVE through issue #227. The bounded Windows/font tooling repair is merged through PR #230. Strict POC run `33609817951` passed the Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix and downstream literal-font/Unicode/embedding/PDF-A inspection. The remaining R1 product gate is final certification of the complete `template/main.tex` candidate from the canonical merged B8 tooling checkpoint.",
    "R1-BLOCK-8 is DONE. Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. Final Linux inspection run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b. `TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. V3-R2/R2-A is active through issue #232."
)

replace_once(
    "AGENTS.md",
    "- R1-BLOCK-8 is ACTIVE via issue #227. PR #230 merged the bounded Windows/literal-font tooling repair at `d2c24fc85351a410ea1f0101887b2a5228077741`.\n- B8 strict POC certification is DONE: run `33609817951` generated Times New Roman/Arial × pdfLaTeX/LuaLaTeX on hosted Windows; Linux certification verified literal identity, Unicode extraction, embedding and PDF/A-2b for all four artifacts.\n- B8 is not closed by the POC. The immediate product gate is full `template/main.tex` certification from the canonical merged B8 tooling checkpoint, followed by final control-plane reconciliation and issue #227 closure only if that candidate proof passes fail-closed.\n- Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not default cheap checks.\n- Do not rerun completed checks unless current-state validation requires it.\n- Do not redistribute proprietary Microsoft fonts.\n- Do not perform actual CTAN submission or V3-R2 runtime/API migration while R1-BLOCK-8 remains active.",
    f"- R1-BLOCK-8 is DONE. The certified R1 candidate is `{CANDIDATE}`.\n- Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix; final Linux run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b.\n- V3-R2 is ACTIVE in R2-A via issue #232. R2-A is inventory/classification and migration planning before behavioral changes.\n- `public-api.def` is transitional R2 debt. Final canonical public behavior must be implemented directly by responsibility-owning modules; removed Portuguese v2 project API is not retained through runtime aliases.\n- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state during R2-A unless explicit new evidence authorizes a normative change.\n- Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not default cheap checks.\n- Do not rerun completed checks unless current-state validation requires it.\n- Do not redistribute proprietary Microsoft fonts.\n- Do not perform actual CTAN submission during R2-A."
)

replace_once("docs/ARCHITECTURE.md", "Updated: 2026-09-01", "Updated: 2026-09-02")
replace_once(
    "docs/ARCHITECTURE.md",
    "R1-BLOCK-7 is DONE. The permanent orchestration surface is exactly `Static contract`, `Linux integration`, and `Linux release check`, each delegating to its repository-owned entry point (`make static-check`, `make check`, and `make release-check`). B7-D confirmed read-only permissions, immutable action pins, bounded concurrency, stable status semantics, and zero temporary workflow residue. The current `Stable branches` ruleset has no required-status rule; the recorded recommendation is to require `Static contract` and `Linux integration`, while `Linux release check` remains a post-merge/manual release gate. R1-BLOCK-8 is ACTIVE via issue #227 and owns final Windows/literal-font/PDF-A certification.",
    f"R1-BLOCK-7 and R1-BLOCK-8 are DONE. The permanent orchestration surface is exactly `Static contract`, `Linux integration`, and `Linux release check`, each delegating to its repository-owned entry point (`make static-check`, `make check`, and `make release-check`). B7-D confirmed read-only permissions, immutable action pins, bounded concurrency, stable status semantics, and zero temporary workflow residue. The current `Stable branches` ruleset has no required-status rule; the recorded recommendation is to require `Static contract` and `Linux integration`, while `Linux release check` remains a post-merge/manual release gate. B8 certified complete candidate `{CANDIDATE}` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX with final literal text-family, math-policy, Unicode, embedding and PDF/A-2b inspection. V3-R2 is active; `public-api.def` remains transitional R2 debt until canonical public behavior is absorbed directly by responsibility-owning modules."
)

replace_once(
    "docs/CTAN-RELEASE.md",
    "R1-BLOCK-7 is complete. Its Linux result is an engineering gate, not final release certification. B7-D confirmed the permanent workflow inventory and recorded `Static contract` plus `Linux integration` as the recommended required PR checks; `Linux release check` remains post-merge/manual. R1-BLOCK-8 is now ACTIVE via issue #227 for literal Times New Roman/Arial identity and final Windows/font/PDF-A certification. CTAN packaging and current `pkgcheck` validation remain separate release procedures below. Validation evidence under `artifacts/validation/` is not a distribution artifact and must not be inserted into public bundles.",
    f"R1-BLOCK-7 and R1-BLOCK-8 are complete. B7-D confirmed the permanent workflow inventory and recorded `Static contract` plus `Linux integration` as the recommended required PR checks; `Linux release check` remains post-merge/manual. B8 certified complete candidate `{CANDIDATE}`: Windows run `33649620219` passed Times New Roman/Arial × pdfLaTeX/LuaLaTeX, and final Linux inspection run `33655108349` passed literal text-family identity, expected math-font policy, Unicode extraction, embedding and PDF/A-2b. This engineering certification is not CTAN acceptance. CTAN packaging and current `pkgcheck` validation remain separate release procedures below. Validation/B8 evidence is not a distribution artifact and must not be inserted into public bundles."
)
replace_once(
    "docs/CTAN-RELEASE.md",
    "3. Complete the separate B8 Windows/literal-font/PDF-A certification required for the release candidate.",
    "3. Confirm that the intended release commit is still covered by, or has proportionally re-established, the completed Windows/literal-font/PDF-A certification baseline from R1-BLOCK-8."
)

# Normative documents are intentionally unchanged: no normative semantics or proof state changed.
for file_name in ("release/v3-roadmap.json", "release/v3-api-migration.json"):
    json.loads(Path(file_name).read_text(encoding="utf-8"))

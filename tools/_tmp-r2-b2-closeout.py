#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

B1_MERGE = "ded5e77733795aa2958606e899d4e27f12f64df4"
B2_ENTRY = "e418893ee5c89f12cc4ac8d845111c894ec946e4"
B2_HEAD = "4341a2adb4633b634d1e2ad905b1731e8126354b"
B2_MERGE = "8e3e0f2a165e488a00f08a0031ba6fb4a01f9949"
B2_STATIC = 33680378948
B2_LINUX = 33680378846
B2_LINUX_JOB = 100415223907
B2_AUDIT = 33680252116
B2_AUDIT_JOB = 100414804865
B2_FAIL_CLOSED = 33679535751
B2_EXECUTOR_PASS = 33679827267
B2_EXECUTOR_JOB = 100413437018

B2_NAME = "academic and front-matter public rendering API"
B3_NAME = "structural/object environments optional object API and extension hooks"


def path(name: str) -> Path:
    return ROOT / name


def replace_once(file: str, old: str, new: str) -> None:
    p = path(file)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{file}: expected one occurrence, found {count}: {old!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def replace_all(file: str, old: str, new: str, expected: int) -> None:
    p = path(file)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{file}: expected {expected} occurrences, found {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def regex_once(file: str, pattern: str, replacement: str, flags: int = 0) -> None:
    p = path(file)
    text = p.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"{file}: regex expected one occurrence, found {count}: {pattern!r}")
    p.write_text(updated, encoding="utf-8")


# ROADMAP
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "**V3-R1 DONE. V3-R2 ACTIVE — R2-B2 academic and front-matter public rendering API.**",
    "**V3-R1 DONE. V3-R2 ACTIVE — R2-B3 structural/object API ownership.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"Canonical R2-B1 implementation checkpoint on `main`: `{B1_MERGE}`. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.",
    f"Canonical R2-B2 merged checkpoint on `main`: `{B2_MERGE}`. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "R2-A ownership inventory is DONE through issue #232. R2-B1 is DONE through issue #234 / PR #236. Active implementation issue: #237. Machine authority: `release/v3-roadmap.json`.",
    "R2-A ownership inventory, R2-B1 and R2-B2 are DONE. B2 merged through issue #237 / PR #242. Active implementation issue: #238. Machine authority: `release/v3-roadmap.json`.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| R2-B2 | ACTIVE | issue #237 | Academic/front-matter public rendering API | Direct ownership, consumer migration and validation |\n| R2-B3 | PENDING | issue #238 | Structural/object environments, optional object API and hooks | After B2 |",
    f"| R2-B2 | DONE | issue #237; PR #242 → `{B2_MERGE}` | Academic/front-matter rendering API directly owned; final integration `PASS=30 FAIL=0 SKIP=0` | None |\n| R2-B3 | ACTIVE | issue #238 | Structural/object environments, optional object API, extension hooks and project-owned object IDs | Direct ownership, atomic consumer migration and validation |",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline evidence behavior inside a passing aggregate gate and were not changed in B1 because no new normative evidence authorized a semantic change.\n\nSee `docs/R2-API-OWNERSHIP.md`",
    f"The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline evidence behavior inside a passing aggregate gate and were not changed in B1 because no new normative evidence authorized a semantic change.\n\nR2-B2 moved the complete academic/front-matter rendering surface into direct canonical ownership, rebound layout hooks, migrated template/tests/CTAN source/scenario consumers, and removed all B2 forwards from `public-api.def`. The bounded executor first failed closed in run `{B2_FAIL_CLOSED}` on its own cleanup order; after executor repair, run `{B2_EXECUTOR_PASS}` passed. Human review then found hook identifiers and the illustration-list specialization that the initial scan did not cover; strengthened audit `{B2_AUDIT}` closed those gaps. Final head `{B2_HEAD}` passed `Static contract` run `{B2_STATIC}` and `Linux integration` run `{B2_LINUX}`, job `{B2_LINUX_JOB}`, at `PASS=30 FAIL=0 SKIP=0`; PR #242 squash-merged to `main` at `{B2_MERGE}`. No runtime alias layer, normative semantic/proof-state change, proprietary font redistribution or CTAN submission occurred.\n\nSee `docs/R2-API-OWNERSHIP.md`",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## Immediate action\n\nExecute \*\*R2-B2 issue #237\*\*.*\n$",
    "## Immediate action\n\nExecute **R2-B3 issue #238** from canonical `main`. Make `ufclettereditems`, `ufcdashedsubitems`, `ufcdefinitionlist`, `ufcobject`, `ufclisting`, and `ufcalgorithm` direct owners; migrate source/note, object-list, listing/minted APIs, extension hooks, project-owned `codigo` / `algoritmo` object IDs, and all live consumers atomically. Preserve genuine upstream `grafico` / `quadro` identifiers only at explicit integration boundaries and preserve rendered Portuguese labels. Remove only B3 forwarding debt from `public-api.def`; leave bibliography/back-matter B4 debt in place. Do not add runtime aliases, alter normative proof state without evidence, redistribute proprietary fonts or perform actual CTAN submission.\n",
    re.S,
)

# HANDOFF
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    f"- R2-B1 merged checkpoint on `main`: `{B1_MERGE}`.\n- Phase: **V3-R2 ACTIVE**.\n- Active stage: **R2-B2 — academic and front-matter public rendering API**.\n- Active implementation issue: **#237**.\n- R2-B1 issue #234: **DONE through PR #236**.",
    f"- R2-B2 merged checkpoint on `main`: `{B2_MERGE}`.\n- Phase: **V3-R2 ACTIVE**.\n- Active stage: **R2-B3 — structural/object API ownership**.\n- Active implementation issue: **#238**.\n- R2-B2 issue #237: **DONE through PR #242**.\n- R2-B1 issue #234: **DONE through PR #236**.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "R2-A classified direct behavior owners and upstream boundaries. R2-B1 then moved the complete canonical setup/internal-state vocabulary into those owners with all live consumers migrated atomically.",
    "R2-A classified direct behavior owners and upstream boundaries. R2-B1 moved the complete canonical setup/internal-state vocabulary into those owners. R2-B2 then moved academic/front-matter rendering commands and their live consumers/hooks into direct canonical ownership.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "The observational `FRONTMATTER-EVIDENCE` internal FAIL records seen inside the passing front-matter gate predate B1 and match the certified green baseline. They are not B1 regressions and remain outside this API migration lot absent new normative evidence.\n\n## Current runtime/API state",
    f"The observational `FRONTMATTER-EVIDENCE` internal FAIL records seen inside the passing front-matter gate predate B1 and match the certified green baseline. They are not B1 regressions and remain outside this API migration lot absent new normative evidence.\n\n## R2-B2 closure evidence\n\n- entry `main`: `{B2_ENTRY}`;\n- implementation head: `{B2_HEAD}`;\n- PR: #242;\n- merged `main`: `{B2_MERGE}`;\n- `Static contract`: run `{B2_STATIC}`, PASS;\n- final `Linux integration`: run `{B2_LINUX}`, job `{B2_LINUX_JOB}`, `PASS=30 FAIL=0 SKIP=0`;\n- strengthened residual audit: run `{B2_AUDIT}`, job `{B2_AUDIT_JOB}`, PASS;\n- initial executor run `{B2_FAIL_CLOSED}` failed closed on temporary cleanup order and did not publish a product checkpoint;\n- corrected executor run `{B2_EXECUTOR_PASS}`, job `{B2_EXECUTOR_JOB}`, passed;\n- zero B2 Portuguese runtime commands/hooks/forwards remain;\n- no runtime alias layer, normative semantic/proof-state change, proprietary font redistribution or CTAN submission.\n\n## Current runtime/API state",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "`public-api.def` remains transitional R2 debt, but its setup-key forwarding responsibility was removed in B1. Canonical setup/state is now directly owned by `core.def`, `fonts.def`, `modules.def`, `institutional.def`, and `academic-works.def`, with canonical consumers throughout layout/front matter/profile/template/test paths.\n\nThe remaining forwarding surface is bounded to later public commands/environments and helper debt. B2 now owns the academic/front-matter rendering commands and corresponding layout-hook rebinding. B3 owns structural/object environments/APIs/hooks, B4 owns bibliography/back-matter commands and plumbing internalization, and B5 owns the final residual consumer sweep plus removal of `public-api.def`.",
    "`public-api.def` remains transitional R2 debt, but B1 removed setup forwarding and B2 removed academic/front-matter command forwarding. Canonical setup/state and academic/front-matter rendering behavior are now directly owned by their responsibility modules and all live B2 consumers use the canonical API.\n\nThe remaining forwarding surface is bounded to B3 structural/object environments/APIs plus B4 bibliography/back-matter commands. B3 is active and owns structural/object environments, source/note and object-list APIs, optional listing/minted APIs, extension hooks, and project-owned object IDs. B4 owns bibliography/back-matter commands and plumbing internalization. B5 owns the final residual consumer sweep plus removal of `public-api.def`.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "2. **R2-B2 / #237 — ACTIVE.** Academic and front-matter public rendering API; direct canonical commands plus layout-hook rebinding and atomic consumer migration.\n3. **R2-B3 / #238 — PENDING.** Structural/object environments, optional object API, extension hooks and project-owned object IDs.",
    "2. **R2-B2 / #237 — DONE.** Academic/front-matter rendering API directly owned; PR #242 merged with permanent integration green.\n3. **R2-B3 / #238 — ACTIVE.** Structural/object environments, optional object API, extension hooks and project-owned object IDs.",
)
regex_once(
    "docs/HANDOFF-V3.0.0.md",
    r"## Immediate action\n\nExecute R2-B2.*\n$",
    "## Immediate action\n\nExecute R2-B3 through issue #238 from canonical `main`. Migrate structural environments and the definition-list ABNTexto override atomically; move object/source/note/listing/minted/algorithm APIs and extension hooks to direct canonical ownership; replace project-owned `codigo` / `algoritmo` object IDs with English project identifiers while preserving rendered Portuguese labels; migrate all live template/test consumers; and remove only B3 forwarding debt. Run the strengthened residual scan, `make static-check`, and permanent `Linux integration` before B3 closure.\n",
    re.S,
)

# R2 ownership document
replace_once(
    "docs/R2-API-OWNERSHIP.md",
    "This document records the completed R2-A ownership inventory, the closed R2-B1 setup/state migration, and the bounded implementation order for the remaining v3 runtime/API migration.",
    "This document records the completed R2-A ownership inventory, the closed R2-B1 setup/state migration, the closed R2-B2 academic/front-matter migration, and the bounded implementation order for the remaining v3 runtime/API migration.",
)
replace_once(
    "docs/R2-API-OWNERSHIP.md",
    f"R2-B1 merged checkpoint: `{B1_MERGE}`.\nAuthoritative migration contract",
    f"R2-B1 merged checkpoint: `{B1_MERGE}`.\nR2-B2 merged checkpoint: `{B2_MERGE}`.\nAuthoritative migration contract",
)
replace_once(
    "docs/R2-API-OWNERSHIP.md",
    "`abntexto-ufc/public-api.def` remains a transitional forwarding layer loaded last by `abntexto-ufc.cls`, but B1 removed its setup-key forwarding responsibility. Canonical English setup/state is now directly owned by responsibility modules. The remaining forwarding debt is the public rendering/structural/object/bibliography/back-matter surface scheduled for B2–B5.\n\nThe editable reference document and tests have canonical B1 setup/state consumers but still contain Portuguese project rendering commands owned by later lots. Each remaining runtime lot therefore migrates the corresponding `template/` and test consumers atomically with the behavior owner.",
    "`abntexto-ufc/public-api.def` remains a transitional forwarding layer loaded last by `abntexto-ufc.cls`. B1 removed setup-key forwarding and B2 removed academic/front-matter command forwarding. Canonical setup/state and academic/front-matter rendering behavior are directly owned by responsibility modules. The remaining forwarding debt is bounded to B3 structural/object surfaces and B4 bibliography/back-matter surfaces before complete removal in B5.\n\nThe editable reference document and tests use the canonical B1/B2 surfaces but still contain structural/object consumers owned by B3 and bibliography/back-matter consumers owned by B4. Each remaining runtime lot therefore migrates the corresponding `template/` and test consumers atomically with the behavior owner.",
)
for old, new in [
    ("| page geometry, duplex flow, front-matter breaks, structural list environments | `abntexto-ufc/layout.def` | canonical B1 state consumer; B2 layout-hook rebinding; B3 structural environments |", "| page geometry, duplex flow, front-matter breaks, structural list environments | `abntexto-ufc/layout.def` | B1 state DONE; B2 hook rebinding DONE; B3 structural environments ACTIVE |"),
    ("| approval/dedication/acknowledgments/epigraph/errata/summary/abstract/front-matter lists/TOC | `abntexto-ufc/frontmatter.def` | B2 ACTIVE — direct canonical rendering commands and front-matter API |", "| approval/dedication/acknowledgments/epigraph/errata/summary/abstract/front-matter lists/TOC | `abntexto-ufc/frontmatter.def` | B2 DONE — direct canonical rendering commands; B3 definition-list environment ACTIVE |"),
    ("| academic cover/title/catalog card and initial page | `abntexto-ufc/academic-works.def` | B1 key/state DONE; B2 rendering commands ACTIVE |", "| academic cover/title/catalog card and initial page | `abntexto-ufc/academic-works.def` | B1 key/state DONE; B2 rendering commands DONE |"),
    ("| research-project cover/title specialization | `abntexto-ufc/research-projects.def` | canonical B1 state consumer; B2 canonical cover/title specialization ACTIVE |", "| research-project cover/title specialization | `abntexto-ufc/research-projects.def` | canonical B1 state consumer; B2 canonical cover/title specialization DONE |"),
    ("| figures/charts/text tables/code/algorithms/source/note and optional object APIs | `abntexto-ufc/objects.def` | B3 PENDING |", "| figures/charts/text tables/code/algorithms/source/note and optional object APIs | `abntexto-ufc/objects.def` | B3 ACTIVE |"),
    ("| current ABNTexto/LaTeX compatibility | `abntexto-ufc/integrations/abntexto.def` | retain genuine upstream adaptation; update canonical definition-list environment in B3 |", "| current ABNTexto/LaTeX compatibility | `abntexto-ufc/integrations/abntexto.def` | retain genuine upstream adaptation; canonical definition-list environment migration ACTIVE in B3 |"),
    ("| forwarding-only canonical aliases | `abntexto-ufc/public-api.def` | setup forwarding removed in B1; progressively shrink B2–B4; remove completely in B5 |", "| forwarding-only canonical aliases | `abntexto-ufc/public-api.def` | setup forwarding removed in B1; academic/front-matter forwarding removed in B2; absorb B3/B4 then remove completely in B5 |"),
]:
    replace_once("docs/R2-API-OWNERSHIP.md", old, new)
regex_once(
    "docs/R2-API-OWNERSHIP.md",
    r"### R2-B2 — academic and front-matter public rendering API — ACTIVE\n\nOperational issue: #237\. Entry `main`: `[^`]+`\.\n\nMove .*?\n\n### R2-B3 — structural/object environments, optional object API and extension hooks — PENDING",
    f"### R2-B2 — academic and front-matter public rendering API — DONE\n\nOperational issue: #237. Implementation PR: #242. Entry `main`: `{B2_ENTRY}`. Merged `main`: `{B2_MERGE}`.\n\nB2 moved cover/title/approval/catalog-card, dedication/acknowledgments/epigraph/errata, summary/abstract, front-matter lists, list-entry and table-of-contents commands into direct owners; rebound layout hooks; migrated template/test/reference/CTAN/scenario consumers; and removed B2 forwards from `public-api.def`. The first executor run `{B2_FAIL_CLOSED}` failed closed on its own cleanup order. Corrected run `{B2_EXECUTOR_PASS}` passed, then strengthened residual audit `{B2_AUDIT}` caught and closed hook/specialization gaps. Final head `{B2_HEAD}` passed `Static contract` `{B2_STATIC}` and `Linux integration` `{B2_LINUX}` / job `{B2_LINUX_JOB}` with `PASS=30 FAIL=0 SKIP=0`. No normative semantics/proof state changed and no compatibility alias layer was introduced.\n\n### R2-B3 — structural/object environments, optional object API and extension hooks — ACTIVE",
    re.S,
)
replace_once(
    "docs/R2-API-OWNERSHIP.md",
    "Operational issue: #238.\n\nMake `ufclettereditems`",
    f"Operational issue: #238. Entry `main`: `{B2_MERGE}`.\n\nMake `ufclettereditems`",
)
replace_once(
    "docs/R2-API-OWNERSHIP.md",
    "R2-A is complete. The ownership map, machine contracts and control plane agree on the B1–B5 sequence. B1 is complete and B2/#237 is the sole active implementation lot.",
    "R2-A is complete. The ownership map, machine contracts and control plane agree on the B1–B5 sequence. B1 and B2 are complete; B3/#238 is the sole active implementation lot.",
)

# AGENTS
replace_once(
    "AGENTS.md",
    "- V3-R2 is ACTIVE in R2-B2 via issue #237. R2-A ownership inventory and R2-B1 setup/internal-state migration are complete and recorded in `docs/R2-API-OWNERSHIP.md`.\n- R2-B1 merged through PR #236 at `ded5e77733795aa2958606e899d4e27f12f64df4`; final `Linux integration` run `33668283890` passed `PASS=30 FAIL=0 SKIP=0`.\n- R2-B2 owns academic/front-matter public rendering commands and the corresponding layout-hook rebinding. Behavior owner, template consumers and tests move atomically; do not perform a blind global replacement.",
    f"- V3-R2 is ACTIVE in R2-B3 via issue #238. R2-A ownership inventory plus R2-B1 setup/internal-state and R2-B2 academic/front-matter migrations are complete and recorded in `docs/R2-API-OWNERSHIP.md`.\n- R2-B1 merged through PR #236 at `{B1_MERGE}`; final `Linux integration` run `33668283890` passed `PASS=30 FAIL=0 SKIP=0`.\n- R2-B2 merged through PR #242 at `{B2_MERGE}`; final `Linux integration` run `{B2_LINUX}` passed `PASS=30 FAIL=0 SKIP=0`, with strengthened residual audit `{B2_AUDIT}` green.\n- R2-B3 owns structural/object environments, source/note and object-list APIs, optional listing/minted APIs, extension hooks, project-owned `codigo` / `algoritmo` IDs, and their atomic template/test consumers. `ufcdefinitionlist` and the ABNTexto override move together. Do not perform a blind global replacement.",
)

# README
replace_once(
    "README.md",
    "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B2 — academic and front-matter public rendering API, tracked by issue #237.**",
    "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B3 — structural and object API ownership, tracked by issue #238.**",
)
replace_once(
    "README.md",
    "R1 rebuilt and certified the foundation. R2-A completed the runtime/API ownership inventory and R2-B1 completed direct canonical setup/state migration. R2-B2 now moves academic/front-matter rendering commands directly into responsibility-owning modules.",
    "R1 rebuilt and certified the foundation. R2-A completed the runtime/API ownership inventory, R2-B1 completed direct canonical setup/state migration, and R2-B2 completed direct academic/front-matter rendering ownership. R2-B3 now moves structural/object environments, object APIs, hooks and project-owned object identifiers directly into responsibility-owning modules.",
)
replace_once(
    "README.md",
    "R2-A ownership inventory and R2-B1 setup/state migration are complete; V3-R2/R2-B2 is active through issue #237. B1 merged through PR #236 at `ded5e77733795aa2958606e899d4e27f12f64df4` after final `Linux integration` `PASS=30 FAIL=0 SKIP=0`.",
    f"R2-A ownership inventory, R2-B1 setup/state migration and R2-B2 academic/front-matter migration are complete; V3-R2/R2-B3 is active through issue #238. B2 merged through PR #242 at `{B2_MERGE}` after final `Linux integration` run `{B2_LINUX}` closed `PASS=30 FAIL=0 SKIP=0`.",
)

# ARCHITECTURE
replace_once(
    "docs/ARCHITECTURE.md",
    "R2-A classified the forwarding surface and direct owners. R2-B1 is complete: canonical setup/state vocabulary is directly owned and all live setup/state consumers use it. R2-B2 is active and migrates academic/front-matter rendering commands plus layout-hook consumers; later lots migrate structural/object APIs, bibliography/back-matter APIs, and finally remove `public-api.def`.",
    "R2-A classified the forwarding surface and direct owners. R2-B1 is complete: canonical setup/state vocabulary is directly owned and all live setup/state consumers use it. R2-B2 is complete: academic/front-matter rendering commands and layout-hook consumers use direct canonical ownership. R2-B3 is active and migrates structural/object environments, object APIs, extension hooks and project-owned object IDs; later lots migrate bibliography/back-matter APIs and finally remove `public-api.def`.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "V3-R2 is active; `public-api.def` remains transitional R2 debt until canonical public behavior is absorbed directly by responsibility-owning modules.",
    "V3-R2 is active in R2-B3; B1/B2 forwarding debt has been absorbed, and `public-api.def` now contains only remaining B3/B4 transitional forwarding until canonical public behavior is fully owned and the file is removed in B5.",
)

# CTAN guide
replace_once(
    "docs/CTAN-RELEASE.md",
    f"- Development gate: V3-R2 runtime/API migration is active in R2-B2. R2-B1 setup/state migration is complete at `{B1_MERGE}`. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; release publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended release candidate is revalidated proportionally.",
    f"- Development gate: V3-R2 runtime/API migration is active in R2-B3. R2-B2 academic/front-matter migration is complete at `{B2_MERGE}`. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; release publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended release candidate is revalidated proportionally.",
)

# Machine contracts: keep formatting compact by textual surgery, then parse each JSON.
replace_all("release/v3-roadmap.json", '"stage": "R2-B2"', '"stage": "R2-B3"', 2)
replace_all("release/v3-roadmap.json", '"stage_name": "academic and front-matter public rendering API"', '"stage_name": "structural/object environments optional object API and extension hooks"', 2)
regex_once(
    "release/v3-roadmap.json",
    r'  "next_action": ".*?",\n  "r1_status":',
    '  "next_action": "Execute V3-R2 / R2-B3 through issue #238 from canonical main. Move structural/object environments, source/note and object-list APIs, optional listing/minted APIs, extension hooks and project-owned object IDs into direct ownership; migrate consumers atomically; preserve genuine upstream boundaries and rendered Portuguese labels; remove only B3 forwards; validate with strengthened residual scan, make static-check and Linux integration.",\n  "r1_status":',
)
regex_once(
    "release/v3-roadmap.json",
    r'      "R2-B2": \{\n        "status": "ACTIVE",\n        "issue": 237,\n        "name": "academic and front-matter public rendering API",\n        "entry_main_sha": "[^"]+"\n      \},\n      "R2-B3": \{\n        "status": "PENDING",\n        "issue": 238,\n        "name": "structural/object environments optional object API and extension hooks"\n      \},',
    f'      "R2-B2": {{\n        "status": "DONE",\n        "issue": 237,\n        "name": "academic and front-matter public rendering API",\n        "entry_main_sha": "{B2_ENTRY}",\n        "implementation_head_sha": "{B2_HEAD}",\n        "merge_pr": 242,\n        "closure_main_sha": "{B2_MERGE}",\n        "static_contract_run_id": {B2_STATIC},\n        "linux_integration_run_id": {B2_LINUX},\n        "linux_integration_job_id": {B2_LINUX_JOB},\n        "linux_integration_result": "PASS=30 FAIL=0 SKIP=0",\n        "strengthened_residual_audit_run_id": {B2_AUDIT},\n        "strengthened_residual_audit_job_id": {B2_AUDIT_JOB},\n        "fail_closed_executor_run_id": {B2_FAIL_CLOSED},\n        "corrected_executor_run_id": {B2_EXECUTOR_PASS},\n        "corrected_executor_job_id": {B2_EXECUTOR_JOB},\n        "runtime_alias_layer_added": false,\n        "normative_semantics_changed": false,\n        "proof_state_changed": false\n      }},\n      "R2-B3": {{\n        "status": "ACTIVE",\n        "issue": 238,\n        "name": "structural/object environments optional object API and extension hooks",\n        "entry_main_sha": "{B2_MERGE}"\n      }},',
    re.S,
)

replace_once("release/v3-api-migration.json", '"status": "R2_B1_DONE_R2_B2_ACTIVE"', '"status": "R2_B2_DONE_R2_B3_ACTIVE"')
replace_once("release/v3-api-migration.json", '"current_stage": "R2-B2"', '"current_stage": "R2-B3"')
replace_once("release/v3-api-migration.json", '"current_stage_goal": "academic and front-matter public rendering API"', '"current_stage_goal": "structural and object API ownership"')
replace_once("release/v3-api-migration.json", f'"current_main_sha": "{B1_MERGE}"', f'"current_main_sha": "{B2_MERGE}"')
replace_once(
    "release/v3-api-migration.json",
    f'  "r2_b1_closeout": {{"status": "DONE", "issue": 234, "pr": 236, "implementation_head_sha": "99fb58deaa1594ca19fb3a00ca9418623e5b25aa", "merge_main_sha": "{B1_MERGE}", "static_run_id": 33668283912, "linux_integration_run_id": 33668283890, "linux_integration_result": "PASS=30 FAIL=0 SKIP=0", "normative_semantics_changed": false, "proof_state_changed": false}},\n  "active_implementation_lot": {{"stage": "R2-B2", "issue": 237}},',
    f'  "r2_b1_closeout": {{"status": "DONE", "issue": 234, "pr": 236, "implementation_head_sha": "99fb58deaa1594ca19fb3a00ca9418623e5b25aa", "merge_main_sha": "{B1_MERGE}", "static_run_id": 33668283912, "linux_integration_run_id": 33668283890, "linux_integration_result": "PASS=30 FAIL=0 SKIP=0", "normative_semantics_changed": false, "proof_state_changed": false}},\n  "r2_b2_closeout": {{"status": "DONE", "issue": 237, "pr": 242, "entry_main_sha": "{B2_ENTRY}", "implementation_head_sha": "{B2_HEAD}", "merge_main_sha": "{B2_MERGE}", "static_run_id": {B2_STATIC}, "linux_integration_run_id": {B2_LINUX}, "linux_integration_job_id": {B2_LINUX_JOB}, "linux_integration_result": "PASS=30 FAIL=0 SKIP=0", "strengthened_residual_audit_run_id": {B2_AUDIT}, "runtime_alias_layer_added": false, "normative_semantics_changed": false, "proof_state_changed": false}},\n  "active_implementation_lot": {{"stage": "R2-B3", "issue": 238}},',
)

replace_once("release/v3-test-migration.json", '"current_stage": "R2-B2"', '"current_stage": "R2-B3"')
replace_once(
    "release/v3-test-migration.json",
    f'  "r2_b1_closeout": {{"status": "DONE", "merge_main_sha": "{B1_MERGE}", "linux_integration_run_id": 33668283890, "result": "PASS=30 FAIL=0 SKIP=0"}},\n  "r1_reconciliation_status":',
    f'  "r2_b1_closeout": {{"status": "DONE", "merge_main_sha": "{B1_MERGE}", "linux_integration_run_id": 33668283890, "result": "PASS=30 FAIL=0 SKIP=0"}},\n  "r2_b2_closeout": {{"status": "DONE", "merge_main_sha": "{B2_MERGE}", "linux_integration_run_id": {B2_LINUX}, "result": "PASS=30 FAIL=0 SKIP=0", "consumer_migration": "academic/front-matter owners, hooks, template/tests/reference/CTAN/scenario consumers migrated atomically"}},\n  "r1_reconciliation_status":',
)
replace_once("release/v3-test-migration.json", '"active_lot": "R2-B2"', '"active_lot": "R2-B3"')

replace_once("release/v3-path-migration.json", '"current_stage": "R2-B2"', '"current_stage": "R2-B3"')
replace_once(
    "release/v3-path-migration.json",
    f'  "r2_b1_closeout": {{"status": "DONE", "merge_main_sha": "{B1_MERGE}", "next_lot": "R2-B2", "next_issue": 237}},\n  "r1_path_restructuring_status":',
    f'  "r2_b1_closeout": {{"status": "DONE", "merge_main_sha": "{B1_MERGE}", "next_lot": "R2-B2", "next_issue": 237}},\n  "r2_b2_closeout": {{"status": "DONE", "merge_main_sha": "{B2_MERGE}", "next_lot": "R2-B3", "next_issue": 238, "public_api_absorption": "B1 setup plus B2 academic/front-matter forwarding removed; B3/B4 debt remains"}},\n  "r1_path_restructuring_status":',
)

# Validate machine-readable state and canonical agreement.
for file in (
    "release/v3-roadmap.json",
    "release/v3-api-migration.json",
    "release/v3-test-migration.json",
    "release/v3-path-migration.json",
):
    json.loads(path(file).read_text(encoding="utf-8"))

roadmap = json.loads(path("release/v3-roadmap.json").read_text(encoding="utf-8"))
assert roadmap["stage"] == "R2-B3"
assert roadmap["r2"]["stage"] == "R2-B3"
assert roadmap["r2"]["lots"]["R2-B2"]["status"] == "DONE"
assert roadmap["r2"]["lots"]["R2-B2"]["closure_main_sha"] == B2_MERGE
assert roadmap["r2"]["lots"]["R2-B3"]["status"] == "ACTIVE"
assert roadmap["r2"]["lots"]["R2-B3"]["entry_main_sha"] == B2_MERGE

api = json.loads(path("release/v3-api-migration.json").read_text(encoding="utf-8"))
assert api["current_stage"] == "R2-B3"
assert api["r2_b2_closeout"]["merge_main_sha"] == B2_MERGE
assert api["active_implementation_lot"] == {"stage": "R2-B3", "issue": 238}

for file in ("docs/ROADMAP-V3.0.0.md", "docs/HANDOFF-V3.0.0.md", "docs/R2-API-OWNERSHIP.md", "AGENTS.md", "README.md", "docs/ARCHITECTURE.md", "docs/CTAN-RELEASE.md"):
    text = path(file).read_text(encoding="utf-8")
    if "R2-B3" not in text and file != "docs/CTAN-RELEASE.md":
        raise SystemExit(f"{file}: expected R2-B3 status text")

print("R2-B2 closeout documents and machine contracts reconciled; R2-B3 prepared as ACTIVE.")

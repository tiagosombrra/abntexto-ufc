#!/usr/bin/env python3
import json
from pathlib import Path

OLD='3a24ae4f148ea6fd60a6e66eb7cbf42aecd629c8'
NEW='1a126c37653728941ce1ada762376c5fec69cb02'


def replace_once(text, old, new, label):
    count=text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one marker, found {count}: {old[:100]!r}')
    return text.replace(old,new)

p=Path('docs/HANDOFF-V3.0.0.md')
t=p.read_text(encoding='utf-8')
t=replace_once(t,'- Active B4 work item: **B4-C — validator/tool technical-language rebaseline**.','- Active B4 work item: **B4-D — final residual audit and closeout**.','handoff active item')
t=replace_once(t,'- Active B4-C lot: **B4-C2b — diagnostics, report/export labels, and Web UI**.','- Active B4-D focus: **helper ownership, consumer integrity, residual identity/language classification, and temporary-executor absence**.','handoff active subitem')
t=replace_once(t,f'- Latest certified clean implementation checkpoint: **`{OLD}`**.',f'- Latest certified clean implementation checkpoint: **`{NEW}`**.','handoff checkpoint')
t=replace_once(t,'### B4-C — Validator/tool technical-language rebaseline\n\n**ACTIVE.** Entry language-boundary inventory run **`33501038117` PASS** classified the current surfaces before editing.','### B4-C — Validator/tool technical-language rebaseline\n\n**DONE** through PR #197, with final implementation checkpoint **`1a126c37653728941ce1ada762376c5fec69cb02`**. Entry language-boundary inventory run **`33501038117` PASS** classified the current surfaces before editing.','handoff b4c status')
t=replace_once(t,'#### B4-C2 — technical categories, diagnostics, report labels, and Web UI\n\n**ACTIVE.** Split into bounded producer/consumer-safe sublots.','#### B4-C2 — technical categories, diagnostics, report labels, and Web UI\n\n**DONE.** Implemented as bounded producer/consumer-safe sublots.','handoff c2 status')
t=replace_once(t,'##### B4-C2b — diagnostics, report/export labels, and Web UI\n\n**ACTIVE / NEXT.** Translate remaining project-owned human-facing diagnostics, evidence/correction messages, report/export headings and generic Web controls/disclosures. Preserve academic/normative wording, stable machine identifiers, dependency strings, measurement behavior and Portuguese LaTeX runtime/API.','''##### B4-C2b — diagnostics, report/export labels, and Web UI

**DONE** through PR #197, squash-merged at **`1a126c37653728941ce1ada762376c5fec69cb02`**. CLI/Deep and Web/Lite project-owned diagnostics/evidence/corrections, report/export labels, download names, and generic Web controls/disclosures are now English. The Web surface declares `lang=en`; both local-processing disclosure consumers moved with the UI literal.

Validation remained fail-closed: inventory `33506603720` PASS; oversized executor `33506913061` failed before jobs with no functional change; compact run `33507239950` exposed an additional disclosure consumer; migration run **`33507392053` PASS** after reconciliation. Patch review found two remaining PDF/UA technical strings; repair run `33507630613` failed closed on the actual two-occurrence cardinality, and corrected run **`33507724964` PASS** completed the translation and self-removed. Academic/domain labels (`Capa`, `Folha de aprovação`, `Resumo`, `Sumário`, `Referências`), official normative content, stable schema/check/rule IDs, dependency spelling, measurement behavior, proof state, and Portuguese LaTeX runtime/API were preserved.''','handoff c2b')
t=replace_once(t,'### B4-D — Final B4 residual audit/closeout\n\n**PENDING.** Require all helpers classified, no dead helper retained, all live consumers resolving, validator/tool source checks PASS, temporary workflows absent, and canonical docs/machine state synchronized.','### B4-D — Final B4 residual audit/closeout\n\n**ACTIVE / NEXT.** Re-audit helper ownership/current role, live consumers, temporary-executor absence, project-owned identity/language residue, and the bounded validator/tool contract. Any residual must be classified before editing. Closure requires proportional source/contract/syntax/diff checks PASS with no normative semantic, proof-state, tolerance, or runtime/API drift.','handoff b4d')
t=replace_once(t,f'Start B4-C2b from canonical remote `main` using `{OLD}` as the latest certified implementation checkpoint. Translate only remaining project-owned diagnostic/evidence/correction text, report/export labels and generic Web validator UI whose ownership is clear. Preserve academic element labels, official normative text, stable schema/check/rule identifiers, dependency strings, measurement behavior and the Portuguese LaTeX runtime/API. Validate Web/CLI/contract consumers proportionally and remove temporary executors before checkpoint.',f'Start B4-D from canonical remote `main` using `{NEW}` as the latest certified implementation checkpoint. Run a branch-only residual audit over B4-owned tools/validator/metadata surfaces and their consumers. Confirm every helper is current or explicitly B5/B8-assigned, no dead helper or temporary executor remains, and every residual project-owned identity/language occurrence is classified. Repair only proven B4-owned residue, validate proportionally, and then close B4 and synchronize the control plane before activating B5.','handoff next')
p.write_text(t,encoding='utf-8')

p=Path('docs/ROADMAP-V3.0.0.md')
t=p.read_text(encoding='utf-8')
t=replace_once(t,'**V3-R1 ACTIVE — R1-BLOCK-4 active; B4-A done; B4-B done; B4-C active (C1 done, C2a done, C2b active).**','**V3-R1 ACTIVE — R1-BLOCK-4 active; B4-A done; B4-B done; B4-C done; B4-D active.**','roadmap status')
t=replace_once(t,'**B4-A DONE → B4-B DONE → B4-C ACTIVE [C1 DONE → C2a DONE → C2b ACTIVE] → B4-D PENDING**','**B4-A DONE → B4-B DONE → B4-C DONE [C1 DONE → C2a DONE → C2b DONE] → B4-D ACTIVE**','roadmap sequence')
t=replace_once(t,f'- Latest certified implementation checkpoint: **`{OLD}`**.',f'- Latest certified implementation checkpoint: **`{NEW}`**.','roadmap checkpoint')
t=replace_once(t,'### B4-C — Validator/tool technical-language rebaseline\n\n**ACTIVE.** Entry language-boundary inventory run **`33501038117` PASS** classified the current Web/CLI surfaces before modification.','### B4-C — Validator/tool technical-language rebaseline\n\n**DONE** through PR #197 at **`1a126c37653728941ce1ada762376c5fec69cb02`**. Entry language-boundary inventory run **`33501038117` PASS** classified the current Web/CLI surfaces before modification.','roadmap b4c')
t=replace_once(t,'#### B4-C2 — technical categories, diagnostics, report labels and Web UI\n\n**ACTIVE.** Implemented as bounded sublots.','#### B4-C2 — technical categories, diagnostics, report labels and Web UI\n\n**DONE.** Implemented as bounded sublots.','roadmap c2')
t=replace_once(t,'##### B4-C2b — diagnostics, report/export labels and Web UI\n\n**ACTIVE.** Remaining scope is project-owned diagnostic/evidence/correction messages, report/export labels and generic Web controls/disclosures. Academic/normative text, machine identifiers, dependencies, measurement behavior and Portuguese runtime/API remain protected boundaries.','''##### B4-C2b — diagnostics, report/export labels and Web UI

**DONE** via PR #197 at **`1a126c37653728941ce1ada762376c5fec69cb02`**. Project-owned CLI/Web diagnostics, evidence/correction messages, report/export labels, download names and generic validator UI were normalized to English. The Web UI now declares `lang=en`; fail-closed local-processing consumers moved together with the disclosure.

Evidence: `33506603720` inventory PASS; `33506913061` invalid oversized executor/no functional change; `33507239950` exposed a missing disclosure consumer; `33507392053` PASS after reconciliation; patch review exposed two PDF/UA residuals; `33507630613` failed closed on cardinality; **`33507724964` PASS** completed the review repair. Protected academic/normative/runtime boundaries and normative proof state remained unchanged.''','roadmap c2b')
t=replace_once(t,'### B4-D — Residual audit and closeout\n\n**PENDING.** Require all helpers classified, no dead helper retained, all consumers resolving, source/contract/syntax checks passing proportionally, no temporary executor/workflow, and canonical docs/machine state synchronized.','### B4-D — Residual audit and closeout\n\n**ACTIVE.** Reconfirm every B4 helper is current or explicitly later-block-owned, all current consumers resolve, no temporary executor/workflow remains, and all residual project-owned identity/language occurrences are classified. Run proportional source/contract/syntax/diff gates and repair only proven B4-owned residue. Close B4 only with runtime/API and normative semantics unchanged.','roadmap b4d')
t=replace_once(t,f'Start **B4-C2b** from canonical `main` with implementation checkpoint `{OLD}`. Translate only remaining project-owned diagnostics/evidence/correction text, report/export labels and generic Web UI with clear ownership. Preserve academic/normative terms, stable machine contracts, dependency strings, measurement behavior and the Portuguese LaTeX API; validate Web/CLI producer-consumer alignment proportionally and remove temporary executors before checkpoint.',f'Start **B4-D** from canonical `main` with implementation checkpoint `{NEW}`. Run the final branch-only B4 residual audit across helper ownership, consumer resolution, temporary-executor absence and project-owned identity/language residue. Classify before editing, repair only proven B4-owned residue, run proportional source/contract/syntax/diff gates, then close B4 and synchronize the control plane before B5 activation.','roadmap next')
p.write_text(t,encoding='utf-8')

p=Path('release/v3-roadmap.json')
data=json.loads(p.read_text(encoding='utf-8'))
if data['last_certified_clean_checkpoint_sha'] != OLD:
    raise SystemExit('machine checkpoint drift')
block=data['blocks']['R1-BLOCK-4']
if block.get('b4_c2b_status') != 'ACTIVE' or block.get('b4_d_status') != 'PENDING':
    raise SystemExit('machine B4-C2b/B4-D state drift')
data['last_certified_clean_checkpoint_sha']=NEW
block['active_work_item']='B4-D'
block['active_sub_item']='B4-D'
block['b4_c_status']='DONE'
block['b4_c_closure_sha']=NEW
block['b4_c2_status']='DONE'
block['b4_c2_closure_sha']=NEW
block['b4_c2b_status']='DONE'
block['b4_c2b_closure_sha']=NEW
block['b4_c2b_validation_runs']=[
    {'run_id':33506603720,'conclusion':'success','finding':'B4-C2b language-boundary inventory passed'},
    {'run_id':33506913061,'conclusion':'failure','finding':'oversized workflow invalid before jobs; no functional change'},
    {'run_id':33507239950,'conclusion':'failure','finding':'migration applied in workspace; validator-source exposed additional disclosure consumer; no commit'},
    {'run_id':33507392053,'conclusion':'success','finding':'reconciled migration and bounded validator gates passed; temporary helpers removed'},
    {'run_id':33507630613,'conclusion':'failure','finding':'review repair failed closed on actual two-occurrence PDF/UA cardinality; no commit'},
    {'run_id':33507724964,'conclusion':'success','finding':'PDF/UA residual review repair passed and self-removed'},
]
block['b4_c2b_results']={
    'diagnostics_evidence_corrections_normalized':True,
    'report_export_labels_normalized':True,
    'web_ui_language':'en',
    'local_processing_consumers_reconciled':True,
    'academic_domain_labels_preserved':True,
    'stable_machine_identifiers_changed':False,
    'normative_semantics_changed':False,
    'proof_state_changed':False,
    'runtime_api_changed':False,
    'temporary_workflows_removed_before_merge':True,
}
block['b4_d_status']='ACTIVE'
block['b4_d_scope']=[
    'final helper ownership and later-block assignment audit',
    'live consumer resolution and dead-helper audit',
    'temporary executor workflow and helper absence',
    'residual project-owned identity and technical-language classification',
    'proportional validator source contract syntax and diff closure gates',
]
block['planned_lots']['B4-C2']='DONE - C2a and C2b complete'
block['planned_lots']['B4-C2b']='DONE - diagnostics report export labels and Web UI'
block['planned_lots']['B4-D']='ACTIVE - final residual audit and closeout'
data['next_action']=f'Start R1-BLOCK-4 B4-D from canonical remote main using {NEW} as the latest certified implementation checkpoint. Run a branch-only final residual audit across B4-owned tools, validator, metadata and their consumers. Confirm every helper is current or explicitly B5/B8-assigned, all live consumers resolve, no dead helper or temporary executor remains, and all residual project-owned identity/language occurrences are classified before editing. Repair only proven B4-owned residue, validate source/contract/syntax/diff gates proportionally, then close B4 and synchronize the control plane before activating B5.'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

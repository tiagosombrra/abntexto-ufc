# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

**V3-R0 is DONE. V3-R1 is ACTIVE under the clean rebaseline.**

Certified v2 baseline:

`main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`

Clean v3 planning baseline:

`ca2ab12163d16e5eef80c0c8ce9fea543064ab10`

Active implementation branch:

`refactor/v3-r1-rebaseline`

Latest completed implementation checkpoint before this authority synchronization:

`36375e94ce9c6e2048eff2ec9cdcb9f8573b05b7`

Superseded/frozen implementation branches:

- `refactor/n15-b2r-c-full-english-canonicalization`;
- `refactor/v3-full-internationalization`;
- `refactor/v3-foundation-cleanup`;
- `refactor/v3-r1-rebaseline-temp`.

They are evidence only. Do not cherry-pick or copy them wholesale.

## Current operating rule

No known active-tree debt may cross a phase gate.

For V3-R1:

- the active reconstruction branch has no workflows;
- do not restore heavy automatic CI while paths/names are still being rebuilt;
- no auto-mutating workflow, path-rewrite workflow or workflow-generated commit is allowed;
- once static CI is restored, use path filters plus `concurrency` with `cancel-in-progress: true`;
- heavy jobs (Windows Gate T, Overleaf, PDF/A, distribution/CTAN and full multi-engine regression) run only for explicit candidate/final validation or manual dispatch, not every intermediate commit;
- final certification sequence is static gate → affected integration gates → one full exact-SHA candidate suite;
- `main` remains the certified v2 baseline and is not modified just to tune v3-development CI.

## Engineering-language rule

Every project-controlled technical surface is English:

- repository paths and filenames;
- LaTeX public API and project-owned internal identifiers;
- setup keys and internal state values;
- code, scripts, test names, workflow labels and diagnostics;
- comments and technical documentation;
- validator implementation, UI and diagnostics;
- JSON/schema technical keys.

Portuguese is permitted only as academic/rendered content, bibliography data, official UFC/ABNT wording, literal test payload/output when Portuguese content itself is under test, or a technically required upstream identifier at an explicit integration boundary.

`oracle` is not an accepted active engineering term in v3. Use precise `test`, `validation`, `expected` or equivalent naming instead.

## Physical repository identity

Canonical project/package/class identity: `abntexto-ufc`.

The physical GitHub repository is still named `modelo-latex-ufc`. All active metadata and URLs must be prepared for the administrative rename to `abntexto-ufc`, and final v3 certification must occur under the canonical physical repository identity. The connected GitHub action set does not expose repository rename, so that one administrative mutation must be performed explicitly before final certification.

## R1 structural work already completed

Through implementation checkpoint `36375e94...`:

1. GitHub Actions removed from the reconstruction branch;
2. editable document source moved under `template/`;
3. frontmatter, chapter, backmatter and figure paths migrated to English names;
4. `normativa/` moved to `standards/`;
5. current abntexto integration moved under `abntexto-ufc/integrations/`;
6. NBR 6023 adapter moved under `abntexto-ufc/standards/`;
7. test roots established as `tests/checks/`, `tests/documents/`, `tests/fixtures/`, `tests/integration/`, `tests/smoke/`;
8. many test documents/checkers/runners physically moved into semantic roots;
9. `template/main.tex` and class module load paths updated for the new topology.

## R1 remaining work — execute in this order

### Block 1 — terminology and physical naming cleanup

Atomically eliminate active engineering filenames/names containing:

- `oracle`;
- `textual` when it denotes the old document-phase engineering vocabulary;
- `pretextual` / `posttextual`;
- v2 identifiers;
- N-phase identifiers (`n9`, `n10`, `n11`, `n12`, `n13`, `n15`, etc.) outside immutable history.

Update every reference in the same structural block. Do not recreate old paths as shims.

### Block 2 — history isolation

Move v2/N15/B2R evidence from active docs/release namespaces to explicit history namespaces. Preserve immutable evidence; active engineering must not depend on it.

### Block 3 — path consumer reconciliation

Update `tests/run.py`, checkers, integration scripts, standards JSON references and every remaining constructed path to canonical v3 locations.

### Block 4 — build/tool/validator path reconciliation

Update `Makefile`, `tools/` and validator path assumptions. This is path/structure work only; full runtime/API language ownership belongs to R2 and semantic language hardening to R3.

### Block 5 — distribution

Rebuild staging so the repository keeps `template/` while public template/Overleaf bundles flatten it to root. Validate CTAN layout, forbidden assets and deterministic packaging assumptions.

### Block 6 — permanent static gates

Rebuild the repository/path contract directly from v3 contracts and add plan consistency validation. Do not reuse a corrupted v2-derived checker as authority.

### Block 7 — optimized workflows

Restore workflows deliberately under the CI policy above. No heavy workflow may trigger on each reconstruction commit.

### Block 8 — repository identity and exhaustive R1 gate

Prepare canonical URLs/metadata, perform the physical rename to `abntexto-ufc`, audit the entire active tree, synchronize authorities and close R1 only if every structural criterion passes.

## R1 close criteria

- zero obsolete physical paths;
- zero stale active-tree path references;
- zero project-owned Portuguese technical paths;
- zero active `oracle`, old document-phase terminology, v2 or N-phase technical names;
- zero active dependencies on historical evidence;
- all tools/tests/restored workflows use canonical v3 paths;
- template repository build path is coherent;
- flattened public bundle layout is coherent;
- no generated artifacts or temporary migration scaffolding tracked;
- permanent structural and plan-consistency audits pass;
- optimized workflow triggers are installed without CI spam;
- roadmap, machine roadmap and handoff agree.

## Later phases

- **V3-R2:** English-only direct runtime ownership; remove Portuguese project API/aliases, `public-api.def` after ownership absorption, and `ufctex.cls`.
- **V3-R3:** standards/tests/language semantic hardening; validator technical surface English-only.
- **V3-R4:** certification only — Linux/Windows, engines, Gate T, PDF/A-2b, Overleaf, CTAN, deterministic distribution.
- **V3-R5:** foundation freeze and migration/user/maintainer documentation.
- article sequence follows R5.

## Guardrails

- never claim official/homologated UFC status;
- public bundles exclude UFC institutional mark and proprietary Microsoft fonts unless policy changes;
- literal Times New Roman/Arial identity is certified only by Windows Gate T;
- portable fallback is not evidence of literal font identity;
- PDF/A-2b is the project's technical target satisfying UFC's broader PDF/A requirement;
- no tag/release from an uncertified head;
- historical tags/releases remain immutable evidence.

## Immediate next action

Execute **R1 Block 1** on `refactor/v3-r1-rebaseline`: remove obsolete active test/standards engineering terminology (`oracle`, old phase vocabulary and N-phase names) in coherent atomic renames and update all affected references. Keep Actions disabled during this block.

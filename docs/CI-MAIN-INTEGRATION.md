# Linux Integration on main — continuity and mandatory coverage

Incident checkpoint: 2026-10-17; [issue #502](https://github.com/tiagosombrra/abntexto-ufc/issues/502) **CLOSED** on 2026-10-18. This file preserves the dated failure analysis and its acceptance criteria, not the current active-task queue. For current CI/release evidence consult [RELEASE-STATE.md](RELEASE-STATE.md) and [issue #489](https://github.com/tiagosombrra/abntexto-ufc/issues/489). v3.1.0 remains **UNRELEASED**.

## Verified source defect

The previous `.github/workflows/linux-integration.yml` limited `push` events on `main` to four paths (`release/v3-release-candidate.json`, the integration workflow, the integration scope selector and Web/Lite E2E shell script). This omitted changes to `abntexto-ufc.cls`, validators, normative tests and PDF fixtures. The [#500](https://github.com/tiagosombrra/abntexto-ufc/pull/500) merge `8a12e6b27e2795e929fe0dbf5f013e909a6661a8` therefore ran **Static Contract** and **Linux Release** on the merge SHA, but did **not** trigger an exact-main Linux Integration run. The PR head `03d96ddf7b7b042044287fb4447cac8fa93d5a31` independently passed `SCOPE=complete PASS=42 FAIL=0 SKIP=0`; this must not be misreported as an exact-main test.

Main release run `39045970468` did successfully check `SCOPE=complete PASS=38 FAIL=0 SKIP=0` and CTAN pkgcheck 4.1.2 on `8a12e6b27e2795e929fe0dbf5f013e909a6661a8`, with reference/review/distribution outputs.

## Bounded correction

Every `push` to `main` now starts Linux Integration regardless of changed paths, and the existing selector explicitly requires `scope=complete` for a push event. CI configuration changes to this workflow itself also receive the **full 42-check PR suite**, rather than a four-check `smoke` shortcut. All other PR scope classifications (including documentation-only, research project, Web/Lite, article and release-only) retain existing policies.

The mandatory static contract in `tests/checks/repository/linux_integration_suites.py` checks the workflow trigger and selector. Deliberately mutated trigger variants (an added `paths`, `paths-ignore`, and wrong branch) must fail. This is a static source contract for a consciously narrow YAML structure, not a general YAML parser or a substitute for a real GitHub Actions run.

## Original acceptance checklist (2026-10-17)

The `pkgcheck 4.1.2` reference below is the **historical gate version** for the original incident and is not a requirement to downgrade the current runner (subsequent P0.10 runs use 4.1.3).

- PR exact-head Static PASS and full Linux Integration `SCOPE=complete PASS=42 FAIL=0 SKIP=0`, including productive browser Web/Lite E2E and retained real-PDF evidence.
- SHA-guarded merge, no competing PRs or unresolved review threads.
- On **the merge SHA**, Static PASS, Linux Integration **actually triggered** by `push`, `SCOPE=complete PASS=42 FAIL=0 SKIP=0`, Web/Lite E2E PASS, Linux Release `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, CTAN pkgcheck 4.1.2 PASS and all evidence archives present.
- If any main gate is not triggered or fails, never claim certification; correct the proven cause without weakening/silencing checks.

**Resolution and superseded next-step note:** the CI trigger defect in #502 was corrected and closed in October 2026. The formerly proposed subsequent work [#501](https://github.com/tiagosombrra/abntexto-ufc/issues/501) was **also completed** by [PR #523](https://github.com/tiagosombrra/abntexto-ufc/pull/523), with exact-main postmerge evidence recorded in [issue comment #6388179780](https://github.com/tiagosombrra/abntexto-ufc/issues/501#issuecomment-6388179780). It is **not** the current next work item. The active roadmap is #489; do not equate the bounded table regression fix with all IBGE obligations or full technical-norm recertification. Preserve the 29 parent normative rules, seven public profiles, immutable v3.0.5 release and v3.1.0 publication lock.

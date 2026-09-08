# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Steps 1-6 | ACCEPTED |
| Latest fully validated cleanup | `35671aefd932375cad14c9121a833d7daf267817`; Static `34224224990`; Linux `34224225080` PASS |
| Step 7 permanent gate | `make release-reference-reproducibility`, invoked by `make release-check` |
| Step 7 bounded run | `34229431523` on `0040ed413df7bd9126ff1dcb34c23582bfd68403` |
| Step 7 proof predicates | **PASS** — 2 clean builds, exact SHA-256 equality, embedding/validator/Unicode/PDF-A PASS |
| Accepted proof digest | `cf00b4ba784d0e0cd774b080d9cb88cc23b19c4ecc17ace6dc6aa7fc17c5ac7f` |
| Executor result | reporting-only failure after proof; clean rerun required |
| Temporary executor | `.github/workflows/final-cert-step7-repro.yml` — ACTIVE until clean rerun + classification |
| Final phase gate | Step 8 phase-end regression after Step 7 cleanup |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 7 proof classification

The core reproducibility gate in run `34229431523` completed successfully before the workflow wrapper failed. Structured evidence recorded source SHA `0040ed413df7bd9126ff1dcb34c23582bfd68403`, deterministic epoch `1788872450` from Git commit time, two independent clean builds, identical PDF SHA-256 `cf00b4ba784d0e0cd774b080d9cb88cc23b19c4ecc17ace6dc6aa7fc17c5ac7f`, 450652 bytes, and PASS for font embedding, portable UFC PDF validation, Unicode extraction and PDF/A-2b. Artifact `10057223731` uploaded six bounded evidence files.

The overall run failed only in `Publish proof summary`: the shell here-document was syntactically malformed. The proof step and artifact upload both succeeded. This is a temporary-executor reporting defect; it does not invalidate the structured proof, but the executor must rerun clean before Step 7 acceptance.

The summary step is corrected without changing the permanent reproducibility gate or any acceptance predicate.

## Immediate action

| Order | Action | Acceptance boundary |
|---:|---|---|
| 1 | Publish the reporting-only workflow correction with synchronized docs | no proof predicate changes |
| 2 | Require the temporary Step 7 executor to rerun green | core proof + wrapper + artifact upload all green |
| 3 | Remove the temporary workflow and synchronize docs | temporary executor absent |
| 4 | Require cleanup Static/Linux | both green |
| 5 | Close issue #18 / accept Step 7 | proof + cleanup recorded; permanent gate retained |
| 6 | Execute Final Certification **phase-end regression** | one immutable SHA, complete Linux + full release/certification matrix |
| 7 | Activate Release only after Final Certification closes | no earlier publication action |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.

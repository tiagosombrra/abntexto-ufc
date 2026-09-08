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
| Step 4 proof | run `34219229025` PASS on `fae338e...` |
| Step 4 cleanup | checkpoint `35671aefd932375cad14c9121a833d7daf267817`; Static `34224224990`; Linux `34224225080` PASS |
| Temporary executors | none active |
| Current batch | **Step 7 — deterministic release reference PDF / issue #18** |
| Final phase gate | Step 8 phase-end regression after Step 7 acceptance |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 4 accepted closeout

The current-candidate literal-font proof completed on run `34219229025`, and the bounded executor was subsequently removed. The cleanup checkpoint `35671aef...` passed Static and Linux, so Step 4 is accepted. The proof covered Times New Roman and Arial under pdfLaTeX and LuaLaTeX with literal identity, Unicode extraction, embedding and PDF/A-2b all PASS. No raw proprietary fonts were transported.

## Step 7 execution boundary

Issue #18 is now the active blocker. The deterministic release-reference proof must produce at least two independently rebuilt canonical PDFs from clean build states under the same explicit deterministic provenance inputs and require identical SHA-256 values. Existing PDF validity, font/Unicode/embedding and applicable PDF/A checks remain in force.

Reproducibility must be established at build time. Do not make two copies of one output, rewrite PDFs after build merely to obtain equality, or hide nondeterministic metadata by weakening validation.

## Immediate action

1. inspect issue #18 and the current reference/release build path;
2. identify every current nondeterministic input before changing build behavior;
3. implement the smallest permanent deterministic-build gate appropriate to normal release verification;
4. validate it with two independent clean builds and exact SHA-256 equality while preserving existing PDF checks;
5. synchronize documentation/machine evidence and accept Step 7 only after its gate is green;
6. execute Final Certification **phase-end regression** on one immutable SHA;
7. only then activate Release.

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.

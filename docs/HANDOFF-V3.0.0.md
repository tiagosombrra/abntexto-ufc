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
| Step 7 technical parent | `775dfdd6f6fa18475344409ac0bdc491c4435754` |
| Step 7 state | **ACTIVE — permanent gate implemented; bounded proof pending** |
| Permanent release gate | `make release-reference-reproducibility`, invoked by `make release-check` |
| Temporary proof executor | `.github/workflows/final-cert-step7-repro.yml` — ACTIVE; one-day evidence retention; remove after classification |
| Final phase gate | Step 8 phase-end regression after Step 7 acceptance and executor cleanup |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 7 implementation

The permanent gate now builds the canonical `template/main.pdf` twice from two independently extracted clean Git archives of the same source SHA. It derives `SOURCE_DATE_EPOCH` from an explicit environment value when provided, otherwise from the immutable source commit time; it also sets `FORCE_SOURCE_DATE=1` and `TZ=UTC`. The two outputs are compared by exact SHA-256 before acceptance.

When hashes match, the accepted deterministic PDF is revalidated for font embedding, the existing UFC portable PDF contract, Unicode text extraction and PDF/A-2b. The gate writes structured JSON evidence under `artifacts/validation/` during normal release verification. It does not normalize or rewrite the PDF after build.

A temporary branch-triggered workflow is active only to execute the bounded proof before merge. Its artifact retains the two independently generated PDFs/logs for one day so a mismatch can be diagnosed. This temporary executor is not part of the permanent product and must be removed after the proof is classified.

## Immediate action

| Order | Action | Acceptance boundary |
|---:|---|---|
| 1 | Run Static and PR Linux for the synchronized Step 7 checkpoint | both must remain green or failures must be classified |
| 2 | Run the temporary bounded Step 7 proof | two clean builds; exact SHA-256 equality; embedding/validator/Unicode/PDF-A all PASS |
| 3 | Recover and inspect structured evidence/artifact | record source SHA, deterministic epoch, digest and build count |
| 4 | Remove the temporary workflow and synchronize docs | cleanup checkpoint must pass Static/Linux |
| 5 | Close issue #18 only after the accepted cleanup state is recorded | permanent gate remains; temporary executor absent |
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

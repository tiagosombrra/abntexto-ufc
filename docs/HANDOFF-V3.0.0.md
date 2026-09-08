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
| Step 7 clean bounded proof | **PASS** — run `34231038578` on `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` |
| Deterministic proof | epoch `1788873426`; 2 clean builds; SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| PDF acceptance | embedding/portable validator/Unicode/PDF-A all PASS |
| Proof artifact | `10057880627`, 6 files, one-day retention |
| Temporary executor | removed in current cleanup candidate |
| Current batch | **Step 7 — cleanup validation** |
| Final phase gate | Step 8 phase-end regression after Step 7 acceptance |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 7 clean proof

Run `34231038578` is fully green: proof, summary and evidence upload all passed. Structured evidence records source `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522`, deterministic epoch `1788873426` from Git commit time, two independent clean builds, identical PDF SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf`, 450652 bytes, and PASS for font embedding, portable UFC PDF validation, Unicode extraction and PDF/A-2b. Artifact `10057880627` uploaded six bounded evidence files.

The prior run `34229431523` remains classified as a historical reporting-only wrapper failure after a successful proof. The corrected executor run removes that acceptance ambiguity without changing the permanent gate.

## Immediate action

| Order | Action | Acceptance boundary |
|---:|---|---|
| 1 | Remove the temporary Step 7 workflow and synchronize docs | done in current cleanup candidate |
| 2 | Require cleanup Static and Linux | both must be green |
| 3 | Accept Step 7 and close issue #18 | clean proof + executor absent + cleanup green |
| 4 | Create Final Certification **phase-end regression** candidate | one immutable SHA |
| 5 | Run Static + complete Linux + full release/certification matrix | all green on same candidate |
| 6 | Activate Release only after Final Certification closes | no earlier publication action |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.

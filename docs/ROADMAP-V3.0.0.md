# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-6 are accepted. Step 7 core deterministic proof passed; the temporary executor has a reporting-only defect and must rerun clean before cleanup.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7 EXECUTOR CLEAN RERUN** | deterministic reference PDF accepted + temporary executor removed + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State | Evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | canonical branch/base reconciled |
| 2 | Linux release baseline | ACCEPTED | complete release matrix green |
| 3 | Profile and engine certification | ACCEPTED | current candidate matrix accepted |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | ACCEPTED | proof `34219229025`; cleanup `35671aef...` green |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded + cleanup accepted |
| 6 | Distribution/public bundle integrity | ACCEPTED | bundles/checksums/archive integrity accepted |
| 7 | Issue #18 deterministic reference PDF | **ACTIVE — PROOF PASS / WRAPPER RERUN** | run `34229431523` proof PASS; summary wrapper failed after proof; artifact `10057223731` uploaded |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate after Step 7 cleanup |

## Step 7 measured proof

Run `34229431523` on source `0040ed413df7bd9126ff1dcb34c23582bfd68403` produced two independent clean builds with deterministic epoch `1788872450` (`git-commit-time`) and identical PDF SHA-256 `cf00b4ba784d0e0cd774b080d9cb88cc23b19c4ecc17ace6dc6aa7fc17c5ac7f`. The resulting 450652-byte PDF passed font embedding, portable UFC PDF validation, Unicode extraction and PDF/A-2b.

The workflow was marked failure only after that proof, when the optional summary step used a malformed shell here-document. The artifact upload still succeeded. The summary is therefore corrected as an executor-only defect and the bounded workflow must rerun green. No permanent gate or acceptance predicate is weakened.

## Step 7 cleanup requirement

After the clean rerun:

1. record the clean workflow result and structured proof;
2. remove `.github/workflows/final-cert-step7-repro.yml`;
3. synchronize all operational docs/machine state;
4. pass cleanup Static and Linux;
5. accept Step 7 / close issue #18;
6. create the immutable Step 8 candidate.

## Frozen remaining scope

**Step 7 clean rerun → Step 7 executor cleanup/issue #18 closure → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 7-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.

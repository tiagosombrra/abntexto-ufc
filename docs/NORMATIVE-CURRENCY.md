# Normative Currency Policy

Updated: 2026-09-05

`abntexto-ufc` follows the most recent applicable technical edition that is currently in force. An older ABNT edition does not govern an active requirement merely because it is cited by an older UFC guide.

## Decision rule

For technical requirements:

**current applicable ABNT standard → compatible/complementary current UFC requirement → current UFC guide → implementation**.

For institutional requirements:

**current UFC act → current UFC institutional requirement → current UFC guide → applicable technical standard → implementation**.

Current-source conflicts are review items and must not be resolved silently.

## Explicit technical supersessions

The following older editions are contextual only for the active v3 baseline:

- ABNT NBR 14724:2011 → ABNT NBR 14724:2024;
- ABNT NBR 6023:2018 → ABNT NBR 6023:2025;
- ABNT NBR 10520:2002 → ABNT NBR 10520:2023;
- ABNT NBR 12225:2004 → ABNT NBR 12225:2023;
- ABNT NBR 15287:2011 → ABNT NBR 15287:2025.

An older publication year does not imply obsolescence when no superseding edition exists. Currency is determined by normative status, not by year alone.

## UFC guides

UFC normalization guides are institutional sources interpreted under the precedence rule above. When a guide cites a superseded technical edition, compatible institutional guidance may remain useful, but the superseded edition does not become technically governing again.

## Scientific articles

The Scientific Article source-contract reconstruction reconfirmed the corrected UFC scientific-article guide (2022, corrected file dated 2023-04-27) and ABNT NBR 6022:2018 as the current article-presentation basis. The guide's embedded NBR 10520:2002 and NBR 6023:2018 references are superseded for their technical domains by NBR 10520:2023 and NBR 6023:2025.

Scientific Article runtime is now active because the readable Scientific Article phase is active, the retained 18-rule source contract is accepted at `4d018a92697e8f39e3a53b034c451e55996c84fb`, the validated shared foundation is on `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`, and profile/metadata Step 1 was accepted at `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.

Runtime activation is distinct from proof-state promotion. The presence of `abntexto-ufc/articles.def`, profile routing, or a source implementation does not by itself prove article presentation predicates. Article-specific rendered evidence and the later evidence-hardening step remain required before changing article rule proof state.

Static run `34003576066` exposed a stale pre-activation invariant in `tests/checks/normative_currency.py`: it still required `articles.def` to be absent even though the Scientific Article phase had already been formally activated. The fix updates `standards/version-policy.json` and the currency checker to bind runtime presence to the readable machine phase and recorded activation evidence. The source set, technical precedence and article authority contract are unchanged.

## Source updates

When a new technical edition or UFC act is identified:

1. review the source before changing runtime behavior;
2. identify every affected rule and locator;
3. update current machine-readable contracts under `standards/`;
4. remove superseded active authority from the current contract;
5. reconcile implementation, tests, validator behavior, and active documentation;
6. certify the exact candidate head only after the source transition is internally consistent.

Historical source states remain available through Git and release history; they are not duplicated into active repository archive directories.

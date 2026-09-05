# V3 Object Typography Decision

Updated: 2026-09-05
Status: IMPLEMENTED — FINAL BRANCH REGRESSION PENDING

## Decision

The v3 object typography contract must distinguish the upper identification/title from lower auxiliary text.

Accepted project behavior:

- upper illustration/table/object identification/title: 12 pt, single spacing;
- lower source: 10 pt, single spacing;
- lower legend/note/other auxiliary information: 10 pt, single spacing where applicable;
- identification/title/source/legend/note remain constrained to the object width rather than the page width.

## Authority basis

The current UFC normalisation landing page, updated in 2026, continues to publish the UFC academic-work guide as institutional guidance.

Checked institutional source:

- `https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/`
- guide: `https://biblioteca.ufc.br/wp-content/uploads/2022/05/guianormalizacaotrabalhosacademicos-17.05.2022.pdf`
- checked on 2026-09-05.

The guide establishes the relevant distinction:

1. Section 4.1(c) sets 12 pt for the work generally and lists long quotations, footnotes, pagination, cataloguing data, and the **legends and sources of illustrations and tables** as smaller uniform exceptions, recommending 10 pt.
2. Section 4.9(c) defines the illustration **identification above the illustration** as the illustration type, order number, dash and title, single spaced and justified.
3. Section 4.9(d) defines the **source below the illustration**; 4.9(e) allows legend, notes and other information after the source.
4. Section 4.10(b) separately defines the table **identification/title above the table**, while 4.10(c) places sources and notes at the foot of the table.
5. The two recovered librarian-review layers independently mark upper figure/table titles as body-size text.

This reading avoids conflating the guide's lower `legenda` exception with the upper identification/title that the same guide describes separately.

## Defect that was corrected

Before this migration, `abntexto-ufc/objects.def` applied `\abntsmall\singlesp` inside the overridden `\printlegendbox`. Because that box is the upper object identification/title, the runtime forced it to 10 pt.

The old final-PDF contract also certified that defect through:

- `font.size.reduced.illustration-caption`;
- `font.size.reduced.table-caption`.

A green test for those historical rules proved the encoded 10 pt contract, not institutional correctness.

## Implemented contract migration

Implementation checkpoint: `f2f5124c4adcb34069a667f1ef80c76fb17728bd`.

The correction was applied as one semantic migration across source contract, runtime and evidence:

1. upper illustration/table identification/title was removed from the reduced-font exception;
2. semantically correct 12 pt rules were introduced as `illustration.identification.font-size` and `table.identification.font-size`;
3. historical 10 pt rule IDs were retired rather than silently repurposed;
4. `standards/rule-migrations.json` records retired/replacement IDs and values;
5. `objects.def` now uses body-size typography for the upper identification/title while preserving single spacing;
6. lower source/legend/note reduced typography remains 10 pt where applicable;
7. locator ownership is split between exact illustration and table locator sets instead of using one overbroad combined locator;
8. final-PDF scenarios/checkers now expect 12 pt upper title and 10 pt lower source independently;
9. object geometry regression directly distinguishes title size from source/note size;
10. the temporary migration executor and temporary workflow were removed before the generated checkpoint.

## Evidence state

Workflow run `33963033293` successfully:

- generated the migration;
- ran the repository-owned Static contract successfully against the migrated tree;
- restored the permanent Static workflow;
- removed temporary executor surfaces;
- committed and pushed `f2f5124c4adcb34069a667f1ef80c76fb17728bd`.

The immediate PR workflows emitted for the bot-authored generated checkpoint required an external action and therefore produced no executable jobs. They are not acceptance evidence and are not being treated as pass/fail results.

Review item 21 therefore remains `FAIL` only until the normal user-authored branch checkpoint passes Static contract and full Linux integration, including the corrected final-PDF measurements. No semantic implementation work remains open in this object batch unless that regression exposes a real defect.

## Current-edition technical boundary

The repository identifies ABNT NBR 14724:2024 as current technical authority, but exact authoritative clause text for this point is not available in the repository/public evidence corpus. This decision therefore uses the current UFC institutional guidance plus the recovered UFC librarian review evidence and remains reopenable if licensed current-edition ABNT text establishes a contrary rule.

This limitation does not justify retaining the former conflation: the available institutional evidence explicitly separates upper identification/title from lower source/legend/note surfaces.

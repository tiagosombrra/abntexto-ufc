# V3 Object Typography Decision

Updated: 2026-09-05
Status: IMPLEMENTED — CI CONFIRMATION PENDING

## Decision

The v3 object typography contract must distinguish the upper identification/title from lower auxiliary text.

Accepted project behavior:

- upper illustration/table/object identification/title: 12 pt, single spacing;
- lower source: 10 pt, single spacing;
- lower legend/note/other auxiliary information: 10 pt, single spacing where applicable;
- identification/title/source/legend/note remain constrained to the object width rather than the page width.

The current implementation is therefore incorrect where `\abntsmall` is applied to the complete upper `\printlegendbox` identification/title block.

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

## Current implementation defect

`abntexto-ufc/objects.def` currently applies `\abntsmall\singlesp` inside the overridden `\printlegendbox`. Because that box is the upper object identification/title, the runtime forces it to 10 pt.

The final-PDF evidence currently certifies that same defect through rule IDs including:

- `font.size.reduced.illustration-caption`;
- `font.size.reduced.table-caption`.

A green test for those rules proves the encoded 10 pt contract, not that the contract is institutionally correct.

## Contract migration policy

The correction must be atomic across source contract, runtime and evidence.

1. Stop classifying the upper illustration/table identification/title as a reduced-font exception.
2. Introduce semantically correct title-size rules using body-size value 12 pt.
3. Preserve reduced-font rules for source/legend/note surfaces.
4. Preserve provenance for retired/migrated rule IDs; do not silently repurpose an old ID to mean the opposite value.
5. Update locator audits so 4.1(c) no longer falsely groups upper titles under the reduced-font exception.
6. Update final-PDF scenarios/checkers to measure 12 pt upper title and 10 pt lower source independently.
7. Run Static contract and full Linux integration after the migration.
8. Keep item 21 as `FAIL` until the corrected final-PDF measurements are green; only then move it to `PASS`.

## Implementation checkpoint state

The runtime, active normative contract, locator ownership and final-PDF expectations have now been migrated according to this decision. The historical 10 pt title IDs are preserved only through `standards/rule-migrations.json`; they are no longer active rules. Item 21 remains `FAIL` until Static contract and full Linux integration prove the generated candidate, including measured 12 pt upper identification/title and 10 pt lower source evidence.

## Current-edition technical boundary

The repository identifies ABNT NBR 14724:2024 as current technical authority, but exact authoritative clause text for this point is not available in the repository/public evidence corpus. This decision therefore uses the current UFC institutional guidance plus the recovered UFC librarian review evidence and remains reopenable if licensed current-edition ABNT text establishes a contrary rule.

This limitation does not justify retaining the current known conflation: the available institutional evidence explicitly separates upper identification/title from lower source/legend/note surfaces.

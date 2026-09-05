# V3 Object Typography Decision

Updated: 2026-09-05
Status: IMPLEMENTED — TABLE ADAPTER FIX CI PENDING

## Decision

The v3 object typography contract distinguishes the upper identification/title from lower auxiliary text.

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

## Original defect and first migration

Before the first migration, `abntexto-ufc/objects.def` applied `\abntsmall\singlesp` inside the overridden `\printlegendbox`. Because that box is the upper illustration/object identification/title, the runtime forced it to 10 pt.

The old final-PDF contract also certified that defect through:

- `font.size.reduced.illustration-caption`;
- `font.size.reduced.table-caption`.

Implementation checkpoint `f2f5124c4adcb34069a667f1ef80c76fb17728bd` corrected the shared object path and migrated the normative contract:

1. upper illustration/table identification/title was removed from the reduced-font exception;
2. semantically correct 12 pt rules were introduced as `illustration.identification.font-size` and `table.identification.font-size`;
3. historical 10 pt rule IDs were retired rather than silently repurposed;
4. `standards/rule-migrations.json` records retired/replacement IDs and values;
5. `objects.def` uses body-size typography for the upper object identification/title while preserving single spacing;
6. lower source/legend/note reduced typography remains 10 pt where applicable;
7. locator ownership is split between exact illustration and table locator sets;
8. final-PDF scenarios/checkers expect 12 pt upper title and 10 pt lower source independently;
9. object geometry regression directly distinguishes title size from source/note size;
10. temporary migration executor/workflow surfaces were removed before the generated checkpoint.

## Branch regression finding

Branch-level Static contract run `33963240056` passed. Full Linux integration run `33963240297` then provided a useful negative result rather than a false green:

- illustration identification/title: **PASS**, measured 12 pt;
- illustration source: **PASS**, measured 10 pt;
- table source: **PASS**, measured 10 pt;
- table identification/title: **FAIL**, expected 12 pt, measured 10 pt;
- overall Linux summary: `PASS=29 FAIL=1 SKIP=1`.

The failure was isolated to the `tabularray-abnt` compatibility adapter in `abntexto-ufc/modules.def`. That adapter still appended:

```tex
\SetTblrStyle{caption,lasthead,capcont}{font=\abntsmall}
```

This overrode the table theme independently of the corrected `objects.def` path. The upstream `tabularray-abnt` ABNT/quadro themes use body-size typography for `caption,lasthead,capcont` and reduced typography for continuation/footer text, so retaining the project override contradicted both the accepted project decision and the package theme semantics.

## Residual correction

Implementation commit `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c` corrects the remaining adapter surface:

```tex
\SetTblrStyle{caption,lasthead,capcont}{font=\normalsize}
\SetTblrStyle{firsthead-text,lasthead-text,conthead-text,lastfoot}{font=\abntsmall}
```

This preserves the intended split:

- upper table identification/title and continued caption surfaces remain body size;
- lower continuation/source/note auxiliary text remains reduced;
- the final-PDF checker remains unchanged and continues to require 12 pt for the upper table identification and 10 pt for the lower source.

The test was not weakened to recover green CI. The failed acceptance run identified a real second runtime surface and the runtime was corrected instead.

## Evidence state

Review item 21 remains `FAIL` until a normal branch checkpoint containing `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c` passes:

1. Static contract;
2. full Linux integration;
3. illustration final-PDF 12 pt title / 10 pt source evidence;
4. table final-PDF 12 pt title / 10 pt source evidence.

Only then may the review matrix move item 21 to `PASS`.

## Current-edition technical boundary

The repository identifies ABNT NBR 14724:2024 as current technical authority, but exact authoritative clause text for this point is not available in the repository/public evidence corpus. This decision therefore uses the current UFC institutional guidance plus the recovered UFC librarian review evidence and remains reopenable if licensed current-edition ABNT text establishes a contrary rule.

This limitation does not justify retaining either former conflation. The available institutional evidence distinguishes upper identification/title from lower source/legend/note surfaces, and the regression now enforces that distinction independently for illustrations and tables.

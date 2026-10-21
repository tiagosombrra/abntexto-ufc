// Presentation/export boundary only. The canonical report and JSON are unchanged.
// Spreadsheet applications can interpret even quoted CSV fields as formulas.
// Prefix cells beginning with a formula trigger (after leading whitespace or
// controls) with an apostrophe to force a literal text interpretation.
const FORMULA_PREFIX = /^[\s\u0000-\u001f\u007f]*[=+@-]/u;

export function csvCell(value) {
  const source = String(value ?? "");
  const safe = FORMULA_PREFIX.test(source) ? "'" + source : source;
  return '"' + safe.replaceAll('"', '""') + '"';
}

export function csvRows(rows) {
  return rows.map(row => row.map(csvCell).join(",")).join("\r\n");
}

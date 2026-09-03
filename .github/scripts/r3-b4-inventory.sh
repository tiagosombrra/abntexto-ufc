#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' '=== R3-B4 Portuguese engineering diagnostics ==='
git grep -n -I -E 'Auditoria|auditoria|Validando|validando|falhou|Falhou|conclu[ií]d[oa]|Conclu[ií]d[oa]|não foi|Não foi|ausente|incorreto|desconhecido' -- \
  '.github/**' 'tests/checks/**' 'tests/integration/**' 'tests/smoke/**' 'tools/**' 'validator/**' || true

printf '%s\n' '=== R3-B4 retired technical profile identifiers ==='
git grep -n -I -E '\b(tccgraduacao|tccespecializacao|dissertacao|tese|projetoanonimizado|projeto)\b' -- \
  'standards/**' 'tests/checks/**' 'tests/integration/**' 'tests/smoke/**' 'tools/**' 'validator/**' || true

printf '%s\n' '=== R3-B4 migration-contract consumers ==='
for contract in release/v3-api-migration.json release/v3-test-migration.json release/v3-path-migration.json; do
  echo "--- $contract"
  git grep -n -I -F "$contract" -- ':!docs/**' ':!release/v3-roadmap.json' ':!release/v3-r3-inventory.json' ':!AGENTS.md' ':!README.md' || true
done

printf '%s\n' '=== R3-B4 inventory complete ==='

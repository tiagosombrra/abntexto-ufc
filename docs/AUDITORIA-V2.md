# Auditoria da V2

Estado de referência: **v2.1.0**, auditada em 22/08/2026.

Este arquivo registra apenas o estado corrente da auditoria da linha 2.x. O histórico de migração e decisões intermediárias permanece no histórico Git e não integra a árvore documental ativa.

## Fontes de verdade

- `docs/AUDITORIA-FINAL-V2.1.0.md`: auditoria normativa, visual e de validação da candidata corrente;
- `docs/NORMAS.md`: política normativa e matriz requisito → implementação → teste;
- `docs/VIGENCIA-NORMATIVA.md`: vigência e precedência das fontes;
- `normativa/catalog.json` e `normativa/precedence.json`: catálogo operacional e resolução de precedência;
- `tests/run.py`: orquestrador único da validação automatizada.

## Estado estrutural

A implementação corrente usa módulos próprios da V2 sobre `abntexto`. Adaptações necessárias ao upstream e ao escopo testado da NBR 6023:2025 permanecem isoladas em módulos específicos. Componentes, caminhos e APIs retirados da arquitetura anterior não fazem parte da distribuição atual.

O gate `tests/v2-repository-audit.py` percorre os arquivos rastreados e impede a reintrodução de caminhos e padrões retirados, além de verificar versão, módulos, chaves públicas, codificação, artefatos gerados e caminhos locais indevidos.

## Validação

Para PRs, use `python3 tests/run.py --mode pr` ou `make preflight`. Para certificação de release, use o modo `release` e os gates de distribuição correspondentes.

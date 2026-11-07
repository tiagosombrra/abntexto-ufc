# R5 — auditoria externa PDF/A-2b dos 32 PDFs originais R4

**Diagnóstico de integração independente. NÃO publicar ou mesclar automaticamente.**

## Fonte exata e escopo

- 4 artefatos originais de [Actions R4 #42419218910](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/42419218910).
- SHA do corpus `1886bf81bdce8c57e7e28f54e1f2dc9c0749adc7`, PR [#577](https://github.com/tiagosombrra/abntexto-ufc/pull/577).
- 32 PDFs R4 (7 tipos + variante de tese, PT/EN/ES/FR): **1.428 páginas A4**, **324 versos brancos candidatos**, em 16 documentos duplex.
- O workflow valida a origem GitHub, os recibos e hashes SHA256 dos **32 PDFs e seus 32 arquivos TeX** antes de repassar binários intactos ao veraPDF. Confere tipo/perfil, oito documentos por idioma, 357 páginas por idioma, 81 versos por idioma e proibição de homologação humana pelo CI.

## Verificação externa

O workflow usa o contêiner oficial `verapdf/cli:latest` sobre os 32 originais,
com `--flavour 2b --format raw --recurse /data`.
O digest real da imagem é capturado para permitir reprodução exata.
O relatório XML bruto e o resultado interpretado são artefatos Actions
preservados mesmo em falha.

O segundo parser exige **exatamente 32 resultados distintos**, perfil
`PDFA_2_B`, processamento normal de cada arquivo, coerência dos totais
conformes/não conformes, ausência de erros da ferramenta e saída das
violações por documento. **Uma não conformidade bloqueia o job**.

O teste é específico para PDF/A-2b dos PDFs sintéticos R4.
Os **28 exemplos E3** têm gate externo separado na
[PR #576](https://github.com/tiagosombrra/abntexto-ufc/pull/576) e
[run #42420446300](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/42420446300),
todos com o mesmo SHA de fonte acadêmica `1886bf81`.

## Limites do aceite

A conformidade PDF/A-2b **não aprova** conteúdo acadêmico, conformidade
ABNT/UFC, legibilidade, normas de depósito eletrônico, acessibilidade PDF/UA,
fontes de pesquisa ou as 324 folhas de verso em branco. O inventário R5
exige **parecer normativo individual para todas as 324**, incluindo 56
transições pós-textuais.

Mesmo que este gate passe: `human_review=PENDING`,
`publication_authorized=false`, `v3.1.0 UNRELEASED`.

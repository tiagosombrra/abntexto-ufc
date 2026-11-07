# E3/R4 — ensaio de integração de 28 PDFs públicos (diagnóstico)

**Origem imutável do candidato:** exemplos públicos da PR [#574](https://github.com/tiagosombrra/abntexto-ufc/pull/574), commit `8427d3df038ca46348d507e5006051f7dbdfdd1e`.

**Composição experimental da classe:**
- Metadados PDF Info/XMP, bookmarks e segurança de anonimização: PR [#563](https://github.com/tiagosombrra/abntexto-ufc/pull/563), commit `2f1bdf5f1a8dc80eaeb77c09b56eee9cb3a5e427`;
- Correções visuais de sumário/banca/corpo, **com todas as modificações anteriores #563**: PR [#566](https://github.com/tiagosombrra/abntexto-ufc/pull/566), commit `70a6a38ef20d3d64ef4a787c229a5ed8364ccd9d`, blob da classe `9f78a005c35411bcb8e5c4d0110dfb361805cca8`;
- Prefixos de tabelas es/fr após troca do Babel: apenas o trecho delimitado da classe da PR [#565](https://github.com/tiagosombrra/abntexto-ufc/pull/565), commit `b8528c090105d3deb0ec2f36e456b2c759c4342d`.

**Esta é uma composição para teste, não um substituto das PRs de origem.**
Nenhuma correção é aplicada à `main` a partir deste ensaio, que deve
permanecer em draft. As aprovações e CI dos commits individuais **não**
substituem teste sobre o commit composto.

## Critérios de prova

O workflow `.github/workflows/public-mesh-examples.yml` mantém a checagem
rápida de 28 fontes TeX editáveis com SHA256 e controle negativo; na branch
diagnóstica também executa uma matriz **7 perfis × 4 idiomas = 28 PDFs**.

O auditor `tools/examples/run_public_mesh_pdf_matrix.py` executa
`pdflatex`/Biber/duas passagens adicionais, observa **os binários PDF reais**
e registra em recibo individual: hash da fonte, hash do PDF, número de páginas,
metadados Info e XMP, bookmark de introdução, legendas `Tabela`/`Table`/
`Tabla`/`Tableau`, presença do método, discussão original e ausência de
sentinelas sintéticas. Também rejeita páginas sem texto ou somente com folio
no corpus de **leitura digital, single-sided**. Quaisquer conclusões sobre
conformidade normativa de uma folha exigem inspeção humana posterior.

O script inclui controles negativos para perda de título, autor,
XMP, bookmarks, legenda espanhola `Cuadro` e folhas vazias/só com número.
Os PDFs, textos extraídos, XMP, outlines, logs, hashes e evidência de falha
são retidos como artefatos dos quatro jobs.

## Portas não cobertas por um eventual CI verde

1. Revisão **visual e linguística humana** de todas as páginas dos 28 PDFs
   e conferência da separação entre projetos e trabalhos concluídos.
2. Avaliação normativa da UFC e dos respectivos programas para cada gênero,
   confirmação das traduções institucionais por autoridade competente.
3. Verificação independente de PDF/A com `veraPDF` e acessibilidade PDF/UA
   (problema distinto, [#459](https://github.com/tiagosombrra/abntexto-ufc/issues/459)).
4. Regressão no SHA final reconciliado e revisão das PRs #563, #565, #566,
   #568 e #573, sem mesclar um branch diagnóstico por engano.
5. Autorização explícita e separada para eventual publicação.

**Estado obrigatório:** `v3.1.0 UNRELEASED`,
`publication_authorized=false` e `R5 HUMAN_REVIEW_PENDING`.

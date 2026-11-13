# R8.1 — Solicitação de revisão humana dos 28 PDFs da classe corrigida

**Situação: READY_FOR_HUMAN_REVIEW_NOT_ACCEPTED.** Este documento descreve a preparação da revisão da linha `v3.1.0` em desenvolvimento. Não concede aceitação visual, linguística, normativa ou institucional; `publication_authorized=false`. A [PR #592](https://github.com/tiagosombrra/abntexto-ufc/pull/592) continua draft até a conclusão dos gates apropriados.

## Identidade dos PDFs originais

- Classe recompilada: `abntexto-ufc.cls`, Git blob `299293e273dcefb80256eed2e17d2557db6aae52`.
- Fonte completa que gerou os 28 PDFs editoriais: `de99db499cbc5bb78097f415fb91e3bb3ca3128a`.
- Execução: [GitHub Actions #43467471975](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/43467471975). Os quatro jobs de idioma compilaram com sucesso.
- Documentos: 7 perfis × 4 idiomas (PT/EN/ES/FR) = **28 arquivos e 972 páginas**.
- Distribuição após corrigir a issue [#593](https://github.com/tiagosombrra/abntexto-ufc/issues/593): **PT 246, EN 240, ES 240, FR 246 páginas**. No corpus anterior havia 12 páginas EN/ES com somente a última linha da tabela longa. A classe e as 85 linhas do teste sintético R4 foram preservadas; os documentos editoriais empregam 80 linhas para evitar a página residual.
- Recebimentos originais: PT artifact `14059297908`, EN `14057939644`, ES `14059198079`, FR `14058644629`. O auditor verifica identidade, SHA-256 dos ZIPs, SHA-256 de cada PDF e fonte TeX, hashes dos recibos e contagens físicas de páginas, sem regravar os originais.
- A verificação independente do **veraPDF-2b de desenvolvimento** sobre esses PDFs teve 28 conformes e 0 não conformes, sem constituir aprovação visual ou institucional. O antigo verificador R8.1 permanece deliberadamente incompatível com o blob da classe atual.

**Atenção ao avanço da PR #592 após R8.1 #594:** a branch experimental já incorpora a `main` certificada `83dbaa6d...`. O corpus R4 mantém 85 linhas e o novo corpus R5 editorial mantém 80 linhas; ambos devem ter verificadores source-bound separados. Este pacote de 972 páginas é **evidência arquivada do commit `de99db...`**, não comprova a revisão visual nem normativa dos PDFs recompilados pelo HEAD posterior. Os PDFs gerados no novo HEAD exigem novos hashes, revisão e aceite próprios.

## Gerar o pacote de revisão, sem aceite automático

O workflow [R8.1 corrected-runtime human PDF review request](../.github/workflows/r81-v310-human-review-request.yml) produz um artefato `r81-v310-pending-review-request-<run_id>` contendo:

- `request.json`: identidade dos 28 documentos, fonte e SHA-256 original de cada PDF e arquivo TeX, número de páginas, ZIP de origem, oito dimensões de revisão **PENDING** por documento e 972 decisões de páginas inicializadas como **PENDING**;
- `REVIEW-REQUEST.md`: relação por perfil/idioma, URLs para os quatro artefatos originais e orientações de inspeção.

O script `tools/review/prepare_v310_r81_human_review.py` é executado por CI com token somente de leitura e os comandos `qpdf --check` e `pdfinfo`. Uma alteração posterior na classe altera o blob e bloqueia a reutilização da evidência; os pacotes gerados para outra fonte devem ser regenerados. Os ZIPs originais continuam na execução original, e não são republicados como artefatos de distribuição.

Os dados de revisão produzidos são **solicitações em branco**. Qualquer decisão humana deve ser mantida num registro separado e rastreado, com identificação da pessoa revisora, data, PDF, SHA-256, página, justificativa normativa e evidência. A geração de arquivos não pode produzir automaticamente `ACCEPT`.

## Critérios mínimos para a decisão de cada documento

1. **Norma UFC/ABNT:** citar edição e seção aplicável, distinguindo NBR 14724:2024 (com a correção vigente), NBR 15287:2025 para projetos, NBR 6023:2025 para referências e o guia UFC conforme aplicabilidade. Questões contraditórias exigem parecer humano, não suposição por código.
2. **Geometria e apresentação:** margens, títulos, folios em páginas pares/ímpares, recuos de citações, entrelinhas, sumário e pontos de condução, números e capitulares.
3. **Perfil acadêmico:** elementos obrigatórios, opcionais e proibidos para TCC, especialização, mestrado, doutorado, projeto, projeto anônimo e artigo, incluindo a banca e a área de concentração.
4. **Traduções:** português, inglês, espanhol e francês, com revisão de termos acadêmicos, natureza do trabalho e consistência dos textos institucionais.
5. **Elementos pré/pós-textuais:** resumos, listas, glossário, índice, bibliografia, apêndices e anexos, ordem, existência e localização.
6. **Objetos e listagens:** figuras, gráficos, quadros, tabelas, notas, fontes e trechos importados; em `\ufcobject`, verificar a importação com a nova implementação de `\ufcInputListing`. Listagens extensas não devem ser pressupostas divisíveis quando dentro de caixas herdadas.
7. **Frente e verso:** toda página vazia exige fundamentação individual por transição de elemento e modo de impressão; não transformar paridade observada em obrigação normativa.
8. **Anonimização:** o PDF de projeto anonimizado deve ser inspecionado para informações identificadoras, inclusive metadados, conteúdo e possíveis indícios indiretos. O código-fonte TeX de teste pode intencionalmente conter identidades sintéticas e **não é um pacote de submissão cega**.

## PDF/A-2b independente dos mesmos 28 arquivos

A execução [#43470720979](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/43470720979) validou os **28 PDFs originais do pacote de revisão humana**, não os arquivos diferentes recompilados num commit posterior. O workflow específico é [R8.1 archived reviewed-PDF independent PDF/A-2b validation](../.github/workflows/r81-v310-archived-pdfa.yml).

- Fonte original dos PDFs: `de99db499cbc5bb78097f415fb91e3bb3ca3128a`; execução de geração: `43467471975`.
- Resultado do veraPDF oficial: `PASS_ARCHIVED_DEVELOPMENT_EXTERNAL_PDF_A_2B`, **28/28 conformes**, zero não conformidades, 972 páginas.
- Artefato original do laudo: GitHub artifact `14060196996`, ZIP SHA-256 `91fe34f6ea0effcaf33ca74c074124849e7ee1ad53bc31d8e0148e742a8ed476`. Contém o XML bruto do veraPDF, relatório JSON, manifesto de entrada e digest da imagem usada.
- Auditoria independente adicional: os **28 hashes PDF do manifesto do veraPDF** foram confrontados, um a um, com os **28 hashes dos documentos no pedido R8.1**, e todos coincidiram. Isso elimina a ambiguidade gerada quando dois commits compilam PDFs de conteúdo equivalente, mas bytes diferentes.
- A classe continua vinculada ao Git blob `299293e273dcefb80256eed2e17d2557db6aae52`. Os três scripts geradores dos PDFs originais são verificados por seus Git blobs **congelados no commit de origem**. Alterações posteriores dos geradores na branch não modificam os 28 PDFs arquivados e não autorizam transferir seu aceite para novos documentos.

Esse laudo comprova apenas PDF/A-2b nos arquivos originais; **não** atesta PDF/UA, acessibilidade, qualidade dos conteúdos, diagramação UFC/ABNT, traduções ou assinatura visual. Os 972 registros de página e os 28 documentos continuam **PENDING** para decisão humana. A validação R8.1 histórica, feita para a classe antiga, não foi modificada nem herdada.

## Portas de decisão

Revisão humana por página: `PENDING`; revisão visual final: `PENDING`; revisão normativa e linguística: `PENDING`; autorização institucional: `PENDING`. Somente uma pessoa autorizada pode registrar um `ACCEPT` explícito, sempre vinculando o SHA da fonte e os arquivos realmente examinados.

**Ainda não fazer:** merge protegido da PR #592, alteração do registro histórico da classe antiga, tag v3.1.0, GitHub Release ou envio CTAN. Para release, os gates de integração, fonte final e aceite humano precisam ser novamente certificados no commit aprovado.

Veja também [R5 — auditoria de artefatos](R5-ARTIFACT-REVIEW.md) e [Revisão de sete perfis](SEVEN-PROFILE-REVIEW.md).

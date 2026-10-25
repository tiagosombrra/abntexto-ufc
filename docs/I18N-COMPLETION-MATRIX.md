# Internacionalização integral v3.1.0 — matriz de aceitação P0

**Decisão:** foco exclusivo em textos controlados pela classe, na integração dos pacotes suportados e em documentos completos nos idiomas `pt`, `en`, `es`, `fr`. **Status: PENDING — não afirmar 100% antes de cumprir todas as linhas e testar a fonte final.**

**Compatibilidade legacy:** os comandos históricos de resumo e palavras-chave permanecem compatíveis com documentos anteriores; nos resumos opt-in, seus rótulos acompanham o idioma efetivo do resumo. Uma tradução de rótulo não autoriza reescrever conteúdo fornecido pelo autor. A API LaTeX possui nomes canônicos em inglês e **não muda seus identificadores** conforme o idioma. Nunca traduzir prosa do autor, títulos/nomes próprios, nomes oficiais institucionais ou registros bibliográficos fornecidos pelo usuário.

## Matriz de aceitação, não checklist de mera existência

| Domínio / origem | O que deve localizar ao selecionar document-language | Evidência existente | Saída obrigatória |
|---|---|---|---|
| API de configuração `\ufcsetup` | Rótulos, datas e frases automáticas dos 7 tipos; preservar os valores fornecidos | 34 chaves × 4 idiomas, 9 títulos × 4 | Inventário fail-closed de cada rota de uso real, incluindo opções femininas/masculinas e exceções legítimas |
| Capa / título / aprovação / artigo | Natureza, grau, cargos, banca, datas, rótulos autorais | PDFs de resumo e matriz de natureza | Prova de capa/folha/aprovação conforme aplicabilidade nos 7 perfis × 4 idiomas |
| Resumos e palavras-chave | RESUMO / ABSTRACT / RESUMEN / RÉSUMÉ e rótulo próprio do **idioma de cada resumo**, não necessariamente o idioma principal | 8 PDFs de resumos, variantes e negativos; 9 PDFs do contexto de comandos históricos em desenvolvimento | Principal + PT ou EN complementar, sem títulos duplicados, negativos e compatibilidade legada PT/EN |
| Listas e sumário | Ilustrações, figuras, gráficos, quadros, tabelas, códigos, algoritmos, abreviaturas, símbolos e sumário | 28 PDFs de títulos; testes de listas | Entradas, contadores, página e idioma em documentos completos |
| Objetos e tabelas | Legendas simples/aninhadas, fonte, nota, figuras, gráficos, quadros e tabelas IBGE | 5 PDFs herdados (PT antigo + 4 idiomas) | Exercitar todas as variantes sem vazamento PT, incluindo Babel espanhol `~` |
| Referências e citações | Título da lista, termos da formatação, drivers jurídicos, estilos narrativos/parentéticos e locators | Biber: 5 PDFs de jurisprudência, controle sem data | Corpus multi-tipo com `biblatex-abnt` e Biber nos 4 idiomas; datas, apud e citações reais |
| Pós-textuais / módulos | Apêndices, anexos, glossário, índice, códigos e algoritmos conforme pacotes opt-in | Testes de módulos por domínio | Cobertura em PDFs por variante suportada, sem prometer biblioteca que não esteja instalada |
| Linguagem ativa / PDF | Babel, hifenização quando suportada, `/Root/Lang` coerente com `\DocumentMetadata` declarado pelo autor | 28 PDFs reais com `qpdf` e negativos mismatch/missing | Mesmo recibo PDF + SHA da fonte e rótulos em `pt-BR`, `en-US`, `es-ES`, `fr-FR` |
| Site / validador | Interface PT/EN/ES/FR, seletor, feedback, exportação, navegação acessível | Chromium E2E offline, catálogos separados | Auditar todos os 65 textos de validador e 32 do site, negativos de falha segura, não reescrever IDs normativos |
| Continuidade / publicação | Legado PT não pode sofrer regressão | Baselines antigas, gates 42/42 e 38/38/pkgcheck | Revisão Codex exata, pós-merge, sete perfis × idiomas, revisão visual source-bound |

## Auditoria completa das tags e comandos públicos

O mapa `standards/api/i18n-coverage-inventory.json` classifica nominalmente **70 chaves de configuração**, **43 comandos canônicos**, **seis ambientes** e **seis identificadores herdados**, com fronteiras entre texto produzido pela classe, pacotes externos, parâmetros do autor e os comandos PT/EN legados. A verificação `tests/integration/frontmatter/i18n-api-inventory.py` compara integralmente esse mapa com `standards/api/public-api.json` e reprova macros/chaves sem classificação, inclusive em testes negativos. **Classificado não significa testado em PDF:** a certificação dinâmica continuará PENDING até todos os casos pertinentes terem prova produtiva.

## Primeira bateria de documentos integrados — implementação em PR de testes

O gerador `tests/integration/frontmatter/generate-integrated-locale.py` e o executor `tests/integration/frontmatter/run-integrated-locale.py` criam, compilam e verificam **7 PDFs por idioma, 28 no conjunto**. A matriz roda em quatro jobs paralelos no workflow `.github/workflows/integrated-manuscript-locale-matrix.yml`, usando TeX Live 2026, Biber, qpdf e pdftotext. Cada documento integra mais de um domínio: frente aplicável, idioma Babel, rótulos, elementos gráficos e tabulares, duas formas de citação, referências Biber de cinco tipos, texto pós-textual quando aplicável e metadados reais `/Root/Lang`; doutorado exercita adicionalmente glossário e índice.

**Status inicial da bateria: NOT YET CERTIFIED**. A existência dos scripts não implica compilação bem-sucedida: exigir quatro jobs PASS no SHA exato, 28 PDFs reais, 28 recibos fonte+PDF com hashes, catálogo PDF verificado, sete perfis e zero casos ignorados. Os documentos gerados usam conteúdo sintético e dados institucionais apenas como nomes próprios. A bateria inicial não prova ainda todas as opções avançadas (minted, longabnttblr, semântica de traduções institucionais) nem a tradução de prosa autoral. Esses casos permanecem em P0 e exigem fixtures adicionais, nunca uma declaração implícita de 100%.

## Prova integrada de 7 × 4 = 28 manuscritos

Gerar **28 PDFs integrados**, um para cada tipo (`undergraduate-capstone`, `specialization-capstone`, `masters-thesis`, `doctoral-thesis`, `research-project`, `anonymized-research-project`, `scientific-article`) e idioma. Cada um deve combinar, **somente se aplicável**: capa, folha, aprovação, resumos, listas, sumário, seções e corpo, citações Biber e referências, objeto simples e composto, títulos de apêndice/anexo, glossário/índice. Ensaiar também variantes de texto jurídico, tabelas com nota/fonte, `\keywords` e `\ufcSummaryKeywords` dentro e fora de resumos opt-in, e idioma do PDF. O artigo e os projetos não devem ganhar elementos obrigatórios de tese artificialmente.

Cada recibo exige nome da fonte/PDF, SHA-256 dos dois arquivos, SHA do commit, perfil, idioma, Babel, PDF Catalog /Lang, tokens que devem aparecer, tokens proibidos, contagem de páginas e resultado de Biber/compilação. **Não basta** reutilizar as duas matrizes de 28 PDFs existentes, pois são *smokes* de títulos e natureza. Empregar fixtures sintéticas sem dados pessoais; o arquivo .tex de projeto anonimizado permanece `INTERNAL_AUDIT_ONLY`.

## Como rodar sem desperdiçar regressões

1. **Por commit em PR draft:** Static, comparação de catálogos e testes pequenos direcionados ao módulo alterado. Executar Biber ou PDF somente onde há alteração funcional.
2. **Após reparos e pronto para review:** workflow paralelo com a matriz 28 integrada e artifacts, mais integração Linux `SCOPE=complete PASS=42 FAIL=0 SKIP=0` se alterado o runtime da classe, E2E e plataformas aplicáveis; exigir Codex COMPLETED CLEAN no HEAD exato e zero threads.
3. **Pós-merge:** Static, Linux Integration completa e Linux Release `38/38` com CTAN pkgcheck no SHA da main; documentar hashes e defeitos sem relaxar assertivas.
4. **Aceite final:** revisão visual e linguística com os PDFs exatos, e parecer separado sobre nomenclatura oficial UFC. Não declarar PDF/UA ou conformidade normativa integral só por traduzir rótulos.

A versão **v3.0.5 é imutável**. A **v3.1.0 permanece UNRELEASED**, sem autorização para tag, release ou submissão CTAN. A gestão ocorre somente no GitHub.

## Etapa P0.3 — ambientes opcionais em PT/EN/ES/FR

A execução opt-in de `tests/integration/objects/optional-locale-evidence.py`, por meio do workflow `.github/workflows/i18n-optional-modules-matrix.yml`, exercita **dois PDFs reais por idioma**, combinando `listings`, `ufclisting`, `algpseudocodex`, `ufcalgorithm`, lista de códigos/algoritmos, `tabularray-abnt`, `longabnttblr` multipágina com título, fonte e nota, e, separadamente, `minted` / `ufcInputMinted`. Quatro jobs paralelos devem produzir oito PDFs e seus manifests com SHA-256 e `/Root/Lang`, verificando rótulos da classe e Babel.

**Status: PENDING — implementação e testes preparados, sem certificação no SHA final.** Chaves `remark{...}` das tabelas são texto fornecido pelo autor, portanto exigem versão apropriada ao idioma (a classe não traduz essas strings). O teste deve reprovar ausência de `latexminted`, e não registrar SKIP como sucesso. Também devem ser mantidas as regressões específicas já existentes de tabela IBGE, numeração de algoritmos e fontes, que não são substituídas por essa matriz. As traduções institucionais e a revisão visual continuam dependentes de aceite humano.

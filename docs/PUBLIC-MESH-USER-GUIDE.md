# Guia de exemplos acadêmicos multilíngues — ABNTEXTO-UFC

**Estado:** documentação de desenvolvimento da versão 3.1.0. Não implica
homologação pela UFC, compilação dos 28 PDFs, certificação PDF/A ou
autorização de publicação. Este guia complementa
[USER-GUIDE.md](USER-GUIDE.md) e
[COMMAND-REFERENCE.md](COMMAND-REFERENCE.md).

## Fontes oficiais consultadas (07/11/2026)

| Documento / serviço | Uso responsável |
|---|---|
| [Templates da Biblioteca UFC](https://biblioteca.ufc.br/pt/servicos-e-produtos/templates/) | Estrutura institucional de trabalhos, artigos e projetos. O modelo Overleaf oficial está indicado como "Em atualização"; não assumir que esta classe é oficial |
| [Normalização de trabalhos acadêmicos](https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/) | Guias UFC, referências à ABNT, orientação do bibliotecário e modelos de apresentação |
| [Recebimento de TCC, dissertações e teses](https://biblioteca.ufc.br/pt/servicos-e-produtos/recebimento-e-divulgacao-de-dissertacoes-teses-e-tccs/) | Depósito eletrônico e atos institucionais aplicáveis |
| [Ficha catalográfica — FAQ UFC](https://biblioteca.ufc.br/pt/perguntas-frequentes/ficha-catalografica-2/) | A Instrução Normativa Conjunta nº 2/2026 tornou facultativa a ficha visual de TCC, dissertação e tese; ausência não impede depósito |
| [Normas para recebimento de TCC](https://biblioteca.ufc.br/pt/normas-sibi/normas-para-o-recebimento-de-tcc/) | Exigência institucional de arquivo único em PDF/A e folha de aprovação sem assinaturas no documento divulgado |
| [Afiliação institucional em inglês](https://labomar.ufc.br/pt/saiba-como-citar-corretamente-a-ufc-em-ingles/) | A denominação padronizada para afiliação em publicações científicas é "Federal University of Ceara", **sem acento**, segundo Resolução nº 12/CEPE/2018 |

**Hierarquia normativa:** conferir sempre a norma ABNT atual, o guia vigente,
a política de depósito do programa e o edital. O PDF do guia UFC de 2022
contém referências a edições antigas de normas; não tratá-lo como prova
suficiente de que todos os requisitos técnicos atuais continuam iguais.
Traduções espanholas e francesas da instituição são descrições didáticas,
não denominações jurídicas automaticamente aprovadas.

## 1. Instalação e estrutura

Usar o código-fonte da branch de desenvolvimento apenas para avaliar a
v3.1.0. Para um trabalho real, preferir a
[Release publicada](https://github.com/tiagosombrra/abntexto-ufc/releases)
ou versão explicitamente aprovada pelo curso.

Dependências principais: TeX Live 2026, pdfLaTeX, Biber, classe `abntexto`,
`biblatex`, `graphicx` e os pacotes usados por `abntexto-ufc.cls`.
Executar, a partir da raiz do repositório:

```bash
python3 tools/examples/generate_public_mesh_documents.py
python3 tools/examples/generate_public_mesh_documents.py --check
python3 tests/checks/examples/public_mesh_documents.py
```

O gerador usa `examples/canonical-mesh-study/study.json` e produz:
`artifacts/canonical-mesh-study/*.pdf` (figuras vetoriais originais),
`artifacts/canonical-mesh-study/body-{pt,en,es,fr}.tex` (método matemático)
e `artifacts/public-mesh-documents/{idioma}/{perfil}.tex` (28 fontes
editáveis). O arquivo `manifest.json` registra os hashes das fontes.

Os arquivos gerados dependem da estrutura do repositório e **não são
ZIPs Overleaf autocontidos**. Copiar o arquivo TeX isoladamente não garante
que a figura, a bibliografia ou a classe sejam encontrados.

## 2. Sete perfis acadêmicos

| `type` | Documento | Observação editorial |
|---|---|---|
| `undergraduate-capstone` | TCC de graduação | Descrever o sistema e resultados demonstrados |
| `specialization-capstone` | Monografia/TCC de especialização | Relacionar escolha técnica e limitações |
| `masters-thesis` | Dissertação de mestrado | Situar hipóteses e critérios de comparação |
| `doctoral-thesis` | Tese de doutorado | Exige contribuição científica própria, não demonstrada pelo exemplo |
| `research-project` | Projeto de pesquisa | Distinguir cálculo preliminar de resultados futuros |
| `anonymized-research-project` | Projeto de avaliação cega | Eliminar identificação em todas as superfícies |
| `scientific-article` | Artigo científico | Seguir adicionalmente as regras do periódico |

O mesmo estudo computável fornece a conectividade de três configurações:
quadriláteros uniformes (81 vértices, 144 arestas, 64 células),
quadriláteros anisotrópicos (85, 148, 64) e triângulos estruturados
(81, 208, 128). Esses valores obedecem a `V - E + F = 1` em cada caso.
**Não** significam resultado de APMesh, validação de simulação, ganho de
desempenho ou pesquisa doutoral inédita.

## 3. Metadados e idiomas

A API pública mantém chaves em inglês. Exemplo resumido:

```tex
\DocumentMetadata{lang=en-US,pdfstandard=A-2b,pdfversion=1.7}
\documentclass{abntexto-ufc}
\ufcsetup{
  type=undergraduate-capstone,
  document-language=en,
  print-mode=single-sided,
  institution={Universidade Federal do Ceará},
  institution-display={Federal University of Ceara},
  author={Nome do autor},
  title={Título real do trabalho},
  location={Fortaleza},
  year={2026}
}
```

Configurações de idioma:

| Manuscrito | `document-language` | Metadado PDF |
|---|---|---|
| Português | `pt` | `pt-BR` |
| Inglês | `en` | `en-US` |
| Espanhol | `es` | `es-ES` |
| Francês | `fr` | `fr-FR` |

`document-language` seleciona textos produzidos pela classe e Babel;
não traduz o conteúdo do autor. `labels-language` pode traduzir apenas
títulos pré-textuais de maneira independente; os textos oficiais de cursos,
nomes próprios e afiliações devem ser conferidos e, quando necessário,
informados explicitamente pelo autor.

O PDF declara o idioma no `\DocumentMetadata`, mas isso não valida que
toda a redação e a acessibilidade estejam corretas. Campos de orientação,
banca e titulação do corpus são apenas ilustrativos e devem ser substituídos.

## 4. Compilação e bibliografia

Exemplo de compilação do TCC português, com Biber, sempre na raiz:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=exemplo-tcc-pt artifacts/public-mesh-documents/pt/undergraduate-capstone.tex
biber exemplo-tcc-pt
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=exemplo-tcc-pt artifacts/public-mesh-documents/pt/undergraduate-capstone.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=exemplo-tcc-pt artifacts/public-mesh-documents/pt/undergraduate-capstone.tex
```

A bibliografia do estudo contém duas publicações reais usadas **somente
como fundamentação**, não como algoritmos efetivamente executados. No
preâmbulo, use:

```tex
\ufcAddBibliographyResource{examples/canonical-mesh-study/references.bib}
```

O documento cita as fontes por meio de `\autocite` no estudo científico
gerado e encerra com `\ufcPrintReferences`. Caso apareçam citações
indefinidas, examine as saídas do Biber, o caminho da base e o arquivo
`.bcf`, depois repita as passagens LaTeX.

## 5. Equações, figuras, tabelas e módulos opcionais

Os 28 documentos gerados exercitam equações, uma figura vetorial original,
uma tabela de resultados matematicamente calculados, citações, referências
e listas de figuras/tabelas onde pertinentes. Para código e algoritmos,
os módulos são opcionais: ative-os em `\ufcsetup` e consulte os comandos
documentados na referência do projeto.

```tex
\ufcsetup{code=listings,algorithms=algpseudocodex}
\legend{code}{Exemplo de implementação}
\ufcSource{Elaboração própria}
\begin{ufclisting}[here]
int countCells(int nx, int ny) {
    return nx * ny;
}
\end{ufclisting}
```

Para código externo, usar
`\ufcInputListing[language=C++]{caminho/arquivo.cpp}`. Para algoritmo,
verificar a sintaxe de `ufcalgorithm` e as dependências do backend
`algpseudocodex` na referência de comandos antes de habilitar.

Tabelas longas `longabnttblr`, tabelas nativas `longtable`,
listas de códigos/algoritmos, glossário e índice são cobertos
separadamente pelo corpus R4 de regressão; **não** declarar que já
aparecem em todos os 28 exemplos públicos.

## 6. Projeto anonimizado

Em avaliações cegas, não basta omitir o nome da capa. Verificar a
propriedade PDF Info `Author`, XMP, bookmarks, texto selecionável,
links, anexos, fontes embutidas, caminhos locais e os próprios arquivos
TeX distribuídos. O exemplo anonimizado é produzido com autor vazio,
sem capa e sem identificação pessoal de orientação.

**Anonimização não é garantida pela seleção do perfil**: a avaliação
humana deve conferir o PDF final e a política de submissão. A ausência
de nomes no PDF Info não prova que não existam metadados ocultos ou
identificadores em outros pontos.

## 7. Impressão, depósito e acessibilidade

Os exemplos públicos usam `print-mode=single-sided` para reduzir folhas
de separação inúteis em leituras digitais. Isso **não** autoriza apagar
versos necessários de documentos efetivamente configurados como frente
e verso. Os 300 versos brancos do corpus sintético R4 ainda aguardam
fundamentação individual no gate R5.

A UFC recebe TCCs, dissertações e teses em versão eletrônica e publica
exigência de PDF/A para determinados depósitos. A declaração
`pdfstandard=A-2b` solicita a produção nesse padrão, mas **não é laudo
de conformidade**: verificar a saída em ferramenta independente, como
`veraPDF`, e conferir a regra aplicável no curso. A conformidade PDF/UA
e a ordem de leitura acessível permanecem temas separados (issue #459).

Em 2026, a ficha catalográfica visual passou a ser facultativa para os
trabalhos abrangidos pela instrução conjunta UFC 2/2026. Não inserir
ficha fictícia para satisfazer um teste antigo; confirmar as condições
atuais do depósito.

## 8. Erros frequentes e procedimento de validação

| Sintoma | Verificação |
|---|---|
| Arquivo de imagem ausente | Gerar `artifacts/canonical-mesh-study` e compilar na raiz |
| Comando da classe indefinido | Conferir a versão da classe e dependências TeX Live |
| Figura em branco ou cortada | Inspecionar o PDF vetorial original e a posição de composição |
| Referências não aparecem | Rodar Biber entre passagens LaTeX e inspecionar logs |
| Lista de tabelas com numeração inconsistente | Conferir `.lot` e PDF; tratar como regressão R3 |
| Capítulos começam com folhas em branco | Distinguir `single-sided` e `double-sided`; revisar paginação física |
| Autoria aparece em projeto cego | Bloquear entrega até inspeção integral de metadados e texto |
| Aviso de `Overfull hbox` | Localizar a linha no `.log` e corrigir quebras sem mascarar avisos |

A validação é escalonada: **F0** fontes/dados/hashes e testes negativos;
**F1** previews de PDF reais por idioma; **F2** 28 PDFs em todos os perfis,
com logs e hashes; **F3/R5** revisão independente por página, idioma,
estrutura normativa e autorização expressa. Um estágio verde **não**
implica automaticamente a aprovação dos seguintes.

**Estado final:** `v3.1.0 UNRELEASED`,
`publication_authorized=false`. A classe é comunitária e não foi
homologada oficialmente pela UFC.

# Estudo científico canônico e reprodutível: malhas estruturadas

**Objetivo:** fornecer o mesmo conjunto verificável de dados e figuras para os sete
perfis documentais, nos idiomas PT/EN/ES/FR, sem transformar projeto de pesquisa,
artigo, TCC e tese no mesmo texto. Este estudo é um **baseline didático computado**,
não uma tese inédita, uma medição de desempenho nem um resultado do APMesh.

## Fonte única e execução

A fonte versionada é `study.json`; o gerador é
`tools/examples/generate_mesh_study.py` (Python 3, apenas stdlib);
o validador independente é `tests/checks/examples/mesh_study.py`.
O gerador produz três SVGs originais, três PDFs vetoriais, um CSV de métricas,
um manifesto de hashes SHA-256 e quatro seções LaTeX autorais, uma por idioma.
A bibliografia em `references.bib` contém fontes reais de **contexto**,
não os algoritmos executados nesta demonstração.

Execute na raiz do repositório:

    python3 tools/examples/generate_mesh_study.py
    python3 tools/examples/generate_mesh_study.py --check
    python3 tests/checks/examples/mesh_study.py

Para um diretório isolado:

    python3 tools/examples/generate_mesh_study.py --output artifacts/canonical-mesh-study
    python3 tests/checks/examples/mesh_study.py --artifacts artifacts/canonical-mesh-study

O workflow `.github/workflows/mesh-canonical-fast.yml` executa estes
testes sem instalar TeX Live. Uma alteração manual em resultados derivados,
numa figura, ou nos hashes é detectada pelo modo fail-closed. Não confunda
evidência de fonte/conectividade com conformidade acadêmica de um PDF final.

## Protocolo matematicamente verificável

Domínio: Ω = [0,1] × [0,1]. Três malhas com conectividade construída:

| Caso | Resolução | Elementos | Vértices | Arestas | Razão geométrica |
|---|---:|---:|---:|---:|---:|
| Quadriláteros uniformes | 8 × 8 | 64 | 81 | 144 | 1,000 |
| Quadriláteros alongados | 16 × 4 | 64 | 85 | 148 | 4,000 |
| Triângulos estruturados | 8 × 8 | 128 | 81 | 208 | √2 ≈ 1,414 |

A identidade de Euler V−E+F=1 é testada para cada caso. As contagens são
resultado da conectividade e não de medições, estatística ou execução de
algoritmos de remalhamento. A razão geométrica de uma célula não é uma medida
completa de qualidade de malha ou desempenho em EDP.

Referências verificadas, usadas apenas como estado da arte:
Bommes, Zimmer e Kobbelt (2009), *Mixed-Integer Quadrangulation*,
DOI 10.1145/1576246.1531383;
Shewchuk (2002), *Delaunay refinement algorithms for triangular mesh generation*,
DOI 10.1016/S0925-7721(01)00047-5.

## Mesmo corpus, modalidades diferentes

| Modalidade | Dados compartilhados | Texto específico |
|---|---|---|
| TCC de graduação | domínio, figuras, tabela, matemática | implementação, avaliação, limitações |
| Especialização | mesmo benchmark | caso aplicado, decisão técnica |
| Dissertação | mesmo benchmark | hipóteses, comparações e análise |
| Tese | mesmo benchmark | revisão ampliada, lacuna e contribuição **demonstrada** |
| Projeto de pesquisa | problema, literatura, protocolo | cronograma e resultados **esperados** |
| Projeto anonimizado | os mesmos dados públicos | ocultar identidade em texto, XMP e metadados |
| Artigo | dados efetivamente calculados | síntese dos métodos e resultados sem invenção |

Não afirmamos descoberta científica nem desempenho superior. Tese, projeto e
artigo não devem ser padronizados por uma colagem literal do mesmo manuscrito.

## Estrutura oficial da UFC e normas

- Modelos em Word, ODT e projeto DOCX: https://biblioteca.ufc.br/pt/servicos-e-produtos/templates/
- Guias: https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/

A finalidade dessas fontes é validar estrutura e elementos, não copiar
passagens protegidas ou interpretar modelos antigos como norma atual.
O ABNTEXTO-UFC é uma classe comunitária, não homologada pela UFC.

## Estado e limites

**Fase 1:** fonte científica canônica, figuras originais, quatro textos e
testes rápidos de integridade/reprodução. **Fase 2:** alimentar os sete
geradores existentes, com bibliografia real e perfil próprio. A inclusão
da seção gerada exige que o documento carregue o backend de figuras e tabelas
e registre `references.bib` para a compilação Biber; a integração será
testada separadamente em todos os PDFs completos 28+4.

**Fase 3:** auditoria R5 em todas as páginas, análise normativa e
aprovação humana. Os PDFs do corpus anterior continuam como baseline
de regressão, nunca certificados pelo novo conteúdo.

Versão 3.1.0: **UNRELEASED; publication_authorized=false**.

# Modelo de Trabalho Acadêmico UFC em LaTeX

Este pacote preserva a estrutura histórica do template UFC/abnTeX2 e moderniza sua infraestrutura para uso genérico em cursos, programas e unidades acadêmicas da Universidade Federal do Ceará. A atualização foi feita com quatro objetivos simultâneos:

1. manter a conformidade editorial com os guias publicados pelo Sistema de Bibliotecas da UFC;
2. preservar a retrocompatibilidade com documentos construídos sobre o template histórico;
3. adotar interfaces e pacotes atuais do ecossistema LaTeX sem aumentar dependências desnecessárias;
4. oferecer módulos opcionais úteis a trabalhos acadêmicos em Ciência da Computação, Engenharias e demais áreas tecnológicas.

> **Precedência normativa:** regras específicas do curso/programa e do edital aplicável prevalecem sobre o template. O template auxilia a composição; ele não substitui a conferência das normas vigentes no momento da submissão ou depósito.

## Arquitetura da versão modernizada

A classe-base continua sendo `abntex2`, baseada em `memoir`. A decisão é deliberada: toda a camada institucional histórica do template UFC depende da API dessas classes. A classe `abntexto`, embora seja uma alternativa atual e em desenvolvimento ativo, possui outra API e exige uma migração de plataforma, não apenas uma troca de pacote. Essa avaliação fica reservada para uma versão maior futura.

A modernização desta versão ocorre ao redor da classe existente:

```text
documento.tex
    |
    +-- \ufcsetup{...}              configuração pública
    |
    +-- lib/preambulo.tex           infraestrutura LaTeX
    |       +-- tipografia/engines
    |       +-- matemática/unidades
    |       +-- figuras/tabelas
    |       +-- glossários
    |       +-- bibliografia
    |       +-- referências cruzadas
    |
    +-- lib/ufctex.sty              regras UFC + compatibilidade
            +-- LaTeX3/l3keys
            +-- modalidades
            +-- anonimização
            +-- módulos opcionais
            +-- wrappers legados
```

A interface recomendada para documentos novos é `\ufcsetup{...}`. Os comandos do template histórico (`\trabalhoacademico`, `\ies`, `\autor`, `\titulo`, etc.) continuam disponíveis para não quebrar projetos existentes.

## Modos do documento

Selecione o modo pela chave `tipo` em `documento.tex`:

```tex
\ufcsetup{
    tipo = tccgraduacao,
    % ...
}
```

Modos suportados:

- `tccgraduacao`: TCC de graduação;
- `tccespecializacao`: TCC/monografia de especialização;
- `dissertacao`: dissertação de mestrado;
- `tese`: tese de doutorado;
- `projeto`: projeto de pesquisa identificado;
- `projetoanonimizado`: projeto de pesquisa sem identificação pessoal, quando exigido pelo regulamento ou edital.

`projetocego` permanece somente como alias legado e emite aviso de depreciação. Para novos documentos, use `projetoanonimizado`.

## Exemplo de configuração moderna

```tex
\ufcsetup{
    tipo = tese,
    ies = {Universidade Federal do Ceará},
    sigla = {UFC},
    centro = {Centro, Faculdade, Instituto ou Campus},
    departamento = {Departamento ou Unidade Acadêmica},

    programa-doutorado = {Nome do Programa},
    nome-doutorado = {Nome do Doutorado},
    titulo-doutor = {Área do título},
    area-doutorado = {Área de Concentração},

    autor = {Nome Sobrenome},
    titulo = {Título do Trabalho},
    local = {Fortaleza},
    ano = {2026},

    orientador = {Prof. Dr. Nome do Orientador},
    ficha-catalografica = nao,
    links = discretos,

    algoritmos = nenhum,
    codigo = listings,
    graficos = nao,
    caixas = nao,
    teoremas = basico
}
```

## Núcleo LaTeX modernizado

A configuração atual evita sobreposição de pacotes e mantém no núcleo apenas funcionalidades amplamente úteis.

| Área | Infraestrutura atual | Observação |
|---|---|---|
| Classe | `abntex2` / `memoir` | preservada por compatibilidade institucional |
| Configuração | LaTeX3 / `l3keys` | usada por `\ufcsetup` |
| Bibliografia | `biblatex` + estilo `abnt` + Biber | substitui `abntex2cite` |
| Glossários/siglas | `glossaries-extra` | mantém `\newacronym`, `\gls` e listas |
| Matemática | `mathtools` | extensão de `amsmath` |
| Tipografia pdfLaTeX | `newtxtext` / `newtxmath` | substitui `mathptmx` |
| Tipografia Lua/XeLaTeX | `fontspec` + `unicode-math` | OpenType/Unicode |
| Unidades/números | `siunitx` | API atual e vírgula decimal configurada |
| Microtipografia | `microtype` | habilitada; compatibilidade TL2025 tratada seletivamente |
| Figuras | `graphicx`, `adjustbox`, `subcaption` | imagens, limites e subfiguras |
| Tabelas | `tabularray-abnt`, `booktabs`, `siunitx` | padrão recomendado para tabelas novas |
| Tabelas legadas | `array`, `tabularx`, `longtable` | mantidas por compatibilidade |
| URLs | `xurl` | melhora quebra de URLs extensas |
| Referências cruzadas | `cleveref` | API madura e compatível com documentos existentes |
| Código-fonte | `listings` | padrão portátil; `minted` é opcional |

Pacotes que existiam na configuração histórica e deixaram de ser carregados globalmente incluem `inputenc`, `mathptmx`, `abntex2cite`, `algorithm2e`, `paracol`, `appendix`, `tocloft`, `multirow`, `xltabular`, `threeparttable` e `makecell`. Alguns podem ser reativados manualmente por um documento legado, mas não são necessários ao núcleo atual.

## Engines: pdfLaTeX, LuaLaTeX e XeLaTeX

O projeto usa `iftex` para selecionar a infraestrutura adequada ao engine.

### pdfLaTeX — padrão recomendado

É o caminho mais conservador e compatível com o template histórico e com o Overleaf:

```text
pdfLaTeX -> newtxtext/newtxmath
```

UTF-8 é assumido pelo LaTeX moderno; `inputenc` não é carregado explicitamente.

### LuaLaTeX / XeLaTeX — fluxo Unicode/OpenType

O template também possui caminho compatível com engines Unicode:

```text
LuaLaTeX/XeLaTeX -> fontspec + unicode-math
```

A configuração padrão usa fontes OpenType distribuídas com TeX Live (`TeX Gyre Termes X` e `XITS Math`) para não depender de fontes proprietárias instaladas no sistema. Se uma unidade exigir literalmente uma fonte comercial e ela estiver legalmente instalada no ambiente de compilação, a configuração pode ser substituída localmente.

Compilação local com LuaLaTeX:

```bash
make lua
```

O fluxo principal permanece pdfLaTeX até que a cadeia completa de depósito/acessibilidade da UFC exija ou recomende outro engine.

## Módulos opcionais para Ciência da Computação e áreas tecnológicas

Recursos pesados não são carregados globalmente. Eles são ativados por `\ufcsetup` somente quando o trabalho precisa deles.

### Pseudocódigo

Para novos trabalhos:

```tex
algoritmos = algpseudocodex
```

Exemplo:

```tex
\begin{algorithm}[htbp]
    \caption{Exemplo de algoritmo}
    \label{alg:exemplo}
    \begin{algorithmic}[1]
        \Require Dados de entrada $X$
        \Ensure Resultado $Y$
        \State Inicialize $Y \gets \varnothing$
        \ForAll{$x \in X$}
            \If{$x$ satisfaz o critério}
                \State $Y \gets Y \cup \{x\}$
            \EndIf
        \EndFor
        \State \Return $Y$
    \end{algorithmic}
\end{algorithm}
```

Para documentos antigos que já dependem da sintaxe de `algorithm2e`:

```tex
algoritmos = algorithm2e
```

`algorithm2e` é compatibilidade, não o padrão recomendado para conteúdo novo.

### Código-fonte

Padrão portátil:

```tex
codigo = listings
```

Opcional, quando syntax highlighting via Pygments for desejado e o ambiente suportar `minted`:

```tex
codigo = minted
```

`listings` permanece o default porque não exige um processador externo adicional e é mais previsível em instalações restritas.

### Gráficos científicos e diagramas

```tex
graficos = sim
```

Carrega `tikz`, `pgfplots` e `pgfplotstable`. É indicado para curvas experimentais, benchmarks, superfícies, diagramas e gráficos reprodutíveis gerados a partir de dados. Como a pilha PGF aumenta o custo de compilação, ela permanece desligada por padrão.

### Caixas semânticas

```tex
caixas = sim
```

Carrega `tcolorbox`, útil para exemplos, observações, definições especiais e conteúdo técnico destacado. O uso deve respeitar a sobriedade gráfica exigida pelo contexto acadêmico.

### Teoremas avançados

O template continua fornecendo os ambientes históricos de teoremas e definições. Para recursos adicionais de declaração/estilo:

```tex
teoremas = avancado
```

Isso carrega `thmtools`.

## Tabelas e quadros

Para conteúdo novo, o caminho recomendado é `tabularray-abnt`, que fornece temas voltados a tabela/quadro e uma interface moderna baseada em chaves.

Exemplo:

```tex
\begin{table}[htbp]
    \centering
    \UFCtab{
        \Caption{\label{tab:exemplo} Resultados por configuração}
    }{
        \begin{abnttblr}[]{
            colspec = {lcc},
            row{1} = {font=\bfseries},
            hline{1,Z} = {1pt},
            hline{2} = {0.6pt}
        }
            Configuração & Métrica A & Métrica B \\
            Base         & 7,5       & 8,1       \\
            Método       & 8,7       & 9,0
        \end{abnttblr}
    }{
        \Fonte{Elaborada pelo autor.}
    }
\end{table}
```

Para conteúdo longo, avalie `longabnttblr`. `tabularx` e `longtable` continuam disponíveis para documentos legados.

Os helpers `\UFCfig`, `\UFCtab` e `\UFCqua` mantêm legenda, objeto, fonte e nota sob uma largura lógica comum sem reduzir automaticamente o corpo do objeto.

## Figuras

```tex
\begin{figure}[htbp]
    \centering
    \UFCfig{
        \Caption{\label{fig:exemplo} Título da figura}
    }{
        \UFCincludegraphics[width=.8\linewidth]{figura-2}
    }{
        \Fonte{Elaborada pelo autor.}
    }
\end{figure}
```

`\UFCincludegraphics` limita a imagem à área útil e preserva sua proporção.

## Citações e referências

O backend é Biber com estilo `abnt` do ecossistema BibLaTeX.

Prefira:

```tex
\textcite{chave}
\parencite{chave}
```

Compatibilidade histórica:

```tex
\cite{chave}       % mapeado para citação parentética
\citeonline{chave} % mapeado para citação narrativa
```

O template foi configurado para a política UFC atualmente adotada para autoria em citações: até três autores são apresentados e, para quatro ou mais, usa-se o primeiro seguido de *et al.* de forma consistente. Casos bibliográficos incomuns devem ser conferidos visualmente contra o guia institucional vigente.

## Glossários, siglas e índice

A infraestrutura foi migrada para `glossaries-extra`, preservando a API já usada nos exemplos:

```tex
\newacronym{ABNT}{ABNT}{Associação Brasileira de Normas Técnicas}
...
\gls{ABNT}
```

A lista de siglas continua opcional. Em projetos, só deve ser impressa quando fizer sentido para o conteúdo.

## Revisão normativa UFC aplicada

A auditoria editorial considera o conjunto de guias apontado pela página de normalização do SiBi-UFC: Trabalhos Acadêmicos, Artigo Científico, Citações, Referências e Projetos de Pesquisa, além das orientações institucionais mais recentes sobre depósito e ficha catalográfica.

Quando guias de anos diferentes se sobrepõem, a orientação específica mais recente é usada para aquele assunto. Regras de curso, programa ou edital continuam tendo precedência.

Principais regras refletidas no template:

- papel A4, corpo 12 pt e margens institucionais;
- cadeia institucional configurável na capa;
- bloco de natureza com recuo institucional e espaço simples;
- hierarquia de seções e alíneas;
- paginação e elementos pré-textuais;
- legenda, fonte e notas em tamanho reduzido e espaço simples;
- fonte obrigatória sob ilustrações/tabelas quando aplicável;
- título `REFERÊNCIAS` sem numeração e entradas em espaço simples;
- ficha catalográfica preservada por compatibilidade e desativada por padrão;
- metadados de autor removidos no modo `projetoanonimizado`;
- capa de projeto configurável, pois editais podem impor regras próprias;
- PDF/A tratado como requisito de entrega/validação, não como propriedade assumida de toda compilação LaTeX.

## Projeto anonimizado

No modo:

```tex
tipo = projetoanonimizado
```

o template remove identificação de autoria/orientação das partes pré-textuais configuradas para projeto e deixa o campo `Author` dos metadados PDF vazio. O template não decide quais outros identificadores são permitidos; isso deve ser conferido no edital.

## Ficha catalográfica e PDFs externos

A ficha catalográfica permanece no projeto para compatibilidade:

```tex
ficha-catalografica = nao
```

Ative somente quando necessário.

PDFs externos incorporados com `\includepdf` podem introduzir fontes e propriedades incompatíveis com o PDF final. Por isso os exemplos históricos com PDFs externos permanecem no pacote, mas não são incluídos por padrão.

## Compilação

No Overleaf, mantenha `documento.tex` na raiz do projeto. O padrão recomendado é pdfLaTeX com a versão recente do TeX Live disponibilizada pelo serviço.

Localmente:

```bash
make
```

Fluxo executado pelo `Makefile`:

```text
engine -> Biber -> makeglossaries -> makeindex -> engine -> engine
```

LuaLaTeX:

```bash
make lua
```

Validação adicional:

```bash
make preflight
```

O `preflight` falha quando o log final contém warnings LaTeX/pacote, caixas overfull/underfull relevantes ou quando a verificação de incorporação de fontes detecta problemas em ambientes que fornecem `pdffonts`.

O `Makefile` não mascara falhas de Biber, glossários ou índice.

## Compatibilidade com Overleaf / TeX Live 2025

Algumas combinações de `microtype` presentes no TeX Live 2025 e do kernel LaTeX podem emitir o warning conhecido `Command \showhyphens has changed`. O template mantém `microtype` e filtra **somente essa mensagem específica** via `silence`; demais warnings continuam visíveis.

A versão modernizada foi construída para compilar no fluxo atual do Overleaf, mas a versão do TeX Live de um projeto antigo pode ser selecionada nas configurações do próprio Overleaf. Quando houver comportamento divergente, confirme primeiro a versão do TeX Live usada pelo projeto.

## Retrocompatibilidade

Foram mantidos deliberadamente:

- `\trabalhoacademico{...}`;
- campos históricos como `\ies`, `\centro`, `\autor`, `\titulo`, `\orientador` etc.;
- alias `projetocego` para documentos antigos, com aviso de depreciação;
- opção de `algorithm2e` para documentos que já usam essa sintaxe;
- infraestrutura tradicional `tabularx`/`longtable`;
- ficha catalográfica e comandos pré-textuais históricos;
- ambientes de teorema e código já existentes no template.

A estratégia é modernizar a implementação sem obrigar usuários antigos a reescrever seus documentos.

## Decisões deliberadamente adiadas

### Troca de `abntex2` por `abntexto`

Não foi feita nesta versão. `abntexto` é uma classe diferente, com desenvolvimento ativo e API própria. Uma migração deve ser tratada como versão maior e comparada por regressão visual/normativa em todas as modalidades antes de substituir a base institucional atual.

### Tagged PDF / PDF-UA

O LaTeX atual possui infraestrutura crescente para PDF marcado e acessibilidade, mas a cadeia `abntex2`/`memoir` e vários pacotes acadêmicos ainda precisam ser avaliados em conjunto. O template não ativa tagging experimental por padrão. A prioridade desta versão é estabilidade, conformidade editorial e compatibilidade com Overleaf.

### `zref-clever`

Foi avaliado como alternativa moderna de referência cruzada. `cleveref` foi mantido porque é maduro, já integra a API do template e a troca não trouxe benefício suficiente para justificar incompatibilidade neste ciclo.

## Limitações e responsabilidade do usuário

- Programas podem possuir regras próprias para qualificação, banca, folha de aprovação e natureza do trabalho.
- Regras de avaliação anonimizada variam entre editais.
- A formatação automática de referências deve ser conferida em casos bibliográficos incomuns.
- `minted`, PGF/TikZ e outros módulos opcionais aumentam o custo ou os requisitos de compilação.
- O template não substitui a validação PDF/A exigida no fluxo institucional aplicável.
- Em caso de conflito, prevalecem as normas UFC e regras específicas vigentes.

## Atualização técnica

A modernização preserva os créditos e o histórico do template original. A atualização normativa e técnica desta versão foi realizada por **Tiago Guimarães Sombra (2026)**.


## Histórico legado do template original

As entradas abaixo são preservadas da documentação histórica recebida com o template:

```text
Para utilizar este template siga o tutorial disponível em: https://biblioteca.ufc.br/wp-content/uploads/2015/09/tutorial-sharelatex.pdf

# Útimas alterações
03-07-2017              
    -Contagem de tabelas corrigida;
    -Dois pontos após fonte de figuras e tabelas;       
    -Inclusão do departamento na capa do trabalho;      
    -As equações foram alocadas completamente as esquerda. 
04-07-2017
    -inclusão de pdf em apêndice;
    -inclusão de pdf em anexo.
06-07-2017
    -espaçamento dos títulos de figuras, tabelas e quadros foram alterados de 1.5 para espaçamento simples (1.0);
    -Margens dos títulos das figuras ajustadas para ficar do tamanho da figura;
    -Margens dos títulos das tabelas ajustados para ficar do tamanho da tabela;
    -Quadro circunscrito de figuras retirados exceto, figuras de resultados.
    -espaçamento entre linhas ajustado para espaçamento simples nos títulos e legendas de figuras e tabelas;
10-07-2017
    -Elaboração de textos explicativos sobre figuras e equações;
    -Pasta renomeadas para ficar na ordem de pre, textual e pós;  
12-07-2017
    -O nome da pasta das referência estava errado. Isso fazia aparecer um ponto de interrogação nas citações. Isso já foi corrigido.
14-07-2017
    -Espaçamento corrigido entre o texto de identificação do trabalho e o orientador.
18-09-2017
    -Nome da LISTA DE ILUSTRAÇÕES alterado para LISTA DE FIGURAS
15-01-2018
    -Alteração do ano de 2017 para 2018
20-02-2018
    -Alteração do nome "Coorientador" de acordo com a nova norma ortográfica
24-02-2018
    -Inclusão de um texto chamando a atenção para o usuário configurar a opção referente ao nível do trabalho acadêmico que está sendo desenvolvido (tcc de graduação, trabalho de especialização, dissertação de mestrado ou tese de doutorado) nas primeiras opções do arquivo "documento.tex"
22-03-2018
    -Atualização dos e-mails para dúvidas e sugestões;
21-11-2018
    -Adicionada opção para alterar a fonte de todo o texto de Times New Roman para Arial. Basta descomentar as linhas 80 e 81 do arquivo "preambulo.tex" dentro da pasta "lib".
    -Nota de esclarecimento quanto a limitação da geração do referencial bibliográfico. 
09-01-2019
    -Acrescentado comentário explicando com deixar as equações centralizadas na linas 59 do arquivo "documento"
23-01-2019
    -Correção de erro de compilação na linha 60 do arquivo documentos. 
    -Nota de esclarecimento de como utilizar siglas.
07-06-2019
    -Atualização de contato para dúvidas e sugestões.
23-09-2019
    -Alteração do ano de 2018 para 2019. Atualização de tutorial ficha catalográfica para o Overleaf.
```


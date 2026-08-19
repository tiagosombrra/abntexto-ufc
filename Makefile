########################################################################
## Modelo de Trabalho Acadêmico UFC / ufctex V2                        ##
## Revisão normativa e técnica: Tiago Guimarães Sombra (2026).         ##
## Build reproduzível com Biber, glossários e índice.                   ##
########################################################################

VERSION := 2.0.0-dev
filename := documento
ENGINE ?= pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error
V2_LAYOUT_FIXTURES := tests/normativa/layout-anverso.tex tests/normativa/layout-frente-verso.tex
V2_PRETEXTUAL_FIXTURES := tests/normativa/pretextuais-trabalho.tex tests/normativa/pretextuais-projeto-anonimo.tex
V2_OBJECT_FIXTURES := tests/normativa/objetos-avancados.tex
V2_MINTED_FIXTURE := tests/normativa/objetos-minted.tex

.PHONY: all compile pdf lua preflight v2-reference-check v2-check v2-layout-check v2-pdf-geometry-check v2-pretextual-check v2-object-check v2-minted-check v2-bib-check v2-project-check v2-profile-check v2-posttextual-compat-check version clean

all: compile
pdf: compile

version:
	@echo "$(VERSION)"

compile:
	@echo "Compilando $(filename).tex com $(ENGINE) + Biber..."
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	biber $(filename)
	makeglossaries $(filename)
	makeindex $(filename)
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	@echo "Processo finalizado com sucesso."

# Validate the Unicode/OpenType path without changing the default Overleaf flow.
lua:
	$(MAKE) clean
	$(MAKE) ENGINE=lualatex compile

# Validate the user-facing V2 document.
v2-reference-check:
	@sh tests/v2-reference-check.sh

# Compile the isolated v2 layout fixtures with both supported engines.
v2-layout-check:
	@set -e; \
	for engine in pdflatex lualatex; do \
		for fixture in $(V2_LAYOUT_FIXTURES); do \
			echo "Validando $$fixture com $$engine..."; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-layout.log 2>&1; then \
				cat /tmp/ufctex-v2-layout.log; exit 1; \
			fi; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-layout.log 2>&1; then \
				cat /tmp/ufctex-v2-layout.log; exit 1; \
			fi; \
		done; \
	done

# Validate the generated PDF geometry against the normative page model.
v2-pdf-geometry-check:
	@sh tests/v2-pdf-geometry-check.sh

# Validate pre-textual ordering, TOC isolation and anonymized-project output.
v2-pretextual-check:
	@set -e; \
	for engine in pdflatex lualatex; do \
		for fixture in $(V2_PRETEXTUAL_FIXTURES); do \
			echo "Validando $$fixture com $$engine..."; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-pretextual.log 2>&1; then \
				cat /tmp/ufctex-v2-pretextual.log; exit 1; \
			fi; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-pretextual.log 2>&1; then \
				cat /tmp/ufctex-v2-pretextual.log; exit 1; \
			fi; \
		done; \
	done
	@if grep -Eiq 'dedicat[oó]ria|agradecimentos|resumo|abstract|lista de' pretextuais-trabalho.toc; then \
		echo "Preflight V2 falhou: elemento pré-textual entrou no Sumário."; \
		cat pretextuais-trabalho.toc; exit 1; \
	fi
	@grep -Eiq 'Introdu' pretextuais-trabalho.toc || \
		(echo "Preflight V2 falhou: seção textual ausente do Sumário."; exit 1)
	@if command -v pdftotext >/dev/null 2>&1; then \
		pdftotext pretextuais-trabalho.pdf /tmp/ufctex-v2-pretextual.txt; \
		for heading in 'AGRADECIMENTOS' 'RESUMO' 'ABSTRACT' 'LISTA DE FIGURAS' 'LISTA DE TABELAS' 'LISTA DE ABREVIATURAS E SIGLAS' 'LISTA DE SÍMBOLOS' 'SUMÁRIO'; do \
			grep -Fq "$$heading" /tmp/ufctex-v2-pretextual.txt || \
				(echo "Preflight V2 falhou: título pré-textual ausente ou incorreto: $$heading"; exit 1); \
		done; \
		if grep -Eiq '^Dedicat[oó]ria$$' /tmp/ufctex-v2-pretextual.txt; then \
			echo "Preflight V2 falhou: dedicatória recebeu título."; exit 1; \
		fi; \
		pdftotext pretextuais-projeto-anonimo.pdf /tmp/ufctex-v2-anonimo.txt; \
		if grep -Fq 'AUTOR SIGILOSO TESTE' /tmp/ufctex-v2-anonimo.txt; then \
			echo "Preflight V2 falhou: autor vazou no projeto anonimizado."; exit 1; \
		fi; \
		if grep -Fq 'ORIENTADOR SIGILOSO TESTE' /tmp/ufctex-v2-anonimo.txt; then \
			echo "Preflight V2 falhou: orientador vazou no projeto anonimizado."; exit 1; \
		fi; \
		grep -Fq 'PROJETO-ANONIMO-001' /tmp/ufctex-v2-anonimo.txt || \
			(echo "Preflight V2 falhou: identificador anonimizado ausente."; exit 1); \
	fi

# Validate figures, tables, quadros, graphs, code and pseudocode.
v2-object-check:
	@set -e; \
	for engine in pdflatex lualatex; do \
		for fixture in $(V2_OBJECT_FIXTURES); do \
			echo "Validando $$fixture com $$engine..."; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-objects.log 2>&1; then \
				cat /tmp/ufctex-v2-objects.log; exit 1; \
			fi; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-objects.log 2>&1; then \
				cat /tmp/ufctex-v2-objects.log; exit 1; \
			fi; \
		done; \
	done
	@warnings=$$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' objetos-avancados.log | \
		grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true); \
	if [ -n "$$warnings" ]; then \
		printf '%s\n' "$$warnings"; \
		echo "Contexto das caixas excedentes:"; \
		grep -n -A4 -B1 -E 'Overfull \\hbox|Overfull \\vbox' objetos-avancados.log || true; \
		echo "Preflight V2 falhou: fixture de objetos contém warnings ou overflow não reconhecidos."; exit 1; \
	fi
	@grep -Fq 'Figura normativa de teste' objetos-avancados.lof || \
		(echo "Preflight V2 falhou: figura ausente da lista de figuras."; exit 1)
	@grep -Fq 'Tabela acadêmica de teste' objetos-avancados.lot || \
		(echo "Preflight V2 falhou: tabela ausente da lista de tabelas."; exit 1)
	@grep -Fq 'Quadro multipágina de teste' objetos-avancados.loq || \
		(echo "Preflight V2 falhou: quadro ausente da lista de quadros."; exit 1)
	@grep -Fq 'Gráfico normativo de teste' objetos-avancados.logr || \
		(echo "Preflight V2 falhou: gráfico ausente da lista de gráficos."; exit 1)
	@grep -Fq 'Trecho C++ embutido' objetos-avancados.loc || \
		(echo "Preflight V2 falhou: código embutido ausente da lista de códigos."; exit 1)
	@grep -Fq 'Arquivo C++ externo' objetos-avancados.loc || \
		(echo "Preflight V2 falhou: código externo ausente da lista de códigos."; exit 1)
	@grep -Fq 'Busca linear' objetos-avancados.loa || \
		(echo "Preflight V2 falhou: algoritmo ausente da lista de algoritmos."; exit 1)
	@grep -Fq 'Figura normativa de teste' objetos-avancados.loi || \
		(echo "Preflight V2 falhou: figura ausente da lista unificada de ilustrações."; exit 1)
	@grep -Fq 'Gráfico normativo de teste' objetos-avancados.loi || \
		(echo "Preflight V2 falhou: gráfico ausente da lista unificada de ilustrações."; exit 1)
	@grep -Fq 'Quadro multipágina de teste' objetos-avancados.loi || \
		(echo "Preflight V2 falhou: quadro ausente da lista unificada de ilustrações."; exit 1)
	@if grep -Fq 'Tabela acadêmica de teste' objetos-avancados.loi; then \
		echo "Preflight V2 falhou: tabela entrou indevidamente na lista de ilustrações."; exit 1; \
	fi
	@if command -v pdftotext >/dev/null 2>&1; then \
		pdftotext objetos-avancados.pdf /tmp/ufctex-v2-objects.txt; \
		for heading in 'LISTA DE ILUSTRAÇÕES' 'LISTA DE FIGURAS' 'LISTA DE TABELAS' 'LISTA DE QUADROS' 'LISTA DE GRÁFICOS' 'LISTA DE CÓDIGOS' 'LISTA DE ALGORITMOS'; do \
			grep -Fq "$$heading" /tmp/ufctex-v2-objects.txt || \
				(echo "Preflight V2 falhou: lista de objeto ausente: $$heading"; exit 1); \
		done; \
		grep -Fq 'Fonte:' /tmp/ufctex-v2-objects.txt || \
			(echo "Preflight V2 falhou: fonte de objeto ausente."; exit 1); \
		grep -Fq 'Nota:' /tmp/ufctex-v2-objects.txt || \
			(echo "Preflight V2 falhou: nota de objeto ausente."; exit 1); \
	fi

# Exercise minted when its executable is available in the TeX environment.
v2-minted-check:
	@if command -v latexminted >/dev/null 2>&1; then \
		set -e; \
		for engine in pdflatex lualatex; do \
			echo "Validando $(V2_MINTED_FIXTURE) com $$engine..."; \
			if ! $$engine -shell-escape $(LATEXFLAGS) $(V2_MINTED_FIXTURE) > /tmp/ufctex-v2-minted.log 2>&1; then \
				cat /tmp/ufctex-v2-minted.log; exit 1; \
			fi; \
			if ! $$engine -shell-escape $(LATEXFLAGS) $(V2_MINTED_FIXTURE) > /tmp/ufctex-v2-minted.log 2>&1; then \
				cat /tmp/ufctex-v2-minted.log; exit 1; \
			fi; \
		done; \
		overflow=$$(grep -E 'Overfull \\hbox|Overfull \\vbox' objetos-minted.log || true); \
		if [ -n "$$overflow" ]; then \
			printf '%s\n' "$$overflow"; \
			echo "Preflight V2 falhou: fixture minted contém overflow."; exit 1; \
		fi; \
		grep -Fq 'Arquivo Python com minted' objetos-minted.loc || \
			(echo "Preflight V2 falhou: minted ausente da lista de códigos."; exit 1); \
	else \
		echo "latexminted não disponível; rota minted não executada neste ambiente."; \
	fi

# Validate UFC author-date citations and bibliography formatting with Biber.
v2-bib-check:
	@sh tests/v2-bibliography-check.sh

# Validate research projects against NBR 15287:2025.
v2-project-check:
	@sh tests/v2-project-check.sh

# Validate all six document profiles with both supported engines.
v2-profile-check:
	@sh tests/v2-profile-matrix-check.sh

# Validate post-textual elements and the public V1 compatibility layer.
v2-posttextual-compat-check:
	@sh tests/v2-posttextual-compat-check.sh

# Run every isolated V2 gate available locally.
v2-check: v2-layout-check v2-pdf-geometry-check v2-pretextual-check v2-object-check v2-minted-check v2-bib-check v2-project-check v2-profile-check v2-posttextual-compat-check
	@echo "Gate local isolado da V2 concluído."

# Full local gate: user-facing document plus the isolated V2 regression matrix.
preflight: v2-reference-check v2-check
	@echo "Preflight completo da V2 concluído."

clean:
	@echo "Limpando arquivos auxiliares..."
	@rm -f *.out *.aux *.alg *.acr *.dvi *.gls *.log *.bbl *.blg *.bcf *.run.xml
	@rm -f *.ntn *.not *.lof *.loi *.lot *.toc *.loa *.loc *.logr *.lsg *.nlo *.nls *.ilg *.ind
	@rm -f *.glg *.glo *.xdy *.acn *.idx *.loq *.lol *.fls *.fdb_latexmk *.synctex.gz *~
	@rm -f layout-anverso.pdf layout-frente-verso.pdf
	@rm -f pretextuais-trabalho.pdf pretextuais-projeto-anonimo.pdf
	@rm -f objetos-avancados.pdf objetos-minted.pdf citacoes-referencias.pdf
	@rm -f referencias-6023-2025.pdf projeto-15287.pdf projeto-sem-capa.pdf
	@rm -f perfil-*.pdf perfil-*.aux perfil-*.log perfil-*.out perfil-*.toc .ufctex-v2-profile.tex
	@rm -rf _minted-*
	@rm -f $(filename).pdf
	@echo "Processo finalizado com sucesso."

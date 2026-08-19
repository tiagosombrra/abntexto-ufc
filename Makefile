########################################################################
## Modelo de Trabalho Acadêmico UFC / ufctex V2                        ##
## Revisão normativa e técnica: Tiago Guimarães Sombra (2026).         ##
########################################################################

VERSION := 2.0.0
filename ?= documento
ENGINE ?= pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all pdf compile lua version clean \
	preflight release-preflight \
	v2-reference-check v2-pdfa-check v2-check v2-distribution-check \
	v2-layout-check v2-pdf-geometry-check \
	v2-pretextual-check v2-duplex-pretextual-check \
	v2-object-check v2-minted-check v2-bib-check \
	v2-project-check v2-profile-check v2-profile-pdfa-check \
	v2-posttextual-compat-check v2-duplex-posttextual-check \
	v2-build-check v2-multivolume-check v2-catalog-card-check

all: compile
pdf: compile

version:
	@echo "$(VERSION)"

compile:
	@echo "Compilando $(filename).tex com $(ENGINE)..."
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	@if [ -s "$(filename).bcf" ] && grep -q '<bcf:datasource' "$(filename).bcf"; then \
		echo "Executando Biber..."; \
		biber "$(filename)"; \
	else \
		echo "Biber não necessário."; \
	fi
	@if [ -s "$(filename).glo" ]; then \
		echo "Processando glossário..."; \
		makeglossaries "$(filename)"; \
	else \
		echo "Glossário não necessário."; \
	fi
	@if [ -s "$(filename).idx" ]; then \
		echo "Processando índice..."; \
		makeindex "$(filename)"; \
	else \
		echo "Índice não necessário."; \
	fi
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	@echo "Processo finalizado com sucesso."

lua:
	$(MAKE) clean
	$(MAKE) ENGINE=lualatex compile

v2-reference-check:
	@sh tests/v2-reference-check.sh

v2-pdfa-check: v2-reference-check
	@sh tests/v2-pdfa-check.sh

v2-distribution-check:
	@sh tests/v2-distribution-check.sh

v2-layout-check:
	@sh tests/v2-layout-check.sh

v2-pdf-geometry-check:
	@sh tests/v2-pdf-geometry-check.sh

v2-pretextual-check:
	@sh tests/v2-pretextual-check.sh

v2-duplex-pretextual-check:
	@sh tests/v2-duplex-pretextual-check.sh

v2-object-check:
	@sh tests/v2-object-check.sh

v2-minted-check:
	@sh tests/v2-minted-check.sh

v2-bib-check:
	@sh tests/v2-bibliography-check.sh
	@sh tests/v2-reference-spacing-check.sh

v2-project-check:
	@sh tests/v2-project-check.sh

v2-profile-check:
	@sh tests/v2-profile-matrix-check.sh

v2-profile-pdfa-check: v2-profile-check
	@sh tests/v2-profile-pdfa-check.sh

v2-posttextual-compat-check:
	@sh tests/v2-posttextual-compat-check.sh

v2-duplex-posttextual-check:
	@sh tests/v2-duplex-posttextual-check.sh

v2-build-check:
	@sh tests/v2-build-path-check.sh

v2-multivolume-check:
	@sh tests/v2-multivolume-check.sh

v2-catalog-card-check:
	@sh tests/v2-catalog-card-check.sh

v2-check: \
	v2-distribution-check \
	v2-layout-check \
	v2-pdf-geometry-check \
	v2-pretextual-check \
	v2-duplex-pretextual-check \
	v2-object-check \
	v2-minted-check \
	v2-bib-check \
	v2-project-check \
	v2-profile-check \
	v2-posttextual-compat-check \
	v2-duplex-posttextual-check \
	v2-build-check \
	v2-multivolume-check \
	v2-catalog-card-check
	@echo "Gate local isolado da V2 concluído."

preflight: v2-reference-check v2-check
	@echo "Preflight completo da V2 concluído."

release-preflight: preflight
	@sh tests/v2-pdfa-check.sh
	@sh tests/v2-profile-pdfa-check.sh
	@echo "Preflight de release da V2 concluído."

clean:
	@echo "Limpando arquivos auxiliares..."
	@rm -f *.out *.aux *.alg *.acr *.dvi *.gls *.log *.bbl *.blg *.bcf *.run.xml
	@rm -f *.ntn *.not *.lof *.loi *.lot *.toc *.loa *.loc *.logr *.lsg *.nlo *.nls *.ilg *.ind
	@rm -f *.glg *.glo *.xdy *.acn *.idx *.loq *.lol *.fls *.fdb_latexmk *.synctex.gz *~
	@rm -f layout-anverso.pdf layout-frente-verso.pdf geometria-*.pdf
	@rm -f pretextuais-trabalho.pdf pretextuais-projeto-anonimo.pdf pretextuais-duplex-*.pdf
	@rm -f objetos-avancados.pdf objetos-minted.pdf citacoes-referencias.pdf
	@rm -f referencias-6023-2025.pdf projeto-15287.pdf projeto-sem-capa.pdf
	@rm -f postextuais*.pdf multivolume-*.pdf ficha-catalografica-*.pdf
	@rm -f perfil-*.pdf perfil-*.aux perfil-*.log perfil-*.out perfil-*.toc
	@rm -f perfil-*.bbl perfil-*.bcf perfil-*.blg perfil-*.run.xml perfil-*.tex
	@rm -f ufctex-build-minimo.* .ufctex-v2-profile.tex
	@rm -rf _minted-*
	@rm -f $(filename).pdf
	@echo "Processo finalizado com sucesso."

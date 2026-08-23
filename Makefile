########################################################################
## Modelo de Trabalho Acadêmico UFC / abntexto-ufc V2                  ##
## Revisão normativa e técnica: Tiago Guimarães Sombra (2026).         ##
########################################################################

VERSION := 2.1.0
filename ?= documento
ENGINE ?= pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all pdf compile lua version clean reference-assets \
	check release-check preflight release-preflight package distribution-preflight \
	v2-repository-audit v2-reference-check v2-reference-corpus-check v2-overleaf-stable-check

all: compile
pdf: compile

version:
	@echo "$(VERSION)"

reference-assets:
	@python3 tools/fetch-reference-images.py

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

check:
	@python3 tests/run.py --mode pr

release-check:
	@python3 tests/run.py --mode release

v2-repository-audit:
	@python3 tests/v2-repository-audit.py

v2-reference-check:
	@sh tests/v2-reference-check.sh

v2-reference-corpus-check: v2-reference-check
	@sh tests/v2-reference-corpus-check.sh

v2-overleaf-stable-check:
	@sh tests/v2-overleaf-stable-check.sh

preflight: check
	@echo "Preflight completo da V2 concluído."

release-preflight: release-check
	@echo "Preflight de release da V2 concluído."

package: reference-assets
	@$(MAKE) release-preflight
	@python3 tools/fetch-abntexto.py --output .abntexto-ufc-upstream.cls
	@python3 tools/build-release-bundles.py --abntexto .abntexto-ufc-upstream.cls
	@rm -f .abntexto-ufc-upstream.cls
	@echo "Bundles de distribuição da V2 concluídos."

distribution-preflight: package
	@python3 tests/v2-release-package-check.py
	@python3 tests/v2-ctan-archive-check.py dist/abntexto-ufc-ctan-$(VERSION).zip
	@echo "Preflight automatizado de distribuição concluído."

clean:
	@echo "Limpando arquivos auxiliares..."
	@rm -f *.out *.aux *.alg *.acr *.dvi *.gls *.log *.bbl *.blg *.bcf *.run.xml
	@rm -f *.ntn *.not *.lof *.loi *.lot *.toc *.loa *.loc *.logr *.lsg *.nlo *.nls *.ilg *.ind
	@rm -f *.glg *.glo *.xdy *.acn *.idx *.loq *.lol *.fls *.fdb_latexmk *.synctex.gz *~
	@rm -f layout-anverso.pdf layout-frente-verso.pdf geometria-*.pdf normativa-complementar-*.pdf
	@rm -f font-config-*.pdf font-config-*.aux font-config-*.log font-config-*.out ufctex-font-config.tex
	@rm -f matematica-*.pdf matematica-*.aux matematica-*.log matematica-*.out ufctex-matematica.tex
	@rm -f objeto-geometria-*.pdf objeto-geometria-*.aux objeto-geometria-*.log objeto-geometria-*.out
	@rm -f tabela-ibge-*.pdf tabela-ibge-*.aux tabela-ibge-*.log tabela-ibge-*.out tabela-ibge-*.lot
	@rm -f tipografia-codigo-*.pdf tipografia-codigo-*.aux tipografia-codigo-*.log tipografia-codigo-*.out
	@rm -f tipografia-codigo-*.loa tipografia-codigo-*.loc ufctex-code-typography.tex
	@rm -f algoritmo-linhas-*.pdf algoritmo-linhas-*.aux algoritmo-linhas-*.log algoritmo-linhas-*.out algoritmo-linhas-*.loa
	@rm -f fontes-documentais-*.pdf fontes-documentais-*.aux fontes-documentais-*.bbl fontes-documentais-*.bcf
	@rm -f fontes-documentais-*.blg fontes-documentais-*.log fontes-documentais-*.out fontes-documentais-*.run.xml
	@rm -f pretextuais-trabalho.pdf pretextuais-projeto-anonimo.pdf pretextuais-duplex-*.pdf
	@rm -f objetos-avancados.pdf objetos-minted.pdf citacoes-referencias.pdf
	@rm -f referencias-6023-2025.pdf projeto-15287.pdf projeto-sem-capa.pdf
	@rm -f postextuais*.pdf multivolume-*.pdf ficha-catalografica-*.pdf
	@rm -f perfil-*.pdf perfil-*.aux perfil-*.log perfil-*.out perfil-*.toc
	@rm -f perfil-*.bbl perfil-*.bcf perfil-*.blg perfil-*.run.xml perfil-*.tex
	@rm -f ufctex-build-minimo.* abntexto-ufc-build-minimo.* ufctex-compat-minimo.* .ufctex-v2-profile.tex
	@rm -f .ufctex-abntexto.cls .abntexto-ufc-upstream.cls
	@rm -f overleaf-stable-pdflatex.pdf overleaf-stable-lualatex.pdf
	@rm -rf _minted-* dist
	@rm -f $(filename).pdf
	@echo "Processo finalizado com sucesso."

#!/usr/bin/env python3
"""Author human-readable, content-complete review manuscripts from R4 coverage.

This creates exactly seven distinct source PDFs per language, not a public
normative certificate. R4's engineering markers are preserved in its original
regression generator; only this presentation-specific source is rewritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "tests/integration/frontmatter/generate-comprehensive-corpus.py"
PROFILES = ("undergraduate-capstone", "specialization-capstone",
            "masters-thesis", "doctoral-thesis", "research-project",
            "anonymized-research-project", "scientific-article")
LOCALES = ("pt", "en", "es", "fr")
BASE = ROOT / "artifacts/comprehensive-7x4"
OUT = ROOT / "artifacts/human-readable-28"

# Every visible synthetic placeholder must become an ordinary scholarly label.
STRINGS = {
    "pt": {
        "author": "Equipe editorial ABNTEXTO-UFC",
        "title": "Análise reprodutível de malhas computacionais estruturadas",
        "project_title": "Projeto de avaliação reprodutível de malhas computacionais",
        "introduction": "Introdução", "methods": "Metodologia e experimentos",
        "subsection": "Materiais e parâmetros", "subsubsection": "Procedimento de análise",
        "paragraph": "Reprodutibilidade", "subparagraph": "Limitações",
        "results": "Resultados e análise", "implementation": "Implementação computacional",
        "discussion": "Discussão dos resultados", "replication": "Verificação experimental",
        "appendix": "Procedimento complementar de processamento",
        "annex": "Ficha demonstrativa de coleta de dados",
        "figure": "Configuração de uma malha estruturada",
        "chart": "Comparação ilustrativa de malhas estruturadas",
        "texttable": "Síntese dos parâmetros experimentais",
        "shorttable": "Exemplo de tabela com resultados calculados",
        "longtable": "Série demonstrativa de execuções controladas",
        "nativetable": "Registro complementar de casos de teste",
        "inlinecode": "Implementação de uma soma de inteiros",
        "externalcode": "Trecho de código de apoio à reprodução",
        "algorithm": "Busca sequencial em um vetor",
        "header_case": "Caso", "header_value": "Valor",
        "row_case": "Execução", "native_case": "Amostra",
        "source": "Elaboração própria com dados ilustrativos, 2026",
        "note": "Os dados são demonstrativos e não caracterizam um estudo empírico.",
        "summary": ("O documento apresenta uma comparação reproduzível de "
                    "discretizações estruturadas do quadrado unitário. "
                    "A metodologia explicita a representação geométrica, "
                    "a contagem de vértices, arestas e células e os limites "
                    "de interpretação dos resultados. Também exemplifica "
                    "figuras, tabelas, algoritmos e referências acadêmicas."),
        "keywords": "malhas estruturadas; geometria computacional; reprodutibilidade",
        "ack": "Agradecemos às pessoas que revisam os exemplos de normalização e verificam seus elementos pré-textuais.",
        "errata": "Exemplo de errata: onde se lê valor estimado, leia-se valor calculado.",
        "dedication": "Dedico esta demonstração à prática rigorosa da pesquisa reproduzível.",
        "epigraph": "O conhecimento científico se fortalece quando seus procedimentos podem ser examinados.",
        "abbrev": "Malha estruturada de quadriláteros", "symbol": "Número de vértices da malha",
        "term": "Malha estruturada", "definition": "Discretização geométrica definida por uma conectividade regular.",
        "intro_text": ("Este manuscrito demonstra a apresentação de um estudo didático "
                       "sobre discretizações de um domínio quadrado. As tabelas e "
                       "figuras permitem verificar quantidades determinadas de forma "
                       "analítica, sem alegar resultados experimentais inéditos."),
        "project_true": "O projeto descreve objetivos, procedimentos e critérios de avaliação.",
        "project_false": "O documento organiza motivação, metodologia, resultados e conclusões.",
        "anon_true": "A identificação do proponente permanece omitida para avaliação cega.",
        "anon_false": "Os dados de identificação acompanham este exemplo acadêmico.",
        "letter": "Definir explicitamente o domínio e as hipóteses do estudo.",
        "nested": "Registrar as escolhas metodológicas:",
        "dash": "separar dados calculados de observações simuladas.",
        "footnote": "Nota metodológica relativa a um conjunto de dados demonstrativo.",
        "citation": "Consulte as fontes de apoio metodológico",
        "replication_text": ("A validação consiste em recomputar as contagens de células e "
                             "compará-las com os valores tabulados. Não foram avaliados "
                             "tempo de execução nem erro numérico."),
        "equation_note": "A equação representa uma soma fechada usada como exemplo de numeração.",
        "appendix_text": "Este apêndice descreve os passos necessários para reproduzir a construção das grades.",
        "annex_text": "Este anexo apresenta uma ficha ilustrativa de registro de observações.",
        "article_note": "Nota de autoria do documento demonstrativo.",
        "institution": "Universidade Federal do Ceará",
        "program": "Ciência da Computação",
    },
    "en": {
        "author": "ABNTEXTO-UFC editorial team",
        "title": "Reproducible analysis of structured computational meshes",
        "project_title": "Project for reproducible evaluation of computational meshes",
        "introduction": "Introduction", "methods": "Methodology and experiments",
        "subsection": "Materials and parameters", "subsubsection": "Analysis procedure",
        "paragraph": "Reproducibility", "subparagraph": "Limitations",
        "results": "Results and analysis", "implementation": "Computational implementation",
        "discussion": "Discussion of results", "replication": "Experimental verification",
        "appendix": "Supplementary processing procedure",
        "annex": "Illustrative data collection form",
        "figure": "Structured mesh configuration",
        "chart": "Illustrative comparison of structured meshes",
        "texttable": "Summary of experimental parameters",
        "shorttable": "Example table of calculated results",
        "longtable": "Illustrative series of controlled runs",
        "nativetable": "Additional record of test cases",
        "inlinecode": "Implementation of integer addition",
        "externalcode": "Supporting code for reproduction",
        "algorithm": "Sequential search in an array",
        "header_case": "Case", "header_value": "Value",
        "row_case": "Run", "native_case": "Sample",
        "source": "Author-generated illustrative data, 2026",
        "note": "These are demonstration data, not empirical findings.",
        "summary": ("This document presents a reproducible comparison of structured "
                    "discretizations of the unit square. The methodology explains "
                    "geometric representation, vertex, edge and cell counting, "
                    "and the limits of interpreting the resulting measurements. "
                    "Figures, tables, algorithms and scholarly references are included."),
        "keywords": "structured meshes; computational geometry; reproducibility",
        "ack": "We acknowledge the readers who review document formatting and inspect its front matter.",
        "errata": "Illustrative erratum: for estimated value, read calculated value.",
        "dedication": "I dedicate this example to rigorous and reproducible scientific work.",
        "epigraph": "Scientific knowledge grows stronger when its methods can be examined.",
        "abbrev": "Structured quadrilateral mesh", "symbol": "Number of mesh vertices",
        "term": "Structured mesh", "definition": "A geometric discretization with regular connectivity.",
        "intro_text": ("This manuscript demonstrates the presentation of a didactic "
                       "study of square-domain discretization. Its tables and "
                       "figures document analytically determined counts rather "
                       "than claiming original experimental findings."),
        "project_true": "This proposal specifies objectives, procedures and evaluation criteria.",
        "project_false": "The manuscript organizes motivation, methods, results and conclusions.",
        "anon_true": "The proponent's identity is withheld for blind evaluation.",
        "anon_false": "Author-identification details accompany this academic example.",
        "letter": "Explicitly define the domain and assumptions of the study.",
        "nested": "Record the methodological decisions:",
        "dash": "distinguish calculated data from simulated observations.",
        "footnote": "Methodological note about the illustrative dataset.",
        "citation": "Consult the supporting methodological sources",
        "replication_text": ("Validation recomputes the cell counts and compares them "
                             "with the tabulated values. Neither runtime nor numerical "
                             "error is evaluated."),
        "equation_note": "This equation illustrates a closed sum and a numbered reference.",
        "appendix_text": "This appendix describes the steps needed to reproduce the mesh construction.",
        "annex_text": "This annex provides an illustrative record sheet for observations.",
        "article_note": "Author note for a demonstration manuscript.",
        "institution": "Federal University of Ceara",
        "program": "Computer Science",
    },
    "es": {
        "author": "Equipo editorial de ABNTEXTO-UFC",
        "title": "Análisis reproducible de mallas computacionales estructuradas",
        "project_title": "Proyecto de evaluación reproducible de mallas computacionales",
        "introduction": "Introducción", "methods": "Metodología y experimentos",
        "subsection": "Materiales y parámetros", "subsubsection": "Procedimiento de análisis",
        "paragraph": "Reproducibilidad", "subparagraph": "Limitaciones",
        "results": "Resultados y análisis", "implementation": "Implementación computacional",
        "discussion": "Discusión de los resultados", "replication": "Verificación experimental",
        "appendix": "Procedimiento complementario de procesamiento",
        "annex": "Ficha ilustrativa de recolección de datos",
        "figure": "Configuración de una malla estructurada",
        "chart": "Comparación ilustrativa de mallas estructuradas",
        "texttable": "Resumen de parámetros experimentales",
        "shorttable": "Ejemplo de tabla con resultados calculados",
        "longtable": "Serie ilustrativa de ejecuciones controladas",
        "nativetable": "Registro adicional de casos de prueba",
        "inlinecode": "Implementación de una suma de enteros",
        "externalcode": "Código de apoyo para la reproducción",
        "algorithm": "Búsqueda secuencial en un arreglo",
        "header_case": "Caso", "header_value": "Valor",
        "row_case": "Ejecución", "native_case": "Muestra",
        "source": "Elaboración propia con datos ilustrativos, 2026",
        "note": "Los datos son demostrativos y no constituyen resultados empíricos.",
        "summary": ("El documento presenta una comparación reproducible de "
                    "discretizaciones estructuradas del cuadrado unitario. "
                    "La metodología explica la representación geométrica, "
                    "el conteo de vértices, aristas y celdas, y los límites "
                    "de interpretación de los resultados. También incluye "
                    "figuras, tablas, algoritmos y referencias académicas."),
        "keywords": "mallas estructuradas; geometría computacional; reproducibilidad",
        "ack": "Agradecemos a quienes revisan la presentación de documentos y sus elementos preliminares.",
        "errata": "Fe de erratas ilustrativa: donde dice valor estimado, léase valor calculado.",
        "dedication": "Dedico este ejemplo a la práctica rigurosa de la ciencia reproducible.",
        "epigraph": "El conocimiento científico se fortalece cuando sus métodos pueden examinarse.",
        "abbrev": "Malla estructurada de cuadriláteros", "symbol": "Número de vértices de la malla",
        "term": "Malla estructurada", "definition": "Una discretización geométrica con conectividad regular.",
        "intro_text": ("Este manuscrito demuestra la presentación de un estudio "
                       "didáctico sobre discretizaciones del dominio cuadrado. "
                       "Las tablas y las figuras permiten verificar conteos "
                       "analíticos, sin afirmar resultados experimentales originales."),
        "project_true": "El proyecto describe objetivos, procedimientos y criterios de evaluación.",
        "project_false": "El documento organiza motivación, métodos, resultados y conclusiones.",
        "anon_true": "Se omite la identidad del proponente para la evaluación anónima.",
        "anon_false": "Este ejemplo académico incorpora los datos de identificación.",
        "letter": "Definir explícitamente el dominio y las hipótesis del estudio.",
        "nested": "Registrar las decisiones metodológicas:",
        "dash": "distinguir los datos calculados de las observaciones simuladas.",
        "footnote": "Nota metodológica relativa a datos ilustrativos.",
        "citation": "Consúltense las fuentes metodológicas de apoyo",
        "replication_text": ("La validación recalcula los conteos de celdas y los "
                             "compara con los valores tabulados. No se evalúan "
                             "tiempos de ejecución ni errores numéricos."),
        "equation_note": "La ecuación ilustra una suma cerrada con referencia numerada.",
        "appendix_text": "Este apéndice describe los pasos necesarios para reproducir la construcción de las mallas.",
        "annex_text": "Este anexo presenta una ficha ilustrativa de registro de observaciones.",
        "article_note": "Nota de autoría del manuscrito demostrativo.",
        "institution": "Universidad Federal de Ceará",
        "program": "Ciencias de la Computación",
    },
    "fr": {
        "author": "Équipe éditoriale ABNTEXTO-UFC",
        "title": "Analyse reproductible de maillages informatiques structurés",
        "project_title": "Projet d'évaluation reproductible de maillages informatiques",
        "introduction": "Introduction", "methods": "Méthodologie et expériences",
        "subsection": "Matériel et paramètres", "subsubsection": "Procédure d'analyse",
        "paragraph": "Reproductibilité", "subparagraph": "Limites",
        "results": "Résultats et analyse", "implementation": "Implémentation informatique",
        "discussion": "Discussion des résultats", "replication": "Vérification expérimentale",
        "appendix": "Procédure complémentaire de traitement",
        "annex": "Fiche illustrative de collecte des données",
        "figure": "Configuration d'un maillage structuré",
        "chart": "Comparaison illustrative de maillages structurés",
        "texttable": "Synthèse des paramètres expérimentaux",
        "shorttable": "Exemple de tableau de résultats calculés",
        "longtable": "Série illustrative d'exécutions contrôlées",
        "nativetable": "Registre complémentaire de cas de test",
        "inlinecode": "Implémentation d'une addition d'entiers",
        "externalcode": "Code source d'appui à la reproduction",
        "algorithm": "Recherche séquentielle dans un tableau",
        "header_case": "Cas", "header_value": "Valeur",
        "row_case": "Exécution", "native_case": "Échantillon",
        "source": "Élaboration originale avec données illustratives, 2026",
        "note": "Il s'agit de données de démonstration et non de résultats empiriques.",
        "summary": ("Ce document présente une comparaison reproductible de "
                    "discrétisations structurées du carré unité. La méthode "
                    "explique la représentation géométrique, le comptage des "
                    "sommets, des arêtes et des cellules ainsi que les limites "
                    "d'interprétation des mesures. Des figures, des tableaux, "
                    "des algorithmes et des références sont également inclus."),
        "keywords": "maillages structurés; géométrie informatique; reproductibilité",
        "ack": "Nous remercions les lecteurs qui vérifient la présentation et les éléments préliminaires.",
        "errata": "Erratum illustratif : lire valeur calculée au lieu de valeur estimée.",
        "dedication": "Je dédie cet exemple à la rigueur de la recherche reproductible.",
        "epigraph": "Le savoir scientifique s'affermit lorsque ses méthodes peuvent être examinées.",
        "abbrev": "Maillage structuré de quadrilatères", "symbol": "Nombre de sommets du maillage",
        "term": "Maillage structuré", "definition": "Discrétisation géométrique caractérisée par une connectivité régulière.",
        "intro_text": ("Ce manuscrit présente un exemple didactique de discrétisation "
                       "d'un domaine carré. Les tableaux et les figures montrent "
                       "des dénombrements analytiques, sans prétendre à des "
                       "résultats expérimentaux originaux."),
        "project_true": "Le projet décrit des objectifs, des méthodes et des critères d'évaluation.",
        "project_false": "Le document expose la motivation, la méthode, les résultats et les conclusions.",
        "anon_true": "L'identité du candidat reste masquée pour permettre une évaluation anonyme.",
        "anon_false": "Cet exemple universitaire contient les données d'identification.",
        "letter": "Définir explicitement le domaine et les hypothèses de l'étude.",
        "nested": "Consigner les décisions méthodologiques :",
        "dash": "distinguer les données calculées des observations simulées.",
        "footnote": "Note méthodologique sur les données illustratives.",
        "citation": "Consulter les références méthodologiques",
        "replication_text": ("La validation consiste à recalculer les nombres de "
                             "cellules et à les confronter aux tableaux. "
                             "Les durées d'exécution et les erreurs numériques "
                             "ne sont pas évaluées."),
        "equation_note": "Cette équation illustre une somme close et sa référence.",
        "appendix_text": "Cette annexe complémentaire décrit les étapes de reproduction du maillage.",
        "annex_text": "Cette annexe fournit une fiche illustrative d'observations.",
        "article_note": "Note d'auteur du manuscrit de démonstration.",
        "institution": "Université fédérale du Ceará",
        "program": "Informatique",
    },
}


# Human review text must never display engineering marker names or leaked English
# placeholders from the original integration suite.
NAMES = {
    "advisor": "Alex Ferreira",
    "coadvisor": "Cris Almeida",
    "examiners": {
        2: "Marina Carvalho", 3: "João Mendes", 4: "Rafael Soares",
        5: "Carla Brito", 6: "Laura Lima",
    },
}
DIFFERENT_CAPTIONS = {
    "pt": {
        "introfigure": "Malha quadrilateral no domínio unitário",
        "introchart": "Grade inicial de comparação das configurações",
        "introtexttable": "Variáveis consideradas na construção das malhas",
        "introtable": "Contagens iniciais de componentes da malha",
    },
    "en": {
        "introfigure": "Quadrilateral mesh on the unit square",
        "introchart": "Initial comparison grid for the configurations",
        "introtexttable": "Variables used to construct the meshes",
        "introtable": "Initial counts of mesh components",
    },
    "es": {
        "introfigure": "Malla cuadrilateral en el dominio unitario",
        "introchart": "Cuadrícula inicial de comparación de configuraciones",
        "introtexttable": "Variables usadas para construir las mallas",
        "introtable": "Conteos iniciales de componentes de malla",
    },
    "fr": {
        "introfigure": "Maillage quadrilatéral du domaine unité",
        "introchart": "Grille initiale de comparaison des configurations",
        "introtexttable": "Variables utilisées pour construire les maillages",
        "introtable": "Dénombrements initiaux des composants du maillage",
    },
}
NEW_PROSE = {
    "pt": (
        "A discretização do quadrado unitário por malhas estruturadas "
        "permite verificar propriedades topológicas de forma controlada. "
        "Os casos contemplam células quadrilaterais e triangulares e "
        "resoluções definidas explicitamente.",
        "Os resultados são derivados de contagens determinísticas de "
        "vértices, arestas e células. A análise diferencia medidas "
        "calculadas de avaliações de desempenho e apresenta referências "
        "cruzadas para figuras, tabelas e algoritmos.",
    ),
    "en": (
        "Discretizing the unit square with structured meshes enables "
        "controlled checks of topological properties. The cases include "
        "quadrilateral and triangular cells with explicitly specified "
        "resolutions.",
        "The results derive from deterministic counts of vertices, edges "
        "and cells. The analysis distinguishes calculated measurements "
        "from performance evaluation and uses cross-references to "
        "figures, tables and algorithms.",
    ),
    "es": (
        "La discretización del cuadrado unitario mediante mallas "
        "estructuradas permite verificar propiedades topológicas de "
        "manera controlada. Los casos consideran celdas cuadriláteras "
        "y triangulares con resoluciones explícitas.",
        "Los resultados proceden de conteos deterministas de vértices, "
        "aristas y celdas. El análisis distingue mediciones calculadas "
        "de evaluaciones de rendimiento y utiliza referencias cruzadas "
        "a figuras, tablas y algoritmos.",
    ),
    "fr": (
        "La discrétisation du carré unité par des maillages structurés "
        "permet de vérifier les propriétés topologiques dans un cadre "
        "contrôlé. Les cas comprennent des cellules quadrilatérales "
        "et triangulaires de résolutions explicites.",
        "Les résultats découlent du dénombrement déterministe des "
        "sommets, arêtes et cellules. L'analyse distingue les mesures "
        "calculées des évaluations de performance et utilise des renvois "
        "aux figures, tableaux et algorithmes.",
    ),
}
EQUATION_REFERENCE = {
    "pt": r"Consulte também a Equação~\ref{eq:r4-sum}.",
    "en": r"See also Equation~\ref{eq:r4-sum}.",
    "es": r"Véase también la ecuación~\ref{eq:r4-sum}.",
    "fr": r"Voir également l'équation~\ref{eq:r4-sum}.",
}


# These are original, self-authored passages used to test long quotations.
# They are not attributed to real publications, to avoid fabricated citations.
# Their content deliberately exceeds three printed lines at the 4 cm indent.
QUOTE_EXAMPLES = {
    "pt": {
        "heading": "Citações diretas e notas de rodapé",
        "intro": "Os dois blocos seguintes demonstram citações longas, com recuo à esquerda, fonte reduzida e espaço simples. Ambos são textos originais de ensaio e não reproduzem obras publicadas.",
        "first": ("Uma malha computacional representa um domínio contínuo por uma coleção "
                  "finita de elementos conectados. Cada elemento possui uma posição "
                  "no domínio e relações topológicas com seus vizinhos. A qualidade "
                  "da representação depende não apenas da quantidade de células, "
                  "mas também da definição explícita de suas conexões e da "
                  "consistência dos dados geométricos. Para que uma comparação "
                  "seja reproduzível, é necessário preservar a entrada, os critérios "
                  "de construção e o procedimento de contagem."),
        "between": "O próximo bloco exemplifica a identificação da origem após a transcrição; a referência é descritiva e corresponde exclusivamente ao texto-modelo.",
        "second": ("A análise de uma discretização começa pela descrição do domínio "
                   "e das regras que determinam seus elementos. Em seguida, "
                   "registram-se as medidas calculadas e os pressupostos adotados. "
                   "Uma comparação só é interpretável quando especifica as "
                   "condições de obtenção de cada resultado e distingue o que "
                   "foi demonstrado do que permanece como hipótese. A apresentação "
                   "dos dados deve permitir que outras pessoas refaçam as "
                   "operações sem depender de conhecimento não documentado."),
        "author_note": "Trechos originais produzidos somente para ensaio de normalização; não constituem citações bibliográficas de terceiros.",
        "source_tail": "(Texto demonstrativo de autoria própria, 2026).",
        "foot_1": "Esta é uma nota explicativa de teste. A numeração e o corpo da nota devem permanecer junto ao rodapé da página.",
        "foot_2": "As contagens apresentadas são ilustrativas e não devem ser utilizadas como resultados de uma pesquisa empírica.",
        "foot_3": "Uma terceira nota permite inspecionar a continuidade da numeração e a formatação do separador.",
        "closing": "Esse conjunto mostra como a apresentação tipográfica diferencia a citação longa do corpo do texto e como as notas complementam a explicação.",
        "short": "Uma malha reproduzível exige conectividade e parâmetros documentados.",
        "short_intro": "Uma citação direta curta, produzida para este exemplo, permanece no parágrafo: ",
    },
    "en": {
        "heading": "Direct quotations and footnotes",
        "intro": "The two blocks below demonstrate long quotations with a left indent, reduced font size and single spacing. Both are original sample passages rather than excerpts from published works.",
        "first": ("A computational mesh represents a continuous domain with a finite "
                  "collection of connected elements. Each element has a position "
                  "in the domain and topological relations with its neighbors. "
                  "Representation quality depends not only on the number of cells "
                  "but also on explicitly defined connections and consistent "
                  "geometric data. To make a comparison reproducible, the "
                  "input, construction criteria and counting procedure must "
                  "be preserved."),
        "between": "The next block demonstrates a descriptive attribution placed after the excerpt. It refers exclusively to this original sample text.",
        "second": ("The analysis of a discretization begins by describing the domain "
                   "and the rules that determine its elements. The calculated "
                   "measures and assumptions are then recorded. A comparison "
                   "can only be interpreted when it specifies how each result "
                   "was obtained and distinguishes established findings from "
                   "open hypotheses. Data presentation should allow other "
                   "researchers to repeat the computations without relying "
                   "on undocumented knowledge."),
        "author_note": "Original passages written exclusively for typesetting verification; they are not quotations from external publications.",
        "source_tail": "(Original demonstration passage, 2026).",
        "foot_1": "This explanatory test footnote must remain at the foot of the page with its numbering and typographic separator.",
        "foot_2": "The reported counts are illustrative rather than empirical research findings.",
        "foot_3": "A third note allows reviewers to inspect numbering continuity and separator formatting.",
        "closing": "These examples also show the typographic distinction between long quotations and running text, while footnotes supplement the analysis.",
        "short": "A reproducible mesh requires documented connectivity and parameters.",
        "short_intro": "A short direct quotation written for this example remains inline: ",
    },
    "es": {
        "heading": "Citas directas y notas a pie de página",
        "intro": "Los dos bloques siguientes ejemplifican citas extensas con sangría izquierda, letra reducida e interlineado sencillo. Ambos textos son originales de demostración y no reproducen obras publicadas.",
        "first": ("Una malla computacional representa un dominio continuo mediante "
                  "una colección finita de elementos conectados. Cada elemento "
                  "ocupa una posición en el dominio y mantiene relaciones "
                  "topológicas con sus vecinos. La calidad de la representación "
                  "depende no solo del número de celdas, sino también de la "
                  "definición explícita de sus conexiones y la coherencia "
                  "de los datos geométricos. Para garantizar la reproducibilidad, "
                  "deben conservarse las entradas, los criterios constructivos "
                  "y el procedimiento de conteo."),
        "between": "El segundo bloque presenta una identificación descriptiva al final del fragmento; se refiere solamente al texto original de este ejemplo.",
        "second": ("El análisis de una discretización comienza con la descripción "
                   "del dominio y las reglas que determinan sus elementos. "
                   "Después se registran las magnitudes calculadas y las "
                   "hipótesis adoptadas. Una comparación solo puede interpretarse "
                   "cuando se explicitan las condiciones de obtención de cada "
                   "resultado y se distingue entre lo demostrado y lo supuesto. "
                   "La presentación debe permitir reproducir las operaciones "
                   "sin conocimientos que no estén documentados."),
        "author_note": "Fragmentos originales escritos para comprobar la composición; no son citas de publicaciones ajenas.",
        "source_tail": "(Texto demostrativo de elaboración propia, 2026).",
        "foot_1": "Esta nota explicativa de prueba debe aparecer a pie de página con su numeración y separador tipográfico.",
        "foot_2": "Los conteos mostrados son ilustrativos y no constituyen resultados de investigación empírica.",
        "foot_3": "Una tercera nota permite revisar la continuidad de numeración y el formato del separador.",
        "closing": "Los ejemplos también permiten distinguir tipográficamente las citas extensas del texto normal y muestran el uso complementario de las notas.",
        "short": "Una malla reproducible requiere conectividad y parámetros documentados.",
        "short_intro": "Una cita directa breve creada para este ejemplo permanece en el párrafo: ",
    },
    "fr": {
        "heading": "Citations directes et notes de bas de page",
        "intro": "Les deux blocs suivants illustrent des citations longues avec retrait à gauche, caractères réduits et interligne simple. Ces passages originaux servent uniquement à la démonstration et ne reproduisent pas une publication.",
        "first": ("Un maillage informatique représente un domaine continu au moyen "
                  "d'un ensemble fini d'éléments connectés. Chaque élément "
                  "occupe une position dans le domaine et entretient des "
                  "relations topologiques avec ses voisins. La qualité de "
                  "la représentation dépend non seulement du nombre de "
                  "cellules, mais aussi de la définition explicite des "
                  "connexions et de la cohérence des données géométriques. "
                  "Pour rendre la comparaison reproductible, il faut "
                  "conserver les entrées, les critères de construction "
                  "et la méthode de dénombrement."),
        "between": "Le second bloc montre une attribution descriptive placée après l'extrait et renvoyant exclusivement à ce texte original.",
        "second": ("L'analyse d'une discrétisation commence par la description "
                   "du domaine et des règles qui déterminent ses éléments. "
                   "On consigne ensuite les mesures calculées et les "
                   "hypothèses retenues. Une comparaison n'est interprétable "
                   "que si les conditions d'obtention de chaque résultat "
                   "sont explicites et si les faits démontrés se distinguent "
                   "des hypothèses. La présentation doit permettre de "
                   "reproduire les opérations sans connaissances implicites."),
        "author_note": "Passages originaux créés uniquement pour vérifier la mise en page; ils ne proviennent pas de publications tierces.",
        "source_tail": "(Texte de démonstration original, 2026).",
        "foot_1": "Cette note explicative de test doit figurer en bas de page, avec sa numérotation et son filet séparateur.",
        "foot_2": "Les dénombrements présentés sont illustratifs et ne constituent pas des résultats de recherche empirique.",
        "foot_3": "Une troisième note permet de contrôler la continuité de numérotation et la typographie du séparateur.",
        "closing": "Ces exemples permettent de distinguer les citations longues du texte courant et montrent comment les notes complètent l'analyse.",
        "short": "Un maillage reproductible exige des connexions et des paramètres documentés.",
        "short_intro": "Une courte citation directe créée pour cet exemple reste dans le paragraphe : ",
    },
}


def quotation_section(locale: str) -> str:
    """Build two actual long-citation environments and three distinct footnotes."""
    data = QUOTE_EXAMPLES[locale]
    return "\n".join([
        rf"\section{{{data['heading']}}}",
        data["intro"] + rf"\footnote{{{data['author_note']}}}",
        r"\begin{citacao}",
        data["first"],
        r"\end{citacao}",
        data["between"] + rf"\footnote{{{data['foot_1']}}}",
        r"\begin{citacao}",
        data["second"] + " " + data["source_tail"],
        r"\end{citacao}",
        data["short_intro"] + "``" + data["short"] + "''"
        + rf"\footnote{{{data['foot_2']}}}",
        data["closing"] + rf"\footnote{{{data['foot_3']}}}",
    ]) + "\n"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one replacement, found {count}: {old[:60]}")
    return text.replace(old, new, 1)


def rewrite_support(entry: dict, loc: str, d: dict) -> None:
    """Replace all test-only front matter files with readable authored prose."""
    for raw in entry["support_sources"]:
        p = ROOT / raw
        name = p.name
        if "-primary.tex" in name or "-secondary.tex" in name:
            primary = "-primary.tex" in name
            language = loc if primary else ("en" if loc == "pt" else "pt")
            t = STRINGS[language]
            content = t["summary"] + "\n" + (
                rf"\ufcSummaryKeywords{{{t['keywords']}.}}" + "\n"
            )
        elif "-ack.tex" in name:
            content = d["ack"] + "\n"
        elif "-errata.tex" in name:
            content = d["errata"] + "\n"
        elif "-abbreviations.tex" in name:
            content = (r"\begin{ufcdefinitionlist}" + "\n"
                       + rf"\ufcListEntry{{UFC}}{{{d['institution']}}}" + "\n"
                       + rf"\ufcListEntry{{PDF}}{{Portable Document Format}}" + "\n"
                       + r"\end{ufcdefinitionlist}" + "\n")
        elif "-symbols.tex" in name:
            content = (r"\begin{ufcdefinitionlist}" + "\n"
                       + rf"\ufcListEntry{{$V$}}{{{d['symbol']}}}" + "\n"
                       + r"\end{ufcdefinitionlist}" + "\n")
        elif "-dedication.tex" in name:
            content = d["dedication"] + "\n"
        elif "-epigraph.tex" in name:
            content = d["epigraph"] + "\n"
        else:
            # The base authoring layer supplies only these six file roles.
            raise RuntimeError(f"Unrecognized supplementary text: {p}")
        p.write_text(content, encoding="utf-8")


def readable_source(source: str, profile: str, loc: str) -> str:
    """Rewrite presentation only; keep class API calls and mathematical study."""
    d = {**STRINGS[loc], **DIFFERENT_CAPTIONS[loc]}
    # The R4 module imports helpers relative to its own source directory.
    if str(R4.parent) not in sys.path:
        sys.path.insert(0, str(R4.parent))
    original_prose = runpy.run_path(str(R4))["PROSE"][loc]
    project = profile.endswith("research-project")
    anonymous = profile == "anonymized-research-project"
    title = d["project_title"] if project else d["title"]
    source = replace_once(source, "coat-of-arms=false",
                          f"coat-of-arms={'false' if anonymous or profile == 'scientific-article' else 'true'}",
                          "coat-of-arms")
    source = replace_once(source, "print-mode=double-sided" if profile in {
        "masters-thesis", "doctoral-thesis", "anonymized-research-project"
    } else "print-mode=single-sided", "print-mode=single-sided", "print-mode")
    source = replace_once(source, "author={Integrated Test Author}",
                          f"author={{{d['author']}}}", "author")
    source = replace_once(source, "title={Integrated Multilingual Document}",
                          f"title={{{title}}}", "title")
    source = source.replace("article-author-note={Synthetic Test Author Note}",
                            f"article-author-note={{{d['article_note']}}}")
    source = source.replace("advisor={Integrated Advisor}",
                            "advisor={" + NAMES["advisor"] + "}")
    source = source.replace("coadvisor={Integrated Coadvisor}",
                            "coadvisor={" + NAMES["coadvisor"] + "}")
    source = re.sub(r"examiner-(\d+)={(?:Integrated Examiner \d+)}",
                    lambda m: f"examiner-{m[1]}={{{NAMES['examiners'][int(m[1])]}}}", source)
    source = re.sub(r"examiner-(\d+)-institution={(?:Integrated Institution \d+)}",
                    lambda m: f"examiner-{m[1]}-institution={{{d['institution']}}}", source)
    # Both advisors must have their institutions on the approval page.
    # These are existing public metadata keys, not new class behavior.
    if profile in {"undergraduate-capstone", "specialization-capstone",
                   "masters-thesis", "doctoral-thesis"}:
        for role in ("advisor", "coadvisor"):
            metadata = role + "={" + NAMES[role] + "},"
            replacement = metadata + "\n  " + role + "-institution={" + d["institution"] + "},"
            source = replace_once(source, metadata, replacement,
                                  role + "-institution")
    source = source.replace("SYNTHETIC-ANON-001", "REVIEW-PROPOSAL-001")

    simple = {
        "INTEGRATED-SECTION": "introduction",
        "R4-METHOD": "methods", "R4-SUBSECTION": "subsection",
        "R4-SUBSUBSECTION": "subsubsection",
        "R4-PARAGRAPH": "paragraph", "R4-SUBPARAGRAPH": "subparagraph",
        "R4-RESULTS": "results", "R4-IMPLEMENTATION": "implementation",
        "R4-DISCUSSION": "discussion",
        "INTEGRATED-APPENDIX": "appendix", "INTEGRATED-ANNEX": "annex",
        "R4-FIGURE": "figure", "R4-CHART": "chart",
        "R4-TEXTTABLE": "texttable", "R4SHORT": "shorttable",
        "R4LONG": "longtable", "R4NATIVE": "nativetable",
        "R4-INLINE-CODE": "inlinecode", "R4-EXTERNAL-CODE": "externalcode",
        "R4-ALGORITHM": "algorithm",
        "INTEGRATED-OBJECT": "introfigure", "INTEGRATED-TABLE": "introtable",
        "INTEGRATED-CHART": "introchart", "INTEGRATED-TEXTTABLE": "introtexttable",
        "INTEGRATED-TERM": "term", "INTEGRATED-DEFINITION": "definition",
        "INTEGRATED-LETTER": "letter", "INTEGRATED-NESTED-LIST": "nested",
        "INTEGRATED-DASH": "dash",
    }
    for token, key in simple.items():
        source = source.replace(token + "-" + loc.upper(), d[key])
    # Preserve nested-list punctuation while using natural prose.
    source = source.replace("INTEGRATED-NESTED-LIST:", d["nested"])
    source = source.replace("R4-FOOTNOTE synthetic and nonpersonal evidence.",
                            d["footnote"])
    source = source.replace("R4-LONGSOURCE-" + loc.upper(), d["source"])
    source = source.replace("R4LONGHEADER", d["header_case"])
    source = source.replace("R4LONGVALUE", d["header_value"])
    source = source.replace("R4NATIVEHEADER", d["header_case"])
    source = source.replace("R4NATIVEVALUE", d["header_value"])
    source = re.sub(r"R4LONGROW(\d+)",
                    lambda m: f"{d['row_case']} {int(m[1])}", source)
    source = re.sub(r"R4NATIVEROW(\d+)",
                    lambda m: f"{d['native_case']} {int(m[1])}", source)
    source = source.replace("long numeric observations", "")
    source = source.replace("source caption", "")
    source = source.replace("See synthetic sources", d["citation"])
    source = source.replace("Synthetic original", d["source"])
    source = source.replace("Synthetic object note", d["note"])
    source = source.replace(
        "Equation~\\ref{eq:r4-sum} is an artificial reproducibility marker.",
        d["equation_note"] + " " + EQUATION_REFERENCE[loc],
    )

    for flag in ("PROJECT", "ANON"):
        for value in ("TRUE", "FALSE"):
            old = f"INTEGRATED-{flag}-{value}-{loc.upper()}"
            key = (("project_true" if value == "TRUE" else "project_false")
                   if flag == "PROJECT" else
                   ("anon_true" if value == "TRUE" else "anon_false"))
            source = source.replace(old, d[key])
    source = source.replace(
        "INTEGRATED-MANUSCRIPT-" + loc.upper() + "-" + profile.replace("-", "").upper(),
        d["intro_text"]
    )
    source = source.replace("keyword-" + loc + "-article.", d["keywords"] + ".")
    companion = "en" if loc == "pt" else "pt"
    source = source.replace("keyword-" + companion + "-article.",
                            STRINGS[companion]["keywords"] + ".")
    source = source.replace(
        "INTEGRATED-ARTICLE-PRIMARY-" + loc.upper(), d["summary"])
    source = source.replace(
        "INTEGRATED-ARTICLE-COMPANION-" + companion.upper(),
        STRINGS[companion]["summary"])
    source = source.replace(
        r"\newglossaryentry{integratedterm}{name={integrated term},description={synthetic term for locale testing}}",
        rf"\newglossaryentry{{integratedterm}}{{name={{{d['term']}}},description={{{d['definition']}}}}}")
    source = source.replace(r"\index{integrated term}", rf"\index{{{d['term']}}}")
    # Glossaries prints its own terminal full stop; the entry description
    # must not include one, otherwise the PDF contains duplicate punctuation.
    source = source.replace(
        "description={" + d["definition"] + "}",
        "description={" + d["definition"].rstrip(".") + "}",
        1)


    for old, new_text in zip(original_prose, NEW_PROSE[loc]):
        if old not in source:
            raise RuntimeError(f"Original artificial prose not found: {profile}/{loc}")
        source = source.replace(old, new_text)

    # Remove the six cloned synthetic sections; retain three distinct cases.
    replicated = (rf"\\subsection{{R4-REPLICATION-{loc.upper()}-1}}"
                  rf".*?(?=\\section{{{d['discussion']}}})")
    replacement = "\n".join(
        rf"\subsection{{{d['replication']} {i}}}" + "\n" + d["replication_text"]
        for i in (1, 2, 3)
    ) + "\n"
    source, n = re.subn(replicated, lambda _: replacement, source, flags=re.S)
    if n != 1:
        raise RuntimeError(f"Failed to replace repetitive sections: {profile}/{loc}, n={n}")

    # Replace rectangle-only placeholder figures with generated actual vector art.
    image_root = "artifacts/canonical-mesh-study"
    source = source.replace(r"\centering\rule{3cm}{1cm}",
                            rf"\centering\includegraphics[width=.86\linewidth]{{{image_root}/uniform_quads.pdf}}")
    source = source.replace(r"\centering\rule{6cm}{2cm}",
                            rf"\centering\includegraphics[width=.86\linewidth]{{{image_root}/uniform_triangles.pdf}}")
    source = source.replace(r"\centering\rule{5cm}{1.5cm}",
                            rf"\centering\includegraphics[width=.86\linewidth]{{{image_root}/anisotropic_quads.pdf}}")

    # UFC formatting relates the title/source width to the actual illustration
    # or table; avoid a two-number table with a tiny intrinsic width.
    table_re = r"\\begin\{tabular\}\{rr\}.*?\\end\{tabular\}"
    table_body = "\n".join([
        r"\begin{tabular*}{.86\linewidth}{@{\extracolsep{\fill}}lr}",
        rf"{d['header_case']} & {d['header_value']} \\",
        rf"{d['row_case']} 1 & 3 \\",
        rf"{d['row_case']} 2 & 4 \\",
        r"\end{tabular*}",
    ])
    source, table_count = re.subn(table_re, lambda _: table_body,
                                   source, flags=re.S)
    if table_count != 1:
        raise RuntimeError(f"Expected exactly one short table: {profile}/{loc}; "
                           f"found {table_count}")

    # Text tables (quadros) must contain textual information, not placeholder
    # mesh graphics. Give both their captions and source a real readable width.
    quadro_re = (
        r"(\\legend\{quadro\}\{[^{}]*\}\s*"
        r"\\ufcSource\{[^{}]*\}\s*"
        r"\\begin\{ufcobject\}\[here\]\s*)"
        r"\\centering\\includegraphics\[[^]]+\]\{[^{}]*\}"
    )
    quadro_body = "\n".join([
        r"\centering",
        r"\begin{tabular*}{.86\linewidth}{@{\extracolsep{\fill}}ll}",
        rf"{d['header_case']} & {d['header_value']} \\",
        rf"{d['row_case']} 1 & {d['subsection']} \\",
        rf"{d['row_case']} 2 & {d['results']} \\",
        r"\end{tabular*}",
    ])
    source, quadro_count = re.subn(
        quadro_re, lambda m: m.group(1) + quadro_body, source, flags=re.S)
    expected_quadro = 2 if profile in {
        "undergraduate-capstone", "specialization-capstone",
        "masters-thesis", "doctoral-thesis"
    } else 0
    if quadro_count != expected_quadro:
        raise RuntimeError(f"Expected {expected_quadro} text tables: "
                           f"{profile}/{loc}; found {quadro_count}")

    source = source.replace("R4-REPLICATION-" + loc.upper(), d["replication"])

    # The integrated article and appendix/annex also contain abbreviated labels.
    source = re.sub(r"INTEGRATED-[A-Z0-9_-]+", "", source)
    source = re.sub(r"R5-[A-Z0-9_-]+", "", source)
    source = re.sub(r"R4-[A-Z0-9_-]+", "", source)

    # Replace punctuation duplicated by the original engineering sentinels.
    source = re.sub(r"(?<!\.)\.\.(?!\.)", ".", source)

    # The introductory quotation tests deliberately use the inherited
    # public long-quote environment with a 4 cm indent and single spacing.
    first_results = rf"\section{{{d['results']}}}"
    source = replace_once(
        source, first_results, quotation_section(loc) + first_results,
        "long-quotation section")

    # Academic nature and front matter remain the class's own implementations.
    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=LOCALES)
    args = parser.parse_args()
    locales = [args.locale] if args.locale else LOCALES
    for loc in locales:
        subprocess.run([sys.executable, str(R4), "--locale", loc],
                       check=True, cwd=ROOT)
        origin = BASE / loc
        destination = OUT / loc
        destination.mkdir(parents=True, exist_ok=True)
        idx = json.loads((origin / "source-index.json").read_text(encoding="utf-8"))
        entries = []
        for item in idx["entries"]:
            profile = item["profile"]
            rewrite_support(item, loc, STRINGS[loc])
            original = (ROOT / item["source"]).read_text(encoding="utf-8")
            source = readable_source(original, profile, loc)
            name = f"review-{profile}-{loc}"
            tex = destination / (name + ".tex")
            tex.write_text(source, encoding="utf-8")
            entries.append({
                "profile": profile,
                "locale": loc,
                "source": str(tex.relative_to(ROOT)),
                "source_sha256": hashlib.sha256(tex.read_bytes()).hexdigest(),
                "support_sources": item["support_sources"],
                "kind": "human_readable_full_manuscript",
                "human_approval": "PENDING",
            })
        if len(entries) != 7:
            raise RuntimeError("Incomplete seven-document matrix")
        (destination / "review-sources.json").write_text(
            json.dumps({"locale": loc, "entries": entries,
                        "expected_pdf_count": 7,
                        "human_approval": "PENDING"}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        print(f"READABLE-REVIEW-SOURCES locale={loc} sources={len(entries)} status=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

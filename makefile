201023:
	pandoc reunions/src/PREP_Reunion201023.md -o reunions/PREP_Reunion201023.pdf --pdf-engine=pdflatex
	pandoc reunions/src/CR_Reunion201023.md -o reunions/reunion201023.pdf --pdf-engine=pdflatex


# Règle par défaut : génère tous les PDFs
all: clean 201023

# Règle pour nettoyer les fichiers générés
clean:
	rm -f reunions/*.pdf

# Renoie une liste de chaque chaîne de caractères présent dans le fichier ayant comme séparateur l'espace et le retour à la ligne

def fichierReader(nomFichier):
    liste = []
    try:
        with open(nomFichier, 'r') as f:
            for line in f:
                liste += line.strip('\n').split(' ')
            return liste
        
    except FileNotFoundError:
        print("Le fichier n'existe pas")
        return None

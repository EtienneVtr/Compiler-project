from sys import stderr
from token_pcl import Token

error_types = ["(Erreur Lexicale) ", "(Erreur Syntaxique) "]
def print_err(type:int==None, tok:Token, attendu:str, *args, **kwargs):
    if type==1:
        print(f"ligne:{tok.line}", error_types[type], f"'{attendu}' attendu, '{tok.value}' reçu.", *args, file=stderr, **kwargs)
    elif type==0:
        print(error_types[type], *args, file=stderr, **kwargs)
    else:
        print(*args, file=stderr, **kwargs)


def levenshtein_distance(s1, s2):
    """
    Calcule la distance de Levenshtein entre deux chaînes de caractères.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if not s1:
        return len(s2)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Calcul de l'insertion, de la suppression et de la substitution
            # des caractères
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            # On prend le minimum de ces trois opérations
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    # On retourne la distance de Levenshtein
    return previous_row[-1]
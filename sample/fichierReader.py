# Liste des mots-clés
keywords = [
    'access', 'and', 'begin', 'else', 'elsif', 'end',
    'false', 'for', 'function', 'if', 'in', 'is',
    'loop', 'new', 'not', 'null', 'or', 'out',
    'procedure', 'record', 'rem', 'return', 'reverse', 'then',
    'true', 'type', 'use', 'while', 'with'
]

# Liste des opérateurs
operators = [
    'or', 'or else', 'and', 'and then', 'not',
    '=', '/=', '>', '>=', '<', '<=', '+', '-',
    '*', '/', 'rem', '--', '.', ';',':=','(',')',','
]


# Renoie une liste de chaque chaîne de caractères présent dans le fichier ayant comme séparateur l'espace et le retour à la ligne

def fichierReader(nomFichier = "data/codeCanAda"):
    tokens = []
    stack = []
    try:
        with open(nomFichier, 'r') as f:
            for line in f:
                for i in line.strip('\n').strip('\t'):
                    if i == " ":
                        tokens.append("".join(stack))
                        stack = []
                    elif i in operators:
                        if stack != []:
                            tokens.append("".join(stack))
                        tokens.append(i)
                        stack = []
                    else:
                        stack.append(i)
                if stack != []:
                    tokens.append("".join(stack))
                stack = []
            print(tokens)
            return tokens
    except FileNotFoundError:
        print("Le fichier n'existe pas")
        return None

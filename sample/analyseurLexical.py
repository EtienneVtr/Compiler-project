import re

# Définition de la taille max d'un identificateur
MAX_IDENT_SIZE = 40

# Définition de la taille max d'une constante
MAX_CONST_SIZE = 10

# Définition du code des identificateurs et constantes :
STR_CODE = 202
CONST_CODE = 200

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
    '=', '/=', '>', '>=', '<', '<=', '+', '-',
    '*', '/', '--', '.', ';',':=','(',')',',',':'
]

codes = dict()  # Dictionnaire des codes des mots-clés et opérateurs
for i in range(len(operators)):
    codes[operators[i]] = i+1
for i in range(len(keywords)):
    codes[keywords[i]] = i+101

class Token:
    """
    Représente un Token par sa valeur et son code (cf. cours p.4-5)
    0: unite lexicale generic
    1-99: operateurs
    100-: keywords

    How to use:
    >>> t = Token('and')
    >>> t
    Token(102, 'and')
    >>> t == 102
    True
    >>> t == 'and'
    True
    >>> t == 'or'
    False
    >>> t == Token('or')
    False
    >>> print(t)
    (102, 'and')
    >>> t != 102
    False
    >>> t != 'and'
    False
    >>> t != 'or'
    True
    >>> t != Token('or')
    True
    """
    def __init__(self, value:str, line:int=None, code:int=None) -> None:
        """
        Initialise un Tokenœ

        Args:
            value (str): la valeur du Token
            code (int, optional): le code du Token. Si code==None, utilise le code défini dans fichierReader.py.
        """
        self.value = value
        self.line = line
        if code is not None:
            self.code = code
        else:
            if value.startswith('"') and value.endswith('"'):
                self.code = STR_CODE
            else:
                self.code = codes.get(value, 0)
                if self.code == 0:
                    if self.value.isdigit() and len(self.value) <= MAX_CONST_SIZE:
                        self.code = CONST_CODE
                    else :
                        print("Erreur lexicale à la ligne", self.line, ":", self.value)

    
    def __str__(self) -> str:
        if self.code == CONST_CODE :
            return f"('const', '{self.value}')"
        elif self.code == STR_CODE :
            return f"('str', '{self.value}')"
        elif self.code >= 300:
            return f"('{self.value}', {self.code-300})"
        else :
            return f"({self.code}, '{self.value}')"
    
    def __repr__(self) -> str:
        return "Token" + self.__str__()
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Token):
            return self.code == other.code and self.value == other.value
        if isinstance(other, int):
            return self.code == other
        if isinstance(other, str):
            return self.value == other
        return False
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
        

def analyseurLexical(nomFichier:str = "../data/hw.ada") -> (list[Token],list[str]):
    """
    Return une liste des Tokens luent dans un fichiera
    """
    tokens = []
    stack = ""
    stash = ""
    automate = None
    lexique = []
    def tok_append(id_line:int=None)->None:
        nonlocal stack  # Tell the function to use the variable defined in the parent scope
        if not stack:
            return
        if re.match("^[a-zA-Z]([a-zA-Z0-9_])*$", stack) and len(stack) <= MAX_IDENT_SIZE and stack not in keywords:
# Si stack contient un ident, on rentre ce dernier dans la table des symboles et on crée le token de la façon suivante : 
# Token("ident", id_line, indice de l'ident dans la table des symboles)
# On reconnaît un ident ssi il correspond au regex, qu'il n'est pas trop long et qu'il n'est ni dans les mots clés, ni dans les symboles déjà reconnus
# ATTENTION : Les keywords sont entre 0 et 99, les opérateurs enrte 100 et 199, les symboles auront pour code 300 et plus !!!
            for i in range(len(lexique)):
                if lexique[i]==stack:   # Si on trouve dans lexique on ajoute le code dans tokens
                    tokens.append(Token("ident", id_line, lexique.index(stack)+300))
                    stack = ""
                    return  # Sort de la fonction
            lexique.append(stack)   # Sinon on ajoute stack dans le lexique
            tokens.append(Token("ident", id_line, len(lexique)+299)) # len(lexique) + 300 - 1 car # car stack est le dernier elt de lexique
            stack = ""
            return  # Sort de la fonction
        tokens.append(Token(stack, id_line))    # Si pas IDENT
        stack = ""
    def zero(c:str, id_line:int=None)->None:
        nonlocal stack
        nonlocal stash
        nonlocal automate
        # print(f"0: '{c}'\t'{stack}'\t'{stash}'")
        if c in [op[0] for op in operators]:
            stash = stack
            tok_append(id_line)
            stack = c
            automate = one
            return
        if c in [' ', '\t', '\n']:
            tok_append(id_line)
            return
        if c == '"': # Si on reconnaît le début d'une chaîne de caractères, on va à l'état 2 de l'automate
            stack += c
            automate = two
            return
        stack += c
    def one(c:str, id_line:int=None)->None:
        nonlocal stack
        nonlocal stash
        nonlocal automate
        # print(f"1: {c}\t{stack}\t{stash}")
        if stack + c in [op[:len(stack)+1] for op in operators if len(op)>len(stack)]:
            stack += c
            return
        if stack in operators:
            tok_append(id_line)
            automate = zero
            zero(c,id_line)
            return
        tokens.pop()
        stack = stash + stack
        automate = zero
        zero(c,id_line)
        automate = zero
    def two(c: str, id_line:int=None)->None:
        nonlocal stack
        nonlocal stash
        nonlocal automate
        if c == '"': # Si on reconnaît la fin d'une chaîne de caractères, on ajoute tout ça à la suite des tokens
            stack += c
            tok_append(id_line)
            stack = ""
            automate = zero
        else:
            stack += c
    automate = zero
    with open(nomFichier, 'r') as f:
        id_line = 1
        for line in f:
            if '--' in line:
                line = line.split('--', 1)[0] # S'il y a un commentaire dans la ligne, on ignore toute la ligne à partir de --
            if not line.strip(): # Si, après suppression du commentaire, la ligne est vide, alors on passe à la ligne suivante
                continue

            for c in line:
                automate(c,id_line)
                
            id_line += 1
        tok_append(id_line-1)
        return (tokens,lexique)

if __name__=="__main__":
    try:
        (tokens,lexique) = analyseurLexical()
        print()
        for tok in tokens:
            print(tok)
        print()
        for i in range(len(lexique)):
            print(i, lexique[i])
    except Exception as e:
        print(e)

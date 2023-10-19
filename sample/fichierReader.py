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
    '*', '/', '--', '.', ';',':=','(',')',','
]

codes = dict()
for i in range(len(operators)):
    codes[operators[i]] = i+1
for i in range(len(keywords)):
    codes[keywords[i]] = i+101

class Token:
    """
    0: unite lexicale generic
    1-99: operateurs
    100-: keywords 
    """
    def __init__(self, value:str, code:int=None) -> None:
        self.value = value
        if code:
            self.code = code
        else:
            self.code = codes.get(value, 0)
    
    def __str__(self) -> str:
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
        

def fileReader(nomFichier:str = "data/hw.ada") -> list[Token]:
    """
    Renvoie une liste de chaque chaîne de caractères présent dans le fichier ayant comme séparateur l'espace et le retour à la ligne
    """
    tokens = []
    stack = ""
    stash = ""
    automate = None
    def tok_append()->None:
        nonlocal stack
        if not stack:
            return
        tokens.append(Token(stack))
        # print("\t\tAPPEND:", stack)
        stack = ""
    def zero(c:str)->None:
        nonlocal stack
        nonlocal stash
        nonlocal automate
        # print(f"0: '{c}'\t'{stack}'\t'{stash}'")
        if c in [op[0] for op in operators]:
            stash = stack
            tok_append()
            stack = c
            automate = one
            return
        if c in [' ', '\t', '\n']:
            tok_append()
            return
        stack += c
    def one(c:str)->None:
        nonlocal stack
        nonlocal stash
        nonlocal automate
        # print(f"1: {c}\t{stack}\t{stash}")
        if stack + c in [op[:len(stack)+1] for op in operators if len(op)>len(stack)]:
            stack += c
            return
        if stack in operators:
            tok_append()
            automate = zero
            zero(c)
            return
        tokens.pop()
        stack = stash + stack
        automate = zero
        zero(c)
        automate = zero
    automate = zero
    with open(nomFichier, 'r') as f:
        for line in f:
            for c in line:
                automate(c)
        tok_append()
        return tokens

if __name__=="__main__":
    try:
        tokens: list[Token] = fileReader()
        print()
        for tok in tokens:
            print(tok)
    except Exception as e:
        print(e)
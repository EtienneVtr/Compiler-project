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
        

def analyseurLexical(nomFichier:str = "data/hw.ada") -> list[Token]:
    """
    Return une liste des Tokens luent dans un fichier
    """
    tokens = []
    stack = ""
    stash = ""
    automate = None
    def tok_append()->None:
        nonlocal stack  # Tell the function to use the variable defined in the parent scope
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
        tokens: list[Token] = analyseurLexical()
        print()
        for tok in tokens:
            print(tok)
    except Exception as e:
        print(e)

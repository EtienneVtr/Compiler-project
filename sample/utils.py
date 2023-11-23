from sys import stderr
from token_pcl import Token

error_types = ["(Erreur Lexicale) ", "(Erreur Syntaxique) "]
def print_err(type:int==None, tok:Token, attendu:str, *args, **kwargs):
    if type==1:
        print(f"ligne:{tok.line}", error_types[type], f"'{attendu}' attendu, '{tok.value}' reçu", *args, file=stderr, **kwargs)
    if type==0:
        print(error_types[type], *args, file=stderr, **kwargs)
    else:
        print(*args, file=stderr, **kwargs)
from ast import AST
from token import Token
from grammairev2 import *

def analyseSyntaxique(tokens:list[Token]) -> AST:
    root = Node("FICHIER")
    FICHIER(tokens, root)
    print(root)
from ast import AST
from token_pcl import Token
from grammaire import *

def analyseSyntaxique(tokens:list[Token]) -> AST:
    root = Node("FICHIER")
    FICHIER(tokens, root)
    print(root)
# pour IDENT

from token_pcl import Token
from ast import AST
from utils import *
from analyseurLexical import *

def consume(tokens:list[Token], code:int, func:callable=Token.__ne__) -> Token:
    tok  = tokens.pop(0)
    if func(tok, code):
        print_err(1, tok, "with")
    return tok

def FICHIER(tokens: list[Token], node:Node) -> None:
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 12)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, )

    node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)

    consume(tokens, 112)
    
    tok = tokens[0] # On regarde le prochain token
    while tok.code != 103: # Tant qu'on a pas un 'begin'
        DECL(tokens, node.add_child(Node("DECL")))  # On rentre dans la règle DECL
        tok = tokens[0]
    tokens.pop(0)


def DECL(tokens:list[Token], node:Node) -> None:
    pass


def D(tokens:list[Token], node:Node) -> None:
    consume


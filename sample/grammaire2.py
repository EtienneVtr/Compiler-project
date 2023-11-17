# pour IDENT

from token_pcl import Token
from ast import AST
from utils import *
from analyseurLexical import *


# # Définition du code des identificateurs et constantes :
# STR_CODE = 202
# CONST_CODE = 200

# # Liste des mots-clés
# keywords = [
#     101 'access', 102 'and', 103 'begin', 104 'else', 105 'elsif', 106 'end',
#     107 'false', 108'for', 109'function', 110'if', 111'in', 112'is',
#     113'loop', 114'new', 115'not', 116'null', 117'or', 118'out',
#     119'procedure', 120'record', 121'rem', 122'return', 123'reverse', 124'then',
#     125'true', 126'type', 127'use', 128'while', 129'with'
# ]

# # Liste des opérateurs
# operators = [
#     1'=', 2'/=', 3'>', 4'>=', 5'<', 6'<=', 7'+', 8'-',
#     9'*', 10'/', 11'--', 12'.', 13';',14':=',15'(',16')',17',',18':'
# ]

# codes = dict()  # Dictionnaire des codes des mots-clés et opérateurs
# for i in range(len(operators)):
#     codes[operators[i]] = i+1
# for i in range(len(keywords)):
#     codes[keywords[i]] = i+101


def consume(tokens:list[Token], code:int, func:callable=Token.__ne__) -> Token:
    tok  = tokens.pop(0)
    if func(tok, code):
        print_err(1, tok, "with")
    return tok

# fICHIER :	'with Ada.Text_IO ; use Ada.Text_IO ;\nprocedure' IDENT 'is' dECL*'\nbegin' iNSTR+ 'end' iDENTINTER ';';
def FICHIER(tokens: list[Token], node:Node) -> None:
    consume(tokens, 129)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 12)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 13)
    consume(tokens, 129)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 12)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 13)
    consume(tokens, 119)
    node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 112)

    tok = tokens[0] # On regarde le prochain token
    while tok.code != 103: # Tant qu'on a pas un 'begin'
        DECL(tokens, node.add_child(Node("DECL")))  # On rentre dans la règle DECL
        tok = tokens[0]
    tokens.pop(0)
    INSTR(tokens, node.add_child(Node("INSTR"))) # On rentre dans la règle INSTR+
    tok = tokens[0] # On regarde le prochain token
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR"))) # On rentre dans la règle INSTR+
        tok = tokens[0]
    tokens.pop(0)

    consume(tokens, 300, Token.__lt__)
    consume(tokens, 13)

# dECL :	'type' IDENT ('is' d)? ';' | pROCEDURE | fUNC;
def DECL(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    if tok.code == 126:
        consume(tokens, 126)
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
        tok = tokens[0]
        if tok.code == 112:
            consume(tokens, 112)
            D(tokens, node.add_child(Node("D")))
    elif tok.code == 119:
        PROCEDURE(tokens, node.add_child(Node("PROCEDURE")))
    elif tok.code == 120:
        FUNC(tokens, node.add_child(Node("FUNC")))
    else:
        print_err(1, tok, "type, procedure or function")

# d : 'access' IDENT | 'record' cHAMPS+ 'end record ;';
def D(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    if tok.code == 101:
        consume(tokens, 101)
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    elif tok.code == 121:
        consume(tokens, 121)
        tok = tokens[0]
        CHAMPS(tokens, node.add_child(Node("CHAMPS")))
        while tok.code != 106:
            CHAMPS(tokens, node.add_child(Node("CHAMPS")))
            tok = tokens[0]
        tokens.pop(0)
        consume(tokens, 120)
        consume(tokens, 13)
    else:
        print_err(1, tok, "access or record")

# pROCEDURE :	'procedure' IDENT pARAMS? 'is' dECL*'\nbegin' iNSTR+ 'end' IDENT? ';';
def PROCEDURE(tokens:list[Token], node:Node) -> None:
    consume(tokens, 119)
    node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    tok = tokens[0]
    if tok.code == 108:
        PARAMS(tokens, node.add_child(Node("PARAMS")))
    consume(tokens, 112)
    tok = tokens[0]
    while tok.code != 103:
        DECL(tokens, node.add_child(Node("DECL")))
        tok = tokens[0]
    tokens.pop(0)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    tokens.pop(0)
    tok = tokens[0]
    if tok.code == 300:
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 13)

# fUNC :	'function' IDENT pARAMS? 'return' tYPE 'is' dECL*'\nbegin' iNSTR+ 'end' IDENT?';';
def FUNC(tokens:list[Token], node:Node) -> None:
    consume(tokens, 109)
    node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    tok = tokens[0]
    if tok.code == 108:
        PARAMS(tokens, node.add_child(Node("PARAMS")))
    consume(tokens, 127)
    TYPE(tokens, node.add_child(Node("TYPE")))
    consume(tokens, 112)
    tok = tokens[0]
    while tok.code != 103:
        DECL(tokens, node.add_child(Node("DECL")))
        tok = tokens[0]
    tokens.pop(0)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    tokens.pop(0)
    tok = tokens[0]
    if tok.code == 300:
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 13)


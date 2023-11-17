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
        consume(tokens, 106)
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
    consume(tokens, 103)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    consume(tokens, 106)
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
    consume(tokens, 122)
    TYPE(tokens, node.add_child(Node("TYPE")))
    consume(tokens, 112)
    tok = tokens[0]
    while tok.code != 103:
        DECL(tokens, node.add_child(Node("DECL")))
        tok = tokens[0]
    consume(tokens, 103)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    consume(tokens, 106)
    if tok.code == 300:
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 13)

# eXPR :	tERM (oP tERM)*;
def EXPR(tokens:list[Token], node:Node) -> None:
    TERM(tokens, node.add_child(Node("TERM")))
    tok = tokens[0]
    while tok.code in [1,2,3,4,5,6,7,8,9,10,102,117,121]:
        OP(tokens, node.add_child(Node("OP")))
        TERM(tokens, node.add_child(Node("TERM")))
        tok = tokens[0]

# tERM :	ENTIER | CHAR vALEXPR |	'true' | 'false' | 'null' | 'not' eXPR | '-' eXPR | IDENT '(' eXPR vIRGULEEXPRETOILE ')' | 'new' IDENT ;
def TERM(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    if tok.code == 200:
        node.add_child("Entier: " + consume(tokens, 200, Token.__lt__).value)
    elif tok.code == 202:
        CHAR(tokens, node.add_child(Node("CHAR")))
        if tok == 'val' # Temporaire en attendant ce que l'on fait avec val
            consume(tokens, 300, Token.__lt__)
            EXPR(tokens, node.add_child(Node("EXPR")))
    elif tok.code == 125:
        consume(tokens, 125)
    elif tok.code == 107:
        consume(tokens, 107)
    elif tok.code == 116:
        consume(tokens, 116)
    elif tok.code == 115:
        consume(tokens, 115)
        EXPR(tokens, node.add_child(Node("EXPR")))
    elif tok.code == 8:
        consume(tokens, 8)
        EXPR(tokens, node.add_child(Node("EXPR")))
    elif tok.code == 300:
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
        consume(tokens, 15)
        EXPR(tokens, node.add_child(Node("EXPR")))
        while tok.code == 17:
            consume(tokens, 17)
            EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 16)
    elif tok.code == 114:
        consume(tokens, 114)
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    else:
        print_err(1, tok, "entier, char, true, false, null, not, -, ident, new")

# iNSTR : IDENT hELP2 |	'return' eXPR? ';' |	bEGIN |	iF |	fOR |	wHILE |	ENTIER fIN |	CHAR VALEXPR fIN |	'true' fIN |	'false' fIN |	'null' fIN |	'not' EXPR fIN |	'moins' EXPR fIN |	'new' IDENT fIN;
def INSTR(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    if tok.code == 300:
        IDENT(tokens, node.add_child(Node("IDENT")))
        HELP2(tokens, node.add_child(Node("HELP2")))
    elif tok.code == 122:
        consume(tokens, 122)
        if tok.code in [200,202,107,116,115,8,300,114]:
            EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
    elif tok.code == 103:
        BEGIN(tokens, node.add_child(Node("BEGIN")))
    elif tok.code == 110:
        IF(tokens, node.add_child(Node("IF")))
    elif tok.code == 108:
        FOR(tokens, node.add_child(Node("FOR")))
    elif tok.code == 128:
        WHILE(tokens, node.add_child(Node("WHILE")))
    elif tok.code in [200, 125, 107, 116]:
        if tok.code == 200:
            node.add_child("Entier: " + consume(tokens, 200, Token.__lt__).value)
        elif tok.code == 125:
            consume(tokens, 125)
        elif tok.code == 107:
            consume(tokens, 107)
        elif tok.code == 116:
            consume(tokens, 116)
        FIN(tokens, node.add_child(Node("FIN")))
    elif tok.code in [115, 8]:
        if tok.code == 115:
            consume(tokens, 115)
        elif tok.code == 8:
            consume(tokens, 8)
        EXPR(tokens, node.add_child(Node("EXPR")))
        FIN(tokens, node.add_child(Node("FIN")))
    elif tok.code == 114:
        consume(tokens, 114)
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
        FIN(tokens, node.add_child(Node("FIN")))
    elif tok.code == 202:
        CHAR(tokens, node.add_child(Node("CHAR")))
        VALEXPR(tokens, node.add_child(Node("VALEXPR")))
        FIN(tokens, node.add_child(Node("FIN")))
    else:
        print_err(1, tok, "ident, return, begin, if, for, while, entier, char, true, false, null, not, -, new")
    
# fIN -> (oP tERM)* '.' IDENT ':=' EXPR ';';
def FIN(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    while tok.code in [1,2,3,4,5,6,7,8,9,10,102,117,121]:
        OP(tokens, node.add_child(Node("OP")))
        TERM(tokens, node.add_child(Node("TERM")))
        tok = tokens[0]
    consume(tokens, 12)
    node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 14)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 13)
    # Rajouter les erreurs

# hELP2 :	':=' eXPR ';' |	'(' eXPR hELP;
def HELP2(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    if tok.code == 14:
        consume(tokens, 14)
        EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
    elif tok.code == 15:
        consume(tokens, 15)
        EXPR(tokens, node.add_child(Node("EXPR")))
        HELP3(tokens, node.add_child(Node("HELP")))
    else:
        print_err(1, tok, ":= or (")

# hELP3 :	')' hELP |	',' eXPR (','eXPR)* ')' (oP tERM)* IDENT ':=' eXPR ';';
def HELP3(tokens:list[Token], node:Node) -> None:
    tok = tokens[0]
    if tok.code == 16:
        consume(tokens, 16)
        HELP(tokens, node.add_child(Node("HELP")))
    elif tok.code == 17:
        consume(tokens, 17)
        EXPR(tokens, node.add_child(Node("EXPR")))
        tok = tokens[0]
        while tok.code == 17:
            consume(tokens, 17)
            EXPR(tokens, node.add_child(Node("EXPR")))
            tok = tokens[0]
        consume(tokens, 16)
        tok = tokens[0]
        while tok.code in [1,2,3,4,5,6,7,8,9,10,102,117,121]:
            OP(tokens, node.add_child(Node("OP")))
            TERM(tokens, node.add_child(Node("TERM")))
            tok = tokens[0]
        node.add_child("Ident: " + consume(tokens, 300, Token.__lt__).value)
        consume(tokens, 14)
        EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
    else:
        print_err(1, tok, ") or ,") # or n'est pas expected c'est ou LOL

# hELP :	('(' eXPR ')')* ';' |	IDENT ':=' eXPR ';' |	(oP tERM)+ IDENT ':=' eXPR ';';
# A faire BITCH

# oP :	'and' 'then'? |	'or' 'else'? |	'=' |	'/=' |	'<' |	'<=' |	'>' |	'>=' |	'*' |	'/' |	'rem' |	'+' |	'-';
# L_Suivant_OP = [1,2,3,4,5,6,7,8,9,10,102,117,121]

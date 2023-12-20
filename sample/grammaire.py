# pour IDENT

from token_pcl import Token, codes, get_keyword
from AST import Node
from utils import *
# from analyseurLexical import *


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

VERBOSE = True

COUNT = 0
ERROR_COUNTER = 0
MAX_ERROR = 5

ROOT = None

def consume(tokens:list[Token], code:[int, tuple], func:callable=Token.__ne__) -> Token:
    global COUNT
    global ERROR_COUNTER
    tok  = tokens.pop(0)
    if VERBOSE:
        print((COUNT:=COUNT+1),"Consumming", tok, sep=' ')
    if func(tok, code):
        ERROR_COUNTER += 1
        print_err(1, tok, get_keyword(code))
        if isinstance(code, tuple):
            print("Did you mean", " or ".join(["'" + get_keyword(c) + "'" for c in code]), "?", end="\n\n")
            tokens.insert(0, tok)
        else:
            ## On va utiliser la distance de livenstein pour trouver le mot le plus proche
            if tok.__lt__(code):
                liste = get_keyword(code)
                for i in liste:
                    if levenshtein_distance(i, tok.value) <= 3:
                        print("Did you mean", "'" + i + "'", "?", end="\n\n")
                        tok = i
                        ######
                        #@@@@@  A FAIRE
                        #@@@@@  Matthias
                        ######  A FAIRE
                        break
            print("Did you mean", f"'{get_keyword(code)}'", "?", end="\n\n")
            tokens.insert(0, tok)
        if ERROR_COUNTER >= MAX_ERROR:
            print("Too many errors, exiting")
            # if VERBOSE: print(0/0)
            exit(1)
        # print(0/0) # To show the stack trace
        # exit(1)
    return tok

# fICHIER :	'with Ada.Text_IO ; use Ada.Text_IO ;\nprocedure' IDENT 'is' dECL*'\nbegin' iNSTR+ 'end' iDENTINTER ';';
def FICHIER(tokens: list[Token], node:Node) -> None:
    # print("Entering FICHIER")
    consume(tokens, 129)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 12)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 13)
    consume(tokens, 127)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 12)
    consume(tokens, 300, Token.__lt__)
    consume(tokens, 13)
    consume(tokens, 119)
    node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
    consume(tokens, 112)
    while tokens[0]!=103: # not 'begin'
        DECL(tokens, node.add_child(Node("DECL")))
    consume(tokens, 103)
    INSTR(tokens, node.add_child(Node("INSTR")))
    while tokens[0] != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
    consume(tokens, 106)
    if consume(tokens, 13, lambda t, c: t!=c and t<300)!=13:
        consume(tokens, 13)

# dECL :	'type' IDENT ('is' d)? ';' | pROCEDURE | fUNC | IDENT (',' IDENT)* : TYPE  (':=' EXPR)? ';';
def DECL(tokens:list[Token], node:Node) -> None:
    # print("Entering DECL")
    tok = consume(tokens, (126, 119, 109), lambda t, c: not t in c and 300>t) # check whether tok is in (126, 119, 109, 'ident')
    if tok==126: # ==type
        node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
        tok = consume(tokens, (112, 13), lambda t, c: not t in c)
        if tok==112:
            D(tokens, node.add_child(Node("D")))
            consume(tokens, 13)
        return
    if tok==119:
        PROCEDURE(tokens, node.add_child(Node("PROCEDURE")))
        return
    if tok==109:
        FUNC(tokens, node.add_child(Node("FUNC")))
        return
    if tok.code >= 300:
        node.add_child(Node("Ident-" + tok.value))
        while tokens[0] != 18: # not ':'
            consume(tokens, 17)
            node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
        consume(tokens, 18)
        TYPE(tokens, node)
        if tokens[0] == 14: # ':='
            consume(tokens, 14)
            EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
        return
    # Error has been handled before
    tok = consume(tokens, (17, 14, 13, 18), lambda t, c:not t in c) # check whether tok is in (17, 14, 13)
    while tok.code == 17:
        Node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
        tok = consume(tokens, (17, 18), lambda t, c:not t in c)
    TYPE(tokens, node)
    tok = consume(tokens, (14, 13), lambda t, c:not t in c) # check whether tok is in (14, 13)
    if tok==14:
        EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
    # print("Leaving DECL")


# d : 'access' IDENT | 'record' cHAMPS+ 'end record ;';
def D(tokens:list[Token], node:Node) -> None:
    # print("Entering D")
    tok = consume(tokens, (101, 120), lambda t, c: not t in c) # check whether tok is in (101, 120)
    if tok==101:
        node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
        return
    # Error has been handled in consume => tok=='record'
    CHAMPS(tokens, node.add_child(Node("CHAMPS")))
    while (tok := tokens[0]) != 106: # put tok in tok then check if tok != 106
        CHAMPS(tokens, node.add_child(Node("CHAMPS")))
    consume(tokens, 106) # tok==106 but we consume it anyway for consistency
    consume(tokens, 120)
    consume(tokens, 13)

# pROCEDURE :	'procedure' IDENT pARAMS? 'is' dECL*'\nbegin' iNSTR+ 'end' IDENT? ';';
def PROCEDURE(tokens:list[Token], node:Node) -> None:
    # print("Entering PROCEDURE")
    node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
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
        node.add_child(Node("Ident-" + consume(tokens, 300, Token.__lt__).value))
    consume(tokens, 13)
    # print("Leaving PROCEDURE")

# fUNC :	'function' IDENT pARAMS? 'return' tYPE 'is' dECL*'\nbegin' iNSTR+ 'end' IDENT?';';
def FUNC(tokens:list[Token], node:Node) -> None:
    # print("Entering FUNC")
    node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    tok = tokens[0]
    # N'utilise par tok = consume(tokens, (101, 120), lambda t, c: not t in c) # check whether tok is in (101, 120)
    # car si on a params, il faut consume 'return' une fois params terminé, sauf que ce n'est pas toujours le suivant
    if tok.code == 15:
        PARAMS(tokens, node.add_child(Node("PARAMS")))
    consume(tokens, 122)
    TYPE(tokens, node)
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
    if tokens[0].code >= 300:
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 13)

# eXPR :	tERM (oP tERM)* ('.' IDENT)?
def EXPR(tokens:list[Token], node:Node) -> None:
    # print("Entering EXPR")
    TERM(tokens, node.add_child(Node("TERM")))
    while not tokens[0] in (12, 13, 124, 16):
        OP(tokens, node.add_child(Node("OP")))
        TERM(tokens, node.add_child(Node("TERM")))
    if tokens[0] == 12:
        consume(tokens, 12)
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)

# tERM :	ENTIER | CHAR val EXPR |	'true' | 'false' | 'null' | 'not' eXPR | '-' eXPR | IDENT ('(' eXPR vIRGULEEXPRETOILE ')')? | 'new' IDENT ;
def TERM(tokens:list[Token], node:Node) -> None:
    # print("Entering TERM")
    # Manage non terminaux
    match tokens[0]:
        case 200: # ENTIER
            node.add_child("Entier-" + consume(tokens, 200, Token.__lt__).value)
            return
        case 202: # CHAR
            node.add_child("Char: " + consume(tokens, 202, Token.__lt__).value)
            consume(tokens, 130)
            EXPR(tokens, node.add_child(Node("EXPR")))
            return
    # Manage terminaux
    if tokens[0] in (125, 126, 116):
        node.add_child("Const: " + consume(tokens, (125, 126, 116), lambda t, c: not t in c).value)
        return
    if tokens[0] in (115, 8):
        EXPR(tokens, node.add_child(Node("EXPR")))
        return
    if tokens[0] == 114:
        node.add_child("Ident-" + consume(tokens, 114).value)
        return
    # IDENT ('(' eXPR vIRGULEEXPRETOILE ')')?
    node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    if tokens[0] == 15: # '('
        consume(tokens, 15) # consume anyway for consistency
        EXPR(tokens, node.add_child(Node("EXPR")))
        while consume(tokens, (17, 16), lambda t, c: not t in c) == 17:
            EXPR(tokens, node.add_child(Node("EXPR")))
    
    

def VALEXPR(tokens:list[Token], node:Node) -> None:
    pass

    
# iNSTR : IDENT hELP2 |	'return' eXPR? ';' |	bEGIN |	iF |	fOR |	wHILE |	ENTIER fIN |	CHAR VALEXPR fIN |	'true' fIN |	'false' fIN |	'null' fIN |	'not' EXPR fIN |	'-' EXPR fIN |	'new' IDENT fIN;
def INSTR(tokens:list[Token], node:Node) -> None:
    # print("Entering INSTR")
    if tokens[0].code >=300: # If is IDENT
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value) # Consume for consistency
        HELP2(tokens, node.add_child(Node("HELP2")))
        return
    # Manage BEGIN, etc here
    match tokens[0]:
        case 103:
            BEGIN(tokens, node.add_child(Node("BEGIN")))
            return
        case 110:
            IF(tokens, node.add_child(Node("IF")))
            return
        case 108:
            FOR(tokens, node.add_child(Node("FOR")))
            return
        case 128:
            WHILE(tokens, node.add_child(Node("WHILE")))
            return
    # Manage .* fIN here
    tok = consume(tokens, (122, 125, 107, 116, 115, 8, 114, 200, 202), lambda t, c: not t in c) # check whether tok is in (122, 103, 108, 110, 128, 200, 202, 125, 107, 116, 115, 8, 114)
    if tok==122:
        if tokens[0].code!=13:
            EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
        return
    if tok == 114:
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    elif tok==200:
        node.add_child("Entier-" + consume(tokens, 200, Token.__lt__).value)
    # elif tok==202: # Temporaire en attendant ce que l'on fait avec val
    #     node.add_child("Char: " + consume(tokens, 202, Token.__lt__).value)
    elif tok in (115, 8):
        EXPR(tokens, node.add_child(Node("EXPR")))
    elif not tok in (125, 107, 116):
        FIN(tokens, node.add_child(Node("FIN")))
        return
    consume(tokens, 13)

    
    
# fIN -> (oP tERM)* '.' IDENT ':=' EXPR ';';
def FIN(tokens:list[Token], node:Node) -> None:
    # print("Entering FIN")
    tok = tokens[0]
    while tok.code in [1,2,3,4,5,6,7,8,9,10,102,117,121]:
        OP(tokens, node.add_child(Node("OP")))
        TERM(tokens, node.add_child(Node("TERM")))
        tok = tokens[0]
    consume(tokens, 12)
    node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 14)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 13)
    # Rajouter les erreurs

# hELP2 :	':=' eXPR ';' |	'(' eXPR hELP3
def HELP2(tokens:list[Token], node:Node) -> None:
    # print("Entering HELP2")
    tok = consume(tokens, (14, 15), lambda t, c: not t in c) # check whether tok is in (14, 15)
    EXPR(tokens, node.add_child(Node("EXPR")))
    if tok==15:
        HELP3(tokens, node.add_child(Node("HELP3")))
    else:
        consume(tokens, 13)

# hELP3 :	')' hELP |	',' eXPR (','eXPR)* ')' (oP tERM)* IDENT ':=' eXPR ';';
def HELP3(tokens:list[Token], node:Node) -> None:
    # print("Entering HELP3")
    tok = consume(tokens, (16, 17), lambda t, c: not t in c) # check whether tok is in (16, 17)
    if tok==16: # == ')'
        HELP(tokens, node.add_child(Node("HELP")))
        return
    EXPR(tokens, node.add_child(Node("EXPR")))
    while(consume(tokens, (16, 17), lambda t, c: not t in c)==17):
        EXPR(tokens, node.add_child(Node("EXPR")))
    while tokens[0] < 300: # If is not IDENT
        OP(tokens, node.add_child(Node("OP")))
        TERM(tokens, node.add_child(Node("TERM")))
    consume(tokens, 14)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 13)

# hELP :	('(' eXPR ')')* ';' |	IDENT ':=' eXPR ';' |	(oP tERM)+ IDENT ':=' eXPR ';';
def HELP(tokens:list[Token], node:Node) -> None:
    # print("Entering HELP")
    if tokens[0] > 300:
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
        consume(tokens, 14)
        EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 13)
        return
    while tokens[0]==15:
        consume(tokens, 15)
        EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 16)
    if tokens[0]==13:
        consume(tokens, 13)
        return
    OP(tokens, node.add_child(Node("OP")))
    TERM(tokens, node.add_child(Node("TERM")))
    while tokens[0] < 300:
        OP(tokens, node.add_child(Node("OP")))
        TERM(tokens, node.add_child(Node("TERM")))
    consume(tokens, 14)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 13)

# bEGIN :	'begin' iNSTR+ 'end';
def BEGIN(tokens:list[Token], node:Node) -> None:
    # print("Entering BEGIN")
    consume(tokens, 103)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    consume(tokens, 106)

# iF :	'if' eXPR 'then' iNSTR+ iF_TAIL ';'
def IF(tokens:list[Token], node:Node) -> None:
    # print("Entering IF")
    consume(tokens, 110)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 124)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while not tok.code in (106, 104):
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    IF_TAIL(tokens, node.add_child(Node("IF_TAIL")))
    consume(tokens, 13)

# iF_TAIL :	'elsif' eXPR 'then' iNSTR+ iF_TAIL |	('else' iNSTR+)? 'end' 'if'
def IF_TAIL(tokens:list[Token], node:Node) -> None:
    # print("Entering IF_TAIL")
    tok = tokens[0]
    if tok.code == 105:
        consume(tokens, 105)
        EXPR(tokens, node.add_child(Node("EXPR")))
        consume(tokens, 124)
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
        while tok.code != 106:
            INSTR(tokens, node.add_child(Node("INSTR")))
            tok = tokens[0]
        IF_TAIL(tokens, node.add_child(Node("IF_TAIL")))
    elif tok.code == 104:
        consume(tokens, 104)
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
        while tok.code != 106:
            INSTR(tokens, node.add_child(Node("INSTR")))
            tok = tokens[0]
        consume(tokens, 106)
        consume(tokens, 110)
    elif tok.code == 106:
        consume(tokens, 106)
        consume(tokens, 110)
    else:
        print_err(1, tok, "elsif, else, end")
    
# fOR :	'for' IDENT 'in' 'reverse'? eXPR '...' eXPR'\nloop' iNSTR+ 'end' 'loop' ';';
def FOR(tokens:list[Token], node:Node) -> None:
    # print("Entering FOR")
    consume(tokens, 108)
    node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    consume(tokens, 111)
    tok = tokens[0]
    if tok.code == 123:
        consume(tokens, 123)
    EXPR(tokens, node.add_child(Node("EXPR")))
    # Methode temporaire en attendant l'insertion des '..' officiels ou des '...' officieux dans les caractères spéciaux
    if tokens[0] == 12 and tokens[1] == 12 : # and tokens[2] == 12:
        consume(tokens, 12)
        consume(tokens, 12)
        #consume(tokens, 12)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 113)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    consume(tokens, 106)
    consume(tokens, 113)
    consume(tokens, 13)
    
# wHILE :	'while' eXPR 'loop' iNSTR+ 'end loop';
def WHILE(tokens:list[Token], node:Node) -> None:
    # print("Entering WHILE")
    consume(tokens, 128)
    EXPR(tokens, node.add_child(Node("EXPR")))
    consume(tokens, 113)
    INSTR(tokens, node.add_child(Node("INSTR")))
    tok = tokens[0]
    while tok.code != 106:
        INSTR(tokens, node.add_child(Node("INSTR")))
        tok = tokens[0]
    consume(tokens, 106)
    consume(tokens, 113)

# cHAMPS :	IDENT (','IDENT)* ':' tYPE ';';
def CHAMPS(tokens:list[Token], node:Node) -> None:
    # print("Entering CHAMPS")
    node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    tok = tokens[0]
    while tok.code == 17:
        consume(tokens, 17)
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
        tok = tokens[0]
    consume(tokens, 18)
    TYPE(tokens, node)
    consume(tokens, 13)

# tYPE :	IDENT |	'access' IDENT ;
def TYPE(tokens:list[Token], node:Node) -> None:
    # print("Entering TYPE")
    tok = consume(tokens, (300, 101), lambda t, c: t in c,) # check whether tok is in (300, 101)
    if tok==101:
        node.add_child("Type-" + consume(tokens, 300, Token.__lt__).value)
    else:
        node.add_child("Type-" + tok.value)
    # print('Fin Type')

# pARAMS :	'('pARAM (';'pARAM)*')';
def PARAMS(tokens:list[Token], node:Node) -> None:
    # print("Entering PARAMS")
    consume(tokens, 15)
    PARAM(tokens, node.add_child(Node("PARAM")))
    tok = consume(tokens, (16, 13), lambda t, c: not t in c) # check whether tok is in (16, 17))
    while tok.code == 13:
        PARAM(tokens, node.add_child(Node("PARAM")))
        # print('retour PARAMS')
        tok = consume(tokens, (16, 17), lambda t, c: not t in c)
  

# pARAM :	IDENT (','IDENT)* ':' mODE? tYPE;
def PARAM(tokens:list[Token], node:Node) -> None:
    # print("Entering PARAM")
    node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
    tok = consume(tokens, (17, 18), lambda t, c: not t in c) # check whether tok is in (17, 18)
    while tok.code == 17:
        consume(tokens, 17)
        node.add_child("Ident-" + consume(tokens, 300, Token.__lt__).value)
        tok = consume(tokens, (17, 18), lambda t, c: not t in c)
    # JE SAIS I KNOW deux check mais plus simple à comprendre
    tok = tokens[0]
    if tok.code == 111:
        MODE(tokens, node.add_child(Node("MODE")))
    TYPE(tokens, node)

# mODE :	'in' 'out'?;
def MODE(tokens:list[Token], node:Node) -> None:
    # print("Entering MODE")
    consume(tokens, 111)
    tok = tokens[0]
    if tok.code == 118:
        consume(tokens, 118)

# oP :	'and' 'then'? |	'or' 'else'? |	'=' |	'/=' |	'<' |	'<=' |	'>' |	'>=' |	'*' |	'/' |	'rem' |	'+' |	'-';
def OP(tokens:list[Token], node:Node) -> None:
    # print("Entering OP")
    tok = consume(tokens, (102, 117, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 121, 17), lambda t, c: not t in c) # check whether tok is in (102, 117, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    if tok==102 and tokens[0]==124:
        consume(tokens, 124) # Consume anyway for consistency
    elif tok==117 and tokens[0]==104:
        consume(tokens, 104) # Consume anyway for consistency

if __name__=="__main__":
    from analyseurLexical import analyseurLexical
    from sys import argv
    tokens: list[Token]
    lexique: list[str]
    tokens, lexique = analyseurLexical(argv[1] if len(argv)>=2 else "../data/test1_correct.ada")
    # print(tokens, end="\n\n")
    # print(lexique, end="\n\n")
    ROOT = Node("FICHIER")
    FICHIER(tokens, ROOT)
    # print("\n\n")
    # print(ROOT)
    # print("\n\n")
    print(ROOT.mermaid())

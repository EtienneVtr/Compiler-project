from analyseurLexical import Token
current_token = None
tokens = None

def next_token(tokens):
    try:
        return next(tokens)
    except StopIteration:
        return None
    

def consume(expected_type):
    global current_token, tokens
    print(f"Consuming {current_token}")
    if current_token == expected_type:
        current_token = next_token(tokens)
    else:
        raise SyntaxError(f"Expected token type {expected_type}, but got {current_token}")

def Fichier():
    global current_token, tokens
    print("ok")
    consume("with")
    consume("Ada")
    consume(".")
    consume("Text_IO")
    consume(";")
    consume("use")
    consume("Ada")
    consume(".")
    consume("Text_IO")
    consume(";")
    consume("procedure")
    IDENT()
    consume("is")
    while current_token in ["type", "procedure", "function"]:
        if current_token == "type":
            DECL()
        elif current_token == "procedure":
            PROCEDURE()
        elif current_token == "function":
            FUNCTION()
    consume("begin")
    while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
        INSTR()
    consume("end")
    if current_token.type == 'IDENT':
        IDENT()
    consume(";")
        
def DECL():
    global current_token, tokens
    if current_token == 'type':
        consume('type')
        IDENT()
        if current_token == 'is':
            consume('is')
            d()
        consume(';')
    else:
        raise SyntaxError(f"Expected 'type' token, but got {current_token}")

def d():
    global current_token, tokens
    if current_token == 'access':
        consume('access')
        IDENT()
    elif current_token == 'record':
        consume('record')
        while current_token.type == 'IDENT':
            CHAMPS()
        consume('end record;')
    else:
        raise SyntaxError(f"Expected 'access' or 'record', but got {current_token}")

def CHAMPS():
    global current_token, tokens
    IDENT()
    while current_token == ',':
        consume(',')
        IDENT()
    consume(':')
    TYPE()
    consume(';')

def PROCEDURE():
    global current_token, tokens
    if current_token == 'procedure':
        consume('procedure')
        IDENT()
        PARAMS()
        if current_token == 'is':
            consume('is')
            DECL()
            while current_token.type == 'IDENT':
                INSTR()
            consume('end')
            if current_token == 'IDENT':
                IDENT()
            consume(';')
        else:
            raise SyntaxError(f"Expected 'is', but got {current_token}")
    else:
        raise SyntaxError(f"Expected 'procedure', but got {current_token}")

def PARAMS():
    global current_token, tokens
    if current_token == '(':
        consume('(')
        PARAM()
        while current_token == ',':
            consume(',')
            PARAM()
        consume(')')

def FUNCTION():
    global current_token, tokens
    if current_token == 'function':
        consume('function')
        IDENT()
        PARAMS()
        if current_token == 'return':
            consume('return')
            TYPE()
            if current_token == 'is':
                consume('is')
                DECL()
                while current_token.type == 'IDENT':
                    INSTR()
                consume('end')
                if current_token == 'IDENT':
                    IDENT()
                consume(';')
            else:
                raise SyntaxError(f"Expected 'is', but got {current_token}")
        else:
            raise SyntaxError(f"Expected 'return', but got {current_token}")
    else:
        raise SyntaxError(f"Expected 'function', but got {current_token}")

def INSTR():
    global current_token, tokens
    if current_token == 'IDENT':
        IDENT()
        if current_token == ':=':
            consume(':=')
            EXPR()
            consume(';')
        elif current_token == '(':
            consume('(')
            EXPR()
            while current_token == ',':
                consume(',')
                EXPR()
            consume(')')
            consume(';')
        elif current_token == 'begin':
            BEGIN()
        elif current_token == 'if':
            IF()
        elif current_token == 'for':
            FOR()
        elif current_token == 'while':
            WHILE()
        else:
            raise SyntaxError(f"Unexpected token {current_token}")
    elif current_token == 'return':
        consume('return')
        EXPR()
        consume(';')
    else:
        raise SyntaxError(f"Unexpected token {current_token}")

def PARAM():
    global current_token, tokens
    IDENT()
    while current_token == ',':
        consume(',')
        IDENT()
    consume(':')
    MODE()
    TYPE()

def MODE():
    global current_token, tokens
    if current_token == 'in':
        consume('in')
    elif current_token == 'in out':
        consume('in out')

def TYPE():
    global current_token, tokens
    if current_token.type == 'IDENT':
        IDENT()
    elif current_token == 'access':
        consume('access')
        IDENT()
    else:
        raise SyntaxError(f"Unexpected token {current_token}")

def EXPR():
    global current_token, tokens
    TERM()
    while current_token in ['=', '/=', '<', '<=', '>', '>=', '+', '-', '*', '/', 'rem', 'and', 'and then', 'or', 'or else']:
        OP()
        TERM()

def BEGIN():
    global current_token, tokens
    consume('begin')
    while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
        INSTR()
    consume('end')

def IF():
    global current_token, tokens
    consume('if')
    EXPR()
    consume('then')
    while current_token == 'elsif':
        consume('elsif')
        EXPR()
        consume('then')
    if current_token == 'else':
        consume('else')
        while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
            INSTR()
    consume('end if')

def FOR():
    global current_token, tokens
    consume('for')
    IDENT()
    consume('in')
    if current_token == 'reverse':
        consume('reverse')
    EXPR()
    consume('...')
    EXPR()
    consume('loop')
    while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
        INSTR()
    consume('end loop;')

def WHILE():
    global current_token, tokens
    consume('while')
    EXPR()
    consume('loop')
    while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
        INSTR()
    consume('end loop')

def TERM():
    global current_token, tokens
    if current_token.type == 'ENTIER':
        consume('ENTIER')
    elif current_token.type == 'CHAR':
        consume('CHAR')
    elif current_token in ['true', 'false', 'null']:
        consume(current_token)
    elif current_token == 'not':
        consume('not')
        EXPR()
    elif current_token == '-':
        consume('-')
        EXPR()
    elif current_token.type == 'IDENT':
        ACCES()
    elif current_token == 'new':
        consume('new')
        IDENT()
    else:
        raise SyntaxError(f"Unexpected token {current_token}")

def OP():
    global current_token, tokens
    if current_token in ['=', '/=', '<', '<=', '>', '>=', '+', '-', '*', '/', 'rem', 'and', 'and then', 'or', 'or else']:
        consume(current_token)
    else:
        raise SyntaxError(f"Unexpected token {current_token}")

def ACCES():
    global current_token, tokens
    if current_token.type == 'IDENT':
        IDENT()
    elif current_token == '(':
        consume('(')
        EXPR()
        while current_token == ',':
            consume(',')
            EXPR()
        consume(')')
    elif current_token == '.':
        consume('.')
        IDENT()
    else:
        raise SyntaxError(f"Unexpected token {current_token}")

def IF_TAIL():
    global current_token, tokens
    if current_token == 'elsif':
        consume('elsif')
        EXPR()
        consume('then')
        while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
            INSTR()
        IF_TAIL()
    elif current_token == 'else':
        consume('else')
        while current_token.type in ['if', 'for', 'while', 'IDENT', 'begin']:
            INSTR()

def IDENT():
    global current_token, tokens
    if current_token.code == 201:  # Code d'un identificateur
        consume(current_token.code)
        ID()
    else:
        raise SyntaxError("Expected IDENT token, but got {current_token}")

def ID():
    global current_token, tokens
    if current_token.value in ["entier", "caractère", "_"]:
        consume(current_token.value)
        if current_token.code == "ID":
            ID()
    else:
        raise SyntaxError("Expected ID token, but got {current_token}")



Tokens = [
    Token("with", 1, 129), Token("Ada", 1, 201), Token(".", 1, 12), Token("Text_IO", 1, 201), Token(";", 1, 13),
    Token("procedure", 2, 119), Token("hello", 2, 201), Token("is", 2, 112),
    Token("begin", 4, 103),
    Token("x", 5, 201), Token(":=", 5, 14), Token("3", 5, 200),
    Token("if", 6, 110), Token("x", 6, 201), Token("=", 6, 1), Token("3", 6, 200),
    Token("then", 7, 124), Token("Ada", 7, 201), Token(".", 7, 12), Token("Text_IO", 7, 201), Token(".", 7, 12), Token("Put_Line", 7, 201), Token("(", 7, 15), Token("\"Hello, world!\"", 7, 202), Token(")", 7, 16), Token(";", 7, 13),
    Token("else", 8, 104), Token("Ada", 8, 201), Token(".", 8, 12), Token("Text_IO", 8, 201), Token(".", 8, 12), Token("Put_Line", 8, 201), Token("(", 8, 15), Token("\"Pas Hello, world!\"", 8, 202), Token(")", 8, 16), Token(";", 8, 13),
    Token("end", 9, 106), Token("if", 9, 110), Token(";", 9, 13),
    Token("end", 10, 106), Token("Hello", 10, 201), Token(";", 10, 13)
]

tokens = iter(Tokens)
current_token = next_token(tokens)

print(f"Initial token: {current_token}")


try:
    Fichier()

    print("Analyse syntaxique réussie. Aucune erreur détectée.")
except SyntaxError as e:
    print("Erreur syntaxique détectée:", str(e))
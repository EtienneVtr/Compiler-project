from analyseurLexical import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def consume(self, expected_type):
        print(f"Consuming {self.current_token}")
        if self.current_token == expected_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected token type {expected_type}, but got {self.current_token}")

    def analyseFichier(self):
        print("Start Fichier")
        self.consume("with")
        self.consume("Ada")
        self.consume(".")
        self.consume("Text_IO")
        self.consume(";")
        """
        self.consume("use")
        self.consume("Ada")
        self.consume(".")
        self.consume("Text_IO")
        self.consume(";")
        """
        self.consume("procedure")
        self.analyseIdent()
        self.consume("is")
        while self.current_token in ["type", "procedure", "function"]:
            self.analyseDecl()
        self.consume("begin")
        while self.current_token not in ["end"]:
            self.analyseInstr()
        self.consume("end")
        if self.current_token == "ident":
            self.analyseIdent()
        self.consume("; EOF")

    def analyseDecl(self):
        print("Analyzing declaration")
        if self.current_token == "type":
            self.consume("type")
            self.analyseIdent()
            self.analyseD()
            self.consume(";")
        elif self.current_token == "procedure":
            self.analyseProcedure()
        elif self.current_token == "function":
            self.analyseFunction()
        else:
            raise SyntaxError("Expected declaration")

    def analyseInstr(self):
        print("Analyzing instruction")
        if self.current_token == "access":
            self.consume("access")
        elif self.current_token == "return":
            self.consume("return")
            if self.current_token in ["entier", "caractère", "true", "false", "null", "accès", "E", "new"]:
                self.analyseExpr()
            self.consume(";")
        elif self.current_token == "ident":
            self.consume("ident")
            self.analyseI()
            self.consume(";")
        elif self.current_token == "begin":
            self.analyseBegin()
        elif self.current_token == "if":
            self.analyseIf()
        elif self.current_token == "for":
            self.analyseFor()
        elif self.current_token == "while":
            self.analyseWhile()
        else:
            raise SyntaxError("Expected instruction")
        
    def analyseExpr(self):
        print("Analyzing expression")
        if self.current_token in ["entier", "caractère", "true", "false", "null"]:
            self.consume(self.current_token)
        elif self.current_token == "accès":
            self.analyseAccès()
        elif self.current_token == "E":
            self.analyseE()
        elif self.current_token == "new":
            self.consume("new")
            self.analyseIdent()
        else:
            raise SyntaxError("Expected expression")
        
    def analyseI(self):
        print("Analyzing I")
        if self.current_token == "(":
            self.consume("(")
            self.analyseExpr()
            while self.current_token == ",":
                self.consume(",")
                self.analyseExpr()
            self.consume(")")

    def analyseBegin(self):
        print("Analyzing begin")
        self.consume("begin")
        while self.current_token not in ["end"]:
            self.analyseInstr()
        self.consume("end")

    def analyseIf(self):
        self.consume("if")
        self.analyseExpr()
        self.consume("then")
        while self.current_token not in ["elsif", "else", "end"]:
            self.analyseInstr()
        self.analyseIfTail()

    def analyseIfTail(self):
        if self.current_token == "elsif":
            self.consume("elsif")
            self.analyseExpr()
            self.consume("then")
            while self.current_token not in ["elsif", "else", "end"]:
                self.analyseInstr()
            self.analyseIfTail()
        elif self.current_token == "else":
            self.consume("else")
            while self.current_token != "end":
                self.analyseInstr()
        self.consume("end if")

    def analyseFor(self):
        self.consume("for")
        self.analyseIdent()
        self.consume("in")
        if self.current_token == "reverse":
            self.consume("reverse")
        self.analyseExpr()
        self.consume("...")
        self.analyseExpr()
        self.consume("loop")
        while self.current_token not in ["end"]:
            self.analyseInstr()
        self.consume("end loop")

    def analyseWhile(self):
        self.consume("while")
        self.analyseExpr()
        self.consume("loop")
        while self.current_token not in ["end"]:
            self.analyseInstr()
        self.consume("end loop")

    def analyseIdent(self):
        print(f"Analyzing identifier {self.current_token}")
        self.consume(self.current_token)

    def analyseID(self):
        if self.current_token in ["entier", "caractère", "_"]:
            self.consume(self.current_token)
            if self.current_token == "ID":
                self.analyseID()


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


parser = Parser(iter(Tokens))

try:
    parser.analyseFichier()
    print("Analyse syntaxique réussie. Aucune erreur détectée.")
except SyntaxError as e:
    print("Erreur syntaxique détectée:", str(e))

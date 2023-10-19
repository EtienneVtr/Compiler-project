import re

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
    'or', 'or else', 'and', 'and then', 'not',
    '=', '/=', '>', '>=', '<', '<=', '+', '-',
    '*', '/', 'rem', '--', '.', ';',':=','(',')',','
]

# Expression régulière pour identifier les commentaires
comment_pattern = re.compile(r'--.*')

# Création d'une regex pour les opérateurs
operator_pattern = re.compile('|'.join(map(re.escape, operators)))

# Expression régulière pour identifier les mots-clés
keyword_pattern = re.compile('|'.join(map(re.escape, keywords)))

# Expression régulière pour les identificateurs
identifier_pattern = re.compile(r'[a-zA-Z][a-zA-Z0-9_]*')

# Expression régulière pour les constantes entières
integer_pattern = re.compile(r'[0-9]+')

# Expression régulière pour les constantes caractères
char_pattern = re.compile(r"'[ -~]'")

def lexer(input_string):
    tokens = []
    in_comment = False  # Pour suivre si nous sommes actuellement dans un commentaire multiligne
    lines = input_string.split('\n')
    for line_number, line in enumerate(lines, start=1):
        if in_comment:
            # Si nous sommes déjà dans un commentaire, nous ajoutons la ligne entière comme commentaire
            tokens.append(('COMMENT', line, line_number))
            in_comment = False
            continue

        match = comment_pattern.search(line)
        if match:
            # Correspondance de commentaire sur la ligne
            comment = match.group(0)
            tokens.append(('COMMENT', comment, line_number))
            continue

        line = line.strip()
        while line:
            match = keyword_pattern.match(line)
            if match:
                keyword = match.group(0)
                tokens.append(('KEYWORD', keyword, line_number))
                line = line[len(keyword):].lstrip()
            else:
                match = operator_pattern.match(line)
                if match:
                    operator = match.group(0)
                    tokens.append(('OPERATOR', operator, line_number))
                    line = line[len(operator):].lstrip()
                else:
                    match = identifier_pattern.match(line)
                    if match:
                        identifier = match.group(0)
                        tokens.append(('IDENTIFIER', identifier, line_number))
                        line = line[len(identifier):].lstrip()
                    else:
                        match = integer_pattern.match(line)
                        if match:
                            integer = match.group(0)
                            tokens.append(('INTEGER', integer, line_number))
                            line = line[len(integer):].lstrip()
                        else:
                            match = char_pattern.match(line)
                            if match:
                                char = match.group(0)
                                tokens.append(('CHARACTER', char, line_number))
                                line = line[len(char):].lstrip()
                            else:
                                # Gérer les caractères inconnus
                                tokens.append(('UNKNOWN', line[0], line_number))
                                line = line[1:]

    return tokens

# Exemple d'utilisation
input_code = """
with Ada.Text_IO ; use Ada.Text_IO ;
procedure unDebut is
function aireRectangle(larg : integer; long : integer) return integer is
aire: integer;
begin
aire := larg * long ;
return aire
end aireRectangle ;
function perimetreRectangle(larg : integer; long : integer) return integer is
p : integer
begin
p := larg*2 + long*2 ;
return p
end perimetreRectangle;
-- VARIABLES
choix : integer ;
-- PROCEDURE PRINCIPALE
begin
choix := 2;
if choix = 1
then valeur := perimetreRectangle(2, 3) ;
put(valeur) ;
else valeur := aireRectangale(2, 3) ;
put(valeur) ;
end if;
end unDebut ;
"""
tokens = lexer(input_code)
for token in tokens:
    print(token)

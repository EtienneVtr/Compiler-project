# Fonction test du fichier src.fichierReader
import unittest
from sample.analyseurLexical import analyseurLexical, Token

nomFichier = "data/hw.ada"

attentes = [
    Token("with", 1, 129), Token("Ada", 1, 0), Token(".", 1, 12), Token("Text_IO", 1, 0), Token(";", 1, 13),
    Token("procedure", 2, 119), Token("Hello", 2, 0), Token("is", 2, 112),
    Token("begin", 4, 103),
    Token("x", 5, 0), Token(":=", 5, 14), Token("3", 5, 0),
    Token("if", 6, 110), Token("x", 6, 0), Token("=", 6, 1), Token("3", 6, 0),
    Token("then", 7, 124), Token("Ada", 7, 0), Token(".", 7, 12), Token("Text_IO", 7, 0), Token(".", 7, 12), Token("Put_Line", 7, 0), Token("(", 7, 15), Token("\"Hello", 7, 0), Token(",", 7, 17), Token("world!\"", 7, 0), Token(")", 7, 16), Token(";", 7, 13),
    Token("else", 8, 104), Token("Ada", 8, 0), Token(".", 8, 12), Token("Text_IO", 8, 0), Token(".", 8, 12), Token("Put_Line", 8, 0), Token("(", 8, 15), Token("\"Pas", 8, 0), Token("Hello", 8, 0), Token(",", 8, 17), Token("world!\"", 8, 0), Token(")", 8, 16), Token(";", 8, 13),
    Token("end", 9, 106), Token("if", 9, 110), Token(";", 9, 13),
    Token("end", 10, 106), Token("Hello", 10, 0), Token(";", 10, 13)
]

class TestAnalyseurLexical(unittest.TestCase):
    def test_ma_fonction(self):
        # Écrire vos tests ici
        result = analyseurLexical(nomFichier)
        print(result)
        self.assertEqual(result, attentes)

if __name__ == "__main__":
    unittest.main()


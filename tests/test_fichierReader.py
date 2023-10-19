# Fonction test du fichier src.fichierReader
import unittest
from sample.fichierReader import fileReader, Token

nomFichier = "data/hw.ada"

attentes = [
    Token("with", 129), Token("Ada", 0), Token(".", 12), Token("Text_IO", 0), Token(";", 13),
    Token("procedure", 119), Token("Hello", 0), Token("is", 112),
    Token("begin", 103),
    Token("x", 0), Token(":=", 14), Token("3", 0),
    Token("if", 110), Token("x", 0), Token("=", 1), Token("3", 0),
    Token("then", 124), Token("Ada", 0), Token(".", 12), Token("Text_IO", 0), Token(".", 12), Token("Put_Line", 0), Token("(", 15), Token("\"Hello", 0), Token(",", 17), Token("world!\"", 0), Token(")", 16), Token(";", 13),
    Token("else", 104), Token("Ada", 0), Token(".", 12), Token("Text_IO", 0), Token(".", 12), Token("Put_Line", 0), Token("(", 15), Token("\"Pas", 0), Token("Hello", 0), Token(",", 17), Token("world!\"", 0), Token(")", 16), Token(";", 13),
    Token("end", 106), Token("if", 110), Token(";", 13),
    Token("end", 106), Token("Hello", 0), Token(";", 13)
]

class TestFichierReader(unittest.TestCase):
    def test_ma_fonction(self):
        # Écrire vos tests ici
        result = fileReader(nomFichier)
        print(result)
        self.assertEqual(result, attentes)

if __name__ == "__main__":
    unittest.main()


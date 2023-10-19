# Fonction test du fichier src.fichierReader
import unittest
from sample.fichierReader import fichierReader

nomFichier = "data/codeCanAda"

attentes = ['Trouver', 'un', 'code', 'Ada', 'int', 'x', ';', 'if', '(', 'x', '>', '10', ')', '', '', '', '', 'then', 'print', '(', 'x', ')', ';']

class TestFichierReader(unittest.TestCase):
    def test_ma_fonction(self):
        # Écrire vos tests ici
        result = fichierReader(nomFichier)
        print(result)
        self.assertEqual(result, attentes)

if __name__ == "__main__":
    unittest.main()


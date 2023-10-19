# Projet compilateur

L'objectif de ce projet est d'écrire un compilateur d'un langage de haut niveau, en développant toutes les étapes qui le compose, depuis l'analyse lexicale jusqu'à la production de code assembleur ARM. Il s'agit d'un petit fragment du langage Ada.

## Arborescence du Projet

L'arborescence de ce projet suit une structure standard pour faciliter la gestion et le développement.
```
Aulagnie2u1/
│
├── README.md # Documentation du projet
├── requirements.txt # (Si nécessaire)
├── setup.py # (A faire) Fichier de configuration pour l'installation du projet
├── .gitignore # Liste des fichiers et répertoires à ignorer dans Git
│
├── sample/ # Dossier contenant le code source
│ ├── init.py # Fichier d'initialisation du module
│ ├── fichierReader.py # fichierReader
│ ├── module2.py # Module 2
│
├── tests/ # Tests unitaires
│ ├── init.py
│ ├── test_module1.py # Tests pour module1
│ ├── test_module2.py # Tests pour module2
│
├── docs/ # Données de cours ou utiles
│
├── data/ # Données statiques ou fichiers de configuration
│   ├── codeCanAda #Utile pour la réalision de test
│
└── app.py # Point d'entrée de l'application
```

## Tests Unitaires

Vous pouvez trouver les tests unitaires dans le répertoire `tests`. Chaque module à tester a un fichier de test correspondant.

### Comment créer un test

1. Créez un fichier de test dans le répertoire `tests` et nommez-le en utilisant la convention de nommage `test_nomdumodule.py`.

2. Importez le module que vous souhaitez tester. Par exemple, pour tester `module1`, vous pouvez utiliser :
   
```python
from mon_module.module1 import fonction_a_tester
```

Écrivez des méthodes de test en utilisant le module unittest. Par exemple :
```Python
import unittest

class TestModule1Functions(unittest.TestCase):
    def test_fonction_a_tester(self):
        # Écrire le test ici
        self.assertEqual(fonction_a_tester(arg1, arg2), attentes)  # Un exemple de test
```

### Comment executer les tests

Pour exécuter les tests, assurez-vous d'être dans le répertoire racine de votre projet, puis utilisez la commande suivante :

```bash
python3 -m unittest tests.test_fichierReader
``````
Cela exécutera le test du module fichierReader.

```bash
python -m unittest discover -s tests -p 'test_*.py'
``````
Cela exécutera tous les tests dont les noms de fichiers commencent par "test_".


import unittest
import importlib
import os
import sys
# modules/-Verzeichnis zum sys.path hinzufügen, damit dynamische Imports funktionieren
modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

class TestBeispielModul(unittest.TestCase):
    def test_run(self):
        mod = importlib.import_module('beispiel_modul')
        self.assertIsNone(mod.run())

class TestWetterModul(unittest.TestCase):
    def test_run(self):
        mod = importlib.import_module('wetter_modul')
        result = mod.run()
        self.assertTrue(isinstance(result, dict) or result is None)

class TestKIIntegrationModul(unittest.TestCase):
    def test_run(self):
        mod = importlib.import_module('ki_integration_modul')
        result = mod.run()
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()

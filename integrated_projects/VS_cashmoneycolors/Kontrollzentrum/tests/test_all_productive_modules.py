import unittest
import importlib.util
import os

class TestDropshippingModul(unittest.TestCase):
    def setUp(self):
        modul_name = "dropshipping_modul"
        modul_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "dropshipping_modul.py"))
        spec = importlib.util.spec_from_file_location(modul_name, modul_pfad)
        self.dropshipping_modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.dropshipping_modul)

    def test_run_returns_status(self):
        result = self.dropshipping_modul.run()
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "Dropshipping-Modul aktiv")

class TestKiModul(unittest.TestCase):
    def setUp(self):
        modul_name = "ki_modul"
        modul_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "ki_modul.py"))
        spec = importlib.util.spec_from_file_location(modul_name, modul_pfad)
        self.ki_modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.ki_modul)

    def test_run_returns_status(self):
        result = self.ki_modul.run()
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "KI-Modul aktiv")

class TestGrafikDesignModul(unittest.TestCase):
    def setUp(self):
        modul_name = "grafik_design_modul"
        modul_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "grafik_design_modul.py"))
        spec = importlib.util.spec_from_file_location(modul_name, modul_pfad)
        self.grafik_design_modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.grafik_design_modul)

    def test_run_returns_status(self):
        result = self.grafik_design_modul.run()
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "Grafik/Design-Modul aktiv")

class TestDataImportModul(unittest.TestCase):
    def setUp(self):
        modul_name = "data_import"
        modul_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "data_import.py"))
        spec = importlib.util.spec_from_file_location(modul_name, modul_pfad)
        self.data_import_modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.data_import_modul)

    def test_run_executes(self):
        # Der Rückgabewert kann None sein, wenn keine CSV vorhanden ist
        try:
            self.data_import_modul.run()
        except Exception as e:
            self.fail(f"data_import.run() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()

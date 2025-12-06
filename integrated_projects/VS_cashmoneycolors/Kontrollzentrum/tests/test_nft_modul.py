import unittest
import importlib.util
import os

class TestNftModul(unittest.TestCase):
    def setUp(self):
        modul_name = "nft_modul"
        modul_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "nft_modul.py"))
        spec = importlib.util.spec_from_file_location(modul_name, modul_pfad)
        self.nft_modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.nft_modul)

    def test_run_returns_status(self):
        result = self.nft_modul.run()
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "NFT-Modul aktiv")

if __name__ == "__main__":
    unittest.main()

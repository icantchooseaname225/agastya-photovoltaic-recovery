import tempfile
import unittest
from pathlib import Path

from inference.ledger import Ledger


class LedgerHealthTests(unittest.TestCase):
    def test_health_check_reads_a_valid_ledger_without_changing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "eye.sqlite3"
            ledger = Ledger(database, Path(directory) / "images")
            before = database.read_bytes()

            result = ledger.health_check()

            self.assertTrue(result["healthy"])
            self.assertEqual(result["integrity"], "ok")
            self.assertEqual(result["inspections"], 0)
            self.assertEqual(database.read_bytes(), before)

    def test_health_check_reports_missing_or_corrupt_database(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Ledger.__new__(Ledger)
            missing.database_path = Path(directory) / "missing.sqlite3"
            self.assertFalse(missing.health_check()["healthy"])

            corrupt_path = Path(directory) / "corrupt.sqlite3"
            corrupt_path.write_bytes(b"not a SQLite database")
            corrupt = Ledger.__new__(Ledger)
            corrupt.database_path = corrupt_path
            result = corrupt.health_check()
            self.assertFalse(result["healthy"])
            self.assertEqual(result["integrity"], "error")


if __name__ == "__main__":
    unittest.main()

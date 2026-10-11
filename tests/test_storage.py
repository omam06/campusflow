import unittest
import json
import os
import tempfile
from unittest.mock import patch

from campusflow.storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(
            self.temp_dir.name, "tickets.json"
        )
        self.patcher = patch(
            "campusflow.storage.TICKETS_FILE", self.file_path
        )
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_load_missing_file(self):
        self.assertEqual(load_tickets(), [])

    def test_save_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi issue",
                "status": "open"
            }
        ]

        save_tickets(tickets)

        with open(self.file_path, "r") as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data, tickets)

    def test_load_saved_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi issue",
                "status": "open"
            }
        ]

        save_tickets(tickets)

        self.assertEqual(load_tickets(), tickets)

    def test_load_malformed_json(self):
        with open(self.file_path, "w") as file:
            file.write("{invalid json")

        with self.assertRaises(json.JSONDecodeError):
            load_tickets()


if __name__ == "__main__":
    unittest.main()
import unittest
from campusflow.reports import get_active_queue, count_tickets_by_status, count_tickets_by_priority, generate_report

class TestReports(unittest.TestCase):
    def test_get_active_queue(self):
        tickets = [
            {"id": 5, "priority": "low", "status": "open"},
            {"id": 3, "priority": "critical", "status": "open"},
            {"id": 2, "priority": "high", "status": "resolved"},
            {"id": 1, "priority": "high", "status": "open"}
        ]   

        queue = get_active_queue(tickets)
        ids = [ticket["id"] for ticket in queue]

        self.assertEqual(ids, [3, 1, 5])
    
    def test_excludes_resolved_tickets(self):
        tickets = [
            {"id": 1, "priority": "high", "status": "resolved"},
            {"id": 2, "priority": "critical", "status": "resolved"}
        ]

        queue = get_active_queue(tickets)
        self.assertEqual(queue, [])

    def test_priority_ordering(self):
        tickets = [
            {"id": 1, "priority": "low", "status": "open"},
            {"id": 2, "priority": "medium", "status": "open"},
            {"id": 3, "priority": "high", "status": "open"},
            {"id": 4, "priority": "critical", "status": "open"}
        ]

        queue = get_active_queue(tickets)
        priorities = [ticket["priority"] for ticket in queue]

        self.assertEqual(
            priorities,
            ["critical", "high", "medium", "low"]
        )

    def test_same_priority_sorted_by_id(self):
        tickets = [
            {"id": 12, "priority": "high", "status": "open"},
            {"id": 4, "priority": "high", "status": "open"},
            {"id": 8, "priority": "high", "status": "open"}
        ]

        queue = get_active_queue(tickets)
        ids = [ticket["id"] for ticket in queue]

        self.assertEqual(ids, [4, 8, 12])

    def test_empty_ticket_list(self):
        tickets = []

        queue = get_active_queue(tickets)

        self.assertEqual(queue, [])

    def test_count_tickets_by_status(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "resolved", "priority": "low"},
            {"id": "T003", "status": "open", "priority": "high"},
            {"id": "T004", "status": "in_progress", "priority": "medium"}
        ]

        result = count_tickets_by_status(tickets)

        expected = {
            "open": 2,
            "in_progress": 1,
            "resolved": 1
        }

        self.assertEqual(result, expected)

    def test_count_tickets_by_priority(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "resolved", "priority": "low"},
            {"id": "T003", "status": "open", "priority": "critical"},
            {"id": "T004", "status": "in_progress", "priority": "high"}
        ]

        result = count_tickets_by_priority(tickets)

        expected = {
            "critical": 2,
            "high": 1,
            "medium": 0,
            "low": 1
        }

        self.assertEqual(result, expected)

    def test_generate_report(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "resolved", "priority": "low"},
            {"id": "T003", "status": "open", "priority": "high"}
        ]

        result = generate_report(tickets)

        expected = {
            "total": 3,
            "by_status": {
                "open": 2,
                "in_progress": 0,
                "resolved": 1
            },
            "by_priority": {
                "critical": 1,
                "high": 1,
                "medium": 0,
                "low": 1
            }
        }

        self.assertEqual(result, expected)

    def test_generate_empty_report(self):
        result = generate_report([])

        expected = {
            "total": 0,
            "by_status": {
                "open": 0,
                "in_progress": 0,
                "resolved": 0
            },
            "by_priority": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
        }

        self.assertEqual(result, expected)

    def test_same_priority_sorted_by_string_ticket_id(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"}
        ]

        queue = get_active_queue(tickets)
        ids = [ticket["id"] for ticket in queue]

        self.assertEqual(ids, ["T002", "T010"])
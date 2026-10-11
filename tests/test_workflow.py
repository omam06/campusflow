import unittest
from copy import deepcopy
from campusflow.workflow import assign_ticket, update_ticket_status
ticket_list = [
    {
        "id": 1,
        "title": "Cannot connect to campus Wi-Fi",
        "category": "Network",
        "urgency": "high",
        "affected_users": 15,
        "priority": "critical",
        "status": "open",
        "assigned_to": None
    },
    {
        "id": 2,
        "title": "Printer not working",
        "category": "Hardware",
        "urgency": "medium",
        "affected_users": 2,
        "priority": "low",
        "status": "open",
        "assigned_to": None
    },
    {
        "id": 3,
        "title": "Unable to access student portal",
        "category": "Software",
        "urgency": "high",
        "affected_users": 8,
        "priority": "high",
        "status": "open",
        "assigned_to": "Ada"
    }
]
class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.tickets = deepcopy(ticket_list)
    def test_assign_ticket(self):
        result = assign_ticket(self.tickets, 1, "Chidi")
        self.assertTrue(result)
        self.assertEqual(self.tickets[0]["assigned_to"], "Chidi")

    def test_assign_nonexistent_ticket(self):
        result = assign_ticket(self.tickets, 99, "Chidi")
        self.assertIsNone(result)

    def test_update_status_to_in_progress(self):
        result = update_ticket_status(self.tickets, 3, "in_progress")
        self.assertTrue(result)
        self.assertEqual(self.tickets[2]["status"], "in_progress")


    def test_cannot_start_unassigned_ticket(self):
        result = update_ticket_status(self.tickets, 1, "in_progress")
        self.assertIsNone(result)
        self.assertEqual(self.tickets[0]["status"], "open")


    def test_cannot_resolve_open_ticket(self):
        result = update_ticket_status(self.tickets, 2, "resolved")
        self.assertIsNone(result)
        self.assertEqual(self.tickets[1]["status"], "open")


    def test_resolve_in_progress_ticket(self):
        update_ticket_status(self.tickets, 3, "in_progress")
        result = update_ticket_status(self.tickets, 3, "resolved")
        self.assertTrue(result)
        self.assertEqual(self.tickets[2]["status"], "resolved")

    def test_reopen_resolved_ticket(self):
        update_ticket_status(self.tickets, 3, "in_progress")
        update_ticket_status(self.tickets, 3, "resolved")
        result = update_ticket_status(self.tickets, 3, "open")
        self.assertTrue(result)
        self.assertEqual(self.tickets[2]["status"], "open")


    def test_reject_invalid_status(self):
        result = update_ticket_status(self.tickets, 1, "pending")

        self.assertIsNone(result)
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_reject_empty_worker_name(self):
        result = assign_ticket(self.tickets, 1, "")

        self.assertIsNone(result)
        self.assertIsNone(self.tickets[0]["assigned_to"])


    def test_reject_whitespace_worker_name(self):
        result = assign_ticket(self.tickets, 1, "   ")

        self.assertIsNone(result)
        self.assertIsNone(self.tickets[0]["assigned_to"])

    def test_assignment_strips_whitespace(self):
        result = assign_ticket(self.tickets, 1, "  Chidi  ")

        self.assertTrue(result)
        self.assertEqual(self.tickets[0]["assigned_to"], "Chidi")

    def test_cannot_move_resolved_ticket_to_in_progress(self):
        update_ticket_status(self.tickets, 3, "in_progress")
        update_ticket_status(self.tickets, 3, "resolved")

        result = update_ticket_status(self.tickets, 3, "in_progress")

        self.assertIsNone(result)
        self.assertEqual(self.tickets[2]["status"], "resolved")
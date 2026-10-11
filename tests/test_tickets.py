import unittest
from campusflow.tickets import create_ticket, calculate_priority   #import function from campusflow 

class TestTicketCreationAndValidation(unittest.TestCase):
  #create a global empty list for all tests to
    def test_valid_ticket_creation(self):                #  Test that a perfectly valid input successfully builds a ticket dictionary.                                
        empty_list = []
        ticket = create_ticket(empty_list, "Cluster 3 Wi-Fi is completely down", "nEtwORk", "HIGH", 15)
        
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Cluster 3 Wi-Fi is completely down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 15)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_priority_matrix_hierarchy(self):         #Calculate priority exactly as specified
      # Rule 1 Boundary: high urgency AND 10+ users is of critical priority            
        self.assertEqual(calculate_priority("high", 10), "critical")

      # Rule 2 Boundary: high urgency OR 10+ users is of high priority
        self.assertEqual(calculate_priority("high", 7), "high")
        self.assertEqual(calculate_priority("low", 12), "high")
        
    # Rule 3 Boundaries: medium urgency OR 3+ users is of medium priority 
        self.assertEqual(calculate_priority("medium", 2), "medium")
        self.assertEqual(calculate_priority("low", 4), "medium")

      # Rule 4 Boundaries: all remaining valid tickets is of low priority
        self.assertEqual(calculate_priority("low", 2), "low")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_empty_title_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Ticket title cannot be empty or whitespace-only."):
            create_ticket(empty_list, "   ", "Network", "high", 5)

    def test_invalid_category_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Invalid category"):
            create_ticket(empty_list, "Broken chair", "Furniture", "low", 1)

    def test_invalid_urgency_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Invalid urgency"):
            create_ticket(empty_list, "Blank monitor screen", "Hardware", "highly critical", 7)

    def test_zero_and_negative_users_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Affected users must be a positive integer greater than zero."):
            create_ticket(empty_list, "TalentNation portal is down", "Software", "high", 0)
        with self.assertRaisesRegex(ValueError, "Affected users must be a positive integer greater than zero."):
            create_ticket(empty_list, "TalentNation portal is down", "Software", "high", -4)

    def test_text_user_count_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Affected users must be a positive integer greater than zero."):
            create_ticket(empty_list, "Slow server", "Hardware", "medium", "ten")

    def test_decimal_user_count_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Affected users must be a positive integer greater than zero."):
            create_ticket(empty_list, "Slow Server", "Hardware", "medium", 4.5)   

    def test_non_string_title_guard(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Ticket title must be a valid string"):
            create_ticket(empty_list, 5, "Network", "high", 3)

    def test_non_string_urgency_guard(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Urgency must be a valid string"):
            create_ticket(empty_list, "Valid Title", "Network", None, 3)

    def test_none_as_category_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Category must be a valid string"):
            create_ticket(empty_list, "Valid Title", None, "high", 3)

    def test_boolean_as_user_count_rejection(self):
        empty_list = []
        with self.assertRaisesRegex(ValueError, "Affected users cannot be a boolean value"):
            create_ticket(empty_list, "Valid Title", "Network", "low", True)
   
   # To test that a rejected tickets leave the list unchanged
    def test_rejected_ticket_leaves_stored_list_unchanged(self):
        # first build an initial list containing one valid ticket
        stored_tickets = [
            {"id": "T001", "title": "Initial Ticket", "category": "Hardware", "urgency": "low", "affected_users": 1, "priority": "low", "status": "open", "assigned_to": None}
        ]
        # copy it into another to compare against
        snapshot_copy = stored_tickets.copy()
        
        # input an invalid ticket execution that will fail
        with self.assertRaises(ValueError):
            create_ticket(stored_tickets, "   ", "Network", "high", 5)
            
        self.assertEqual(stored_tickets, snapshot_copy)     # Assert, to confirm that the primary container was completely untouched by the failure

# ID sequencing tests
    def test_id_empty_list_gives_t001(self):
        existing_tickets = []
        ticket = create_ticket(existing_tickets, "Wi-Fi is down", "Network", "high", 5)
        self.assertEqual(ticket["id"], "T001")

    def test_id_sequential_generation(self):
        existing_tickets = []
          # Create and append the first ticket
        ticket1 = create_ticket(existing_tickets, "Wi-Fi down", "Network", "high", 5)
        existing_tickets.append(ticket1)
        # Create the second ticket passing the updated list
        ticket2 = create_ticket(existing_tickets, "Keyboard broken", "Hardware", "medium", 2)
        self.assertEqual(ticket2["id"], "T002")
    
    def test_id_skips_to_next_highest(self):        #A hand-built list with the highest ID T005 gives T006.
    
        existing_tickets = [    
        {"id": "T001", "title": "Old Ticket 1"},
        {"id": "T005", "title": "Old Ticket 5"},
        {"id": "T003", "title": "Old Ticket 3"}
        ]
        new_ticket = create_ticket(existing_tickets, "New Bug", "Software", "low", 1)
        self.assertEqual(new_ticket["id"], "T006")


if __name__ == "__main__":
    unittest.main()                                                                                                                         


import unittest
from unittest.mock import patch

from campusflow.main import main


class TestMain(unittest.TestCase):

    @patch("campusflow.main.save_tickets")
    @patch("campusflow.main.load_tickets", return_value=[])
    @patch("builtins.input", side_effect=["7"])
    def test_save_and_exit(self, mock_input, mock_load, mock_save):
        main()

        mock_save.assert_called_once_with([])

    @patch("builtins.input", side_effect=["9", "7"])
    @patch("campusflow.main.save_tickets")
    @patch("campusflow.main.load_tickets", return_value=[])
    def test_invalid_menu_choice(self, mock_load, mock_save, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call("Invalid option. Please try again.")
        mock_save.assert_called_once_with([])

    @patch("builtins.input", side_effect=["2", "7"])
    @patch("campusflow.main.save_tickets")
    @patch("campusflow.main.load_tickets", return_value=[])
    def test_view_tickets_when_empty(self, mock_load, mock_save, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call("No tickets to display")

    @patch("builtins.input", side_effect=["5", "7"])
    @patch("campusflow.main.save_tickets")
    @patch("campusflow.main.load_tickets", return_value=[])
    def test_active_queue_when_empty(self, mock_load, mock_save, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call("Sorry, empty queue")

    
    
    @patch("builtins.input", side_effect=["6", "7"])
    @patch("campusflow.main.save_tickets")
    @patch("campusflow.main.load_tickets", return_value=[])
    def test_generate_empty_report(self, mock_load, mock_save, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call(
            "Total Ticket(s): 0, "
            "By order of status: {'open': 0, 'in_progress': 0, 'resolved': 0}, "
            "By order of priority: {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}"
        )



if __name__ == "__main__":
    unittest.main()
import json
import os
TICKETS_FILE =  "tickets.json"
def load_tickets():
    if os.path.exists(TICKETS_FILE):
        try:
            with open(TICKETS_FILE, "r") as file_content:
                tickets = json.load(file_content)
                return tickets
        except json.JSONDecodeError:
            raise 
    else:
        return []

def save_tickets(tickets):
    with open(TICKETS_FILE, "w") as opened_file:
        json.dump(tickets, opened_file)
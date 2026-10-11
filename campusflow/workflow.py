def assign_ticket(ticket_list, ticket_id, worker_name):
    if worker_name is None or not worker_name.strip():
        return None
    for ticket in ticket_list:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = worker_name.strip() 
            return True
    return None   

def update_ticket_status(ticket_list, ticket_id, new_status):
    valid_statuses = {"open", "in_progress", "resolved"}
    for ticket in ticket_list:
        if ticket["id"] == ticket_id:
            if new_status not in valid_statuses:
                return None
            if new_status == "in_progress" and ticket["assigned_to"] is None:
                return None
            if new_status == "resolved" and ticket["status"] != "in_progress":
                return None
            if ticket["status"] == "resolved" and new_status != "open":
                return None
            ticket["status"] = new_status
            return True
    return None
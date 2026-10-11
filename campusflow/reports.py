priority_order = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4
}

def get_active_queue(ticket_list):
    active_tickets = []
    for ticket in ticket_list:
        if ticket["status"] != "resolved":
            active_tickets.append(ticket)
    active_tickets = sorted(active_tickets, key=lambda ticket: (priority_order[ticket["priority"]], ticket["id"]))
    return active_tickets

def count_tickets_by_status(ticket_list):
    status_counts = {
        "open": 0,
        "in_progress": 0,
        "resolved": 0
    }
    for ticket in ticket_list:
        status = ticket["status"]
        status_counts[status] += 1
    return status_counts


def count_tickets_by_priority(ticket_list):
    priority_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low":0
    }
    for ticket in ticket_list:
        priority = ticket["priority"]
        priority_counts[priority] += 1
    return priority_counts

def generate_report(ticket_list):
    total = len(ticket_list)
    status_result = count_tickets_by_status(ticket_list)
    priority_result = count_tickets_by_priority(ticket_list)
    report = {
        "total": total,
        "by_status": status_result,
        "by_priority": priority_result
    }
    return report
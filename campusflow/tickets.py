# These are the official choices allowed by the rules
allowed_categories = {"Network", "Hardware", "Software", "Other"}
allowed_urgency_levels = {"low", "medium", "high"}

#first define a func to generate next unique ticket id
def next_ticket_id(ticket_list):
    highest = 0
    for each_ticket in ticket_list:
        ticket_id = each_ticket['id']
        numeric_part = int(ticket_id[1:])
        if numeric_part > highest:
            highest = numeric_part
    next_id = highest + 1
    return f'T{next_id:03d}' 

def calculate_priority(urgency, affected_users):         # Calculates ticket priority based on both info provided by user
   #ensure case normalization
    nocase_urgency = urgency.strip().lower()

    if nocase_urgency == "high" and affected_users >= 10:
        return "critical"
    elif nocase_urgency == "high" or affected_users >= 10:
        return "high"
    elif nocase_urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"

def create_ticket(existing_tickets, title, category, urgency, affected_users):
 #first check for text input types to prevent crash 
    if not isinstance(title, str):
        raise ValueError("Ticket title must be a valid string")
    if not isinstance(category, str):
        raise ValueError("Category must be a valid string")
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a valid string")

    if isinstance(affected_users, bool):
        raise ValueError("Affected users cannot be a boolean value") 
    if not isinstance(affected_users, int) or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer greater than zero.")   
        
 # normalizing valid case variations
    nocase_category = category.strip().capitalize()
    nocase_urgency = urgency.strip().lower()

#field requirements
    if not title or not title.strip():         # Check1: Reject empty or whitespace-only titles
        raise ValueError("Ticket title cannot be empty or whitespace-only.")
    
    if nocase_category not in allowed_categories:       # Check2: Reject unsupported categories
        raise ValueError(f"Invalid category. Must be one of {allowed_categories}")
 
    if nocase_urgency not in allowed_urgency_levels:          #Check3: Reject invalid urgency values
        raise ValueError(f"Invalid urgency. Must be one of {allowed_urgency_levels}")
        
    
    ticket_id = next_ticket_id(existing_tickets)  #to generate next idea sequentially
    priority_level = calculate_priority(urgency, affected_users)   #using the func to calc.  priority level
    
    return {                                #Assemble and return the complete 8-key dictionary contract
        "id": ticket_id,
        "title": title.strip(),
        "category": nocase_category,
        "urgency": nocase_urgency,
        "affected_users": affected_users,
        "priority": priority_level,
        "status": "open",
        "assigned_to": None
    }

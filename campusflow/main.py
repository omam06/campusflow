from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_ticket_status
from campusflow.reports import get_active_queue, generate_report
from campusflow.storage import load_tickets, save_tickets

def main():
    saved_tickets = load_tickets()
    running = True
    while running:
        print()
        print("CAMPUSFLOW HELP DESK")
        print("1. Create ticket")
        print("2. View all tickets")
        print("3. Assign ticket")
        print("4. Update ticket status")
        print("5. View active ticket queue")
        print("6. Generate report")
        print("7. Save and exit")
    
        user_input = input("Pick an option: ")
    
        if user_input == "1":
            user_title = input("Enter title: ")
            user_category = input("Enter category: ")
            user_urgency = input("Enter urgency level: ")
            try:
                users_affected = int(input("Enter number of affected users: "))
                next_ticket = create_ticket(saved_tickets, user_title, user_category, user_urgency, users_affected)
                if next_ticket:
                    saved_tickets.append(next_ticket)
                    save_tickets(saved_tickets)  #Saving the updated list with our imported persistence function save_tickets()
                    print(f"{next_ticket['id']} - {next_ticket['title']} created and saved successfully")
        
            except ValueError as e:
                print(e)
                continue
        

        elif user_input == "2":
            if not saved_tickets:
                print("No tickets to display")
            else:
                for each_ticket in saved_tickets:
                    print(each_ticket)
    
        elif user_input == "3":
            user_id = input("Enter ticket ID: ").strip().upper()
            worker = input("Enter worker name: ")
            assigned_ticket = assign_ticket(saved_tickets, user_id, worker)
            if assigned_ticket is True:
                print("Ticket assigned successfully")
                save_tickets(saved_tickets)
            else:
                print("Oops, cannot assign ticket")

        elif user_input == "4":
            user_tick_id = input("Enter ticket ID: ").strip().upper()
            user_status = input("Enter new status: ").strip().lower()
            updated_ticket = update_ticket_status(saved_tickets, user_tick_id, user_status)
            if updated_ticket is True:
                print("Status was updated")
                save_tickets(saved_tickets)
            else:
                print("Status update rejected")


        elif user_input == "5":
            active_queue = get_active_queue(saved_tickets)
            if not active_queue:
                print("Sorry, empty queue")
            else:
                for eachticket in active_queue:
                    print(eachticket)

        elif user_input == "6":
            generated_report = generate_report(saved_tickets)
            print(f"Total Ticket(s): {generated_report['total']}, By order of status: {generated_report['by_status']}, By order of priority: {generated_report['by_priority']}")

        elif user_input == "7":
            save_tickets(saved_tickets)
            running = False
            print("Goodbye")

        else:
            print("Invalid option. Please try again.")
    running = False
main()
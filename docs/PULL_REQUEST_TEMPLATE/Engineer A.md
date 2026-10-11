# PR Title

`feat: implement ticket creation and validation`

## Related Issue

N/A — add the issue number if one exists.

## 1. What changed?

* Implemented ticket creation and input validation in `campusflow/tickets.py`.
* Added sequential ticket ID generation (`T001`, `T002`, and so on).
* Added validation for ticket titles, categories, urgency levels, and affected-user counts.
* Implemented automatic priority calculation based on urgency and the number of affected users.
* Added tests in `tests/test_tickets.py` covering valid ticket creation, invalid inputs, priority rules, and ID generation.

## 2. How does it work?

* `create_ticket()` validates the supplied ticket details and returns a ticket dictionary containing the ID, title, category, urgency, affected-user count, priority, initial status, and assignee.
* `next_ticket_id()` determines the next sequential ID from the existing tickets.
* `calculate_priority()` applies the project's priority rules.
* Invalid ticket details raise `ValueError`, preventing rejected tickets from being added to the stored ticket list by the caller.

## 3. How was it tested?

* **Command:** `python3 -m unittest discover -s tests -v`
* **Actual result:** The integrated test suite reported 42 tests passing, with no failures or errors after the branches were merged.
* **Edge cases verified:** Empty or whitespace-only titles, unsupported categories, invalid urgency, zero or negative affected-user counts, text and decimal user counts, Boolean user counts, invalid input types, sequential IDs, and priority calculations.
* **Additional verification:** The tests check that rejected ticket creation leaves the existing ticket list unchanged.

## 4. What did I learn with AI?

* **Concept explored:** Input validation, functions, dictionaries, sequential ID generation, and automated testing.
* **How I used AI:** Used AI to discuss implementation approaches, understand errors, and identify edge cases.
* **My verification:** Ran the ticket-creation tests as part of the integrated test suite.
* **Advice changed or rejected:** Document any suggestions that were modified or rejected during implementation; otherwise, state N/A.

## 5. Reviewer notes

* Check that ticket IDs remain unique and sequential when existing tickets are supplied.
* Verify that category and urgency normalization works for valid case variations.
* Review the priority calculation against the assessment's priority rules.
* Confirm that invalid input does not mutate existing ticket data.

## 6. Known limitations

* End-to-end behavior through the complete command-line interface must be verified after integration with `main.py`.
* No additional limitations are claimed without further verification.

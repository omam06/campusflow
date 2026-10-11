# Omale Moses - Engineer A
# Design Decisions — CampusFlow

# Data Architecture
Tickets are stored in a standard Python list containing 8-key dictionaries matching the specification contract exactly.

# Error Handling Contracts
- Validation and processing functions will raise a standard `ValueError` with clear contextual messaging on failure.
- The UI layer (`main.py`) will trap these errors inside try-except blocks to gracefully alert users without terminating execution.

# Storage Domain Ownership
- Module `storage.py` manages all disk serializations.
- Persistence targets native `.json` strings written to `data/tickets.json`, which is explicitly filtered from version control histories via local workspace rules.



# Reggie — Engineer B

## Decision 1 — Separating Application Startup into `main()`

**Context:** The interactive menu was executing as soon as `campusflow.main` was imported. This interfered with automated test discovery.

**Options considered:**

* Leave the menu loop at module level.
* Put the menu inside a `main()` function and call it only when the module is run directly.

**Decision:** Organize the menu inside `main()` and use the `if __name__ == "__main__":` guard.

**Reasoning:** This separates importing the module from starting the application. Tests can import `main()` without triggering interactive prompts, while users can still run the application normally.

**Consequences:** The application becomes easier to test and its startup behaviour is more predictable.

**Related files:** `campusflow/main.py`, `tests/test_main.py`

---

## Decision 2 — Keeping the Application Modular

**Context:** CampusFlow handles ticket creation, assignment, status updates, reporting, and persistence. Combining all this functionality in one file would make the program harder to maintain.

**Decision:** Keep related functionality in separate modules: `tickets.py`, `workflow.py`, `reports.py`, `storage.py`, and `main.py`.

**Reasoning:** Each module has a distinct responsibility. The menu coordinates the operations, while the other modules implement the relevant business logic or persistence behaviour.

**Consequences:** Individual functions can be tested independently, and changes to one responsibility are less likely to affect unrelated functionality.

**Related files:** `campusflow/tickets.py`, `campusflow/workflow.py`, `campusflow/reports.py`, `campusflow/storage.py`, `campusflow/main.py`

---

## Decision 3 — Using Mocking for Menu Tests

**Context:** Menu tests need predictable inputs and should not depend on existing saved tickets or modify real storage files.

**Options considered:**

* Manually run the menu and inspect each result.
* Use `unittest.mock.patch` to control input and replace storage dependencies during tests.

**Decision:** Use mocked input and mocked storage functions in `tests/test_main.py`.

**Reasoning:** Mocks make test scenarios repeatable and allow assertions about interactions, such as whether `save_tickets()` was called when the user exits.

**Consequences:** Menu behaviour can be tested automatically. The tests must still be designed to reflect the application's actual output and expected behaviour.

**Related file:** `tests/test_main.py`

---

## Decision 4 — Separating Report Data from Its Display

**Context:** `generate_report()` returns structured information containing the total ticket count, status counts, and priority counts. The menu displays that information to the user.

**Decision:** Keep report generation in `reports.py` and format the returned values in `main.py`.

**Reasoning:** The reporting function can be reused by other parts of the application without being tied to a particular display format. The menu is responsible for presenting the result to the user.

**Consequences:** Report calculations can be tested independently from menu output. Menu tests must assert the formatted output that the application actually displays.

**Related files:** `campusflow/reports.py`, `campusflow/main.py`, `tests/test_reports.py`, `tests/test_main.py`

---

## Decision 5 — Verifying Behaviour with Automated Tests

**Context:** CampusFlow includes validation, ticket workflows, queue ordering, reports, and persistence. Manual testing alone may miss edge cases.

**Decision:** Use Python's `unittest` framework to test individual functions and menu interactions.

**Reasoning:** Automated tests make expected behaviour repeatable and help detect regressions when the code changes.

**Consequences:** The test suite provides feedback on whether existing behaviour still works. A passing test only establishes the behaviour covered by that test, so meaningful assertions and additional edge cases remain important.

**Related files:** `tests/test_tickets.py`, `tests/test_workflow.py`, `tests/test_reports.py`, `tests/test_storage.py`, `tests/test_main.py`

# Design Decisions — CampusFlow

## Data Architecture
Tickets are stored in a standard Python list containing 8-key dictionaries matching the specification contract exactly.

## Error Handling Contracts
- Validation and processing functions will raise a standard `ValueError` with clear contextual messaging on failure.
- The UI layer (`main.py`) will trap these errors inside try-except blocks to gracefully alert users without terminating execution.

## Storage Domain Ownership
- Module `storage.py` manages all disk serializations.
- Persistence targets native `.json` strings written to `data/tickets.json`, which is explicitly filtered from version control histories via local workspace rules.

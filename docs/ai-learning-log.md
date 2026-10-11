# Omale Moses - Engineer A

# Interaction 1 — Package Initialization with __init__.py
Problem: I wasn't clear on what the empty `__init__.py` file inside Reggie's branch was doing.
My initial understanding: I thought it might be an extra setup file we could skip until the merge phase.
Prompt to AI: "Reggie's branch has it and __init__.py, whatsthe later for?"
Useful AI guidance: AI explained that `__init__.py` turns a standard directory into an importable Python package, which allows automated discovery tools like `unittest` to run properly.
My independent experiment/test: Verified our project structure and compared how root directories map files.
Verification source or result: Confirmed with official Python packaging documentation.
Decision: Accepted the structure and kept the file empty as recommended.
Related file/commit: `campusflow/__init__.py`

# Interaction 2 — Runtime Cache Exclusion via Gitignore
Problem: Compiled `.pyc` and `__pycache__` folders were showing up with green "U" indicators in my Git workflow status.
My initial understanding: I thought adding a file named `gitignore.md` or waiting until a main branch merge would handle tracking.
Prompt to AI: "i thought it goes in the gitignore.md"
Useful AI guidance: AI corrected my file naming mismatch, explaining that Git tracks exactly `.gitignore` without extensions, and that files already caught in tracking need a `git rm --cached` step.
My independent experiment/test: Created the exact `.gitignore` file, verified the files turned a faded gray in VS Code, and committed it.
Verification source or result: Terminal outputs cleanly executed deletions of tracked cache instances upon staging.
Decision: Modified tracking immediately rather than waiting for integration to prevent trunk pollution.
Related file/commit: `.gitignore`


# Interaction 3 — Critical Type Interception (Boolean & None Validation)
Problem: AI models frequently suggest `isinstance(val, int)` for numeric checks without accounting for Python's boolean implementation where `isinstance(True, int)` is true. Additionally, standard string functions like `.strip()` crash with an AttributeError if non-strings are passed.
My initial understanding: I assumed standard type checks caught all non-integers, and that invalid inputs would naturally drop into a standard catch-block.
Useful AI guidance: Identified how Python builds `bool` as a subclass of `int` and provided the explicit type checking blocks.
My independent experiment/test: Added explicit testing for type injection inside `test_tickets.py`.
Verification source or result: Tests failed initially when passing `True` or `None`, then passed after adding strict typing checks.
Decision: Improved the standard code pattern to proactively intercept boolean and non-string injections.


# Interaction 4 — Robust Exception Verification via assertRaisesRegex
Problem: Standard `assertRaises` passes on any matching exception type, meaning a test could green-light a failure if a `ValueError` was triggered by an unrelated validation mismatch.
My initial understanding: I thought checking the exception type alone was sufficient to prove an input was rejected correctly.
Prompt to AI: "how about the missing scenario frpm the question: low urgency + 4 users → medium... Make each one check which error was raised (look up assertRaisesRegex)"
Useful AI guidance: AI explained that `assertRaisesRegex` bounds the exception test to match specific internal string message substrings, preventing false positives.
My independent experiment/test: Implemented `assertRaisesRegex(ValueError, "Affected users must be a positive integer")` and intentionally changed the error string in `tickets.py` to see it fail.
Verification source or result: The test correctly caught the mismatch and failed until the error strings matched precisely.
Decision: Accepted and implemented across all negative validation assertions.
Related file/commit: `tests/test_tickets.py`

#5 
Using assertRaisesRegex guarantees that your test is passing for the exact right reason, which perfectly aligns with the guide's demand for "meaningful assertions and reliable behavior."
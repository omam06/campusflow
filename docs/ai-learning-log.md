# Omale Moses - Engineer A

# Interaction 1 — Package Initialization with __init__.py
Problem: I wasn't clear on what the empty `__init__.py` file inside Reggie's branch was doing.
My initial understanding: I thought it might be an extra setup file we could skip until the merge phase.
Prompt to AI: Reggie's branch has it and __init__.py, whatsthe later for?
Useful AI guidance: AI explained that `__init__.py` turns a standard directory into an importable Python package, which allows automated discovery tools like `unittest` to run properly.
My independent experiment/test: Verified our project structure and compared how root directories map files.
Verification source or result: Confirmed with official Python packaging documentation.
Decision: Accepted the structure and kept the file empty as recommended.
Related file/commit: `campusflow/__init__.py`

# Interaction 2 — Runtime Cache Exclusion via Gitignore
Problem: Compiled `.pyc` and `__pycache__` folders were showing up with green "U" indicators in my Git workflow status.
My initial understanding: I thought adding a file named `gitignore.md` or waiting until a main branch merge would handle tracking.
Prompt to AI: i thought it goes in the gitignore.md
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


# Regina Chijioke — Engineer B

## Interaction 1 — Preventing Application Execution During Imports

**Problem:** When running `python3 -m unittest discover -s tests -v`, the CampusFlow menu started running before the tests could be loaded correctly.

**My initial understanding:** I thought the problem was caused by the report output or by the way `unittest` discovered the test files.

**Prompt to AI:** "why this crash" — followed by the traceback showing that `test_main.py` could not import `main`.

**Useful AI guidance:** AI explained the difference between defining a function and executing application code at module level. It guided me to put the menu logic inside `main()` and use the `if __name__ == "__main__":` guard to prevent the menu from running automatically during imports.

**My independent experiment/test:** Refactored `campusflow/main.py` to use a `main()` function and the direct-execution guard, then reran the test suite.

**Verification source or result:** The import error disappeared, and the menu-related tests began running. The test suite subsequently reported 47 tests, with remaining failures related to output expectations rather than importing `main`.

**Learning outcome:** I learned that Python executes top-level statements when a module is imported. Keeping application startup inside a function makes the application easier to test and reuse.

**Related file:** `campusflow/main.py`, `tests/test_main.py`

---

## Interaction 2 — Testing Interactive Menus with Mock Objects

**Problem:** I needed to test menu options without manually entering choices every time or relying on actual saved ticket data.

**My initial understanding:** I understood how to call functions and write assertions, but I was still learning how to test an interactive program that depends on `input()`, `print()`, and file storage.

**Prompt to AI:** I asked for a `test_main.py` written in the same `unittest` style as my existing report tests.

**Useful AI guidance:** AI introduced the use of `unittest.mock.patch` to replace dependencies temporarily. Mocking `input()` allows a test to supply menu choices automatically, while mocking `load_tickets()` and `save_tickets()` isolates the menu tests from persistent storage.

**My independent experiment/test:** Added tests for saving and exiting, invalid menu choices, viewing an empty ticket list, an empty active queue, and generating an empty report.

**Verification source or result:** The menu tests ran as part of the full test suite. The save-and-exit, invalid-choice, empty-list, and empty-queue tests passed.

**Learning outcome:** I learned that mocks let me control dependencies and inspect how a function interacts with them without requiring real user input or file operations.

**Related file:** `tests/test_main.py`

---

## Interaction 3 — Aligning Report Tests with Actual Program Output

**Problem:** My empty-report test failed because it expected `print()` to receive a dictionary, while the menu displayed a formatted string containing the report values.

**My initial understanding:** I initially treated the report data returned by `generate_report()` and the text displayed by the menu as if they were the same output.

**Prompt to AI:** I asked for the correct test case after the report assertion failed.

**Useful AI guidance:** AI explained that a test assertion must match the behaviour being tested. Since the menu formats the report into a string, the test should verify the expected formatted output rather than expect the original dictionary to be printed.

**My independent experiment/test:** Updated the report test to expect a formatted string and reran the test suite.

**Verification source or result:** The test still failed because the expected string was not found among the captured `print()` calls. The next debugging step is to inspect `mock_print.call_args_list` and compare the actual captured output with the expected string.

**Learning outcome:** I learned that exact-output assertions are sensitive to differences in wording, punctuation, and formatting. I also learned to inspect mock call history when an assertion fails rather than assume the expected output is correct.

**Related file:** `campusflow/main.py`, `tests/test_main.py`

---

## Interaction 4 — Controlling a Menu Loop

**Problem:** I needed the menu to keep accepting choices until the user selected the save-and-exit option.

**My initial understanding:** I knew that a `while` loop repeats while its condition is true, but I needed to understand how to end the loop from a particular menu option.

**Prompt to AI:** "how to end while"

**Useful AI guidance:** AI explained that a loop can stop when its condition becomes false or when `break` is executed. It recommended using the existing `running` variable and setting it to `False` when the user chooses option 7.

**My independent experiment/test:** Updated the exit option to save the ticket list, change `running` to `False`, and display a goodbye message.

**Verification source or result:** The menu displayed "Goodbye" after option 7, and the save-and-exit unit test passed.

**Learning outcome:** I learned how a Boolean control variable manages the lifetime of a menu loop and how to save application state before exiting.

**Related file:** `campusflow/main.py`, `tests/test_main.py`

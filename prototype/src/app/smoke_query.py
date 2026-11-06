"""Smoke run for #62: prove we can reach SonarX's Snowflake account.

Run from prototype/:  python src/app/smoke_query.py
Prints the row count and the account, warehouse, database and schema the
session landed in. Never prints the password.
"""
from __future__ import annotations  # allow modern type hints

import sys  # exit codes and the import path
from pathlib import Path  # find prototype/src from this file

# Make prototype/src importable when this file is run directly as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # prototype/src

from config.settings import MissingSettingsError, load_settings  # noqa: E402  validated settings
from database.snowflake_client import fetch_rows, smoke_query_text  # noqa: E402  the query runner


def main() -> int:
    """Run the smoke query and return a process exit code."""
    try:  # settings may be missing on a fresh machine
        settings = load_settings()  # read and validate the SNOWFLAKE_ variables
    except MissingSettingsError as error:  # tell the user which variables to set
        print(error, file=sys.stderr)  # the message names variables only, never values
        return 2  # exit code 2 means configuration problem
    rows = fetch_rows(settings, smoke_query_text)  # run the smoke query
    print(f"smoke query returned {len(rows)} row(s)")  # the row count the #62 PR asks for
    for row in rows:  # show where the session landed
        print("account, warehouse, database, schema:", row)  # contains no secrets
    return 0  # success


if __name__ == "__main__":  # only when run as a script
    raise SystemExit(main())  # pass the exit code to the shell

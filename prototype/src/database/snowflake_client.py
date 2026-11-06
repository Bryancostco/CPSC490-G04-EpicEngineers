"""Open read only connections to SonarX's Snowflake account and run queries.

Position matching, PNL and ranking never import this module; they work on plain
records so they can be tested on fixtures without credentials (#84).
"""
from __future__ import annotations  # allow modern type hints

from collections.abc import Callable, Iterator  # types for the injectable connect function and the context manager
from contextlib import contextmanager  # turn snowflake_connection into a with block
from typing import Any  # connector objects are untyped

from config.settings import SnowflakeSettings  # validated connection settings

# The query the smoke run uses: it touches no SonarX table, so it proves the connection only.
smoke_query_text = "select current_account(), current_warehouse(), current_database(), current_schema()"


def default_connect(**arguments: str) -> Any:
    """Open a real connection; imported here so tests and fixture runs never need the connector."""
    import snowflake.connector  # imported lazily so a missing package only fails live runs

    return snowflake.connector.connect(**arguments)  # open the connection with the given settings


@contextmanager  # lets callers write: with snowflake_connection(settings) as connection
def snowflake_connection(
    settings: SnowflakeSettings,  # where and how to connect
    connect: Callable[..., Any] = default_connect,  # injectable so tests can pass a fake
) -> Iterator[Any]:
    """Yield an open connection and always close it, even if the caller raises."""
    connection = connect(**settings.connector_arguments())  # open the connection
    try:  # hand the connection to the caller
        yield connection  # the caller's with block runs here
    finally:  # runs on success and on error
        connection.close()  # never leave a session open in SonarX's account


def fetch_rows(
    settings: SnowflakeSettings,  # where and how to connect
    query_text: str,  # the read only query to run
    parameters: tuple[Any, ...] = (),  # bound values, never pasted into the query text
    connect: Callable[..., Any] = default_connect,  # injectable so tests can pass a fake
) -> list[tuple[Any, ...]]:
    """Run one query and return every row."""
    with snowflake_connection(settings, connect) as connection:  # open and later close the connection
        cursor = connection.cursor()  # cursor that runs the query
        try:  # make sure the cursor closes too
            cursor.execute(query_text, parameters)  # run the query with bound parameters
            return list(cursor.fetchall())  # read every row into a list
        finally:  # runs on success and on error
            cursor.close()  # release the cursor

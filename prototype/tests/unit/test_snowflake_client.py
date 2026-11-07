"""Tests for #62: the Snowflake client opens, uses and always closes its connection, with a fake connector."""
import pytest  # test runner

from config.settings import load_settings  # builds settings from a fake environment
from database.snowflake_client import fetch_rows, snowflake_connection  # the module under test

# Fake settings; none of these are real credentials.
fake_settings = load_settings({
    "SNOWFLAKE_ACCOUNT": "test_account",  # fake account
    "SNOWFLAKE_USER": "test_user",  # fake user
    "SNOWFLAKE_PASSWORD": "fake-password-for-tests",  # pragma: allowlist secret (fake test value)
    "SNOWFLAKE_WAREHOUSE": "test_warehouse",  # fake warehouse
    "SNOWFLAKE_DATABASE": "test_database",  # fake database
    "SNOWFLAKE_SCHEMA": "test_schema",  # fake schema
})  # end of the fake settings


class FakeCursor:
    """Stands in for a Snowflake cursor and records what was run."""

    def __init__(self, rows):
        self.rows = rows  # rows this cursor will return
        self.executed = []  # every (query, parameters) pair run on it
        self.closed = False  # whether close was called

    def execute(self, query_text, parameters):
        self.executed.append((query_text, parameters))  # remember the call

    def fetchall(self):
        return self.rows  # hand back the canned rows

    def close(self):
        self.closed = True  # remember the cursor was released


class FakeConnection:
    """Stands in for a Snowflake connection and records whether it was closed."""

    def __init__(self, rows):
        self.cursor_object = FakeCursor(rows)  # the single cursor this connection gives out
        self.closed = False  # whether close was called

    def cursor(self):
        return self.cursor_object  # always the same fake cursor

    def close(self):
        self.closed = True  # remember the connection was closed


def test_connect_receives_the_settings():
    """The connector is called with the account, user and other settings from the environment."""
    received = {}  # arguments the fake connector saw
    connection = FakeConnection([])  # connection to return

    def fake_connect(**arguments):
        received.update(arguments)  # record what was passed
        return connection  # hand back the fake connection

    with snowflake_connection(fake_settings, fake_connect):  # open and close once
        pass  # nothing to do inside
    assert received["account"] == "test_account"  # account came from settings
    assert received["warehouse"] == "test_warehouse"  # warehouse came from settings


def test_connection_closes_even_when_the_caller_fails():
    """A failure inside the with block still closes the session in SonarX's account."""
    connection = FakeConnection([])  # connection to watch
    with pytest.raises(RuntimeError):  # the error must still reach the caller
        with snowflake_connection(fake_settings, lambda **arguments: connection):  # open the fake connection
            raise RuntimeError("query failed")  # simulate a failing query
    assert connection.closed  # the connection was closed anyway


def test_fetch_rows_binds_parameters_and_closes_everything():
    """Values are bound, never pasted into the query, and both cursor and connection close."""
    connection = FakeConnection([("row one",), ("row two",)])  # two canned rows
    rows = fetch_rows(  # run a query through the fake connector
        fake_settings,  # fake settings
        "select * from trades where wallet = %s",  # query with a placeholder
        ("0xabc",),  # the bound value
        connect=lambda **arguments: connection,  # use the fake connection
    )  # end of the call
    assert rows == [("row one",), ("row two",)]  # every row returned
    assert connection.cursor_object.executed == [("select * from trades where wallet = %s", ("0xabc",))]  # value bound, not pasted
    assert connection.cursor_object.closed  # cursor released
    assert connection.closed  # connection closed

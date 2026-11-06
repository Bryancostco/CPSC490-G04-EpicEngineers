"""Live smoke test for #62: runs only when SonarX Snowflake credentials are set locally; skipped in CI."""
import pytest  # test runner and skip support

from config.settings import has_snowflake_settings, load_settings  # credential check and loader
from database.snowflake_client import fetch_rows, smoke_query_text  # the query runner and smoke query

# Skip every test in this file unless all SNOWFLAKE_ variables are set (CI has none).
pytestmark = [  # markers applied to the whole module
    pytest.mark.snowflake,  # label these as needing live credentials
    pytest.mark.skipif(not has_snowflake_settings(), reason="SNOWFLAKE_ variables not set"),  # skip without them
]  # end of the markers


def test_smoke_query_returns_one_row():
    """The smoke query reaches SonarX's account and returns exactly one row."""
    rows = fetch_rows(load_settings(), smoke_query_text)  # run the live query
    assert len(rows) == 1  # one row naming the account, warehouse, database and schema

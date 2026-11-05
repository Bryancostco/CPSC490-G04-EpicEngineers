"""Tests for #62: Snowflake settings come only from environment variables and fail safely."""
from pathlib import Path  # locate prototype/.env.example

import pytest  # test runner and assertions on raised errors

from config.settings import (  # the module under test
    MissingSettingsError,  # raised when settings are incomplete
    has_snowflake_settings,  # tells live tests whether to run
    load_settings,  # builds the settings record
    required_variable_names,  # the variables that must be set
)  # end of imports

# A complete set of fake settings; none of these are real credentials.
fake_environment = {
    "SNOWFLAKE_ACCOUNT": "test_account",  # fake account
    "SNOWFLAKE_USER": "test_user",  # fake user
    "SNOWFLAKE_PASSWORD": "fake-password-for-tests",  # pragma: allowlist secret (fake test value)
    "SNOWFLAKE_WAREHOUSE": "test_warehouse",  # fake warehouse
    "SNOWFLAKE_DATABASE": "test_database",  # fake database
    "SNOWFLAKE_SCHEMA": "test_schema",  # fake schema
}  # end of the fake environment


def test_complete_environment_loads():
    """Every required variable set gives a usable settings record."""
    settings = load_settings(fake_environment)  # load from the fake source
    assert settings.account == "test_account"  # account copied through
    assert settings.role is None  # role is optional and absent here


def test_missing_variable_is_named_and_values_are_not_leaked():
    """A missing variable stops the run, and the error names it without printing any value."""
    environment = dict(fake_environment)  # copy so the shared fake stays intact
    del environment["SNOWFLAKE_WAREHOUSE"]  # remove one required variable
    with pytest.raises(MissingSettingsError) as error:  # loading must fail
        load_settings(environment)  # try to load incomplete settings
    message = str(error.value)  # the text a user would see
    assert "SNOWFLAKE_WAREHOUSE" in message  # the missing name is reported
    assert "fake-password-for-tests" not in message  # the password never appears


def test_blank_variable_counts_as_missing():
    """A variable set to only spaces is treated as unset, so a blank .env.example copy fails safely."""
    environment = dict(fake_environment, SNOWFLAKE_PASSWORD="   ")  # blank password
    with pytest.raises(MissingSettingsError):  # loading must fail
        load_settings(environment)  # try to load with a blank password


def test_password_is_hidden_from_repr():
    """Printing or logging the settings never shows the password."""
    settings = load_settings(fake_environment)  # load valid settings
    assert "fake-password-for-tests" not in repr(settings)  # repr leaves the password out


def test_role_is_passed_only_when_set():
    """The optional role reaches the connector only when it is configured."""
    without_role = load_settings(fake_environment).connector_arguments()  # no role set
    with_role = load_settings(dict(fake_environment, SNOWFLAKE_ROLE="analyst")).connector_arguments()  # role set
    assert "role" not in without_role  # absent when unset
    assert with_role["role"] == "analyst"  # present when set


def test_has_snowflake_settings_reports_completeness():
    """Live tests can ask whether credentials exist before trying to connect."""
    assert has_snowflake_settings(fake_environment)  # complete settings
    assert not has_snowflake_settings({})  # nothing set


def test_env_example_lists_every_required_variable_with_a_blank_value():
    """The committed template names every variable and holds no values (CI gate G5)."""
    example_path = Path(__file__).resolve().parents[2] / ".env.example"  # prototype/.env.example
    lines = [  # every non comment, non empty line of the template
        line.strip()  # drop surrounding whitespace
        for line in example_path.read_text(encoding="utf-8").splitlines()  # read the template
        if line.strip() and not line.strip().startswith("#")  # skip comments and blanks
    ]  # end of the list
    assignments = dict(line.split("=", 1) for line in lines)  # name to value pairs
    for name in required_variable_names:  # check every required variable
        assert name in assignments  # the template names it
        assert assignments[name] == ""  # and leaves it blank

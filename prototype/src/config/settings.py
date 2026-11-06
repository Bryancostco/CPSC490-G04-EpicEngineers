"""Load and validate the Snowflake connection settings (docs/design/implementation.md §3).

Settings come only from environment variables, optionally filled from a local,
untracked prototype/.env file. Nothing here ever prints or logs the password.
"""
from __future__ import annotations  # allow modern type hints such as str | None

import os  # read the process environment
from collections.abc import Mapping  # type for any dict like source of settings
from dataclasses import dataclass, field  # build an immutable settings record
from pathlib import Path  # locate prototype/.env relative to this file

from dotenv import load_dotenv  # copy values from a local .env file into os.environ

# Path to prototype/.env: this file is prototype/src/config/settings.py, so go up three levels.
default_env_file = Path(__file__).resolve().parents[2] / ".env"

# Variables that must be set before the prototype may connect to Snowflake.
required_variable_names = (
    "SNOWFLAKE_ACCOUNT",  # account identifier SonarX gives us
    "SNOWFLAKE_USER",  # our Snowflake user name
    "SNOWFLAKE_PASSWORD",  # our Snowflake password, from the SonarX Slack only
    "SNOWFLAKE_WAREHOUSE",  # warehouse that runs our read only queries
    "SNOWFLAKE_DATABASE",  # database holding the Polymarket tables
    "SNOWFLAKE_SCHEMA",  # schema holding the Polymarket tables
)  # end of the required names

# Variables that may be left blank.
optional_variable_names = ("SNOWFLAKE_ROLE",)  # role, only if SonarX assigns one


class MissingSettingsError(Exception):
    """Raised when required Snowflake settings are missing; the message names variables, never values."""


@dataclass(frozen=True)  # settings never change after loading
class SnowflakeSettings:
    """Everything the Snowflake connector needs to open a connection."""

    account: str  # SNOWFLAKE_ACCOUNT
    user: str  # SNOWFLAKE_USER
    password: str = field(repr=False)  # SNOWFLAKE_PASSWORD, hidden from repr so it never reaches a log
    warehouse: str = ""  # SNOWFLAKE_WAREHOUSE
    database: str = ""  # SNOWFLAKE_DATABASE
    schema: str = ""  # SNOWFLAKE_SCHEMA
    role: str | None = None  # SNOWFLAKE_ROLE, or None when not set

    def connector_arguments(self) -> dict[str, str]:
        """Return the keyword arguments snowflake.connector.connect expects."""
        arguments = {  # start with the values every connection needs
            "account": self.account,  # which Snowflake account to reach
            "user": self.user,  # who we log in as
            "password": self.password,  # how we authenticate
            "warehouse": self.warehouse,  # where queries run
            "database": self.database,  # default database for queries
            "schema": self.schema,  # default schema for queries
        }  # end of the required arguments
        if self.role:  # only pass a role when one was configured
            arguments["role"] = self.role  # add the optional role
        return arguments  # hand the arguments to the caller


def read_environment(env_file: Path | None = None) -> Mapping[str, str]:
    """Return os.environ after loading the local .env file, without overriding variables already set."""
    load_dotenv(env_file or default_env_file, override=False)  # fill gaps from .env if the file exists
    return os.environ  # the process environment now holds both sources


def missing_variable_names(environment: Mapping[str, str]) -> list[str]:
    """Return the required variable names that are unset or blank."""
    return [  # build the list of names with no usable value
        name  # keep the name only, never the value
        for name in required_variable_names  # check every required variable
        if not environment.get(name, "").strip()  # unset or whitespace only counts as missing
    ]  # end of the list


def has_snowflake_settings(environment: Mapping[str, str] | None = None) -> bool:
    """Return True when every required variable is set, so live tests know whether to run."""
    source = environment if environment is not None else read_environment()  # use the given source or the real one
    return not missing_variable_names(source)  # True only when nothing is missing


def load_settings(environment: Mapping[str, str] | None = None) -> SnowflakeSettings:
    """Build SnowflakeSettings, or raise MissingSettingsError naming every missing variable."""
    source = environment if environment is not None else read_environment()  # use the given source or the real one
    missing = missing_variable_names(source)  # find anything that is not set
    if missing:  # refuse to continue without full settings (fail safely, implementation.md §3)
        raise MissingSettingsError(  # stop with a message that is safe to print
            "Missing Snowflake settings: " + ", ".join(missing)  # list the variable names only
            + ". Copy prototype/.env.example to prototype/.env and fill them in."  # tell the reader how to fix it
        )  # end of the error
    role = source.get("SNOWFLAKE_ROLE", "").strip() or None  # blank role becomes None
    return SnowflakeSettings(  # build the immutable settings record
        account=source["SNOWFLAKE_ACCOUNT"].strip(),  # account identifier
        user=source["SNOWFLAKE_USER"].strip(),  # user name
        password=source["SNOWFLAKE_PASSWORD"],  # password exactly as given, spaces and all
        warehouse=source["SNOWFLAKE_WAREHOUSE"].strip(),  # warehouse name
        database=source["SNOWFLAKE_DATABASE"].strip(),  # database name
        schema=source["SNOWFLAKE_SCHEMA"].strip(),  # schema name
        role=role,  # optional role
    )  # end of the settings record

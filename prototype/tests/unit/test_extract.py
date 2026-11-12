import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import pytest

from src.database.extract import (
    ExtractionError, SourceSchema, build_trades_sql, build_resolutions_sql,
    fetch_trades, fetch_resolutions,
)

FIXTURE_PATH = Path(__file__).parents[1] / "fixtures" / "pnl_worked_example.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
T = datetime.fromisoformat(FIXTURE["as_of"]["m1_resolved"])
T_UNRESOLVED = datetime.fromisoformat(FIXTURE["as_of"]["m1_unresolved"])

class Cursor:
    def __init__(self, rows, columns):
        self.rows, self.description = rows, [(c,) for c in columns]
        self.params = None
        self.sql = None
        self.closed = False
    def execute(self, sql, params):
        self.sql, self.params = sql, params
    def fetchall(self): return self.rows
    def close(self): self.closed = True

class Connection:
    def __init__(self, cursor): self.c = cursor
    def cursor(self): return self.c

def test_fixture_uses_exact_decimal_strings():
    assert FIXTURE["trades"][0]["shares"] == "100"
    assert FIXTURE["trades"][0]["price"] == "0.40"
    assert Decimal(FIXTURE["trades"][0]["price"]) == Decimal("0.40")
    assert Decimal(FIXTURE["resolutions"][0]["payout_per_share"]["M1_YES"]) == Decimal("1.00")

def test_trade_query_is_select_only_half_open_twelve_month_window_and_chain_ordered():
    sql = build_trades_sql().upper()
    assert sql.startswith("SELECT")
    assert "DATEADD(MONTH, -12, %S)" in sql and " < %S" in sql
    assert "ORDER BY BLOCK_NUMBER, LOG_INDEX" in sql
    assert not any(word in sql for word in ("INSERT ", "UPDATE ", "DELETE ", "MERGE "))

def test_resolution_query_is_select_only_and_as_of_bounded():
    sql = build_resolutions_sql().upper()
    assert sql.startswith("SELECT")
    assert "SELECT DISTINCT MARKET_ID" in sql
    assert "RESOLVED_AT <= %S" in sql
    assert not any(word in sql for word in ("INSERT ", "UPDATE ", "DELETE ", "MERGE "))

def test_trade_fetch_binds_same_as_of_for_start_and_exclusive_end():
    cols = ["WALLET","MARKET","OUTCOME_TOKEN","SIDE","SHARES","PRICE","BLOCK_NUMBER","LOG_INDEX","BLOCK_TIME"]
    row = ("0xwallet_w","M1","M1_YES","buy",Decimal("100"),Decimal("0.40"),100,0,datetime.fromisoformat("2026-01-10T00:00:00+00:00"))
    c = Cursor([row], cols)
    result = fetch_trades(Connection(c), T)
    assert result[0]["SHARES"] == Decimal("100")
    assert result[0]["PRICE"] == Decimal("0.40")
    assert c.params == (T,T) and c.closed

def test_resolution_fetch_binds_window_and_as_of():
    cols = ["MARKET","RESOLVED_AT","PAYOUT_PER_SHARE"]
    row = ("M1",datetime.fromisoformat("2026-03-01T00:00:00+00:00"),{"M1_YES":Decimal("1.00"),"M1_NO":Decimal("0.00")})
    c = Cursor([row], cols)
    result = fetch_resolutions(Connection(c), T)
    assert result[0]["PAYOUT_PER_SHARE"]["M1_YES"] == Decimal("1.00")
    assert c.params == (T,T,T)

def test_empty_results_return_empty_list():
    assert fetch_trades(Connection(Cursor([],["WALLET"])), T) == []
    assert fetch_resolutions(Connection(Cursor([],["MARKET"])), T) == []

def test_naive_datetime_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        fetch_trades(Connection(Cursor([],[])), datetime(2026,4,1))

def test_unsafe_identifiers_rejected():
    with pytest.raises(ValueError, match="Unsafe Snowflake identifier"):
        build_trades_sql(SourceSchema(trades_table="TRADES; DROP TABLE X"))

def test_common_query_failure_is_wrapped_without_exposing_details():
    class Broken(Cursor):
        def execute(self, sql, params): raise RuntimeError("password=secret")
    with pytest.raises(ExtractionError) as err:
        fetch_trades(Connection(Broken([],[])), T)
    assert "secret" not in str(err.value)

def test_example_dates_define_t_and_m1_resolution_cases():
    assert T.isoformat() == "2026-04-01T00:00:00+00:00"
    assert T_UNRESOLVED.isoformat() == "2026-02-25T00:00:00+00:00"
    m1 = datetime.fromisoformat(FIXTURE["resolutions"][0]["resolved_at"])
    assert m1 > T_UNRESOLVED and m1 <= T


def test_fixture_contains_expected_trades_in_twelve_month_window():
    from datetime import timedelta

    start = T.replace(year=T.year - 1)

    trades = FIXTURE["trades"]

    # Include start date, exclude end date.
    matching_trades = [
        trade for trade in trades
        if start <= datetime.fromisoformat(trade["block_time"]) < T
    ]

    assert len(matching_trades) == 4

    assert [trade["market"] for trade in matching_trades] == [
        "M1", "M1", "M1", "M2"
    ]


def test_trade_at_exclusive_end_timestamp_is_excluded():
    from datetime import timedelta

    end_trade = {
        "market": "M3",
        "block_time": T.isoformat()
    }

    assert not (
        datetime.fromisoformat(end_trade["block_time"]) < T
    )


def test_resolutions_respect_as_of_timestamp():
    resolutions = FIXTURE["resolutions"]

    unresolved_results = [
        r for r in resolutions
        if datetime.fromisoformat(r["resolved_at"]) <= T_UNRESOLVED
    ]

    resolved_results = [
        r for r in resolutions
        if datetime.fromisoformat(r["resolved_at"]) <= T
    ]

    assert [r["market"] for r in unresolved_results] == ["M2"]
    assert [r["market"] for r in resolved_results] == ["M1", "M2"]


def test_resolution_query_uses_trade_window_and_as_of_parameter():
    sql = build_resolutions_sql().upper()

    assert "DATEADD(MONTH, -12, %S)" in sql
    assert " < %S" in sql
    assert "RESOLVED_AT <= %S" in sql


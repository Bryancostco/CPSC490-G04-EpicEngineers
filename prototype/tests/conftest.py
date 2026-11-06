"""Shared test fixtures: the PNL spec's worked example as Trade records (docs/specs/pnl-calculation.md)."""
import json  # read the fixture file
from datetime import datetime  # parse block times
from decimal import Decimal  # exact numbers (NFR-2)
from pathlib import Path  # locate the fixture file

import pytest  # fixture decorator

from services.positions import Trade  # the trade record under test

# Path to the worked example fixture shared by #108, #109 and #110 onward.
worked_example_path = Path(__file__).resolve().parent / "fixtures" / "pnl_worked_example.json"


def make_trade(row: dict) -> Trade:
    """Turn one fixture row into a Trade, keeping shares and prices as exact decimals."""
    return Trade(  # build the record
        wallet=row["wallet"],  # proxy wallet address
        market=row["market"],  # market id
        outcome_token=row["outcome_token"],  # YES or NO token id
        side=row["side"],  # buy or sell
        shares=Decimal(row["shares"]),  # exact shares
        price=Decimal(row["price"]),  # exact price per share
        block_number=row["block_number"],  # chain order, first key
        log_index=row["log_index"],  # chain order within the block
        block_time=datetime.fromisoformat(row["block_time"]),  # when the block was mined
    )  # end of the record


@pytest.fixture
def worked_example() -> dict:
    """Return the raw worked example fixture (trades, resolutions and as of times)."""
    return json.loads(worked_example_path.read_text(encoding="utf-8"))  # parse the JSON file


@pytest.fixture
def worked_example_trades(worked_example) -> list[Trade]:
    """Return the worked example's trades as Trade records, in file order."""
    return [make_trade(row) for row in worked_example["trades"]]  # convert every row


def make_resolution(row: dict):
    """Turn one fixture row into a Resolution, with payouts as exact decimals."""
    from services.resolutions import Resolution  # imported here so #108's tests do not depend on #109's module

    return Resolution(  # build the record
        market=row["market"],  # market id
        resolved_at=datetime.fromisoformat(row["resolved_at"]),  # when the market resolved
        payout_per_share={token: Decimal(value) for token, value in row["payout_per_share"].items()},  # exact payouts
    )  # end of the record


@pytest.fixture
def worked_example_resolutions(worked_example) -> list:
    """Return the worked example's market resolutions as Resolution records."""
    return [make_resolution(row) for row in worked_example["resolutions"]]  # convert every row


@pytest.fixture
def worked_example_as_of(worked_example) -> dict[str, datetime]:
    """Return the worked example's two as of times: M1 unresolved and M1 resolved."""
    return {name: datetime.fromisoformat(value) for name, value in worked_example["as_of"].items()}  # parse both

from datetime import datetime
from decimal import Decimal

from src.services.positions import Trade
from src.services.pnl_ranking import build_wallet_summaries


def test_wallet_is_incomplete_if_any_position_is_incomplete():

    timestamp = datetime(2026, 1, 1)

    trades = [
        Trade(
            wallet="wallet_a",
            market="market_1",
            outcome_token="YES",
            side="buy",
            shares=Decimal("10"),
            price=Decimal("0.50"),
            block_number=1,
            log_index=0,
            block_time=timestamp,
        ),
        Trade(
            wallet="wallet_a",
            market="market_1",
            outcome_token="YES",
            side="sell",
            shares=Decimal("20"),
            price=Decimal("0.60"),
            block_number=2,
            log_index=0,
            block_time=timestamp,
        ),
        Trade(
            wallet="wallet_a",
            market="market_2",
            outcome_token="YES",
            side="buy",
            shares=Decimal("10"),
            price=Decimal("0.50"),
            block_number=3,
            log_index=0,
            block_time=timestamp,
        ),
    ]

    summaries = build_wallet_summaries(trades)

    assert len(summaries) == 1
    assert summaries[0].incomplete is True
    assert summaries[0].distinct_markets == 2
    assert summaries[0].trade_count == 3
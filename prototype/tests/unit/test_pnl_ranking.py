
from datetime import datetime, timezone
from decimal import Decimal

from services.positions import Trade
from services.pnl_ranking import build_wallet_rankings


def make_trade(wallet, side, shares, price, block, day=1):
    return Trade(
        wallet=wallet,
        market="M1",
        outcome_token="M1_YES",
        side=side,
        shares=Decimal(str(shares)),
        price=Decimal(str(price)),
        block_number=block,
        log_index=0,
        block_time=datetime(2026, 1, day, tzinfo=timezone.utc),
    )


# FR-1: Total PNL includes realized and unrealized PNL.
def test_fr1_wallet_total_pnl_sums_all_positions():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5.00")
        },
    )

    assert rankings[0].total_pnl == Decimal("5.00")


# FR-2: Total spent includes every buy.
def test_fr2_total_spent_sums_all_buys_in_window():
    trades = [
        make_trade("0xa", "buy", "10", "0.40", 1),
        make_trade("0xa", "buy", "20", "0.50", 2),
        make_trade("0xa", "sell", "5", "0.70", 3),
    ]

    rankings = build_wallet_rankings(trades)

    assert rankings[0].total_spent == Decimal("14.00")


# FR-3: ROI is calculated correctly.
def test_fr3_roi_is_calculated_when_total_spent_is_positive():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5.00")
        },
    )

    assert rankings[0].roi == Decimal("1")


# FR-3: ROI is empty when total spent is zero.
def test_fr3_roi_is_empty_when_total_spent_is_zero():
    trades = [
        make_trade("0xa", "sell", "10", "0.50", 1),
    ]

    rankings = build_wallet_rankings(trades)

    assert rankings[0].total_spent == Decimal("0")
    assert rankings[0].roi is None


# FR-4: Highest PNL ranks first, including negative PNL.
def test_fr4_wallets_rank_by_total_pnl_descending():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1),
        make_trade("0xb", "buy", "10", "0.50", 2),
        make_trade("0xc", "buy", "10", "0.50", 3),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("-5"),
            ("0xb", "M1", "M1_YES"): Decimal("10"),
            ("0xc", "M1", "M1_YES"): Decimal("2"),
        },
    )

    assert [r.wallet for r in rankings] == ["0xb", "0xc", "0xa"]
    assert [r.rank for r in rankings] == [1, 2, 3]


# FR-5: Higher ROI wins when PNL is equal.
def test_fr5_equal_pnl_uses_roi_as_tiebreaker():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1),
        make_trade("0xb", "buy", "20", "0.50", 2),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5"),
            ("0xb", "M1", "M1_YES"): Decimal("5"),
        },
    )

    assert [r.wallet for r in rankings] == ["0xa", "0xb"]


# FR-5: Empty ROI ranks after populated ROI.
def test_fr5_empty_roi_ranks_after_populated_roi():
    trades = [
        make_trade("0xa", "sell", "10", "0.50", 1),
        make_trade("0xb", "buy", "10", "0.50", 2),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5"),
            ("0xb", "M1", "M1_YES"): Decimal("5"),
        },
    )

    assert [r.wallet for r in rankings] == ["0xb", "0xa"]


# FR-5: Higher total spent wins the next tie.
def test_fr5_equal_pnl_and_roi_uses_total_spent():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1),
        make_trade("0xb", "buy", "20", "0.50", 2),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5"),
            ("0xb", "M1", "M1_YES"): Decimal("10"),
        },
    )

    assert [r.wallet for r in rankings] == ["0xb", "0xa"]


# FR-5: Earlier first trade wins.
def test_fr5_equal_pnl_roi_and_spent_uses_first_trade_time():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1, day=2),
        make_trade("0xb", "buy", "10", "0.50", 2, day=1),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5"),
            ("0xb", "M1", "M1_YES"): Decimal("5"),
        },
    )

    assert [r.wallet for r in rankings] == ["0xb", "0xa"]


# FR-5: Alphabetical wallet address resolves the final tie.
def test_fr5_final_tiebreaker_is_wallet_address():
    trades = [
        make_trade("0xb", "buy", "10", "0.50", 1),
        make_trade("0xa", "buy", "10", "0.50", 1),
    ]

    rankings = build_wallet_rankings(
        trades,
        unrealized_pnl={
            ("0xa", "M1", "M1_YES"): Decimal("5"),
            ("0xb", "M1", "M1_YES"): Decimal("5"),
        },
    )

    assert [r.wallet for r in rankings] == ["0xa", "0xb"]


# Additional safeguard: As-of filtering.
def test_as_of_time_ignores_trades_after_cutoff():
    trades = [
        make_trade("0xa", "buy", "10", "0.50", 1, day=1),
        make_trade("0xa", "buy", "10", "0.50", 2, day=2),
    ]

    rankings = build_wallet_rankings(
        trades,
        as_of=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    assert rankings[0].total_spent == Decimal("5.00")

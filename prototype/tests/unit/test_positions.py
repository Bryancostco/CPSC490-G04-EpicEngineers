"""Tests for #108: position grouping and lot building, FR-1 to FR-5 of docs/specs/pnl-calculation.md.

Each test is written so it fails if its requirement is removed from the code.
FR-6 (oldest lot first) and FR-7 (realized PNL) are tested in #110.
"""
from datetime import datetime, timezone  # block times for hand built trades
from decimal import Decimal  # exact numbers (NFR-2)

from services.positions import Trade, build_positions  # the code under test

# One shared block time for hand built trades whose time does not matter to the test.
some_time = datetime(2026, 1, 1, tzinfo=timezone.utc)


def trade(wallet, token, side, shares, price, block, log=0, market=None):
    """Build a Trade for a test; the market defaults to the token's prefix (M1_YES belongs to M1)."""
    return Trade(  # build the record
        wallet=wallet,  # proxy wallet
        market=market or token.split("_")[0],  # market id
        outcome_token=token,  # outcome token id
        side=side,  # buy or sell
        shares=Decimal(shares),  # exact shares
        price=Decimal(price),  # exact price
        block_number=block,  # chain order, first key
        log_index=log,  # chain order within the block
        block_time=some_time,  # time is not under test here
    )  # end of the record


def lot_summary(position):
    """Return the position's lots as (shares, price) pairs, oldest first."""
    return [(lot.shares, lot.price) for lot in position.lots]  # plain tuples are easy to compare


def test_fr1_one_position_per_wallet_market_and_outcome_token():
    """FR-1: a wallet holding YES and NO in one market has two positions, and other wallets stay separate."""
    trades = [  # three trades that must land in three positions
        trade("0xw", "M1_YES", "buy", "10", "0.40", 1),  # wallet w, YES
        trade("0xw", "M1_NO", "buy", "20", "0.55", 2),  # wallet w, NO in the same market
        trade("0xv", "M1_YES", "buy", "30", "0.45", 3),  # another wallet, YES
    ]  # end of trades
    positions = build_positions(trades)  # group them
    assert set(positions) == {("0xw", "M1", "M1_YES"), ("0xw", "M1", "M1_NO"), ("0xv", "M1", "M1_YES")}  # three keys
    assert lot_summary(positions[("0xw", "M1", "M1_NO")]) == [(Decimal("20"), Decimal("0.55"))]  # NO lot kept apart


def test_fr2_trades_apply_in_chain_order_across_blocks(worked_example_trades):
    """FR-2: the worked example's sell is listed first, but its block is last, so it must apply last."""
    shuffled = [worked_example_trades[2], worked_example_trades[1], worked_example_trades[0]]  # sell first in the list
    position = build_positions(shuffled)[("0xwallet_w", "M1", "M1_YES")]  # build position A
    assert not position.incomplete  # applied in block order, the sell is fully covered
    assert lot_summary(position) == [(Decimal("30"), Decimal("0.60"))]  # same lots as the spec


def test_fr2_trades_apply_in_chain_order_within_a_block():
    """FR-2: within one block, the earlier position in the block (log index) applies first."""
    trades = [  # listed sell first, but the buy sits earlier in the same block
        trade("0xw", "M1_YES", "sell", "40", "0.70", 5, log=7),  # later in block 5
        trade("0xw", "M1_YES", "buy", "40", "0.50", 5, log=2),  # earlier in block 5
    ]  # end of trades
    position = build_positions(trades)[("0xw", "M1", "M1_YES")]  # build the position
    assert not position.incomplete  # the buy came first, so the sell is covered
    assert position.shares_held() == Decimal("0")  # everything bought was sold


def test_fr3_each_buy_adds_a_lot_with_its_shares_and_price(worked_example_trades):
    """FR-3: after t1 and t2 position A holds L1 100 @ 0.40 and L2 50 @ 0.60, oldest first."""
    position = build_positions(worked_example_trades[:2])[("0xwallet_w", "M1", "M1_YES")]  # buys only
    assert lot_summary(position) == [(Decimal("100"), Decimal("0.40")), (Decimal("50"), Decimal("0.60"))]  # two lots


def test_fr4_a_sell_removes_the_sold_shares_from_the_lots(worked_example_trades):
    """FR-4: after the t3 sell of 120, position A holds only L2: 30 @ 0.60 (spec worked example)."""
    position = build_positions(worked_example_trades)[("0xwallet_w", "M1", "M1_YES")]  # all of position A
    assert lot_summary(position) == [(Decimal("30"), Decimal("0.60"))]  # 150 bought, 120 sold
    assert position.shares_held() == Decimal("30")  # what is left


def test_fr5_selling_more_than_held_matches_what_is_held_and_marks_incomplete():
    """FR-5: a sell of 130 against 100 held matches 100, flags the position and records 30 unmatched."""
    trades = [  # a wallet that bought before the window and sells inside it
        trade("0xw", "M1_YES", "buy", "100", "0.40", 1),  # only 100 held
        trade("0xw", "M1_YES", "sell", "130", "0.70", 2),  # sells 130
    ]  # end of trades
    position = build_positions(trades)[("0xw", "M1", "M1_YES")]  # build the position
    assert position.incomplete  # flagged
    assert position.unmatched_shares == Decimal("30")  # the shares with no lot
    assert sum(match.shares for match in position.sale_matches) == Decimal("100")  # only held shares matched
    assert position.lots == []  # nothing left


def test_a_complete_position_is_not_flagged(worked_example_trades):
    """Guard for FR-5: a covered sell leaves the position complete with zero unmatched shares."""
    position = build_positions(worked_example_trades)[("0xwallet_w", "M1", "M1_YES")]  # position A
    assert not position.incomplete  # the sell was covered
    assert position.unmatched_shares == Decimal("0")  # nothing unmatched


def test_trades_after_the_as_of_time_are_ignored(worked_example_trades):
    """The spec's as of time T: everything after T is ignored, so the t3 sell does not count before t3."""
    before_sell = datetime(2026, 1, 25, tzinfo=timezone.utc)  # between t2 and t3
    position = build_positions(worked_example_trades, as_of=before_sell)[("0xwallet_w", "M1", "M1_YES")]  # build at T
    assert position.shares_held() == Decimal("150")  # both buys, no sell yet


def test_shares_and_prices_stay_exact_decimals(worked_example_trades):
    """NFR-2: lots hold Decimal values, never binary floating point."""
    position = build_positions(worked_example_trades)[("0xwallet_w", "M1", "M1_YES")]  # position A
    assert all(isinstance(lot.shares, Decimal) and isinstance(lot.price, Decimal) for lot in position.lots)  # exact types

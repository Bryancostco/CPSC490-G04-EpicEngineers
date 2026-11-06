"""Tests for #109: resolution matching and open or closed status, FR-8 to FR-10 of docs/specs/pnl-calculation.md.

Each test is written so it fails if its requirement is removed from the code.
"""
from datetime import datetime, timezone  # times for hand built cases
from decimal import Decimal  # exact numbers (NFR-2)

import pytest  # error assertions

from services.positions import Trade, build_positions  # positions from #108
from services.resolutions import Resolution, closed_status, open_status, set_status  # the code under test

# Keys of the worked example's two positions.
position_a = ("0xwallet_w", "M1", "M1_YES")  # W holds YES in M1
position_b = ("0xwallet_w", "M2", "M2_NO")  # W holds NO in M2


def statuses_at(trades, resolutions, as_of):
    """Build positions as of T and return their statuses as of the same T."""
    positions = build_positions(trades, as_of=as_of)  # step 2 at T
    return set_status(positions, resolutions, as_of)  # step 3 at T


def test_fr8_a_market_resolved_at_or_before_t_closes_the_position(
    worked_example_trades, worked_example_resolutions, worked_example_as_of
):
    """FR-8: once M1 has resolved, position A is closed even though it still holds 30 shares."""
    statuses = statuses_at(worked_example_trades, worked_example_resolutions, worked_example_as_of["m1_resolved"])  # T after M1 resolves
    assert statuses[position_a].status == closed_status  # closed by the resolution
    assert statuses[position_a].resolution.payout_per_share["M1_YES"] == Decimal("1.00")  # payout ready for #110 (FR-11)


def test_fr8_resolution_exactly_at_t_counts(worked_example_trades, worked_example_resolutions):
    """FR-8 says "at or before T": a resolution at exactly T closes the position."""
    resolved_at = worked_example_resolutions[0].resolved_at  # M1's resolution time
    statuses = statuses_at(worked_example_trades, worked_example_resolutions, resolved_at)  # T equals that time
    assert statuses[position_a].status == closed_status  # closed at the boundary


def test_fr8_a_resolution_after_t_is_ignored(worked_example_trades, worked_example_resolutions, worked_example_as_of):
    """FR-8 only counts resolutions at or before T, so M1 resolving later leaves position A without one."""
    statuses = statuses_at(worked_example_trades, worked_example_resolutions, worked_example_as_of["m1_unresolved"])  # T before M1 resolves
    assert statuses[position_a].resolution is None  # the later resolution is not attached


def test_fr9_no_resolution_and_zero_shares_is_closed():
    """FR-9: everything bought was sold and the market has not resolved, so the position is closed."""
    when = datetime(2026, 1, 1, tzinfo=timezone.utc)  # any time before T
    trades = [  # buy 50, sell 50
        Trade("0xw", "M9", "M9_YES", "buy", Decimal("50"), Decimal("0.30"), 1, 0, when),  # buy
        Trade("0xw", "M9", "M9_YES", "sell", Decimal("50"), Decimal("0.45"), 2, 0, when),  # sell all
    ]  # end of trades
    statuses = statuses_at(trades, [], datetime(2026, 2, 1, tzinfo=timezone.utc))  # no resolutions at all
    assert statuses[("0xw", "M9", "M9_YES")].status == closed_status  # closed with zero shares


def test_fr10_no_resolution_and_shares_held_is_open(
    worked_example_trades, worked_example_resolutions, worked_example_as_of
):
    """FR-10: before M1 resolves, position A still holds 30 shares, so it is open (spec worked example)."""
    statuses = statuses_at(worked_example_trades, worked_example_resolutions, worked_example_as_of["m1_unresolved"])  # T before M1 resolves
    assert statuses[position_a].status == open_status  # open


def test_worked_example_position_b_is_closed_by_m2_resolving(
    worked_example_trades, worked_example_resolutions, worked_example_as_of
):
    """Spec worked example: M2 resolved YES before either T, so W's NO position is closed in both cases."""
    for as_of in worked_example_as_of.values():  # both as of times
        statuses = statuses_at(worked_example_trades, worked_example_resolutions, as_of)  # statuses at that T
        assert statuses[position_b].status == closed_status  # closed by M2's resolution
        assert statuses[position_b].resolution.payout_per_share["M2_NO"] == Decimal("0.00")  # the losing side pays nothing


def test_two_resolutions_for_one_market_are_rejected():
    """A market can resolve once; two records for it means the data is wrong, so stop instead of guessing."""
    when = datetime(2026, 1, 1, tzinfo=timezone.utc)  # any time
    duplicate = [  # the same market twice
        Resolution("M1", when, {"M1_YES": Decimal("1")}),  # first record
        Resolution("M1", when, {"M1_YES": Decimal("0")}),  # conflicting second record
    ]  # end of resolutions
    with pytest.raises(ValueError):  # must refuse
        set_status({}, duplicate, when)  # no positions needed to trigger the check

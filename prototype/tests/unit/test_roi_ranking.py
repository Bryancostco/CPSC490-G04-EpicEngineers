from datetime import datetime
from decimal import Decimal

import pytest

from src.services.pnl_ranking import (
    WalletRanking,
    RankingConfig,
    build_roi_rankings,
    build_pnl_rankings,
)


@pytest.fixture
def config():
    return RankingConfig(
        min_distinct_markets=10,
        min_trades=30,
        min_total_spent=Decimal("1000"),
        top_n=100,
    )


def make_wallet(
    wallet,
    roi="0.20",
    pnl="1000",
    spent="5000",
    markets=12,
    trades=40,
    first_trade=None,
    incomplete=False,
):
    return WalletRanking(
        wallet=wallet,
        total_pnl=Decimal(pnl),
        total_spent=Decimal(spent),
        roi=Decimal(roi) if roi is not None else None,
        first_trade=first_trade or datetime(2026, 1, 1),
        distinct_markets=markets,
        trade_count=trades,
        incomplete=incomplete,
    )


# --------------------------------------------------
# FR-6: Minimum activity thresholds
# --------------------------------------------------

def test_wallet_z_excluded_from_roi_but_present_in_pnl(config):

    wallet_z = make_wallet(
        "Z",
        roi="2.25",
        pnl="900",
        spent="400",
        markets=3,
        trades=8,
    )

    pnl_result = build_pnl_rankings([wallet_z], config)
    roi_result = build_roi_rankings([wallet_z], config)

    assert wallet_z.wallet in [w.wallet for w in pnl_result]
    assert wallet_z.wallet not in [w.wallet for w in roi_result]


@pytest.mark.parametrize(
    "markets,trades,spent",
    [
        (9, 30, "1000"),
        (10, 29, "1000"),
        (10, 30, "999.99"),
    ],
)
def test_roi_excludes_wallet_below_each_threshold(
    config,
    markets,
    trades,
    spent,
):

    wallet = make_wallet(
        "wallet_a",
        markets=markets,
        trades=trades,
        spent=spent,
    )

    result = build_roi_rankings([wallet], config)

    assert result == []


def test_roi_includes_wallet_meeting_all_thresholds(config):

    wallet = make_wallet(
        "wallet_a",
        markets=10,
        trades=30,
        spent="1000",
    )

    result = build_roi_rankings([wallet], config)

    assert len(result) == 1


# --------------------------------------------------
# FR-7: ROI descending
# --------------------------------------------------

def test_roi_sorted_highest_to_lowest(config):

    wallets = [
        make_wallet("A", roi="0.20"),
        make_wallet("B", roi="0.50"),
        make_wallet("C", roi="0.10"),
    ]

    result = build_roi_rankings(wallets, config)

    assert [w.wallet for w in result] == [
        "B",
        "A",
        "C",
    ]


# --------------------------------------------------
# FR-8: ROI tie-breaking
# --------------------------------------------------

def test_roi_tie_breaks_by_total_pnl(config):

    wallets = [
        make_wallet("A", roi="0.5000", pnl="1000"),
        make_wallet("B", roi="0.5000", pnl="2000"),
    ]

    result = build_roi_rankings(wallets, config)

    assert [w.wallet for w in result] == ["B", "A"]


def test_roi_tie_breaks_by_total_spent(config):

    wallets = [
        make_wallet("A", roi="0.5000", pnl="1000", spent="2000"),
        make_wallet("B", roi="0.5000", pnl="1000", spent="3000"),
    ]

    result = build_roi_rankings(wallets, config)

    assert [w.wallet for w in result] == ["B", "A"]


def test_roi_tie_breaks_by_earlier_first_trade(config):

    wallets = [
        make_wallet(
            "A",
            roi="0.5000",
            first_trade=datetime(2026, 2, 1),
        ),
        make_wallet(
            "B",
            roi="0.5000",
            first_trade=datetime(2026, 1, 1),
        ),
    ]

    result = build_roi_rankings(wallets, config)

    assert [w.wallet for w in result] == ["B", "A"]


def test_roi_tie_breaks_alphabetically_by_wallet(config):

    wallets = [
        make_wallet("wallet_b", roi="0.5000"),
        make_wallet("wallet_a", roi="0.5000"),
    ]

    result = build_roi_rankings(wallets, config)

    assert [w.wallet for w in result] == [
        "wallet_a",
        "wallet_b",
    ]


def test_roi_values_rounded_to_four_decimal_places(config):

    wallets = [
        make_wallet("A", roi="0.50004"),
        make_wallet("B", roi="0.50003"),
    ]

    result = build_roi_rankings(wallets, config)

    # Both round to 0.5000, so the alphabetical tie-break applies.
    assert [w.wallet for w in result] == ["A", "B"]


# --------------------------------------------------
# FR-9: Top N and configuration
# --------------------------------------------------

def test_roi_returns_only_top_n(config):

    small_config = RankingConfig(
        min_distinct_markets=10,
        min_trades=30,
        min_total_spent=Decimal("1000"),
        top_n=2,
    )

    wallets = [
        make_wallet("A", roi="0.10"),
        make_wallet("B", roi="0.30"),
        make_wallet("C", roi="0.20"),
    ]

    result = build_roi_rankings(wallets, small_config)

    assert len(result) == 2
    assert [w.wallet for w in result] == ["B", "C"]
    assert [w.rank for w in result] == [1, 2]


def test_pnl_returns_only_top_n(config):

    small_config = RankingConfig(
        top_n=2,
    )

    wallets = [
        make_wallet("A", pnl="100"),
        make_wallet("B", pnl="300"),
        make_wallet("C", pnl="200"),
    ]

    result = build_pnl_rankings(wallets, small_config)

    assert len(result) == 2
    assert [w.wallet for w in result] == ["B", "C"]


def test_roi_prints_configuration(config, capsys):

    build_roi_rankings([], config)

    output = capsys.readouterr().out

    assert "min_distinct_markets=10" in output
    assert "min_trades=30" in output
    assert "min_total_spent=1000" in output
    assert "top_n=100" in output


# --------------------------------------------------
# FR-10: Incomplete flag
# --------------------------------------------------

def test_roi_preserves_incomplete_flag(config):

    wallet = make_wallet(
        "A",
        incomplete=True,
    )

    result = build_roi_rankings([wallet], config)

    assert result[0].incomplete is True


def test_pnl_preserves_incomplete_flag(config):

    wallet = make_wallet(
        "A",
        incomplete=True,
    )

    result = build_pnl_rankings([wallet], config)

    assert result[0].incomplete is True


# --------------------------------------------------
# NFR-1: Deterministic rankings
# --------------------------------------------------

def test_roi_ranking_is_deterministic(config):

    wallets = [
        make_wallet("C", roi="0.30"),
        make_wallet("A", roi="0.30"),
        make_wallet("B", roi="0.20"),
    ]

    first = build_roi_rankings(wallets, config)
    second = build_roi_rankings(wallets, config)

    assert [w.wallet for w in first] == [
        w.wallet for w in second
    ]
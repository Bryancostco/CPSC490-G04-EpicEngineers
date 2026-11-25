from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from services.positions import Trade, build_positions


@dataclass
class WalletRanking:
    wallet: str
    total_pnl: Decimal
    total_spent: Decimal
    roi: Optional[Decimal]
    first_trade: datetime
    distinct_markets: int = 0
    trade_count: int = 0
    incomplete: bool = False
    rank: int = 0


@dataclass(frozen=True)
class RankingConfig:
    min_distinct_markets: int = 10
    min_trades: int = 30
    min_total_spent: Decimal = Decimal("1000")
    top_n: int = 100


def build_wallet_summaries(
    trades: list[Trade],
    unrealized_pnl: dict = None,
    as_of: datetime = None,
) -> list[WalletRanking]:
    """
    Calculate wallet summaries from trades and positions.

    FR-1: Total PNL.
    FR-2: Total amount spent.
    FR-3: ROI.
    FR-6: Activity counts.
    FR-10: Incomplete wallet flag.

    Does not filter or truncate wallets.
    """

    unrealized_pnl = unrealized_pnl or {}

    if as_of is not None:
        trades = [
            trade for trade in trades
            if trade.block_time <= as_of
        ]

    wallet_trades = {}

    for trade in trades:
        wallet_trades.setdefault(trade.wallet, []).append(trade)

    positions = build_positions(trades, as_of=as_of)

    rankings = []

    for wallet, wallet_trade_list in wallet_trades.items():

        # FR-1: Calculate total PNL.
        total_pnl = Decimal("0")

        for key, position in positions.items():
            if key[0] != wallet:
                continue

            realized = getattr(
                position,
                "realized_pnl",
                Decimal("0"),
            )

            unrealized = unrealized_pnl.get(
                key,
                Decimal("0"),
            )

            total_pnl += realized + unrealized

        # FR-2: Calculate total amount spent.
        total_spent = sum(
            (
                trade.shares * trade.price
                for trade in wallet_trade_list
                if trade.side.lower() == "buy"
            ),
            Decimal("0"),
        )

        # FR-3: Calculate ROI.
        roi = (
            total_pnl / total_spent
            if total_spent > 0
            else None
        )

        # FR-6: Count distinct markets.
        distinct_markets = len({
            trade.market
            for trade in wallet_trade_list
        })

        # FR-6: Count all buys and sells.
        trade_count = len(wallet_trade_list)

        # Find earliest trade.
        first_trade = min(
            trade.block_time
            for trade in wallet_trade_list
        )

        # FR-10: Aggregate incomplete status.
        incomplete = any(
            position.incomplete
            for key, position in positions.items()
            if key[0] == wallet
        )

        rankings.append(
            WalletRanking(
                wallet=wallet,
                total_pnl=total_pnl,
                total_spent=total_spent,
                roi=roi,
                first_trade=first_trade,
                distinct_markets=distinct_markets,
                trade_count=trade_count,
                incomplete=incomplete,
            )
        )

    return rankings


def build_pnl_rankings(
    rankings: list[WalletRanking],
    config: RankingConfig = RankingConfig(),
) -> list[WalletRanking]:
    """
    Build PNL ranking.

    FR-4: Sort by total PNL descending.
    FR-5: Resolve PNL ties.
    FR-9: Return top N.
    FR-10: Preserve incomplete flags.

    No activity filtering is applied.
    """

    def sort_key(wallet):

        pnl_rounded = wallet.total_pnl.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        roi_rounded = (
            wallet.roi.quantize(
                Decimal("0.0001"),
                rounding=ROUND_HALF_UP,
            )
            if wallet.roi is not None
            else None
        )

        return (
            -pnl_rounded,
            roi_rounded is None,
            -(roi_rounded or Decimal("0")),
            -wallet.total_spent,
            wallet.first_trade,
            wallet.wallet.lower(),
        )

    sorted_wallets = sorted(rankings, key=sort_key)

    result = [
        replace(wallet, rank=index)
        for index, wallet in enumerate(
            sorted_wallets[:config.top_n],
            start=1,
        )
    ]

    print_ranking_config("PNL", config)

    return result


def build_roi_rankings(
    rankings: list[WalletRanking],
    config: RankingConfig = RankingConfig(),
) -> list[WalletRanking]:
    """
    Build ROI ranking.

    FR-6: Filter minimum activity thresholds.
    FR-7: Sort by ROI descending.
    FR-8: Resolve ROI ties.
    FR-9: Return top N.
    FR-10: Preserve incomplete flags.
    """

    # FR-6: Apply all three minimum thresholds.
    eligible = [
        wallet for wallet in rankings
        if (
            wallet.distinct_markets >= config.min_distinct_markets
            and wallet.trade_count >= config.min_trades
            and wallet.total_spent >= config.min_total_spent
            and wallet.roi is not None
        )
    ]

    # FR-7 and FR-8.
    def sort_key(wallet):

        roi_rounded = wallet.roi.quantize(
            Decimal("0.0001"),
            rounding=ROUND_HALF_UP,
        )

        return (
            -roi_rounded,
            -wallet.total_pnl,
            -wallet.total_spent,
            wallet.first_trade,
            wallet.wallet.lower(),
        )

    eligible.sort(key=sort_key)

    # FR-9: Return top N with independent ranks.
    result = [
        replace(wallet, rank=index)
        for index, wallet in enumerate(
            eligible[:config.top_n],
            start=1,
        )
    ]

    print_ranking_config("ROI", config)

    return result


def print_ranking_config(
    ranking_type: str,
    config: RankingConfig,
) -> None:
    """FR-9: Print ranking thresholds and N."""

    print(
        f"{ranking_type} ranking configuration: "
        f"min_distinct_markets={config.min_distinct_markets}, "
        f"min_trades={config.min_trades}, "
        f"min_total_spent={config.min_total_spent}, "
        f"top_n={config.top_n}"
    )


def build_wallet_rankings(
    trades: list[Trade],
    unrealized_pnl: dict = None,
    as_of: datetime = None,
    config: RankingConfig = RankingConfig(),
) -> list[WalletRanking]:
    """
    Backwards-compatible PNL ranking entry point.

    Existing callers can continue using build_wallet_rankings().
    """

    summaries = build_wallet_summaries(
        trades,
        unrealized_pnl=unrealized_pnl,
        as_of=as_of,
    )

    return build_pnl_rankings(summaries, config)
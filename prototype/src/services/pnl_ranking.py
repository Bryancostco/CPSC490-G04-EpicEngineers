
from dataclasses import dataclass
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
    rank: int = 0


def build_wallet_rankings(
    trades: list[Trade],
    unrealized_pnl: dict = None,
    as_of: datetime = None,
) -> list[WalletRanking]:
    """
    Build wallet rankings using realized and unrealized PNL.

    FR-1: Total PNL = realized PNL + unrealized PNL.
    FR-2: Total spent = sum of shares * price for every buy.
    FR-3: ROI = total PNL / total spent, or None if spent is zero.
    FR-4: Rank by total PNL descending.
    FR-5: Resolve ties using ROI, amount spent, first trade,
          then wallet address.
    """

    unrealized_pnl = unrealized_pnl or {}

    # Ignore trades after the requested as-of time.
    if as_of is not None:
        trades = [
            trade for trade in trades
            if trade.block_time <= as_of
        ]

    # Group trades by wallet.
    wallet_trades = {}

    for trade in trades:
        wallet_trades.setdefault(trade.wallet, []).append(trade)

    # Build positions using the existing position service.
    positions = build_positions(trades, as_of=as_of)

    rankings = []

    for wallet, wallet_trade_list in wallet_trades.items():

        # FR-1: Sum realized and unrealized PNL across positions.
        total_pnl = Decimal("0")

        for key, position in positions.items():
            if key[0] != wallet:
                continue

            realized = getattr(position, "realized_pnl", Decimal("0"))
            unrealized = unrealized_pnl.get(key, Decimal("0"))

            total_pnl += realized + unrealized

        # FR-2: Calculate total amount spent on buys.
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

        # Find the earliest trade in the window.
        first_trade = min(
            trade.block_time for trade in wallet_trade_list
        )

        rankings.append(
            WalletRanking(
                wallet=wallet,
                total_pnl=total_pnl,
                total_spent=total_spent,
                roi=roi,
                first_trade=first_trade,
            )
        )

    # FR-4 and FR-5: Sort by PNL and tie-breaking rules.
    def sort_key(wallet):
        pnl_to_cent = wallet.total_pnl.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return (
            -pnl_to_cent,
            -(wallet.roi if wallet.roi is not None else Decimal("-Infinity")),
            -wallet.total_spent,
            wallet.first_trade,
            wallet.wallet.lower(),
        )

    rankings.sort(key=sort_key)

    # Assign distinct ranks.
    for index, wallet in enumerate(rankings, start=1):
        wallet.rank = index

    return rankings

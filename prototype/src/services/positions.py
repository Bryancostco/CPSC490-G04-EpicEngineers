"""Step 2 of the PNL pipeline: group trades into positions and build FIFO lots.

Implements FR-1 to FR-5 of docs/specs/pnl-calculation.md (#108). FR-4 removes
sold shares "under FR-6", so the oldest lot is drawn first here and every draw
is recorded as a SaleMatch (NFR-3). Turning those matches into realized PNL
(FR-7) and the FR-6 tests belong to #110.
"""
from __future__ import annotations  # allow modern type hints

from collections.abc import Iterable  # any sequence of trades
from dataclasses import dataclass, field  # plain records
from datetime import datetime  # block times and the as of time
from decimal import Decimal  # exact shares and prices (NFR-2)

# The two trade sides the spec defines. Other share changing events (split,
# merge, redeem, transfer) wait on open question Q4 and are rejected for now.
buy_side = "buy"  # a trade that adds shares
sell_side = "sell"  # a trade that removes shares
supported_sides = (buy_side, sell_side)  # everything else is an error until Q4 is answered

# Zero as an exact decimal, so sums never mix in an int or float.
zero = Decimal("0")

# A position's identity: proxy wallet, market and outcome token (FR-1).
PositionKey = tuple[str, str, str]


@dataclass(frozen=True)  # trades never change once loaded
class Trade:
    """One fill: a proxy wallet buys or sells shares of one outcome token at one price."""

    wallet: str  # proxy wallet address
    market: str  # market id
    outcome_token: str  # YES or NO token id
    side: str  # "buy" or "sell"
    shares: Decimal  # shares filled, always positive
    price: Decimal  # price per share
    block_number: int  # chain order, first key (FR-2)
    log_index: int  # position within the block, second key (FR-2)
    block_time: datetime  # when the block was mined, compared with the as of time

    def chain_order(self) -> tuple[int, int]:
        """Return the sort key FR-2 defines: earlier block first, then earlier position in the block."""
        return (self.block_number, self.log_index)  # block, then position in block


@dataclass  # lots shrink as shares are sold
class Lot:
    """The shares left from one buy, with the price per share paid (FR-3)."""

    shares: Decimal  # shares still held from this buy
    price: Decimal  # price per share paid
    buy: Trade  # the buy that created the lot, kept for tracing (NFR-3)


@dataclass(frozen=True)  # a match is a fact about the past
class SaleMatch:
    """Shares one sell took from one lot; #110 turns these into realized PNL (FR-7)."""

    sell: Trade  # the sell that took the shares
    buy: Trade  # the buy whose lot they came from
    shares: Decimal  # how many shares came from that lot
    lot_price: Decimal  # what those shares cost per share
    sale_price: Decimal  # what they sold for per share


@dataclass  # positions are filled in as trades apply
class Position:
    """All of one proxy wallet's shares in one outcome token of one market (FR-1)."""

    wallet: str  # proxy wallet address
    market: str  # market id
    outcome_token: str  # outcome token id
    lots: list[Lot] = field(default_factory=list)  # remaining lots, oldest first
    sale_matches: list[SaleMatch] = field(default_factory=list)  # every lot draw, in order (NFR-3)
    trades: list[Trade] = field(default_factory=list)  # trades applied, in chain order
    incomplete: bool = False  # True when a sell exceeded the shares held (FR-5)
    unmatched_shares: Decimal = zero  # shares sold with no lot to match (FR-5)

    @property
    def key(self) -> PositionKey:
        """Return the position's identity (FR-1)."""
        return (self.wallet, self.market, self.outcome_token)  # wallet, market, token

    def shares_held(self) -> Decimal:
        """Return the shares still held across all lots."""
        return sum((lot.shares for lot in self.lots), zero)  # exact sum starting from Decimal zero


def position_key(trade: Trade) -> PositionKey:
    """Return the key FR-1 groups by: proxy wallet, market and outcome token."""
    return (trade.wallet, trade.market, trade.outcome_token)  # one position per triple


def check_trade(trade: Trade) -> None:
    """Reject trades the spec does not define yet, instead of guessing what they mean."""
    if trade.side not in supported_sides:  # only buys and sells are specified
        raise ValueError(f"unsupported trade side {trade.side!r}; see open question Q4 in the PNL spec")  # stop loudly
    if trade.shares <= zero:  # a fill always moves a positive number of shares
        raise ValueError(f"trade shares must be positive, got {trade.shares}")  # stop loudly


def add_lot(position: Position, buy: Trade) -> None:
    """FR-3: a buy adds a lot with the shares bought and the price per share paid."""
    position.lots.append(Lot(shares=buy.shares, price=buy.price, buy=buy))  # newest lot goes last


def remove_sold_shares(position: Position, sell: Trade) -> None:
    """FR-4 and FR-5: take the sold shares from the lots, oldest lot first (FR-6), and flag any shortfall."""
    shares_to_match = sell.shares  # shares this sell still needs to take
    while shares_to_match > zero and position.lots:  # keep drawing while there is demand and supply
        oldest_lot = position.lots[0]  # FR-6: always the oldest remaining lot
        taken = min(oldest_lot.shares, shares_to_match)  # take what this lot can give
        position.sale_matches.append(  # record the draw for #110 and for tracing
            SaleMatch(sell=sell, buy=oldest_lot.buy, shares=taken, lot_price=oldest_lot.price, sale_price=sell.price)  # one match
        )  # end of the record
        oldest_lot.shares -= taken  # shrink the lot
        shares_to_match -= taken  # shrink the demand
        if oldest_lot.shares == zero:  # an empty lot is gone
            position.lots.pop(0)  # move on to the next oldest lot
    if shares_to_match > zero:  # FR-5: the lots ran out before the sell was covered
        position.incomplete = True  # mark the position incomplete
        position.unmatched_shares += shares_to_match  # record how many shares had no lot


def apply_trade(position: Position, trade: Trade) -> None:
    """Apply one trade to its position: buys add a lot, sells remove shares."""
    position.trades.append(trade)  # keep every applied trade for tracing
    if trade.side == buy_side:  # FR-3
        add_lot(position, trade)  # add a lot
    else:  # FR-4, the only other supported side
        remove_sold_shares(position, trade)  # remove shares


def build_positions(trades: Iterable[Trade], as_of: datetime | None = None) -> dict[PositionKey, Position]:
    """Group trades into positions (FR-1) and apply each position's trades in chain order (FR-2).

    Trades whose block_time is after as_of are ignored, as the spec's
    definition of the as of time T requires. With as_of None every trade counts.
    """
    positions: dict[PositionKey, Position] = {}  # one entry per wallet, market and token
    in_window = [trade for trade in trades if as_of is None or trade.block_time <= as_of]  # drop trades after T
    for trade in sorted(in_window, key=Trade.chain_order):  # FR-2: chain order across all trades
        check_trade(trade)  # refuse undefined events
        key = position_key(trade)  # FR-1 grouping key
        if key not in positions:  # first trade of this position
            positions[key] = Position(wallet=trade.wallet, market=trade.market, outcome_token=trade.outcome_token)  # start it
        apply_trade(positions[key], trade)  # update the position
    return positions  # every position, keyed by wallet, market and token

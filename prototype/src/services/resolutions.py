"""Step 3 of the PNL pipeline: match positions to market resolutions and set open or closed.

Implements FR-8 to FR-10 of docs/specs/pnl-calculation.md (#109). The matched
resolution, with its payout per share, is attached to each status so #110 and
#111 can apply FR-11 to FR-13 without looking it up again.
"""
from __future__ import annotations  # allow modern type hints

from collections.abc import Iterable, Mapping  # inputs from #108 and from the data layer
from dataclasses import dataclass  # plain records
from datetime import datetime  # resolution times and the as of time
from decimal import Decimal  # exact payouts (NFR-2)

from services.positions import Position, PositionKey  # positions built in #108

# The two statuses the spec defines.
open_status = "open"  # shares held in a market not resolved by T (FR-10)
closed_status = "closed"  # resolved by T (FR-8) or no shares left (FR-9)


@dataclass(frozen=True)  # a resolution never changes
class Resolution:
    """A market's final outcome: when it resolved and what each outcome token pays per share."""

    market: str  # market id
    resolved_at: datetime  # when the market resolved
    payout_per_share: Mapping[str, Decimal]  # outcome token id to payout, read from the data (Q5)


@dataclass(frozen=True)  # a status describes one moment T
class PositionStatus:
    """A position's status as of T, with the resolution that set it when there is one."""

    key: PositionKey  # wallet, market and outcome token
    status: str  # open_status or closed_status
    resolution: Resolution | None  # the market's resolution at or before T, or None


def resolutions_by_market(resolutions: Iterable[Resolution]) -> dict[str, Resolution]:
    """Index resolutions by market, refusing two records for one market."""
    indexed: dict[str, Resolution] = {}  # market id to its resolution
    for resolution in resolutions:  # look at every record
        if resolution.market in indexed:  # a market resolves once
            raise ValueError(f"market {resolution.market!r} has more than one resolution")  # bad data, stop
        indexed[resolution.market] = resolution  # remember it
    return indexed  # one resolution per market


def resolution_at_or_before(resolution: Resolution | None, as_of: datetime) -> Resolution | None:
    """Return the resolution only if it happened at or before T; later ones do not exist yet."""
    if resolution is not None and resolution.resolved_at <= as_of:  # "at or before T" (FR-8)
        return resolution  # it counts
    return None  # unresolved as of T


def status_of(position: Position, resolution: Resolution | None) -> str:
    """Apply FR-8 to FR-10 to one position, given its market's resolution as of T (or None)."""
    if resolution is not None:  # FR-8: the market resolved at or before T
        return closed_status  # closed, shares or not
    if position.shares_held() == Decimal("0"):  # FR-9: unresolved and nothing held
        return closed_status  # closed
    return open_status  # FR-10: unresolved and shares held


def set_status(
    positions: Mapping[PositionKey, Position],  # positions from build_positions at the same T
    resolutions: Iterable[Resolution],  # every known market resolution
    as_of: datetime,  # the as of time T
) -> dict[PositionKey, PositionStatus]:
    """Return every position's status as of T, keyed like the positions."""
    by_market = resolutions_by_market(resolutions)  # one resolution per market
    statuses: dict[PositionKey, PositionStatus] = {}  # results
    for key, position in positions.items():  # every position
        resolution = resolution_at_or_before(by_market.get(position.market), as_of)  # its market's resolution by T
        statuses[key] = PositionStatus(key=key, status=status_of(position, resolution), resolution=resolution)  # FR-8 to FR-10
    return statuses  # statuses for #110 and #111

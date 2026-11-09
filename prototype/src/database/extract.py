"""Read-only Snowflake extraction. SonarX identifiers remain schema-configurable."""
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

class ExtractionError(RuntimeError):
    pass

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*){0,2}$")

def _id(value: str) -> str:
    if not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"Unsafe Snowflake identifier: {value!r}")
    return value

@dataclass(frozen=True)
class SourceSchema:
    # PROVISIONAL: replace with the official SonarX names from docs/specs/data-sources.md.
    trades_table: str = "SONARX_DB.PUBLIC.POLYMARKET_TRADES"
    resolutions_table: str = "SONARX_DB.PUBLIC.POLYMARKET_RESOLUTIONS"
    wallet: str = "WALLET_ADDRESS"
    market: str = "MARKET_ID"
    outcome_token: str = "OUTCOME_TOKEN"
    side: str = "SIDE"
    shares: str = "SHARES"
    price: str = "PRICE"
    block_number: str = "BLOCK_NUMBER"
    log_index: str = "LOG_INDEX"
    block_time: str = "BLOCK_TIME"
    resolution_time: str = "RESOLVED_AT"
    payout_per_share: str = "PAYOUT_PER_SHARE"

def build_trades_sql(s: SourceSchema = SourceSchema()) -> str:
    t = _id(s.trades_table)
    c = {k:_id(getattr(s,k)) for k in ("wallet","market","outcome_token","side","shares","price","block_number","log_index","block_time")}
    return f"""
SELECT
  {c['wallet']} AS WALLET,
  {c['market']} AS MARKET,
  {c['outcome_token']} AS OUTCOME_TOKEN,
  {c['side']} AS SIDE,
  {c['shares']} AS SHARES,
  {c['price']} AS PRICE,
  {c['block_number']} AS BLOCK_NUMBER,
  {c['log_index']} AS LOG_INDEX,
  {c['block_time']} AS BLOCK_TIME
FROM {t}
WHERE {c['block_time']} >= DATEADD(month, -12, %s)
  AND {c['block_time']} < %s
ORDER BY {c['block_number']}, {c['log_index']}
""".strip()

def build_resolutions_sql(s: SourceSchema = SourceSchema()) -> str:
    t, r = _id(s.trades_table), _id(s.resolutions_table)
    trade_market, trade_time = _id(s.market), _id(s.block_time)
    market, resolved, payout = _id(s.market), _id(s.resolution_time), _id(s.payout_per_share)
    return f"""
SELECT
  {market} AS MARKET,
  {resolved} AS RESOLVED_AT,
  {payout} AS PAYOUT_PER_SHARE
FROM {r}
WHERE {market} IN (
  SELECT DISTINCT {trade_market}
  FROM {t}
  WHERE {trade_time} >= DATEADD(month, -12, %s)
    AND {trade_time} < %s
)
  AND {resolved} <= %s
ORDER BY {resolved}, {market}
""".strip()

def _fetch(connection: Any, sql: str, params: Sequence[Any]) -> list[dict[str, Any]]:
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        names = [col[0].upper() for col in (cursor.description or ())]
        if not rows:
            return []
        if not names:
            raise ExtractionError("Snowflake returned rows without column metadata.")
        return [
            ({str(k).upper():v for k,v in row.items()} if isinstance(row, Mapping) else dict(zip(names,row)))
            for row in rows
        ]
    except ExtractionError:
        raise
    except Exception as exc:
        raise ExtractionError(f"Snowflake extraction failed: {type(exc).__name__}") from exc
    finally:
        if cursor is not None:
            try: cursor.close()
            except Exception: pass

def _validate_as_of(as_of: datetime) -> None:
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")

def fetch_trades(connection: Any, as_of: datetime, schema: SourceSchema = SourceSchema()):
    _validate_as_of(as_of)
    return _fetch(connection, build_trades_sql(schema), (as_of, as_of))

def fetch_resolutions(connection: Any, as_of: datetime, schema: SourceSchema = SourceSchema()):
    _validate_as_of(as_of)
    return _fetch(connection, build_resolutions_sql(schema), (as_of, as_of, as_of))

def extract_trades_and_resolutions(connection: Any, as_of: datetime, schema: SourceSchema = SourceSchema()):
    return fetch_trades(connection, as_of, schema), fetch_resolutions(connection, as_of, schema)

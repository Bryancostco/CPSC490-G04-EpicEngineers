> Epic: #24, #29 · Stories: #26, #27, #30, #31 · Task: #57
> Owner: Justin Cox · Sprint: 2 · Status: draft
> Specifications: [`../specs/pnl-calculation.md`](../specs/pnl-calculation.md), [`../specs/trader-ranking.md`](../specs/trader-ranking.md)

# Design — Data model for the SonarX tables we read and the tables we create

*What data the PNL pipeline reads from SonarX, what tables it builds from that
data (positions, lots, wallet PNL and wallet metrics), and how they connect.*

**Heads up: we do not have the SonarX tables yet.** The team has not received
SonarX's schema documents, so the two SonarX boxes in Figure 1 are *inferred*
from what our specifications need. Their names, columns and keys are our best
guess and are marked PENDING. Our own five tables are drawn from the two
specifications and do not depend on SonarX's naming.

## 1. The picture

Figure 1 shows the whole model. Read it from the top: trades and market
resolutions come in from SonarX, the pipeline groups the trades into positions
and lots, and the wallet totals and metrics are built from the positions.

![ER diagram. Two pending SonarX tables, trades and resolutions, feed our tables. Many trades are grouped into one position, and each buy trade creates at most one lot. A position holds zero or more lots and is resolved by at most one resolution. One wallet PNL row totals one or more positions, and has at most one wallet metrics row.](diagrams/data-model.png)

*Figure 1 — ER diagram of the SonarX source tables (pending, inferred) and the
tables we create. It answers one question: what data do we read and store, and
how is it related? Editable source: [`diagrams/data-model.mmd`](diagrams/data-model.mmd).
Comments on our columns cite the requirement that needs them (FR numbers are
from the position spec unless marked "ranking").*

Figure 1 shows how our data fits together. We start with two kinds of data from SonarX: the trades each wallet made and the results of the markets those trades were in. We don't have SonarX's table documentation yet, so those two boxes are our best guess based on what our specs need, and they're marked pending. From the trades we build a position for each wallet, market and outcome (YES or NO), and a lot for each buy so that sales can be matched against the oldest purchase first. A market's result, or running out of shares, closes a position, and each position records its profit and loss.

From there the diagram rolls up. The wallet PNL table adds up a wallet's positions into one total, and the wallet metrics table holds the numbers we use to rank and describe traders, like ROI, win rate and average entry price. Everything in our own tables comes from a requirement in the PNL and ranking specs. Anything we haven't decided yet, such as tracking exactly which lots each sale used up, is left out on purpose and listed in the design document. Once SonarX sends its schema documents, we'll check the two SonarX boxes against them and note the document and date.

## 2. The tables we create

| Table | One row for each | Key | Why it exists |
|---|---|---|---|
| `POSITION` | proxy wallet, market, outcome token and as of time | `position_id` | FR-1 groups trades into one position per wallet, market and outcome token. It holds open or closed status, the incomplete flag, and realized and unrealized PNL. |
| `LOT` | buy added to a position | `lot_id` | FR-3 adds a lot for every buy. FIFO (FR-6) shrinks `shares_remaining` as sales come in. |
| `WALLET_PNL` | wallet and as of time | `wallet_address` + `as_of_time` | FR-14 sums a wallet's positions into realized, unrealized and total PNL. |
| `WALLET_METRICS` | ranked wallet and as of time | `wallet_address` + `as_of_time` | The ranking spec's amount spent, ROI, ranks, win rate, average entry price, holding period, open and incomplete counts and primary category. |

The `as_of_time` column is there because both specs define every result "as of
time T", and the ranking spec (NFR-4) requires each output to state it.

## 3. How the tables connect

| Link | Cardinality | In plain words |
|---|---|---|
| Trade → position | many trades to exactly one position | every trade lands in one wallet, market and outcome token position (FR-1) |
| Buy trade → lot | one buy to at most one lot | a buy makes a lot; a sell makes none (FR-3, FR-4) |
| Position → lot | one position to zero or more lots | zero when the first trade is a sell we cannot match (FR-5) |
| Resolution → position | one resolution to zero or more positions | a position has at most one resolution at or before T (FR-8 to FR-10); a market with no resolution yet has none |
| Wallet PNL → position | one wallet row to one or more positions | the totals add up the wallet's positions (FR-14) |
| Wallet PNL → wallet metrics | one to zero or one | metrics are built for ranked wallets (ranking FR-11) |

## 4. SonarX source tables: pending

| Drawn as | What our specs need from it | Status |
|---|---|---|
| SonarX trades (inferred) | wallet, market, outcome token, buy or sell, price per share, shares, chain order (block, then position in block) and time | **pending**: no SonarX schema document received |
| SonarX resolutions (inferred) | resolved outcome, payout per share, resolution time | **pending**: same |

The column names in these two boxes are the *ideas* the specs use, not real
SonarX column names. Which SonarX table and column holds each field is the job
of `docs/specs/data-sources.md` (#25). Task #57 asks us to check the source
attributes against the SonarX schema documents that arrive through Slack and
to note the document and date. That check is **not done yet**:

| SonarX schema document | Received through Slack on | Checked against Figure 1 on |
|---|---|---|
| 〈document name〉 | 〈date〉 | 〈date〉 |

When the documents arrive, fill in this table, rename the two boxes and their
columns to match, and remove "inferred" from Figure 1 in the same pull request.

## 5. Choices to confirm and things left out

These are proposals from the first draft. Please confirm or change them in
review, since the data model will outlast the sprint.

- **Rows are keyed by `as_of_time`**, so running again for another T does not
  overwrite the first run.
- **Per position PNL is stored on `POSITION`.** `data-flow.md` (#58, still on
  its own branch) says the PNL store holds PNL per position and per wallet, so
  one of the two documents will change.
- **Rank, ROI and amount spent live in `WALLET_METRICS`** rather than a
  separate ranking table.
- **Keys such as `position_id` and `lot_id` are generated ids** we chose so a
  lot can point at its position with one column.

Left out on purpose, because the specs have not decided them (a box nobody has
chosen would break `DIAGRAMS.md` §5):

- **Which lots each sale used up.** The position spec (NFR-3) wants every
  figure traceable to its trades and lots, but today only `shares_remaining`
  is stored. Whether to add a table for this is a team decision.
- **Per category breakdown.** Ranking FR-15 reports each category's share of
  spending and PNL. We store only `primary_category` for now, because which
  SonarX column holds a market's category is still open (ranking Q3).
- **Fees, and events other than buys and sells** such as splits, merges and
  redemptions (position spec open questions).
- **First buy time, close time and open position age.** The ranking spec
  computes them from trades, so they are not stored.
- **Owner (EOA) wallet links and real time data:** Phase 2.

## 6. What was checked and what was not

Checked by reading the two specs against the diagram: every column on our four
tables cites a requirement, and every link in §3 does too. Not checked: the
SonarX columns (§4), that a SonarX trade has a single column key, and that the
exported image matches the Mermaid source after any future edit (re-export
both together).
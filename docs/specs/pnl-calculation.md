# Specification — Position matching and PNL calculation

> Epic: #24 · Stories: #26, #27 · Task: #55
> Owner: Bryan Orozco · Sprint: 2 · Status: draft

*How the system turns a proxy wallet's Polymarket trades into positions,
decides whether each position is open or closed, and computes realized and
unrealized profit and loss (PNL). The prototype code for #26 and #27 is
tested against this document, and the validation in #28 checks it.*

The two objectives it serves, quoted from proposal §2:

> Objective 1.2: Associate each wallet's transactions with their market
> resolution in order to determine whether each position is open or closed.

> Objective 1.3: Compute the realized PNL for closed positions and the
> unrealized PNL for open positions for each proxy wallet.

## Scope

**In scope.** Proxy wallets only (Phase 1). Trades and market resolutions
from SonarX's Polygon data in Snowflake over the last 12 months, the Phase 1
window our mentor set on Oct 20, 2026
([#20](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)).
Grouping trades into positions, FIFO cost basis, open or closed status,
realized PNL, unrealized PNL, and wallet totals.

**Out of scope.** Linking proxy wallets to their owner (EOA) wallets, which is
Phase 2 and future work. Real time data. Ranking, return on investment and
trading behavior metrics, which belong to `docs/specs/trader-ranking.md`
(#54). Which tables and columns hold each field, which belongs to
`docs/specs/data-sources.md` (#25). How the dashboard shows any of this (#33).

### Pipeline steps

The pipeline has six numbered steps. The data flow diagrams in
`docs/design/data-flow.md` (#58) number their processes the same way
(process 1.0 is step 1), so a process in a diagram and a step here always
mean the same thing.

| Step | Name | Defined in |
|---|---|---|
| 1 | Extract trades and market resolutions | `docs/specs/data-sources.md` (#25) |
| 2 | Build positions and cost basis lots | this document, FR-1 to FR-7 |
| 3 | Match positions to resolutions and set status | this document, FR-8 to FR-10 |
| 4 | Compute realized and unrealized PNL | this document, FR-11 to FR-15 |
| 5 | Rank wallets and compute trading metrics | `docs/specs/trader-ranking.md` (#54) |
| 6 | Serve results to the dashboard | dashboard documents (#33) |

## Definitions

| Term | Meaning in this project |
|---|---|
| Proxy wallet | The wallet address that holds a Polymarket user's shares and appears on chain as the trader. Phase 1 computes PNL per proxy wallet. |
| EOA | Externally owned account: the owner wallet behind one or more proxy wallets. Phase 2 only. |
| Outcome token | One side of a market, such as YES or NO. Each outcome token is traded separately. |
| Trade | One fill in which a proxy wallet buys or sells shares of one outcome token at one price per share. |
| Position | All of one proxy wallet's shares in one outcome token of one market. |
| Lot | The shares from one buy, with the price per share paid. FIFO consumes lots oldest first. |
| Cost basis | What the shares still held cost, taken from the lots that remain. |
| Payout per share | What one share of an outcome token is worth once its market resolves, taken from the resolution data. A winning share pays 1.00 and a losing share 0.00 [1]. |
| Latest price | The price of the most recent trade in an outcome token at or before the as of time. |
| As of time (T) | The moment the calculation describes. Everything after T is ignored. |
| Realized PNL | Profit or loss that is locked in, from a sale or from the market resolving. |
| Unrealized PNL | Profit or loss on shares still held in a market that has not resolved, marked at the latest price. |

## Functional requirements

Written in EARS form ("when a trigger happens, the system shall respond") so each
one becomes a test almost verbatim. FR-6 and FR-7 apply FIFO, the cost basis
our mentor set as the default on Oct 20, 2026
([#20](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)).

| ID | Requirement | Story |
|---|---|---|
| FR-1 | When trades are loaded, the system shall group them into one position per proxy wallet, market and outcome token, so a wallet holding both YES and NO in one market has two positions. | #26 |
| FR-2 | When the system processes a position, it shall apply that position's trades in chain order: earlier block first, and within a block, earlier position in the block first. | #26 |
| FR-3 | When a trade is a buy, the system shall add a lot with the shares bought and the price per share paid. | #26 |
| FR-4 | When a trade is a sell, the system shall remove the sold shares from the position's lots under FR-6. | #26 |
| FR-5 | When a sell is for more shares than the position's lots hold, the system shall match only the shares that are held, mark the position as incomplete, and record how many shares were unmatched. | #26 |
| FR-6 | When a sale is matched, the system shall take shares from the oldest remaining lot first, and move to the next oldest lot only when the current one is empty. | #27 |
| FR-7 | When shares from a lot are sold, the system shall add (sale price − lot price) × shares sold from that lot to the position's realized PNL. | #27 |
| FR-8 | When a position's market has a resolution at or before T, the system shall mark the position closed. | #26 |
| FR-9 | When a position's market has no resolution at or before T and its lots hold zero shares, the system shall mark the position closed. | #26 |
| FR-10 | When a position's market has no resolution at or before T and its lots hold more than zero shares, the system shall mark the position open. | #26 |
| FR-11 | When a position's market resolves at or before T, the system shall add (payout per share − lot price) × shares for every lot still held to the position's realized PNL, using the payout per share from the resolution data. | #27 |
| FR-12 | When a position is open, the system shall set its unrealized PNL to the sum over its remaining lots of (latest price − lot price) × shares. | #27 |
| FR-13 | When a position is closed, the system shall set its unrealized PNL to zero. | #27 |
| FR-14 | When wallet totals are requested, the system shall report the sum of realized PNL, the sum of unrealized PNL, and their total, across all of the wallet's positions. | #27 |
| FR-15 | When any position in a wallet is incomplete under FR-5, the system shall flag the wallet's totals as incomplete. | #27 |

FR-5 exists because the window starts 12 months back. A wallet that bought
before the window and sold inside it has no lot to match against, and
inventing a cost for those shares would make its PNL look certain when it is
not.

FR-8 closes a position when its market resolves, whether or not the wallet
has redeemed its winning shares yet. Redemption turns shares into cash; it
does not change what the position earned. Polymarket describes winning
shares as redeemable for 1.00 each once the outcome is final [1].

### PNL formulas

For a position, with lots *i* still held after all sales:

```
realized PNL   = Σ over sales  (sale price − lot price) × shares taken from that lot
               + Σ over lots i (payout per share − price_i) × shares_i      if resolved by T
unrealized PNL = Σ over lots i (latest price − price_i) × shares_i          if open at T
               = 0                                                          if closed at T
total PNL      = realized PNL + unrealized PNL
```

Unrealized PNL is marked at the latest market price, as our mentor set
([#20](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)).

### Worked example, computed by hand

A made up proxy wallet **W** with two positions. Prices are per share.

**Position A: W holds YES in market M1.**

| Time | Trade | Shares | Price | Lots after the trade |
|---|---|---|---|---|
| t1 | buy | 100 | 0.40 | L1: 100 @ 0.40 |
| t2 | buy | 50 | 0.60 | L1: 100 @ 0.40, L2: 50 @ 0.60 |
| t3 | sell | 120 | 0.70 | L2: 30 @ 0.60 |

The sale at t3 takes all 100 shares of L1, then 20 shares of L2 (FR-6):

| From | Shares | Calculation | Realized |
|---|---|---|---|
| L1 | 100 | (0.70 − 0.40) × 100 | 30.00 |
| L2 | 20 | (0.70 − 0.60) × 20 | 2.00 |
| **Sale total** | 120 | | **32.00** |

The cost basis method changes the answer: an average cost method prices all
150 shares at 70.00 ÷ 150 = 0.4667, so the same sale would realize
(0.70 − 0.4667) × 120 = 28.00 instead of 32.00.

What happens next depends on M1 at the as of time T:

| Case at T | Status | Realized | Unrealized | Total |
|---|---|---|---|---|
| M1 unresolved, latest YES price 0.55 | open (FR-10) | 32.00 | (0.55 − 0.60) × 30 = −1.50 | 30.50 |
| M1 resolved YES, payout 1.00 | closed (FR-8) | 32.00 + (1.00 − 0.60) × 30 = 44.00 | 0.00 | 44.00 |

Cash check for the resolved case: W paid 40.00 + 30.00 = 70.00, received
84.00 from the sale and 30 × 1.00 = 30.00 at resolution, so it ends 44.00
ahead, which matches.

**Position B: W holds NO in market M2.** W buys 200 NO shares at 0.25 (cost
50.00). M2 resolves YES, so NO pays 0.00: realized PNL is
(0.00 − 0.25) × 200 = −50.00, unrealized is 0.00, and the position is closed.

**Wallet W totals (FR-14):**

| Case for M1 | Realized | Unrealized | Total |
|---|---|---|---|
| M1 unresolved | 32.00 − 50.00 = −18.00 | −1.50 | −19.50 |
| M1 resolved YES | 44.00 − 50.00 = −6.00 | 0.00 | −6.00 |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Running the calculation twice on the same trades, resolutions and T gives identical results. | #25 asks a teammate to rerun our work and match it, and #28 compares our numbers against outside sources; neither works if results drift. |
| NFR-2 | Prices, shares and PNL are held as exact decimals, never binary floating point, and are rounded only when displayed. | PNL sums thousands of small differences such as 0.70 − 0.60; floating point error adds up across a 12 month window. |
| NFR-3 | Every realized or unrealized figure can be traced back to the trades and lots that produced it. | #28 must explain any discrepancy with an outside source, which means showing the trades behind a number. |

## Acceptance criteria (epic level)

- [ ] The prototype reproduces the worked example exactly, as tests that
      each fail if FR-6, FR-7, FR-8, FR-10, FR-11 or FR-12 is removed.
- [ ] A position with a sell larger than its lots is marked incomplete
      (FR-5), with a test.
- [ ] Every functional requirement cites #26 or #27, and every open
      question below has an owner.
- [ ] This document is listed in proposal §4 under Specification and design
      documents.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Should positions marked incomplete (FR-5) be left out of the leaderboard, shown with a warning, or fixed by loading earlier trades for those wallets only? (ask Erel) | Bryan Orozco | before ranking work in #30 |
| Do SonarX's Polymarket tables record trading fees per trade? If they do, realized PNL subtracts them; if not, we report PNL before fees and say so. (ask Sergio) | Bryan Orozco | before #27 is implemented |
| Which table and column give the latest price for an outcome token, and how fresh is it? (ask Sergio) | Bryan Orozco | before #27 is implemented |
| Besides buys and sells, which events change a wallet's shares in the data (for example splitting collateral into a YES and NO pair, merging a pair back, redeeming after resolution, or transfers between wallets), and how does each appear? Each needs its own requirement before #26 is built. (ask Sergio) | Bryan Orozco | before #26 is implemented |
| Can a market resolve with a payout per share other than 1.00 or 0.00? FR-11 already reads the payout from the data, so this only changes the test cases. (ask Sergio) | Bryan Orozco | before #27 tests |
| What tolerance between our PNL and the Polymarket leaderboard counts as a match? Our mentor said to set it together after a first pass. (ask Erel) | Bryan Orozco | before #28 |

## Sources

[1] Polymarket, "Polymarket 101," Polymarket Documentation. Available:
https://docs.polymarket.com/polymarket-101 (accessed Oct. 24, 2026).

# Specification — Trader ranking and trading behavior metrics

> Epic: #29 · Stories: #30, #31 · Task: #54
> Owner: Justin Cox · Sprint: 2 · Status: draft

*How the system ranks proxy wallets by profitability and describes how each
ranked wallet trades. It takes the per position results of the position
matching and PNL specification (#55, "the position spec") and turns them into
two rankings (#30) and four trading behavior metrics (#31). The prototype
code for #30 and #31 is tested against this document, and the validation in
#28 checks it. The rules and definitions here are written by the team for this
project; they are not copied from an outside standard.*

The two objectives it serves, quoted from proposal §2:

> Objective 2.1: Compute the PNL and return on investment for each proxy
> wallet and produce a leaderboard of the most profitable traders.

> Objective 2.2: Analyze the trading behaviors of each ranked wallet,
> including win rate, average entry price, market categories traded, and
> position holding period.

## Scope

**In scope.** Proxy wallets only (Phase 1). The same 12 month window as the
position spec, set by our mentor on Oct 20, 2026
([#20](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)).
Wallet total PNL, return on investment (ROI), the minimum activity rule, two
rankings (one by total PNL and one by ROI) with a written tie break for each,
and the four metrics: win rate, average entry price, market categories
traded, and position holding period.

**Out of scope.** How positions, lots and PNL are computed, which belongs to
the position spec (#55). Linking proxy wallets to their owner (EOA) wallets,
which is Phase 2 and future work. Real time data. Which tables and columns
hold each field, which belongs to `docs/specs/data-sources.md` (#25). How the
dashboard shows the rankings or the metrics (#33).

### Pipeline steps

This document defines step 5. The numbering is the one used in the position
spec and in the data flow diagrams in `docs/design/data-flow.md` (#58): a
process in a diagram and a step here always mean the same thing.

| Step | Name | Defined in |
|---|---|---|
| 1 | Extract trades and market resolutions | `docs/specs/data-sources.md` (#25) |
| 2 | Build positions and cost basis lots | position spec (#55), FR-1 to FR-7 |
| 3 | Match positions to resolutions and set status | position spec (#55), FR-8 to FR-10 |
| 4 | Compute realized and unrealized PNL | position spec (#55), FR-11 to FR-15 |
| 5 | Rank wallets and compute trading metrics | this document, FR-1 to FR-18 |
| 6 | Serve results to the dashboard | dashboard documents (#33) |

Step 5 reads only the output of step 4 (each position's status, realized PNL,
unrealized PNL and incomplete flag) plus the trades behind it. It does not
recompute PNL.

## Definitions

Terms the position spec already defines (proxy wallet, outcome token, trade,
position, lot, closed and open, as of time T, realized PNL, unrealized PNL)
keep the same meaning here. The terms below are new.

| Term | Meaning in this project |
|---|---|
| Incomplete position | A position flagged under position spec FR-5: it sold more shares than its lots held, so part of its PNL could not be matched. |
| Incomplete wallet | A wallet flagged under position spec FR-15: at least one of its positions is incomplete. |
| Window | The 12 month period ending at T. Only trades inside it are used. |
| Total PNL | A wallet's realized PNL plus its unrealized PNL, summed across all its positions. |
| Total amount spent | What the wallet spent on every buy in the window: Σ shares × price per share. It counts buys whose shares were later sold or are still held. |
| Return on investment (ROI) | Total PNL divided by total amount spent. |
| PNL ranking | All wallets ordered by total PNL, highest first (FR-4, FR-5). |
| ROI ranking | Eligible wallets ordered by ROI, highest first (FR-7, FR-8). |
| Eligible wallet | A wallet that meets every threshold of the minimum activity rule (FR-6). Only eligible wallets appear in the ROI ranking. |
| Ranked wallet | A wallet in the top N of the PNL ranking or the ROI ranking. The metrics are computed for every ranked wallet (FR-11). |
| Winning position | A closed position whose realized PNL is greater than zero. |
| Entry price | The price per share paid on a buy. Every share is priced between 0.00 and 1.00, and the price reflects the market's belief in the probability of that outcome [1]. |
| Category | The label that groups markets by topic, taken from the market data (Q3 asks where it comes from). |
| Holding period | The time from a position's first buy to the moment it closes, in days. |

### Minimum activity thresholds

Starting values, kept in configuration and printed with every ranking
(FR-9). Q2 asks our mentor to confirm them.

| Threshold | Starting value |
|---|---|
| Distinct markets traded in the window | at least 10 |
| Trades (buys and sells) in the window | at least 30 |
| Total amount spent | at least 1,000 USD |
| Ranking size N (each ranking) | 100 |

## Functional requirements

Written in EARS form ("when a trigger happens, the system shall respond") so each
one becomes a test almost verbatim. FR-1 to FR-10 serve #30 and FR-11 to FR-18
serve #31.

| ID | Requirement | Story |
|---|---|---|
| FR-1 | When the ranking runs for as of time T, the system shall set each wallet's total PNL to the sum of realized PNL and unrealized PNL across all of the wallet's positions, as computed by the position spec. | #30 |
| FR-2 | When the ranking runs, the system shall set each wallet's total amount spent to the sum of shares × price per share over every buy by the wallet in the window. | #30 |
| FR-3 | When a wallet's total amount spent is greater than zero, the system shall set its ROI to total PNL ÷ total amount spent; when it is zero, the system shall leave ROI empty. | #30 |
| FR-4 | When the PNL ranking is built, the system shall order all wallets by total PNL from highest to lowest, so rank 1 is the highest total PNL and wallets with negative total PNL rank below all wallets with positive total PNL. | #30 |
| FR-5 | When two wallets have the same total PNL, compared to the cent (0.01 USD), the system shall order them by higher ROI (a wallet with empty ROI after one with a value), then higher total amount spent, then earlier first trade in the window, then lower wallet address in alphabetical order, so every wallet gets a distinct rank. | #30 |
| FR-6 | When the ROI ranking is built, the system shall leave out any wallet that has fewer than the threshold number of distinct markets, trades or total amount spent. The PNL ranking is not filtered by this rule. | #30 |
| FR-7 | When the ROI ranking is built, the system shall order the eligible wallets by ROI from highest to lowest. | #30 |
| FR-8 | When two eligible wallets have the same ROI, compared to four decimal places (0.01 percentage points), the system shall order them by higher total PNL, then higher total amount spent, then earlier first trade in the window, then lower wallet address in alphabetical order, so every wallet gets a distinct rank. | #30 |
| FR-9 | When the ranking runs, the system shall return the top N wallets of each ranking and print the thresholds and N used. | #30 |
| FR-10 | When a wallet is incomplete, the system shall carry the incomplete flag onto its row in every ranking it appears in. | #30 |
| FR-11 | When the metrics run, the system shall output win rate, average entry price, market categories traded and holding period for every ranked wallet. | #31 |
| FR-12 | When the win rate of a wallet is requested, the system shall report the number of winning positions divided by the number of closed positions that are not incomplete. | #31 |
| FR-13 | When a position is open or incomplete, the system shall leave it out of the win rate and the holding period statistics, and report the number of open positions and the number of incomplete positions for the wallet. | #31 |
| FR-14 | When the average entry price of a wallet is requested, the system shall report Σ (shares × price per share) ÷ Σ shares over every buy by the wallet in the window, ignoring sells. | #31 |
| FR-15 | When the market categories of a wallet are requested, the system shall report each category traded, the share of the wallet's total amount spent in that category, the total PNL in that category, and the primary category (the one with the largest share of total amount spent). A market with no category is reported as `Uncategorized`. | #31 |
| FR-16 | When the holding period of a wallet is requested, the system shall set each closed position's holding period to its close time minus its first buy time, where the close time is the time of the trade that took the lots to zero shares or, if the market resolved first, the resolution time, and report the average (mean) and the median over those positions in days. | #31 |
| FR-17 | When an open position is reported, the system shall report its age as T minus its first buy time, separately from the holding period of closed positions. | #31 |
| FR-18 | When a metric has nothing to divide or average (no closed positions, or no buys), the system shall report it as empty, never as zero. | #31 |

FR-6 exists so that one lucky bet on a nearly empty wallet cannot take the top
of the ROI ranking: ROI is a ratio, and a ratio over a tiny amount spent is
easy to inflate. Total PNL is a dollar amount, so FR-4 leaves the PNL ranking
unfiltered; Q2 asks whether that is right. FR-13 leaves incomplete positions
out of the win rate and the holding period because their PNL and first buy
time are partly unknown when the window starts after the wallet began
trading, the same reason position spec FR-5 flags them. Q1 asks whether
incomplete wallets should be ranked at all.

FR-14 always gives a number between 0 and 1, because every share is priced
between 0.00 and 1.00 and the price reflects the market's belief in the
probability of the outcome [1]. Read that way, it is the average probability
the market gave the outcomes the wallet bought, weighted by shares.

FR-18 matters because an empty win rate and a 0% win rate say different
things: the first means no evidence, the second means every closed position
lost.

### Formulas

For a wallet, over the window ending at T:

```
total PNL          = Σ over positions (realized PNL + unrealized PNL)
total amount spent = Σ over buys (shares × price per share)
ROI                = total PNL ÷ total amount spent                 if total amount spent > 0

win rate           = winning positions ÷ closed positions that are not incomplete
avg entry price    = Σ over buys (shares × price) ÷ Σ over buys (shares)
category share     = amount spent in category ÷ total amount spent
holding period     = close time − first buy time                    per closed position
```

Ranking orders:

```
PNL ranking (all wallets)          ROI ranking (eligible wallets only)
1. total PNL, highest first        1. ROI, highest first
2. ROI, highest first              2. total PNL, highest first
3. total amount spent, highest     3. total amount spent, highest
4. first trade, earliest first     4. first trade, earliest first
5. wallet address, alphabetical    5. wallet address, alphabetical
```

### Worked example, computed by hand

**Ranking.** Five made up wallets at the same T, with the starting thresholds.
Wallet W is the one from the position spec's worked example, where M1 has
resolved YES (total PNL −6.00, total amount spent 70.00 + 50.00 = 120.00,
4 trades in 2 markets).

| Wallet | Markets | Trades | Total amount spent | Total PNL | ROI | PNL rank | Eligible | ROI rank |
|---|---|---|---|---|---|---|---|---|
| X | 12 | 40 | 5,000.00 | 1,000.00 | 20.0% | 2 | yes | 2 |
| Y | 15 | 60 | 2,000.00 | 1,000.00 | 50.0% | 1 | yes | 1 |
| Z | 3 | 8 | 400.00 | 900.00 | 225.0% | 3 | no | none |
| W | 2 | 4 | 120.00 | −6.00 | −5.0% | 4 | no | none |
| V | 20 | 100 | 8,000.00 | −200.00 | −2.5% | 5 | yes | 3 |

- X and Y tie on total PNL at 1,000.00. FR-5 breaks the tie on ROI:
  Y at 1,000 ÷ 2,000 = 50.0% beats X at 1,000 ÷ 5,000 = 20.0%.
- Z has the highest ROI of all five, but fails all three thresholds
  (3 < 10 markets, 8 < 30 trades, 400 < 1,000 spent), so FR-6 keeps it out of
  the ROI ranking. It still ranks 3rd on total PNL, because FR-4 is not
  filtered. W fails the same way.
- W, at −6.00, ranks above V at −200.00 on total PNL, because a smaller loss
  is a higher number.

**Metrics for wallet W.** From the position spec: position A is YES in M1
(buys 100 @ 0.40 and 50 @ 0.60, then a sale of 120 @ 0.70), and position B is
NO in M2 (buy 200 @ 0.25, M2 resolves YES). Added for this example, both
made up: M1 is in category Politics and M2 in Crypto; A's first buy is on
2026-01-10 and M1 resolves 2026-03-01; B's buy is on 2026-02-01 and M2
resolves 2026-02-21; T is 2026-04-01.

| Metric | Calculation | Result |
|---|---|---|
| Total amount spent | (100 × 0.40) + (50 × 0.60) + (200 × 0.25) = 40 + 30 + 50 | 120.00 |
| Total PNL (M1 resolved) | 44.00 + (−50.00) | −6.00 |
| ROI | −6.00 ÷ 120.00 | −5.0% |
| Win rate | A wins (44.00 > 0), B loses (−50.00); 1 ÷ 2 | 50% |
| Average entry price | 120.00 ÷ (100 + 50 + 200) = 120 ÷ 350 | 0.3429 |
| Category share of total amount spent | Politics 70 ÷ 120, Crypto 50 ÷ 120 | 58.3%, 41.7% |
| PNL by category | Politics 44.00, Crypto −50.00 | primary: Politics |
| Holding period | A: 2026-01-10 to 2026-03-01 = 50 days; B: 2026-02-01 to 2026-02-21 = 20 days | average 35, median 35 days |

Cash check on the average entry price: the three buys cost 120.00 for 350
shares, and 120 ÷ 350 = 0.342857, which rounds to 0.3429.

If M1 had not resolved by T (latest YES price 0.55), A would be open
(position spec FR-10) and the metrics change as follows:

| Metric | Result | Why |
|---|---|---|
| Total PNL | −19.50 | 32.00 − 1.50 − 50.00 |
| ROI | −16.25% | −19.50 ÷ 120.00 |
| Win rate | 0% (0 of 1) | A is open and leaves the win rate (FR-13); only B counts, and it lost |
| Holding period | average 20, median 20 days | only B counts (FR-13) |
| Open positions | 1 | A, reported separately with its age at T (FR-17) |
| Average entry price | 0.3429 | unchanged: it uses buys only (FR-14) |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Running the ranking twice on the same positions, trades and T gives the same ranks in the same order. | The tie breaks in FR-5 and FR-8 go down to the wallet address so no ties are left to chance; #28 compares our rankings against outside sources and a shifting order would hide real differences. |
| NFR-2 | PNL, shares, prices and ratios are held as exact decimals, never binary floating point, and are rounded only when displayed and for the tie comparisons in FR-5 and FR-8. | ROI and win rate are divisions of sums; rounding early can swap two close wallets. |
| NFR-3 | Every ranking row and metric can be traced back to the positions and trades that produced it. | #28 must explain any gap with an outside leaderboard, which means showing the positions behind a rank. |
| NFR-4 | Every ranking output states the as of time, the window, the thresholds and N it was run with. | A ranking cannot be compared or rerun without them. |

## Acceptance criteria (epic level)

- [ ] The prototype reproduces both worked examples exactly, as tests that
      each fail if FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-12, FR-13, FR-14,
      FR-15 or FR-16 is removed.
- [ ] A wallet below any one threshold is left out of the ROI ranking but
      still appears in the PNL ranking, with a test (wallet Z).
- [ ] Running the ranking twice on the same data gives the same order in both
      rankings, with a test (NFR-1).
- [ ] A metric with nothing to divide is reported as empty rather than zero
      (FR-18), with a test.
- [ ] The metrics for at least 3 wallets match a hand calculation by a
      teammate who did not write the code.
- [ ] Every functional requirement cites #30 or #31, and every open question
      below has an owner.
- [ ] This document is listed in proposal §4 under Specification and design
      documents.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Q1. Should incomplete wallets (position spec Q1) be left out of the rankings, ranked with a warning, or ranked only after earlier trades are loaded for them? FR-10 only carries the flag for now. (ask Erel) | TBD | before ranking work in #30 |
| Q2. Are the starting thresholds (10 markets, 30 trades, 1,000 USD) and N = 100 right for the data we have? Should the minimum activity rule also apply to the PNL ranking? #30 names only the ROI ranking, so this draft leaves the PNL ranking unfiltered. (ask Erel) | TBD | before #30 is implemented |
| Q3. Which table and column give a market's category, does a market ever have more than one, and which one counts if so? FR-15 assumes one category per market. (ask Sergio) | TBD | before #31 is implemented |
| Q4. Should holding period be measured per position (first buy to close, as in FR-16) or per lot under FIFO? A wallet that keeps adding to a position gets a longer period per position than per lot. (ask Erel) | TBD | before #31 tests |
| Q5. Which wallets are "ranked wallets" for #31? FR-11 uses the top N of either ranking; the alternative is the PNL ranking only. (ask Erel) | TBD | before #31 is implemented |
| Q6. If SonarX has no trading fees (position spec Q2), total PNL and ROI are before fees. Do we say that on the rankings themselves or only in this document? (ask Sergio) | TBD | before #33 |
| Q7. Polymarket's documentation says trades use pUSD as collateral [1]. Which collateral token do trades in our 12 month window use, and can its amounts be treated as dollars one for one? This document writes amounts in USD. (ask Sergio) | TBD | before #30 is implemented |

## Sources

[1] Polymarket. Polymarket 101. Polymarket Documentation.
https://docs.polymarket.com/polymarket-101 (accessed Oct. 26, 2026).
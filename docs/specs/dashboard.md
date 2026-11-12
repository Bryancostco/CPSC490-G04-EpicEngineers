> Epic: #33 · Stories: #35, #36, #37 · Feature: #96

# Specification — Client-facing dashboard (Goal 3)

> Owner: Leila De Belen · Sprint: 3 · Status: draft

*What SonarX clients see and do in the dashboard: which pages exist, what each
page shows, how the leaderboard is sorted and filtered, and how fast pages
must load. The leaderboard and wallet lookup pages are built and tested
against this document. It answers the client questions approved by our SonarX
mentor in `docs/specs/dashboard-questions.md` (#95), referred to below as DQ1
to DQ8 so they are not confused with this document's open questions (OQ).*

## Scope

**In scope.** The two pages in Goal 3 and the flow between them, as drawn in
`docs/design/dashboard-flow.md` (#97):

- **P1 Trader Leaderboard**: the PNL ranking and the ROI ranking, with a
  change of time window and filtering (Objective 3.2, DQ1, DQ5).
- **P2 Trader Profile**, the wallet lookup page: one wallet's open and closed
  positions, realized and unrealized PNL, and trading behaviors (Objective 3.3,
  DQ4 to DQ7).
- Two ways into P2: clicking a trader on P1, or entering a wallet address.
- A load time under 3 seconds for every page on our demo data (Objective 3.4,
  #37).

**Out of scope.** P3 Markets and Strategies and P4 Early Movers in the
question list (DQ2, DQ3, DQ8). No Goal 3 objective, page flow or data flow
covers them, and OQ-1 asks our mentor whether they are deferred. How PNL is
calculated (`docs/specs/pnl-calculation.md`, #55). How traders are ranked and
how ROI, win rate and the other metrics are computed
(`docs/specs/trader-ranking.md`, #54). Which tables and columns hold the data
(`docs/specs/data-sources.md`, #25). Linking proxy wallets to owner (EOA)
wallets, which is Phase 2. Real time data.

## Pages

| Page | What it shows | Ways to reach it | Answers |
|---|---|---|---|
| P1 Trader Leaderboard | Top wallets in the PNL ranking or the ROI ranking, with controls for time window and filter | Opening the dashboard; back from P2 | DQ1, DQ5 |
| P2 Trader Profile (wallet lookup) | One wallet's open and closed positions, realized and unrealized PNL, and trading behaviors | Clicking a trader on P1; entering a wallet address | DQ4 to DQ7 |

## Functional requirements

Written in EARS form ("when a trigger happens, the system shall respond") so each
one becomes a test almost verbatim. Terms such as position, realized PNL and
unrealized PNL mean what `docs/specs/pnl-calculation.md` defines; ROI, win
rate, the rankings and the other metrics mean what
`docs/specs/trader-ranking.md` defines.

| ID | Requirement | Story |
|---|---|---|
| FR-1 | When a client opens the dashboard, the system shall show P1 and a way to enter a wallet address. | #35 |
| FR-2 | When P1 is shown, the system shall list the wallets of the selected ranking, up to the ranking size N, with each wallet's rank, address, realized PNL, unrealized PNL, total PNL, ROI and win rate. | #35 |
| FR-3 | When P1 is shown, the system shall show the as of time and the window the ranking was run with, and for the ROI ranking the minimum activity thresholds and N it used. | #35 |
| FR-4 | When a client sorts by total PNL, the system shall show the PNL ranking: all wallets ordered by total PNL, highest first, with the tie breaks in `trader-ranking.md` (FR-4, FR-5). | #35 |
| FR-5 | When a client sorts by ROI, the system shall show the ROI ranking: only eligible wallets ordered by ROI, highest first, with the tie breaks in `trader-ranking.md` (FR-6 to FR-8). | #35 |
| FR-6 | When a client changes the time window, the system shall update P1 for that window without leaving the page. | #35 |
| FR-7 | When a client applies a filter, the system shall show only the wallets that match it, without leaving the page. | #35 |
| FR-8 | When a client clicks a trader on P1, the system shall open P2 for that trader's wallet. | #35 |
| FR-9 | When a client enters a wallet address, the system shall open P2 for that address. | #36 |
| FR-10 | If the entered address is not a valid wallet address, then the system shall show an error message and stay on the current page. | #36 |
| FR-11 | When a client goes back from P2, the system shall return to P1. | #36 |
| FR-12 | When P2 is shown, the system shall list the wallet's open positions and closed positions separately. | #36 |
| FR-13 | When P2 shows an open position, the system shall show its mark price and its unrealized PNL; when it shows a closed position, the system shall show its realized PNL. The mark price is the latest price, as `pnl-calculation.md` defines. | #36 |
| FR-14 | When P2 is shown, the system shall show the wallet's realized PNL, unrealized PNL and their total, as computed under `pnl-calculation.md` (FR-14 there). | #36 |
| FR-15 | When P2 is shown, the system shall show the wallet's win rate, average entry price, market categories traded and holding period, as `trader-ranking.md` defines them (FR-11 to FR-18 there), including the counts of open and incomplete positions. | #36 |
| FR-16 | When a wallet is flagged incomplete, the system shall show the flag on the wallet's row on P1 and on its P2 page. | #35, #36 |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Every dashboard page shall load in under 3 seconds on our demo data. | Objective 3.4 (#37) sets this target. |
| NFR-2 | The pages shall read rankings and wallet results that were computed ahead of time, and shall not recompute PNL or rankings when a page is requested. | A full FIFO pass over 12 months per request would not meet NFR-1; the data flow design (#58) and the plan in proposal §4 (#131) both compute ahead of time. |
| NFR-3 | A PNL, ROI or metric figure shown on the dashboard shall equal the figure the calculation produced for the same wallet and as of time. | The dashboard must not drift from the numbers #28 validates. |
| NFR-4 | Prices, shares and PNL are rounded only when displayed. | Matches NFR-2 of `pnl-calculation.md` and `trader-ranking.md`. |

## Acceptance criteria (epic level)

- [ ] A client can open the dashboard, sort by total PNL and by ROI, change the
      window and apply a filter, click a trader, and return to P1, all through
      the served interface and not by calling functions in a console.
- [ ] A client can enter a valid wallet address and reach P2, and an invalid
      address shows an error and does not change the page.
- [ ] P2 shows open positions, closed positions, realized PNL, unrealized PNL
      and trading behaviors for the chosen wallet.
- [ ] A wallet below the minimum activity thresholds is missing from the ROI
      sort but present in the PNL sort, with a test (wallet Z in the ranking
      spec's worked example).
- [ ] For a sample wallet, the PNL on the page matches the calculation output
      for that wallet.
- [ ] Every page loads in under 3 seconds on the demo data, measured the way
      OQ-6 settles.
- [ ] FR-1 to FR-16 each have a test that fails if the behavior is removed.
- [ ] Every functional requirement cites a story, and every open question
      below has an owner.
- [ ] This document is listed in proposal §4 under Specification and design
      documents.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| OQ-1. Are P3 Markets and Strategies and P4 Early Movers (DQ2, DQ3, DQ8) deferred? No Goal 3 objective, the page flow (#97) or the data flow (#58) covers them. If they are in, each needs an objective, a page in the flow diagram, and the open definitions of "early" and strategy labels from `dashboard-questions.md` §4. (ask Erel) | TBD | before this PR is merged |
| OQ-2. Which time windows does a client choose from? The question list proposes 7d, 30d, 90d and all-time plus a custom range, but both specs use one fixed 12 month window ending at T. Does the pipeline precompute each window, or is the selector limited to what is precomputed? What are the default window, the default sort, and the ranking size N (starting value 100, `trader-ranking.md` Q2)? (ask Erel) | TBD | before FR-2 and FR-6 are implemented |
| OQ-3. Which filters does the leaderboard offer? Task #127 says the approved question list calls for filters, but the list names none. (ask Erel) | TBD | before FR-7 is implemented |
| OQ-4. Several things in the question list are not defined in either spec: cumulative realized and unrealized PNL over time (DQ6), PNL by period, per-position PNL distribution and largest-win share (DQ4), capital at risk over time (DQ5), a list of the wallet's trades, and the resolution date of an open position (DQ7). Which are in this phase, and which spec defines each? ROI (total PNL ÷ total amount spent) already covers PNL divided by capital deployed. | TBD | before FR-13 to FR-15 are implemented |
| OQ-5. Trading metrics are computed only for ranked wallets (`trader-ranking.md` FR-11, Q5), but FR-9 lets a client look up any address. What does P2 show for a valid address that is not ranked, and for one with no trades in the data? | TBD | before FR-9 and FR-15 are implemented |
| OQ-6. What counts as "loaded" for the 3 second target (first content, full table, or everything), and on what size of demo data is it measured? | TBD | before NFR-1 is tested |
| OQ-7. When a client goes back to P1, are the window, filter and sort they chose kept? And once `pnl-calculation.md` Q1 and `trader-ranking.md` Q1 are answered, are incomplete wallets left out, ranked with a warning, or ranked as is? FR-16 only shows the flag. | TBD | before FR-11 and FR-16 are implemented |

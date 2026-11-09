> Epic: #33 · Stories: #35, #36, #37 · Feature: #96

# Specification — Client-facing dashboard (Goal 3)

> Owner: Leila De Belen · Sprint: 3 · Status: draft

*What SonarX clients see and do in the dashboard: which pages exist, what each
page shows, how the leaderboard is filtered and sorted, and how fast pages
must load. The pages are built and tested against this document. It answers
the client questions approved by our SonarX mentor in
`docs/specs/dashboard-questions.md` (#95), referred to below as DQ1 to DQ8 so
they are not confused with this document's open questions (OQ).*

## Scope

**In scope.** The four pages in `docs/specs/dashboard-questions.md` and the
flow between them:

- **P1 Trader Leaderboard**: ranks wallets over a selectable time window, with
  filtering and sorting (Objective 3.2, DQ1, DQ5).
- **P2 Trader Profile** (the wallet lookup page in
  `docs/design/dashboard-flow.md`, #97): one wallet's PNL history, positions
  and trading behaviors (DQ4 to DQ7).
- **P3 Markets and Strategies**: returns broken down by market, category and
  strategy (DQ2, DQ8).
- **P4 Early Movers**: wallets that are consistently early on winning
  outcomes (DQ3).
- Two ways into P2: clicking a trader on P1, or entering a wallet address.
- A page load target of 3 seconds (Objective 3.4, #37).

**Out of scope.** How PNL is calculated (`docs/specs/pnl-calculation.md`,
#55). How traders are ranked and how ROI, win rate and other trading behavior
metrics are computed (`docs/specs/trader-ranking.md`, #54). Which tables and
columns hold the data (`docs/specs/data-sources.md`, #25). Linking proxy
wallets to owner (EOA) wallets (Phase 2). Real time data. Any question not in
the approved list.

## Pages

| Page | What it shows | Ways to reach it | Answers |
|---|---|---|---|
| P1 Trader Leaderboard | Top traders with controls for time window, filter and sort | Opening the dashboard; back from P2 | DQ1, DQ5 |
| P2 Trader Profile | One wallet's PNL history, open and closed positions, realized and unrealized PNL, trades, trading behaviors | Clicking a trader on P1; entering a wallet address | DQ2 to DQ7 |
| P3 Markets and Strategies | PNL and volume by market, category and strategy, across wallets and per wallet | Link from P2; navigation from P1 | DQ2, DQ8 |
| P4 Early Movers | Wallets ranked by how early they enter positions that win | Navigation from P1 | DQ3 |

## Functional requirements

Written in EARS form ("when a trigger happens, the system shall respond") so each
one becomes a test almost verbatim. Terms such as position, realized PNL and
unrealized PNL mean what `docs/specs/pnl-calculation.md` defines; ROI, win
rate and the other metrics mean what `docs/specs/trader-ranking.md` defines.

| ID | Requirement | Story |
|---|---|---|
| FR-1 | When a client opens the dashboard, the system shall show P1 and a way to enter a wallet address. | #35 |
| FR-2 | When P1 is shown, the system shall list the top traders with each trader's realized PNL, unrealized PNL, total PNL, ROI and win rate for the selected time window. | #35 |
| FR-3 | When a client changes the time window, the system shall update P1 for that window without leaving the page. | #35 |
| FR-4 | When a client applies a filter, the system shall show only the traders that match it, without leaving the page. | #35 |
| FR-5 | When a client sorts by total PNL, the system shall order the listed traders by total PNL, highest first. | #35 |
| FR-6 | When a client sorts by ROI, the system shall order the listed traders by ROI, highest first. | #35 |
| FR-7 | When a client clicks a trader on P1, the system shall open P2 for that trader's wallet. | #35 |
| FR-8 | When a client enters a wallet address, the system shall open P2 for that address. | #35 |
| FR-9 | If the entered address is not a valid wallet address, then the system shall show an error message and stay on the current page. | #35 |
| FR-10 | When a client goes back from P2, the system shall return to P1. | #35 |
| FR-11 | When P2 is shown, the system shall list the wallet's open positions and closed positions separately. | #36 |
| FR-12 | When P2 shows an open position, the system shall show its current mark price, its unrealized PNL, and the resolution date of its market. | #36 |
| FR-13 | When P2 is shown, the system shall show the wallet's realized PNL, unrealized PNL and their total, as computed under `docs/specs/pnl-calculation.md`. | #36 |
| FR-14 | When P2 is shown, the system shall show the wallet's cumulative realized and unrealized PNL over time. | #36 |
| FR-15 | When P2 is shown, the system shall show the wallet's per-position PNL distribution, win rate, PNL by period, and the share of total PNL that comes from its largest win. | #36 |
| FR-16 | When P2 is shown, the system shall show the wallet's position sizes, capital at risk over time, and PNL divided by capital deployed. | #36 |
| FR-17 | When P2 is shown, the system shall list the wallet's trades. | #36 |
| FR-18 | When P3 is shown, the system shall show PNL and volume grouped by market and by market category, across all wallets. | #36 |
| FR-19 | When a client opens P3 from a wallet on P2, the system shall show that wallet's PNL grouped by market, category and strategy label, with position sizes and holding periods. | #36 |
| FR-20 | When P4 is shown, the system shall list wallets ranked by how early they entered positions that resolved as winners, using the definition settled in OQ-3. | #36 |

FR-12 marks open positions at the latest price, the mark price our mentor set
on Oct 20, 2026 and `docs/specs/pnl-calculation.md` already uses (FR-12 there).

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Each dashboard page shall finish loading within 3 seconds. | Objective 3.4 and #37 set this target. The question list notes P1 and P4 may need precomputed tables to meet it. |
| NFR-2 | A PNL figure shown on the dashboard shall equal the figure the calculation produced for the same wallet and time window. | The dashboard must not recompute or drift from the validated numbers. |
| NFR-3 | Prices, shares and PNL are rounded only when displayed. | Matches NFR-2 of `docs/specs/pnl-calculation.md`. |

## Acceptance criteria (epic level)

- [ ] A client can open the dashboard, change the window, filter, sort by total
      PNL and by ROI, click a trader, and return to P1, all through the served
      interface and not by calling functions in a console.
- [ ] A client can enter a valid wallet address and reach P2, and an invalid
      address shows an error and does not change the page.
- [ ] P2 shows open and closed positions, realized and unrealized PNL, PNL
      over time, consistency metrics, capital deployed and trades for the
      chosen wallet.
- [ ] P3 and P4 each answer the client questions listed for them in Pages
      above.
- [ ] For a sample wallet, the PNL on the page matches the calculation output
      for that wallet.
- [ ] Each page loads within 3 seconds, measured the way OQ-7 settles.
- [ ] FR-1 to FR-20 each have a test that fails if the behavior is removed.
- [ ] Every functional requirement cites a story, and every open question
      below has an owner.
- [ ] This document is listed in proposal §4 under Specification and design
      documents.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| OQ-1. Which time windows does a client choose from? The question list proposes 7d, 30d, 90d and all-time plus a custom range. What are the default window, default sort, and the number of traders that count as "top"? (ask Erel) | Leila De Belen | before FR-2 to FR-4 are implemented |
| OQ-2. Is a leaderboard ranked by total PNL, realized-only PNL or return on capital, and is there a minimum trade count or volume so tiny wallets do not top it? FR-5 and FR-6 assume total PNL and ROI sorts. (ask Erel) | Leila De Belen | before FR-5 and FR-6 are implemented |
| OQ-3. How is "early" measured (time before resolution, time since market open, or price moved in the trader's favor after entry), and what threshold counts as "consistently"? (ask Erel) | Leila De Belen | before FR-20 is implemented |
| OQ-4. Which strategy labels do we derive from on-chain data (for example holding period, market category, position sizing, favorite vs. underdog)? (ask Erel) | Leila De Belen | before FR-19 is implemented |
| OQ-5. Are P3 and P4 built in this phase? The flow diagram (#97) shows only P1 and P2, so it needs P3 and P4 added if they are in scope. | Leila De Belen | before this PR is merged |
| OQ-6. When a client goes back to P1, are the window, filter and sort they chose kept? Also, what does P2 show for a valid address with no trades in the data, and for a wallet flagged incomplete under FR-5 of `pnl-calculation.md`? | Leila De Belen | before FR-10 and FR-11 are implemented |
| OQ-7. What counts as "loaded" for the 3 second target (first content, full table, or all charts), on what dataset size, and does #37 confirm 3 seconds, since the question list says "a few seconds"? | Leila De Belen | before NFR-1 is tested |
| OQ-8. Which story covers each page, so the Story column above is correct? FR-11 to FR-20 are assigned to #36. | Leila De Belen | before this PR is merged |

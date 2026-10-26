# Dashboard Questions (Objective 3.1, #34)

**Status:** Draft, awaiting mentor approval
**Parent:** Goal 3 (#33)
**Related:** Performance requirement in #37

## 1. Purpose

This document lists the questions clients want the PNL dashboard to answer. For each question it names the data that answers it and the dashboard page that presents it. No interface design is merged until the mentor has approved this list (see Section 6).

## 2. Dashboard pages

| Page | Purpose |
|------|---------|
| **P1. Trader Leaderboard** | Rank wallets by PNL over a selectable time window |
| **P2. Trader Profile** | Drill-down on a single wallet: PNL history, positions, trades |
| **P3. Markets & Strategies** | Break down returns by market, category, and strategy |
| **P4. Early Movers** | Identify wallets that are consistently early on winning outcomes |

## 3. Client questions

Source column: **Mentor** = from mentor guidance (#20), **Proposed** = added by the team for mentor review.

| ID | Question | Data that answers it | Page | Source |
|----|----------|----------------------|------|--------|
| Q1 | Who are the most profitable traders over a given window? | Per-wallet realized PNL, unrealized PNL, and total PNL, aggregated over the selected date range; trade timestamps | P1 | Mentor |
| Q2 | What markets and strategies drive their returns? | Per-wallet PNL grouped by market, market category, and strategy label; position sizes and holding periods | P3 (linked from P2) | Mentor |
| Q3 | Which wallets are consistently early on winning outcomes? | Entry timestamp and entry price per position vs. market open, price path, and resolution time; resolved outcome per position | P4 | Mentor |
| Q4 | How consistent is a trader's profitability, or is it driven by a few big wins? | Per-position PNL distribution, win rate, PNL by period, largest-win share of total PNL | P2 | Proposed |
| Q5 | How much capital does a trader deploy, and what return do they earn on it? | Position sizes, capital at risk over time, PNL divided by capital deployed | P1, P2 | Proposed |
| Q6 | How does a trader's PNL change over time? | Cumulative realized and unrealized PNL time series per wallet | P2 | Proposed |
| Q7 | What is a trader currently holding, and how much is unrealized? | Open positions, current mark price, unrealized PNL, linked market resolution date | P2 | Proposed |
| Q8 | Which markets or categories are the most profitable for traders overall? | PNL and volume aggregated across all wallets by market and category | P3 | Proposed |

## 4. Definitions to settle with the mentor

These affect how questions are answered, so they need a decision before design starts.

1. **Profitable.** Ranked by total PNL, realized-only PNL, or return on capital? Is there a minimum trade count or volume so tiny wallets do not top the board?
2. **Early (Q3).** Measured as time before resolution, time since market open, or price moved in the trader's favor after entry? What threshold counts as "consistently"?
3. **Strategy (Q2).** Which labels do we derive from on-chain data (for example holding period, market category, position sizing, or buying the favorite vs. the underdog)?
4. **Time windows.** Which presets (7d, 30d, 90d, all-time) plus custom range?
5. **Unrealized PNL.** What mark price do we use for open positions?

## 5. Non-functional requirement

Main views (P1 to P4) should load within a few seconds, per mentor guidance and #37. Questions that require heavy aggregation (Q1, Q3) may need precomputed tables. Confirm the specific target in #37.

## 6. Approval

The mentor approves this finished list before any interface design is merged.

- [ ] Mentor approved
- **Approver:** Erel Saul
- **Date:**
- **Evidence:** (link to meeting notes or PR/issue comment)

## 7. Change log

| Date | Change | Author |
|------|--------|--------|
| October 26, 2026 | Initial draft | Leila De Belen |

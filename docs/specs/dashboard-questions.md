# Dashboard Questions (Objective 3.1, #34)

**Status:** Approved by the mentor on November 5, 2026, with the changes below. Strategy labels (Section 4, item 3) are still open.

**Parent:** Goal 3 (#33)

**Related:** Performance requirement in #37

## 1. Purpose

This document lists the questions clients want the PNL dashboard to answer. For each question it names the data that answers it and the dashboard page that presents it. No interface design is merged until the mentor has approved this list (see Section 6).

## 2. Dashboard pages

| Page | Purpose |
|------|---------|
| **P1. Trader Leaderboard** | Rank wallets by PNL over a selectable time window, with a consistency metric for each wallet |
| **P2. Trader Profile** | Drill-down on a single wallet: PNL history, positions, trades |
| **P3. Markets & Strategies** | Break down returns by market, category, and strategy. Showing all wallets together (Q8) is a stretch goal. |
| **P4. Early Movers** | Identify wallets that are consistently early on winning outcomes |

## 3. Client questions

Source column: **Mentor** = from mentor guidance (#20), **Proposed** = added by the team for mentor review.
Status column: result of the mentor's review on November 5, 2026.

| ID | Question | Data that answers it | Page | Source | Status |
|----|----------|----------------------|------|--------|--------|
| Q1 | Who are the most profitable traders over a given window, and how consistent are they? | Per-wallet realized PNL, unrealized PNL, total PNL, return on capital, and trade timestamps, aggregated over the selected window. Consistency metric: win rate (share of closed positions that were profitable) or share of total PNL from the wallet's top few trades. Count of resolved trades. | P1 | Mentor | Approved. Absorbs Q4. |
| Q2 | What markets and strategies drive their returns? | Per-wallet PNL grouped by market, market category, and strategy label; position sizes and holding periods | P3 (linked from P2) | Mentor | Approved |
| Q3 | Which wallets are consistently early on winning outcomes? | Entry price (implied probability) and entry timestamp per position; price movement after entry toward the winning outcome; time between entry and resolution; resolved outcome per position | P4 | Mentor | Approved |
| Q4 | How consistent is a trader's profitability, or is it driven by a few big wins? | (moved to Q1) | P1 | Proposed | Merged into Q1 as a consistency metric on the leaderboard, not its own view |
| Q5 | How much capital does a trader deploy, and what return do they earn on it? | Position sizes, capital at risk over time, PNL divided by capital deployed | P1, P2 | Proposed | Approved. Return on capital is a toggle on the leaderboard (Section 4, item 1). |
| Q6 | How does a trader's PNL change over time? | Cumulative realized and unrealized PNL time series per wallet | P2 | Proposed | Approved |
| Q7 | What is a trader currently holding, and how much is unrealized? | Open positions, last traded price, unrealized PNL, linked market resolution date | P2 | Proposed | Approved |
| Q8 | Which markets or categories are the most profitable for traders overall? | PNL and volume aggregated across all wallets by market and category | P3 | Proposed | Stretch goal. Build only if time remains at the end. |

## 4. Definitions

Decisions from Erel Saul's message of November 5, 2026.

1. **Profitable (Q1, Q5): settled.** Rank by total PNL (realized + unrealized) by default, with return on capital as a toggle. A wallet needs at least 10 resolved trades to appear on the leaderboard, so one lucky bet cannot top it.
2. **Early (Q3): settled.** "Early" means the price moved in the trader's favor after entry: they bought at a low implied probability before the market repriced toward the winning outcome. Time before resolution is a secondary filter.
3. **Strategy (Q2): open.** The mentor did not answer which labels to derive from on-chain data (for example holding period, market category, position sizing, or favorite vs. underdog).
4. **Time windows: settled.** 7d, 30d, 90d, and all-time. A custom range was not mentioned in the reply, so it is not included.
5. **Unrealized PNL: settled.** Open positions are marked at the last traded price. Unrealized PNL is always labeled as unrealized and shown separately from realized PNL.

Still to settle (not answered on November 5):

- What counts as "low implied probability," how large a price move counts as "repriced," and what threshold counts as "consistently" early (Q3).
- Whether the 10 resolved trades minimum counts trades or positions, and whether it applies inside the selected window or over all time (Q1).
- Whether the consistency metric is win rate, share of PNL from the top few trades, or both, and how many trades is "a few" (Q1).

## 5. Non-functional requirement

Main views (P1 to P4) should load in under 3 seconds on the demo data, per mentor guidance and Objective 3.4 (#37). Questions that require heavy aggregation (Q1, Q3) may need precomputed tables.

## 6. Approval

The mentor approves this finished list before any interface design is merged.

- [x] Mentor approved
- **Approver:** Erel Saul
- **Date:** November 5, 2026
- **Evidence:** Erel Saul's Slack message of November 5, 2026 (link to a comment on #124 or paste the message there)

## 7. Change log

| Date | Change | Author |
|------|--------|--------|
| October 26, 2026 | Initial draft | Leila De Belen |
| November 5, 2026 | Erel Saul approved questions (#124) | Leila De Belen |
| November 8, 2026 | Applied mentor feedback: merged Q4 into Q1, made Q8 a stretch goal, settled definitions 1, 2, 4 and 5, set the 3 second target, recorded approval | Leila De Belen |

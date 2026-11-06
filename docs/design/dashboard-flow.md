> Epic: #33 · Stories: #34, #35, #36

# Dashboard page flow

Figure 1 shows how a SonarX client moves between dashboard pages. Each page answers questions in `docs/specs/dashboard-questions.md`.

![Page flow diagram with two pages. A client opens the leaderboard, clicks a trader to reach the wallet lookup page, or enters a wallet address to reach it directly, and can return to the leaderboard.](dashboard-flow.png)

*Figure 1 — Page flow. How does a client get from the top traders to the details of one wallet? Source: `dashboard-flow.mmd`.*

## Pages and the questions they answer

| Page | Story | Questions answered |
|------|-------|--------------------|
| Leaderboard | #35 | Q1, Q5 |
| Wallet lookup | #36 | Q4, Q6, Q7 |

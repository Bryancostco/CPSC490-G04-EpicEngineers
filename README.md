# CPSC 490 — Group 4 Epic Engineer

**Project title:** Polygon Prediction Market PNL and Trader Profitability Analytics
**Sponsor:** SNX-1
**Section:** 01 Tuesday

## Team

| Name | GitHub | Role | Leader |
|---|---|---|---|
| Orozco, Bryan | @Bryancostco | leader/QA | ✅ |
| De Belen, Leila | @leiladb | front end | |
| Cox, Justin | @justincox8 | back end | |
| Quach, Kyle | @kyquach | back end | |

**Contact person:** Bryan Orozco — bryancostco@csu.fullerton.edu

## Links

- **Proposal:** [`proposal/proposal.md`](proposal/proposal.md)
- **Project board:** [`projects`](https://github.com/users/Bryancostco/projects/1).
- **Specifications:** [`docs/specs/`](docs/specs/) · **Designs:** [`docs/design/`](docs/design/)
- **Prototype:** [`prototype/`](prototype/) — run instructions in its README
- **Sprint reviews:** [`docs/sprint-reviews/`](docs/sprint-reviews/)
- **Current sprint plan (start here):** [`docs/sprint-plans/sprint-3.md`](docs/sprint-plans/sprint-3.md)

## Project summary

Polymarket is a prediction market where people trade on the outcomes of real world events, and every trade is recorded on the Polygon blockchain. That raw on chain data shows what each wallet traded, but not how much it made or lost, and existing tracker sites rank the top traders without explaining what drives their success. We're proposing a profit and loss (PNL) accounting tool, built on SonarX's Polygon blockchain data, that parses on chain trades, matches positions to market resolutions, and computes realized and unrealized PNL for each wallet. It would then rank the most profitable traders and identify what drives their edge, in a dashboard that surfaces top performers and trading patterns. By the end of the semester, we'll have a complete proposal and a working prototype in `prototype/`, with the full dashboard built in CPSC 491.

## How we work

- Sprints: four 2-week sprints (`Sprint 1`–`Sprint 4` milestones).
  Sprint boundary ritual every other Tuesday.
- Every change lands by pull request; **the author never approves their own PR**.
- Every issue carries: assignee (owner), milestone (sprint), `priority:`,
  and a `sp:` story-point label.
- AI tools are used and disclosed — see the proposal's *AI Usage* section.

# Project context — SNX-1 Polymarket PNL, condensed

> Task: #63 · Epics: #24, #29, #33
> Owner: Bryan Orozco · Sprint: 2 · Status: draft

*One page the whole team, and any assistant, reads first. It holds the
decisions and research findings we keep needing, each with its source. It
does not repeat the proposal or the specifications; it points to them.*

## Where the detail lives

| For | Read |
|---|---|
| Goals, objectives and problem statements | [`proposal/proposal.md`](../proposal/proposal.md) §1.2 and §2 |
| How trades become positions and PNL | `docs/specs/pnl-calculation.md` (#55, PR #67) |
| How data moves through the system | `docs/design/data-flow.md` (#58, PR #68) |
| How we work (issues, PRs, sprints) | [`CLAUDE.md`](../CLAUDE.md) and [`CONTRIBUTING.md`](../CONTRIBUTING.md) |

## Phase 1 scope

This semester covers Phase 1 only: PNL per **proxy wallet**, computed from
historical data and validated against it. Phase 2, which links proxy wallets
to their owner (EOA) wallets and uses real time data, is future work. Source:
kickoff meeting, Oct 6, 2026 (#20).

## Mentor decisions

| Decision | Value | Source |
|---|---|---|
| Data source | SonarX's Snowflake warehouse | Kickoff, Oct 6 (#20) |
| Tools | Open source tools and libraries are allowed | Kickoff, Oct 6 (#20) |
| Phase 1 window | The last 12 months of Polygon data, extendable later | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |
| Cost basis | FIFO by default; raise any reason to change it with Erel | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |
| Unrealized PNL | Marked at the latest market price | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |
| Validation | Compare a handful of well known wallets against the Polymarket leaderboard; tolerance set together after a first pass | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |
| Dashboard audience | Client facing: SonarX's clients use it | Kickoff, Oct 6 (#20) |
| Dashboard order of work | Agree the questions first, then how to show each answer, and keep it fast | Kickoff, Oct 6 (#20) |
| Starting client questions | Most profitable traders over a window; which markets and strategies drive their returns; which wallets are consistently early on winning outcomes | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |
| Load time | A few seconds for the main views | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |
| Who to ask | Data and table questions go to Sergio in the SonarX Slack channel; Snowflake credentials and schema documents come through Slack | Erel, Oct 20 ([#20 comment](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20#issuecomment-6330393347)) |

## Glossary

Use these words the same way everywhere. The full definitions are in
`docs/specs/pnl-calculation.md`.

| Term | Meaning |
|---|---|
| Proxy wallet | The wallet that holds a Polymarket user's shares and shows up on chain as the trader. Phase 1 works at this level. |
| EOA | Externally owned account: the owner wallet behind one or more proxy wallets. Phase 2 only. |
| Position | All of one proxy wallet's shares in one outcome token (YES or NO) of one market. |
| Realized PNL | Profit or loss locked in by a sale or by the market resolving. |
| Unrealized PNL | Profit or loss on shares still held in an unresolved market, marked at the latest price. |
| FIFO cost basis | A sale is matched against the oldest shares bought first, at the price paid for them. |

## Research by member

### Kyle Quach — how prediction markets and Polymarket work (#12)

- Polymarket is a prediction market on Polygon where users trade on real
  world event outcomes; prices act as probabilities, and a winning share is
  worth $1 while a losing share is worth $0. Polymarket 101,
  https://docs.polymarket.com/polymarket-101 (accessed Oct. 4, 2026).
- There is no house: every trade's counterparty is another user, so prices
  come only from supply and demand. What is Polymarket, Polymarket Help
  Center, https://help.polymarket.com/en/articles/13364060-what-is-polymarket
  (accessed Oct. 4, 2026).
- Prediction markets in general let people trade contracts on future events.
  Fidelity, https://www.fidelity.com/learning-center/trading-investing/prediction-markets
  (accessed Oct. 4, 2026).
- Contracts settle at a fixed amount or become worthless once the outcome is
  known, which makes losses sharper than in traditional markets. Investopedia,
  https://www.investopedia.com/terms/p/prediction-market.asp (accessed Oct. 4, 2026).

### Justin Cox — existing PNL and leaderboard tools (#13)

- **Polymarket's own leaderboard** is our validation benchmark. Its all time
  board counts realized profit only, while shorter windows use the change in
  marked account value, so the meaning of "profit" depends on the window.
  https://polymarket.com/leaderboard and
  https://docs.polymarket.com/api-reference/boards/get-the-trader-leaderboard
  (accessed Oct. 4, 2026).
- **Polymarket Analytics, Predicts.guru, Polycopy, Polynyx and PolyWallet**
  all rank wallets by PNL. Polynyx says it rebuilds PNL from each wallet's
  trades but, like the others, does not publish the method, and none of
  them explains what drives a trader's edge. That gap is what Goals 1 and 2
  address. Links and dates are on #13.

### Bryan Orozco — mentor answers and scope (#20)

- The kickoff notes and Erel's Oct 20 follow up on #20 are the source for
  every row in the Mentor decisions table above.

### Leila De Belen

Not shared in the repository yet. Leila's research goes here, with sources
and dates accessed, before this document is marked final.

## Open questions we are waiting on

The open questions for Erel and Sergio live in the Open questions table of
`docs/specs/pnl-calculation.md`, so there is one list to keep current.

> Epic: #24 · Stories: #25, #26, #27 · Task: #59
> Owner: Justin Cox · Sprint: 2 · Status: draft
> Specification: [`../specs/pnl-calculation.md`](../specs/pnl-calculation.md)

# Design — Sequence of one PNL run

*What happens, in order, between the components of the PNL pipeline during one
run: pull trades and market resolutions from SonarX's Snowflake database,
build positions, compute realized and unrealized PNL, and save the results.
The lifelines are the components in
[`architecture.md`](architecture.md), and the step numbers are the pipeline
steps in the specification. Every box and arrow is something the team has
decided to build; anything not decided is named in §4 and §5 instead of
drawn.*

## 1. The picture

Figure 1 shows one run for a single as of time T, from the first query to the
saved results. Time runs from top to bottom. Solid arrows are calls, dashed
arrows are what comes back, and an arrow that loops back to its own lifeline
is work a component does by itself.

![Sequence diagram of one PNL run with five lifelines. Pull trades queries SonarX's Snowflake database for trades and then for market resolutions and receives both back, then passes them to Build positions. Build positions builds positions and FIFO lots, then matches them to resolutions and sets each open or closed, then sends the positions to Compute PnL. Compute PnL realizes and marks the PNL and totals it per wallet, then saves the results to Results storage.](diagrams/pnl-run-sequence.png)

*Figure 1 — UML sequence diagram of one PNL run. It answers one question: in
what order do the components talk to each other, and what do they pass, when
the pipeline runs once? Source:
[`diagrams/pnl-run-sequence.mmd`](diagrams/pnl-run-sequence.mmd). Step numbers
and FR numbers are from [`pnl-calculation.md`](../specs/pnl-calculation.md).*

Figure 1 displays what happens when we compute profit and loss in order. Time runs from the top of the diagram to the bottom, where each column is a part of our system. Pull trades requests SonarX's Snowflake database for the last 12 months of trades and results. It then hands those off to build positions where it groups the trades into a position for each and every wallet as well as its market and outcome. It then matches each one to its market's result and marks whether it's open or closed.

Compute PnL calculates the profit or loss on each position, then adds up each wallet's total and saves the results.

## 2. Lifelines

One lifeline for each component in the high level architecture in
[`architecture.md`](architecture.md) that takes part in a run.

| Lifeline | Box in `architecture.md` | What it does in a run | Pipeline step |
|---|---|---|---|
| SonarX-owned Snowflake database | SonarX-owned Snowflake database | Answers the two queries; it is outside our system | none (data source) |
| Pull trades | Pull trades | Queries trades and market resolutions, and hands both on | 1 |
| Build positions | Build positions | Groups trades into positions and FIFO lots, then sets each position open or closed | 2 and 3 |
| Compute PnL | Compute PnL | Computes realized and unrealized PNL per position and per wallet | 4 |
| Results storage | Results storage (pending #52) | Receives the saved results | none (storage) |

## 3. Messages, in order

| Order | From → to | What is sent or done | Step | Specification |
|---|---|---|---|---|
| 1 | Pull trades → Snowflake | Query the Polymarket trades in the 12 month window ending at T | 1 | `docs/specs/data-sources.md` (#25) |
| 2 | Snowflake → Pull trades | The trades | 1 | same |
| 3 | Pull trades → Snowflake | Query the market resolutions | 1 | same |
| 4 | Snowflake → Pull trades | The resolutions | 1 | same |
| 5 | Pull trades → Build positions | Hand over the trades and the resolutions | 1 to 2 | |
| 6 | Build positions (itself) | Group trades into one position per wallet, market and outcome token; apply them in chain order; add a lot per buy; take sales from the oldest lot first and add the realized PNL of each sale; flag a position incomplete when a sale is bigger than its lots | 2 | FR-1 to FR-7 (#26, #27) |
| 7 | Build positions (itself) | Match each position to its market's resolution and mark it open or closed | 3 | FR-8 to FR-10 (#26) |
| 8 | Build positions → Compute PnL | Send the positions with their remaining lots, status, incomplete flag, realized PNL from sales, and the payout per share of resolved markets | 3 to 4 | |
| 9 | Compute PnL (itself) | Realize the lots still held in resolved markets; mark the lots of open positions at the latest price; set unrealized PNL to zero for closed positions; total each wallet and carry the incomplete flag onto it | 4 | FR-11 to FR-15 (#27) |
| 10 | Compute PnL → Results storage | Save the PNL per position and per wallet | none | |

Messages 1 to 4 come from step 1, which `pnl-calculation.md` defines as
"Extract trades and market resolutions". The two queries are separate arrows
because the trades and the resolutions are two different kinds of data.

## 4. Choices to confirm in review

`DIAGRAMS.md` §5 says an arrow is a claim about how components depend on each
other. The diagram has to make four claims that no existing document states
word for word. They are proposals from this first draft, and the team should
confirm or change each one when it reviews this pull request.

| Proposal | Why it is not already settled | Where it shows in Figure 1 |
|---|---|---|
| **Build positions does steps 2 and 3.** There is no separate box for matching positions to resolutions. | `architecture.md` has one box between Pull trades and Compute PnL, but the specification has two steps there (2 and 3) and the data flow design (#58) draws two processes (2.0 and 3.0). | Messages 6 and 7 both belong to the Build positions lifeline. |
| **Compute PnL writes to Results storage.** | `architecture.md` draws Compute PnL → Rank wallets → Data results → Results storage. This issue asks for a run that ends with "write results" right after the PNL is computed, so ranking (step 5, specified in #54) is not part of this run. | Message 10 goes straight from Compute PnL to Results storage. |
| **Positions and lots travel between components and are not saved.** Only the PNL results are saved. | The data flow design (#58) draws stores between the steps (D1 trades and resolutions, D2 positions and lots, D3 wallet PNL). Which of them are saved is a storage question that waits for #52. NFR-3 in the specification asks that every figure traces back to its lots, which may need positions and lots saved too. | Message 8 is a call that carries the positions; no arrow goes to Results storage until message 10. |
| **Pull trades fetches the resolutions as well as the trades.** | The box is named "Pull trades", while step 1 covers trades and resolutions. | Messages 1 to 4. |

## 5. Left out on purpose

A box or arrow nobody has chosen would break `DIAGRAMS.md` §5, so these are
named here and not drawn.

- **What starts a run.** No scheduler, command or button has been chosen. The
  note at the top of Figure 1 says so. The data flow design (#58) lists the
  refresh schedule as not designed yet.
- **Where the latest price comes from.** Open question Q3 in the
  specification. The data flow design (#58) proposes the most recent trade,
  which would need Compute PnL to have the trades; Figure 1 does not draw
  that until Q3 is answered.
- **Failures and retries**, such as a query that fails or a write that does
  not land. No behavior has been decided.
- **What a second run for the same T does to saved results** (replace or add).
  NFR-1 in the specification requires identical results, and storage is
  pending #52.
- **Ranking and trading metrics (step 5, #54), serving the dashboard (step 6,
  #33).** They come after the run in this document.
- **Storage technology and the stack.** Decided in #52.
- **Events other than buys and sells** (splits, merges, redemptions,
  transfers). Open question Q4 in the specification.
- **Phase 2**: linking proxy wallets to owner wallets, and real time data.

## 6. What was checked and what was not

Checked by reading Figure 1 against the documents it depends on: every
lifeline matches a box in `architecture.md`; messages 5 and 8 follow the
arrows Pull trades → Build positions and Build positions → Compute PnL;
messages 1 to 4 are the request and reply that sit on the "Source data" arrow
from the database to Pull trades; message 10 matches no arrow there and is
proposal 2 in §4; each step number and FR range matches the pipeline steps
table and the functional requirements table in
[`pnl-calculation.md`](../specs/pnl-calculation.md).

Not checked: whether SonarX's data can be queried as two separate queries
(no SonarX schema document has been received, see #57 and #25); that the
proposals in §4 are what the team wants; and that the exported image matches
the Mermaid source after any later edit, so re-export both together.

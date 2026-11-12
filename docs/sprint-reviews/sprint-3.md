# Sprint 3 review — Oct 27 – Nov 9

> Group 04 Epic Engineers · SNX-1 · Sprint 3 review Tue Nov 10 · Task: #142

**Draft, Nov 7.** Velocity, the completed table, the carried over reasons and
the contribution snapshot are filled in after the sprint ends on Monday,
Nov 9 (Pacific time). Everything else below is true as of Nov 7. Open pull
requests are listed with their state on Nov 7; any not merged by Nov 9 move
to Carried over, because we treat unmerged work as unfinished
(`CONTRIBUTING.md`).

## What Sprint 3 asked for

From the course guide (§6) for Groups 01 to 05: design documents with
diagrams (architecture, system context, ER, DFD), a prototype that proves the
riskiest design choice, and the spring timeline drafted. Report draft #1 was
due Nov 1.

| Asked for | Where it stands on Nov 7 | Where |
|---|---|---|
| Architecture and system context diagrams | Revised diagrams merged into `main` | PR #81 (sub-task #80) |
| ER diagram | Merged Nov 5 | PR #136 (task #57) |
| Data flow diagrams, Level 0 and Level 1 | Written in Sprint 2, restored to `develop` Nov 5 | PR #135 (task #58) |
| Dashboard page flow | Merged Nov 5; its paragraph added to §4 Nov 7 | PR #79 (task #60), PR #145 (task #97) |
| Prototype proves the riskiest design choice | Positions, FIFO lots and open or closed status on the spec's worked example merged Nov 5; FIFO realized and unrealized PNL (#110, #111) in progress with @justincox8 on Nov 7 | PRs #138, #139, #140 (tasks #62, #108, #109) |
| Spring timeline (proposal §6) | Drafted Nov 7, in review; owners and hours wait on the team | PR #150 (task #149) |

## Progress this sprint — the substance

**Proposal moved:**
| Section | What changed | Where |
|---|---|---|
| §3 Proposed Approaches | Written | PR #77 (task #49), merged Oct 27 |
| §4 Specification and design documents | Architecture revision indexed | PR #81 (sub-task #80), merged into `main` |
| §4 Planned activities | Rewritten as prose grouped by goal and objective, citing the 52 new feature and task issues (#83 to #134), per Kyoung's Sprint 3 guidance | PR #135 (task #82), merged Nov 5 |
| §4 Environment | The prototype stack recorded: Python outside Snowflake | PR #137 (task #52), merged Nov 5 |
| §4 Specification and design documents | The full text of every spec and design document copied in, with all 7 figures; the Word export is 64 pages | PR #143 (task #141), merged Nov 7 |
| §4 Specification and design documents | Each figure appears once: summaries moved into their own documents, and CI checks the copies | PR #148 (task #147), in review |
| §5, §6, §7 | First drafts of the outcomes, the spring timeline and the AI usage disclosure; AI rules updated and §4's facts corrected | PR #150 (tasks #149, #152), in review |
| §4 Dashboard page flow | Paragraph describing the page flow (@leiladb) | PR #145 (task #97), merged Nov 7 |
| Issue board | Every user story broken into features and tasks as sub-issues (#83 to #134); carried over Sprint 2 issues moved to the Sprint 3 milestone | Issues |

**Prototype moved:** `prototype/` changes from the course's login example to
our own project (merged Nov 5): a Python skeleton with settings from
environment variables and a Snowflake client (#62), position grouping and
FIFO lots (#108), and open or closed status against market resolutions
(#109), each requirement with a test that fails if the requirement is
removed. The live Snowflake smoke query still waits for credentials.

## Velocity

Filled in on Nov 9 from `python scripts/sprint_report.py --sprint 3`.

## Completed (merged PRs)

Merged into `develop` or `main` so far this sprint:

| Story | Owner | Points | PR |
|---|---|---|---|
| #49 Write §3 Proposed Approach | @leiladb | 2 | PR #77, merged Oct 27 |
| #80 Revision of the architecture and system context diagrams | @kyquach | under #56 | PR #81, merged Nov 5 into `main` |
| #59 PNL run sequence diagram | @justincox8 | under #87 | PR #151, merged Nov 8 |

The rest of this table is filled in on Nov 9.

## Carried over — and why

Final reasons are added on Nov 9. Known so far:

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #103, #104 Data source specification | @justincox8 | Waits on SonarX's schema documents; Erel sent console invites to our school emails on Oct 30 | Start as soon as the console shows the Polymarket tables |
| #105 Snowflake extract queries | @kyquach | Same | Same |
| #110, #111 FIFO realized PNL, unrealized PNL and totals | @justincox8 | In progress on Nov 7; #108 and #109 merged Nov 5 | Carried to Sprint 4 if not merged by Nov 9 |
| #116 to #119 Rankings and behavior metrics | @kyquach, @justincox8 | Wait on #111 | Sprint 4 |
| #106 Architecture document in six sections | @kyquach | Not started; after PR #81 the document is only diagrams | Decide on Nov 10 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | Filled in on Nov 9 |
| Harness rules added (rows in the harness log) | 4 (`docs/aidlc/harness-log.md`, rows dated Nov 3 and Nov 5) |

## Prototype increment

Filled in on Nov 9 from what is merged. Merged on Nov 5 and rerun on Nov 7:
from `prototype/`, `python -m pytest -q` passes 26 tests (1 more, the live
Snowflake smoke test, skips without credentials).

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Sprint 3 guidance: describe the planned activities in prose, and break each story into features and tasks (Kyoung) | §4 work items rewritten as prose; 52 feature and task issues filed under the stories | #82, PR #135 |
| Console access to SonarX's schemas and a sample query result, invites to our school emails (Erel, SonarX Slack, Oct 30) | Unblocks the data source specification and the extract queries once the invites arrive | #103, #104, #105 |
| Keep client questions 1, 2, 3, 5, 6 and 7; fold 4 into 1 as a consistency metric (win rate or share of PNL from the top few trades); keep 8 as a stretch goal (Erel, SonarX Slack, Nov 5) | The question list is approved with these changes; the list in `docs/specs/dashboard-questions.md` is updated in its own PR | #124, #123, PR #73 |
| "Profitable" defaults to total PNL (realized plus unrealized) with return on capital as a toggle, and a minimum of 10 resolved trades so one lucky bet does not top the leaderboard (Erel, Nov 5) | Differs from the ranking spec, which filters only the ROI ranking and uses other thresholds; raised on #115 for Justin | #115 |
| "Early" means the price moved toward the winning outcome after entry; time before resolution is a secondary filter (Erel, Nov 5) | A new metric the ranking spec does not define yet; raised on #115 | #115 |
| Time windows: 7 days, 30 days, 90 days and all time (Erel, Nov 5) | For Phase 1, all time means the 12 month window; raised on #115 | #115 |
| Section 4 shows the ER diagram twice (@leiladb and @justincox8, Discord, Nov 7) | Keep the full documents for the 50 page paper; move each hand written summary into its document; CI checks the copies | #147, PR #148 |
| An assistant may now help write the proposal, not only the documents and code (Kyoung, in class, week of Nov 2) | Development plan §3 rewritten with the conditions we follow; §7 discloses AI use per section; §4's stale "who did what" facts corrected | #152, PR #150 |
| Nobody has SonarX console access a week after the Oct 30 promise (@justincox8, Discord, Nov 6) | Tracked as its own task, owned by @Bryancostco | #153 |
| Unrealized PNL at the last traded price, labelled clearly as unrealized (Erel, Nov 5) | Matches the PNL spec's definition of latest price; the label goes in the dashboard spec | #107, #125 |

## Contribution snapshot

Filled in on Nov 9 from the repository, as in Sprint 1 and Sprint 2. As of
Nov 5, merged so far this sprint: @leiladb 1 (PR #77), @kyquach 1 (PR #81),
@Bryancostco 0, @justincox8 0; reviews given: @justincox8 1 (PR #77),
@leiladb 1 (PR #81). Ten pull requests are open and waiting on review.

## Development plan revisited

| Risk | Status on Nov 7 |
|---|---|
| R1 Snowflake access arrives late | Still a problem: console invites were promised Oct 30; on Nov 7 nobody on the team has them, and credentials are not in hand |
| R2 The prototype stack is still undecided | Resolved: decided Nov 5 and recorded in PR #137 |
| R5 Contribution stays uneven | Still a problem; see the contribution snapshot on Nov 9 |

The QA / harness owner for Sprint 3 is @justincox8 (`docs/development-plan.md`
§1).

## What we change next sprint

Filled in at the Sprint 3 review on Nov 10.

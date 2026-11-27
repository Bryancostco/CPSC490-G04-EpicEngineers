# Sprint 3 review — Oct 27 – Nov 9

> Group 04 Epic Engineers · SNX-1 · Sprint 3 review Tue Nov 10 · Task: #142

The sprint ended on Monday, Nov 9 (Pacific time). Everything below is the
final state on Nov 9 unless a line says otherwise. Pull requests that were
still open on Nov 9 are listed under Carried over, because we treat unmerged
work as unfinished (`CONTRIBUTING.md`).

## What Sprint 3 asked for

From the course guide (§6) for Groups 01 to 05: design documents with
diagrams (architecture, system context, ER, DFD), a prototype that proves the
riskiest design choice, and the spring timeline drafted. Report draft #1 was
due Nov 1.

| Asked for | Where it stands on Nov 9 | Where |
|---|---|---|
| Architecture and system context diagrams | Revised diagrams merged Nov 5; `architecture.md` expanded into the six design sections and merged Nov 9 | PR #81 (sub-task #80), PR #157 (task #106) |
| ER diagram | Merged Nov 5 | PR #136 (task #57) |
| Data flow diagrams, Level 0 and Level 1 | Written in Sprint 2, restored to `develop` Nov 5 | PR #135 (task #58) |
| PNL run sequence diagram | Merged Nov 8 | PR #151 (task #59) |
| Dashboard page flow | Merged Nov 5; its paragraph added to §4 Nov 7 | PR #79 (task #60), PR #145 (task #97) |
| Prototype proves the riskiest design choice | Positions, FIFO lots and open or closed status on the spec's worked example merged Nov 5; FIFO realized and unrealized PNL (#110, #111) carried to Sprint 4 | PRs #138, #139, #140 (tasks #62, #108, #109) |
| Spring timeline (proposal §6) | Drafted Nov 7 and in review; owners and hours wait on the team | PR #150 (task #149) |

## Progress this sprint — the substance

**Proposal moved:**
| Section | What changed | Where |
|---|---|---|
| §3 Proposed Approaches | Written | PR #77 (task #49), merged Oct 27 |
| §4 Specification and design documents | Architecture revision indexed, then the architecture document rewritten in six sections | PR #81 (sub-task #80), PR #157 (task #106) |
| §4 Planned activities | Rewritten as prose grouped by goal and objective, citing the 52 new feature and task issues (#83 to #134), per Kyoung's Sprint 3 guidance | PR #135 (task #82), merged Nov 5 |
| §4 Environment | The prototype stack recorded: Python outside Snowflake | PR #137 (task #52), merged Nov 5 |
| §4 Specification and design documents | The full text of every spec and design document copied in, with all 7 figures; the Word export is 64 pages | PR #143 (task #141), merged Nov 7 |
| §4 Specification and design documents | Each figure appears once: summaries moved into their own documents, and CI checks the copies | PR #148 (task #147), merged Nov 8 |
| §4 PNL run sequence | Diagram and its description added | PR #151 (task #59), merged Nov 8 |
| §4 Dashboard page flow | Paragraph describing the page flow (@leiladb) | PR #145 (task #97), merged Nov 7 |
| §4 Dashboard questions | Erel's approval of the client question list recorded | PR #146 (task #124), merged Nov 7 |
| §5, §6, §7 | First drafts of the outcomes, the spring timeline and the AI usage disclosure; AI rules updated and §4's facts corrected; the team added contributions and AI usage on Nov 8 | PR #150 (tasks #149, #152), in review |
| Issue board | Every user story broken into features and tasks as sub-issues (#83 to #134); carried over Sprint 2 issues moved to the Sprint 3 milestone | Issues |

**Prototype moved:** `prototype/` changed from the course's login example to
our own project (merged Nov 5): a Python skeleton with settings from
environment variables and a Snowflake client (#62), position grouping and
FIFO lots (#108), and open or closed status against market resolutions
(#109), each requirement with a test that fails if the requirement is
removed. Read only extract queries for trades and resolutions, tested
without Snowflake credentials, are written and in review (#105, PR #158).
The live Snowflake smoke query still waits for credentials.

## Velocity

From `python scripts/sprint_report.py --sprint 3` (run Nov 10):

| | Story points |
|---|---|
| Committed at sprint start | 16 |
| Added mid sprint | 20 |
| Completed in the sprint | 10 |
| Open or carried over | 26 |
| Closed late | 0 |

Closed late is 0 this sprint: the workflow added in PR #135 now closes an
issue as soon as its pull request merges into `develop`, which fixed the gap
that showed 0 completed in Sprint 2.

Most of the open points (21 of 26) sit on the five objective stories #25,
#26, #27, #30 and #31. A story stays open until every task under it is
merged, and several of those tasks wait on SonarX data or on #110 and #111.
Seven tasks were filed during the sprint as the work became clear (#141,
#142, #147, #149, #152, #154, #155), which is part of the points added mid
sprint. The report suggests committing about 10 points in Sprint 4.

## Completed (merged PRs)

| Story | Owner | Points | PR |
|---|---|---|---|
| #49 Write §3 Proposed Approach | @leiladb | 2 | PR #77, merged Oct 27 |
| #34 Dashboard client question list (objective 3.1) | @leiladb | 2 | PR #73, PR #146 |
| #123 Draft `docs/specs/dashboard-questions.md` | @leiladb | under #34 | PR #73, merged Nov 5 |
| #124 Get the question list approved by Erel | @leiladb | under #34 | PR #146, merged Nov 7 |
| #95 Dashboard client question list (feature) | @leiladb | under #34 | PR #73, PR #146 |
| #60 Dashboard page flow | @leiladb | under #35 | PR #79, merged Nov 5 |
| #97 Dashboard page flow design | @leiladb | under #35 | PR #145, merged Nov 7 |
| #57 Data model and ER diagram | @justincox8 | under #87 | PR #136, merged Nov 5 |
| #59 PNL run sequence diagram | @justincox8 | under #87 | PR #151, merged Nov 8 |
| #80 Revision of the architecture and system context diagrams | @kyquach | under #56 | PR #81, merged Nov 5 |
| #106 Architecture document in six sections | @kyquach | under #85 | PR #157, merged Nov 9 into `main` |
| #82 Bring the repo in line with the Sprint 3 instructions | @Bryancostco | 2 | PR #135, merged Nov 5 |
| #58 Data flow design | @Bryancostco | under #87 | PR #135, merged Nov 5 |
| #52 Record the prototype stack | @Bryancostco | 1 | PR #137, merged Nov 5 |
| #62 Prototype skeleton and Snowflake client | @Bryancostco | under #84 | PR #138, merged Nov 5 |
| #108 Position grouping and lots | @Bryancostco | under #88 | PR #139, merged Nov 5 |
| #109 Resolution matching and open or closed status | @Bryancostco | under #88 | PR #140, merged Nov 5 |
| #53 Sprint 2 review | @Bryancostco | 1 | PR #72, merged Nov 5 |
| #141 Full spec and design documents in §4 | @Bryancostco | 2 | PR #143, merged Nov 7 |
| #147 Fix duplicate figures in §4 and check the copies | @Bryancostco | 1 | PR #148, merged Nov 8 |
| #142 Sprint 3 review draft | @Bryancostco | 1 | PR #144, merged Nov 8 |

## Carried over — and why

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #110, #111 FIFO realized PNL, unrealized PNL and totals | @justincox8 | Not merged by Nov 9 | First priority in Sprint 4; it unblocks #112, #116 to #120 |
| #116 to #119 Rankings and behavior metrics | @kyquach, @justincox8 | Wait on #111 | Sprint 4, after #111 |
| #103, #104 Data source specification | @justincox8 | Waits on SonarX's schema documents; console access arrives Nov 10 | Start as soon as the console shows the Polymarket tables |
| #105 Snowflake extract queries | @kyquach | Queries and fixture tests written; PR #158 opened Nov 9 into `main` | Retarget to `develop`, review, and run against Snowflake once credentials arrive |
| #125 Dashboard specification | @leiladb | Written after Erel approved the questions; PR #159 opened at the end of the sprint | Review early in Sprint 4 |
| #149, #152 Proposal §5 to §7 and the AI rules | @Bryancostco | PR #150 waits on a review | Review and merge early in Sprint 4 |
| #107, #115 Open questions for Erel and Sergio | @Bryancostco | Erel's Nov 5 answers are posted on both issues; the data questions for Sergio need the console | Ask Sergio once access arrives, then write the answers into the specs |
| #153 SonarX console access | @Bryancostco | Followed up in the SonarX Slack on Nov 7 and Nov 9; access arrives Nov 10 | Close once all four members can log in |
| #154 Release 0.4 | @Bryancostco | `main` has PR #157, which `develop` does not have yet | Sync `main` into `develop`, then release |
| #155 Remove the blank review row in `data-model.md` | @justincox8 | Filed Nov 8 as a small cleanup | Sprint 4 |
| #112, #120 Prototype README for the PNL slice, hand check of the metrics | @Bryancostco | Wait on #110 and #111 | Sprint 4 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | 4.2 over 18 merged PRs (median 2; 4 were green on the first CI run) |
| Harness rules added (rows in the harness log) | 5 (`docs/aidlc/harness-log.md`, rows dated Nov 3, Nov 5 and Nov 7) |

Iterations come from the CI runs on each pull request's branch, counted up
to the first green run. Most pull requests went green within two runs;
three took 13 or 14 runs, which raises the average. The new harness rules
came from real failures this sprint: issues not closing on merges into
`develop`, the `.env.example` template being ignored, the PR template's
reviewer comment, and the §4 document copies going stale.

## Prototype increment

What a reviewer can run on `develop` today: from `prototype/`,
`python -m pytest -q` passes 26 tests and skips 1, the live Snowflake smoke
test, which needs credentials. Evidence: the CI run on `develop` at commit
`497e42d` (Nov 8) and on `main` at `9f50483` (Nov 9), "Prototype build &
tests" job, both reporting `26 passed, 1 skipped`.

The slice covers trades grouped into positions per wallet and market, FIFO
lots, and open or closed status against market resolutions, on the PNL
spec's worked example (`prototype/tests/fixtures/pnl_worked_example.json`).
Realized and unrealized PNL (#110, #111) are the next step.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Sprint 3 guidance: describe the planned activities in prose, and break each story into features and tasks (Kyoung) | §4 work items rewritten as prose; 52 feature and task issues filed under the stories | #82, PR #135 |
| Sprint 3 guidance: each design document has six parts (Kyoung) | `architecture.md` rewritten in the six sections | #106, PR #157 |
| Console access to SonarX's schemas and a sample query result, invites to our school emails (Erel, SonarX Slack, Oct 30) | Unblocks the data source specification and the extract queries once the invites arrive | #103, #104, #105 |
| Keep client questions 1, 2, 3, 5, 6 and 7; fold 4 into 1 as a consistency metric (win rate or share of PNL from the top few trades); keep 8 as a stretch goal (Erel, SonarX Slack, Nov 5) | The question list is approved with these changes and recorded | #124, #123, PR #73, PR #146 |
| "Profitable" defaults to total PNL (realized plus unrealized) with return on capital as a toggle, and a minimum of 10 resolved trades so one lucky bet does not top the leaderboard (Erel, Nov 5) | Differs from the ranking spec, which filters only the ROI ranking and uses other thresholds; posted on #115 for @justincox8 to decide how the spec changes | #115 |
| "Early" means the price moved toward the winning outcome after entry; time before resolution is a secondary filter (Erel, Nov 5) | A new metric the ranking spec does not define yet; posted on #115 | #115 |
| Time windows: 7 days, 30 days, 90 days and all time (Erel, Nov 5) | For Phase 1, all time means the 12 month window; posted on #115 | #115 |
| Unrealized PNL at the last traded price, labelled clearly as unrealized (Erel, Nov 5) | Matches the PNL spec's definition of latest price; posted on #107; the label goes in the dashboard spec | #107, #125 |
| Section 4 shows the ER diagram twice (@leiladb and @justincox8, Discord, Nov 7) | Keep the full documents for the 50 page paper; move each hand written summary into its document; CI checks the copies | #147, PR #148 |
| An assistant may now help write the proposal, not only the documents and code (Kyoung, in class, week of Nov 2) | Development plan §3 rewritten with the conditions we follow; §7 discloses AI use per section; §4's stale "who did what" facts corrected | #152, PR #150 |
| Nobody had SonarX console access a week after the Oct 30 promise (@justincox8, Discord, Nov 6) | Tracked as its own task; the team followed up with Erel in the SonarX Slack on Nov 7 and Nov 9; access arrives Nov 10 | #153 |

## Contribution snapshot

| Member | Meetings attended | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @Bryancostco | team to fill in | 9 (#72, #135, #137, #138, #139, #140, #143, #144, #148) | 10 | 1 (#151) |
| @justincox8 | team to fill in | 2 (#136, #151) | 2 | 10 (#72, #73, #77, #79, #135, #139, #140, #145, #146, #148) |
| @leiladb | team to fill in | 5 (#73, #77, #79, #145, #146) | 6 | 7 (#81, #136, #137, #138, #143, #148, #157) |
| @kyquach | team to fill in | 2 (#81, #157) | 2 | 1 (#144) |

Merged PRs and reviews count Sprint 3 only (Oct 27 to Nov 9) and come from
the repository. Issues closed counts the Sprint 3 milestone. Meetings
attended is for the team to fill in.

Everyone worked well this sprint. All four members met the working
agreement of at least 2 merged contributions, every pull request was
reviewed by a teammate who was not its author, and the reviews were shared
across the whole team. @leiladb carried the dashboard work from Erel's
approval of the question list to the page flow and the dashboard spec.
@justincox8 delivered the data model and the PNL run sequence diagram and
gave the most reviews on the team, which kept pull requests moving.
@kyquach revised the architecture diagrams, rewrote the architecture
document in six sections, and wrote the extract queries ahead of the
credentials. @Bryancostco set up the repository for Sprint 3, built the
first prototype slice and brought the full documents into §4. Teammates
also kept following up with SonarX in the Slack channel until access came
through.

## Development plan revisited

| Risk | Status on Nov 9 |
|---|---|
| R1 Snowflake access arrives late | Improving: console access arrives Nov 10, eleven days after the Oct 30 promise. The extract queries (#105) were written and tested without credentials in the meantime, so the team is ready to use the access right away |
| R2 The prototype stack is still undecided | Resolved: decided Nov 5 and recorded in PR #137 |
| R5 Contribution stays uneven | Resolved this sprint: all four members met the working agreement, and reviews were shared across the team |

The QA / harness owner for Sprint 3 is @justincox8 (`docs/development-plan.md`
§1).

## What we change next sprint

Filled in by the team at the Sprint 3 review on Nov 10. Proposed for
discussion:

- Open every pull request into `develop`, so `main` and `develop` stop
  drifting (PR #157 and PR #158 targeted `main` this sprint)
- Start #103, #104 and #105's live run on the first day of console access
- Merge #110 and #111 first, since the rankings, metrics and validation wait
  on them

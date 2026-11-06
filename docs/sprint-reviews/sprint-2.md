# Sprint 2 review — Oct 13 – Oct 26

> Group 04 Epic Engineers · SNX-1 · Sprint 2 review Tue Oct 27 · Task: #53

Started Oct 24 and finished Nov 5, after the review meeting. All counts below
come from the repository and use Pacific time for the sprint boundary
(Oct 26, 11:59 pm).

## Progress this sprint — the substance

**Proposal moved:**
| Section | What changed | Where |
|---|---|---|
| §4 Planned activities | Every Sprint 2 task (#49 to #63, #65) cited as a typed reference, with its owner | PR #66 (task #65) |
| §4 Specification and design documents | First entries: the PNL calculation spec, the trader ranking spec, the architecture design and the implementation design | PR #67 (task #55), PR #75 (task #54), PR #76 (task #56), PR #78 (task #61) |
| §8 References | Template references replaced with sources [1] to [7], each with URL and access date | PR #69 (task #51) |
| Specification | `docs/specs/pnl-calculation.md`: positions, FIFO cost basis, open and closed status, realized and unrealized PNL, worked example | PR #67 (task #55) |
| Specification | `docs/specs/trader-ranking.md`: total PNL and ROI rankings, minimum activity rule, behavior metrics, worked example | PR #75 (task #54) |
| Design | `docs/design/architecture.md`: high level architecture and system context diagrams | PR #76 (task #56) |
| Design | `docs/design/implementation.md`: proposed prototype layout, configuration, secret handling and build order | PR #78 (task #61) |
| Project context | `docs/project-context.md`: mentor decisions with sources, glossary, research by member, linked from `CLAUDE.md` | PR #70 (task #63) |
| Development plan | Charter, QA owners, AI rules and risk register filled in | PR #71 (task #50) |
| Issue board | Sprint 2 tasks assigned, Sprint 3 and Sprint 4 milestones set on #26 to #28, #30 to #32 and #35 to #38 | Issues |

**Prototype moved:** It did not move this sprint. `prototype/` still holds the
course's login example. The project skeleton (#62) waits on the stack
decision (#52); the options were posted on #52 on Oct 24, but the team has
not decided.

## Velocity

From `python scripts/sprint_report.py --sprint 2` (run Nov 5):

| | Story points |
|---|---|
| Committed at sprint start | 0 |
| Added mid sprint | 7 |
| Completed in the sprint | 0 |
| Closed late | 7 |

The report reads 0 completed even though every pointed task's pull request
merged by Oct 26, for two reasons we have since fixed:

- **Closed late.** GitHub only closes an issue from `Closes #N` when the pull
  request merges into the default branch (`main`). Our feature pull requests
  merge into `develop`, so their issues stayed open until they were closed by
  hand on Nov 3. PR #135 adds a workflow that closes them on merge into
  `develop`.
- **Added mid sprint.** The Sprint 2 milestone was put on the tasks on Oct 24,
  after the sprint began, which is the same thing that happened in Sprint 1.

#52 and #53 (1 point each) were moved to the Sprint 3 milestone on Nov 5, so
the report no longer counts them here; they are listed under Carried over.

## Completed (merged PRs)

| Story | Owner | Points | PR |
|---|---|---|---|
| #65 Cite the Sprint 2 work items in proposal §4 | @Bryancostco | 1 | PR #66 |
| #55 Draft docs/specs/pnl-calculation.md | @Bryancostco | under #26 | PR #67 |
| #51 Fix §8 References in proposal.md | @Bryancostco | 1 | PR #69 |
| #63 Write the team source of truth doc | @Bryancostco | 2 | PR #70 |
| #50 Fill in docs/development-plan.md | @Bryancostco | 3 | PR #71 |
| #54 Draft docs/specs/trader-ranking.md | @justincox8 | under #30 | PR #75 |
| #56 Write docs/design/architecture.md | @kyquach | not pointed | PR #76 (into `main`) |
| #61 Write docs/design/implementation.md | @kyquach | not pointed | PR #78 (into `main`) |

PR #64 synced `main` into `develop` before the Sprint 2 branches. PR #76 and
PR #78 merged into `main` instead of `develop`, so `develop` did not get
either document until PR #135 synced them back.

## Carried over — and why

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #49 Write §3 Proposed Approach | @leiladb | PR #77 merged Oct 27, the first day of Sprint 3 | Done; counts toward Sprint 3 |
| #52 Record the chosen prototype stack | @Bryancostco | The stack is a team decision and the team has not made it; options were posted on #52 on Oct 24 | Decide at the next standup; it blocks every prototype task (#62, #105, #108 onward) |
| #53 Write the Sprint 2 review | @Bryancostco | Draft opened Oct 24 (PR #72); the numbers could only be filled in after the sprint ended | This file; closes when PR #72 merges |
| #57 Data model and ER diagram | @justincox8 | Not started in Sprint 2 | PR #136 opened Nov 5 |
| #58 Data flow design | @Bryancostco | PR #68 merged into the `55-pnl-calculation-spec` branch sixteen minutes after that branch merged into `develop`, so the document never reached `develop` | Restored in PR #135 |
| #59 PNL run sequence diagram | @justincox8 | Not started | Sprint 3 |
| #60 Dashboard page flow | @leiladb | PR #79 opened Oct 27 and is waiting on review | Merge after PR #135 |
| #62 Prototype skeleton and Snowflake connection | @kyquach | Blocked on #52; Snowflake credentials had not arrived | Sprint 3, starting with the parts that run on fixtures |
| #34 Dashboard client question list | @leiladb | Draft in PR #73; Erel has not approved the list yet (#124) | Sprint 3 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | 1.7 over 9 merged PRs (8 were green on the first CI run; PR #76 took 7) |
| Harness rules added (rows in the harness log) | 0 |

Iterations come from the CI runs on each pull request's branch, counted up
to the first green run.

## Prototype increment

None this sprint. See "Prototype moved" above.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Phase 1 window is the last 12 months of Polygon data (Erel, Oct 20, #20) | Written into the PNL spec's scope and the data flow design | #25, PR #67, PR #68 |
| Cost basis is FIFO by default; unrealized PNL is marked at the latest market price (Erel, Oct 20, #20) | FR-6, FR-7 and FR-12 in the PNL spec, with a worked example | PR #67 |
| Validate against the Polymarket leaderboard for a handful of well known wallets; set the tolerance together (Erel, Oct 20, #20) | Tolerance recorded as an open question in the PNL spec; the leaderboard is named as our benchmark in the project context | PR #67, PR #70 |
| Starting client questions for the dashboard (Erel, Oct 20, #20) | Recorded in the project context and on #34 for its question list | #34, PR #70 |
| Give stories #26 to #28, #30 to #32 and #35 to #38 a Sprint milestone (repo readiness card, Oct 24) | Sprint 3 and Sprint 4 milestones set | Issues |
| Cite #49 to #63 in proposal.md (repo readiness card, Oct 24) | All cited in §4 | PR #66 |
| Add #55 to #63 to the board (repo readiness card, Oct 24) | Added | Board |
| Assign all open issues to one person each (repo readiness card, Oct 24) | Sprint 2 issues assigned; Sprint 3 and 4 stories and the epics still to assign | Issues |
| Rewrite PR template text and add `Closes #N`; one PR closed no issue (repo readiness card, Oct 24) | PR #48 said `Closes #48`; changed to `Closes #42` | PR #48 |
| Give #12 and #13 their own `sp:` (repo readiness card, Oct 24) | Left unpointed: they are sub issues of task #11, which carries their points, and pointing them counts the work twice | #11 |

## Contribution snapshot

| Member | Meetings attended | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @Bryancostco | team to fill in | 8 (#48, #64, #66, #67, #68, #69, #70, #71) | 0 | 1 (#79) |
| @justincox8 | team to fill in | 1 (#75) | 0 | 5 (#64, #66, #67, #68, #70) |
| @leiladb | team to fill in | 0 | 0 | 4 (#69, #75, #76, #78) |
| @kyquach | team to fill in | 2 (#76, #78) | 2 (#56, #61) | 3 (#48, #71, #72) |

Merged PRs, issues closed and reviews count Sprint 2 only (Oct 13 to Oct 26)
and come from the repository. Issues closed is low across the team because
of the auto close gap described under Velocity: seven tasks whose pull
requests merged in Sprint 2 were closed by hand on Nov 3. Meetings attended
is for the team to fill in.

Our working agreement asks for at least 2 merged contributions per member
per sprint. Two members reached it and two did not (@justincox8 with 1 and
@leiladb with 0; Leila's §3 pull request, PR #77, merged on Oct 27, one day
after the sprint ended). Under the accountability rule in
`docs/development-plan.md` §1, both are named here with their plan: the
Sprint 3 plan (`docs/sprint-plans/sprint-3.md`) gives each of them a
sequence of tasks, and the team checks progress against it at the
Sprint 3 review.

## Development plan revisited

Three early warning signs in the risk register (`docs/development-plan.md`
§4) appeared during Sprint 2. The plan says a risk whose sign has appeared is
a problem, tracked in an issue:

| Risk | Sign that appeared | Tracked in |
|---|---|---|
| R1 Snowflake access arrives late | No Snowflake credentials by Oct 26; the team joined the SonarX Slack that day | The live queries (#105) and the data source spec (#103, #104); the prototype slice runs on fixtures meanwhile |
| R2 The prototype stack is still undecided | #52 still open on Oct 25, blocking #56, #61 and #62 | #52; #56 and #61 shipped as documents that defer the stack, #62 is still blocked |
| R5 Contribution stays uneven | Two members under 2 merged pull requests | The contribution snapshot above and the Sprint 3 plan |

No rule in the plan changes this sprint. The QA / harness owner for
Sprint 3 is @justincox8, as the plan's rotation says.

## What we change next sprint

- Pull requests merged into `develop` close their issues automatically
  (PR #135), so the sprint report counts work in the sprint it finished.
- Every feature pull request targets `develop`. Four did not (PR #76, PR #78,
  PR #81 and PR #136), which split `main` and `develop` twice; only release
  pull requests go into `main`.
- The stack (#52) is decided at the first Sprint 3 standup, because every
  prototype task waits on it.
- Every pull request gets a reviewer the day it opens, as agreed in Sprint 1.
  PR #79 waited nine days and PR #72 twelve.
- Sprint 2 work that carried over moved to the Sprint 3 milestone on Nov 5,
  so the Sprint 3 report counts it.

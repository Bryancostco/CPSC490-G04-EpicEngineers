# Sprint 2 review — Oct 13 – Oct 26

> Group 04 Epic Engineers · SNX-1 · Sprint 2 review Tue Oct 27 · Task: #53

**Draft, Oct 24.** Velocity, the completed table and the contribution
snapshot are filled in after the sprint ends on Oct 26. Everything else
below is already true.

## Progress this sprint — the substance

**Proposal moved** (pull requests open as of Oct 24; any not merged by Oct 26 move to Carried over):
| Section | What changed | Where |
|---|---|---|
| §4 Planned activities | Every Sprint 2 task (#49 to #63, #65) cited as a typed reference, with its owner | PR #66 (task #65) |
| §4 Specification and design documents | First entries: the PNL calculation spec and the data flow design | PR #67 (task #55), PR #68 (task #58) |
| §8 References | Template references replaced with sources [1] to [7], each with URL and access date | PR #69 (task #51) |
| Specification | `docs/specs/pnl-calculation.md`: positions, FIFO cost basis, open and closed status, realized and unrealized PNL, worked example | PR #67 (task #55) |
| Design | `docs/design/data-flow.md`: Level 0 and Level 1 DFDs numbered to the spec | PR #68 (task #58) |
| Project context | `docs/project-context.md`: mentor decisions with sources, glossary, research by member, linked from `CLAUDE.md` | PR #70 (task #63) |
| Development plan | Charter, QA owners, AI rules and risk register filled in | PR #71 (task #50) |
| Issue board | Sprint 2 tasks assigned, Sprint 3 and Sprint 4 milestones set on #26 to #28, #30 to #32 and #35 to #38 | Issues |

**Prototype moved:** Filled in after Oct 26 from #62.

## Velocity

Filled in on Oct 26 from `python scripts/sprint_report.py --sprint 2`.

## Completed (merged PRs)

Filled in on Oct 26 from the pull requests merged into `develop` during the
sprint.

## Carried over — and why

Known so far; final reasons are added on Oct 26.

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #52 Record the chosen prototype stack | @Bryancostco | The stack is a team decision; options were posted on #52 on Oct 24 | Decide at a team meeting, then record it in `CLAUDE.md` and §4 |
| #60 Page flow diagram | @leiladb | Blocked until Erel approves the dashboard question list (#34) | Carry over if approval has not arrived by Oct 26 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | Filled in on Oct 26 |
| Harness rules added (rows in the harness log) | 0 |

## Prototype increment

Filled in after Oct 26 from #62.

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

Filled in on Oct 26 from the repository, as in Sprint 1.

## What we change next sprint

Filled in at the Sprint 2 review on Oct 27.

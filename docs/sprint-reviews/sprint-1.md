# Sprint 1 review — Sep 29 – Oct 12

> Group 04 Epic Engineers · SNX-1 · Sprint 1 review Tue Oct 13 · Task: #42

## Progress this sprint — the substance

**Proposal moved:**
| Section | What changed | Where |
|---|---|---|
| Cover fields, §0 Abstract, §1 Introduction | Replaced the template with our project background on Polymarket, Polygon, and SonarX's data | PR #21 (task #11) |
| §1.1 Related Work | Comparison table of four existing tools: Polymarket Analytics, Predicts.guru, Polycopy, and Polytrackhq.app | PR #21 (research #12, #13) |
| §1 Introduction (revised) | Rewrote the introduction to match our HW#5 version | PR #45 |
| §1.2 Problem Statements | P1 to P4 written, each mapped to the goal that addresses it | PR #21, PR #43, PR #45 |
| §2 Goals and Objectives | 3 goals and 12 objectives from our HW#5, each cited as a typed reference to its epic or story | PR #43, PR #45 (task #41) |
| §4 Environment and planned activities | Snowflake recorded as our data source, and every other work item listed as a typed reference | PR #43 (task #41) |
| Issue board | 3 epics (#24, #29, #33) and 12 user stories (#25 to #28, #30 to #32, #34 to #38), one per goal and objective | Issues |
| README.md and CLAUDE.md | Replaced the template and Sentinel details with the SNX-1 project | PR #6, PR #16, released to main in PR #19 |

**Prototype moved:** It did not move this sprint. `prototype/` still holds the course's login example. Sprint 1 was spent on the proposal, the kickoff with SonarX, and turning our goals into issues. The first prototype work comes from Objective 1.1 (#25), querying SonarX's Polygon data in Snowflake, once we have data access.

## Velocity

From `python scripts/sprint_report.py --sprint 1` (run Oct 12, end of sprint):

| | Story points | Stories |
|---|---|---|
| Planned | 10 | 9 |
| Completed | 9 | 8 |

All 10 points show as "added mid" sprint in the report because the Sprint 1 milestone was put on the issues after the sprint started, not at the start.

## Completed (merged PRs)

| Story | Owner | Points | PR |
|---|---|---|---|
| #1 Replace course setup guide README with team README template | @justincox8 | 1 | PR #6 |
| #3 Fill in team README.md and CLAUDE.md | @justincox8 | 1 | PR #6 |
| #10 README and CLAUDE.md | @Bryancostco | 1 | PR #16 |
| #11 Fill proposal cover page and draft §1 Introduction | @leiladb | 3 | PR #21 |
| #12 Research: how prediction markets and Polymarket work | @kyquach | under #11 | findings on the issue, used in PR #21 |
| #13 Research: existing Polymarket PNL and leaderboard tools | @justincox8 | under #11 | findings on the issue, used in PR #21 |
| #20 SNX-1 kickoff meeting notes (Oct 6) | team | 1 | notes on the issue |
| #41 Write §2 and §4 into proposal.md | @Bryancostco | 2 | PR #43, PR #45 |

#11 was closed on Oct 5, but its PR #21 was merged on Oct 12. From now on, an issue closes when its PR merges.

## Carried over — and why

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #42 Write the Sprint 1 review | @Bryancostco | This file was merged into develop on Oct 12, but the issue closes only when it reaches main | Closes with the release pull request into main before the review on Oct 13 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | not tracked in Sprint 1 |
| Harness rules added (rows in the harness log) | 0 |

Our requirements are still being found during writing, not during implementation, since there is no implementation yet. Objective 3.1 (#34) is there so the dashboard questions are agreed on before any interface work starts.

## Prototype increment

None this sprint. See "Prototype moved" above.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Snowflake is the main warehouse we will use for queries (SonarX kickoff, #20) | Recorded as our data source in §4 and in Objective 1.1 | PR #43, #25 |
| Phase 1 traces PNL per proxy wallet on historical data; Phase 2 links proxy wallets to EOA wallets with real time data (SonarX kickoff, #20) | §2 goals cover Phase 1, and Phase 2 is stated as future work | PR #43 |
| The dashboard is client facing; decide what questions it answers before designing the UI, and keep it fast (SonarX kickoff, #20) | Objective 3.1 (questions approved by our mentor first) and Objective 3.4 (pages load in under 3 seconds) | #34, #37 |
| Questions we still owe SonarX: which client questions, our plan for keeping the dashboard fast, our architecture (SonarX kickoff, #20) | Not answered yet; tracked by the objectives that will answer them | #34, #37, §4 |
| Merge the instructor's Word export PR and update course files (repo readiness card, Oct 11) | Ran the course update script; PR #23 had been closed without merging | PR #40 |
| Merge PR #21 (repo readiness card) | Merged into develop | PR #21 |
| Write §2 and §4 into proposal.md, cite every issue (repo readiness card) | Done with typed references | PR #43 |
| Create one epic per goal and one story per objective in the objective's exact words (repo readiness card) | Filed and titled with our §2 wording | #24 to #38 |
| Give #1, #3, #12, #13, #20 their own `sp:` (repo readiness card) | #1, #3, #20 pointed. #12 and #13 left unpointed, because they are sub-issues of #11, which already carries their points, and the sprint report counts them twice otherwise | Issues |
| Replace PR template text and add `Closes #N` (repo readiness card) | PR #39 description filled in | PR #39 |
| Every change goes through a pull request into `develop` (repo readiness page, rule 5) | PR #45 went straight into `main`, so `main` and `develop` drifted apart. We merged `main` back into `develop` and removed the duplicate §4 it added. Only release pull requests go into `main` from now on | PR #45, this PR |

## Contribution snapshot

| Member | Meetings attended | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @Bryancostco | 1 | 7 (#9, #16, #19, #39, #40, #43, #44) | 2 | 6 |
| @justincox8 | 1 | 2 (#6, #45) | 3 | 2 |
| @leiladb | 1 | 1 (#21) | 1 | 5 |
| @kyquach | 0 | 0 | 1 | 1 |

Merged PRs, issues closed, and reviews count Sprint 1 only (Sep 29 to Oct 12) and come from the repository. Meetings attended is for the team to fill in.

Our working agreement asks for at least 2 merged contributions per member per sprint. In Sprint 1, two members reached it and two did not. The team should talk about this at the review and say here what we will do about it.

## What we change next sprint

- Every story committed to Sprint 2 gets one assignee, `sp:`, a `priority:` label, and the Sprint 2 milestone at the Sprint 1 review, not later.
- Every pull request gets a reviewer the day it opens, and is merged or closed within two days.
- Issues close through the PR that finishes them (`Closes #N`), not by hand.
- Feature branches merge into `develop` only; `main` gets changes through a release pull request from `develop`.

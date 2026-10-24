# Development plan — Group 04 Epic Engineers

> Group 04 Epic Engineers · SNX-1 · Task: #50

> Due with the proposal. Revisit it at **every sprint review** and change what
> is not working — a plan nobody revises is a plan nobody uses.

## 1. Team charter

### External goals

Beyond the grade, we want two things. First, a dashboard SonarX can put in
front of its clients, which also makes SonarX a reference we can name.
Second, a portfolio project every member can explain end to end in an
interview: the data pipeline, the PNL accounting, and the dashboard. When
time runs short, we protect a correct and validated PNL calculation (Goal 1)
over dashboard polish, because a fast dashboard with wrong numbers is worth
nothing to either goal.

### Attendance

| | Our rule |
|---|---|
| Expected meetings | The sprint meeting in class every other Tuesday (Section 01), plus one team meeting per sprint that the leader schedules in the group chat |
| Acceptable excuse | Illness, a work shift, a class conflict or family, told in the group chat before the meeting starts |
| Unacceptable | A silent no show, or telling the team after the meeting |
| In an emergency | Tell Bryan Orozco (leader) as soon as possible; push any work in progress to its branch and say in the issue what is left, so a teammate can pick it up |

### Accountability — with numbers

**Write a quantified trigger and a real consequence for each row.** A vague
charter ("we will all do our share") is useless at the moment you need it.
The point of numbers is that nobody has to muster the courage to accuse a
teammate — they point at the rule everyone already agreed to.

| Concern | Trigger (measurable) | Consequence |
|---|---|---|
| Missing meetings | Misses 2 team or sprint meetings in one sprint without an acceptable excuse | First time: takes the next sprint review write up. Second time in the semester: the team raises it with the instructor at the sprint meeting |
| Not contributing code/docs | Fewer than 2 merged pull requests in a sprint (our working agreement in §2) | Named in the sprint review's contribution snapshot with a plan for the next sprint; two sprints in a row means a meeting with the instructor |
| Work quality | A pull request reopened or sent back twice for the same missed acceptance criterion | Pairs with a teammate on their next story |
| Not reviewing | Reviews no pull request in a sprint | Takes the next sprint's QA / harness owner role in §1, or the first review of every PR for one week |
| Going dark | No reply in the group chat for 3 days during a sprint | The leader calls or texts; after 5 days, the instructor is told |

### Quality assurance

The QA / harness owner rotates by sprint. Each sprint they make sure the
harness (`python .github/scripts/check_repo.py`) is green, the board matches
reality, and the sprint review is written and merged. See the "harness
owner" idea in `docs/aidlc/loop-engineering.md` §8.

| Sprint | QA / harness owner |
|---|---|
| 1 | Bryan Orozco |
| 2 | Bryan Orozco |
| 3 | Justin Cox |
| 4 | Kyle Quach |

Leila De Belen takes the role if a sprint's owner is out, and the rotation
continues in CPSC 491 starting with her.

### Decision making

We try for consensus first. If the team still disagrees after everyone has
been heard, we vote and the majority decides; on a tie, the leader decides.
A decision that blocks someone's work may stay open for at most 48 hours,
after which the leader calls it and records it in the related issue.
Anything that touches SonarX or a course deliverable is checked with Erel or
the instructor before it is final.

## 2. Workflow

- Branching, PRs, review and CI: [`git-workflow.md`](git-workflow.md).
- Issues, labels, sprints and the board: setup guide §4.
- **Working agreements we set for ourselves** (recommended defaults, not
  course requirements — see setup guide §8): every member
  makes at least **2 merged contributions per sprint**; pull requests stay
  under **10 files / 500 lines** except by agreement; and we treat
  **unmerged work as unfinished** — if it is not merged by the sprint
  boundary it carries over.

## 3. Use of AI and LLMs

We use assistants to draft specification and design documents, diagrams,
prototype code and tests, pull request descriptions, and review comments.
The proposal's prose is our own writing, as the course template requires;
an assistant may suggest structure or check it, but does not write it.
`CLAUDE.md` and `docs/project-context.md` give every teammate's assistant the
same starting facts.

The course rules are in [`aidlc/hitl-gates.md`](aidlc/hitl-gates.md); the
prompts are in [`aidlc/prompt-library.md`](aidlc/prompt-library.md). Every
deliverable carries a disclosure, and every PR says what was verified.

Our own additions:

- Nobody merges generated work they cannot explain at the sprint meeting.
- The reviewer of an AI assisted pull request spot checks at least two facts
  or numbers against their source, and names them in the review.
- No Snowflake credentials, and no SonarX data beyond what SonarX has made
  public, go into a prompt or into the repository.
- A source an assistant suggests is cited only after a teammate has opened
  it and read the part being cited.

## 4. Risk register

Review and update at every sprint boundary. Likelihood and impact: H / M / L.

| # | Risk | L | I | Early warning sign | What we will do about it | Owner |
|---|---|---|---|---|---|---|
| R1 | Snowflake access arrives late | M | H | No Snowflake credentials by the end of Sprint 2 (Oct 26) | Build and test the prototype against a small made up dataset shaped like the worked example in `docs/specs/pnl-calculation.md`; ask Sergio in the SonarX Slack channel | Bryan Orozco |
| R2 | The prototype stack is still undecided | M | H | #52 still open on Oct 25, blocking #56, #61 and #62 | Decide it at a short team meeting, with the leader calling it after 48 hours per §1 | Bryan Orozco |
| R3 | SonarX's tables record share changes we have no rule for (splits, merges, redemptions, transfers) | M | M | The schema documents show event types beyond buys and sells | Add a requirement for each one to `docs/specs/pnl-calculation.md` before #26 is built (open question Q4 there) | Justin Cox |
| R4 | Our PNL does not match the Polymarket leaderboard | M | M | The first comparison in #28 differs beyond the tolerance agreed with Erel | Check which leaderboard window counts realized profit only, trace the gap to the trades behind it, and record it in #28 | Justin Cox |
| R5 | Contribution stays uneven | M | M | A member has fewer than 2 merged pull requests by the middle of a sprint (two of four members missed this in Sprint 1) | Apply the accountability rows in §1 and rebalance issues at the next team meeting | Bryan Orozco |
| R6 | A member drops the course | L | H | Missed meetings, per the charter triggers | Re-scope to the objectives and tell the instructor early | Bryan Orozco |

When a risk's early warning sign has already appeared, it is a problem, not a
risk: we move it to an issue.

## 5. Technology and environment

| Need | Choice | Owner |
|---|---|---|
| Data warehouse | SonarX's Snowflake, credentials through the SonarX Slack | Bryan Orozco |
| Code, issues, board and CI | This GitHub repository and its project board | Bryan Orozco |
| Diagrams | Mermaid, with sources in `docs/design/diagrams/` | Bryan Orozco |
| Proposal export to Word | pandoc with `proposal/reference.docx` | Leila De Belen |
| Languages, frameworks and services for the prototype | Not chosen yet; decided in #52 and recorded in proposal §4 and `CLAUDE.md` | Bryan Orozco |

# Sprint 3 plan: who does what, in what order

> Group 04 Epic Engineers · SNX-1 · Sprint 3 (Oct 27 to Nov 9) · Task: #82

Every user story is now broken into features and tasks as sub issues
(story → feature → task). Each task says what it is, what to read first,
the requirements it implements (quoted from the spec), when it is done, what
it waits on, and the exact branch name to use. Open your tasks from the
[board](https://github.com/users/Bryancostco/projects/1) (Current Sprint
view, filter by your name).

## Sprint 3 goal

Kyoung's Sprint 3 guidance asks for two things by the review:

1. **Proposal §4 wrapped up.** One specification per epic, a design document
   with six parts for each design (system context, components, data model,
   data flow, key decisions with rejected alternatives, what is not designed
   yet), and prose around every diagram.
2. **A prototype slice to demo.** The slice our design depends on most, with
   a test for each acceptance criterion. For us that is trades → positions →
   realized and unrealized PNL, run on fixture data.

## First, as a team (blocks most of the code)

- **#52 Pick the prototype stack.** Nothing under `prototype/` can be written
  until the language and framework are chosen. Decide it at the next standup
  and record it.
- **Review the open PRs:** #135 (repo fixes), #81 (architecture revision,
  retarget to `develop`), #79 (dashboard flow), #73 (dashboard questions),
  #72 (Sprint 2 review). Each needs one approval from someone who is not
  the author.

## By person, in order

**Kyle Quach**
1. #62 project skeleton (the part that does not need Snowflake first)
2. #108 position grouping and lots, then #109 open or closed status
3. #116 and #117 rankings, once #111 is done
4. #106 expand `architecture.md` to six sections; #80 diagram revision (PR #81)

**Justin Cox**
1. #57 data model and #59 PNL run sequence diagram
2. #110 FIFO and realized PNL (after #108), then #111 unrealized PNL and totals
3. #118 and #119 behavior metrics
4. #103 and #104 data source spec, as soon as SonarX sends the schema docs

**Leila De Belen**
1. #123 get PR #73 merged (change its body to `Closes #123`)
2. #60 dashboard page flow (PR #79)
3. #125 dashboard specification, after #124 (Erel's approval)

**Bryan Orozco**
1. Chase SonarX for Snowflake credentials and schema docs (blocks #62's
   live connection, #103, #104, #105)
2. #107 and #115 open questions for Erel and Sergio; #124 question list approval
3. #53 finish the Sprint 2 review (PR #72)
4. #112 prototype README and proposal §5; #120 hand check of the metrics

## Waiting on SonarX

Snowflake credentials and the Polymarket schema docs. Everything in the code
slice above runs on fixtures, so it does not have to wait; only the live
queries do.

## How a card moves

Assign yourself → **In Progress** when you branch (`<issue>-<slug>`, given
in each task) → open a PR into `develop` that starts with `Closes #<issue>`,
which moves the card to **In Review** → merge, which closes the issue and
moves the card to **Done**. Nobody drags cards to Done by hand.

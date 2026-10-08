# Project Proposal — Polygon Prediction Market PNL and Trader Profitability Analytics

Department of Computer Science
CPSC 490 Undergraduate Seminar in Computer Science — Proposal for Capstone Project

**Group 04** — Epic Engineers · **Sponsor** — SonarX  
**Authors:** Orozco, Bryan (Bryancostco); Cox, Justin (github-username); De Belen, Leila (leiladb); Quach, Kyle (github-username);  
**Proposal Date:** 2026-11-29  

## 0. Abstract  
Polymarket generates large amounts of on-chain trading activity based on real-world events. However, Polymarket’s raw blockchain data is not able to account for profits and losses. In this project, we will use SonarX’s Polygon blockchain data to build a profit and loss (PNL) accounting tool for Polymarket. We will parse on-chain trades, match positions to resolutions, and compute the realized and unrealized PNL for each wallet. We will then rank the top traders and see what drives their edge. The final deliverable will be a working dashboard that showcases these top traders and trading patterns. The sections below will cover the problems, our goals to fix them, the outcome of our project, and our timeline. This project is significant because by doing this we are addressing the issue of raw data not being able to represent profits and losses, as well as discovering the drive behind successful traders. 	

## 1. Introduction  
Our project will be a tool used for Polymarket. Polymarket is a real-world events-based prediction market platform where users trade the outcomes of events [1]. This market is not structured as typical gambling because instead of betting against a house, a user will trade contracts with other users, which determines if they profit off of their contracts [1]. The system of Polymarket works off “Yes”, if they think this event will happen, and “No”, if they think it will not [1]. Users profit a dollar for every correct bid minus how much they already paid for the contract, though they lose the money they paid if incorrect [1]. For example if a user thinks an event will happen, they will put in a buy for $0.70. Another user will then sell them the “Yes” for $0.70 for certain reasons, one potentially being because they do not think it will happen. If the first user is correct, they gain $0.30, but lose $0.70 if the event does not happen.  

Our project is using SonarX's Polygon blockchain data to build a profit and loss accounting tool for Polymarket. Polygon is “a global network of aggregated blockchains” [2]. Polygon is a network that Polymarket is built upon because anyone with internet can participate, users can control their own funds, all activity done is publicly verifiable onchain, and it enables quick, low-cost transactions [3]. 

One problem we encounter when building this project is Polymarket’s blockchain data displays a trader’s wallet transactions, but it does not explain how there is profit and loss. The second problem is that our competitors show who is profiting the most, but not the drive behind traders. The importance of solving these problems is that we are able to understand how there is profit and loss, which is better for understanding the ranking of traders. It is also important that we are able to learn what drives traders, as that is the key to discovering their success. Our proposal is different than existing projects because we will be focusing on an industrial standpoint of the Polymarket. 

### 1.1 Related Work
| Existing approach | What it does | Pros | Cons | Why ours differs |
|---|---|---|---|---|
| Polymarket Analytics  |“Real-time analytics for Polymarket prediction markets. Track whale wallets and insider-sized trades, follow the traders with the best P&L, pull historical price data on any market, and see open interest and volume across every event” [4].  | Has a whale tracker that allows people to see large trades, and allows them to understand its positioning, and detects unusual activity [4]. People can look up other user’s positions and their own portfolio [4]. Market data is updated regularly [4].  | “The data is pulled from third-party APIs and blockchain sources”, meaning data can be delayed or not completely accurate. Tracking the whale wallets does not guarantee users land a successful trade as well [4].   | *Will discover after meeting with mentor  |
| Predicts.guru  | “Predicts.guru provides free wallet analytics based on public Polymarket trading data. Review profit and loss, win rate, markets traded, and open positions” [5]. | Users can use website for free with no sign-up needed [5]. Users can compare wallets side-by-side for easier access [5].  | “Only public Polymarket activity is covered. A trader using several addresses appears as separate wallets, transfers between addresses are not linked, and trading on other venues is out of scope” [5].  | *Will discover after meeting with mentor  |
| Polycopy   | “Mirror traders and strategies on the best copy trading platform for Polymarket” [6].  | No experience is needed, which is useful for first time users of Polymarket [6]. Has bots to make it easier to copy traders, and strategies [6]. Also has paper bots to stimulate trade [6].  | If the bot is mirroring a trader that is losing money, the user will also lose money [6]. | *Will discover after meeting with mentor  |
| Polytrackhq.app  | “The #1 Polymarket whale tracker. Follow smart money traders with proven 60%+ win rates. Real-time wallet tracking, P&L analytics, and instant alerts when whales make moves” [7]. | Allows for whale tracking and the ability to mirror traders on the same platform [7]. Users are able to monitor the market  in real time [7]. | Mirroring successful traders does not guarantee users make a profit [7]. Users are dependent on trades of other Polymarket users [7].  | *Will discover after meeting with mentor  |

While there are many competitors, and some recognized in the table above, our project wants to use a more industrial take on Polymarket, rather than only a bot-trading tool. The first two projects in the table analyze the wallets of top traders, while the other competitors focus on users using bot trading. When reviewing the table, it is clear that our project will be achieving the same goal of those that already exist, which is wallet lookup. But, with the websites that are already made, and the raw data from Polymarket, their data will help our PNL tool compute and explain the wallets that already exist to allow users to understand the wallets being traded, the profits and losses that are open and closed, and what drives the successful traders. As projects cited as [4] and [7] in the table above demonstrate, there is a common theme present within their advantages which is they review whale trading, to which our tool would be built to excel in documenting. When reviewing the table of the cons of projects cited [6] and [7], we see that users depend on bots and mirroring. Our project would be used to help users read the raw trade data easily with our dashboard, allowing users to understand the current state of the wallets and how profits and losses happen to traders in Polymarket. 

### 1.2 Problem Statements
| Existing approach | What it does |
|---|---|
| P1 - Polymarket’s blockchain data displays a trader’s wallet transactions, but it does not explain how there is profit and loss. | *goal will be put here later  |
| P2 - Our competitors show who is profiting the most, but not the drive behind traders.  | *goal will be put here later  |

## 2. Goals and Objectives

> Describe goals and objectives. Goals are general statements of what you are
> trying to accomplish with the project or problems to solve. Objectives are
> specific, measurable statements of what you want to complete to reach the
> project goals. Most projects have 2-3 goals.
>
> List the objectives for each goal. To write objectives, look at the goal
> statement and list what you need to complete using action words like use
> case names in order to meet the goal.
>
> Note that the goals and objectives in a proposal will be an important
> metric to evaluate whether or not you successfully finished your project
> when you turn in your final project report.

Each **goal** is tracked as an **Epic** issue and each **objective** as a
**User Story** issue in the team repository (see the setup guide's *Epics and user stories* section).
**Every epic and user story in the repository is linked from this section** —
CI gate G8 fails if one exists that this section does not link. That is what
keeps the goals in this document and the work on the board from drifting
apart.

Write each objective the way the guidance above asks — **an action word plus
the measure that says it is done**, not a role-play sentence:

- **Goal 1: 〈e.g. Secure account management〉** (Epic #〈n〉)
  - Objective 1.1: 〈Implement member registration and login with hashed
    credentials, session expiry, and rejection of malformed input.〉 (#〈n〉)
  - Objective 1.2: 〈Demonstrate the login round-trip in a runnable prototype
    at the Week-8 in-class check.〉 (#〈n〉)
- **Goal 2: 〈your second goal〉** (Epic #〈n〉)
  - Objective 2.1: 〈Action word + what you will complete + how it will be
    measured〉 (#〈n〉)

〈Replace the brackets with your own 2–3 goals and their objectives, and put
the **real issue numbers** in as you file them — gate G8 checks that every
epic and story in your repository is linked from this section. A fully worked
version of this, with live issues and a populated board, is in the course
example repository.〉

## 3. Proposed Approaches

> Describe your proposed approach to solve the problem, specifying how you
> will achieve the stated goals. List some possible strategies.

〈Your approach — **clear and concise**. State the strategy you chose, the
alternatives you considered, and the reasoning that decided between them.
Think of this as the argument, not the manual: a reader should finish this
section understanding *what* you will do and *why that* rather than the
alternatives.〉

**Keep the details out of this section.** Tooling, platforms, frameworks,
DBMS choices, environment setup, diagrams, and the work breakdown all belong
in §4 (Required Environment, Resources, and Planned Activities). If a
sentence here names a version number, a library, or a configuration, it
probably belongs in §4 — leave a pointer instead ("the implementation stack
is detailed in §4").

〈A few paragraphs, or a short list of candidate strategies with one line of
trade-off each. If it runs past a page, you are writing §4.〉

## 4. Required Environment, Resources, and Planned Activities

> Review the required and available resources and environment to complete
> your project. For example, server, platform, software tools, operating
> systems, DBMS, or any required skills.
>
> Describe the expected activities to achieve the stated goals, e.g.,
> software development process.

〈Your environment, resources, and planned activities.〉

**Diagrams belong in this section.** Include at minimum a high-level
architecture diagram and a system (context) diagram; add the ER/EER model and
a data-flow diagram where they help the reader understand what you are
building and what it depends on. Draw them with any graphical tool
(Lucidchart, draw.io, Miro, Mermaid, ERDPlus, Figma), keep the authoritative
copies in `docs/design/` with both editable source and exported image, and
reference them here.

〈Number every figure, caption it, and point at it from the prose — "Figure 1
shows the three deployment tiers and the trust boundary between them." A
figure the text never mentions is decoration. See `docs/design/DIAGRAMS.md`
for tools, conventions, and the rule that every box and arrow must be
verified against reality.〉

### Specification and design documents

**Every specification and design document the team writes is listed here**
with the objective it serves. This section is the index of the project's
technical detail: §3 holds the argument, §4 holds the documents that make it
buildable. CI gate G9 fails if a document exists in `docs/specs/` or
`docs/design/` that this section does not link.

| Document | Kind | Covers | Issues |
|---|---|---|---|
| 〈docs/specs/account-management.md〉 | specification | 〈account management requirements〉 | 〈#n, #n〉 |
| 〈docs/design/architecture.md〉 | design | 〈system architecture + data model〉 | 〈#n〉 |

〈The scaffold ships `docs/specs/example-spec.md` and
`docs/design/example-design.md` as worked examples — read them, then delete
them once you have your own, and list yours here.〉

〈Replace these rows with your own. Each document names its epic and stories
in its own first lines too (gate G2), so the trail runs both ways.〉

### Planned activities — the work items

The goals and objectives live in §2 as epics and user stories. **This section
links every *other* work item: features, enhancements, bugs, tasks, and
sub-tasks** — the concrete activities that deliver those objectives. CI gate
G8 fails if such an issue exists that this section does not link.

| Issue | Type | Activity | Parent | Owner | Sprint |
|---|---|---|---|---|---|
| 〈#n〉 | 〈task〉 | 〈stand up the prototype login endpoint〉 | 〈#story〉 | 〈owner〉 | 〈Sprint 1〉 |
| 〈#n〉 | 〈feature/enhancement/bug/task/sub-task〉 | 〈…〉 | 〈#story〉 | 〈…〉 | 〈…〉 |

〈Replace these rows with your own, and keep the table current as you file new
issues — with §2 it gives a reader every planned activity in one place, each
traceable to the objective it serves.〉

## 5. Project Outcomes

> Describe the outcomes or deliverables, e.g., final project report, user
> manuals, source code, data or database files, etc.
>
> Note: the deliverables always include the team GitHub repository, which
> must already contain prototype v0 (a thin end-to-end proof-of-concept,
> however small, running when this proposal is submitted). Briefly describe
> what your v0 demonstrates and how to run it.

〈**One or two paragraphs** explaining the project outcome overall — what will
exist when the project is finished, and what it will let someone do. Keep it
prose, not a checklist; name the deliverables inside the paragraphs, and say
briefly what prototype v0 demonstrates today and how to run it.〉

## 6. Project Timeline

> Identifies tasks (project objectives) to be performed, milestones to be
> met, and the estimated number of hours for each task.

〈**This is the plan for CPSC 491 next semester — the implementation timeline,
not this semester's proposal work.** Identify the tasks (your objectives from
§2), the milestones, and the estimated hours for each, in the order they will
be built. State the assumptions it rests on (sponsor availability, data
access, hardware).〉

| Task (objective) | Milestone | Owner | Est. hours | Spring phase |
|---|---|---|---|---|
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |

〈Do **not** put this fall's four proposal sprints here — those live on the
project board and in `docs/sprint-reviews/`. This section answers "how does
the system actually get built next semester?"〉

## 7. AI Usage

> Per the course AI policy (see the syllabus, Use of AI Tools), disclose the
> AI tools used in preparing this proposal and the prototype: which tools,
> for what tasks (e.g., code generation, test writing, debugging,
> diagramming), and approximately what fraction of each artifact was
> AI-assisted.
>
> Reminder: the prose of this proposal must be your own writing. You remain
> fully responsible for the correctness of all AI-assisted work, including
> the prototype code.

〈Your disclosure. Naming the tool is not disclosure — name what it drafted,
what fraction of each artifact was AI-assisted, and how you verified it.〉

## 8. References

> [1] Burges, C. J. C. Tutorial on Support Vector Machines for Pattern
> Recognition. Kluwer Academic Publishers, 1998.
> [2] Chen, P., Fan, R., and Lin, C. A study on SMO-type decomposition
> methods for support vector machines. IEEE Transactions on Neural Networks,
> 2006.
> [3] For Wikipedia, specify the URL here
> [4] For a web source, specify the URL here plus date accessed

〈Number references in the order first cited and cite them in the text as
[1], [2]. Every entry must be a source a team member has actually read and
can produce on request.〉

# Project Proposal — Polygon Prediction Market PNL and Trader Profitability Analytics

Department of Computer Science
CPSC 490 Undergraduate Seminar in Computer Science — Proposal for Capstone Project

**Group 04** — Epic Engineers · **Sponsor** — SonarX  
**Authors:** Orozco, Bryan (Bryancostco); Cox, Justin (justincox8); De Belen, Leila (leiladb); Quach, Kyle (kyquach);  
**Proposal Date:** 2026-11-29  

## 0. Abstract  
Polymarket generates large amounts of on-chain trading activity based on real-world events. However, Polymarket’s raw blockchain data is not able to account for profits and losses. In this project, we will use SonarX’s Polygon blockchain data to build a profit and loss (PNL) accounting tool for Polymarket. We will parse on-chain trades, match positions to resolutions, and compute the realized and unrealized PNL for each wallet. We will then rank the top traders and see what drives their edge. The final deliverable will be a working dashboard that showcases these top traders and trading patterns. The sections below will cover the problems, our goals to fix them, the outcome of our project, and our timeline. This project is significant because by doing this we are addressing the issue of raw data not being able to represent profits and losses, as well as discovering the drive behind successful traders. 	

## 1. Introduction  
Polymarket is a real-world events-based prediction market platform where users trade the outcomes of events [1]. This market is not structured as typical gambling because instead of betting against a house, a user will trade contracts with other users, which determines if they profit off of their contracts [1]. The system of Polymarket works off “Yes”, if they think this event will happen, and “No”, if they think it will not [1]. Users profit a dollar for every correct bid minus how much they already paid for the contract, though they lose the money they paid if incorrect [1]. For example if a user thinks an event will happen, they will put in a buy for $0.70. Another user will then sell them the “Yes” for $0.70 for certain reasons, one potentially being because they do not think it will happen. If the first user is correct, they gain $0.30, but lose $0.70 if the event does not happen. Polygon is “a global network of aggregated blockchains” [2]. Polygon is a network that Polymarket is built upon because anyone with internet can participate, users can control their own funds, all activity done is publicly verifiable onchain, and it enables quick, low-cost transactions [3]. Our project will use SonarX's Polygon blockchain data to build a profit and loss accounting tool for Polymarket. We will be creating a dashboard tool that identifies the top traders, and what drives their edge. 

While there are many competitors, our project wants to use a more industrial take on Polymarket, rather than only a bot-trading tool. The projects Polymarket Analytics and Predicts.guru analyze the wallets of top traders [4][5]. When reviewing their sites, it is clear that our project will be achieving the same goal as those that already exist, which is wallet lookup. But, with the websites that are already made, and the raw data from Polymarket, their data will help our PNL tool compute and explain the wallets that already exist to allow users to understand the wallets being traded, the profits and losses that are open and closed, and what drives the successful traders. Our project would be used to help users read the raw trade data easily with our dashboard, allowing users to understand the current state of the wallets and how profits and losses happen to traders in Polymarket. 

One problem we encounter when building this project is that Polymarket’s blockchain data displays a trader’s wallet transactions, but it does not explain how there is profit and loss. The second problem is that our competitors show who is profiting the most, but not the drive behind traders. The importance of solving these problems is that we are able to understand how there is profit and loss, which is better for understanding the ranking of traders. It is also important that we are able to learn what drives traders, as that is the key to discovering their success. Our proposal is different than existing projects because we will be focusing on an industrial standpoint of the Polymarket. Alongside these problems with the data and existing tools we also aim to solve two business problems for SonarX. We want to afford SonarX the ability to visualize Polymarket trader PNL for potential clients. The importance of solving this problem is that not all clients may be technical, so visualizing the data makes it easier for the company to work with potential clients. The final problem we want to address is that competitors of SonarX are creating and institutionalizing similar dashboards, and with the rise of institutional needs for prediction market analytics, it is imperative that SonarX stays competitive. 



### 1.1 Related Work
| Existing approach | What it does | Pros | Cons | Why ours differs |
|---|---|---|---|---|
| Polymarket Analytics  |“Real-time analytics for Polymarket prediction markets. Track whale wallets and insider-sized trades, follow the traders with the best P&L, pull historical price data on any market, and see open interest and volume across every event” [4].  | Has a whale tracker that allows people to see large trades, and allows them to understand its positioning, and detects unusual activity [4]. People can look up other user’s positions and their own portfolio [4]. Market data is updated regularly [4].  | “The data is pulled from third-party APIs and blockchain sources”, meaning data can be delayed or not completely accurate. Tracking the whale wallets does not guarantee users land a successful trade as well [4].   | *Will discover after meeting with mentor  |
| Predicts.guru  | “Predicts.guru provides free wallet analytics based on public Polymarket trading data. Review profit and loss, win rate, markets traded, and open positions” [5]. | Users can use website for free with no sign-up needed [5]. Users can compare wallets side-by-side for easier access [5].  | “Only public Polymarket activity is covered. A trader using several addresses appears as separate wallets, transfers between addresses are not linked, and trading on other venues is out of scope” [5].  | *Will discover after meeting with mentor  |
| Polycopy   | “Mirror traders and strategies on the best copy trading platform for Polymarket” [6].  | No experience is needed, which is useful for first time users of Polymarket [6]. Has bots to make it easier to copy traders, and strategies [6]. Also has paper bots to simulate trade [6].  | If the bot is mirroring a trader that is losing money, the user will also lose money [6]. | *Will discover after meeting with mentor  |
| Polytrackhq.app  | “The #1 Polymarket whale tracker. Follow smart money traders with proven 60%+ win rates. Real-time wallet tracking, P&L analytics, and instant alerts when whales make moves” [7]. | Allows for whale tracking and the ability to mirror traders on the same platform [7]. Users are able to monitor the market  in real time [7]. | Mirroring successful traders does not guarantee users make a profit [7]. Users are dependent on trades of other Polymarket users [7].  | *Will discover after meeting with mentor  |

While there are many competitors, and some recognized in the table above, our project wants to use a more industrial take on Polymarket, rather than only a bot-trading tool. The first two projects in the table analyze the wallets of top traders, while the other competitors focus on users using bot trading. When reviewing the table, it is clear that our project will be achieving the same goal of those that already exist, which is wallet lookup. But, with the websites that are already made, and the raw data from Polymarket, their data will help our PNL tool compute and explain the wallets that already exist to allow users to understand the wallets being traded, the profits and losses that are open and closed, and what drives the successful traders. As projects cited as [4] and [7] in the table above demonstrate, there is a common theme present within their advantages which is they review whale trading, to which our tool would be built to excel in documenting. When reviewing the table of the cons of projects cited [6] and [7], we see that users depend on bots and mirroring. Our project would be used to help users read the raw trade data easily with our dashboard, allowing users to understand the current state of the wallets and how profits and losses happen to traders in Polymarket. 

### 1.2 Problem Statements
| Problem | Addressed by |
|---|---|
| P1 - Polymarket’s blockchain data displays a trader’s wallet transactions, but it does not explain how there is profit and loss. | Goal 1 |
| P2 - Our competitors show who is profiting the most, but not the drive behind traders.  | Goal 2 |
| P3 - SonarX needs to visualize trader PNL for potential clients. | Goal 3 |
| P4 - Competitors of SonarX are building similar dashboards, we want SonarX to stay competitive.  | Goal 1,2,3 |

## 2. Goals and Objectives

We have determined three goals for our project. All relate to the issues discussed in the introduction. Our goals also correspond to the discussion we had at the initial meeting with SonarX. Phase 1 of our project deals with calculating the profit and loss of each proxy wallet using historical data. Phase 2 associates proxy wallets with their owner (EOA) wallets and uses real time data. We will leave Phase 2 as future work. Each goal is listed as an epic in the GitHub repository used by our team, and each objective is listed as a user story in the same repository.

**Goal 1: Compute the profit and loss of each Polymarket proxy wallet** [[epic:#24]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/24 "Goal 1: Compute the profit and loss of each Polymarket proxy wallet")

Objective 1.1: Collect all Polymarket market resolutions and trades from SonarX's Polygon blockchain data stored in Snowflake over a historical period agreed upon with SonarX. [[story:#25]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/25 "Objective 1.1: Collect all Polymarket market resolutions and trades from SonarX's Polygon blockchain data stored in Snowflake over a historical period agreed upon with SonarX")

Objective 1.2: Associate each wallet's transactions with their market resolution in order to determine whether each position is open or closed. [[story:#26]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/26 "Objective 1.2: Associate each wallet's transactions with their market resolution in order to determine whether each position is open or closed")

Objective 1.3: Compute the realized PNL for closed positions and the unrealized PNL for open positions for each proxy wallet. [[story:#27]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/27 "Objective 1.3: Compute the realized PNL for closed positions and the unrealized PNL for open positions for each proxy wallet")

Objective 1.4: Test the accuracy of the computed PNL by comparing a sample of at least 25 wallets, including both highly profitable and ordinary wallets, to data from Predicts.guru and Polymarket Analytics and note any discrepancies. [[story:#28]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/28 "Objective 1.4: Test the accuracy of the computed PNL by comparing a sample of at least 25 wallets, including both highly profitable and ordinary wallets, to data from Predicts.guru and Polymarket Analytics and note any discrepancies")

**Goal 2: Determine the most profitable traders and the factors that contribute to that profitability** [[epic:#29]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/29 "Goal 2: Determine the most profitable traders and the factors that contribute to that profitability")

Objective 2.1: Compute the PNL and return on investment for each proxy wallet and produce a leaderboard of the most profitable traders. [[story:#30]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/30 "Objective 2.1: Compute the PNL and return on investment for each proxy wallet and produce a leaderboard of the most profitable traders")

Objective 2.2: Analyze the trading behaviors of each ranked wallet, including win rate, average entry price, market categories traded, and position holding period. [[story:#31]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/31 "Objective 2.2: Analyze the trading behaviors of each ranked wallet, including win rate, average entry price, market categories traded, and position holding period")

Objective 2.3: Determine how the top 100 traders differ from the remaining wallets by comparing their trading behaviors to all other wallets, and note at least three observations regarding the differences between profitable and unprofitable traders. [[story:#32]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/32 "Objective 2.3: Determine how the top 100 traders differ from the remaining wallets by comparing their trading behaviors to all other wallets, and note at least three observations regarding the differences between profitable and unprofitable traders")

**Goal 3: Create a client-facing dashboard that allows for an easy interpretation of PNL data** [[epic:#33]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/33 "Goal 3: Create a client-facing dashboard that allows for an easy interpretation of PNL data")

Objective 3.1: Determine a list of questions that SonarX clients would like answered by the dashboard, and have this list approved by our SonarX mentor, prior to creating any aspect of the dashboard. [[story:#34]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/34 "Objective 3.1: Determine a list of questions that SonarX clients would like answered by the dashboard, and have this list approved by our SonarX mentor, prior to creating any aspect of the dashboard")

Objective 3.2: Create a leaderboard page to display the top traders and allow filtering and sorting of these traders. [[story:#35]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/35 "Objective 3.2: Create a leaderboard page to display the top traders and allow filtering and sorting of these traders")

Objective 3.3: Create a wallet lookup page to display a wallet's open and closed positions, realized and unrealized PNL, and trading behaviors. [[story:#36]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/36 "Objective 3.3: Create a wallet lookup page to display a wallet's open and closed positions, realized and unrealized PNL, and trading behaviors")

Objective 3.4: Create a fast dashboard where all pages load in under 3 seconds on our demo data. [[story:#37]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/37 "Objective 3.4: Create a fast dashboard where all pages load in under 3 seconds on our demo data")

Objective 3.5: Show a functional version of our dashboard to SonarX and note their feedback. [[story:#38]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/38 "Objective 3.5: Show a functional version of our dashboard to SonarX and note their feedback")

## 3. Proposed Approach

Deciding on how traders are ranked. We chose to rank traders by both total PNL and return on investment (ROI), rather than only choosing one (Objective 2.1). Total PNL will help show us the amount of profit or loss a trader generates in actual dollars, though it tends to favor the wallets with more capital, rather than the wallets profiting more capital. ROI measures profit relative to the capital invested, percentage wise, but it over-reward small wallets that may have had lucky bets. By using both, on the dashboard we can have clients sort the different traders, by either total PNL or ROI (Objective 3.2), and our dashboard is more detailed with both.

How accuracy is validated. We decided to compare 25+ wallets to Predicts.guru and Polymarket Analytics instead of internal consistency checks only because we can check that our data matches the external sources provided (Objective 1.4). By doing that, our credibility is better because  it is relying on reliable sources. If we were to only do internal consistency checks, it would be great for testing during our development phase, but overall would not be able to match the real-world trading market.

Scope. We will start with historical proxy wallets (Phase 1) rather than starting with linking to owner wallets and use real-time data (Phase 2). This is because for the beginning, we are able to validate wallet rankings, PNL, and ROI before interweaving live data complexity, which will be easier to work with. If we were to link owner wallets and use-real time data, there would be data reliability issues because the real data will be constantly changing, whereas historical proxy wallets allow us to validate our data with external resources like Polymarket Analytics. 

Dashboard. We have decided to agree on client questions with the mentor first (Objective 3.1), rather than build first and adjust later. We already made a document containing questions that the clients would want answered within this dashboard. By choosing to have client questions to frame our dashboard, we can easily work with our mentor on how our project is supposed to look, rather than building a completely different dashboard that we may need to change completely. 

The implementation stack and tooling are detailed in §4.

## 4. Required Environment, Resources, and Planned Activities

Our project will run its queries on Snowflake, which is the main warehouse SonarX uses for its Polygon blockchain data, as confirmed at our kickoff meeting with SonarX. SonarX allows us to use open source tools and libraries. The languages, frameworks, and services for the PNL pipeline and the dashboard have not been chosen yet. We will record them in this section once the team decides, along with a high level architecture diagram and a system context diagram kept in `docs/design/`.

### Specification and design documents

No specification or design documents have been written yet. Each one will be listed here with the objective it serves as it is added to `docs/specs/` or `docs/design/`.

### Planned activities — the work items

The goals and objectives are listed in §2 as epics and user stories. The table below lists every other work item, the activities that support those objectives and the proposal itself.

| Issue | Type | Activity | Parent | Owner | Sprint |
|---|---|---|---|---|---|
| [[task:#1]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/1 "Replace the course setup guide README with the team README template") | task | Replace the course setup guide README with the team README template | none (writing task) | Justin Cox | Sprint 1 |
| [[task:#3]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/3 "Fill in team README.md and CLAUDE.md") | task | Fill in team README.md and CLAUDE.md | none (writing task) | Justin Cox | Sprint 1 |
| [[task:#10]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/10 "README and CLAUDE.md updated with the SNX-1 project details") | task | README and CLAUDE.md updated with the SNX-1 project details | none (writing task) | Bryan Orozco | Sprint 1 |
| [[task:#11]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/11 "Fill the proposal cover page and draft §1 Introduction background") | task | Fill the proposal cover page and draft §1 Introduction background | none (writing task) | Leila De Belen | Sprint 1 |
| [[sub-task:#12]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/12 "Research how prediction markets and Polymarket work") | sub-task | Research how prediction markets and Polymarket work | #11 | Kyle Quach | Sprint 1 |
| [[sub-task:#13]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/13 "Research existing Polymarket PNL and leaderboard tools") | sub-task | Research existing Polymarket PNL and leaderboard tools | #11 | Justin Cox | Sprint 1 |
| [[task:#20]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20 "SNX-1 kickoff meeting notes with SonarX (Oct 6, 2026)") | task | SNX-1 kickoff meeting notes with SonarX (Oct 6, 2026) | none (meeting) | Team | Sprint 1 |
| [[task:#41]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/41 "Write §2 Goals and Objectives and §4 work item links into proposal.md") | task | Write §2 Goals and Objectives and §4 work item links into proposal.md | none (writing task) | Bryan Orozco | Sprint 1 |
| [[task:#42]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/42 "Write the Sprint 1 review") | task | Write the Sprint 1 review | none (writing task) | Bryan Orozco | Sprint 1 |
| [[task:#49]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/49 "Write §3 Proposed Approach in proposal.md") | task | Proposal §3 Proposed Approach | none (writing task) | Leila De Belen | Sprint 2 |

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

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

## 3. Proposed Approaches

Deciding on how traders are ranked. We chose to rank traders by both total PNL and return on investment (ROI), rather than only choosing one (Objective 2.1). Total PNL will help show us the amount of profit or loss a trader generates in actual dollars, though it tends to favor the wallets with more capital, rather than the wallets profiting more capital. ROI measures profit relative to the capital invested, percentage wise, but it over-reward small wallets that may have had lucky bets. By using both, on the dashboard we can have clients sort the different traders, by either total PNL or ROI (Objective 3.2), and our dashboard is more detailed with both.

How accuracy is validated. We decided to compare 25+ wallets to Predicts.guru and Polymarket Analytics instead of internal consistency checks only because we can check that our data matches the external sources provided (Objective 1.4). By doing that, our credibility is better because  it is relying on reliable sources. If we were to only do internal consistency checks, it would be great for testing during our development phase, but overall would not be able to match the real-world trading market.

Scope. We will start with historical proxy wallets (Phase 1) rather than starting with linking to owner wallets and use real-time data (Phase 2). This is because for the beginning, we are able to validate wallet rankings, PNL, and ROI before interweaving live data complexity, which will be easier to work with. If we were to link owner wallets and use-real time data, there would be data reliability issues because the real data will be constantly changing, whereas historical proxy wallets allow us to validate our data with external resources like Polymarket Analytics. 

Dashboard. We have decided to agree on client questions with the mentor first (Objective 3.1), rather than build first and adjust later. We already made a document containing questions that the clients would want answered within this dashboard. By choosing to have client questions to frame our dashboard, we can easily work with our mentor on how our project is supposed to look, rather than building a completely different dashboard that we may need to change completely. 

The implementation stack and tooling are detailed in §4.

## 4. Required Environment, Resources, and Planned Activities

Our project will run its queries on Snowflake, which is the main warehouse SonarX uses for its Polygon blockchain data, as confirmed at our kickoff meeting with SonarX. SonarX allows us to use open source tools and libraries. The languages, frameworks, and services for the PNL pipeline and the dashboard have not been chosen yet. We will record them in this section once the team decides, along with a high level architecture diagram and a system context diagram kept in `docs/design/`.

### Specification and design documents

Each specification and design document is listed here with the objectives it serves, as it is added to `docs/specs/` or `docs/design/`.

The position matching and PNL specification, [`docs/specs/pnl-calculation.md`](../docs/specs/pnl-calculation.md), defines how trades become positions, how FIFO cost basis works, when a position is open or closed, and the realized and unrealized PNL formulas, with a worked example computed by hand. It serves Objective 1.2 and Objective 1.3. [[task:#55]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/55 "Draft docs/specs/pnl-calculation.md (Goal 1 definitions)")

The trader ranking and behavior specification, [`docs/specs/trader-ranking.md`](../docs/specs/trader-ranking.md), defines how proxy wallets are ranked by total PNL and by return on investment (including the minimum activity rule and the tie breaks), and how win rate, average entry price, market categories traded, and position holding period are calculated, with a worked example computed by hand. It serves Objective 2.1 and Objective 2.2. [[task:#54]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/54 "Draft docs/specs/trader-ranking.md (Goal 2 definitions)")

The architecture design, [`docs/design/architecture.md`](../docs/design/architecture.md), holds the high level architecture diagram and the system context diagram: SonarX's Snowflake data feeds the analysis, the analysis produces results, and the dashboard shows those results to its user. It serves Objectives 1.1, 2.1 and 3.2. [[task:#56]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/56 "Write docs/design/architecture.md with high level architecture and system context diagrams")

The prototype implementation and module diagram, [`docs/design/implementation.md`](../docs/design/implementation.md), displays how our prototype directory is structured, credential configuration, security, proposed structure for setup and testing, and proposed build order. It serves Objective 1.1. [[task:#61]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/61 "Write docs/design/implementation.md (module layout, configuration, build order)")

The data flow design, [`docs/design/data-flow.md`](../docs/design/data-flow.md), shows how data moves from SonarX's Snowflake tables through position matching, PNL, ranking and metrics to the dashboard, as a Level 0 context diagram and a Level 1 diagram whose processes are numbered to match the specification. It serves Objectives 1.1 to 1.3, 2.1, 2.2, 3.2 and 3.3. [[task:#58]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/58 "Write docs/design/data-flow.md with Level 0 and Level 1 data flow diagrams")


### Planned activities: the work items

The goals and objectives in §2 are tracked as epics and user stories. Each user story is broken into the features it needs, each feature into tasks, and a task into sub tasks where that helps, all linked as GitHub sub issues so a reader can start at a goal and walk down to the smallest piece of work. A feature does not have to be code: writing a specification, designing a data model or drawing a data flow diagram is a feature or a task, and it closes when a reviewed pull request merges the document it produces. Story points sit on the user story only, so none of the items below carry their own, except the writing tasks at the end of this section that have no objective above them. Each paragraph ends with the issues it describes.

#### Goal 1: computing the profit and loss of each proxy wallet

Objective 1.1 starts with a data source specification. Both of our specifications leave the question of which SonarX tables and columns hold each field to a separate document, because the answer depends on the Polymarket schema documentation SonarX shares with our Snowflake access. Justin Cox maps the trade and market resolution tables from that documentation and writes the specification, covering scope, functional and non functional requirements, acceptance criteria and open questions in the same form as our other specifications. [[feature:#83]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/83 "Data source specification for Polymarket trades and market resolutions") [[task:#103]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/103 "Map SonarX's Polymarket trade and resolution tables and columns from the schema docs") [[task:#104]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/104 "Write docs/specs/data-sources.md (scope, requirements, acceptance criteria, open questions)")

The prototype reads those tables through one extraction layer in `prototype/src/database/`, so that position matching, PNL and ranking never talk to Snowflake directly and can be tested on synthetic fixtures. Kyle Quach first wires the project skeleton and the Snowflake connection, with credentials supplied only through environment variables, and then writes the read only queries that pull trades and resolutions for the 12 month Phase 1 window. [[feature:#84]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/84 "Snowflake extraction layer in prototype/src/database") [[task:#62]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/62 "Wire prototype v0 infrastructure: project skeleton and Snowflake connection") [[task:#105]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/105 "Write read only extract queries for trades and resolutions over the 12 month window, with fixture tests")

The structure of `prototype/` follows the architecture and implementation design. The high level architecture and system context diagrams merged in Sprint 2, and a revision of both diagrams is in review. The implementation design lays out the module folders, configuration and secret handling, and the order the prototype is built in. In Sprint 3 the architecture document is expanded into the six parts a design document needs: the system context, the components and their responsibilities, the data model, the data flow, the key decisions with the alternatives we rejected, and what is not designed yet. [[feature:#85]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/85 "Prototype architecture and implementation design") [[task:#56]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/56 "Write docs/design/architecture.md with high level architecture and system context diagrams") [[sub-task:#80]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/80 "Revision of High Level Architecture and System Context Diagrams") [[task:#61]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/61 "Write docs/design/implementation.md (module layout, configuration, build order)") [[task:#106]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/106 "Expand architecture.md into the six design sections Kyoung lists")

Objective 1.2 rests on the position matching and PNL specification, which defines how trades become positions, how FIFO lots are built and matched, and when a position is open or closed. The draft merged in Sprint 2. Six open questions remain for our mentor and SonarX's data owner, about incomplete positions, trading fees, latest prices, other events that change a wallet's shares, payouts other than 1.00 or 0.00, and the validation tolerance; Bryan Orozco owns getting those answers. [[feature:#86]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/86 "Position matching and PNL specification") [[task:#55]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/55 "Draft docs/specs/pnl-calculation.md (Goal 1 definitions)") [[task:#107]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/107 "Get answers to PNL spec open questions Q1 to Q6 from Erel and Sergio")

The PNL pipeline design shows how the pipeline steps fit together through three documents: the data model with its entity relationship diagram, the data flow design with its Level 0 and Level 1 diagrams, and the PNL pipeline design with a UML sequence diagram of one PNL run. The data flow design numbers its processes the same way the specifications number the pipeline steps, so a process in a diagram and a step in a specification always mean the same thing. [[feature:#87]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/87 "PNL pipeline design: data model, data flow and sequence diagrams") [[task:#57]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/57 "Write docs/design/data-model.md with the ER diagram") [[task:#58]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/58 "Write docs/design/data-flow.md with Level 0 and Level 1 data flow diagrams") [[task:#59]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/59 "Write docs/design/pnl-pipeline.md with a UML sequence diagram of a PNL run")

The first half of the Sprint 3 demo slice is the position builder. Kyle Quach implements grouping trades into one position per wallet, market and outcome token with FIFO lots, including the rule that marks a position incomplete when a sale is larger than the shares held, and then the matching of each position to its market resolution to set it open or closed. Each functional requirement gets a test. [[feature:#88]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/88 "Position builder and resolution matching in the prototype (FR-1 to FR-5, FR-8 to FR-10)") [[task:#108]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/108 "Implement position grouping and lot building (FR-1 to FR-5) with tests") [[task:#109]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/109 "Implement resolution matching and open or closed status (FR-8 to FR-10) with tests")

Objective 1.3 is the second half of the Sprint 3 slice. Justin Cox implements FIFO sale matching and realized PNL, using the worked example in the specification as tests that fail if any one rule is removed, and then unrealized PNL, wallet totals and the incomplete flag. Bryan Orozco writes the setup, run and test steps in `prototype/README.md` and updates §5 so the proposal says what the prototype does today. [[feature:#89]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/89 "Realized and unrealized PNL in the prototype (FR-6, FR-7, FR-11 to FR-15)") [[task:#110]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/110 "Implement FIFO sale matching and realized PNL (FR-6, FR-7, FR-11) with the worked example as tests") [[task:#111]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/111 "Implement unrealized PNL, wallet totals and the incomplete flag (FR-12 to FR-15) with tests") [[task:#112]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/112 "Write prototype/README.md setup, run and test steps for the PNL slice and update proposal §5")

Objective 1.4 validates the computed PNL in Sprint 4. Bryan Orozco chooses a sample of at least 25 wallets, both highly profitable and ordinary, compares our PNL for each to Predicts.guru and Polymarket Analytics, and writes up every discrepancy with its likely cause. [[feature:#90]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/90 "PNL validation against Predicts.guru and Polymarket Analytics") [[task:#113]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/113 "Choose the 25 wallet validation sample, both highly profitable and ordinary") [[task:#114]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/114 "Compare computed PNL to Predicts.guru and Polymarket Analytics and write up the discrepancies")

#### Goal 2: the most profitable traders and what drives them

Objective 2.1 rests on the trader ranking and behavior specification, which defines total PNL, return on investment, the minimum activity rule, the two rankings and their tie breaks. The draft merged in Sprint 2, and seven open questions remain for our mentor and SonarX's data owner. [[feature:#91]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/91 "Trader ranking and behavior specification") [[task:#54]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/54 "Draft docs/specs/trader-ranking.md (Goal 2 definitions)") [[task:#115]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/115 "Get answers to ranking spec open questions Q1 to Q7 from Erel and Sergio")

Kyle Quach implements the ranking in the prototype: total PNL, return on investment and the PNL ranking with its tie breaks first, then the ROI ranking with the minimum activity thresholds that keep one lucky bet on a nearly empty wallet from taking the top. [[feature:#92]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/92 "Wallet ranking in the prototype (FR-1 to FR-10)") [[task:#116]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/116 "Implement total PNL, ROI and the PNL ranking with tie breaks (FR-1 to FR-5) with tests") [[task:#117]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/117 "Implement the ROI ranking with minimum activity thresholds (FR-6 to FR-10) with tests")

Objective 2.2 adds the trading behavior metrics. Justin Cox implements win rate, holding period and open position age, then average entry price and market categories traded, each with tests. Bryan Orozco then checks the metrics for three wallets by hand, since the specification requires the check to be done by a teammate who did not write the code. [[feature:#93]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/93 "Trading behavior metrics in the prototype (FR-11 to FR-18)") [[task:#118]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/118 "Implement win rate, holding period and open position age (FR-12, FR-13, FR-16 to FR-18) with tests") [[task:#119]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/119 "Implement average entry price and market categories (FR-14, FR-15) with tests") [[task:#120]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/120 "Hand check the metrics for 3 wallets against the code output (reviewer did not write the code)")

Objective 2.3 compares the top 100 traders with all other wallets in Sprint 4. Justin Cox computes each behavior metric for both groups, and Bryan Orozco writes at least three observations about how profitable and unprofitable traders differ. [[feature:#94]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/94 "Top 100 versus remaining wallets comparison") [[task:#121]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/121 "Compute each behavior metric for the top 100 and for all other wallets") [[task:#122]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/122 "Write at least three observations on profitable versus unprofitable traders")

#### Goal 3: the client facing dashboard

Objective 3.1 comes before any part of the dashboard is built. Leila De Belen drafts the list of questions SonarX clients want the dashboard to answer, starting from the questions our mentor sent on October 20, and Bryan Orozco takes the list to our mentor for approval. [[feature:#95]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/95 "Dashboard client question list") [[task:#123]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/123 "Draft docs/specs/dashboard-questions.md from Erel's starting client questions") [[task:#124]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/124 "Get the dashboard question list approved by Erel")

Objective 3.2 depends on two documents. The dashboard specification is the third of our specifications, one for each goal, and the dashboard page flow design shows how a user moves between the leaderboard and the wallet lookup page. The leaderboard page itself is built in Sprint 4: a table of top traders that sorts by total PNL and by return on investment, with the filters the approved question list calls for. [[feature:#96]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/96 "Dashboard specification (Goal 3)") [[task:#125]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/125 "Write docs/specs/dashboard.md (scope, requirements, acceptance criteria, open questions)") [[feature:#97]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/97 "Dashboard page flow design") [[task:#60]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/60 "Write docs/design/dashboard-flow.md with the page flow diagram") [[feature:#98]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/98 "Leaderboard page") [[task:#126]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/126 "Build the leaderboard table with sorting by total PNL and by ROI") [[task:#127]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/127 "Add the leaderboard filters the approved question list calls for")

Objective 3.3 is the wallet lookup page, where a user searches for a wallet and sees its open and closed positions, its realized and unrealized PNL and its behavior metrics. Leila De Belen builds the page, and Kyle Quach builds the results API that serves both pages from the pipeline's stored output. [[feature:#99]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/99 "Wallet lookup page") [[task:#128]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/128 "Build wallet search and the open and closed positions table") [[task:#129]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/129 "Show the wallet's realized and unrealized PNL and behavior metrics") [[feature:#100]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/100 "Results API that serves the dashboard pages") [[task:#130]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/130 "Serve leaderboard and wallet results from precomputed tables")

Objective 3.4 keeps every page under 3 seconds on our demo data. Rankings and wallet summaries are computed ahead of time so the pages only read stored results, and Bryan Orozco measures and records every page's load time. [[feature:#101]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/101 "Page load times under 3 seconds on demo data") [[task:#131]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/131 "Precompute rankings and wallet summaries so pages read stored results") [[task:#132]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/132 "Measure every page's load time on the demo data and record the results")

Objective 3.5 closes the semester's work with a demonstration to SonarX. Bryan Orozco runs the demo, records the feedback in a meeting issue, and files an issue for each change SonarX asks for. [[feature:#102]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/102 "SonarX dashboard demo and feedback") [[task:#133]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/133 "Run the dashboard demo with SonarX and record their feedback in a meeting issue") [[task:#134]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/134 "File an issue for each change SonarX asks for")

#### Work that sits outside the objectives

Sprint 1 was mostly writing and setup. Justin Cox replaced the course setup guide with our team README and filled in the README and the assistant instructions, which Bryan Orozco later updated with the SNX-1 project details. Leila De Belen filled in the cover page and drafted the introduction, drawing on research by Kyle Quach on how prediction markets work and by Justin Cox on existing PNL and leaderboard tools. The team recorded the kickoff meeting with SonarX, and Bryan Orozco wrote the goals and objectives into this proposal and wrote the Sprint 1 review. [[task:#1]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/1 "Replace course setup guide README with team README template") [[task:#3]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/3 "Fill in team README.md and CLAUDE.md") [[task:#10]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/10 "README and CLAUDE.md") [[task:#11]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/11 "Fill proposal cover page and draft §1 Introduction: background") [[sub-task:#12]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/12 "Research: how prediction markets and Polymarket work") [[sub-task:#13]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/13 "Research: existing Polymarket PNL and leaderboard tools") [[task:#20]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/20 "SNX-1 Kickoff Meeting Notes (Oct 6, 2026)") [[task:#41]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/41 "Write §2 Goals and Objectives and §4 work item links into proposal.md") [[task:#42]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/42 "Write the Sprint 1 review (docs/sprint-reviews/sprint-1.md)")

Sprint 2 continued the proposal. Leila De Belen wrote §3, and Bryan Orozco filled in the development plan, replaced the template references with our sources, condensed the team's research into one project context document, cited the Sprint 2 work items in this section, and is writing the Sprint 2 review. Recording the chosen prototype stack is still open, because the stack has not been decided. [[task:#49]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/49 "Write §3 Proposed Approach in proposal.md") [[task:#50]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/50 "Fill in docs/development-plan.md") [[task:#51]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/51 "Fix §8 References in proposal.md") [[task:#63]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/63 "Write the team source of truth doc from today's research") [[task:#65]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/65 "Cite the Sprint 2 work items in proposal §4") [[task:#53]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/53 "Write the Sprint 2 review (docs/sprint-reviews/sprint-2.md)") [[task:#52]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/52 "Record the chosen prototype stack in CLAUDE.md and proposal §4")

In Sprint 3, Bryan Orozco brought the repository in line with the course's Sprint 3 guidance: pull requests merged into our integration branch now close their issues, every user story is broken into features and tasks, and this section describes the work in prose. [[task:#82]](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/82 "Bring repo in line with Sprint 3 instructions: auto close, issue chain, §4 prose")

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

[1] Polymarket. What is Polymarket. Polymarket Help Center. https://help.polymarket.com/en/articles/13364060-what-is-polymarket (accessed Oct. 4, 2026).

[2] Polygon. WTF is Polygon? Polygon Blog, Apr. 4, 2024. https://polygon.technology/blog/wtf-is-polygon (accessed Oct. 24, 2026).

[3] Polymarket. Polymarket 101. Polymarket Documentation. https://docs.polymarket.com/polymarket-101 (accessed Oct. 4, 2026).

[4] Polymarket Analytics. Polymarket Analytics: Prediction Market Data, Analytics and Trader Leaderboard. https://polymarketanalytics.com/ (accessed Oct. 4, 2026).

[5] Predicts.guru. https://www.predicts.guru/ (accessed Oct. 4, 2026).

[6] Polycopy. Polycopy: The Home for Copy Trading on Polymarket. https://polycopy.app/ (accessed Oct. 24, 2026).

[7] PolyTrack. PolyTrack: #1 Polymarket Whale Tracker and Copy Trading Platform. https://polytrackhq.app/ (accessed Oct. 24, 2026).

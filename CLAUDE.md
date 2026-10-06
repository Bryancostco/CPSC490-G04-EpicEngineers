## The project

- **Course:** CPSC 490 Undergraduate Seminar, Fall 2026 (proposal + prototype
  semester; full implementation happens in CPSC 491).
- **Team:** Group 4 Epic Engineers — members in `README.md`.
- **Project:** Polygon Prediction Market PNL and Trader Profitability Analytics. A profit and loss (PNL) accounting tool for Polymarket that parses on chain trades from SonarX's Polygon blockchain data, matches positions to market resolutions, computes realized and unrealized PNL per wallet, and ranks the most profitable traders by what drives their edge, shown in a dashboard.
- **Sponsor:** SNX-1 (SonarX)
- **Source of truth:** `proposal/proposal.md`. Specs in `docs/specs/`,
  designs in `docs/design/`, proof-of-concept code in `prototype/`.
- **Stack (prototype):** data source is SonarX's Polygon blockchain data (Polymarket trades and market resolutions). Languages, frameworks, and services are not chosen yet; the team records them here and in proposal §4 once decided. Do not assume a stack.

## How we work

- Work is tracked as GitHub issues: **epic = goal**, **user story =
  objective**; every story carries assignee, sprint milestone, `priority:`,
  and a `sp:` story-point label.
- Four 2-week sprints (`Sprint 1`–`Sprint 4`).
- Every change lands through a **pull request** that says `Closes #<story>`
  and is **approved by a teammate who is not the author**. CI must be green.
- A story is done only when its acceptance criteria are checked off and its
  PR is merged.

## What the assistant may and may not do

**May draft:** proposal and document prose, spec/design sections, prototype
code, tests, diagrams, commit messages, PR descriptions, review comments,
alternatives and trade-off analyses.

**Must NOT decide (a human decides):**
- whether a story is **done** — acceptance criteria are judged by a person;
- **scope**: adding, dropping, or reinterpreting a goal, objective, or
  acceptance criterion;
- **design trade-offs** that outlive the sprint (architecture, data model,
  third-party dependencies);
- anything that touches the **sponsor relationship** or course deliverables.

**Never:**
- weaken or reword an acceptance criterion so the current output passes —
  if the criterion is wrong, a human changes it deliberately, in its own PR;
- invent citations, benchmark numbers, sponsor requirements, or API behavior;
  cite what can be checked, and say plainly what you could not verify;
- claim something works without naming the evidence (command run, test
  passed, page opened);
- commit secrets, API keys, `.env` files, or anything student-identifying
  beyond the team's own names.

## House rules for output

1. **Quote the requirement verbatim** before working on it (story text or
   acceptance criterion). Do not paraphrase it into something easier.
2. **Verify what you can, name what you cannot.** End substantial work with
   what was checked and what remains unverified.
3. **Small steps.** One story at a time; if it cannot be finished in one
   pass, say so and propose a split instead of half-doing it.
4. **Match the existing document or code style** in this repo rather than
   introducing a new one.
5. **Cite file paths and issue numbers** so a reviewer can follow the trail
   (`docs/specs/x.md §2`, `#12`).

## Conventions

- Markdown documents, one topic per file; every doc's first lines name its
  epic and stories (`> Epic: #1 · Stories: #2, #4`).
- Branches: `<issue-number>-short-slug` (e.g. `12-login-spec`).
- Commit subject: imperative, under ~72 chars; body explains *why*.
- Disclose AI use in each PR (see `.github/PULL_REQUEST_TEMPLATE.md`) and in
  the proposal's **AI Usage** section.

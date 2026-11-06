# Prototype

> Epic: #24 · Stories: #25 · Feature: #84 · Task: #62

Proof of concept for SNX-1: Polymarket PNL per proxy wallet from SonarX's
Polygon data. The stack is recorded in `CLAUDE.md` (#52): Python 3.12 running
outside Snowflake, with `snowflake-connector-python` for reads, exact
decimals for money, and `pytest` on fixtures. The layout follows
`docs/design/implementation.md`.

```text
prototype/
├── .env.example        blank list of the Snowflake variables (copy to .env)
├── requirements.txt    pinned dependencies
├── pytest.ini          puts src/ on the import path for tests
├── src/
│   ├── config/         settings.py: reads and validates SNOWFLAKE_ variables
│   ├── database/       snowflake_client.py: the only code that talks to Snowflake
│   ├── services/       positions, PNL and ranking (no Snowflake imports)
│   └── app/            smoke_query.py: command line entry points
└── tests/
    ├── unit/           run anywhere, no credentials
    ├── integration/    live Snowflake tests, skipped unless credentials are set
    └── fixtures/       synthetic data, such as the specs' worked examples
```

## How to run

Prerequisites: Python 3.12 and the Snowflake credentials SonarX shares
through the Slack channel. Never commit them.

```bash
cd prototype
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env
# fill in .env, then:
python src/app/smoke_query.py      # prints the row count and where the session landed
```

Without a complete `.env` the smoke run stops with exit code 2 and names the
missing variables. It never prints the password.

## How to test

```bash
cd prototype
python -m pytest -q
```

CI runs the same command on every pull request (job **Prototype build &
tests**). Unit tests use fakes and fixtures, so they need no credentials. The
live smoke test in `tests/integration/` is skipped unless every `SNOWFLAKE_`
variable is set.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Missing Snowflake settings: ...` | Copy `.env.example` to `.env` in `prototype/` and fill in the named variables |
| `ModuleNotFoundError: config` when running a test file directly | Run `python -m pytest` from `prototype/`, which reads `pytest.ini` |
| Authentication or permission errors | Check the values with SonarX in Slack; do not paste credentials into an issue, a PR or a prompt |

## Status

| Sprint | Increment |
|---|---|
| Sprint 3 | v0 skeleton: settings from environment variables, Snowflake client, smoke query, tests without credentials (#62) |

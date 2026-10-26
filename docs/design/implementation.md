# Prototype Structure, Setup, and Implementation Plan

## 1. Purpose

The `prototype/` directory will contain the initial working implementation of EpicEngineers. It will provide a small, testable environment for validating the selected application stack, connecting to Snowflake, and demonstrating the core workflow before expanding into a complete application.

**Dependency:** Implementation is blocked on the technology stack decision in [Issue #52](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/52). The folder structure below is a proposed baseline. Framework-specific dependencies, commands, and configuration must be finalized after that decision.

## 2. Proposed Directory Structure

```text
prototype/
├── README.md
├── .env.example
├── .gitignore
├── config/
│   └── README.md
├── src/
│   ├── app/
│   │   └── README.md
│   ├── services/
│   │   └── README.md
│   ├── database/
│   │   └── README.md
│   └── config/
│       └── README.md
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── docs/
    └── architecture.md
```

The exact filenames and source directories may change based on the decision in Issue #52.

### Directory responsibilities

- **`README.md`** — Documents prerequisites, environment setup, running the prototype, troubleshooting, and the implementation sequence.
- **`.env.example`** — Lists required environment variable names and safe placeholder values. It must never contain actual credentials.
- **`.gitignore`** — Prevents local environment files, secrets, virtual environments, dependency artifacts, caches, and generated files from being committed.
- **`config/`** — Holds non-secret configuration documentation and configuration examples.
- **`src/app/`** — Contains application entry points and the primary application workflow.
- **`src/services/`** — Contains reusable business logic and operations independent of the user interface.
- **`src/database/`** — Contains Snowflake connection handling and data-access logic, including queries or repository functions.
- **`src/config/`** — Loads and validates environment variables and exposes application configuration.
- **`tests/unit/`** — Tests individual functions and modules without requiring a live Snowflake connection.
- **`tests/integration/`** — Tests interactions between components and, when credentials and access are available, Snowflake connectivity and queries.
- **`tests/fixtures/`** — Contains synthetic test data and other non-sensitive test fixtures.
- **`docs/architecture.md`** — Records architectural decisions, component responsibilities, data flow, and known limitations.

Do not create unnecessary abstraction layers before the stack and initial requirements are confirmed. Keep the first working version small.

## 3. Configuration and Secret Management

### Security requirement

**Snowflake passwords must always be supplied through environment variables. Never hardcode passwords, commit them to the repository, or include them in logs, screenshots, error messages, or documentation.**

The prototype must fail safely when required configuration is missing instead of silently using credentials embedded in source code.

### Environment variables

The following names are proposed; confirm the required connection parameters against the selected Snowflake connector.

| Variable | Purpose |
|---|---|
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake password |
| `SNOWFLAKE_WAREHOUSE` | Warehouse used for queries |
| `SNOWFLAKE_DATABASE` | Target database |
| `SNOWFLAKE_SCHEMA` | Target schema |
| `SNOWFLAKE_ROLE` | Role used by the connection, if required |

### Local setup

1. Install the runtime and dependency manager required by the selected stack.
2. Copy `.env.example` to a local `.env` file, if the chosen framework supports this workflow.
3. Enter the required configuration values locally. Obtain credentials through the team's approved secret-sharing process.
4. Verify that `.env` is ignored by Git before entering any secrets.
5. Install the project's dependencies using the commands documented for the selected stack.
6. Run configuration validation and unit tests before attempting a database connection.

The `.env.example` file should contain only placeholder values, for example:

```dotenv
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role
```

The real `.env` file must remain local and untracked. If the selected deployment environment provides a secret manager or injects environment variables directly, use that mechanism instead of requiring a `.env` file.

### Required Git protections

The `.gitignore` file should include at least:

```gitignore
# Secrets and local configuration
.env
.env.*
!.env.example

# Runtime artifacts
__pycache__/
*.py[cod]
.venv/
venv/
node_modules/
dist/
build/
coverage/
.pytest_cache/
```

Adjust these patterns for the selected stack and any existing repository conventions. Before committing, inspect staged changes and verify that no credentials or sensitive configuration files are included.

## 4. How to Run the Prototype

The exact commands are intentionally deferred until Issue #52 establishes the stack.

Once the decision is finalized, the `prototype/README.md` must provide a verified sequence covering:

1. **Prerequisites:** Supported runtime version, dependency manager, and any required external accounts or permissions.
2. **Installation:** Exact commands to install dependencies from the prototype directory.
3. **Configuration:** How to supply environment variables and validate required settings.
4. **Local execution:** The exact command to launch the application and the local URL or CLI invocation, as applicable.
5. **Testing:** Commands for unit tests and integration tests, with clear instructions for tests requiring Snowflake access.
6. **Troubleshooting:** Common setup failures, missing environment variables, authentication errors, and connectivity or permission issues.

The first run should support a local smoke test without requiring live Snowflake credentials wherever practical. Database-dependent tests must clearly identify their prerequisites and must not run destructive operations against shared data.

## 5. Implementation Order

Build the prototype incrementally, validating each stage before moving on.

### Phase 1 — Resolve the stack decision

- Resolve [Issue #52](https://github.com/Bryancostco/CPSC490-G04-EpicEngineers/issues/52).
- Confirm the language, framework, dependency manager, Snowflake connector, and execution environment.
- Record the selected stack and rationale.
- Finalize the directory structure and runnable setup instructions.

**Exit criterion:** The team agrees on the stack and can document a reproducible development environment.

### Phase 2 — Establish the project foundation

- Create the prototype directory and essential files.
- Add dependency and runtime configuration.
- Add `.gitignore` and `.env.example`.
- Implement environment-variable loading and validation.
- Add a minimal application entry point and a basic unit-test setup.

**Exit criterion:** A developer can install dependencies, validate configuration, and run a basic local test without exposing secrets.

### Phase 3 — Implement Snowflake connectivity

- Configure the selected Snowflake client to read connection settings from environment variables.
- Implement a small, reusable connection module.
- Add safe error handling for missing settings, authentication failures, and connection timeouts.
- Add unit tests using mocked connections.
- Add an optional integration test that verifies connectivity and executes a harmless read-only query.

**Exit criterion:** The connection can be tested independently, and no credentials are embedded in source code or printed in logs.

### Phase 4 — Build the core data workflow

- Identify the minimum data required for the prototype.
- Implement the necessary Snowflake queries and data-access functions.
- Separate data-access logic from application or presentation logic.
- Test the workflow with synthetic fixtures and, where available, approved test data.
- Validate expected results and handle empty results and common query failures.

**Exit criterion:** The core workflow returns the expected data and has repeatable tests.

### Phase 5 — Build the application interface

- Implement the smallest interface or command-line workflow needed to demonstrate the core functionality.
- Connect the interface to the service and data-access layers.
- Add input validation, loading or execution feedback, and useful error messages.
- Confirm that secrets and sensitive connection details are never exposed to users.

**Exit criterion:** A developer can demonstrate the intended end-to-end prototype workflow.

### Phase 6 — Validate and document

- Run all unit tests and applicable integration tests.
- Test setup from a clean environment using the documented instructions.
- Review Git changes for accidentally staged secrets.
- Document architecture, limitations, and remaining work.
- Record follow-up issues for features that are outside the prototype's scope.

**Exit criterion:** Another team member can configure, run, test, and demonstrate the prototype using the README alone.

## 6. Development Principles

- **Security first:** Credentials come from environment variables or an approved secret-management mechanism.
- **Incremental delivery:** Build and test one layer at a time rather than implementing the entire application at once.
- **Separation of concerns:** Keep configuration, data access, business logic, and presentation independently testable.
- **Reproducibility:** Document exact, verified commands and required software versions.
- **Minimal scope:** Implement only the functionality needed to validate the prototype's core workflow.
- **Safe database access:** Prefer read-only operations and approved test data during early development.
- **Document decisions:** Update the architecture documentation when the team finalizes the stack or changes a major design choice.

## 7. Open Dependencies and Completion Criteria

The following remain dependent on Issue #52:

- Selected language and framework.
- Dependency installation and application launch commands.
- Snowflake connector and authentication mechanism.
- Final module layout and framework-specific configuration.
- Deployment and environment-specific setup.

The prototype foundation is ready for implementation when the stack decision is recorded, the setup is reproducible, secret handling is verified, and the team has agreed on the minimum end-to-end workflow.

The prototype is ready for demonstration when that workflow runs successfully, the applicable tests pass, and another developer can follow the documented setup without needing undocumented steps.

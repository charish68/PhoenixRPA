# PhoenixRPA

**PhoenixRPA** is a self-healing, workflow-based Robotic Process Automation (RPA) framework built with Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Playwright, and a browser-recording extension.

The framework allows browser workflows to be created, stored, executed, monitored, retried, and diagnosed through a backend API.

## Features

- Browser automation with Playwright
- Job management APIs
- Workflow step creation and persistence
- Conditional IF / ELSE execution
- Nested conditional branches
- Branch-path execution logging
- Execution runs and execution history
- Step-level execution logs
- Retry and failure handling
- Failure screenshots
- Deterministic selector healing
- AI-powered selector healing using Groq
- Playwright validation of AI-generated selectors
- AI healing timeout protection
- Healing metadata tracking
- Deterministic healing confidence scoring
- AI healing validation confidence
- Healing statistics and analytics API
- Browser recording extension
- PostgreSQL persistence
- Alembic database migrations
- FastAPI Swagger/OpenAPI documentation
- Automated test suite

## AI Self-Healing

PhoenixRPA can recover when a browser element's selector changes.

```text
Browser Action
      |
      v
Original Selector
      |
      | Failed
      v
Deterministic Healing
      |
      | Failed
      v
AI Healing Agent
      |
      v
Groq LLM
      |
      v
Suggested Selector
      |
      v
Playwright Validation
      |
      | Valid
      v
Retry Action
      |
      v
Store Healing Metadata

## Architecture

PhoenixRPA is organized around the following workflow:

Browser Recording Extension
            |
            v
      FastAPI Backend
            |
            v
      Job / Workflow API
            |
            v
      Workflow Validation
            |
            v
      Workflow Runner
            |
            v
      Workflow Dispatcher
            |
            v
    Playwright Browser
            |
            v
PostgreSQL + Execution Logs

## Workflow Execution

PhoenixRPA supports:

- Sequential workflow execution
- Conditional IF / ELSE branches
- Nested workflow steps
- Variable resolution
- Retry handling
- Execution logging
- Failure screenshots
- State preservation after successful and failed execution

## Reliability and Validation

Recent improvements include:

- Validation of workflow actions
- Validation of nested workflow structures
- Validation of conditions and condition operators
- Workflow runner state preservation tests
- Top-level step execution order tests
- Step failure handling tests
- Logging behavior tests
- Empty workflow handling tests
- Validation for empty and whitespace-only job fields
- Maximum job field length validation
- Invalid job field type validation
- Positive job ID validation

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Playwright
- Pydantic
- Groq API
- Pytest

## Testing

Run the automated test suite:

```bash
uv run python -m pytest -q --ignore=tests/test_groq_ai_healing_integration.py

```

The external Groq integration test is excluded because it depends on an external AI service.

## Project Goals

PhoenixRPA focuses on building reliable browser automation with:

- Workflow-based automation
- Self-healing selectors
- AI-assisted recovery
- Execution monitoring
- Failure diagnostics
- Workflow validation
- Automated testing

## Author

**Nagalla Venkata Charish Yadav**

AI / Automation Developer
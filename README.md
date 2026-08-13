PhoenixRPA

PhoenixRPA is a self-healing, workflow-based Robotic Process Automation (RPA) framework built with Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Playwright, and a browser-recording extension.

The framework allows browser workflows to be created, stored, executed, monitored, retried, and diagnosed through a backend API.

Features

Browser automation with Playwright

Job management APIs

Workflow step creation and persistence

Conditional IF / ELSE execution

Nested conditional branches

Branch-path execution logging

Execution runs and execution history

Step-level execution logs

Retry handling

Failure handling

Failure screenshots

Deterministic selector healing

AI-powered selector healing with Groq-compatible LLMs

Playwright validation of AI-generated selectors

AI healing timeout protection

Healing metadata tracking:

Healing status

Original selector

Healed selector

Healing method

Browser recording extension

PostgreSQL persistence

Alembic database migrations

FastAPI Swagger/OpenAPI documentation

Automated test suite

Self-Healing Selector Architecture

PhoenixRPA can recover from browser UI changes that make an existing selector invalid.

Browser Action
      |
      v
Original Selector
      |
      | selector fails
      v
Deterministic Healing
      |
      | no valid candidate
      v
AI Healing Agent
      |
      v
Groq / OpenAI-Compatible LLM
      |
      v
Suggested Selector
      |
      v
Playwright Validation
      |
      | valid
      v
Retry Browser Action
      |
      v
Record Healing Metadata

For example, a workflow may contain:

#userEmail

If the page changes the element to:

#emailInputChanged

PhoenixRPA can detect the failure, attempt deterministic recovery, and then ask the AI healing agent for a replacement selector when deterministic healing cannot recover the element.

AI-generated selectors are validated against the current Playwright page before they are accepted.

The AI request is also protected by a timeout so an external LLM call cannot indefinitely block workflow execution.

Healing Metadata

Successful healing is returned as structured metadata and persisted with execution logs.

Example:

{
  "status": "HEALED",
  "original_selector": "#userEmail",
  "healed_selector": "#emailInputChanged",
  "method": "AI"
}

This makes it possible to distinguish deterministic healing from AI-assisted healing and provides an execution-history trail for diagnosing automation failures.

Architecture

Browser Extension
       |
       v
   FastAPI API
       |
       +-------------------+-------------------+
       |                   |                   |
       v                   v                   v
   Services        Workflow Engine      Browser Services
       |                   |                   |
       +-------------------+-------------------+
                           |
                           v
                      Repositories
                           |
                           v
                       PostgreSQL
                           |
                           +-------------+-------------+
                           |             |             |
                           v             v             v
                         Jobs    Workflow Steps   Execution Runs
                                                     |
                                                     v
                                               Execution Logs

Technology Stack

Backend: Python, FastAPI

Browser Automation: Playwright

Database: PostgreSQL

ORM: SQLAlchemy

Migrations: Alembic

AI Healing: Groq / OpenAI-compatible LLM provider

Testing: Pytest, AsyncMock, integration tests

Package/Environment Management: uv

Testing

The project currently has 49 automated tests passing.

Run the complete test suite:

uv run python -m pytest -q

Run the AI healing integration test:

uv run python -m pytest -m integration -q -s

The integration test verifies the end-to-end AI selector healing flow using the configured Groq provider.

Configuration

Example database configuration:

DATABASE_URL=postgresql+psycopg2://postgres:phoenix@localhost:5432/phoenixrpa
PHOENIXRPA_EXTENSION_PATH=C:\Projects\PhoenixRPAackend\extension

AI healing uses the application's LLM configuration, including the provider, API key, model, base URL, and timeout settings.

API Documentation

When the FastAPI application is running, Swagger/OpenAPI documentation is available through the standard FastAPI documentation endpoints.

Project Status

PhoenixRPA currently has a working workflow execution engine with retries, browser automation, selector healing, AI-assisted selector recovery, execution logging, and automated test coverage.

The self-healing subsystem is designed to evolve toward richer execution analytics and production-oriented observability.

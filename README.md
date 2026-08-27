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
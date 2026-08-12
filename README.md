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
- Retry handling
- Failure handling
- Failure screenshots
- Selector healing / self-healing components
- Browser recording extension
- PostgreSQL persistence
- Alembic database migrations
- FastAPI Swagger/OpenAPI documentation
- Automated test suite

## Architecture

```text
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
DATABASE_URL=postgresql+psycopg2://postgres:phoenix@localhost:5432/phoenixrpa
PHOENIXRPA_EXTENSION_PATH=C:\Projects\PhoenixRPA\backend\extension
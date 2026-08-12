\# PhoenixRPA



\*\*PhoenixRPA\*\* is a self-healing, workflow-based Robotic Process Automation (RPA) framework built with Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Playwright, and a browser-recording extension.



The framework allows browser workflows to be created, stored, executed, monitored, retried, and diagnosed through a backend API.



\## Features



\- Browser automation with Playwright

\- Job management APIs

\- Workflow step creation and persistence

\- Conditional IF / ELSE execution

\- Nested conditional branches

\- Branch-path execution logging

\- Execution runs and execution history

\- Step-level execution logs

\- Retry handling

\- Failure handling

\- Failure screenshots

\- Selector healing / self-healing components

\- Browser recording extension

\- PostgreSQL persistence

\- Alembic database migrations

\- FastAPI Swagger/OpenAPI documentation

\- Automated test suite



\## Architecture



```text

Browser Extension

&#x20;      |

&#x20;      v

&#x20;  FastAPI API

&#x20;      |

&#x20;      +-------------------+-------------------+

&#x20;      |                   |                   |

&#x20;      v                   v                   v

&#x20;  Services        Workflow Engine      Browser Services

&#x20;      |                   |                   |

&#x20;      +-------------------+-------------------+

&#x20;                          |

&#x20;                          v

&#x20;                   Repositories

&#x20;                          |

&#x20;                          v

&#x20;                     PostgreSQL

&#x20;                          |

&#x20;            +-------------+-------------+

&#x20;            |             |             |

&#x20;            v             v             v

&#x20;           Jobs    Workflow Steps   Execution Runs

&#x20;                                         |

&#x20;                                         v

&#x20;                                  Execution Logs

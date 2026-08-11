import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from phoenixrpa.core.logger import logger

from phoenixrpa.api.health import router as health_router
from phoenixrpa.api.jobs import router as job_router
from phoenixrpa.api.executor import router as executor_router
from phoenixrpa.api.workflow import router as workflow_router
from phoenixrpa.api.execution import router as execution_router
from phoenixrpa.api.recorder import router as recorder_router

logger.info("Starting PhoenixRPA Backend")

app = FastAPI(
    title="PhoenixRPA API",
    description="Self-Healing Agentic RPA Framework",
    version="0.1.0",
)

# ----------------------------------------------------
# Enable CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Register Routers
# ----------------------------------------------------

app.include_router(health_router)
app.include_router(job_router)
app.include_router(executor_router)
app.include_router(workflow_router)
app.include_router(execution_router)
app.include_router(recorder_router)


@app.get("/")
async def root():
    return {
        "project": "PhoenixRPA",
        "version": "0.1.0",
        "status": "running",
    }

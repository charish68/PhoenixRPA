from fastapi import FastAPI

from phoenixrpa.api.health import router as health_router
from phoenixrpa.core.logger import logger

logger.info("Starting PhoenixRPA Backend")

app = FastAPI(
    title="PhoenixRPA API",
    description="Self-Healing Agentic RPA Framework",
    version="0.1.0",
)

app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "project": "PhoenixRPA",
        "version": "0.1.0",
        "status": "running",
    }
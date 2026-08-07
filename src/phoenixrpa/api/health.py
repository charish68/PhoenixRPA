from fastapi import APIRouter

from phoenixrpa.core.logger import logger

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {
        "status": "healthy",
        "service": "backend",
    }
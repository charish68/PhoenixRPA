from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO",
    colorize=True,
)

logger.add(
    LOG_DIR / "phoenixrpa.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="DEBUG",
    enqueue=True,
)

__all__ = ["logger"]
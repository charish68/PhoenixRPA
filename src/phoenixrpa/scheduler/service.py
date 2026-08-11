from apscheduler.schedulers.asyncio import AsyncIOScheduler

from phoenixrpa.core.logger import logger


class SchedulerService:

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        logger.info("Starting Scheduler")

        self.scheduler.start()

    def shutdown(self):
        logger.info("Stopping Scheduler")

        self.scheduler.shutdown()

    def add_job(
        self,
        func,
        trigger,
        **kwargs,
    ):
        self.scheduler.add_job(
            func,
            trigger,
            **kwargs,
        )
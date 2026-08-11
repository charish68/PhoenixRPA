from datetime import datetime, timezone

from sqlalchemy.orm import Session

from phoenixrpa.models.execution_log import ExecutionLog
from phoenixrpa.models.execution_run import ExecutionRun


class ExecutionRepository:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------
    # Execution Runs
    # --------------------------------------------------

    def create_run(
        self,
        job_id: int,
    ):
        run = ExecutionRun(
            job_id=job_id,
            status="RUNNING",
            started_at=datetime.now(timezone.utc),
        )

        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        return run

    def mark_run_success(
        self,
        run: ExecutionRun,
    ):
        run.status = "SUCCESS"
        run.finished_at = datetime.now(timezone.utc)

        run.duration_ms = int(
            (
                run.finished_at - run.started_at
            ).total_seconds() * 1000
        )

        self.db.commit()
        self.db.refresh(run)

        return run

    def mark_run_failed(
        self,
        run: ExecutionRun,
        error: str,
    ):
        run.status = "FAILED"
        run.error_message = error
        run.finished_at = datetime.now(timezone.utc)

        run.duration_ms = int(
            (
                run.finished_at - run.started_at
            ).total_seconds() * 1000
        )

        self.db.commit()
        self.db.refresh(run)

        return run

    # --------------------------------------------------
    # Step Execution Logs
    # --------------------------------------------------

    def create(
        self,
        job_id: int,
        step_order: int,
        action: str,
        run_id: int | None = None,
        branch_path: str | None = None,
    ):
        log = ExecutionLog(
            job_id=job_id,
            run_id=run_id,
            step_order=step_order,
            action=action,
            branch_path=branch_path,
            status="RUNNING",
            started_at=datetime.now(timezone.utc),
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log

    def mark_success(
        self,
        log: ExecutionLog,
    ):
        log.status = "SUCCESS"
        log.finished_at = datetime.now(timezone.utc)

        log.duration_ms = int(
            (
                log.finished_at - log.started_at
            ).total_seconds() * 1000
        )

        self.db.commit()
        self.db.refresh(log)

        return log

    def mark_failed(
        self,
        log: ExecutionLog,
        error: str,
    ):
        log.status = "FAILED"
        log.error_message = error
        log.finished_at = datetime.now(timezone.utc)

        log.duration_ms = int(
            (
                log.finished_at - log.started_at
            ).total_seconds() * 1000
        )

        self.db.commit()
        self.db.refresh(log)

        return log

    # --------------------------------------------------
    # History
    # --------------------------------------------------

    def list_by_job(
        self,
        job_id: int,
    ):
        return (
            self.db.query(ExecutionLog)
            .filter(
                ExecutionLog.job_id == job_id
            )
            .order_by(
                ExecutionLog.id
            )
            .all()
        )

    def list_by_run(
        self,
        run_id: int,
    ):
        return (
            self.db.query(ExecutionLog)
            .filter(
                ExecutionLog.run_id == run_id
            )
            .order_by(
                ExecutionLog.step_order,
                ExecutionLog.id,
            )
            .all()
        )

    def list_runs_by_job(
        self,
        job_id: int,
    ):
        return (
            self.db.query(ExecutionRun)
            .filter(
                ExecutionRun.job_id == job_id
            )
            .order_by(
                ExecutionRun.id.desc()
            )
            .all()
        )

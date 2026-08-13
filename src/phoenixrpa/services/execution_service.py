from phoenixrpa.repositories.execution_repository import (
    ExecutionRepository,
)


class ExecutionService:

    def __init__(self, db):
        self.repo = ExecutionRepository(db)

    # --------------------------------------------------
    # Execution Runs
    # --------------------------------------------------

    def start_run(
        self,
        job_id: int,
    ):
        return self.repo.create_run(
            job_id,
        )

    def finish_run(
        self,
        run,
    ):
        return self.repo.mark_run_success(
            run,
        )

    def fail_run(
        self,
        run,
        error: str,
    ):
        return self.repo.mark_run_failed(
            run,
            error,
        )

    # --------------------------------------------------
    # Step Execution Logs
    # --------------------------------------------------

    def start_step(
        self,
        job_id: int,
        step_order: int,
        action: str,
        run_id: int | None = None,
        branch_path: str | None = None,
        original_selector: str | None = None,
    ):
        return self.repo.create(
            job_id,
            step_order,
            action,
            run_id=run_id,
            branch_path=branch_path,
            original_selector=original_selector,
        )

    def finish_step(
        self,
        log,
    ):
        return self.repo.mark_success(
            log,
        )

    def mark_step_healed(
        self,
        log,
        original_selector: str,
        healed_selector: str,
        healing_method: str | None = None,
    ):
        return self.repo.mark_healed(
            log,
            original_selector,
            healed_selector,
            healing_method=healing_method,
        )

    def fail_step(
        self,
        log,
        error: str,
    ):
        return self.repo.mark_failed(
            log,
            error,
        )

    # --------------------------------------------------
    # History
    # --------------------------------------------------

    def list_logs(
        self,
        job_id: int,
    ):
        return self.repo.list_by_job(
            job_id,
        )

    def get_healing_stats(
        self,
        job_id: int,
    ):
        return self.repo.get_healing_stats(
            job_id,
        )

    def list_run_logs(
        self,
        run_id: int,
    ):
        return self.repo.list_by_run(
            run_id,
        )

    def list_runs(
        self,
        job_id: int,
    ):
        return self.repo.list_runs_by_job(
            job_id,
        )
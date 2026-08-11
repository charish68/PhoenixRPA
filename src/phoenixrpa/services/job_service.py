from sqlalchemy.orm import Session

from phoenixrpa.repositories.job_repository import JobRepository


class JobService:
    def __init__(self, db: Session):
        self.repo = JobRepository(db)

    def create_job(
        self,
        name: str,
        target_site: str,
    ):
        return self.repo.create(name, target_site)

    def list_jobs(self):
        return self.repo.list()

    def get_job(self, job_id: int):
        return self.repo.get(job_id)

    def delete_job(self, job_id: int):
        return self.repo.delete(job_id)
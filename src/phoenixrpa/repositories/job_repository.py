from sqlalchemy.orm import Session

from phoenixrpa.models.job import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        target_site: str,
    ) -> Job:

        job = Job(
            name=name,
            target_site=target_site,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get(self, job_id: int):
        return self.db.get(Job, job_id)

    def list(self):
        return self.db.query(Job).order_by(Job.id.desc()).all()

    def update_status(
        self,
        job_id: int,
        status,
    ):
        job = self.get(job_id)

        if job is None:
            return None

        job.status = status

        self.db.commit()
        self.db.refresh(job)

        return job

    def delete(self, job_id: int):

        job = self.get(job_id)

        if job is None:
            return False

        self.db.delete(job)
        self.db.commit()

        return True
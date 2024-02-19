from datetime import datetime, timedelta


class AnflerQueue:

    def __init__(self, user, service):
        self.user = user
        self.service = service

    def finished(self, job_id):
        jobs = self.service.select().where(self.service.job_id == job_id)
        if len(jobs) > 0:
            for job in jobs:
                return bool(job.finished)

    def exists_user(self, cuit):
        exists = self.user.select().where(self.user.user_cuit == cuit)
        return bool(len(exists) == 1)

    def insert_user_or_create(self, cuit):
        if not self.exists_user(cuit):
            self.user.create(user_cuit=cuit).save()

    def register(self, service_name, job_id, user):
        self.insert_user_or_create(user)
        service = self.service.create(user=user, job_id=job_id, service_name=service_name)
        service.save()

    def next_service(self, service_name, cuit):
        pendings = self.service.select(
        ).where(
            self.service.user == cuit,
            self.service.service_name == service_name
        ).order_by(
            self.service.created_date
        )
        services = list()
        for pending in pendings:
            created = pending.created_date
            time_elapsed = datetime.now() - created
            if time_elapsed < timedelta(seconds=300):
                services.append(pending)
            else:
                old_job = self.service.get(self.service.job_id == pending.job_id)
                old_job.delete_instance()
        return next(iter(services)).job_id

from celery import shared_task
from datetime import datetime

from db.repositories.temporary_token import TemporaryTokenRepository


class TemporaryTokenTasks:
    temp_token_repo = TemporaryTokenRepository()

    @shared_task
    def clear_expired_tokens():
        TemporaryTokenTasks.temp_token_repo.delete(filter=lambda Token: Token.expiration_date <= datetime.now())

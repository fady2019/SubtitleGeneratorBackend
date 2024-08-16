from celery import shared_task
from flask_mail import Mail, Message

from app_factory import AppFactorySingleton


mail = Mail(AppFactorySingleton.create())


class EmailTasks:
    @shared_task
    def send_email(subject: str, recipients: list[str], body: str = None, html: str = None):
        msg = Message(subject=subject, recipients=recipients, body=body, html=html)
        mail.send(msg)

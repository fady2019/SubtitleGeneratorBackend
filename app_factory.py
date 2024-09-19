from flask import Flask
from celery import Celery, Task
from flask_cors import CORS
import os

from helpers.date import format_date


def create_celery(app: Flask):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.import_name, task_cls=FlaskTask)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    celery.set_default()

    return celery


class AppFactorySingleton:
    __app: Flask | None = None

    @staticmethod
    def create():
        if AppFactorySingleton.__app != None:
            return AppFactorySingleton.__app

        app = Flask(__name__)

        app.jinja_env.filters["format_date"] = format_date

        app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
        app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_SENDER")
        app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "false") == "true"
        app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "true") == "true"
        app.config["CELERY_CONFIG"] = {
            "broker_url": os.getenv("CELERY_BROKER_URL"),
            "result_backend": os.getenv("CELERY_BACKEND"),
            "task_ignore_result": True,
            "broker_connection_retry_on_startup": True,
        }

        app.extensions["celery"] = create_celery(app)

        api_allowed_origin = os.getenv("API_ALLOWED_ORIGINS") or "*"
        api_origin_list = [origin.strip() for origin in api_allowed_origin.split(",")]

        CORS(
            app,
            resources={
                r"/api/*": {
                    "supports_credentials": True,
                    "origins": api_origin_list,
                    "expose_headers": ["Content-Disposition"],
                }
            },
        )

        AppFactorySingleton.__app = app

        return app

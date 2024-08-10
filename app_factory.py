from flask import Flask
from flask_cors import CORS
import os

from helpers.date import format_date


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

        api_allowed_origin = os.getenv("API_ALLOWED_ORIGINS") or "*"
        api_origin_list = [origin.strip() for origin in api_allowed_origin.split(",")]

        CORS(
            app,
            resources={r"/api/*": {"supports_credentials": True, "origins": api_origin_list}},
        )

        AppFactorySingleton.__app = app

        return app

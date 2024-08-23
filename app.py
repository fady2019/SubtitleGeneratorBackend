from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import inspect, os

load_dotenv()

import db.entities.user as _
import db.entities.temporary_token as _
import db.entities.subtitle as _
import db.entities.segment as _

import celery_tasks.temporary_tokens as _
from routes.api import api_blueprint
from app_factory import AppFactorySingleton
from decorators.errors.app_error_handler import app_error_handler
from swagger import config_swagger


app = AppFactorySingleton.create()
celery: Celery = app.extensions["celery"]


celery.conf.beat_schedule = {
    "clear-expired-tokens": {
        "task": "celery_tasks.temporary_tokens.clear_expired_tokens",
        "schedule": crontab(minute=0, hour=os.getenv("TEMP_TOKEN_CLEANING_CRONJOB_HOUR", "*/6")),
    },
}


app.register_blueprint(api_blueprint)
config_swagger(app)


# wrap all custom endpoint function with a decorator that handles the app errors
# this app error handler, handles all errors even ones which happen before calling the endpoint functions
for rule in app.url_map.iter_rules():
    func = app.view_functions[rule.endpoint]

    # check if the endpoint function is a custom not built-in
    if "site-packages" not in inspect.getfile(func):
        app.view_functions[rule.endpoint] = app_error_handler(func)


if __name__ == "__main__":
    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = os.getenv("SERVER_PORT")
    SERVER_DEBUG = os.getenv("SERVER_DEBUG", "true").lower() == "true"

    app.run(debug=SERVER_DEBUG, host=SERVER_HOST, port=SERVER_PORT)

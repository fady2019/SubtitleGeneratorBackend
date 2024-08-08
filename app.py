from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import inspect, os

load_dotenv()

from routes.api import api_blueprint
from decorators.errors.app_error_handler import app_error_handler
from swagger import config_swagger


API_ALLOWED_ORIGIN = os.getenv("API_ALLOWED_ORIGINS") or "*"
API_ORIGIN_LIST = [origin.strip() for origin in API_ALLOWED_ORIGIN.split(",")]


app = Flask(__name__)

CORS(
    app,
    resources={r"/api/*": {"supports_credentials": True, "origins": API_ORIGIN_LIST}},
)

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

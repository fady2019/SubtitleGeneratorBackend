from dotenv import load_dotenv
import inspect, os

load_dotenv()

from app import create_app
from decorators.errors.app_error_handler import app_error_handler
from swagger import config_swagger


app = create_app()
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
    SERVER_POST = os.getenv("SERVER_POST")

    app.run(debug=True, host=SERVER_HOST, port=SERVER_POST)

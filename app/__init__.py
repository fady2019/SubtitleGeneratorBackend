from flask import Flask, Blueprint
from flask_cors import CORS
import os


def create_app():
    from .auth.routes import auth_blueprint

    app = Flask(__name__)

    api_allowed_origin = os.getenv("API_ALLOWED_ORIGINS") or "*"
    api_origin_list = [origin.strip() for origin in api_allowed_origin.split(",")]

    CORS(
        app,
        resources={r"/api/*": {"supports_credentials": True, "origins": api_origin_list}},
    )

    api_blueprint = Blueprint("api", __name__, url_prefix="/api")

    api_blueprint.register_blueprint(auth_blueprint)

    app.register_blueprint(api_blueprint)

    return app

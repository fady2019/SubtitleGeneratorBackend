from flask import Blueprint

from routes.auth import auth_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


api_blueprint.register_blueprint(auth_blueprint)

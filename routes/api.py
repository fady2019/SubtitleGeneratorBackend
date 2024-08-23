from flask import Blueprint

from routes.auth import auth_blueprint
from routes.subtitles.subtitles import subtitles_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


api_blueprint.register_blueprint(auth_blueprint)
api_blueprint.register_blueprint(subtitles_blueprint)

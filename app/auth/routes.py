from flask import Blueprint, request, jsonify

from services.auth import AuthService
from validation.auth import singup_validator
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestJson
from decorators.security.jwt import sign_token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/sign-up", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=singup_validator)
@sign_token
def signup():
    user_data = AuthService.signup(request.json)
    return jsonify(user_data)

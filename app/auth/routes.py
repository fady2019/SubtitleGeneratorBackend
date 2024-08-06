from flask import Blueprint, request, g, jsonify

from services.auth import AuthService
from validation.auth import singup_validator, login_validator
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestJson
from decorators.security.jwt import sign_token, validate_token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/sign-up", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=singup_validator)
@sign_token
def signup():
    user_data = AuthService.signup(request.json)
    return jsonify(user_data)


@auth_blueprint.route("/login", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=login_validator)
@sign_token
def login():
    user_date = AuthService.login(request.json)
    return jsonify(user_date)


@auth_blueprint.route("/auto-login", methods=["POST"])
@validate_token(ignore_invalid_token=True)
def auto_login():
    user_id = g.get("user_id")

    if not user_id:
        return jsonify()

    user_data = AuthService.auto_login(user_id)
    return jsonify(user_data)

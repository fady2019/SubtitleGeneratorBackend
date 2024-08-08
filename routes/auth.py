from flask import Blueprint, request, g, jsonify

from services.auth import AuthService
from validation.auth import singup_validator, login_validator, change_password_validator
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestJson
from decorators.security.auth_token import sign_token, validate_token, unsign_token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

auth_service = AuthService()


@auth_blueprint.route("/sign-up", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=singup_validator)
@sign_token(get_payload=lambda res: {"id": res.json["id"]})
def signup():
    user_data = auth_service.signup(request.json)
    return jsonify(user_data)


@auth_blueprint.route("/login", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=login_validator)
@sign_token(get_payload=lambda res: {"id": res.json["id"]})
def login():
    user_date = auth_service.login(request.json)
    return jsonify(user_date)


@auth_blueprint.route("/auto-login")
@validate_token(ignore_invalid_token=True)
@unsign_token(only_if=lambda res: not res.json)  # clear the cookie of the token if no response (invalid token)
def auto_login():
    user_data = g.get("user")
    return jsonify(user_data)


@auth_blueprint.route("/logout")
@unsign_token()
def logout():
    return jsonify()


@auth_blueprint.route("/change-password", methods=["PUT"])
@validate_token()
@input_validator(input_source=RequestJson(), validator=change_password_validator)
def change_password():
    user = g.get("user", {})
    user_id = user.get("id", "")
    auth_service.change_password(user_id, data=request.json)
    return jsonify()

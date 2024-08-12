from flask import Blueprint, request, g, jsonify

from services.auth import AuthService
from validation.auth import (
    singup_validator,
    login_validator,
    change_password_validator,
    request_password_reset_validator,
    password_reset_validator,
    request_email_verification_validator,
    email_verification_validator,
)
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestJson, RequestViewArgs
from decorators.security.auth_token import sign_token, validate_token, unsign_token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

auth_service = AuthService()


@auth_blueprint.route("/sign-up", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=singup_validator)
def signup():
    auth_service.signup(request.json)
    return jsonify()


@auth_blueprint.route("/login", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=login_validator)
@sign_token(get_payload=lambda res: {"user_id": res.json["id"]} if (res.json or {})["id"] else None)
def login():
    user_data = auth_service.login(request.json)
    return jsonify(user_data)


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


@auth_blueprint.route("/request-password-reset", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=request_password_reset_validator)
def request_password_reset():
    auth_service.request_password_reset(request.json["email"])
    return jsonify()


@auth_blueprint.route("/reset-password", methods=["POST"])
@input_validator(input_source=RequestJson(), validator=password_reset_validator)
def reset_password():
    auth_service.reset_password(request.json)
    return jsonify()


@auth_blueprint.route("/request-email-verification/<user_id>")
@input_validator(input_source=RequestViewArgs(), validator=request_email_verification_validator)
def request_email_verification(user_id: str):
    auth_service.request_email_verification(user_id)
    return jsonify()


@auth_blueprint.route("/verify-email/<token>")
@input_validator(input_source=RequestViewArgs(), validator=email_verification_validator)
def verify_email(token: str):
    auth_service.verify_email(token)
    return jsonify()

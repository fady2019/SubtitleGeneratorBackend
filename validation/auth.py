from voluptuous import Schema, All, Invalid

from validation.shared import validator_executor
from validation.validators import (
    required,
    valid_string,
    valid_uuid,
    name_validator,
    username_validator,
    email_validator,
    password_validator,
)
from validation.transformers import trim


SignUpValidatorSchema = Schema(
    {
        required("first_name", "first name"): name_validator("first name"),
        required("last_name", "last name"): name_validator("last name"),
        required("username", "username"): username_validator("username"),
        required("email", "email"): email_validator("email"),
        required("password", "password"): password_validator("password"),
    },
)

LoginValidatorSchema = Schema(
    {
        required("username_or_email", "username/email"): All(valid_string("username/email"), trim),
        required("password", "password"): valid_string("password"),
    }
)


def different_current_and_new_passwords(data):
    if data["current_password"] == data["new_password"]:
        raise Invalid("the new password must be different from the current password")

    return data


ChangePasswordValidatorSchema = All(
    Schema(
        {
            required("current_password", "current password"): valid_string("current password"),
            required("new_password", "new password"): password_validator("new password"),
        },
    ),
    different_current_and_new_passwords,
)

RequestPasswordResetValidatorSchema = Schema(
    {
        required("email", "email"): All(valid_string("email"), trim),
    },
)

PasswordResetValidatorSchema = Schema(
    {
        required("new_password", "new password"): password_validator("new password"),
        required("token", "token"): valid_string("token"),
    },
)

RequestEmailVerificationValidatorSchema = Schema(
    {
        required("user_id", "user id"): All(valid_string("user id"), valid_uuid("user id")),
    },
)

EmailVerificationValidatorSchema = Schema(
    {
        required("token", "token"): valid_string("token"),
    },
)


def singup_validator(data):
    validator_executor(SignUpValidatorSchema, data)


def login_validator(data):
    validator_executor(LoginValidatorSchema, data)


def change_password_validator(data):
    validator_executor(ChangePasswordValidatorSchema, data)


def request_password_reset_validator(data):
    validator_executor(RequestPasswordResetValidatorSchema, data)


def password_reset_validator(data):
    validator_executor(PasswordResetValidatorSchema, data)


def request_email_verification_validator(data):
    validator_executor(RequestEmailVerificationValidatorSchema, data)


def email_verification_validator(data):
    validator_executor(EmailVerificationValidatorSchema, data)

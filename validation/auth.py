from voluptuous import Schema, All, Coerce, Required, Email, Length, Invalid
import regex as re

from validation.shared import CustomInvalid, validator_executor
from validation.transformers import trim
from services.user import UserService


def valid_name(field_placeholder: str):
    def validator(name: str):
        if not bool(re.match(r"^[\p{L} ]+$", name)):
            raise Invalid(f"invalid {field_placeholder}, it should only contain letters or/and space")

        return name

    return validator


def valid_username(field_placeholder: str):
    def validator(username: str):
        if not bool(re.match(r"^[a-zA-Z0-9_]+$", username)):
            raise Invalid(f"invalid {field_placeholder}, it should only contain english letters, digits or/and underscore")

        return username

    return validator


def unique_username(field_placeholder: str):
    def validator(username: str):
        if UserService.find_first_by(UserService.username_filter(username)) != None:
            raise CustomInvalid(message=f"the {field_placeholder} should be unique", status_code=409)

        return username

    return validator


def valid_email(field_placeholder: str):
    def validator(email: str):
        try:
            Email()(email)
        except:
            raise Invalid(f"invalid {field_placeholder}")

        return email

    return validator


def unique_email(field_placeholder: str):
    def validator(email: str):
        if UserService.find_first_by(UserService.email_filter(email)) != None:
            raise CustomInvalid(message=f"the {field_placeholder} should be unique", status_code=409)

        return email

    return validator


def valid_password(field_placeholder: str):
    def validator(password: str):
        required_chars_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W]).+$"

        if not re.search(required_chars_pattern, password):
            raise Invalid(
                f"the {field_placeholder} must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
            )

        allowed_chars_pattern = r"^[A-Za-z\d!\W]+$"

        if not re.match(allowed_chars_pattern, password):
            raise Invalid(
                f"the {field_placeholder} must contain only uppercase letters, lowercase letters, digits, and special characters"
            )

        return password

    return validator


SignUpValidatorSchema = Schema(
    {
        Required("first_name", msg="the first name is required"): All(
            Coerce(str, msg="the first name should be string"),
            Length(min=2, max=30, msg="the first name should be between 2 and 30 characters"),
            trim,
            valid_name("first name"),
        ),
        Required("last_name", msg="the last name is required"): All(
            Coerce(str, msg="the first name should be string"),
            Length(min=2, max=30, msg="the last name should be between 2 and 30 characters"),
            trim,
            valid_name("last name"),
        ),
        Required("username", msg="the username is required"): All(
            Coerce(str, msg="the username should be string"),
            Length(min=3, max=25, msg="the username should be between 3 and 25 characters"),
            trim,
            valid_username("username"),
            unique_username("username"),
        ),
        Required("email", msg="the email is required"): All(
            Coerce(str, msg="the email should be string"),
            trim,
            valid_email("email"),
            unique_email("email"),
        ),
        Required("password"): All(
            Coerce(str, msg="the password should be string"),
            Length(min=8, max=32, msg="the password should be between 8 and 32 characters"),
            valid_password("password"),
        ),
    },
)

LoginValidatorSchema = Schema(
    {
        Required("username_or_email", msg="the username/email is required"): All(
            Coerce(str, msg="the username/email should be string"),
            trim,
        ),
        Required("password", msg="the password is required"): Coerce(str, msg="the password should be string"),
    }
)

ChangePasswordValidatorSchema = Schema(
    {
        Required("current_password", msg="the current password is required"): All(
            Coerce(str, msg="the current password should be string"),
            trim,
        ),
        Required("new_password", msg="the new password is required"): All(
            Coerce(str, msg="the new password should be string"),
            Length(min=8, max=32, msg="the new password should be between 8 and 32 characters"),
            valid_password("new password"),
        ),
    }
)


def singup_validator(data):
    validator_executor(SignUpValidatorSchema, data)


def login_validator(data):
    validator_executor(LoginValidatorSchema, data)


def change_password_validator(data):
    validator_executor(ChangePasswordValidatorSchema, data)

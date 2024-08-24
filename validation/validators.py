from voluptuous import Coerce, All, Required, Email, Length, Invalid
from werkzeug.datastructures import FileStorage
from uuid import UUID
import regex as re


from validation.shared import CustomInvalid
from validation.transformers import trim
from db.repositories.user import UserRepository


user_repo = UserRepository()


def required(field_name: str, field_placeholder: str, msg: str = None):
    return Required(field_name, msg=msg or f"the {field_placeholder} is required")


def valid_string(field_placeholder: str, msg: str = None):
    return Coerce(str, msg=msg or f"the {field_placeholder} should be string")


def valid_int(field_placeholder: str, msg: str = None):
    return Coerce(int, msg=msg or f"the {field_placeholder} should be integer")


def valid_length(field_placeholder: str, min: int = None, max: int = None, msg: str = None):
    return Length(min=min, max=max, msg=msg or f"the {field_placeholder} should be between {min} and {max} characters")


def not_empty(field_placeholder: str):
    def validator(value: str):
        if not str(value.strip()):
            raise Invalid(f"the {field_placeholder} shouldn't be empty")

        return value

    return validator


def positive_num(field_placeholder: str):
    def validator(value: str):
        if float(value) <= 0:
            raise Invalid(f"the {field_placeholder} should be a positive number")

        return value

    return validator


def valid_file(field_placeholder: str, supported_mimetypes: list[str] = []):
    def validator(value):
        if not isinstance(value, FileStorage):
            raise Invalid(f"the {field_placeholder} should be a file")

        for mimetype in supported_mimetypes:
            if re.match(mimetype, value.mimetype):
                return value

        if len(supported_mimetypes) > 0:
            raise Invalid(f"unsupported file type. only support {', '.join(set(supported_mimetypes))}")

        return value

    return validator


def valid_name(field_placeholder: str):
    def validator(name: str):
        if not bool(re.match(r"^[\p{L} ]+$", name)):
            raise Invalid(f"invalid {field_placeholder}, it should only contain letters or/and space")

        return name

    return validator


def valid_username(field_placeholder: str):
    def validator(username: str):
        if not bool(re.match(r"^\w+$", username)):
            raise Invalid(f"invalid {field_placeholder}, it should only contain english letters, digits or/and underscore")

        if not bool(re.match(r"^[a-zA-Z].*$", username)):
            raise Invalid(f"invalid {field_placeholder}, it should start with english letters")

        return username

    return validator


def unique_username(field_placeholder: str):
    def validator(username: str):
        if user_repo.find(filter=lambda User: User.username.ilike(username)):
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
        if user_repo.find(filter=lambda User: User.email.ilike(email)):
            raise CustomInvalid(message=f"the {field_placeholder} should be unique", status_code=409)

        return email

    return validator


def valid_password(field_placeholder: str):
    def validator(password: str):
        required_chars_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W]).+$"

        if not re.search(required_chars_pattern, password):
            raise Invalid(
                f"invalid {field_placeholder}, it should contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
            )

        allowed_chars_pattern = r"^[A-Za-z\d!\W]+$"

        if not re.match(allowed_chars_pattern, password):
            raise Invalid(
                f"invalid {field_placeholder}, it should contain only uppercase letters, lowercase letters, digits, and special characters"
            )

        return password

    return validator


def valid_uuid(field_placeholder: str):
    def validator(value: str):
        try:
            UUID(value)
        except:
            raise Invalid(f"invalid {field_placeholder}")

    return validator


def valid_subtitle_title(field_placeholder: str):
    def validator(value: str):
        if not bool(re.match(r"^[\w. -]+$", value)):
            raise Invalid(
                f"invalid {field_placeholder}, it should only contain letters, numbers, underscores, periods or/and hyphens"
            )

    return validator


#
#
#
#
#


# USER INFO VALIDATORS
def name_validator(field_placeholder: str):
    return All(
        valid_string(field_placeholder),
        trim,
        valid_length(field_placeholder, min=2, max=30),
        valid_name(field_placeholder),
    )


def username_validator(field_placeholder: str):
    return All(
        valid_string(field_placeholder),
        trim,
        valid_length(field_placeholder, min=3, max=25),
        valid_username(field_placeholder),
        unique_username(field_placeholder),
    )


def email_validator(field_placeholder: str):
    return All(
        valid_string(field_placeholder),
        trim,
        valid_email(field_placeholder),
        unique_email(field_placeholder),
    )


def password_validator(field_placeholder: str):
    return All(
        valid_string(field_placeholder),
        valid_length(field_placeholder, min=8, max=32),
        valid_password(field_placeholder),
    )


# SUBTITLE INFO VALIDATORS
def subtitle_title_validator(field_placeholder: str):
    return All(
        valid_string(field_placeholder),
        valid_length(field_placeholder, 1, 100),
        valid_subtitle_title(field_placeholder),
    )

from voluptuous import Schema, Optional, All

from validation.shared import validator_executor
from validation.validators import valid_int, positive_num


PaginationSchema = Schema(
    {
        Optional("page"): All(valid_int("page"), positive_num("page")),
        Optional("items_per_page"): All(valid_int("items per page"), positive_num("items per page")),
    }
)


def pagination_validator(data):
    validator_executor(PaginationSchema, data)

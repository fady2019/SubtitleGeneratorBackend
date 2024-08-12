from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, DeclarativeMeta
from typing import Callable, TypeVar, TypedDict


TEntity = TypeVar("Entity", bound=type[DeclarativeMeta])
TTransactionCbReturn = TypeVar("TransactionCbReturn")
TFilter = Callable[[type[TEntity]], ColumnElement[bool]]


class MethodOptions(TypedDict):
    session: Session | None


class FindWithErrorOptions(MethodOptions):
    error_msg: str | None


def set_default_method_options(options: MethodOptions) -> MethodOptions:
    default = {"session": None}

    if options != None:
        default.update(options)

    return default


def set_default_find_with_error_options(options: FindWithErrorOptions) -> FindWithErrorOptions:
    default = {"session": None, "error_msg": ""}

    if options != None:
        default.update(options)

    return default

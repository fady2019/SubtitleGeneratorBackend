from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, DeclarativeMeta
from typing import Callable, TypeVar, TypedDict


TEntity = TypeVar("Entity", bound=type[DeclarativeMeta])
TTransactionCbReturn = TypeVar("TransactionCbReturn")
TFilter = Callable[[type[TEntity]], ColumnElement[bool]]


class MethodOptions(TypedDict):
    session: Session | None


TOptions = TypeVar("Options", bound=MethodOptions)


def update_options(options: TOptions, get_default: Callable[[], TOptions]) -> TOptions:
    default = get_default() or {}

    if options != None:
        default.update(options)

    return default

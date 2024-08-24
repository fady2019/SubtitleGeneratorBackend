from sqlalchemy import ColumnElement, UnaryExpression
from sqlalchemy.orm import Session, DeclarativeMeta
from typing import Callable, TypeVar, TypedDict, Union, Sequence


TEntity = TypeVar("Entity", bound=type[DeclarativeMeta])
TTransactionCbReturn = TypeVar("TransactionCbReturn")
TFilter = Callable[[type[TEntity]], ColumnElement[bool]]
TOrderBy = Callable[[type[TEntity]], Union[ColumnElement, UnaryExpression, Sequence[Union[ColumnElement, UnaryExpression]]]]


class MethodOptions(TypedDict):
    session: Session | None


TOptions = TypeVar("Options", bound=MethodOptions)


def update_options(options: TOptions, get_default: Callable[[], TOptions]) -> TOptions:
    default = get_default() or {}

    if options != None:
        default.update({k: v for k, v in options.items() if v is not None})

    return default

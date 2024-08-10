from sqlalchemy import BinaryExpression, ColumnElement
from sqlalchemy.orm import Session, DeclarativeMeta
from typing import Callable, TypeVar, TypedDict

from db.dtos.dto import DTO, UpdateDTO


TFilter = Callable[..., Callable[[], BinaryExpression[bool] | ColumnElement[bool]]]
TDto = TypeVar("Dto", bound=DTO)
TUpdateDto = TypeVar("UpdateDto", bound=UpdateDTO)
TEntity = TypeVar("Entity", bound=DeclarativeMeta)
TTransactionCbReturn = TypeVar("TransactionCbReturn")


class MethodOptions(TypedDict):
    session: Session | None


class FindWithErrorOptions(MethodOptions):
    error_msg: str | None


def set_default_method_options(options: MethodOptions) -> MethodOptions:
    default = {"session": None}
    default.update(options)
    return default


def set_default_find_with_error_options(options: FindWithErrorOptions) -> FindWithErrorOptions:
    default = {"session": None, "error_msg": ""}
    default.update(options)
    return default

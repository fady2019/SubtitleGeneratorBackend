import typing
from sqlalchemy import BinaryExpression, ColumnElement, or_


TFilter = typing.Callable[..., typing.Callable[[], BinaryExpression[bool] | ColumnElement[bool]]]


class Service:
    @staticmethod
    def or_filter(*filters: tuple[TFilter]):
        return lambda: or_(*[filter() for filter in filters])

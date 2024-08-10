from abc import ABC
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from typing import Callable

from db.repositories.repository.repository_typing import TFilter, TTransactionCbReturn
from db.db_config import create_session


class Repository(ABC):
    def or_filter(self, *filters: tuple[TFilter]):
        return lambda: or_(*[filter() for filter in filters])

    def and_filter(self, *filters: tuple[TFilter]):
        return lambda: and_(*[filter() for filter in filters])

    def start_transaction(self, callback: Callable[[Session], TTransactionCbReturn], default_session: Session | None = None):
        """
        Description

        Args:
            callback (Callable[[Session], T]):
                a callback that receive the transaction session.

            default_session (Session, optional):
                a session that will be managed by you, if no session is passed a new session will be created and managed for you.

        Returns:
            T: it returns what the "callback" returns
        """

        if default_session != None:
            return callback(default_session)

        session = create_session()

        try:
            res = callback(session)
            session.commit()
            return res
        except Exception as err:
            session.rollback()
            raise err
        finally:
            session.close()

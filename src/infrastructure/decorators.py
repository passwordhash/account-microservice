from functools import wraps

from psycopg2._psycopg import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.exceptions import DuplicateEmailError, RepositoryError


def handle_session_errors(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self.db_session as session:
            try:
                return method(self, session, *args, **kwargs)
            except IntegrityError as e:
                raise DuplicateEmailError("Unique constraint violation.") from e
            except SQLAlchemyError as e:
                raise RepositoryError(
                    "Error occurred while executing method") from e

    return wrapper

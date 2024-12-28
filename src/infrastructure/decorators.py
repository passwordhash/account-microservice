import logging
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.infrastructure.exceptions import DuplicateError, RepositoryError

logger = logging.getLogger(__name__)


def handle_session_errors(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self.db_session as session:
            try:
                return method(self, session, *args, **kwargs)
            except IntegrityError as e:
                raise DuplicateError("Unique constraint violation.") from e
            except SQLAlchemyError as e:
                raise RepositoryError(
                    f"Error occurred while executing method: {e}") from e
            except Exception as e:
                logger.error(f"Unexpected error occurred: {e}")
                raise RepositoryError(
                    f"Unexpected error occurred: {e}") from e

    return wrapper

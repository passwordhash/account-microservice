from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from src.core.account import Account
from src.infrastructure.account.converter import model_to_domain, \
    domain_to_model
from src.infrastructure.account.model import AccountModel
from src.infrastructure.database import SessionLocal
from src.infrastructure.exceptions import DuplicateEmailError, RepositoryError


class AccountRepository:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session or SessionLocal()

    def save(self, account: Account) -> str:
        model = domain_to_model(account)
        with self.db_session as session:
            try:
                session.add(model)
                session.commit()
                return model.uuid
            except IntegrityError as e:
                raise DuplicateEmailError(
                    "Аккаунт с таким email уже существует.") from e
            except SQLAlchemyError as e:
                raise RepositoryError(
                    "Произошла ошибка при сохранении аккаунта.") from e

    def get_all(self) -> List[Account]:
        try:
            with self.db_session as session:
                return [model_to_domain(model) for model in
                        session.query(AccountModel).all()]
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Ошибка при получении всех аккаунтов.") from e

    def find_by_uuid(self, uuid: str) -> Optional[Account]:
        with self.db_session as session:
            try:
                model = session.get(AccountModel, uuid)
                if model is None:
                    return None
                return model_to_domain(model)
            except SQLAlchemyError as e:
                raise RepositoryError(
                    f"Ошибка при поиске аккаунта с UUID {uuid}.") from e

    def find_by_email(self, email: str) -> Optional[Account]:
        with self.db_session as session:
            try:
                model = session.get(AccountModel, email)
                if model is None:
                    return None
                return model_to_domain(model)
            except SQLAlchemyError as e:
                raise RepositoryError(
                    f"Ошибка при поиске аккаунта с Email {email}.") from e

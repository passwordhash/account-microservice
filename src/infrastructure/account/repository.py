from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from src.core.account import Account
from src.infrastructure.account.model import AccountModel
from src.infrastructure.database import SessionLocal


class AccountSaveError(Exception):
    pass


class AccountRepository:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session or SessionLocal()

    def save(self, account: Account) -> str:
        db_account = AccountModel(
            email=account.email,
            hashed_password=account.hashed_password
        )

        with self.db_session as session:
            try:
                session.add(db_account)
                session.commit()
                session.refresh(db_account)
                return db_account.uuid
            except IntegrityError as e:
                session.rollback()
                raise AccountSaveError(
                    "Аккаунт с таким email уже существует.") from e
            except SQLAlchemyError as e:
                session.rollback()
                raise AccountSaveError(
                    "Произошла ошибка при сохранении аккаунта.") from e

        return db_account.uuid

    def get_all(self):
        with self.db_session as session:
            accounts_data = session.query(AccountModel).all()
            accounts = [
                Account(
                    uuid=account.uuid,
                    email=account.email,
                    hashed_password=account.hashed_password,
                    is_verified=account.is_verified,
                    created_at=account.created_at
                )
                for account in accounts_data
            ]
            return accounts

    # def find_by_email(self, email: str):
    #     return self.db_session.query(AccountModel).filter(AccountModel.email == email).first()

    def find_by_uuid(self, uuid: str):
        return self.db_session.query(AccountModel).get(uuid)

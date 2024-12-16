from typing import Optional, List

from sqlalchemy.orm import Session

from src.core.account import Account
from src.infrastructure.account.converter import model_to_domain, \
    domain_to_model
from src.infrastructure.account.model import AccountModel
from src.infrastructure.database import SessionLocal
from src.infrastructure.decorators import handle_session_errors


class AccountRepository:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session or SessionLocal()

    @handle_session_errors
    def save(self, session, account: Account) -> str:
        model = domain_to_model(account)
        session.add(model)
        session.commit()
        return model.uuid

    @handle_session_errors
    def get_all(self, session) -> List[Account]:
        return [model_to_domain(model) for model in
                session.query(AccountModel).all()]

    @handle_session_errors
    def find_by_uuid(self, session, uuid: str) -> Optional[Account]:
        model = session.get(AccountModel, uuid)
        if model is None:
            return None
        return model_to_domain(model)

    @handle_session_errors
    def find_by_email(self, session, email: str) -> Optional[Account]:
        model = session.query(AccountModel).filter_by(
            email=email).first()
        if model is None:
            return None
        return model_to_domain(model)

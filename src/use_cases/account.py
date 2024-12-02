import logging
from uuid import uuid4

from src.core.account import Account, AccountCreate
from src.core.converter import account_to_pb
from src.infrastructure.account.repository import AccountRepository

logger = logging.getLogger(__name__)


class AccountUseCase:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def get_all(self):
        """Возвращает список всех аккаунтов в виде списка pb.Account."""
        db_accounts = self.account_repository.get_all()
        pb_accounts = list(map(lambda x: account_to_pb(x), db_accounts))
        return pb_accounts

    def register(self, req: AccountCreate) -> str:
        """Регистрация аккаунта. Возвращает uuid созданного аккаунта."""
        uuid = str(uuid4())
        hashed_password = self.hash(req.password)

        candidate = Account(uuid=uuid, email=req.email, hashed_password=hashed_password)

        uuid = self.account_repository.save(candidate)

        return uuid

    @staticmethod
    def hash(password):
        """Хеширование пароля."""
        import hashlib
        # TODO: add secret
        return hashlib.sha256(password.encode()).hexdigest()

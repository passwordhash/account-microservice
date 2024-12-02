import logging
from dataclasses import asdict
from datetime import timedelta, datetime
from typing import Tuple

import jwt
from uuid import uuid4

from src.core.account import Account, AccountCreate, AccountLogin
from src.core.config import Config
from src.core.consts import DEFAULT_JWT_EXPIRES_IN, JWT_TOKEN_ALG
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

    def register(self, req: AccountCreate) -> tuple[str, str]:
        """Регистрация аккаунта. Возвращает JWT Token"""
        uuid = str(uuid4())
        hashed_password = self.hash(req.password)

        candidate = Account(uuid=uuid, email=req.email,
                            hashed_password=hashed_password)

        uuid = self.account_repository.save(candidate)

        jwt_token = self._create_jwt_token(uuid)

        return uuid, jwt_token

    def login(self, req: AccountLogin) -> str:
        """Аутентификация пользователя. Возвращает JWT Token"""
        # TODO: decrypt password

        account = self.account_repository.find_by_email(req.email)
        if not account:
            raise ValueError("Account not found")

        if self.hash(req.encrypted_password) != account.hashed_password:
            raise ValueError("Invalid password")

        return self._create_jwt_token(account.uuid)

    @staticmethod
    def _create_jwt_token(uuid: str,
                          expires_in: int = DEFAULT_JWT_EXPIRES_IN) -> str:
        """Создание JWT токена."""
        payload = {"uuid": uuid,
                   "exp": datetime.utcnow() + timedelta(minutes=expires_in),
                   "iat": datetime.utcnow()
                   }
        token = jwt.encode(payload, Config.JWT_SECRET.value,
                           algorithm=JWT_TOKEN_ALG)
        return token

    @staticmethod
    def _decode_jwt_token(token: str) -> str:
        """Декодирование JWT токена."""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET.value,
                                 algorithms=[JWT_TOKEN_ALG])
            return payload["uuid"]
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    @staticmethod
    def hash(password):
        """Хеширование пароля."""
        import hashlib
        # TODO: add secret
        return hashlib.sha256(password.encode()).hexdigest()

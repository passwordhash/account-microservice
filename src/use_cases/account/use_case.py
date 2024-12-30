import base64
import logging
from datetime import timedelta, datetime
from uuid import uuid4

import jwt
from bcrypt import checkpw, hashpw, gensalt

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from src.core.account import Account, AccountCreate, AccountLogin
from src.core.config import config
from src.core.consts import DEFAULT_JWT_EXPIRES_IN, JWT_TOKEN_ALG
from src.infrastructure.account.repository import AccountRepository
from src.infrastructure.exceptions import RepositoryError, DuplicateError
from src.use_cases.account.converter import account_to_pb
from src.use_cases.exceptions import AccountError, EmailConflictError, \
    AccountNotFoundError, InvalidPasswordError, TokenExpiredError, \
    InvalidTokenError

logger = logging.getLogger(__name__)


class AccountUseCase:
    def __init__(self, account_repository: AccountRepository, jwt_secret: str,
                 jwt_expires_in: int):
        self.private_key = self.load_private_key()
        self.account_repository = account_repository
        self.jwt_secret = jwt_secret
        self.jwt_expires_in = jwt_expires_in

    def register(self, req: AccountCreate) -> tuple[str, str]:
        """
        Регистрация аккаунта. Возвращает UUID и JWT Token.
        """
        try:
            uuid = str(uuid4())
            decrtyped_password = self._decrypt_password(req.encrypted_password)

            hashed_password = self._hash(decrtyped_password)

            candidate = Account(uuid=uuid, email=req.email,
                                hashed_password=hashed_password)
            uuid = self.account_repository.save(candidate)

            jwt_token = self._create_jwt_token(uuid)

            logger.info(f"Account registered: {req.email}")
            return uuid, jwt_token
        except DuplicateError as e:
            raise EmailConflictError(f"Account with email {req.email} already "
                                     f"exists.") from e
        except (RepositoryError, Exception) as e:
            raise AccountError("Error while registering account") from e

    def login(self, req: AccountLogin) -> str:
        """Аутентификация пользователя. Возвращает JWT Token."""
        try:
            account = self.account_repository.find_by_email(req.email)
            if not account:
                logger.warning(f"Account with email {req.email} not found.")
                raise AccountNotFoundError("Account not found.")

            decrtyped_password = self._decrypt_password(req.encrypted_password)
            if not self._verify_password(decrtyped_password,
                                         account.hashed_password):
                logger.warning(
                    f"Incorrect password for account with email {req.email}")
                raise InvalidPasswordError("Invalid password.")

            jwt_token = self._create_jwt_token(account.uuid)
            logger.info(f"Account logged in: {req.email}")
            return jwt_token
        except (AccountNotFoundError, InvalidPasswordError) as e:
            raise e
        except Exception as e:
            raise AccountError("Error while logging in.") from e

    def verify_token(self, token: str) -> str:
        """Проверка JWT токена и пользователя. Возвращает UUID."""
        try:
            uuid = self._decode_jwt_token(token)
            user = self.account_repository.find_by_uuid(uuid)
            if not user:
                raise AccountNotFoundError("Account not found.")
            return uuid
        except (TokenExpiredError, InvalidTokenError) as e:
            raise e
        except Exception as e:
            raise AccountError("Error while verifying token.") from e

    @staticmethod
    def get_public_key() -> str:
        """Возвращает публичный ключ RSA ключ."""
        with open(config.get_public_key_path(), "r") as file:
            return file.read()

    def get_all(self):
        """Возвращает список всех аккаунтов в виде списка pb.Account."""
        try:
            db_accounts = self.account_repository.get_all()
            pb_accounts = list(map(lambda x: account_to_pb(x), db_accounts))
            return pb_accounts
        except (RepositoryError, Exception) as e:
            logger.error(f"Error while getting all accounts: {e}")
            raise AccountError("Error while getting all accounts") from e

    def _decrypt_password(self, encrypted_password: str) -> str:
        cipher = PKCS1_v1_5.new(self.private_key)
        decoded_password = base64.b64decode(encrypted_password)
        return cipher.decrypt(decoded_password, None).decode("utf-8")

    @staticmethod
    def load_private_key():
        with open(config.get_private_key_path(), "r") as file:
            return RSA.import_key(file.read())

    @staticmethod
    def _create_jwt_token(uuid: str,
                          expires_in: int = DEFAULT_JWT_EXPIRES_IN) -> str:
        """Создание JWT токена."""
        payload = {"uuid": uuid,
                   "exp": datetime.utcnow() + timedelta(minutes=expires_in),
                   "iat": datetime.utcnow()
                   }
        token = jwt.encode(payload, config.JWT_TOKEN_SECRET,
                           algorithm=JWT_TOKEN_ALG)
        return token

    @staticmethod
    def _decode_jwt_token(token: str) -> str:
        """Декодирование JWT токена."""
        try:
            payload = jwt.decode(token, config.JWT_TOKEN_SECRET,
                                 algorithms=[JWT_TOKEN_ALG])
            return payload["uuid"]
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredError("Token expired") from e
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError("Invalid token") from e

    @staticmethod
    def _hash(password: str) -> str:
        return hashpw(password.encode(), config.PASSWORD_SALT.encode()).decode()

    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode(), hashed_password.encode())

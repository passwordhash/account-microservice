class AccountError(Exception):
    pass


class EmailConflictError(AccountError):
    """Ошибка при попытке создать аккаунт с уже существующим email."""
    pass


class AccountNotFoundError(AccountError):
    pass


class InvalidPasswordError(AccountError):
    pass


class TokenError(AccountError):
    pass


class InvalidTokenError(TokenError):
    pass


class TokenExpiredError(TokenError):
    pass

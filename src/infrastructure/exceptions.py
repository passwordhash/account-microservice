class RepositoryError(Exception):
    """Базовое исключение для ошибок репозитория"""
    pass


class DuplicateError(RepositoryError):
    pass


class DatabaseSaveError(RepositoryError):
    pass

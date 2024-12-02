class RepositoryError(Exception):
    """Базовое исключение для ошибок репозитория."""
    pass


class DuplicateEmailError(RepositoryError):
    """Исключение при попытке добавить дублирующийся email."""
    pass


class DatabaseSaveError(RepositoryError):
    """Исключение при ошибке сохранения в базу данных."""
    pass

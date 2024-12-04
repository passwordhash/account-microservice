from src.core.account import Account
from src.infrastructure.account.model import AccountModel


def domain_to_model(account: Account) -> AccountModel:
    return AccountModel(
        email=account.email,
        hashed_password=account.hashed_password,
    )


def model_to_domain(account_model: AccountModel) -> Account:
    return Account(
        uuid=account_model.uuid,
        email=account_model.email,
        hashed_password=account_model.hashed_password,
        is_verified=account_model.is_verified,
        created_at=account_model.created_at
    )

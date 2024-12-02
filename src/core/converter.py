from src.core.account import Account
from src.interfaces.grpc import account_pb2 as pb


def account_to_pb(account: Account) -> pb.Account:
    return pb.Account(
        uuid=account.uuid,
        email=account.email,
        hashed_password=account.hashed_password,
        is_verified=account.is_verified,
        created_at=account.created_at
    )
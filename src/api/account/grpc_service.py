import grpc as grpc_mod

from src.core import config
from src.core.account import AccountCreate, AccountLogin
from src.core.config import Config
from src.core.consts import DEFAULT_JWT_EXPIRES_IN
from src.infrastructure.account.repository import AccountRepository
from src.infrastructure.database import SessionLocal
from src.interfaces.grpc import account_pb2 as pb, account_pb2_grpc as grpc
from src.use_cases.account.use_case import AccountUseCase


class AccountService(grpc.AccountServiceServicer):
    def __init__(self):
        self.account_use_case = AccountUseCase(
            account_repository=AccountRepository(db_session=SessionLocal()),
            jwt_secret=Config.JWT_SECRET.value,
            jwt_expires_in=DEFAULT_JWT_EXPIRES_IN
        )

    def Create(self, request: pb.CreateRequest, context):
        if request.email == "":
            context.set_code(grpc_mod.StatusCode.INVALID_ARGUMENT)
            context.set_details("email is required")
            return pb.CreateResponse()

        if request.encrypted_password == "":
            context.set_code(grpc_mod.StatusCode.INVALID_ARGUMENT)
            context.set_details("encrypted_password is required")
            return pb.CreateResponse()

        uuid, token = self.account_use_case.register(
            AccountCreate(email=request.email, password=request.encrypted_password)
        )

        return pb.CreateResponse(uuid=uuid, jwt_token=token)

    def Login(self, request: pb.LoginRequest, context):
        if request.email == "":
            context.set_code(grpc_mod.StatusCode.INVALID_ARGUMENT)
            context.set_code
            context.set_details("email is required")
            return pb.LoginResponse()

        if request.encrypted_password == "":
            context.set_code(grpc_mod.StatusCode.INVALID_ARGUMENT)
            context.set_details("password is required")
            return pb.LoginResponse()

        token = self.account_use_case.login(
            AccountLogin(email=request.email, encrypted_password=request.encrypted_password)
        )

        return pb.LoginResponse(jwt_token=token)

    def GetAll(self, request, context):
        accounts = self.account_use_case.get_all()
        return pb.GetAllResponse(accounts=accounts)

    def Get(self, request, context):
        pass

import grpc as grpc_mod

from src.core.account import AccountCreate
from src.infrastructure.account.repository import AccountRepository
from src.infrastructure.database import SessionLocal
from src.interfaces.grpc import account_pb2 as pb, account_pb2_grpc as grpc
from src.use_cases.account import AccountUseCase


class AccountService(grpc.AccountServiceServicer):
    def __init__(self):
        self.account_use_case = AccountUseCase(AccountRepository(SessionLocal()))

    def Create(self, request, context):
        if request.email == "":
            context.set_code(grpc_mod.StatusCode.INVALID_ARGUMENT)
            context.set_details("email is required")
            return pb.CreateResponse()

        if request.encrypted_password == "":
            context.set_code(grpc_mod.StatusCode.INVALID_ARGUMENT)
            context.set_details("password is required")
            return pb.CreateResponse()

        uuid, token = self.account_use_case.register(
            AccountCreate(email=request.email, password=request.encrypted_password)
        )

        return pb.CreateResponse(uuid=uuid, jwt_token=token)

    def GetAll(self, request, context):
        accounts = self.account_use_case.get_all()
        print(accounts)
        return pb.GetAllResponse(accounts=accounts)

    def Get(self, request, context):
        pass

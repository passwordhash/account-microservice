import grpc as grpc_mod

from src.core.account import AccountCreate, AccountLogin
from src.core.config import config
from src.core.consts import DEFAULT_JWT_EXPIRES_IN
from src.infrastructure.account.repository import AccountRepository
from src.infrastructure.database import SessionLocal
from src.interfaces.grpc import account_pb2 as pb, account_pb2_grpc as grpc
from src.api.account.responses import Responses, response, handle_error
from src.use_cases.account.use_case import AccountUseCase
from src.use_cases.exceptions import EmailConflictError, AccountNotFoundError


class AccountService(grpc.AccountServiceServicer):
    def __init__(self):
        self.account_use_case = AccountUseCase(
            account_repository=AccountRepository(db_session=SessionLocal()),
            jwt_secret=config.JWT_TOKEN_SECRET,
            jwt_expires_in=DEFAULT_JWT_EXPIRES_IN
        )

    def Signup(self, request: pb.CreateRequest, context):
        try:
            if request.email == "":
                response(context, grpc_mod.StatusCode.INVALID_ARGUMENT,
                         Responses.EMAIL_REQUIRED)
                return pb.CreateResponse()

            if request.encrypted_password == "":
                response(context, grpc_mod.StatusCode.INVALID_ARGUMENT,
                         Responses.PASSWORD_REQUIRED)
                return pb.CreateResponse()

            uuid, token = self.account_use_case.register(
                AccountCreate(email=request.email,
                              password=request.encrypted_password)
            )

            response(context, grpc_mod.StatusCode.OK, Responses.CREATE_OK)
            return pb.CreateResponse(uuid=uuid, jwt_token=token)
        except EmailConflictError as e:
            response(context, grpc_mod.StatusCode.ALREADY_EXISTS, str(e))
            return pb.CreateResponse
        except Exception as e:
            handle_error(context, e, Responses.CREATE_ERROR)
            return pb.CreateResponse()

    def Login(self, request: pb.LoginRequest, context):
        try:
            if request.email == "":
                response(context, grpc_mod.StatusCode.INVALID_ARGUMENT,
                         Responses.EMAIL_REQUIRED)
                return pb.LoginResponse()

            if request.encrypted_password == "":
                response(context, grpc_mod.StatusCode.INVALID_ARGUMENT,
                         Responses.PASSWORD_REQUIRED)
                return pb.LoginResponse()

            token = self.account_use_case.login(
                AccountLogin(email=request.email,
                             encrypted_password=request.encrypted_password)
            )

            response(context, grpc_mod.StatusCode.OK, Responses.LOGIN_OK)
            return pb.LoginResponse(jwt_token=token)
        except AccountNotFoundError as e:
            response(context, grpc_mod.StatusCode.NOT_FOUND, str(e))
            return pb.LoginResponse()
        except Exception as e:
            handle_error(context, e, Responses.LOGIN_ERROR)
            return pb.LoginResponse()

    def GetAll(self, request, context):
        try:
            accounts = self.account_use_case.get_all()
            return pb.GetAllResponse(accounts=accounts)
        except Exception as e:
            handle_error(context, e)
            return pb.GetAllResponse()

    def Get(self, request, context):
        pass

import logging

import grpc as grpc_mod

logger = logging.getLogger(__name__)


def response(context, code: grpc_mod.StatusCode, message: str):
    context.set_code(code)
    context.set_details(message)


def handle_error(context, error: Exception, message="An error occurred"):
    logger.error(f"{message}: {str(error.__context__)}")
    if isinstance(error, grpc_mod.RpcError):
        response(context, error.code(), error.details())
    else:
        response(context, grpc_mod.StatusCode.INTERNAL, message)


class Responses:
    """Account response messaages."""

    """Input validation messages."""
    EMAIL_REQUIRED = "email is required"
    PASSWORD_REQUIRED = "encrypted_password is required"

    """Success messages."""
    CREATE_OK = "account created successfully"
    LOGIN_OK = "account logged in successfully"

    """Error messages."""
    SIGN_UP_ERROR = "error during account creation"
    LOGIN_ERROR = "error during account login"

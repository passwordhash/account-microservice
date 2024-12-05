import grpc as grpc_mod


def response(context, code: grpc_mod.StatusCode, message: str):
    context.set_code(code)
    context.set_details(message)


def handle_error(context, error, default_message="An error occurred"):
    if isinstance(error, grpc_mod.RpcError):
        response(context, error.code(), error.details())
    else:
        response(context, grpc_mod.StatusCode.INTERNAL, default_message)


class Responses:
    """Account response messaages."""

    """Input validation messages."""
    EMAIL_REQUIRED = "email is required"
    PASSWORD_REQUIRED = "encrypted_password is required"

    """Success messages."""
    CREATE_OK = "account created successfully"
    LOGIN_OK = "account logged in successfully"

    """Error messages."""
    CREATE_ERROR = "error during account creation"
    LOGIN_ERROR = "error during account login"

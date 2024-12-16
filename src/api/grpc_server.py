import logging
from concurrent import futures
import grpc as grpc_mod

from src.api.account.grpc_service import AccountService
from src.infrastructure.database import init_db
from src.interfaces.grpc import account_pb2_grpc as grpc


def create_server():
    try:
        init_db()
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        exit(1)

    logging.info("Database initialized successfully")

    server = grpc_mod.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc.add_AccountServiceServicer_to_server(AccountService(), server)

    return server
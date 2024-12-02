import logging
from dotenv import load_dotenv


from src.api.grpc import create_server

logging.basicConfig(level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def serve():
    load_dotenv()
    server = create_server()
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("gRPC api started on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

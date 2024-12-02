import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")

    JWT_SECRET = os.getenv("JWT_TOKEN_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

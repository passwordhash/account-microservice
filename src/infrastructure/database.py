import logging

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.infrastructure"
# TODO: move to .env
POSTGRES_DATABASE_URL = ("postgresql://postgres:password@localhost:5432"
                         "/account-service")

engine = create_engine(POSTGRES_DATABASE_URL)
# engine = create_engine(POSTGRES_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    test_connection()
    from src.infrastructure.account.model import Base
    Base.metadata.create_all(bind=engine)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
    except Exception as e:
        raise e

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PASSWORD_SALT: str = Field(..., env="PASSWORD_SALT")
    JWT_TOKEN_SECRET: str = Field(..., env="JWT_TOKEN_SECRET")

    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    POSTGRES_DB: str = Field("account-service", env="POSTGRES_DB")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")

    RSA_KEYS_DIR: str = Field("./keys", env="RSA_KEYS_DIR", required=False)

    def get_postgres_db_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_public_key_path(self):
        return f"{self.RSA_KEYS_DIR}/public.pem"

    def get_private_key_path(self):
        return f"{self.RSA_KEYS_DIR}/private.pem"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()

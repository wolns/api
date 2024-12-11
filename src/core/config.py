from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    ENV: str = "prod"
    PROJECT_NAME: str = "wolns-API"

    backend_port: str

    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        extra = "allow"
        case_sensitive = False


class PostgresSettings(BaseSettings):
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@postgres:{self.postgres_port}/{self.postgres_db}"

    class Config:
        extra = "allow"


def get_postgres_settings():
    return PostgresSettings()


def get_settings():
    return Settings()

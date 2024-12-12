from pydantic.v1 import BaseSettings


class JWTSettings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24  # 1 day

    class Config:
        extra = "allow"


class TimezoneSettings(BaseSettings):
    tz: str

    class Config:
        extra = "allow"


class Settings(BaseSettings):
    ENV: str = "prod"
    PROJECT_NAME: str = "wolns-API"

    tz: str

    backend_port: str

    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_minutes: int

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


def get_timezone_settings():
    return TimezoneSettings()

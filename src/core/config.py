from pydantic.v1 import BaseSettings


class EnvSettings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "allow"


class SpotifySettings(EnvSettings):
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str


class YandexMusicSettings(EnvSettings):
    yandex_music_client_id: str
    yandex_music_client_secret: str
    yandex_music_redirect_uri: str


class JWTSettings(EnvSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24  # 1 day


class TimezoneSettings(EnvSettings):
    tz: str


class Settings(EnvSettings):
    ENV: str = "prod"
    PROJECT_NAME: str = "wolns-API"

    tz: str

    backend_port: str

    redis_port: str

    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_minutes: int

    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str

    yandex_music_client_id: str
    yandex_music_client_secret: str
    yandex_music_redirect_uri: str


class RedisSettings(EnvSettings):
    redis_port: str

    @property
    def redis_url(self) -> str:
        return f"redis://redis:{self.redis_port}/"

    @property
    def broker_url(self) -> str:
        return f"{self.redis_url}0"


class PostgresSettings(EnvSettings):
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @property
    def localhost_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@localhost:{self.postgres_port}/{self.postgres_db}"

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@postgres:{self.postgres_port}/{self.postgres_db}"


def get_postgres_settings():
    return PostgresSettings()


def get_settings():
    return Settings()


def get_timezone_settings():
    return TimezoneSettings()


def get_redis_settings():
    return RedisSettings()


def get_spotify_settings():
    return SpotifySettings()


def get_yandex_music_settings():
    return YandexMusicSettings()

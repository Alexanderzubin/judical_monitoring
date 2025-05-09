from pathlib import Path

from pydantic import AnyUrl, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / '.env'


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file=ENV_FILE, env_prefix='CELERY_')

    broker_url: AnyUrl = 'redis://localhost:6379/0'
    backend_url: AnyUrl = 'redis://localhost:6379/1'
    redbeat_redis_url: AnyUrl = 'redis://localhost:6379/2'


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file=ENV_FILE, env_prefix='DB_')

    engine: str = 'postgresql+psycopg2'
    host: str = 'localhost'
    port: int = 5432
    database: str = 'postgres'
    user: str = 'postgres'
    password: str = 'password'
    connection_timeout: int = 10
    pool_size: int = 2
    max_overflow: int = 0
    encoding: str = 'utf-8'
    url: str = ''

    @field_validator('url')
    @classmethod
    def validate_dsn(cls, url: str | None, values: ValidationInfo) -> str:
        """Валидация URL(URI) адреса синхронного подключения к БД.

        Args:
            url: URL(URI) для синхронного подключения к БД.
            values: Входные данные модели.

        Returns:
            URL(URI) адрес для синхронного подключения к БД.
        """
        if url is None or not url:
            return '{engine}://{user}:{password}@{host}:{port}/{database}'.format(**values.data)

        return url


class TelegramBotSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file=ENV_FILE, env_prefix='TG_')

    bot_token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file=ENV_FILE,
    )

    project_name: str
    debug: bool

    max_days_since_event_for_notification: int = 2
    case_page_request_timeout_seconds: int = 20

    db: DatabaseSettings = DatabaseSettings()
    telegram_bot: TelegramBotSettings = TelegramBotSettings()
    celery: CelerySettings = CelerySettings()


settings = Settings()

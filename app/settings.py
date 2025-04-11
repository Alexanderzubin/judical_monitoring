from pathlib import Path

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / '.env'


class DatabaseSettings(BaseSettings): 
    model_config = SettingsConfigDict(
        extra='ignore', 
        env_file=ENV_FILE,
        env_prefix='DB_'
    )

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
    model_config = SettingsConfigDict(
        extra='ignore', 
        env_file=ENV_FILE,
        env_prefix='TG_'
    )

    bot_token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore', 
        env_file=ENV_FILE,
    )

    project_name: str
    debug: bool

    db: DatabaseSettings = DatabaseSettings()
    telegram_bot: TelegramBotSettings = TelegramBotSettings()


settings = Settings()

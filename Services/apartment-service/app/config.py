from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, Extra


class Config(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(
        default='postgresql://postgres:postgres@postgresql:5432/postgres',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    FRONT: str = Field(
        default='http://localhost:3000',
        env='FRONT',
        alias='FRONT'
    )

    JWT_SECRET: str = Field(
        default='JWT_SECRET',
        env='JWT_SECRET',
        alias='JWT_SECRET'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()


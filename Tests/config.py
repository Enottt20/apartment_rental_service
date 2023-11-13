from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, Extra, AmqpDsn


class Config(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(
        default='postgresql://postgres:postgres@localhost:5432/postgres',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    POLICY_SERVICE_ENTRYPOINT: str = Field(
        default='http://localhost:5100/',
        env='POLICY_SERVICE_ENTRYPOINT',
        alias='POLICY_SERVICE_ENTRYPOINT'
    )

    APARTMENT_SERVICE_ENTRYPOINT: str = Field(
        default='http://apartment-service:5002/',
        env='APARTMENT_SERVICE_ENTRYPOINT',
        alias='APARTMENT_SERVICE_ENTRYPOINT'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()


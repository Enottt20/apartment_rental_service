from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, Extra, SecretStr, FilePath


class Config(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(
        default='postgresql+asyncpg://postgres:postgres@postgresql:5432/postgres',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    default_groups_config_path: FilePath = Field(
        default='/mnt/default-groups.json',
        env='DEFAULT_GROUPS_CONFIG_PATH',
        alias='DEFAULT_GROUPS_CONFIG_PATH'
    )

    jwt_secret: SecretStr = Field(
        default='JWT_SECRET',
        env='JWT_SECRET',
        alias='JWT_SECRET'
    )

    reset_password_token_secret: SecretStr = Field(
        default='RESET_PASSWORD_TOKEN_SECRET',
        env='RESET_PASSWORD_TOKEN_SECRET',
        alias='RESET_PASSWORD_TOKEN_SECRET'
    )

    verification_token_secret: SecretStr = Field(
        default='VERIFICATION_TOKEN_SECRET',
        env='VERIFICATION_TOKEN_SECRET',
        alias='VERIFICATION_TOKEN_SECRET'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные


def load_config() -> Config:
    return Config()
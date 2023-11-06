from pydantic_settings import BaseSettings
from pydantic import Field, Extra, AmqpDsn


class Config(BaseSettings):

    SMTP_SERVER: str = Field(
        default='smtp.gmail.com',
        env='SMTP_SERVER',
        alias='SMTP_SERVER'
    )

    SMTP_PORT: int = Field(
        default='587',
        env='SMTP_PORT',
        alias='SMTP_PORT'
    )

    EMAIL_LOGIN: str = Field(
        default='EMAIL_LOGIN',
        env='EMAIL_LOGIN',
        alias='EMAIL_LOGIN'
    )

    EMAIL_PASSWORD: str = Field(
        default='EMAIL_PASSWORD',
        env='EMAIL_PASSWORD',
        alias='EMAIL_PASSWORD'
    )

    RABBITMQ_DSN: AmqpDsn = Field(
        default='amqp://guest:guest@localhost//',
        env='RABBITMQ_DSN',
        alias='RABBITMQ_DSN'
    )

    QUEUE_NAME: str = Field(
        default='notification',
        env='QUEUE_NAME',
        alias='QUEUE_NAME'
    )


    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()


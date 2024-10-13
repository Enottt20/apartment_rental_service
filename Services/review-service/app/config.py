from pydantic_settings import BaseSettings
from pydantic import Field, Extra, MongoDsn, AmqpDsn


class Config(BaseSettings):
    mongo_dsn: MongoDsn = Field(
        default='mongodb://mongo:mongo@mongo:27017/mongo',
        env='MONGO_DSN',
        alias='MONGO_DSN'
    )

    FRONT: str = Field(
        default='http://localhost:3000',
        env='FRONT',
        alias='FRONT'
    )

    APARTMENT_SERVICE_ENTRYPOINT: str = Field(
        default='http://apartment-service:5002/',
        env='APARTMENT_SERVICE_ENTRYPOINT',
        alias='APARTMENT_SERVICE_ENTRYPOINT'
    )

    RABBITMQ_DSN: AmqpDsn = Field(
        default='amqp://guest:guest@rabbitmq//',
        env='RABBITMQ_DSN',
        alias='RABBITMQ_DSN'
    )

    QUEUE_REVIEW_NAME: str = Field(
        default='notification publish review',
        env='QUEUE_REVIEW_NAME',
        alias='QUEUE_REVIEW_NAME'
    )

    EXCHANGE_NAME: str = Field(
        default='notification',
        env='EXCHANGE_NAME',
        alias='EXCHANGE_NAME'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()


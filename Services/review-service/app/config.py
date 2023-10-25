from pydantic_settings import BaseSettings
from pydantic import Field, Extra, MongoDsn


class Config(BaseSettings):
    mongo_dsn: MongoDsn = Field(
        default='mongodb://mongo:mongo@mongodb:27017/mongo',
        env='MONGO_DSN',
        alias='MONGO_DSN'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()


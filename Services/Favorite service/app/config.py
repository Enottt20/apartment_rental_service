from pydantic_settings import BaseSettings

class Config(BaseSettings):
    POSTGRES_DSN: str = "postgresql://postgres:1111@postgresql:5432/postgres"

    class Config:
        env_file = ".env"  # Указываем имя файла .env

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()


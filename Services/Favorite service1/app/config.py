from pydantic import BaseSettings, PostgresDsn, Field

class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default='postgresql://postgres:1111@localhost/apartment_rental',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )
    int_example: int = Field(
        default=5,
        env='INT_EXAMPLE',
        alias='INT_EXAMPLE'
    )

    bool_example: bool = Field(
        default=False,
        env='BOOL_EXAMPLE',
        alias='BOOL_EXAMPLE'
    )

    class Config:
        env_file = ".env"


# app = FastAPI()
#
# # Настройки подключения к PostgreSQL
# DATABASE_URL = "postgresql://username:password@localhost/dbname"
#
# # Создание SQLAlchemy Engine
# engine = create_engine(DATABASE_URL)
#
# # Создание сессии SQLAlchemy
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # Создание асинхронного подключения к PostgreSQL
# async def create_pg_pool():
#     return await asyncpg.create_pool(DATABASE_URL)
#
# pg_pool = asyncio.get_event_loop().run_until_complete(create_pg_pool())


# Base = declarative_base()
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)
#
# Base.metadata.create_all(bind=engine)



def load_config() -> Config:
    return Config()
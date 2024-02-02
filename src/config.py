from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Database_settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    PGPORT: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")


class Database_utils:
    def __init__(self):
        self.settings = Database_settings()

    def get_async_url(self) -> str:
        return (f'postgresql+asyncpg://{self.settings.POSTGRES_USER}:{self.settings.POSTGRES_PASSWORD}'
                f'@{self.settings.POSTGRES_HOST}:{self.settings.PGPORT}/{self.settings.POSTGRES_DB}')


async_url = Database_utils().get_async_url()
async_engine = create_async_engine(async_url, echo=True)
Session = async_sessionmaker(bind=async_engine)
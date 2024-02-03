from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class MainSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file=".env")



class Database_settings(MainSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    PGPORT: str
    POSTGRES_PASSWORD: str


class JWT_settings(MainSettings):
    ISS: str
    SUB: str
    ACCESS_TOKEN_EXP_TIME: int
    REFRESH_TOKEN_EXP_TIME: int
    SECRET_KEY: str
    ALGORITHM: str


class Database_utils:
    def __init__(self):
        self.settings = Database_settings()

    def get_async_url(self) -> str:
        return (f'postgresql+asyncpg://{self.settings.POSTGRES_USER}:{self.settings.POSTGRES_PASSWORD}'
                f'@{self.settings.POSTGRES_HOST}:{self.settings.PGPORT}/{self.settings.POSTGRES_DB}')


async_url = Database_utils().get_async_url()
async_engine = create_async_engine(async_url, echo=True)
Session = async_sessionmaker(bind=async_engine)

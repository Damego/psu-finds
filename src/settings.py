from functools import cached_property
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJTWT(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"

    @cached_property
    def PRIVATE_KEY(self) -> str:
        return self.PRIVATE_KEY_PATH.read_text()

    @cached_property
    def PUBLIC_KEY(self) -> str:
        return self.PUBLIC_KEY_PATH.read_text()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT: str
    S3_BUCKET: str

    auth_jwt: AuthJTWT = AuthJTWT()

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()

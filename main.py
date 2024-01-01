from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.templating import Jinja2Templates


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/admin_db"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30_000
    model_config = SettingsConfigDict(env_file=".env")
    SECRET_KEY: str = 'asckjasncksnacjksanc234lm32n'
    templates: Jinja2Templates = Jinja2Templates(directory="templates")
    BASE_URL: str = "http://localhost:8000"
    USE_NGROK: bool = True


settings = Settings()

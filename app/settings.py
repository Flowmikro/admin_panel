import os
from pydantic_settings import BaseSettings
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str = str(os.getenv("DATABASE_URL"))
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET_KEY: str = str(os.getenv("SECRET_KE"))
    templates: Jinja2Templates = Jinja2Templates(directory="templates")


settings = Settings()

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

# print("env " ,os.getenv('DATABASE_HOSTNAME'))

class Settings(BaseSettings):
    database_hostname: str
    database_dbname: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
# print(settings.dict())

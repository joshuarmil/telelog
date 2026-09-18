import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    database_url: PostgresDsn
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()

db_string = str(settings.database_url)
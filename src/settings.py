from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str
    cors_allow_origin: str
    environment: str = 'development'

settings = Settings()
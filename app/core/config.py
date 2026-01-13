from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Instancia de configuración
settings = Settings()

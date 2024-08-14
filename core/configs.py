# Arquivo responsável pelas configurações gerais que vamos utilizar no projeto

from typing import List, ClassVar
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):

    # Configurações gerais usadas na aplicação
    
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://gabriel-caetano:python@localhost:5432/course"
    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()






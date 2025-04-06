from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Union
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Content_Creator_Assistant"
    ASYNC_DATABASE_URL: str = Field(env="ASYNC_DATABASE_URL")
    DATABASE_URL: str = Field(env="DATABASE_URL")
    TAVILY_SEARCH_API_KEY: str = Field(env="TAVILY_SEARCH_API_KEY")
    OPENAI_API_KEY: str  = Field(env="OPENAI_API_KEY")
    ALLOWED_HOSTS: Union[str, List[str]] = Field(..., env="ALLOWED_HOSTS")
    OPENAI_MODEL: str = "gpt-4o-mini"
    MINIO_ENDPOINT: str = Field(env="MINIO_ENDPOINT")
    AWS_ACCESS_KEY_ID: str = Field(env='AWS_ACCESS_KEY_ID') 
    AWS_SECRET_ACCESS_KEY: str = Field(env='AWS_SECRET_ACCESS_KEY')
    MINIO_BUCKET_NAME: str = Field(env='MINIO_BUCKET_NAME') 

    class Config():
        env_file = ".env"
        
@lru_cache
def get_settings() -> Settings:
    return Settings()
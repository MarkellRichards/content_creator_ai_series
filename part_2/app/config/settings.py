from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TAVILY_SEARCH_API_KEY: str = Field(env="TAVILY_SEARCH_API_KEY")
    OPENAI_API_KEY: str  = Field(env="OPENAI_API_KEY")
    
    class Config():
        env_file = ".env"
        
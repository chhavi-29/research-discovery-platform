from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Research Discovery Platform API"

    SEMANTIC_SCHOLAR_API_KEY: str = ""
    SEMANTIC_SCHOLAR_BASE_URL: str = "https://api.semanticscholar.org/graph/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
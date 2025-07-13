from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    max_chunk_tokens: int = 1200

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

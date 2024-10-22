from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Social media manager API"
    DATABASE_URL: str | None = "sqlite:///./social_media_manager.db"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_AI_API_KEY: str
    SECRET_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

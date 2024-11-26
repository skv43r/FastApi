from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Worldof123@postgres:5432/Users"
    ECHO_SQL: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
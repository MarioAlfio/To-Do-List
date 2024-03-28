from pydantic_settings import BaseSettings

class Settings(BaseSettings):
     DATABASE_HOST: str
     DATABASE_NAME: str
     DATABASE_USER: str
     DATABASE_PASSWORD: str
     DATABASE_PORT: int
     app_name: str = "AI DB"
     OPENAI_API_KEY: str

class Config:
    env_file = ".env"
    extra = "ignore"

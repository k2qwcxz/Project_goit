from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://project_goit:project_goit@localhost:5432/project_goit"
    SECRET_KEY: str = "s9EzdYvgLZzJ8hnbcdFqpIrtUk2YeWkJdOETU0Rt8Xp259GttG"
    ALGORITHM: str = "HS256"
    CLOUDINARY_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
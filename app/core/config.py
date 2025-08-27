from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # This will automatically look for a GOOGLE_API_KEY in your .env file
    GOOGLE_API_KEY: str

    class Config:
        env_file = ".env"

# Create an instance of the settings
settings = Settings()
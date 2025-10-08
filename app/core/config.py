from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    This is like a configuration file for your app.
    """
    # Project info
    PROJECT_NAME: str = "Production Monitoring API"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database connection string
    DATABASE_URL: str
    
    # Security settings for JWT tokens
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - which websites can access your API
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    @property
    def origins_list(self) -> List[str]:
        """Convert comma-separated string to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a single instance to use throughout the app
settings = Settings()
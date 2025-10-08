from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Project info
    PROJECT_NAME: str = "Production Monitoring API"
    API_V1_PREFIX: str = "/api/v1"
    
    # Authentication Database
    AUTH_DATABASE_URL: str
    # AUTH_DB_HOST: str = "localhost"
    # AUTH_DB_PORT: int = 5433
    # AUTH_DB_USER: str
    # AUTH_DB_PASSWORD: str
    # AUTH_DB_NAME: str = "auth_db"
    
    # Production Database
    PROD_DATABASE_URL: str
    # PROD_DB_HOST: str = "localhost"
    # PROD_DB_PORT: int = 5432
    # PROD_DB_USER: str
    # PROD_DB_PASSWORD: str
    # PROD_DB_NAME: str = "production_monitoring"
    
    # Security settings for JWT tokens
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    @property
    def origins_list(self) -> List[str]:
        """Convert comma-separated string to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a single instance
settings = Settings()
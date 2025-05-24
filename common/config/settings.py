import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # App settings
    APP_NAME: str = "Hyperlocal Marketplace"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Database settings
    DB_TYPE: str = os.getenv("DB_TYPE", "mysql")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "hyperlocal_marketplace")
    DB_PATH: str = os.getenv("DB_PATH", "/workspace/localmarket/hyperlocal.db")
    
    # Database URL
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """
        Get async database URL for SQLAlchemy
        """
        if self.DB_TYPE.lower() == "sqlite":
            return f"sqlite+aiosqlite:///{self.DB_PATH}"
        else:
            return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Firebase settings
    FIREBASE_CREDENTIALS: str = os.getenv("FIREBASE_CREDENTIALS", "")
    
    # AWS S3 settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "hyperlocal-marketplace")
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    # Service ports
    USER_SERVICE_PORT: int = int(os.getenv("USER_SERVICE_PORT", "8001"))
    SELLER_SERVICE_PORT: int = int(os.getenv("SELLER_SERVICE_PORT", "8002"))
    CUSTOMER_SERVICE_PORT: int = int(os.getenv("CUSTOMER_SERVICE_PORT", "8003"))
    CATALOG_SERVICE_PORT: int = int(os.getenv("CATALOG_SERVICE_PORT", "8004"))
    ADMIN_SERVICE_PORT: int = int(os.getenv("ADMIN_SERVICE_PORT", "8005"))
    
    # Service URLs
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", f"http://localhost:{USER_SERVICE_PORT}")
    SELLER_SERVICE_URL: str = os.getenv("SELLER_SERVICE_URL", f"http://localhost:{SELLER_SERVICE_PORT}")
    CUSTOMER_SERVICE_URL: str = os.getenv("CUSTOMER_SERVICE_URL", f"http://localhost:{CUSTOMER_SERVICE_PORT}")
    CATALOG_SERVICE_URL: str = os.getenv("CATALOG_SERVICE_URL", f"http://localhost:{CATALOG_SERVICE_PORT}")
    ADMIN_SERVICE_URL: str = os.getenv("ADMIN_SERVICE_URL", f"http://localhost:{ADMIN_SERVICE_PORT}")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings object
_settings = None

def get_settings() -> Settings:
    """
    Get settings singleton
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

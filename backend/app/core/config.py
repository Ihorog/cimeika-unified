"""
Configuration management for CIMEIKA API
Centralized environment variable handling and application settings
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables
    """
    
    # Environment
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # API Configuration
    API_VERSION: str = "0.1.0"
    API_TITLE: str = "CIMEIKA API"
    API_DESCRIPTION: str = "Центральна екосистема проєкту Cimeika - Family Management Platform"
    
    # Server
    BACKEND_HOST: str = os.getenv('BACKEND_HOST', '0.0.0.0')
    BACKEND_PORT: int = int(os.getenv('BACKEND_PORT', '8000'))
    FASTAPI_RELOAD: bool = os.getenv('FASTAPI_RELOAD', '1') == '1'
    
    # CORS
    CORS_ORIGINS: list = os.getenv(
        'CORS_ORIGINS', 
        'http://localhost:3000,http://localhost:5173'
    ).split(',')
    
    # Database
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'cimeika')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'cimeika_user')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'change_me_in_production')
    
    # Optional: Monitoring
    SENTRY_DSN: Optional[str] = os.getenv('SENTRY_DSN', None)
    
    # Optional: AI Integration
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY', None)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY', None)
    
    # Optional: Redis (for rate limiting, caching)
    REDIS_HOST: Optional[str] = os.getenv('REDIS_HOST', None)
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD', None)
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'change_me_in_production')
    
    @property
    def database_url(self) -> str:
        """
        Construct PostgreSQL database URL
        
        Returns:
            str: SQLAlchemy-compatible database URL
        """
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == 'production'
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == 'development'
    
    def validate(self) -> dict:
        """
        Validate configuration and return status
        
        Returns:
            dict: Validation results with warnings and errors
        """
        warnings = []
        errors = []
        
        # Check for default passwords in production
        if self.is_production:
            if self.POSTGRES_PASSWORD == 'change_me_in_production':
                errors.append("POSTGRES_PASSWORD is using default value in production")
            if self.SECRET_KEY == 'change_me_in_production':
                errors.append("SECRET_KEY is using default value in production")
        
        # Check for CORS wildcard in production
        if self.is_production and '*' in self.CORS_ORIGINS:
            errors.append("CORS_ORIGINS should not use wildcard (*) in production")
        
        # Warn about missing optional services
        if not self.SENTRY_DSN:
            warnings.append("SENTRY_DSN not configured (monitoring disabled)")
        
        if not self.OPENAI_API_KEY and not self.ANTHROPIC_API_KEY:
            warnings.append("No AI API keys configured (AI features disabled)")
        
        return {
            "valid": len(errors) == 0,
            "warnings": warnings,
            "errors": errors
        }


# Global settings instance
settings = Settings()
